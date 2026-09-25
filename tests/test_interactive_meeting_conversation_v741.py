from pathlib import Path

def test_interactive_meeting_ui_has_session_approval_and_followup():
    html=Path("templates/real_meeting_attendance.html").read_text(encoding="utf-8")
    assert "Interactive Meeting Conversation" in html
    assert "conversationApproved" in html
    assert "meetingConversationHistory" in html
    assert "Ask Adam & Speak" in html
    assert "ready for follow-up" in html

def test_interactive_meeting_auto_response_is_addressed_to_adam_and_governed():
    html=Path("templates/real_meeting_attendance.html").read_text(encoding="utf-8")
    assert "autoRespond" in html
    assert "/\\badam\\b/i" in html or "/\badam\b/i" in html
    assert "owner session approval required" in html
    assert "Do not promise, send, approve, purchase, trade, schedule, or execute external actions" in html
    app=Path("app.py").read_text(encoding="utf-8")
    assert 'VERSION = "v8.1.0.1"' in app
