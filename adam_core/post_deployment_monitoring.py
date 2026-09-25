"""Post-deployment monitoring and safety watch for Adam Acquisition v5.4.

Privacy-safe operational monitoring contract. Acceptance mode is synthetic and
never performs a real rollback, shutdown, connector call, or network action.
"""
from __future__ import annotations
from typing import Any, Callable

SUPPORTED_CONNECTORS=("email","calendar","whatsapp","meeting_platform","documents")
HEALTH_SIGNALS=("service_healthy","connector_healthy","audit_pipeline_healthy","privacy_boundary_healthy")

class PostDeploymentMonitoringError(ValueError):
    pass


def evaluate_deployment_health(data: dict[str,Any]|None=None)->dict:
    data=data or {}
    connector=str(data.get("connector") or "").strip().lower()
    if connector not in SUPPORTED_CONNECTORS:
        raise PostDeploymentMonitoringError("Unsupported connector.")
    signals=data.get("signals") if isinstance(data.get("signals"),dict) else {}
    checks={k:bool(signals.get(k,False)) for k in HEALTH_SIGNALS}
    healthy=all(checks.values())
    failed=[k for k,v in checks.items() if not v]
    return {
        "ok":True,
        "status":"deployment_healthy" if healthy else "safety_watch_alert",
        "connector":connector,
        "deployment_healthy":healthy,
        "failed_signal_count":len(failed),
        "rollback_recommended":not healthy,
        "automatic_rollback_allowed":False,
        "owner_approval_required_for_rollback":True,
        "credentials_used_by_core":False,
        "private_values_returned":False,
        "external_network_accessed":False,
        "synthetic_only":True,
    }


def execute_safety_response(*, connector:str, signals:dict[str,bool], owner_approved:bool,
                            responder:Callable[[str,str],dict]|None=None)->dict:
    health=evaluate_deployment_health({"connector":connector,"signals":signals})
    if health["deployment_healthy"]:
        return {
            "ok":True,"status":"monitoring_healthy","connector":connector,
            "alert_detected":False,"rollback_recommended":False,
            "owner_gate_preserved":True,"responder_called":False,
            "rollback_authorized":False,"real_rollback_executed":False,
            "credentials_used_by_core":False,"private_values_returned":False,
            "external_network_accessed":False,"synthetic_only":True,
        }
    if not owner_approved:
        return {
            "ok":False,"status":"approval_required","connector":connector,
            "alert_detected":True,"rollback_recommended":True,
            "owner_gate_preserved":True,"responder_called":False,
            "rollback_authorized":False,"real_rollback_executed":False,
            "credentials_used_by_core":False,"private_values_returned":False,
            "external_network_accessed":False,"synthetic_only":True,
        }
    if responder is None:
        return {
            "ok":False,"status":"buyer_safety_response_adapter_required","connector":connector,
            "alert_detected":True,"rollback_recommended":True,
            "owner_gate_preserved":True,"responder_called":False,
            "rollback_authorized":False,"real_rollback_executed":False,
            "credentials_used_by_core":False,"private_values_returned":False,
            "external_network_accessed":False,"synthetic_only":True,
        }
    receipt=responder(connector,"rollback_authorization") or {}
    authorized=bool(receipt.get("ok",False))
    return {
        "ok":authorized,
        "status":"rollback_authorized" if authorized else "safety_response_adapter_failed",
        "connector":connector,"alert_detected":True,"rollback_recommended":True,
        "owner_gate_preserved":True,"responder_called":True,
        "rollback_authorized":authorized,
        # Acceptance mode authorizes only; it never executes a real rollback.
        "real_rollback_executed":False,
        "credentials_used_by_core":False,"private_values_returned":False,
        "external_network_accessed":False,"synthetic_only":True,
    }


def public_manifest()->dict:
    return {
        "post_deployment_monitoring":True,
        "continuous_health_watch_contract":True,
        "supported_connectors":list(SUPPORTED_CONNECTORS),
        "health_signals":list(HEALTH_SIGNALS),
        "connector_failure_detection":True,
        "audit_pipeline_monitoring":True,
        "privacy_boundary_monitoring":True,
        "rollback_recommendation":True,
        "automatic_destructive_response_allowed":False,
        "owner_approval_required_before_rollback":True,
        "buyer_controlled_safety_response_adapter":True,
        "credentials_stored_by_adam_core":False,
        "real_rollback_enabled_by_acceptance_test":False,
        "privacy":{
            "credentials_exposed":False,"contact_values_exposed":False,
            "message_bodies_exposed":False,"meeting_references_exposed":False,
            "document_contents_exposed":False,"monitoring_payload_values_exposed":False,
        },
    }
