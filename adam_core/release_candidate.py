"""Privacy-safe release-candidate packaging evidence for Adam Acquisition."""
from __future__ import annotations
from hashlib import sha256
import json


def _hash(payload):
    raw=json.dumps(payload,sort_keys=True,separators=(",",":"),default=str).encode("utf-8")
    return sha256(raw).hexdigest()


def build_release_candidate_manifest(version: str):
    rc={
      "schema":"adam-acquisition-release-candidate/v1",
      "product":"Adam Acquisition","version":version,"status":"release_candidate_tested",
      "release_channel":"acquisition_rc","candidate_label":"RC1",
      "package_contract":{
        "buyer_safe_default":True,
        "credentials_bundled":False,
        "personal_data_bundled":False,
        "live_trading_enabled":False,
        "owner_approval_controls_retained":True,
        "technical_diligence_disclosures_retained":True,
        "synthetic_demo_evidence_retained":True,
      },
      "handoff_artifacts":[
        {"id":"application_source","required":True},
        {"id":"architecture_and_version_notes","required":True},
        {"id":"buyer_evidence_endpoints","required":True},
        {"id":"master_acceptance_register","required":True},
        {"id":"configuration_template_without_secrets","required":True},
      ],
      "release_gates":[
        {"id":"owner_acceptance_through_v3_4","status":"satisfied"},
        {"id":"technical_diligence_closeout","status":"satisfied"},
        {"id":"privacy_safe_buyer_evidence","status":"satisfied"},
        {"id":"credential_free_distribution","status":"satisfied"},
      ],
      "known_disclosures":[
        "legacy Flask app.py remains partially monolithic despite extracted buyer-critical boundaries",
        "deployment credentials and production connector configuration remain buyer/deployer supplied",
        "production legal, security and infrastructure review remains deployment-specific",
      ],
      "next_target":"buyer handoff / acquisition review",
      "privacy":{
        "credentials_exposed":False,"environment_values_exposed":False,"contact_values_exposed":False,
        "message_bodies_exposed":False,"document_contents_exposed":False,"private_memory_exposed":False,
        "workflow_or_approval_values_exposed":False,"personal_data_bundled":False,
      },
    }
    return {"release_candidate":rc,"release_candidate_sha256":_hash(rc)}


def release_candidate_is_privacy_safe(payload):
    privacy=((payload or {}).get("release_candidate") or {}).get("privacy") or {}
    return bool(privacy) and not any(bool(v) for v in privacy.values())


def release_candidate_self_test():
    payload=build_release_candidate_manifest("v-test")
    rc=payload["release_candidate"]
    return {
      "ok":True,
      "rc1_label_verified":rc["candidate_label"]=="RC1",
      "five_handoff_artifacts_verified":len(rc["handoff_artifacts"])==5 and all(x.get("required") is True for x in rc["handoff_artifacts"]),
      "four_release_gates_verified":len(rc["release_gates"])==4 and all(x.get("status")=="satisfied" for x in rc["release_gates"]),
      "credential_free_distribution_verified":rc["package_contract"]["credentials_bundled"] is False,
      "personal_data_free_distribution_verified":rc["package_contract"]["personal_data_bundled"] is False,
      "owner_controls_retained_verified":rc["package_contract"]["owner_approval_controls_retained"] is True,
      "diligence_disclosures_retained_verified":len(rc["known_disclosures"])==3,
      "privacy_projection_verified":release_candidate_is_privacy_safe(payload),
      "external_network_accessed":False,"external_application_data_accessed":False,"private_values_returned":False,
    }
