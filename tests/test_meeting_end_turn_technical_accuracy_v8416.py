from pathlib import Path
import ast
import re

ROOT = Path(__file__).resolve().parents[1]
APP_TEXT = (ROOT / 'app.py').read_text(encoding='utf-8')
HTML = (ROOT / 'templates' / 'real_meeting_attendance.html').read_text(encoding='utf-8')


def _cleaner(form=None):
    tree = ast.parse(APP_TEXT)
    outer = next(n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == 'real_meeting_attendance_transcribe_v831')
    inner = next(n for n in outer.body if isinstance(n, ast.FunctionDef) and n.name == 'clean_provider_text')
    module = ast.Module(body=[inner], type_ignores=[])
    ast.fix_missing_locations(module)
    class Req:
        pass
    request = Req()
    request.form = form or {}
    ns = {'re': re, 'request': request}
    exec(compile(module, str(ROOT / 'app.py'), 'exec'), ns, ns)
    return ns['clean_provider_text']


def test_version_bumped():
    assert 'VERSION = "v8.4.1.6"' in APP_TEXT


def test_natural_pause_boundary_is_less_aggressive():
    assert 'MEETING_END_OF_TURN_SILENCE_MS=4200' in HTML
    assert 'MEETING_FINAL_TURN_MERGE_GRACE_MS=1500' in HTML
    assert 'MEETING_FINAL_TURN_MAX_WAIT_MS=10000' in HTML
    assert 'MEETING_CONTINUATION_SPEECH_HOLD_MS=900' in HTML


def test_final_microphone_turn_is_buffered_not_immediately_dispatched():
    assert "if(options.finalTurn&&options.source==='typed')return await dispatchCompletedParticipantTurn" in HTML
    assert "scheduleAutomaticConversationAfterEndOfTurn(q,stableQuestionId,{finalBoundary:!!options.finalTurn})" in HTML
    assert "source:'microphone_server'" in HTML
    assert 'participantContinuation' in HTML
    assert 'requiredStability=finalBoundary?MEETING_FINAL_TURN_MERGE_GRACE_MS' in HTML


def test_fragment_continuations_reuse_one_stable_question_id():
    assert "const pendingTurnId=(meetingPendingAutoParts.length&&meetingPendingAutoQuestionId)?meetingPendingAutoQuestionId:'';" in HTML
    assert 'options.questionId||pendingTurnId||newMeetingQuestionId()' in HTML


def test_low_information_noise_does_not_inflate_focus_counters():
    assert "looksLikeLowInformationNoise(q)&&!wakeNameDetected(q)&&!meetingAwaitingClarification" in HTML
    assert 'transient low-information speech ignored' in HTML


def test_technical_context_is_sent_with_server_transcription():
    assert "fd.append('technical_context'" in HTML
    assert "transcript.value.slice(-1200)" in HTML


def test_flow_floor_repair_is_conservative():
    assert 'accepted_technical_context_repair' in APP_TEXT
    assert 'contextual_flow_floor_guard' in APP_TEXT
    assert r'floor\s+(?:is\s+)?unchanged' in APP_TEXT
    block = APP_TEXT[APP_TEXT.index('before_context_repair'):APP_TEXT.index('return raw.strip(), clean_status')]
    assert r'floor\s+level' not in block


def test_real_cleaner_repairs_hydronic_flow_confusion():
    cleaner = _cleaner({'capture_ms': '12000', 'technical_context': 'MEP chilled water hydraulic pipe sizing 100 mm 125 mm'})
    text, status = cleaner('Regarding the same chilled water line, the contractor says the floor is unchanged and they want to proceed with 100 mm.')
    assert 'the flow is unchanged' in text.lower()
    assert status == 'accepted_technical_context_repair'


def test_legitimate_floor_level_phrase_is_not_rewritten():
    cleaner = _cleaner({'capture_ms': '8000', 'technical_context': 'MEP chilled water coordination'})
    text, status = cleaner('The chilled water pipe is coordinated and the floor level is unchanged.')
    assert 'floor level is unchanged' in text.lower()
    assert status != 'accepted_technical_context_repair'


def test_cleaner_does_not_repair_floor_without_hydronic_context():
    cleaner = _cleaner({'capture_ms': '8000', 'technical_context': 'general project meeting'})
    text, status = cleaner('The floor is unchanged from the approved drawing.')
    assert 'floor is unchanged' in text.lower()
    assert status != 'accepted_technical_context_repair'
