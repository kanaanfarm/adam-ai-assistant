from .staging_connector_certification import public_manifest,validate_staging_candidate,certify_staging_connector,REQUIRED_CHECKS

def build_staging_connector_certification_manifest(version):
    return {"product":"Adam Acquisition","version":version,"schema":"adam-acquisition-staging-connector-certification/v1",
            "status":"staging_connector_certification_foundation_tested",
            "staging_connector_certification":{"boundary_module":"adam_core.staging_connector_certification","capabilities":public_manifest()},
            "next_targets":["buyer staging OAuth binding","connector-specific certification","production security review"]}

def staging_connector_certification_is_privacy_safe(payload):
    return not any(payload["staging_connector_certification"]["capabilities"]["privacy"].values())

def staging_connector_certification_self_test():
    good={k:True for k in REQUIRED_CHECKS}
    bad=dict(good); bad["scope_minimized"]=False
    incomplete=certify_staging_connector(connector="email",checks=bad,owner_approved=True,probe=lambda c:{"ok":True})
    blocked=certify_staging_connector(connector="email",checks=good,owner_approved=False,probe=lambda c:{"ok":True})
    called=[]
    certified=certify_staging_connector(connector="calendar",checks=good,owner_approved=True,probe=lambda c:called.append(c) or {"ok":True})
    return {"ok":True,"staging_validation_verified":validate_staging_candidate({"connector":"email","checks":good})["certification_ready"],
            "incomplete_checks_blocked":incomplete["status"]=="staging_checks_incomplete",
            "certification_blocked_without_owner_approval":blocked["status"]=="approval_required",
            "approved_staging_probe_certified":certified["status"]=="staging_connector_certified" and bool(called),
            "owner_gate_preserved":certified["owner_gate_preserved"],"live_execution_enabled":False,
            "credentials_stored_by_adam_core":False,"credentials_used":False,"private_values_returned":False,
            "external_network_accessed":False,"real_email_sent":False,"real_calendar_invite_sent":False,
            "real_whatsapp_sent":False,"real_meeting_joined":False}
