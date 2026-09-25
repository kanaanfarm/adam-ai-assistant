from adam_core.incident_response_certification import READINESS_CHECKS,validate_incident_readiness,run_incident_response_drill
from adam_core.incident_response_certification_boundary import build_incident_response_certification_manifest,incident_response_certification_is_privacy_safe,incident_response_certification_self_test


def test_incident_readiness_and_owner_gated_response_drill():
    good={k:True for k in READINESS_CHECKS}
    bad=dict(good); bad["audit_capture_ready"]=False
    incomplete=validate_incident_readiness({"connector":"email","incident_type":"connector_failure","checks":bad})
    assert incomplete["status"]=="incident_readiness_incomplete"
    ready=validate_incident_readiness({"connector":"email","incident_type":"connector_failure","checks":good})
    assert ready["status"]=="incident_response_ready"
    blocked=run_incident_response_drill(connector="email",incident_type="connector_failure",checks=good,owner_approved=False,responder=lambda c,i,a:{"ok":True})
    assert blocked["status"]=="approval_required" and blocked["responder_called"] is False
    approved=run_incident_response_drill(connector="email",incident_type="connector_failure",checks=good,owner_approved=True,responder=lambda c,i,a:{"ok":True})
    assert approved["status"]=="incident_response_certified"
    assert approved["real_containment_executed"] is False and approved["real_rollback_executed"] is False


def test_incident_response_boundary_privacy_and_self_test():
    payload=build_incident_response_certification_manifest("v5.5.0")
    assert incident_response_certification_is_privacy_safe(payload) is True
    st=incident_response_certification_self_test()
    assert st["ok"] is True
    assert st["incomplete_readiness_blocked"] is True
    assert st["incident_response_blocked_without_owner_approval"] is True
    assert st["approved_synthetic_incident_response_certified"] is True
    assert st["real_containment_executed"] is False and st["real_rollback_executed"] is False
