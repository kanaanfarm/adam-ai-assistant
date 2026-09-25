"""Final acquisition release-candidate and buyer-demo certification for Adam Acquisition v5.8."""
from __future__ import annotations
from typing import Any, Callable

CERTIFICATION_CHECKS = (
    "acceptance_suite_locked",
    "buyer_demo_flow_verified",
    "security_hardening_verified",
    "privacy_boundary_verified",
    "deployment_safety_verified",
    "buyer_handoff_package_ready",
)

class FinalAcquisitionCertificationError(ValueError):
    pass

def evaluate_release_candidate(data: dict[str, Any] | None = None) -> dict:
    data = data or {}
    checks = data.get("checks") if isinstance(data.get("checks"), dict) else {}
    normalized = {k: bool(checks.get(k, False)) for k in CERTIFICATION_CHECKS}
    complete = all(normalized.values())
    return {
        "ok": complete,
        "status": "release_candidate_ready" if complete else "release_candidate_incomplete",
        "release_candidate_complete": complete,
        "missing_check_count": sum(not v for v in normalized.values()),
        "credentials_used_by_core": False,
        "private_values_returned": False,
        "external_network_accessed": False,
        "real_buyer_handoff_executed": False,
        "synthetic_only": True,
    }

def certify_buyer_demo_release(*, checks: dict[str, bool], owner_approved: bool,
                               certifier: Callable[[str], dict] | None = None) -> dict:
    readiness = evaluate_release_candidate({"checks": checks})
    base = {
        "release_candidate_complete": readiness["release_candidate_complete"],
        "owner_gate_preserved": True,
        "certifier_called": False,
        "buyer_demo_certified": False,
        "final_release_authorized": False,
        "credentials_used_by_core": False,
        "private_values_returned": False,
        "external_network_accessed": False,
        "real_buyer_handoff_executed": False,
        "real_deployment_executed": False,
        "synthetic_only": True,
    }
    if not readiness["release_candidate_complete"]:
        return {"ok": False, "status": "release_candidate_incomplete", **base}
    if not owner_approved:
        return {"ok": False, "status": "approval_required", **base}
    if certifier is None:
        return {"ok": False, "status": "buyer_certification_adapter_required", **base}
    receipt = certifier("final_acquisition_release_and_buyer_demo_certification") or {}
    ok = bool(receipt.get("ok", False))
    return {
        "ok": ok,
        "status": "final_acquisition_release_certified" if ok else "certification_adapter_failed",
        **{**base, "certifier_called": True, "buyer_demo_certified": ok, "final_release_authorized": ok},
    }

def public_manifest() -> dict:
    return {
        "final_acquisition_release_candidate": True,
        "buyer_demo_certification": True,
        "required_certification_checks": list(CERTIFICATION_CHECKS),
        "acceptance_suite_lock_required": True,
        "security_hardening_verification_required": True,
        "privacy_boundary_verification_required": True,
        "deployment_safety_verification_required": True,
        "buyer_handoff_package_required": True,
        "owner_approval_required_before_final_release_authorization": True,
        "buyer_controlled_certification_adapter": True,
        "credentials_stored_by_adam_core": False,
        "automatic_buyer_handoff_allowed": False,
        "real_handoff_enabled_by_acceptance_test": False,
        "privacy": {
            "credentials_exposed": False,
            "contact_values_exposed": False,
            "message_bodies_exposed": False,
            "document_contents_exposed": False,
            "customer_payload_values_exposed": False,
            "buyer_private_values_exposed": False,
        },
    }
