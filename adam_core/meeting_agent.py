"""Governed Meeting Agent foundation for Adam Acquisition v4.4.

This module deliberately does not join a live meeting or impersonate a user.
It converts bounded transcript segments into a privacy-safe meeting plan and
requires explicit owner approval before Adam may speak, commit, invite or send.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable
import re

MAX_SEGMENTS = 120
MAX_SEGMENT_CHARS = 1200
MAX_ACTION_ITEMS = 20
CONSEQUENTIAL_MEETING_ACTIONS = {"speak", "commit", "invite", "send_followup"}
SAFE_MEETING_ACTIONS = {"listen", "summarize", "extract_action_items", "answer_from_approved_knowledge"}

class MeetingAgentError(RuntimeError):
    pass

def _clean(v: Any, limit: int) -> str:
    return " ".join(str(v or "").split())[:limit]

@dataclass(frozen=True)
class MeetingAction:
    action: str
    content: str = ""
    owner_approved: bool = False
    @property
    def consequential(self) -> bool:
        return self.action in CONSEQUENTIAL_MEETING_ACTIONS
    def public_dict(self) -> dict:
        return {"action": self.action, "consequential": self.consequential,
                "owner_approved": bool(self.owner_approved), "content_present": bool(self.content)}

def ingest_transcript(segments: list[dict] | None) -> dict:
    bounded=[]
    for raw in list(segments or [])[:MAX_SEGMENTS]:
        text=_clean(raw.get("text"), MAX_SEGMENT_CHARS)
        if text:
            bounded.append({"speaker_present": bool(_clean(raw.get("speaker"),80)), "text": text})
    return {"ok": True, "segment_count": len(bounded), "segments": bounded}

ACTION_PREFIX_RE = re.compile(r"^\s*(?:[-*•]\s*)?(?:action(?:\s+item)?|todo|to-do|follow[- ]?up)\s*[:\-]\s*\S+", re.IGNORECASE)
COMMITMENT_RE = re.compile(r"\b(?:i|we|[A-Za-z][A-Za-z0-9_.-]*)\s+(?:will|shall|must|need(?:s)?\s+to|is\s+to|are\s+to)\s+\w+", re.IGNORECASE)
IMPERATIVE_ACTION_RE = re.compile(r"^\s*(?:[-*•]\s*)?(?:provide|send|submit|prepare|check|review|update|issue|coordinate|confirm|complete|close|revise|share|deliver|follow\s+up)\b", re.IGNORECASE)

def _looks_like_action_item(text: str) -> bool:
    """Recognize explicit and natural meeting commitments without an AI/network call."""
    t = _clean(text, MAX_SEGMENT_CHARS)
    if not t:
        return False
    low = t.lower()
    return bool(
        ACTION_PREFIX_RE.search(t)
        or COMMITMENT_RE.search(t)
        or IMPERATIVE_ACTION_RE.search(t)
        or "follow up" in low
    )

def build_meeting_notes(segments: list[dict] | None) -> dict:
    data=ingest_transcript(segments)
    texts=[x["text"] for x in data["segments"]]
    action_items=[]
    for t in texts:
        if _looks_like_action_item(t):
            action_items.append(t[:MAX_SEGMENT_CHARS])
        if len(action_items)>=MAX_ACTION_ITEMS: break
    return {"ok": True, "segment_count": len(texts), "summary_available": bool(texts),
            "action_item_count": len(action_items), "action_items": action_items}

def execute_meeting_action(raw: dict, adapter: Callable[[MeetingAction], Any]) -> dict:
    action=_clean(raw.get("action"),60).lower()
    if action not in SAFE_MEETING_ACTIONS | CONSEQUENTIAL_MEETING_ACTIONS:
        raise MeetingAgentError("Unsupported meeting action.")
    item=MeetingAction(action=action, content=_clean(raw.get("content"),MAX_SEGMENT_CHARS),
                       owner_approved=raw.get("owner_approved") is True)
    if item.consequential and not item.owner_approved:
        return {"ok":False,"status":"approval_required","action":action,"owner_gate_preserved":True,
                "executed":False,"private_values_returned":False}
    result=adapter(item)
    return {"ok":bool(result is not False),"status":"executed","action":action,"consequential":item.consequential,
            "owner_gate_preserved":True,"executed":True,"private_values_returned":False}

def public_manifest() -> dict:
    return {
        "meeting_listen_and_notes": True,
        "action_item_extraction": True,
        "answer_from_approved_knowledge": True,
        "ai_identity_required_for_speaking": True,
        "user_impersonation_allowed": False,
        "per_action_owner_approval": True,
        "safe_actions": sorted(SAFE_MEETING_ACTIONS),
        "consequential_actions": sorted(CONSEQUENTIAL_MEETING_ACTIONS),
        "bounds":{"max_segments":MAX_SEGMENTS,"max_segment_chars":MAX_SEGMENT_CHARS,"max_action_items":MAX_ACTION_ITEMS},
        "privacy":{"transcript_exposed_in_buyer_evidence":False,"meeting_links_exposed_in_buyer_evidence":False,
                   "participant_identity_exposed_in_buyer_evidence":False,"credentials_stored":False},
        "live_meeting_join_enabled": False,
    }
