from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / 'app.py').read_text(encoding='utf-8')
HTML = (ROOT / 'templates' / 'real_meeting_attendance.html').read_text(encoding='utf-8')

def test_version_and_label():
    assert 'VERSION = "v8.3.4.1"' in APP
    assert 'Professional conversation — questions / corrections / orders' in HTML

def test_correction_and_order_classifiers():
    assert 'function likelyMeetingCorrection' in HTML
    assert 'function likelyMeetingOrder' in HTML
    assert "turnKind==='correction'" in HTML
    assert "turnKind==='order'" in HTML
    assert 'response_required:responseRequired' in HTML

def test_server_requires_reply_for_non_question_interaction():
    assert 'CONVERSATIONAL TURN REQUIRED' in APP
    assert 'RESPONSE REQUIRED: this participant interaction must receive a natural reply' in APP
    assert 'elif response_required and ignore_requested:' in APP
    assert 'thanks for the correction' in APP

def test_safety_and_project_boundaries_preserved():
    route=APP.split('def meeting_conversation_ask_v7411():',1)[1]
    assert 'detect_explicit_project_mismatch' in route
    assert 'project_mismatch_filtered' in route
    assert 'must NOT approve variations' in APP
    assert 'separate owner approval mechanism' in APP

def test_wake_hold_preserved():
    assert 'if(isWakeOnly(q)){armMeetingAddressHold' in HTML
    assert 'if(isQuestionPreamble(q)){armMeetingAddressHold' in HTML
