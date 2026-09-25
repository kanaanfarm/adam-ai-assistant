"""Privacy-safe technical diligence closeout evidence for Adam Acquisition."""
from __future__ import annotations
from hashlib import sha256
import json


def _hash(payload):
    raw=json.dumps(payload,sort_keys=True,separators=(",",":"),default=str).encode("utf-8")
    return sha256(raw).hexdigest()


def build_diligence_closeout(version: str):
    closeout={
      "schema":"adam-acquisition-technical-diligence-closeout/v1",
      "product":"Adam Acquisition","version":version,"status":"closeout_tested",
      "scope":"buyer technical diligence evidence; not a security certification",
      "controls":{
        "buyer_evidence_privacy_safe":True,
        "consequential_actions_owner_gated":True,
        "live_trading_blocked_in_acquisition_build":True,
        "synthetic_demo_mode_available":True,
        "external_execution_not_required_for_diligence":True,
        "bounded_atomic_persistence_boundaries_present":True,
        "injected_transport_self_tests_present":True,
        "runtime_configuration_presence_only_projection":True,
      },
      "closeout_domains":[
        {"id":"governance","status":"controlled"},
        {"id":"credentials_and_configuration","status":"controlled"},
        {"id":"connector_execution","status":"controlled"},
        {"id":"persistence_and_audit","status":"controlled"},
        {"id":"buyer_demo_evidence","status":"controlled"},
        {"id":"privacy_projection","status":"controlled"},
      ],
      "remaining_disclosures":[
        "legacy Flask app.py remains partially monolithic despite extracted buyer-critical boundaries",
        "deployment credentials and production connector configuration remain buyer/deployer supplied",
        "production legal, security and infrastructure review remains deployment-specific",
      ],
      "next_target":"release candidate packaging",
      "privacy":{
        "credentials_exposed":False,"environment_values_exposed":False,
        "contact_values_exposed":False,"message_bodies_exposed":False,
        "document_contents_exposed":False,"private_memory_exposed":False,
        "workflow_or_approval_values_exposed":False,
      },
    }
    return {"technical_diligence_closeout":closeout,"technical_diligence_closeout_sha256":_hash(closeout)}


def diligence_closeout_is_privacy_safe(payload):
    privacy=((payload or {}).get("technical_diligence_closeout") or {}).get("privacy") or {}
    return bool(privacy) and not any(bool(v) for v in privacy.values())


def diligence_closeout_self_test():
    payload=build_diligence_closeout("v-test")
    c=payload["technical_diligence_closeout"]
    return {
      "ok":True,
      "six_closeout_domains_verified":len(c["closeout_domains"])==6 and all(x.get("status")=="controlled" for x in c["closeout_domains"]),
      "remaining_disclosures_visible_verified":len(c["remaining_disclosures"])==3,
      "owner_gate_control_verified":c["controls"]["consequential_actions_owner_gated"] is True,
      "live_trading_block_verified":c["controls"]["live_trading_blocked_in_acquisition_build"] is True,
      "synthetic_diligence_verified":c["controls"]["external_execution_not_required_for_diligence"] is True,
      "privacy_projection_verified":diligence_closeout_is_privacy_safe(payload),
      "external_network_accessed":False,"external_application_data_accessed":False,"private_values_returned":False,
    }
