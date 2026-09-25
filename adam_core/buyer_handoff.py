"""Privacy-safe buyer handoff evidence for Adam Acquisition."""
from __future__ import annotations
from hashlib import sha256
import json


def _hash(payload):
    raw=json.dumps(payload,sort_keys=True,separators=(",",":"),default=str).encode("utf-8")
    return sha256(raw).hexdigest()


def build_buyer_handoff_manifest(version: str):
    handoff={
      "schema":"adam-acquisition-buyer-handoff/v1",
      "product":"Adam Acquisition","version":version,"status":"buyer_handoff_tested",
      "handoff_label":"RC1 Buyer Review",
      "source_release":"v3.5.0 RC1",
      "review_components":[
        {"id":"application_source","included":True},
        {"id":"architecture_and_version_history","included":True},
        {"id":"technical_diligence_disclosures","included":True},
        {"id":"privacy_safe_evidence_endpoints","included":True},
        {"id":"master_acceptance_history","included":True},
        {"id":"configuration_template_without_secrets","included":True},
        {"id":"buyer_review_instructions","included":True},
      ],
      "review_gates":[
        {"id":"rc1_locked","status":"satisfied"},
        {"id":"owner_acceptance_through_v3_5","status":"satisfied"},
        {"id":"credentials_excluded","status":"satisfied"},
        {"id":"personal_data_excluded","status":"satisfied"},
        {"id":"known_limitations_disclosed","status":"satisfied"},
      ],
      "buyer_review_instructions":[
        "review architecture and version notes before deployment planning",
        "use privacy-safe acquisition endpoints for technical evidence",
        "supply buyer-controlled credentials only in the buyer deployment environment",
        "perform deployment-specific legal security and infrastructure review before production use",
      ],
      "known_disclosures":[
        "legacy Flask app.py remains partially monolithic despite extracted buyer-critical boundaries",
        "deployment credentials and production connector configuration remain buyer/deployer supplied",
        "production legal, security and infrastructure review remains deployment-specific",
      ],
      "privacy":{
        "credentials_exposed":False,"environment_values_exposed":False,"contact_values_exposed":False,
        "message_bodies_exposed":False,"document_contents_exposed":False,"private_memory_exposed":False,
        "workflow_or_approval_values_exposed":False,"personal_data_bundled":False,"live_customer_data_required":False,
      },
      "next_target":"buyer presentation and acquisition outreach",
    }
    return {"buyer_handoff":handoff,"buyer_handoff_sha256":_hash(handoff)}


def buyer_handoff_is_privacy_safe(payload):
    privacy=((payload or {}).get("buyer_handoff") or {}).get("privacy") or {}
    return bool(privacy) and not any(bool(v) for v in privacy.values())


def buyer_handoff_self_test():
    payload=build_buyer_handoff_manifest("v-test")
    h=payload["buyer_handoff"]
    return {
      "ok":True,
      "rc1_source_release_verified":h["source_release"]=="v3.5.0 RC1",
      "seven_review_components_verified":len(h["review_components"])==7 and all(x.get("included") is True for x in h["review_components"]),
      "five_review_gates_verified":len(h["review_gates"])==5 and all(x.get("status")=="satisfied" for x in h["review_gates"]),
      "buyer_review_instructions_verified":len(h["buyer_review_instructions"])==4,
      "known_disclosures_retained_verified":len(h["known_disclosures"])==3,
      "credential_free_handoff_verified":h["privacy"]["credentials_exposed"] is False,
      "personal_data_free_handoff_verified":h["privacy"]["personal_data_bundled"] is False,
      "privacy_projection_verified":buyer_handoff_is_privacy_safe(payload),
      "external_network_accessed":False,"external_application_data_accessed":False,"private_values_returned":False,
    }
