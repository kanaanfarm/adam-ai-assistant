from adam_core.post_deployment_monitoring import HEALTH_SIGNALS,evaluate_deployment_health,execute_safety_response
from adam_core.post_deployment_monitoring_boundary import build_post_deployment_monitoring_manifest,post_deployment_monitoring_is_privacy_safe,post_deployment_monitoring_self_test


def test_monitoring_health_and_owner_gated_safety_response():
    good={k:True for k in HEALTH_SIGNALS}
    bad=dict(good); bad["audit_pipeline_healthy"]=False
    healthy=evaluate_deployment_health({"connector":"email","signals":good})
    assert healthy["status"]=="deployment_healthy"
    alert=evaluate_deployment_health({"connector":"email","signals":bad})
    assert alert["status"]=="safety_watch_alert" and alert["rollback_recommended"] is True
    blocked=execute_safety_response(connector="email",signals=bad,owner_approved=False,responder=lambda c,a:{"ok":True})
    assert blocked["status"]=="approval_required" and blocked["responder_called"] is False
    approved=execute_safety_response(connector="email",signals=bad,owner_approved=True,responder=lambda c,a:{"ok":True})
    assert approved["status"]=="rollback_authorized"
    assert approved["real_rollback_executed"] is False


def test_monitoring_boundary_privacy_and_self_test():
    payload=build_post_deployment_monitoring_manifest("v5.4.0")
    assert post_deployment_monitoring_is_privacy_safe(payload) is True
    st=post_deployment_monitoring_self_test()
    assert st["ok"] is True
    assert st["healthy_deployment_verified"] is True
    assert st["connector_failure_detected"] is True
    assert st["safety_response_blocked_without_owner_approval"] is True
    assert st["approved_synthetic_rollback_authorized"] is True
    assert st["real_rollback_executed"] is False
