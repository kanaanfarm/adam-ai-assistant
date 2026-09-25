from pathlib import Path

from adam_core.security_privacy_certification import (
    REQUIRED_CONTROLS,
    build_status,
    certify_controls,
    privacy_safe_projection,
    self_test,
)


def test_v780_projection_never_returns_private_values():
    secrets = ["TOKEN-MARKER", "SECRET-MARKER", "owner@example.invalid", "+971500000000"]
    r = privacy_safe_projection({
        "workflow_id": "safe-id", "access_token": secrets[0], "client_secret": secrets[1],
        "contact_email": secrets[2], "contact_phone": secrets[3],
    })
    assert r["protected_field_count"] == 4
    assert r["private_values_returned"] is False and r["credentials_returned"] is False
    assert all(value not in repr(r) for value in secrets)


def test_v780_certification_requires_every_control_and_owner_approval():
    good = certify_controls({name: True for name in REQUIRED_CONTROLS})
    missing = certify_controls({name: True for name in REQUIRED_CONTROLS if name != "owner_approval_enforced"})
    assert good["ok"] is True and good["status"] == "security_privacy_certified"
    assert good["owner_approval_preserved"] is True and good["live_trading_blocked"] is True
    assert missing["ok"] is False and "owner_approval_enforced" in missing["missing_controls"]


def test_v780_self_test_and_runtime_surface_are_safe():
    result = self_test()
    assert result["ok"] is True
    assert result["permission_boundary_verified"] is True
    assert result["private_payload_redaction_verified"] is True
    assert result["memory_boundary_verified"] is True
    assert result["audit_metadata_only_verified"] is True
    assert result["external_network_accessed"] is False
    assert result["external_action_executed"] is False
    status = build_status()
    assert status["private_owner_data_required_for_certification"] is False
    app = Path("app.py").read_text()
    html = Path("templates/security_privacy_certification.html").read_text()
    assert 'VERSION = "v8.1.0.1"' in app
    assert "/api/personal-assistant/security-privacy-certification/self-test" in app
    assert "Run Safe Certification" in html
