from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
APP=(ROOT/'app.py').read_text(encoding='utf-8')
HTML=(ROOT/'templates'/'real_meeting_attendance.html').read_text(encoding='utf-8')

def test_version():
    assert 'VERSION = "v8.3.1.1"' in APP

def test_representative_approval_arms_auto_response():
    assert "const representativeArmed=representativeMode && document.getElementById('representativeApproved').checked" in HTML
    assert "document.getElementById('autoRespond').checked=checked" in HTML
    assert 'representative auto-response armed' in HTML

def test_adam_wake_name_still_triggers():
    assert r'/\badam\b|آدم|ادم/i.test(q)' in HTML
    assert 'runInteractiveConversation(q)' in HTML

def test_representative_session_approval_reaches_ai_endpoint():
    assert 'const sessionApproved=representativeApproved||activeParticipantApproved' in HTML
    assert 'owner_approved:sessionApproved' in HTML

def test_active_participant_gate_preserved():
    assert "const activeParticipantApproved=!representativeMode && document.getElementById('conversationApproved').checked" in HTML

def test_consequential_boundary_copy_preserved():
    assert 'consequential actions still require their own separate owner approval' in HTML
    assert 'cannot approve costs, variations, contractual changes' in HTML
