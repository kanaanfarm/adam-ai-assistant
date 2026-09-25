"""Staging connector certification and deployment-readiness boundary for Adam Acquisition v5.2."""
from __future__ import annotations
from typing import Any, Callable

SUPPORTED_CONNECTORS=("email","calendar","whatsapp","meeting_platform","documents")
REQUIRED_CHECKS=("configuration_present","transport_reachable","scope_minimized","owner_gate_enabled","privacy_boundary_verified")

class StagingConnectorCertificationError(ValueError):
    pass

def validate_staging_candidate(data: dict[str,Any]|None=None)->dict:
    data=data or {}
    connector=str(data.get("connector") or "").strip().lower()
    if connector not in SUPPORTED_CONNECTORS:
        raise StagingConnectorCertificationError("Unsupported connector.")
    checks=data.get("checks") if isinstance(data.get("checks"),dict) else {}
    results={k:bool(checks.get(k,False)) for k in REQUIRED_CHECKS}
    passed=all(results.values())
    return {"ok":True,"status":"staging_candidate_validated","connector":connector,
            "certification_ready":passed,"required_checks":results,"credentials_accepted_by_core":False,
            "live_execution_enabled":False,"private_values_returned":False,"synthetic_only":True}

def certify_staging_connector(*, connector:str, checks:dict[str,bool], owner_approved:bool,
                              probe:Callable[[str],dict]|None=None)->dict:
    validated=validate_staging_candidate({"connector":connector,"checks":checks})
    if not validated["certification_ready"]:
        return {"ok":False,"status":"staging_checks_incomplete","connector":connector,
                "owner_gate_preserved":True,"probe_called":False,"deployment_ready":False,
                "live_execution_enabled":False,"credentials_used_by_core":False,
                "private_values_returned":False,"synthetic_only":True}
    if not owner_approved:
        return {"ok":False,"status":"approval_required","connector":connector,
                "owner_gate_preserved":True,"probe_called":False,"deployment_ready":False,
                "live_execution_enabled":False,"credentials_used_by_core":False,
                "private_values_returned":False,"synthetic_only":True}
    if probe is None:
        return {"ok":False,"status":"buyer_staging_probe_required","connector":connector,
                "owner_gate_preserved":True,"probe_called":False,"deployment_ready":False,
                "live_execution_enabled":False,"credentials_used_by_core":False,
                "private_values_returned":False,"synthetic_only":True}
    receipt=probe(connector) or {}
    return {"ok":bool(receipt.get("ok",False)),"status":"staging_connector_certified" if receipt.get("ok") else "staging_probe_failed",
            "connector":connector,"owner_gate_preserved":True,"probe_called":True,
            "deployment_ready":bool(receipt.get("ok",False)),"live_execution_enabled":False,
            "credentials_used_by_core":False,"private_values_returned":False,"synthetic_only":True}

def public_manifest()->dict:
    return {"staging_connector_certification":True,"deployment_readiness_gate":True,
            "supported_connectors":list(SUPPORTED_CONNECTORS),"required_checks":list(REQUIRED_CHECKS),
            "buyer_supplied_staging_configuration":True,"credentials_stored_by_adam_core":False,
            "owner_approval_before_certification":True,"live_execution_enabled_by_certification":False,
            "production_enablement_separate_step":True,
            "privacy":{"credentials_exposed":False,"contact_values_exposed":False,"message_bodies_exposed":False,
                       "meeting_references_exposed":False,"document_contents_exposed":False}}
