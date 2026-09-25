"""Audit event persistence boundary for Adam Acquisition v2.6.

Operational callers may pass their existing details dictionary. This service owns
record construction and JSONL persistence, while buyer-facing evidence is
produced separately and never returns event-detail values.
"""
from __future__ import annotations
from datetime import datetime, timezone
import json

MAX_EVENT_NAME = 120
MAX_RECORD_BYTES = 64 * 1024


def build_event(event, details, *, now=None):
    name = str(event or "").strip()[:MAX_EVENT_NAME]
    if not name:
        raise ValueError("Audit event name is required.")
    if details is None:
        details = {}
    if not isinstance(details, dict):
        raise ValueError("Audit details must be a dictionary.")
    stamp = (now or datetime.now(timezone.utc)).isoformat(timespec="seconds")
    record = {"timestamp_utc": stamp, "event": name, "details": details}
    encoded = json.dumps(record, ensure_ascii=False, default=str).encode("utf-8")
    if len(encoded) > MAX_RECORD_BYTES:
        raise ValueError("Audit record exceeds the bounded size limit.")
    return record


def append_event(path, event, details, *, now=None):
    record = build_event(event, details, now=now)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
    return record


def read_recent(path, limit=100):
    limit = max(1, min(int(limit or 100), 500))
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines()[-limit:]:
        try:
            item = json.loads(line)
            if isinstance(item, dict):
                out.append(item)
        except Exception:
            continue
    return out
