"""Contact service boundary for Adam Acquisition v1.7.

This module owns contact persistence validation and safe upsert behavior without
Flask, AI providers, or connector credentials.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable


def normalize_contact(item):
    row = dict(item or {})
    row["name"] = str(row.get("name") or "").strip()
    row["phone"] = str(row.get("phone") or "").strip()
    row["email"] = str(row.get("email") or "").strip()
    row.setdefault("company", "")
    row.setdefault("language", "English")
    row.setdefault("notes", "")
    aliases = row.get("aliases")
    row["aliases"] = list(aliases) if isinstance(aliases, list) else []
    return row


def load_contacts(path: Path):
    try:
        p = Path(path)
        if not p.exists():
            return []
        raw = json.loads(p.read_text(encoding="utf-8"))
        if not isinstance(raw, list):
            return []
        return [normalize_contact(x) for x in raw if isinstance(x, dict)]
    except Exception:
        return []


def save_contacts(path: Path, items: Iterable[dict]):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    rows = [normalize_contact(x) for x in items if isinstance(x, dict)]
    temp = p.with_suffix(".tmp")
    temp.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    temp.replace(p)
    return rows


def upsert_contact(items, *, name, phone="", email="", new_id=""):
    name = str(name or "").strip()
    phone = str(phone or "").strip()
    email = str(email or "").strip()
    if not name:
        raise ValueError("Name is required.")
    if not phone and not email:
        raise ValueError("Enter at least a phone number or email address.")

    rows = [normalize_contact(x) for x in (items or []) if isinstance(x, dict)]
    existing = next((c for c in rows if str(c.get("name") or "").casefold() == name.casefold()), None)
    if existing:
        if phone:
            existing["phone"] = phone
        if email:
            existing["email"] = email
        return rows, existing, False

    created = normalize_contact({
        "id": str(new_id or ""),
        "name": name,
        "phone": phone,
        "email": email,
        "company": "",
        "language": "English",
        "notes": "",
        "aliases": [],
    })
    rows.append(created)
    return rows, created, True
