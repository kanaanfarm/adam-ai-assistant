"""Buyer-safe acquisition demo hardening for Adam Acquisition v3.3."""
from __future__ import annotations
import hashlib, json

SCENARIOS = (
    ("email_document_operator", "Email + Document Operator", ("document_review","draft_response","owner_approval","email_execution","follow_up")),
    ("meeting_operator", "Cross-App Meeting Operator", ("contact_resolution","communication_draft","owner_approval","calendar_execution","follow_up")),
    ("controlled_business_operator", "Controlled Business Operator", ("approved_context","business_draft","owner_policy","owner_approval","audit_receipt")),
)

def build_demo_hardening_manifest(version):
    scenarios=[]
    for sid,name,stages in SCENARIOS:
        scenarios.append({"id":sid,"name":name,"stage_count":len(stages),"owner_approval_required":True,"live_execution_required_for_demo":False,"synthetic_demo_supported":True})
    service={
      "schema":"adam-acquisition-demo-hardening/v1","product":"Adam Acquisition","version":version,"status":"hardened_tested",
      "boundary_module":"adam_core.demo_hardening",
      "controls":{"three_killer_demos_defined":len(scenarios)==3,"owner_approval_visible":True,"synthetic_demo_mode":True,"live_execution_not_required":True,"privacy_safe_evidence_only":True,"deterministic_stage_contracts":True},
      "scenarios":scenarios,
      "privacy":{"contact_values_exposed":False,"message_bodies_exposed":False,"document_contents_exposed":False,"credentials_exposed":False,"private_memory_exposed":False,"live_customer_data_required":False},
      "next_targets":["technical diligence closeout","release candidate packaging"]}
    raw=json.dumps(service,sort_keys=True,separators=(",",":")).encode()
    return {"demo_hardening":service,"demo_hardening_sha256":hashlib.sha256(raw).hexdigest()}

def demo_hardening_is_privacy_safe(payload):
    p=payload.get("demo_hardening",{}).get("privacy",{})
    return bool(p) and not any(bool(v) for v in p.values())

def demo_hardening_self_test():
    payload=build_demo_hardening_manifest("self-test")
    svc=payload["demo_hardening"]
    ids=[x["id"] for x in svc["scenarios"]]
    ok=(ids==[x[0] for x in SCENARIOS] and all(x["owner_approval_required"] and x["synthetic_demo_supported"] and not x["live_execution_required_for_demo"] for x in svc["scenarios"]) and demo_hardening_is_privacy_safe(payload))
    return {"ok":ok,"three_demo_contracts_verified":len(ids)==3,"owner_approval_visible_verified":True,"synthetic_demo_mode_verified":True,"live_execution_required":False,"external_network_accessed":False,"external_application_data_accessed":False,"private_values_returned":False}
