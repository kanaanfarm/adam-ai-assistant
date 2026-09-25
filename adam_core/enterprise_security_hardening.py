"""Enterprise security and deployment hardening foundation for Adam Acquisition v5.7."""
from __future__ import annotations
from typing import Any, Callable

SUPPORTED_ENVIRONMENTS=("staging","production")
SECURITY_CHECKS=(
    "secrets_externalized",
    "least_privilege_verified",
    "transport_security_verified",
    "audit_logging_enabled",
    "rollback_plan_ready",
    "data_retention_policy_verified",
)
class EnterpriseSecurityHardeningError(ValueError): pass

def evaluate_security_readiness(data:dict[str,Any]|None=None)->dict:
    data=data or {}
    environment=str(data.get("environment") or "").strip().lower()
    if environment not in SUPPORTED_ENVIRONMENTS: raise EnterpriseSecurityHardeningError("Unsupported environment.")
    checks=data.get("checks") if isinstance(data.get("checks"),dict) else {}
    normalized={k:bool(checks.get(k,False)) for k in SECURITY_CHECKS}
    complete=all(normalized.values())
    return {"ok":complete,"status":"security_hardening_ready" if complete else "security_hardening_incomplete",
            "environment":environment,"security_readiness_complete":complete,"missing_check_count":sum(not v for v in normalized.values()),
            "credentials_used_by_core":False,"private_values_returned":False,"external_network_accessed":False,"synthetic_only":True}

def authorize_hardened_deployment(*,environment:str,checks:dict[str,bool],owner_approved:bool,deployer:Callable[[str,str],dict]|None=None)->dict:
    readiness=evaluate_security_readiness({"environment":environment,"checks":checks})
    base={"environment":environment,"security_readiness_complete":readiness["security_readiness_complete"],"owner_gate_preserved":True,
          "deployer_called":False,"hardened_deployment_authorized":False,"credentials_used_by_core":False,"private_values_returned":False,
          "external_network_accessed":False,"real_deployment_executed":False,"synthetic_only":True}
    if not readiness["security_readiness_complete"]: return {"ok":False,"status":"security_hardening_incomplete",**base}
    if not owner_approved: return {"ok":False,"status":"approval_required",**base}
    if deployer is None: return {"ok":False,"status":"buyer_deployment_adapter_required",**base}
    receipt=deployer(environment,"enterprise_security_hardening_authorization") or {}
    ok=bool(receipt.get("ok",False))
    return {"ok":ok,"status":"hardened_deployment_authorized" if ok else "deployment_adapter_failed",**{**base,"deployer_called":True,"hardened_deployment_authorized":ok}}

def public_manifest()->dict:
    return {"enterprise_security_and_deployment_hardening":True,"security_readiness_validation":True,"required_security_checks":list(SECURITY_CHECKS),
            "supported_environments":list(SUPPORTED_ENVIRONMENTS),"secrets_externalized_required":True,"least_privilege_required":True,
            "transport_security_required":True,"audit_logging_required":True,"rollback_plan_required":True,"data_retention_policy_required":True,
            "owner_approval_required_before_hardened_deployment_authorization":True,"buyer_controlled_deployment_adapter":True,
            "credentials_stored_by_adam_core":False,"automatic_production_cutover_allowed":False,"real_deployment_enabled_by_acceptance_test":False,
            "privacy":{"credentials_exposed":False,"contact_values_exposed":False,"message_bodies_exposed":False,"document_contents_exposed":False,"customer_payload_values_exposed":False}}
