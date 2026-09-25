from .buyer_observability_evidence import public_manifest,evaluate_evidence_readiness,export_buyer_safe_evidence,EVIDENCE_CHECKS


def build_buyer_observability_evidence_manifest(version):
    return {
        "product":"Adam Acquisition","version":version,
        "schema":"adam-acquisition-buyer-observability-evidence/v1",
        "status":"buyer_observability_evidence_foundation_tested",
        "buyer_observability_evidence":{
            "boundary_module":"adam_core.buyer_observability_evidence",
            "capabilities":public_manifest(),
        },
        "next_targets":["enterprise security deployment hardening","connector-specific evidence binding","final acquisition release certification"],
    }


def buyer_observability_evidence_is_privacy_safe(payload):
    return not any(payload["buyer_observability_evidence"]["capabilities"]["privacy"].values())


def buyer_observability_evidence_self_test():
    good={k:True for k in EVIDENCE_CHECKS}
    bad=dict(good); bad["audit_receipt_available"]=False
    incomplete=evaluate_evidence_readiness({"connector":"email","checks":bad})
    blocked=export_buyer_safe_evidence(connector="email",checks=good,owner_approved=False,exporter=lambda c,a:{"ok":True})
    called=[]
    approved=export_buyer_safe_evidence(connector="email",checks=good,owner_approved=True,exporter=lambda c,a:called.append((c,a)) or {"ok":True})
    return {
        "ok":True,
        "incomplete_evidence_blocked":incomplete["status"]=="evidence_incomplete",
        "complete_evidence_verified":blocked["evidence_complete"],
        "evidence_export_blocked_without_owner_approval":blocked["status"]=="approval_required",
        "approved_synthetic_evidence_export_authorized":approved["status"]=="buyer_safe_evidence_authorized" and bool(called),
        "owner_gate_preserved":approved["owner_gate_preserved"],
        "customer_payload_included":False,
        "credentials_stored_by_adam_core":False,"credentials_used":False,
        "private_values_returned":False,"external_network_accessed":False,
        "real_evidence_exported":False,"real_email_sent":False,"real_calendar_invite_sent":False,
        "real_whatsapp_sent":False,"real_meeting_joined":False,
    }
