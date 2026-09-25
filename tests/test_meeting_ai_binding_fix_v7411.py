from pathlib import Path


def test_interactive_meeting_uses_dedicated_ai_endpoint_not_generic_chat():
    html=Path("templates/real_meeting_attendance.html").read_text(encoding="utf-8")
    start=html.index("async function runInteractiveConversation")
    end=html.index("document.getElementById('askAdam')")
    block=html[start:end]
    assert "/api/personal-assistant/meeting-conversation/ask" in block
    assert "/api/chat" not in block
    assert "owner_approved" in block
    assert "meeting_context" in block
    assert "meetingConversationHistory" in block


def test_dedicated_meeting_ai_route_calls_provider_and_preserves_gate():
    app=Path("app.py").read_text(encoding="utf-8")
    assert 'VERSION = "v8.1.0.1"' in app
    assert '@app.route("/api/personal-assistant/meeting-conversation/ask", methods=["POST"])' in app
    assert 'if not bool(body.get("owner_approved"))' in app
    assert 'answer = call_ai(prompt, "English", max_tokens=1200).strip()' in app
    assert '"ai_provider_bound": True' in app
    assert '"external_action_executed": False' in app


def test_ai_binding_self_test_route_present():
    app=Path("app.py").read_text(encoding="utf-8")
    assert '/api/personal-assistant/meeting-conversation/ai-binding-self-test' in app
    assert '"generic_chat_intent_routing_bypassed": True' in app
