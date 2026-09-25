"""Buyer observability and production evidence foundation for Adam Acquisition v5.6.

Produces bounded, privacy-safe operational evidence from buyer-supplied health
signals. Acceptance mode is synthetic and never contacts a live connector,
observability vendor, customer system, credential store, or network endpoint.
"""
from __future__ import annotations
from typing import Any, Callable

SUPPORTED_CONNECTORS=("email","calendar","whatsapp","meeting_platform","documents")
EVIDENCE_CHECKS=(
    "health_snapshot_available",
    "audit_receipt_available",
    "approval_receipt_available",
    "privacy_boundary_verified",
    "incident_state_known",
)

class BuyerObservabilityEvidenceError(ValueError):
    pass


def evaluate_evidence_readiness(data:dict[str,Any]|None=None)->dict:
    data=data or {}
    connector=str(data.get("connector") or "").strip().lower()
    if connector not in SUPPORTED_CONNECTORS:
        raise BuyerObservabilityEvidenceError("Unsupported connector.")
    checks=data.get("checks") if isinstance(data.get("checks"),dict) else {}
    normalized={k:bool(checks.get(k,False)) for k in EVIDENCE_CHECKS}
    complete=all(normalized.values())
    missing=[k for k,v in normalized.items() if not v]
    return {
        "ok":complete,
        "status":"evidence_ready" if complete else "evidence_incomplete",
        "connector":connector,
        "evidence_complete":complete,
        "missing_check_count":len(missing),
        "customer_payload_included":False,
        "credentials_used_by_core":False,
        "private_values_returned":False,
        "external_network_accessed":False,
        "synthetic_only":True,
    }


def export_buyer_safe_evidence(*,connector:str,checks:dict[str,bool],owner_approved:bool,
                               exporter:Callable[[str,str],dict]|None=None)->dict:
    readiness=evaluate_evidence_readiness({"connector":connector,"checks":checks})
    base={
        "connector":connector,"evidence_complete":readiness["evidence_complete"],
        "owner_gate_preserved":True,"exporter_called":False,"evidence_export_authorized":False,
        "customer_payload_included":False,"credentials_used_by_core":False,
        "private_values_returned":False,"external_network_accessed":False,
        "real_evidence_exported":False,"synthetic_only":True,
    }
    if not readiness["evidence_complete"]:
        return {"ok":False,"status":"evidence_incomplete",**base}
    if not owner_approved:
        return {"ok":False,"status":"approval_required",**base}
    if exporter is None:
        return {"ok":False,"status":"buyer_evidence_export_adapter_required",**base}
    receipt=exporter(connector,"privacy_safe_production_evidence") or {}
    authorized=bool(receipt.get("ok",False))
    return {
        "ok":authorized,
        "status":"buyer_safe_evidence_authorized" if authorized else "evidence_export_adapter_failed",
        **{**base,"exporter_called":True,"evidence_export_authorized":authorized},
    }


def public_manifest()->dict:
    return {
        "buyer_observability_and_production_evidence":True,
        "operational_health_evidence":True,
        "audit_receipt_evidence":True,
        "owner_approval_receipt_evidence":True,
        "incident_state_evidence":True,
        "supported_connectors":list(SUPPORTED_CONNECTORS),
        "required_evidence_checks":list(EVIDENCE_CHECKS),
        "buyer_controlled_evidence_export_adapter":True,
        "owner_approval_required_before_evidence_export":True,
        "credentials_stored_by_adam_core":False,
        "customer_payload_persisted_in_buyer_evidence":False,
        "real_export_enabled_by_acceptance_test":False,
        "privacy":{
            "credentials_exposed":False,"contact_values_exposed":False,
            "message_bodies_exposed":False,"meeting_references_exposed":False,
            "document_contents_exposed":False,"customer_payload_values_exposed":False,
        },
    }
