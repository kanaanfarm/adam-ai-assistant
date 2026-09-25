"""Follow-up service boundary for Adam Acquisition v1.7.

Owns persistence, due parsing, status projection, and record creation without
Flask or external connector dependencies.
"""
from __future__ import annotations

import json
import re
import uuid
from datetime import datetime, timedelta
from pathlib import Path


def load_followups(path: Path):
    try:
        p = Path(path)
        if not p.exists():
            return []
        raw = json.loads(p.read_text(encoding="utf-8"))
        return raw if isinstance(raw, list) else []
    except Exception:
        return []


def save_followups(path: Path, rows):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    values = [dict(x) for x in (rows or []) if isinstance(x, dict)]
    temp = p.with_suffix(".tmp")
    temp.write_text(json.dumps(values, ensure_ascii=False, indent=2), encoding="utf-8")
    temp.replace(p)
    return values


def add_followup(path: Path, title, contact_name="", contact_email="", due_at="", source="Adam Main", *, now=None, item_id=None):
    rows = load_followups(path)
    now = now or datetime.now()
    item = {
        "id": str(item_id or uuid.uuid4().hex),
        "title": str(title or "").strip(),
        "contact_name": str(contact_name or "").strip(),
        "contact_email": str(contact_email or "").strip(),
        "due_at": str(due_at or "").strip(),
        "source": str(source or "Adam Main").strip(),
        "completed": False,
        "created_at": now.isoformat(timespec="seconds"),
    }
    rows.append(item)
    save_followups(path, rows)
    return item


def parse_due(text, *, now=None):
    low = str(text or "").lower()
    now = now or datetime.now()
    m = re.search(r"\b(?:after|in|within)\s+(\d+)\s+(day|days|hour|hours)\b", low)
    if m:
        n = int(m.group(1))
        due = now + (timedelta(days=n) if m.group(2).startswith("day") else timedelta(hours=n))
        return due.isoformat(timespec="minutes")
    if "tomorrow" in low:
        return (now + timedelta(days=1)).replace(hour=9, minute=0, second=0, microsecond=0).isoformat(timespec="minutes")
    return ""


def status(item, *, now=None):
    if bool((item or {}).get("completed")):
        return "Completed"
    now = now or datetime.now()
    due_raw = str((item or {}).get("due_at") or (item or {}).get("due") or "").strip()
    if not due_raw:
        return "Upcoming"
    try:
        due = datetime.fromisoformat(due_raw.replace("Z", "+00:00"))
        if due.tzinfo is not None:
            due = due.astimezone().replace(tzinfo=None)
    except Exception:
        return "Upcoming"
    if due.date() == now.date():
        return "Due Today"
    if due < now:
        return "Overdue"
    return "Upcoming"


def public_item(item, *, now=None):
    row = dict(item or {})
    row["due"] = str(row.get("due_at") or row.get("due") or "")
    row["status"] = status(row, now=now)
    return row
