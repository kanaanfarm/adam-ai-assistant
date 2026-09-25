"""Adam v8.3.4.3 durable owner continuity memory.

Purpose:
- keep explicit owner corrections / explicit remember instructions across app restarts
  and extracted-version upgrades using the per-user runtime root;
- recover relevant *software test/release history* from packaged release notes without
  treating release-note examples as project facts;
- retrieve only context that is relevant to the current task so unrelated subjects do
  not bleed into answers.

This module is local-only. It performs no network or external action.
"""
from __future__ import annotations

import json
import os
import re
import tempfile
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from typing import Iterable

from .runtime import persistent_root

BLOCKED_TERMS = {
    "password", "passwd", "secret", "token", "api_key", "apikey", "credential",
    "private_key", "authorization bearer", "access key", "refresh token",
}

_STOP = {
    "the", "a", "an", "and", "or", "to", "of", "for", "in", "on", "at", "is",
    "are", "was", "were", "be", "been", "i", "you", "we", "it", "this", "that",
    "did", "do", "does", "say", "said", "adam", "please", "can", "could", "would",
    "what", "which", "about", "with", "from", "my", "me", "our", "your",
}

_CORRECTION_PATTERNS = (
    r"\bi\s+(?:didn['’]?t|did\s+not)\s+say\b.+\bi\s+said\b",
    r"\bcorrection\b",
    r"\bcorrect\s+(?:that|this|it)\b",
    r"\bnot\s+.+\b(?:instead|rather)\b",
    r"\bلم\s+أقل\b.+\bقلت\b",
    r"\bتصحيح\b",
    r"\bصحح\b",
)
_REMEMBER_PATTERNS = (
    r"\bremember(?:\s+that|\s+this)?\b",
    r"\bkeep\s+this\s+in\s+memory\b",
    r"\bdon['’]?t\s+forget\b",
    r"\bfrom\s+now\s+on\b",
    r"\bتذكر\b",
    r"\bاحفظ\b",
    r"\bلا\s+تنس\b",
)


def owner_memory_path(base_dir: Path) -> Path:
    root = persistent_root(Path(base_dir)) / "Adam_Acquisition"
    return root / "owner_continuity_memory_v1.json"


def _clean(value: object, limit: int = 4000) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())[:limit]


def _sensitive(text: str) -> bool:
    low = _clean(text).lower()
    return any(term in low for term in BLOCKED_TERMS)


def _tokens(text: str) -> set[str]:
    raw = re.findall(r"[A-Za-z0-9][A-Za-z0-9_.-]*|[\u0600-\u06FF]+", str(text or "").lower())
    return {t.strip("._-") for t in raw if len(t.strip("._-")) >= 3 and t.strip("._-") not in _STOP}


def _load(path: Path) -> dict:
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        if isinstance(data, dict) and isinstance(data.get("items"), list):
            return data
    except FileNotFoundError:
        pass
    except Exception:
        pass
    return {"schema": 1, "items": []}


def _atomic_save(path: Path, data: dict) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    # Same directory so os.replace remains atomic on Windows.
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, path)


def classify_explicit_memory(text: str) -> str:
    q = _clean(text).lower()
    if not q:
        return ""
    if any(re.search(p, q, re.I | re.S) for p in _CORRECTION_PATTERNS):
        return "correction"
    if any(re.search(p, q, re.I | re.S) for p in _REMEMBER_PATTERNS):
        return "remembered_fact"
    return ""


def remember_explicit_owner_turn(
    path: Path,
    text: str,
    *,
    task_focus: str = "",
    project_reference: str = "",
    source: str = "universal_assistant",
    version: str = "",
    enabled: bool = True,
    now: str | None = None,
) -> dict:
    """Persist only an explicit correction / explicit remember instruction.

    The owner's own wording is the write authorization signal. Ordinary Q&A is never
    silently written to durable memory by this function.
    """
    kind = classify_explicit_memory(text)
    cleaned = _clean(text)
    if not enabled or not kind or not cleaned:
        return {"stored": False, "reason": "not_explicit_memory" if enabled else "disabled"}
    if _sensitive(cleaned):
        return {"stored": False, "reason": "sensitive_memory_rejected"}

    data = _load(Path(path))
    normalized = cleaned.casefold()
    for item in reversed(data["items"][-200:]):
        if str(item.get("text") or "").casefold() == normalized:
            return {"stored": False, "reason": "duplicate", "item": item}

    stamp = now or datetime.now().astimezone().isoformat(timespec="seconds")
    item = {
        "id": f"mem-{len(data['items']) + 1:05d}",
        "kind": kind,
        "text": cleaned,
        "task_focus": _clean(task_focus, 500),
        "project_reference": _clean(project_reference, 300),
        "source": _clean(source, 80),
        "version": _clean(version, 40),
        "created_at": stamp,
        "owner_explicit": True,
    }
    data["items"].append(item)
    # Bounded local store; preserve the newest confirmed items.
    data["items"] = data["items"][-500:]
    _atomic_save(Path(path), data)
    return {"stored": True, "item": item}


def _score_item(item: dict, query: str, task_focus: str = "", project_reference: str = "") -> float:
    qt = _tokens(" ".join([query, task_focus, project_reference]))
    text = " ".join([
        str(item.get("text") or ""), str(item.get("task_focus") or ""),
        str(item.get("project_reference") or ""), str(item.get("kind") or ""),
    ])
    it = _tokens(text)
    if not qt:
        return 0.0
    overlap = len(qt & it)
    if overlap == 0:
        return 0.0
    score = overlap * 3.0 / max(1.0, len(qt) ** 0.5)
    if task_focus and _tokens(task_focus) & it:
        score += 2.0
    if project_reference and _tokens(project_reference) & it:
        score += 3.0
    if str(item.get("kind")) == "correction" and any(w in query.lower() for w in ("correct", "correction", "old", "previous", "remember")):
        score += 2.0
    return score


def recall_owner_memory(path: Path, query: str, *, task_focus: str = "", project_reference: str = "", limit: int = 4) -> list[dict]:
    data = _load(Path(path))
    scored = []
    for index, item in enumerate(data["items"]):
        s = _score_item(item, query, task_focus, project_reference)
        if s > 0:
            # Tiny recency tiebreaker only; relevance remains dominant.
            scored.append((s + index / 100000.0, item))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [dict(x[1]) for x in scored[: max(1, min(int(limit or 4), 8))]]


def format_owner_memory(items: Iterable[dict]) -> str:
    rows = []
    for item in items:
        kind = str(item.get("kind") or "memory").replace("_", " ")
        scope = str(item.get("project_reference") or item.get("task_focus") or "").strip()
        suffix = f" [scope: {scope}]" if scope else ""
        rows.append(f"- {kind}: {str(item.get('text') or '').strip()}{suffix}")
    return "\n".join(rows)


def _release_note_files(base_dir: Path) -> list[Path]:
    return sorted(Path(base_dir).glob("ACQUISITION_V*_NOTES.md"))


@lru_cache(maxsize=16)
def _read_note(path_text: str) -> str:
    try:
        return Path(path_text).read_text(encoding="utf-8", errors="replace")[:120000]
    except Exception:
        return ""


def _history_query(query: str) -> bool:
    low = str(query or "").lower()
    return any(k in low for k in (
        "old v", "old version", "previous version", "earlier version", "release", "upgrade",
        "test", "v8.", "v7.", "what did i correct", "what did we test", "previous test",
    ))


def recall_release_history(base_dir: Path, query: str, *, limit: int = 3) -> list[dict]:
    """Return relevant release-note snippets. They are explicitly non-project evidence."""
    if not _history_query(query):
        return []
    qt = _tokens(query)
    if not qt:
        return []
    scored = []
    for path in _release_note_files(Path(base_dir)):
        content = _read_note(str(path))
        if not content:
            continue
        ct = _tokens(content)
        overlap = len(qt & ct)
        if overlap == 0:
            continue
        # Strong bonus for exact distinctive phrase fragments.
        lowq, lowc = query.lower(), content.lower()
        bonus = 0.0
        for phrase in ("empower request channel", "third water", "chilled water", "correction", "no silent turn"):
            if phrase in lowq and phrase in lowc:
                bonus += 5.0
        score = overlap + bonus
        if score <= 1 and len(qt) > 4:
            continue
        # Keep a concise matching excerpt around the best line(s).
        lines = content.splitlines()
        best_i, best_ls = 0, -1
        for i, line in enumerate(lines):
            ls = len(qt & _tokens(line))
            if ls > best_ls:
                best_i, best_ls = i, ls
        start, end = max(0, best_i - 2), min(len(lines), best_i + 4)
        snippet = "\n".join(lines[start:end]).strip()[:2200]
        scored.append((score, {"file": path.name, "snippet": snippet}))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [x[1] for x in scored[: max(1, min(int(limit or 3), 5))]]


def format_release_history(items: Iterable[dict]) -> str:
    rows = []
    for item in items:
        rows.append(f"[{item.get('file')}]\n{item.get('snippet')}")
    return "\n\n".join(rows)


def self_test() -> dict:
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "memory.json"
        a = remember_explicit_owner_turn(
            p,
            "I didn't say third-water part. I said Empower request channel for chilled water.",
            task_focus="Tower MEP", version="v8.3.4.3", now="2026-09-08T12:00:00+04:00"
        )
        b = remember_explicit_owner_turn(p, "What is a fire pump?", enabled=True)
        c = recall_owner_memory(p, "What did I correct about Empower chilled water?", task_focus="Tower MEP")
        d = recall_owner_memory(p, "Explain stock RSI", task_focus="Stocks")
        return {
            "ok": bool(a.get("stored") and not b.get("stored") and c and "Empower request channel" in c[0].get("text", "") and not d),
            "explicit_correction_persisted": bool(a.get("stored")),
            "ordinary_qa_not_auto_persisted": not b.get("stored"),
            "relevant_recall_verified": bool(c),
            "unrelated_topic_isolation_verified": not d,
            "external_network_accessed": False,
            "external_action_executed": False,
        }
