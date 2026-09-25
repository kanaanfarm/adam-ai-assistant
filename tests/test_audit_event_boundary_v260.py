from pathlib import Path
from datetime import datetime, timezone
from adam_core.audit_events import build_event, append_event, read_recent, MAX_RECORD_BYTES
from adam_core.audit_boundary import build_audit_manifest, audit_boundary_is_privacy_safe, audit_boundary_self_test
ROOT=Path(__file__).resolve().parents[1]

def test_manifest_privacy_and_hash():
    p=build_audit_manifest("v2.7.0")
    assert audit_boundary_is_privacy_safe(p)
    assert p["audit_event_service"]["status"]=="extracted_tested"
    assert len(p["audit_event_service_sha256"])==64

def test_network_free_self_test():
    r=audit_boundary_self_test()
    assert r["ok"] and r["jsonl_persistence_verified"] and r["record_size_bound_enforced"]
    assert not r["event_detail_values_returned_by_evidence"] and not r["external_application_data_accessed"]

def test_service_preserves_shape_and_reads(tmp_path):
    p=tmp_path/"audit.jsonl"
    row=append_event(p,"TEST",{"x":1},now=datetime(2026,8,31,tzinfo=timezone.utc))
    assert set(row)=={"timestamp_utc","event","details"}
    assert read_recent(p,1)[0]["details"]["x"]==1

def test_app_delegates_audit_and_exposes_routes():
    src=(ROOT/"app.py").read_text(encoding="utf-8")
    assert 'VERSION = "v8.1.0.1"' in src
    assert "core_audit_append_event" in src
    assert "/api/acquisition/audit-event-boundary" in src
    html=(ROOT/"templates"/"acquisition.html").read_text(encoding="utf-8")
    assert "Audit Event Service Boundary" in html
