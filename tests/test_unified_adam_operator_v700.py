from pathlib import Path
from adam_core.unified_adam_operator import build_unified_operator_plan, self_test


def test_v700_self_test_is_synthetic_and_governed():
    r = self_test()
    assert r["ok"] is True
    assert r["unified_capability_routing_verified"] is True
    assert r["owner_approval_gate_verified"] is True
    assert r["text_confirmation_gate_verified"] is True
    assert r["approved_governed_handoff_verified"] is True
    assert r["specialist_boundary_preservation_verified"] is True
    assert r["live_trading_block_verified"] is True
    assert r["sensitive_content_rejection_verified"] is True
    assert r["audit_chain_verified"] is True
    assert r["real_action_executed"] is False
    assert r["external_network_accessed"] is False


def test_v700_interactive_safe_example_requires_owner_approval():
    r = build_unified_operator_plan(
        "Review the attached site photo, open the contractor portal, send an email and WhatsApp message, then analyze NVDA before any trade.",
        False,
        False,
    )
    assert r["status"] == "owner_approval_required"
    assert r["owner_approved"] is False
    assert r["text_confirmed"] is False
    assert r["ready_for_governed_execution_handoff"] is False
    assert r["execution_performed"] is False
    assert r["external_network_accessed"] is False
    assert r["live_trading_blocked"] is True
    assert {"vision_attachments", "browser_computer", "email", "whatsapp", "stock_intelligence"}.issubset(set(r["capabilities"]))


def test_v700_app_wiring_and_acquisition_card():
    app = Path("app.py").read_text(encoding="utf-8")
    acq = Path("templates/acquisition.html").read_text(encoding="utf-8")
    assert 'VERSION = "v8.1.0.1"' in app
    assert '/unified-adam-operator' in app
    assert '/api/personal-assistant/unified-operator/review' in app
    assert '/api/personal-assistant/unified-operator/self-test' in app
    assert 'Unified Adam Operator — v7.0' in acq
    assert '/unified-adam-operator' in acq
    assert acq.index('Unified Adam Operator — v7.0') < acq.index('</body>')
