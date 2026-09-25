"""Privacy-safe meeting memory foundation for Adam Acquisition v4.7.

Stores only bounded structured meeting outcomes supplied by the caller. Raw
transcripts, meeting links, credentials and participant identities are not part
of the memory record. Persistence is injected by the deployment.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable

MAX_SUMMARY_CHARS = 1800
MAX_DECISIONS = 20
MAX_ACTION_ITEMS = 20
MAX_ITEM_CHARS = 300

class MeetingMemoryError(RuntimeError):
    pass

def _clean(value: Any, limit: int) -> str:
    return " ".join(str(value or "").split())[:limit]

def _bounded_items(values: Any, maximum: int) -> list[str]:
    if not isinstance(values, list):
        return []
    out=[]
    for value in values[:maximum]:
        text=_clean(value, MAX_ITEM_CHARS)
        if text: out.append(text)
    return out

@dataclass(frozen=True)
class MeetingMemoryRecord:
    summary: str
    decisions: tuple[str, ...]
    action_items: tuple[str, ...]

    def public_receipt(self) -> dict:
        return {
            "summary_present": bool(self.summary),
            "decision_count": len(self.decisions),
            "action_item_count": len(self.action_items),
            "raw_transcript_stored": False,
            "meeting_reference_stored": False,
            "participant_identity_stored": False,
            "private_values_returned": False,
        }

def build_memory_record(raw: dict | None) -> MeetingMemoryRecord:
    raw=raw or {}
    summary=_clean(raw.get("summary"), MAX_SUMMARY_CHARS)
    if not summary:
        raise MeetingMemoryError("A bounded meeting summary is required.")
    return MeetingMemoryRecord(
        summary=summary,
        decisions=tuple(_bounded_items(raw.get("decisions"), MAX_DECISIONS)),
        action_items=tuple(_bounded_items(raw.get("action_items"), MAX_ACTION_ITEMS)),
    )

def save_memory(raw: dict | None, store: Callable[[MeetingMemoryRecord], Any]) -> dict:
    record=build_memory_record(raw)
    result=store(record)
    return {
        "ok": result is not False,
        "status": "meeting_memory_saved",
        "receipt": record.public_receipt(),
        "persistence_injected": True,
        "owner_private_store_required": True,
    }

def recall_memory(query: str, search: Callable[[str], list[dict] | None]) -> dict:
    q=_clean(query, 500)
    if not q:
        raise MeetingMemoryError("A recall query is required.")
    rows=search(q) or []
    # Buyer-safe response exposes counts only. Operational adapters may use the
    # private rows internally but must not put raw meeting memory in evidence.
    return {
        "ok": True,
        "status": "meeting_memory_recalled",
        "matches_found": min(len(rows), 20),
        "memory_contents_returned_in_buyer_evidence": False,
        "private_values_returned": False,
    }

def public_manifest() -> dict:
    return {
        "meeting_memory_foundation": True,
        "structured_outcomes_only": True,
        "bounded_summary": True,
        "decision_memory": True,
        "action_item_memory": True,
        "injected_private_persistence": True,
        "cross_meeting_recall_contract": True,
        "bounds": {
            "max_summary_chars": MAX_SUMMARY_CHARS,
            "max_decisions": MAX_DECISIONS,
            "max_action_items": MAX_ACTION_ITEMS,
            "max_item_chars": MAX_ITEM_CHARS,
        },
        "privacy": {
            "raw_transcript_stored": False,
            "meeting_links_stored": False,
            "participant_identity_stored": False,
            "credentials_stored": False,
            "memory_contents_exposed_in_buyer_evidence": False,
        },
    }
