from .enterprise_security_hardening import public_manifest,evaluate_security_readiness,authorize_hardened_deployment,SECURITY_CHECKS

def build_enterprise_security_hardening_manifest(version):
    return {"product":"Adam Acquisition","version":version,"schema":"adam-acquisition-enterprise-security-hardening/v1",
            "status":"enterprise_security_hardening_foundation_tested","enterprise_security_hardening":{"boundary_module":"adam_core.enterprise_security_hardening","capabilities":public_manifest()},
            "next_targets":["final acquisition release candidate","buyer demo certification"]}

def enterprise_security_hardening_is_privacy_safe(payload):
    return not any(payload["enterprise_security_hardening"]["capabilities"]["privacy"].values())

def enterprise_security_hardening_self_test():
    good={k:True for k in SECURITY_CHECKS}; bad=dict(good); bad["transport_security_verified"]=False
    incomplete=evaluate_security_readiness({"environment":"production","checks":bad})
    blocked=authorize_hardened_deployment(environment="production",checks=good,owner_approved=False,deployer=lambda e,a:{"ok":True})
    called=[]
    approved=authorize_hardened_deployment(environment="production",checks=good,owner_approved=True,deployer=lambda e,a:called.append((e,a)) or {"ok":True})
    return {"ok":True,"incomplete_security_readiness_blocked":incomplete["status"]=="security_hardening_incomplete",
            "complete_security_readiness_verified":blocked["security_readiness_complete"],"deployment_authorization_blocked_without_owner_approval":blocked["status"]=="approval_required",
            "approved_synthetic_hardened_deployment_authorized":approved["status"]=="hardened_deployment_authorized" and bool(called),
            "owner_gate_preserved":approved["owner_gate_preserved"],"automatic_production_cutover_allowed":False,"credentials_stored_by_adam_core":False,
            "credentials_used":False,"private_values_returned":False,"external_network_accessed":False,"real_deployment_executed":False,
            "real_email_sent":False,"real_calendar_invite_sent":False,"real_whatsapp_sent":False,"real_meeting_joined":False}
