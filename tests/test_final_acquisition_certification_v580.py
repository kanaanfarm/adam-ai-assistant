from adam_core.final_acquisition_certification import CERTIFICATION_CHECKS, evaluate_release_candidate, certify_buyer_demo_release
from adam_core.final_acquisition_certification_boundary import build_final_acquisition_certification_manifest, final_acquisition_certification_is_privacy_safe, final_acquisition_certification_self_test

def test_boundary_and_privacy():
    p=build_final_acquisition_certification_manifest("v5.8.0")
    assert final_acquisition_certification_is_privacy_safe(p)
    c=p["final_acquisition_certification"]["capabilities"]
    assert c["real_handoff_enabled_by_acceptance_test"] is False
    assert c["automatic_buyer_handoff_allowed"] is False

def test_owner_gate_and_self_test():
    good={k:True for k in CERTIFICATION_CHECKS}
    r=certify_buyer_demo_release(checks=good,owner_approved=False,certifier=lambda a:{"ok":True})
    assert r["status"]=="approval_required" and not r["certifier_called"]
    s=final_acquisition_certification_self_test()
    assert s["ok"] and s["approved_synthetic_final_release_certified"]
