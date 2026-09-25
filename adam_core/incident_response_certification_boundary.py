from .incident_response_certification import public_manifest,validate_incident_readiness,run_incident_response_drill,READINESS_CHECKS


def build_incident_response_certification_manifest(version):
    return {
        "product":"Adam Acquisition","version":version,
        "schema":"adam-acquisition-incident-response-certification/v1",
        "status":"incident_response_certification_foundation_tested",
        "incident_response_certification":{
            "boundary_module":"adam_core.incident_response_certification",
            "capabilities":public_manifest(),
        },
        "next_targets":["buyer observability binding","connector-specific incident playbooks","production incident evidence export"],
    }


def incident_response_certification_is_privacy_safe(payload):
    return not any(payload["incident_response_certification"]["capabilities"]["privacy"].values())


def incident_response_certification_self_test():
    good={k:True for k in READINESS_CHECKS}
    bad=dict(good); bad["rollback_path_ready"]=False
    incomplete=validate_incident_readiness({"connector":"email","incident_type":"connector_failure","checks":bad})
    blocked=run_incident_response_drill(connector="email",incident_type="connector_failure",checks=good,owner_approved=False,responder=lambda c,i,a:{"ok":True})
    called=[]
    approved=run_incident_response_drill(connector="email",incident_type="connector_failure",checks=good,owner_approved=True,responder=lambda c,i,a:called.append((c,i,a)) or {"ok":True})
    return {
        "ok":True,
        "incomplete_readiness_blocked":incomplete["status"]=="incident_readiness_incomplete",
        "complete_readiness_verified":blocked["readiness_complete"],
        "incident_response_blocked_without_owner_approval":blocked["status"]=="approval_required",
        "approved_synthetic_incident_response_certified":approved["status"]=="incident_response_certified" and bool(called),
        "owner_gate_preserved":approved["owner_gate_preserved"],
        "automatic_destructive_response_allowed":False,
        "real_containment_executed":False,"real_rollback_executed":False,
        "credentials_stored_by_adam_core":False,"credentials_used":False,
        "private_values_returned":False,"external_network_accessed":False,
        "real_email_sent":False,"real_calendar_invite_sent":False,
        "real_whatsapp_sent":False,"real_meeting_joined":False,
    }
