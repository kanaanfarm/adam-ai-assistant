"""Buyer-safe governance and audit helpers for Adam Acquisition v1.2.

No credentials, attachment bodies, email bodies, phone numbers, or contact details
are included in the governance views produced here.
"""
from __future__ import annotations
from hashlib import sha256
import json

APPROVAL_GATED_STEPS = {"email_review", "whatsapp_review", "calendar_review"}


def policy_manifest():
    return {
        "owner_approval_required_for": sorted(APPROVAL_GATED_STEPS),
        "execution_confirmation_required": True,
        "followup_requires_successful_delivery": True,
        "attachment_context_exposed": False,
        "credentials_exposed": False,
    }


def _safe_event(event):
    # Deliberately omit arbitrary event details; they may contain connector data.
    return {
        "at": event.get("at"),
        "type": event.get("type"),
        "step": event.get("step"),
    }


def workflow_receipt(row):
    steps = [
        {
            "name": s.get("name"),
            "status": s.get("status"),
            "approval_required": bool(s.get("approval_required")),
        }
        for s in row.get("steps", [])
    ]
    events = [_safe_event(e) for e in row.get("events", [])[-50:]]
    approval_events = sum(1 for e in events if e.get("type") == "owner_approved")
    completion_events = sum(1 for e in events if e.get("type") == "step_completed")
    payload = {
        "workflow_id": row.get("id"),
        "status": row.get("status"),
        "created_at": row.get("created_at"),
        "updated_at": row.get("updated_at"),
        "steps": steps,
        "events": events,
        "approval_events": approval_events,
        "completion_events": completion_events,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    payload["receipt_sha256"] = sha256(canonical).hexdigest()
    return payload



def followup_as_workflow_record(item):
    """Convert a Follow-Up Queue item into a privacy-safe workflow-shaped record.

    Deliberately excludes title, contact name, email, phone, draft/body and source.
    """
    raw_id = str(item.get("id") or "")
    completed = bool(item.get("completed"))
    created = item.get("created_at")
    updated = item.get("completed_at") or item.get("updated_at") or created
    step_status = "completed" if completed else "pending"
    events = [{"at": created, "type": "workflow_created", "step": None}]
    if completed:
        events.append({"at": updated, "type": "step_completed", "step": "followup"})
    return {
        "id": "followup_" + raw_id,
        "status": "completed" if completed else "pending",
        "created_at": created,
        "updated_at": updated,
        "steps": [{"name": "followup", "status": step_status, "approval_required": False}],
        "events": events,
    }

def governance_summary(rows):
    receipts = [workflow_receipt(r) for r in rows]
    return {
        "workflow_count": len(receipts),
        "completed_workflows": sum(1 for r in receipts if r.get("status") == "completed"),
        "attention_required": sum(1 for r in receipts if r.get("status") == "attention_required"),
        "approval_events": sum(r.get("approval_events", 0) for r in receipts),
        "completion_events": sum(r.get("completion_events", 0) for r in receipts),
        "policy": policy_manifest(),
        "receipts": receipts[-25:][::-1],
    }
