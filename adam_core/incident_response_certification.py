"""Incident response certification and recovery drill for Adam Acquisition v5.5.

Buyer-controlled, privacy-safe incident readiness contract. Acceptance mode is
synthetic: it never performs a real containment, rollback, shutdown, connector
call, credential operation, or network action.
"""
from __future__ import annotations
from typing import Any, Callable

SUPPORTED_CONNECTORS=("email","calendar","whatsapp","meeting_platform","documents")
INCIDENT_TYPES=("connector_failure","audit_pipeline_failure","privacy_boundary_alert","service_degradation")
READINESS_CHECKS=(
    "monitoring_alert_verified",
    "incident_owner_assigned",
    "containment_plan_ready",
    "rollback_path_ready",
    "audit_capture_ready",
)

class IncidentResponseCertificationError(ValueError):
    pass


def validate_incident_readiness(data: dict[str,Any]|None=None)->dict:
    data=data or {}
    connector=str(data.get("connector") or "").strip().lower()
    incident_type=str(data.get("incident_type") or "").strip().lower()
    if connector not in SUPPORTED_CONNECTORS:
        raise IncidentResponseCertificationError("Unsupported connector.")
    if incident_type not in INCIDENT_TYPES:
        raise IncidentResponseCertificationError("Unsupported incident type.")
    checks=data.get("checks") if isinstance(data.get("checks"),dict) else {}
    normalized={k:bool(checks.get(k,False)) for k in READINESS_CHECKS}
    complete=all(normalized.values())
    missing=[k for k,v in normalized.items() if not v]
    return {
        "ok":complete,
        "status":"incident_response_ready" if complete else "incident_readiness_incomplete",
        "connector":connector,
        "incident_type":incident_type,
        "readiness_complete":complete,
        "missing_check_count":len(missing),
        "owner_approval_required_for_containment_or_recovery":True,
        "automatic_destructive_response_allowed":False,
        "credentials_used_by_core":False,
        "private_values_returned":False,
        "external_network_accessed":False,
        "synthetic_only":True,
    }


def run_incident_response_drill(*, connector:str, incident_type:str, checks:dict[str,bool], owner_approved:bool,
                                responder:Callable[[str,str,str],dict]|None=None)->dict:
    readiness=validate_incident_readiness({"connector":connector,"incident_type":incident_type,"checks":checks})
    if not readiness["readiness_complete"]:
        return {
            "ok":False,"status":"incident_readiness_incomplete","connector":connector,
            "incident_type":incident_type,"readiness_complete":False,
            "owner_gate_preserved":True,"responder_called":False,
            "containment_authorized":False,"recovery_authorized":False,
            "real_containment_executed":False,"real_rollback_executed":False,
            "credentials_used_by_core":False,"private_values_returned":False,
            "external_network_accessed":False,"synthetic_only":True,
        }
    if not owner_approved:
        return {
            "ok":False,"status":"approval_required","connector":connector,
            "incident_type":incident_type,"readiness_complete":True,
            "owner_gate_preserved":True,"responder_called":False,
            "containment_authorized":False,"recovery_authorized":False,
            "real_containment_executed":False,"real_rollback_executed":False,
            "credentials_used_by_core":False,"private_values_returned":False,
            "external_network_accessed":False,"synthetic_only":True,
        }
    if responder is None:
        return {
            "ok":False,"status":"buyer_incident_response_adapter_required","connector":connector,
            "incident_type":incident_type,"readiness_complete":True,
            "owner_gate_preserved":True,"responder_called":False,
            "containment_authorized":False,"recovery_authorized":False,
            "real_containment_executed":False,"real_rollback_executed":False,
            "credentials_used_by_core":False,"private_values_returned":False,
            "external_network_accessed":False,"synthetic_only":True,
        }
    receipt=responder(connector,incident_type,"containment_and_recovery_authorization") or {}
    authorized=bool(receipt.get("ok",False))
    return {
        "ok":authorized,
        "status":"incident_response_certified" if authorized else "incident_response_adapter_failed",
        "connector":connector,"incident_type":incident_type,"readiness_complete":True,
        "owner_gate_preserved":True,"responder_called":True,
        "containment_authorized":authorized,"recovery_authorized":authorized,
        "real_containment_executed":False,"real_rollback_executed":False,
        "credentials_used_by_core":False,"private_values_returned":False,
        "external_network_accessed":False,"synthetic_only":True,
    }


def public_manifest()->dict:
    return {
        "incident_response_certification":True,
        "incident_readiness_validation":True,
        "supported_connectors":list(SUPPORTED_CONNECTORS),
        "incident_types":list(INCIDENT_TYPES),
        "required_readiness_checks":list(READINESS_CHECKS),
        "buyer_controlled_incident_response_adapter":True,
        "owner_approval_required_before_containment_or_recovery":True,
        "automatic_destructive_response_allowed":False,
        "audit_capture_required":True,
        "rollback_path_required":True,
        "credentials_stored_by_adam_core":False,
        "real_incident_action_enabled_by_acceptance_test":False,
        "privacy":{
            "credentials_exposed":False,"contact_values_exposed":False,
            "message_bodies_exposed":False,"meeting_references_exposed":False,
            "document_contents_exposed":False,"incident_payload_values_exposed":False,
        },
    }
