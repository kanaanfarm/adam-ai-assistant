from pathlib import Path

from adam_core.commercial_buyer_demo_certification import (
    CERTIFICATION_CONTROLS,
    build_buyer_demo_pack,
    build_status,
    certify_demo,
    self_test,
)


def test_v790_demo_pack_is_buyer_safe_and_evidence_bounded():
    pack = build_buyer_demo_pack()
    assert pack["ok"] is True and pack["scenario_count"] == 4
    assert pack["claim_count"] == 14
    assert pack["private_owner_data_required"] is False
    assert pack["credentials_required"] is False
    assert pack["production_connectors_required"] is False
    assert pack["external_action_executed"] is False


def test_v790_certification_requires_all_controls_and_owner_gate():
    good = certify_demo({name: True for name in CERTIFICATION_CONTROLS})
    missing = certify_demo({name: True for name in CERTIFICATION_CONTROLS if name != "owner_approval_preserved"})
    assert good["ok"] is True and good["status"] == "commercial_buyer_demo_certified"
    assert good["owner_approval_preserved"] is True and good["live_trading_blocked"] is True
    assert missing["ok"] is False and "owner_approval_preserved" in missing["missing_controls"]


def test_v790_self_test_and_runtime_surface_are_safe():
    result = self_test()
    assert result["ok"] is True
    assert result["buyer_demo_pack_verified"] is True
    assert result["capability_claims_evidence_backed"] is True
    assert result["buyer_safe_redaction_verified"] is True
    assert result["production_connector_independence_verified"] is True
    assert result["external_network_accessed"] is False
    assert result["external_action_executed"] is False
    status = build_status()
    assert status["private_owner_data_required"] is False
    app = Path("app.py").read_text()
    html = Path("templates/commercial_buyer_demo_certification.html").read_text()
    assert 'VERSION = "v8.1.0.1"' in app
    assert "/api/personal-assistant/commercial-buyer-demo-certification/self-test" in app
    assert "Run Buyer-Safe Certification" in html
