from pathlib import Path

from adam_core.production_commercial_release import (
    RELEASE_CONTROLS,
    build_release_manifest,
    build_status,
    certify_release,
    select_mode,
    self_test,
)


def test_v800_modes_are_explicit_and_isolated():
    personal = select_mode("personal_operation")
    buyer = select_mode("buyer_presentation")
    invalid = select_mode("unknown")
    assert personal["ok"] and personal["owner_approval_required_for_external_actions"]
    assert buyer["ok"] and buyer["synthetic_only"]
    assert buyer["private_owner_data_allowed"] is False
    assert buyer["production_connectors_allowed_when_configured"] is False
    assert invalid["ok"] is False and invalid["external_action_executed"] is False


def test_v800_release_manifest_and_certification_preserve_safety():
    manifest = build_release_manifest()
    good = certify_release({name: True for name in RELEASE_CONTROLS})
    missing = certify_release({name: True for name in RELEASE_CONTROLS if name != "operating_modes_isolated"})
    assert manifest["release"] == "v8.1.0" and manifest["single_codebase"] is True
    assert manifest["automatic_connector_activation"] is False
    assert good["ok"] and good["status"] == "production_commercial_release_certified"
    assert good["owner_approval_preserved"] and good["live_trading_blocked"]
    assert missing["ok"] is False and "operating_modes_isolated" in missing["missing_controls"]


def test_v800_self_test_and_runtime_surface_are_safe():
    result = self_test()
    assert result["ok"] is True
    assert result["single_codebase_verified"] is True
    assert result["dual_mode_selection_verified"] is True
    assert result["operating_modes_isolated_verified"] is True
    assert result["automatic_activation_blocked_verified"] is True
    assert result["external_network_accessed"] is False
    assert result["external_action_executed"] is False
    assert build_status()["release"] == "v8.1.0"
    app = Path("app.py").read_text()
    html = Path("templates/production_commercial_release.html").read_text()
    assert 'VERSION = "v8.1.0.1"' in app
    assert "/api/personal-assistant/production-commercial-release/self-test" in app
    assert "Run Final Release Certification" in html
