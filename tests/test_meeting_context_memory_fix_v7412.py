from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def test_version_and_server_session_memory_binding():
    app=(ROOT/"app.py").read_text(encoding="utf-8")
    assert 'VERSION = "v8.1.0.1"' in app
    assert '_MEETING_CONVERSATION_SESSIONS' in app
    assert 'context_memory_bound' in app
    assert '/api/personal-assistant/meeting-conversation/reset' in app
    assert '/api/personal-assistant/meeting-conversation/context-memory-self-test' in app

def test_browser_keeps_session_id_and_clear_resets_context():
    html=(ROOT/"templates"/"real_meeting_attendance.html").read_text(encoding="utf-8")
    assert 'meetingConversationSessionId' in html
    assert 'session_id:meetingConversationSessionId' in html
    assert '/api/personal-assistant/meeting-conversation/reset' in html
    assert 'meetingConversationHistory=[]' in html
