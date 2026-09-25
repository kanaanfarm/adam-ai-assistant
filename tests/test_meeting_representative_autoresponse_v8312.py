from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
APP=(ROOT/'app.py').read_text(encoding='utf-8')
HTML=(ROOT/'templates'/'real_meeting_attendance.html').read_text(encoding='utf-8')

def test_version():
    assert 'VERSION = "v8.3.1.2"' in APP

def test_single_visible_session_approval_for_representative():
    assert 'listen/capture and act as my disclosed AI representative for this meeting session' in HTML
    assert 'representativeApprovalRow" style="display:none' in HTML
    assert "const representativeApproved=representativeMode && approved()" in HTML

def test_professional_direct_question_trigger():
    assert 'value="adam_or_question"' in HTML
    assert 'Professional representative — Adam / direct questions' in HTML
    assert 'likelyDirectQuestion(q)' in HTML
    assert 'wakeNameDetected(q)' in HTML

def test_busy_and_duplicate_suppression():
    assert 'meetingAutoResponseBusy' in HTML
    assert 'meetingLastAutoQuestion' in HTML
    assert 'now-meetingLastAutoAt<15000' in HTML

def test_stt_remains_prompt_free():
    start=APP.index('provider_data = {"model": "gpt-4o-transcribe"')
    block=APP[start:start+150]
    assert '"prompt"' not in block

def test_question_can_be_detected_inside_multiline_chunk():
    assert 'if(/[?؟]/.test(t))return true;' in HTML
    assert 't.split(/\\n+/)' in HTML

def test_consequential_boundary_preserved():
    assert 'cannot approve costs, variations, contractual changes' in HTML
    assert 'consequential actions still require their own separate owner approval' in HTML
