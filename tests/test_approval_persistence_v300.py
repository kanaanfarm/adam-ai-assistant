from pathlib import Path
from adam_core.approval_persistence import ApprovalStore
from adam_core.approval_persistence_boundary import build_approval_persistence_manifest,approval_persistence_is_privacy_safe,approval_persistence_self_test

def test_manifest_privacy_and_hash():
 p=build_approval_persistence_manifest("v3.0.0"); assert approval_persistence_is_privacy_safe(p); assert len(p["owner_approval_persistence_service_sha256"])==64

def test_self_test():
 r=approval_persistence_self_test(); assert r["ok"]; assert not r["external_application_data_accessed"]

def test_store_explicit_and_bounded(tmp_path):
 s=ApprovalStore(tmp_path/"a.json",max_records=2); assert not s.is_approved("w","email_review"); s.record("w","email_review"); assert s.is_approved("w","email_review"); assert not s.is_approved("w","calendar_review"); s.record("w2","calendar_review"); s.record("w3","whatsapp_review"); assert len(s.load())==2

def test_app_integration_source():
 src=Path("app.py").read_text(); assert 'VERSION = "v8.1.0.1"' in src; assert 'ADAM_APPROVAL_STORE_V300.record(workflow_id, step)' in src; assert '/api/acquisition/owner-approval-persistence-boundary' in src
