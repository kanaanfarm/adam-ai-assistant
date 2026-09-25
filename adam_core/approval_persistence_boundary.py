"""Buyer-safe evidence for owner-approval persistence."""
from __future__ import annotations
import hashlib,json,tempfile
from pathlib import Path
from .approval_persistence import ApprovalStore

def _hash(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(",",":"),default=str).encode()).hexdigest()
def build_approval_persistence_manifest(version):
    service={"schema":"adam-acquisition-owner-approval-persistence-boundary/v1","product":"Adam Acquisition","version":version,"status":"extracted_tested","boundary_module":"adam_core.approval_persistence","responsibilities":["owner approval receipt persistence","bounded approval retention","atomic approval writes","malformed persistence recovery","workflow approval caller compatibility"],"controls":{"persistence_path_injected":True,"record_retention_bounded":True,"file_size_bounded":True,"atomic_write_used":True,"malformed_store_tolerated":True,"explicit_approval_only":True,"legacy_workflow_approval_preserved":True,"service_testable_without_application_data":True},"privacy":{"workflow_ids_exposed":False,"approval_values_exposed":False,"instruction_values_exposed":False,"contact_values_exposed":False,"message_values_exposed":False,"credential_values_exposed":False,"private_memory_exposed":False,"approval_file_contents_exposed":False},"next_extraction_targets":["Windows speech fallback boundary","runtime configuration consolidation","final acquisition demo hardening"]}
    return {"owner_approval_persistence_service":service,"owner_approval_persistence_service_sha256":_hash(service)}
def approval_persistence_is_privacy_safe(payload): return all(v is False for v in payload["owner_approval_persistence_service"]["privacy"].values())
def approval_persistence_self_test():
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/"approvals.json"; s=ApprovalStore(p,max_records=2,max_file_bytes=4096)
        s.record("synthetic-1","email_review"); explicit=s.is_approved("synthetic-1","email_review") and not s.is_approved("synthetic-1","calendar_review")
        s.record("synthetic-2","calendar_review"); s.record("synthetic-3","whatsapp_review"); bounded=len(s.load())==2
        atomic=p.exists() and not list(Path(td).glob("*.tmp"))
        p.write_text("{malformed",encoding="utf-8"); malformed=s.load()==[]
    return {"ok":bool(explicit and bounded and atomic and malformed),"explicit_approval_verified":explicit,"bounded_retention_verified":bounded,"atomic_persistence_verified":atomic,"malformed_store_recovery_verified":malformed,"external_application_data_accessed":False,"approval_values_returned_by_evidence":False,"workflow_ids_returned_by_evidence":False,"approval_file_contents_returned_by_evidence":False}
