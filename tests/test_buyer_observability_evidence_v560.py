from adam_core.buyer_observability_evidence import EVIDENCE_CHECKS,evaluate_evidence_readiness,export_buyer_safe_evidence
from adam_core.buyer_observability_evidence_boundary import build_buyer_observability_evidence_manifest,buyer_observability_evidence_is_privacy_safe,buyer_observability_evidence_self_test


def test_evidence_readiness_and_owner_gated_export():
    good={k:True for k in EVIDENCE_CHECKS}
    bad=dict(good); bad["incident_state_known"]=False
    assert evaluate_evidence_readiness({"connector":"email","checks":bad})["status"]=="evidence_incomplete"
    assert evaluate_evidence_readiness({"connector":"email","checks":good})["status"]=="evidence_ready"
    blocked=export_buyer_safe_evidence(connector="email",checks=good,owner_approved=False,exporter=lambda c,a:{"ok":True})
    assert blocked["status"]=="approval_required" and blocked["exporter_called"] is False
    approved=export_buyer_safe_evidence(connector="email",checks=good,owner_approved=True,exporter=lambda c,a:{"ok":True})
    assert approved["status"]=="buyer_safe_evidence_authorized"
    assert approved["real_evidence_exported"] is False and approved["customer_payload_included"] is False


def test_observability_boundary_privacy_and_self_test():
    payload=build_buyer_observability_evidence_manifest("v5.7.0")
    assert buyer_observability_evidence_is_privacy_safe(payload) is True
    st=buyer_observability_evidence_self_test()
    assert st["ok"] is True
    assert st["incomplete_evidence_blocked"] is True
    assert st["evidence_export_blocked_without_owner_approval"] is True
    assert st["approved_synthetic_evidence_export_authorized"] is True
    assert st["real_evidence_exported"] is False
