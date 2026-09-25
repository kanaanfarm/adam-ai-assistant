"""Adam Acquisition v1.1 orchestration primitives.

This module is intentionally provider-neutral. It manages workflow state,
approval gates, event history, and buyer-safe summaries. Connected services
remain in app.py during this incremental migration.
"""
from __future__ import annotations
from datetime import datetime
from pathlib import Path
import json
import uuid

CONSEQUENTIAL_STEPS = {"email_review", "whatsapp_review", "calendar_review"}

def utcish_now():
    return datetime.now().isoformat(timespec="seconds")

def new_workflow(instruction, steps, attachment_context=""):
    return {
        "id": uuid.uuid4().hex[:12],
        "instruction": str(instruction or "")[:12000],
        "steps": [
            {
                "name": str(name),
                "status": "pending",
                "approval_required": str(name) in CONSEQUENTIAL_STEPS,
            }
            for name in steps
        ],
        "attachment_context": str(attachment_context or "")[:100000],
        "created_at": utcish_now(),
        "updated_at": utcish_now(),
        "status": "planned",
        "events": [{"at": utcish_now(), "type": "workflow_created"}],
    }

def update_step(row, step_name, status, *, event_type=None, details=None):
    found = False
    for step in row.get("steps", []):
        if step.get("name") == step_name:
            step["status"] = status
            found = True
            break
    if not found:
        return False
    row["updated_at"] = utcish_now()
    statuses = [s.get("status") for s in row.get("steps", [])]
    if statuses and all(s == "completed" for s in statuses):
        row["status"] = "completed"
    elif any(s in ("completed", "approved", "executing") for s in statuses):
        row["status"] = "in_progress"
    else:
        row["status"] = "planned"
    if event_type:
        event = {"at": utcish_now(), "type": event_type, "step": step_name}
        if details:
            event["details"] = details
        row.setdefault("events", []).append(event)
    return True

def mark_approved(row, step_name):
    return update_step(row, step_name, "approved", event_type="owner_approved")

def mark_completed(row, step_name, details=None):
    return update_step(row, step_name, "completed", event_type="step_completed", details=details)

def mark_failed(row, step_name, details=None):
    ok = update_step(row, step_name, "failed", event_type="step_failed", details=details)
    if ok:
        row["status"] = "attention_required"
    return ok

def public_summary(row):
    return {
        "id": row.get("id"),
        "instruction": row.get("instruction"),
        "status": row.get("status"),
        "created_at": row.get("created_at"),
        "updated_at": row.get("updated_at"),
        "steps": [
            {
                "name": s.get("name"),
                "status": s.get("status"),
                "approval_required": bool(s.get("approval_required")),
            } for s in row.get("steps", [])
        ],
        "events": row.get("events", [])[-20:],
    }
