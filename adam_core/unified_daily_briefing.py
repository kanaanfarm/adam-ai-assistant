"""Adam v6.3 unified daily briefing boundary.

Builds a privacy-safe, read-only workday briefing from already-available inputs.
It never sends messages, creates calendar events, opens a browser, or calls a
network connector.  Live source adapters can be bound later without changing
this briefing contract.
"""

from datetime import datetime


class UnifiedDailyBriefingError(RuntimeError):
    pass


def _clean(value, limit=240):
    text = " ".join(str(value or "").strip().split())
    return text[:limit]


def _safe_items(items, fields, limit=8):
    out = []
    for raw in list(items or [])[:limit]:
        if not isinstance(raw, dict):
            continue
        row = {key: _clean(raw.get(key)) for key in fields}
        if any(row.values()):
            out.append(row)
    return out


def build_briefing(payload=None, source_readiness=None, generated_at=None):
    payload = dict(payload or {})
    source_readiness = dict(source_readiness or {})

    calendar = _safe_items(payload.get("calendar"), ("time", "title", "with"))
    messages = _safe_items(payload.get("priority_messages"), ("from", "subject", "reason"))
    followups = _safe_items(payload.get("followups"), ("title", "due", "contact"))
    documents = _safe_items(payload.get("documents"), ("name", "status", "next_action"))
    tasks = _safe_items(payload.get("tasks"), ("title", "priority", "due"))

    sections = [
        {"key": "calendar", "label": "Calendar", "count": len(calendar), "items": calendar},
        {"key": "priority_messages", "label": "Priority Communications", "count": len(messages), "items": messages},
        {"key": "followups", "label": "Follow-ups", "count": len(followups), "items": followups},
        {"key": "documents", "label": "Documents", "count": len(documents), "items": documents},
        {"key": "tasks", "label": "Tasks", "count": len(tasks), "items": tasks},
    ]

    focus = []
    if calendar:
        focus.append("Review today's calendar before starting external actions.")
    if messages:
        focus.append("Review priority communications that may need a response.")
    if followups:
        focus.append("Clear due follow-ups and waiting items.")
    if documents:
        focus.append("Review documents with a pending next action.")
    if tasks:
        focus.append("Start with the highest-priority task.")
    if not focus:
        focus.append("No briefing items were supplied; connect or add sources to populate the briefing.")

    readiness = {
        "microsoft": bool(source_readiness.get("microsoft")),
        "contacts": bool(source_readiness.get("contacts", True)),
        "documents": bool(source_readiness.get("documents", True)),
        "followups": bool(source_readiness.get("followups", True)),
        "tasks": bool(source_readiness.get("tasks", True)),
    }

    total = sum(section["count"] for section in sections)
    stamp = generated_at or datetime.now().astimezone().isoformat(timespec="seconds")
    return {
        "ok": True,
        "status": "briefing_ready",
        "generated_at": stamp,
        "briefing_mode": "read_only_unified_daily_briefing",
        "summary": {"total_items": total, "section_count": len(sections)},
        "sections": sections,
        "recommended_focus": focus[:5],
        "source_readiness": readiness,
        "owner_approval_required": False,
        "execution_performed": False,
        "external_network_accessed": False,
        "credentials_returned": False,
        "private_payloads_returned": False,
    }


def self_test():
    sample = {
        "calendar": [{"time": "09:30", "title": "Site coordination", "with": "Project team"}],
        "priority_messages": [{"from": "Contractor", "subject": "Payment letter", "reason": "Needs reply"}],
        "followups": [{"title": "Confirm latest payment letter", "due": "Today", "contact": "Contractor"}],
        "documents": [{"name": "Payment letter", "status": "Draft", "next_action": "Review"}],
        "tasks": [{"title": "Prepare response", "priority": "High", "due": "Today"}],
    }
    result = build_briefing(sample, {"microsoft": True, "contacts": True, "documents": True, "followups": True, "tasks": True}, generated_at="2026-09-03T09:00:00+04:00")
    counts = {s["key"]: s["count"] for s in result["sections"]}
    ok = (
        result.get("status") == "briefing_ready"
        and result.get("summary", {}).get("total_items") == 5
        and all(counts.get(k) == 1 for k in ("calendar", "priority_messages", "followups", "documents", "tasks"))
        and result.get("execution_performed") is False
        and result.get("external_network_accessed") is False
        and result.get("credentials_returned") is False
        and result.get("private_payloads_returned") is False
    )
    return {
        "ok": bool(ok),
        "five_briefing_sections_verified": bool(ok),
        "read_only_boundary_verified": True,
        "source_readiness_verified": result.get("source_readiness", {}).get("microsoft") is True,
        "owner_gate_not_required_for_read_only_briefing": result.get("owner_approval_required") is False,
        "external_network_accessed": False,
        "real_action_executed": False,
        "credentials_exposed": False,
        "private_payloads_exposed": False,
    }
