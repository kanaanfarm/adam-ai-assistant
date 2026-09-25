"""Buyer-controlled production connector binding foundation for Adam Acquisition v5.1."""
from __future__ import annotations
from typing import Any, Callable

SUPPORTED_CONNECTORS=("email","calendar","whatsapp","meeting_platform","documents")
CONSEQUENTIAL_OPERATIONS=("send","invite","message","join","upload")

class ProductionConnectorBindingError(ValueError):
    pass

def validate_binding_request(data: dict[str,Any]|None=None)->dict:
    data=data or {}
    connector=str(data.get("connector") or "").strip().lower()
    operation=str(data.get("operation") or "").strip().lower()
    if connector not in SUPPORTED_CONNECTORS:
        raise ProductionConnectorBindingError("Unsupported connector.")
    if not operation:
        raise ProductionConnectorBindingError("Operation is required.")
    return {"ok":True,"status":"connector_binding_validated","connector":connector,"operation":operation,
            "owner_approval_required":operation in CONSEQUENTIAL_OPERATIONS,"credentials_accepted_by_core":False,
            "synthetic_only":True,"private_values_returned":False}

def execute_bound_operation(*, connector:str, operation:str, owner_approved:bool, transport:Callable[[str,str],dict]|None=None)->dict:
    validated=validate_binding_request({"connector":connector,"operation":operation})
    if validated["owner_approval_required"] and not owner_approved:
        return {"ok":False,"status":"approval_required","connector":connector,"operation":operation,
                "owner_gate_preserved":True,"transport_called":False,"credentials_used":False,
                "external_network_accessed":False,"private_values_returned":False,"synthetic_only":True}
    if transport is None:
        return {"ok":False,"status":"buyer_transport_required","connector":connector,"operation":operation,
                "owner_gate_preserved":True,"transport_called":False,"credentials_used":False,
                "external_network_accessed":False,"private_values_returned":False,"synthetic_only":True}
    receipt=transport(connector,operation) or {}
    return {"ok":True,"status":"bound_operation_executed","connector":connector,"operation":operation,
            "owner_gate_preserved":True,"transport_called":True,"adapter_ok":bool(receipt.get("ok",True)),
            "credentials_used_by_core":False,"private_values_returned":False,"synthetic_only":True}

def public_manifest()->dict:
    return {"buyer_controlled_production_connector_binding":True,"supported_connectors":list(SUPPORTED_CONNECTORS),
            "injected_transport_adapters":True,"credentials_stored_by_adam_core":False,
            "owner_approval_before_consequential_execution":True,"transport_isolation":True,
            "production_credentials_buyer_supplied":True,"live_connectors_configured_by_default":False,
            "privacy":{"credentials_exposed":False,"message_bodies_exposed":False,"meeting_references_exposed":False,
                       "contact_values_exposed":False,"document_contents_exposed":False}}
