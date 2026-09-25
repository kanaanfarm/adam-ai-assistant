"""Production activation gate foundation for Adam Acquisition v5.3.

This module validates buyer-controlled production readiness and preserves an
explicit Owner Approval gate. It does not perform live external execution.
"""
from __future__ import annotations
from typing import Any, Callable

SUPPORTED_CONNECTORS=("email","calendar","whatsapp","meeting_platform","documents")
REQUIRED_GATES=(
    "staging_certified",
    "security_review_complete",
    "least_privilege_verified",
    "rollback_plan_ready",
    "audit_logging_enabled",
)

class ProductionActivationGateError(ValueError):
    pass


def validate_activation_candidate(data: dict[str,Any]|None=None)->dict:
    data=data or {}
    connector=str(data.get("connector") or "").strip().lower()
    if connector not in SUPPORTED_CONNECTORS:
        raise ProductionActivationGateError("Unsupported connector.")
    gates=data.get("gates") if isinstance(data.get("gates"),dict) else {}
    results={k:bool(gates.get(k,False)) for k in REQUIRED_GATES}
    ready=all(results.values())
    return {
        "ok":True,
        "status":"production_activation_candidate_validated",
        "connector":connector,
        "activation_ready":ready,
        "required_gates":results,
        "credentials_accepted_by_core":False,
        "live_execution_enabled":False,
        "private_values_returned":False,
        "synthetic_only":True,
    }


def activate_production_connector(*, connector:str, gates:dict[str,bool], owner_approved:bool,
                                  activator:Callable[[str],dict]|None=None)->dict:
    validated=validate_activation_candidate({"connector":connector,"gates":gates})
    if not validated["activation_ready"]:
        return {
            "ok":False,"status":"activation_gates_incomplete","connector":connector,
            "owner_gate_preserved":True,"activator_called":False,
            "production_activation_authorized":False,"live_execution_enabled":False,
            "credentials_used_by_core":False,"private_values_returned":False,"synthetic_only":True,
        }
    if not owner_approved:
        return {
            "ok":False,"status":"approval_required","connector":connector,
            "owner_gate_preserved":True,"activator_called":False,
            "production_activation_authorized":False,"live_execution_enabled":False,
            "credentials_used_by_core":False,"private_values_returned":False,"synthetic_only":True,
        }
    if activator is None:
        return {
            "ok":False,"status":"buyer_activation_adapter_required","connector":connector,
            "owner_gate_preserved":True,"activator_called":False,
            "production_activation_authorized":False,"live_execution_enabled":False,
            "credentials_used_by_core":False,"private_values_returned":False,"synthetic_only":True,
        }
    receipt=activator(connector) or {}
    authorized=bool(receipt.get("ok",False))
    return {
        "ok":authorized,
        "status":"production_activation_authorized" if authorized else "activation_adapter_failed",
        "connector":connector,
        "owner_gate_preserved":True,
        "activator_called":True,
        "production_activation_authorized":authorized,
        # Acceptance mode verifies authorization only. Live execution remains disabled.
        "live_execution_enabled":False,
        "credentials_used_by_core":False,
        "private_values_returned":False,
        "synthetic_only":True,
    }


def public_manifest()->dict:
    return {
        "production_activation_gate":True,
        "deployment_activation_authorization":True,
        "supported_connectors":list(SUPPORTED_CONNECTORS),
        "required_gates":list(REQUIRED_GATES),
        "staging_certification_required":True,
        "security_review_required":True,
        "least_privilege_required":True,
        "rollback_plan_required":True,
        "audit_logging_required":True,
        "owner_approval_before_activation":True,
        "buyer_controlled_activation_adapter":True,
        "credentials_stored_by_adam_core":False,
        "live_execution_enabled_by_acceptance_test":False,
        "privacy":{
            "credentials_exposed":False,
            "contact_values_exposed":False,
            "message_bodies_exposed":False,
            "meeting_references_exposed":False,
            "document_contents_exposed":False,
        },
    }
