from adam_core.buyer_integrated_demo import preview_integrated_demo, execute_integrated_demo, public_manifest
from adam_core.buyer_integrated_demo_boundary import build_buyer_integrated_demo_manifest, buyer_integrated_demo_is_privacy_safe, buyer_integrated_demo_self_test

def test_manifest_privacy_safe():
    p=build_buyer_integrated_demo_manifest("v5.0.0")
    assert buyer_integrated_demo_is_privacy_safe(p)
    assert p["integrated_buyer_demo"]["capabilities"]["buyer_ready_integrated_agent_demo"] is True

def test_owner_gate_and_approved_execution():
    assert execute_integrated_demo(owner_approved=False)["status"]=="approval_required"
    r=execute_integrated_demo(owner_approved=True)
    assert r["status"]=="buyer_demo_completed" and r["audit_receipt_generated"]

def test_self_test_is_synthetic_and_safe():
    r=buyer_integrated_demo_self_test()
    assert r["ok"] and r["approved_integrated_demo_completed"] and not r["external_network_accessed"]
