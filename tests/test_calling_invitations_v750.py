from pathlib import Path
from adam_core.calling_invitations import build_status, prepare_invitation, prepare_call, self_test


def test_v750_calling_invitations_governance_boundary():
    result = self_test()
    assert result["ok"] is True
    assert result["invitation_owner_gate_verified"] is True
    assert result["call_owner_gate_verified"] is True
    assert result["autonomous_call_not_falsely_claimed_verified"] is True
    assert result["external_network_accessed"] is False
    assert result["external_action_executed"] is False


def test_v750_runtime_routes_and_main_navigation_are_present():
    app = Path("app.py").read_text(encoding="utf-8")
    index = Path("templates/index.html").read_text(encoding="utf-8")
    page = Path("templates/calling_invitations.html").read_text(encoding="utf-8")
    assert 'VERSION = "v8.1.0.1"' in app
    assert '/calling-invitations' in app
    assert '/api/personal-assistant/calling-invitations/status' in app
    assert '/api/personal-assistant/calling-invitations/preview' in app
    assert '/api/personal-assistant/calling-invitations/self-test' in app
    assert 'href="/calling-invitations">Calling & Invitations' in index
    assert 'Owner Approval — create and send this invitation' in page
    assert 'Owner Approval — open device dialer' in page
    assert 'does <b>not</b> claim autonomous PSTN/VoIP calling' in page
