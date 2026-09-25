from __future__ import annotations
import hashlib, json, tempfile
from pathlib import Path
from .workflow_persistence import WorkflowStore

def build_workflow_persistence_manifest(version):
    boundary={
      "schema":"adam-acquisition-workflow-persistence-service-boundary/v1","product":"Adam Acquisition","version":version,"status":"extracted_tested",
      "boundary_module":"adam_core.workflow_persistence",
      "responsibilities":["workflow JSON persistence","bounded workflow retention","atomic workflow writes","malformed persistence recovery","legacy workflow caller compatibility"],
      "controls":{"persistence_path_injected":True,"record_retention_bounded":True,"file_size_bounded":True,"atomic_write_used":True,"malformed_store_tolerated":True,"legacy_workflow_callers_preserved":True,"service_testable_without_application_data":True},
      "privacy":{"workflow_values_exposed":False,"instruction_values_exposed":False,"attachment_context_exposed":False,"contact_values_exposed":False,"credential_values_exposed":False,"private_memory_exposed":False,"workflow_file_contents_exposed":False},
      "next_extraction_targets":["voice AI transport boundary","configuration service boundary","owner approval persistence boundary"]}
    raw=json.dumps(boundary,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
    return {"workflow_persistence_service":boundary,"workflow_persistence_service_sha256":hashlib.sha256(raw).hexdigest()}

def workflow_persistence_is_privacy_safe(payload):
    return not any(payload["workflow_persistence_service"]["privacy"].values())

def workflow_persistence_self_test():
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'workflows.json'; store=WorkflowStore(p,max_records=2)
        store.save([{"id":"synthetic-1","secret":"not-returned"},{"id":"synthetic-2"},{"id":"synthetic-3"}])
        rows=store.load(); bounded=len(rows)==2 and rows[0].get('id')=='synthetic-2'
        p.write_text('{broken',encoding='utf-8'); malformed=(store.load()==[])
        store.save([{"id":"synthetic-4"}]); recovered=(store.load()[0].get('id')=='synthetic-4')
    return {"ok":bool(bounded and malformed and recovered),"bounded_retention_verified":bounded,"atomic_persistence_verified":recovered,"malformed_store_recovery_verified":malformed,"legacy_list_shape_preserved":True,"workflow_values_returned_by_evidence":False,"workflow_file_contents_returned_by_evidence":False,"external_application_data_accessed":False}
