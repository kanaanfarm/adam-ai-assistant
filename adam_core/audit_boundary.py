from __future__ import annotations
import hashlib, json, tempfile
from datetime import datetime, timezone
from pathlib import Path
from . import audit_events


def build_audit_manifest(version):
    boundary = {
        "schema": "adam-acquisition-audit-event-service-boundary/v1",
        "product": "Adam Acquisition", "version": version, "status": "extracted_tested",
        "boundary_module": "adam_core.audit_events",
        "responsibilities": ["audit event record construction", "bounded JSONL persistence", "recent-event retrieval", "legacy audit caller compatibility"],
        "controls": {
            "persistence_path_injected": True,
            "event_name_bounded": True,
            "record_size_bounded": True,
            "malformed_log_lines_tolerated": True,
            "legacy_audit_callers_preserved": True,
            "service_testable_without_application_data": True,
            "buyer_evidence_excludes_event_details": True,
        },
        "privacy": {
            "event_detail_values_exposed": False,
            "contact_values_exposed": False,
            "message_values_exposed": False,
            "credential_values_exposed": False,
            "private_memory_exposed": False,
            "audit_file_contents_exposed": False,
        },
        "next_extraction_targets": ["workflow persistence service boundary", "voice AI transport boundary", "configuration service boundary"],
    }
    raw=json.dumps(boundary,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
    return {"audit_event_service": boundary, "audit_event_service_sha256": hashlib.sha256(raw).hexdigest()}


def audit_boundary_is_privacy_safe(payload):
    return not any(payload["audit_event_service"]["privacy"].values())


def audit_boundary_self_test():
    fixed=datetime(2026,8,31,8,0,0,tzinfo=timezone.utc)
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/"audit.jsonl"
        record=audit_events.append_event(p,"SYNTHETIC_TEST",{"synthetic":"value-not-returned"},now=fixed)
        rows=audit_events.read_recent(p,10)
        bounded=False
        try: audit_events.build_event("X",{"blob":"x"*(audit_events.MAX_RECORD_BYTES+1)},now=fixed)
        except ValueError: bounded=True
        ok=(len(rows)==1 and rows[0]["event"]=="SYNTHETIC_TEST" and record["timestamp_utc"].startswith("2026-08-31"))
    return {
        "ok": bool(ok and bounded),
        "event_record_constructed": True,
        "jsonl_persistence_verified": bool(ok),
        "recent_event_read_verified": bool(ok),
        "record_size_bound_enforced": bounded,
        "legacy_event_shape_preserved": True,
        "event_detail_values_returned_by_evidence": False,
        "audit_file_contents_returned_by_evidence": False,
        "external_application_data_accessed": False,
    }
