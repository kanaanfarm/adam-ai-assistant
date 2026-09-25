from pathlib import Path
import ast, re, uuid

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / 'app.py').read_text(encoding='utf-8')
HTML = (ROOT / 'templates' / 'real_meeting_attendance.html').read_text(encoding='utf-8')


def _load_function(name, extra=None):
    tree = ast.parse(APP)
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
    mod = ast.Module(body=[node], type_ignores=[])
    ns = {'re': re, 'uuid': uuid, '_MEETING_QUESTION_COVERAGE_MAX_ITEMS': 160}
    if extra:
        ns.update(extra)
    exec(compile(mod, '<helper>', 'exec'), ns)
    return ns[name]


def test_version_and_question_coverage_monitor_present():
    assert 'VERSION = "v8.3.2.1"' in APP
    assert 'id="questionCoverage"' in HTML
    assert 'Question Coverage Monitor — every direct question accounted for' in HTML
    assert '_MEETING_QUESTION_COVERAGE' in APP


def test_direct_question_detection_examples():
    f = _load_function('_meeting_question_is_direct')
    assert f('Adam, can a dirty AHU filter reduce airflow?') is True
    assert f('What do you recommend next') is True
    assert f('آدم شو رأيك بهيدا التغيير؟') is True
    assert f('Hello everyone') is False


def test_coverage_upsert_reuses_question_id_for_retry():
    f = _load_function('_meeting_coverage_upsert')
    rows = []
    qid, rec = f(rows, question_id='q-1', question='Adam, what is the status?', direct_question=True, state='Processing')
    assert qid == 'q-1' and len(rows) == 1 and rec['state'] == 'Processing'
    qid2, rec2 = f(rows, question_id='q-1', question='Adam, what is the status?', direct_question=True, state='Answered', answer='It remains open.', topic='General')
    assert qid2 == 'q-1' and len(rows) == 1
    assert rec2['state'] == 'Answered' and rec2['answer'] == 'It remains open.'


def test_direct_questions_cannot_be_silently_ignored():
    assert 'QUESTION COVERAGE ASSURANCE' in APP
    assert 'Do NOT return IGNORE' in APP
    assert 'if direct_question and ignore_requested:' in APP
    assert 'Clarification requested' in APP


def test_frontend_uses_one_bounded_retry_and_keeps_same_question_id():
    assert 'temporary response failure — Adam is retrying once' in HTML
    assert 'attempt<1' in HTML
    assert 'questionId,attempt:attempt+1' in HTML
    assert 'question_id:questionId' in HTML
    assert 'direct_question:directQuestion' in HTML


def test_failed_question_can_be_repeated_without_success_dedupe_lock():
    trigger = HTML.split('async function triggerAutomaticConversation(q){', 1)[1].split('function scheduleAutomaticConversationAfterEndOfTurn', 1)[0]
    # Last-auto dedupe timestamp is updated only after runInteractiveConversation reports handled.
    assert 'if(handled){meetingLastAutoQuestion=key;meetingLastAutoAt=Date.now();}' in trigger


def test_report_includes_question_coverage_and_unanswered_items():
    assert 'QUESTION COVERAGE / UNANSWERED ITEMS' in APP
    assert 'DIRECT-QUESTION COVERAGE RECORD' in APP
    assert 'unanswered_question_count' in APP
    assert 'question_coverage_included' in APP
    assert 'QUESTION COVERAGE / UNANSWERED ITEMS' in APP.split('section_names = {',1)[1]


def test_clear_preserves_coverage_but_end_meeting_resets_it():
    clear_handler = HTML.split("document.getElementById('clear').onclick",1)[1].split("document.getElementById('endMeeting').onclick",1)[0]
    assert "questionCoverage').value=''" not in clear_handler
    end_handler = HTML.split("document.getElementById('endMeeting').onclick",1)[1].split("document.getElementById('analyze').onclick",1)[0]
    assert "questionCoverage').value=''" in end_handler
    assert '_MEETING_QUESTION_COVERAGE.pop(sid, None)' in APP


def test_existing_safety_boundaries_preserved():
    assert 'must NOT approve variations' in APP
    assert 'separate owner approval mechanism' in APP
    assert 'Never pretend to be the owner or a human' in APP
    assert 'external_action_executed' in APP
