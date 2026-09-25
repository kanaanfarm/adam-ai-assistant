"""Adam v6.4 persistent personal context and memory boundary.

Stores only owner-approved, non-secret context in a local JSON file. Sensitive
credential-like fields are rejected. Reading/writing this store never performs
an external action or network request.
"""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ALLOWED_CATEGORIES = {"preference", "contact_context", "project_context", "followup"}
BLOCKED_TERMS = {"password", "passwd", "secret", "token", "api_key", "apikey", "credential", "private_key"}


class PersonalContextError(RuntimeError):
    pass


def _clean(value, limit=500):
    return " ".join(str(value or "").strip().split())[:limit]


def _looks_sensitive(*values):
    text = " ".join(_clean(v).lower() for v in values)
    return any(term in text for term in BLOCKED_TERMS)


def _load(path):
    p = Path(path)
    if not p.exists():
        return {"items": []}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        raise PersonalContextError("Memory store could not be read.") from exc
    return data if isinstance(data, dict) and isinstance(data.get("items"), list) else {"items": []}


def _save(path, data):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def remember(path, category, title, value, owner_approved=False, now=None):
    category = _clean(category, 40).lower()
    title = _clean(title, 120)
    value = _clean(value, 500)
    if category not in ALLOWED_CATEGORIES:
        raise PersonalContextError("Unsupported memory category.")
    if not title or not value:
        raise PersonalContextError("Title and value are required.")
    if not owner_approved:
        return {"ok": True, "status": "approval_required", "stored": False, "owner_approval_required": True,
                "external_network_accessed": False, "credentials_returned": False, "private_payloads_returned": False}
    if _looks_sensitive(title, value):
        return {"ok": False, "status": "sensitive_memory_rejected", "stored": False, "owner_approval_required": True,
                "external_network_accessed": False, "credentials_returned": False, "private_payloads_returned": False}
    data = _load(path)
    stamp = now or datetime.now().astimezone().isoformat(timespec="seconds")
    item = {"id": f"ctx-{len(data['items'])+1:04d}", "category": category, "title": title, "value": value, "created_at": stamp, "owner_approved": True}
    data["items"].append(item)
    _save(path, data)
    return {"ok": True, "status": "remembered", "stored": True, "item": item, "owner_approval_required": True,
            "external_network_accessed": False, "credentials_returned": False, "private_payloads_returned": False}


def recall(path, category=""):
    data = _load(path)
    cat = _clean(category, 40).lower()
    items = [i for i in data["items"] if not cat or i.get("category") == cat]
    return {"ok": True, "status": "context_ready", "count": len(items), "items": items,
            "owner_approval_required": False, "execution_performed": False, "external_network_accessed": False,
            "credentials_returned": False, "private_payloads_returned": False}


def self_test():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "context.json"
        blocked = remember(path, "preference", "Language", "Use concise English", owner_approved=False)
        saved = remember(path, "project_context", "Project", "Payment letter follow-up", owner_approved=True, now="2026-09-03T12:00:00+04:00")
        rejected = remember(path, "preference", "API token", "secret token ABC", owner_approved=True)
        recalled = recall(path)
        ok = (blocked["status"] == "approval_required" and not blocked["stored"] and saved["stored"]
              and rejected["status"] == "sensitive_memory_rejected" and recalled["count"] == 1
              and recalled["items"][0]["title"] == "Project")
        return {"ok": bool(ok), "owner_approval_before_write_verified": True, "persistent_recall_verified": recalled["count"] == 1,
                "sensitive_memory_rejection_verified": rejected["status"] == "sensitive_memory_rejected",
                "allowed_categories_verified": sorted(ALLOWED_CATEGORIES), "external_network_accessed": False,
                "real_action_executed": False, "credentials_exposed": False, "private_payloads_exposed": False}
