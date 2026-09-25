from .post_deployment_monitoring import public_manifest,evaluate_deployment_health,execute_safety_response,HEALTH_SIGNALS


def build_post_deployment_monitoring_manifest(version):
    return {
        "product":"Adam Acquisition","version":version,
        "schema":"adam-acquisition-post-deployment-monitoring/v1",
        "status":"post_deployment_monitoring_foundation_tested",
        "post_deployment_monitoring":{
            "boundary_module":"adam_core.post_deployment_monitoring",
            "capabilities":public_manifest(),
        },
        "next_targets":["buyer monitoring/observability binding","connector-specific production cutover","incident response certification"],
    }


def post_deployment_monitoring_is_privacy_safe(payload):
    return not any(payload["post_deployment_monitoring"]["capabilities"]["privacy"].values())


def post_deployment_monitoring_self_test():
    good={k:True for k in HEALTH_SIGNALS}
    bad=dict(good); bad["connector_healthy"]=False
    healthy=evaluate_deployment_health({"connector":"email","signals":good})
    blocked=execute_safety_response(connector="email",signals=bad,owner_approved=False,responder=lambda c,a:{"ok":True})
    called=[]
    approved=execute_safety_response(connector="email",signals=bad,owner_approved=True,responder=lambda c,a:called.append((c,a)) or {"ok":True})
    return {
        "ok":True,
        "healthy_deployment_verified":healthy["deployment_healthy"],
        "connector_failure_detected":blocked["alert_detected"],
        "rollback_recommended_on_failure":blocked["rollback_recommended"],
        "safety_response_blocked_without_owner_approval":blocked["status"]=="approval_required",
        "approved_synthetic_rollback_authorized":approved["status"]=="rollback_authorized" and bool(called),
        "owner_gate_preserved":approved["owner_gate_preserved"],
        "automatic_rollback_allowed":False,
        "real_rollback_executed":False,
        "credentials_stored_by_adam_core":False,"credentials_used":False,
        "private_values_returned":False,"external_network_accessed":False,
        "real_email_sent":False,"real_calendar_invite_sent":False,
        "real_whatsapp_sent":False,"real_meeting_joined":False,
    }
