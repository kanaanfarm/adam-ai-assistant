"""Privacy-safe buyer evidence pack helpers for Adam Acquisition v1.4.

The evidence pack is designed for acquisition demos and technical diligence.
It intentionally contains only capability-level and governance metadata.
No credentials, contact details, message bodies, attachment contents, prompts,
or private memory values are included.
"""
from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
import json


PRIVACY_FLAGS = {
    "credentials_exposed": False,
    "contact_details_exposed": False,
    "message_bodies_exposed": False,
    "attachment_contents_exposed": False,
    "private_memory_exposed": False,
}


def _canonical_sha256(payload):
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return sha256(raw).hexdigest()


def build_evidence_pack(*, version, acquisition, governance):
    """Build a buyer-safe diligence snapshot with a tamper-evident fingerprint."""
    acq = dict(acquisition or {})
    gov = dict(governance or {})
    scenarios = []
    for item in acq.get("demo_scenarios") or []:
        scenarios.append({
            "id": item.get("id"),
            "name": item.get("name"),
            "approval_required": bool(item.get("approval_required")),
            "evidence_endpoints": list(item.get("evidence_endpoints") or []),
        })

    receipts = []
    for item in gov.get("receipts") or []:
        receipts.append({
            "workflow_id": item.get("workflow_id"),
            "status": item.get("status"),
            "approval_events": int(item.get("approval_events") or 0),
            "completion_events": int(item.get("completion_events") or 0),
            "receipt_sha256": item.get("receipt_sha256"),
        })

    core = {
        "schema": "adam-acquisition-evidence/v1",
        "product": "Adam Acquisition",
        "version": version,
        "positioning": acq.get("positioning"),
        "all_core_checks_pass": bool(acq.get("all_core_checks_pass")),
        "readiness_checks": dict(acq.get("readiness_checks") or {}),
        "governance_summary": {
            "workflow_count": int(gov.get("workflow_count") or 0),
            "completed_workflows": int(gov.get("completed_workflows") or 0),
            "attention_required": int(gov.get("attention_required") or 0),
            "approval_events": int(gov.get("approval_events") or 0),
            "completion_events": int(gov.get("completion_events") or 0),
            "record_sources": dict(gov.get("record_sources") or {}),
        },
        "policy": dict(gov.get("policy") or {}),
        "demo_scenarios": scenarios,
        "workflow_receipts": receipts,
        "privacy": dict(PRIVACY_FLAGS),
    }
    fingerprint = _canonical_sha256(core)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "evidence": core,
        "evidence_sha256": fingerprint,
    }


def evidence_pack_is_privacy_safe(pack):
    """Defensive allowlist-style check used by tests and buyer-readiness UI."""
    text = json.dumps(pack or {}, sort_keys=True, default=str).lower()
    forbidden = (
        "api_key", "access_token", "refresh_token", "client_secret", "password",
        "phone_number", "contact_email", "message_body", "attachment_body",
        "private_memory_value", "prompt_text",
    )
    return not any(term in text for term in forbidden)
