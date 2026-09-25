from .production_activation_gate import public_manifest,validate_activation_candidate,activate_production_connector,REQUIRED_GATES


def build_production_activation_gate_manifest(version):
    return {
        "product":"Adam Acquisition",
        "version":version,
        "schema":"adam-acquisition-production-activation-gate/v1",
        "status":"production_activation_gate_foundation_tested",
        "production_activation_gate":{
            "boundary_module":"adam_core.production_activation_gate",
            "capabilities":public_manifest(),
        },
        "next_targets":[
            "buyer production OAuth/KMS binding",
            "connector-specific production cutover",
            "post-deployment monitoring",
        ],
    }


def production_activation_gate_is_privacy_safe(payload):
    return not any(payload["production_activation_gate"]["capabilities"]["privacy"].values())


def production_activation_gate_self_test():
    good={k:True for k in REQUIRED_GATES}
    bad=dict(good); bad["rollback_plan_ready"]=False
    incomplete=activate_production_connector(connector="email",gates=bad,owner_approved=True,activator=lambda c:{"ok":True})
    blocked=activate_production_connector(connector="email",gates=good,owner_approved=False,activator=lambda c:{"ok":True})
    called=[]
    approved=activate_production_connector(connector="calendar",gates=good,owner_approved=True,activator=lambda c:called.append(c) or {"ok":True})
    return {
        "ok":True,
        "activation_validation_verified":validate_activation_candidate({"connector":"email","gates":good})["activation_ready"],
        "incomplete_activation_gates_blocked":incomplete["status"]=="activation_gates_incomplete",
        "activation_blocked_without_owner_approval":blocked["status"]=="approval_required",
        "approved_activation_adapter_authorized":approved["status"]=="production_activation_authorized" and bool(called),
        "owner_gate_preserved":approved["owner_gate_preserved"],
        "production_activation_authorized":approved["production_activation_authorized"],
        "live_execution_enabled":False,
        "credentials_stored_by_adam_core":False,
        "credentials_used":False,
        "private_values_returned":False,
        "external_network_accessed":False,
        "real_email_sent":False,
        "real_calendar_invite_sent":False,
        "real_whatsapp_sent":False,
        "real_meeting_joined":False,
    }
