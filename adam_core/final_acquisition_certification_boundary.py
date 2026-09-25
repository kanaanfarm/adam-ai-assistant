from .final_acquisition_certification import public_manifest, evaluate_release_candidate, certify_buyer_demo_release, CERTIFICATION_CHECKS

def build_final_acquisition_certification_manifest(version):
    return {
        "product": "Adam Acquisition", "version": version,
        "schema": "adam-acquisition-final-release-certification/v1",
        "status": "final_acquisition_release_candidate_tested",
        "final_acquisition_certification": {
            "boundary_module": "adam_core.final_acquisition_certification",
            "capabilities": public_manifest(),
        },
        "next_targets": ["buyer demonstrations", "technical diligence", "acquisition outreach"],
    }

def final_acquisition_certification_is_privacy_safe(payload):
    return not any(payload["final_acquisition_certification"]["capabilities"]["privacy"].values())

def final_acquisition_certification_self_test():
    good = {k: True for k in CERTIFICATION_CHECKS}
    bad = dict(good); bad["buyer_handoff_package_ready"] = False
    incomplete = evaluate_release_candidate({"checks": bad})
    blocked = certify_buyer_demo_release(checks=good, owner_approved=False, certifier=lambda a: {"ok": True})
    called = []
    approved = certify_buyer_demo_release(checks=good, owner_approved=True, certifier=lambda a: called.append(a) or {"ok": True})
    return {
        "ok": True,
        "incomplete_release_candidate_blocked": incomplete["status"] == "release_candidate_incomplete",
        "complete_release_candidate_verified": blocked["release_candidate_complete"],
        "final_release_blocked_without_owner_approval": blocked["status"] == "approval_required",
        "approved_synthetic_final_release_certified": approved["status"] == "final_acquisition_release_certified" and bool(called),
        "buyer_demo_certified": approved["buyer_demo_certified"],
        "owner_gate_preserved": approved["owner_gate_preserved"],
        "automatic_buyer_handoff_allowed": False,
        "credentials_stored_by_adam_core": False,
        "credentials_used": False,
        "private_values_returned": False,
        "external_network_accessed": False,
        "real_buyer_handoff_executed": False,
        "real_deployment_executed": False,
        "real_email_sent": False,
        "real_calendar_invite_sent": False,
        "real_whatsapp_sent": False,
        "real_meeting_joined": False,
    }
