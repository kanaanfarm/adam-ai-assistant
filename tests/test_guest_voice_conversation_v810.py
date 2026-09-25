from pathlib import Path

from adam_core.guest_voice_session import GuestSessionStore, self_test


ROOT = Path(__file__).resolve().parents[1]


def test_v810_guest_session_core_is_owner_approved_ephemeral_and_safe():
    result = self_test()
    assert result["ok"] is True
    assert result["owner_approval_gate_verified"] is True
    assert result["consequential_action_blocked_verified"] is True
    assert result["private_owner_data_blocked_verified"] is True
    assert result["external_action_executed"] is False
    assert result["external_network_accessed"] is False


def test_v810_store_lifecycle_and_private_request_blocking():
    store = GuestSessionStore()
    session = store.create("Ahmed", "Adam product questions", 30, True)
    assert session.public()["active"] is True
    blocked = store.classify_question(session, "What is the owner's phone number?")
    assert blocked["status"] == "owner_approval_required"
    assert blocked["external_action_executed"] is False
    assert store.close(session.token) is True
    assert session.public()["active"] is False


def test_v810_ui_has_natural_turn_detection_and_barge_in():
    guest = (ROOT / "templates" / "guest_voice_session.html").read_text(encoding="utf-8")
    main = (ROOT / "templates" / "index.html").read_text(encoding="utf-8")
    stock = (ROOT / "templates" / "stock.html").read_text(encoding="utf-8")
    for html in (guest, main, stock):
        assert "continuous=true" in html
        assert "3000" in html
    assert "Finish Speaking" in guest
    assert "Stop Listening" in guest
    assert "cancelAdamVoice();clearTimeout(silenceTimer)" in guest
    assert "if(wantContinuous)startRecognition()" in guest


def test_v810_routes_and_version_are_present():
    app = (ROOT / "app.py").read_text(encoding="utf-8")
    assert 'VERSION = "v8.1.0.1"' in app
    for route in [
        '"/guest-voice"',
        '"/guest/<token>"',
        '"/api/personal-assistant/guest-voice/sessions"',
        '"/api/personal-assistant/guest-voice/self-test"',
    ]:
        assert route in app
    assert "GUEST_VOICE_SESSIONS = GuestSessionStore()" in app
    assert "private_owner_data_returned" in app


def test_v810_flask_session_creation_and_safe_action_block(monkeypatch):
    import app as adam_app

    monkeypatch.setattr(adam_app, "audit", lambda *_args, **_kwargs: None)
    client = adam_app.app.test_client()

    denied = client.post("/api/personal-assistant/guest-voice/sessions", json={
        "guest_name": "Ahmed", "topic": "Product questions", "duration_minutes": 30,
        "owner_approved": False,
    })
    assert denied.status_code == 403
    assert denied.get_json()["status"] == "owner_approval_required"

    created = client.post("/api/personal-assistant/guest-voice/sessions", json={
        "guest_name": "Ahmed", "topic": "Product questions", "duration_minutes": 30,
        "owner_approved": True,
    })
    payload = created.get_json()
    assert created.status_code == 200 and payload["ok"] is True
    assert payload["guest_path"].startswith("/guest/")
    assert payload["owner_private_data_available"] is False

    token = payload["token"]
    blocked = client.post(
        f"/api/personal-assistant/guest-voice/sessions/{token}/ask",
        json={"question": "Send an email to the owner"},
    )
    blocked_payload = blocked.get_json()
    assert blocked_payload["status"] == "owner_approval_required"
    assert blocked_payload["external_action_executed"] is False

    closed = client.post(f"/api/personal-assistant/guest-voice/sessions/{token}/close", json={})
    assert closed.get_json()["status"] == "guest_voice_session_closed"
    unavailable = client.get(f"/api/personal-assistant/guest-voice/sessions/{token}")
    assert unavailable.get_json()["active"] is False
