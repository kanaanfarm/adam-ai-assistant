from adam_core.meeting_conversation_agent import authorize_speaking


def test_meeting_identity_only_first_turn():
    first = authorize_speaking({"response":"Welcome to the meeting.","owner_approved":True,"identity_already_declared":False})
    second = authorize_speaking({"response":"Here is the next point.","owner_approved":True,"identity_already_declared":True})
    assert first["response"].lower().startswith("i am adam")
    assert not second["response"].lower().startswith("i am adam")


def test_guest_prompt_has_once_only_rule():
    text = open("app.py", encoding="utf-8").read()
    assert "You already introduced yourself earlier in this session" in text
    assert "Do NOT repeat your name, AI identity, role, or introduction" in text
