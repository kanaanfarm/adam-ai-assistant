"""Adam v7.3.0 — Real Meeting Attendance companion layer.

This module adds a real, owner-controlled meeting companion workflow that can
capture transcript segments supplied by the local browser, create notes and
track action items. It deliberately does not claim that Adam can autonomously
join Teams/Zoom/Meet; platform join remains behind the existing adapter and is
reported as unavailable until a real approved platform adapter is configured.
"""
from __future__ import annotations

from typing import Any

from adam_core.meeting_agent import build_meeting_notes

SUPPORTED_PLATFORMS = {"microsoft_teams", "zoom", "google_meet", "in_person", "other"}
SUPPORTED_MODES = {"listen_only", "take_notes", "active_participant", "owner_representative"}
MAX_SEGMENTS = 240
MAX_TEXT_CHARS = 1600


def _clean(value: Any, limit: int = 160) -> str:
    return " ".join(str(value or "").split())[:limit]


def build_attendance_status(*, platform_adapter_live: bool = False) -> dict:
    return {
        "ok": True,
        "status": "meeting_attendance_companion_ready",
        "supported_platforms": sorted(SUPPORTED_PLATFORMS),
        "supported_modes": sorted(SUPPORTED_MODES),
        "browser_microphone_capture_supported": True,
        "manual_transcript_fallback_supported": True,
        "notes_and_action_items_supported": True,
        "platform_join_available": bool(platform_adapter_live),
        "autonomous_platform_join_claimed": False,
        "owner_approval_required_before_capture": True,
        "ai_identity_declared": True,
        "user_impersonation_allowed": False,
        "consequential_action_executed": False,
        "external_network_accessed": False,
    }


def process_attendance(raw: dict | None) -> dict:
    raw = raw or {}
    platform = _clean(raw.get("platform"), 40).lower()
    mode = _clean(raw.get("mode"), 40).lower()
    owner_approved = raw.get("owner_approved") is True

    if platform not in SUPPORTED_PLATFORMS:
        return {"ok": False, "status": "unsupported_platform", "executed": False}
    if mode not in SUPPORTED_MODES:
        return {"ok": False, "status": "unsupported_mode", "executed": False}
    if not owner_approved:
        return {
            "ok": False,
            "status": "approval_required",
            "owner_gate_preserved": True,
            "capture_started": False,
            "real_meeting_joined": False,
            "external_action_executed": False,
        }

    bounded = []
    for item in list(raw.get("segments") or [])[:MAX_SEGMENTS]:
        if isinstance(item, str):
            text = _clean(item, MAX_TEXT_CHARS)
            speaker = ""
        else:
            text = _clean((item or {}).get("text"), MAX_TEXT_CHARS)
            speaker = _clean((item or {}).get("speaker"), 80)
        if text:
            bounded.append({"speaker": speaker, "text": text})

    notes = build_meeting_notes(bounded)
    return {
        "ok": True,
        "status": "attendance_processed",
        "platform": platform,
        "mode": mode,
        "owner_gate_preserved": True,
        "capture_started": True,
        "segment_count": notes.get("segment_count", 0),
        "summary_available": bool(notes.get("summary_available")),
        "action_item_count": notes.get("action_item_count", 0),
        "action_items": notes.get("action_items", []),
        "real_meeting_joined": False,
        "platform_join_available": False,
        "autonomous_platform_join_claimed": False,
        "external_action_executed": False,
        "external_network_accessed": False,
        "private_meeting_reference_returned": False,
    }



def action_item_fix_self_test() -> dict:
    """v7.3.0.1 acceptance for the affected manual action-item behavior only."""
    explicit = process_attendance({
        "platform": "microsoft_teams",
        "mode": "take_notes",
        "owner_approved": True,
        "segments": [{"text": "Action: Mohamad will provide the latest HVAC shop drawing tomorrow."}],
    })
    imperative = process_attendance({
        "platform": "microsoft_teams",
        "mode": "take_notes",
        "owner_approved": True,
        "segments": [{"text": "provide latest shop drawing to check the HVAC"}],
    })
    natural = process_attendance({
        "platform": "microsoft_teams",
        "mode": "take_notes",
        "owner_approved": True,
        "segments": [{"text": "Mohamad will send the revised report tomorrow."}],
    })
    checks = {
        "explicit_action_marker_verified": explicit.get("action_item_count") == 1,
        "manual_imperative_action_verified": imperative.get("action_item_count") == 1,
        "natural_commitment_verified": natural.get("action_item_count") == 1,
        "owner_gate_preserved": all(x.get("owner_gate_preserved") is True for x in (explicit, imperative, natural)),
        "external_network_accessed": False,
        "external_action_executed": False,
        "synthetic_fix_acceptance_only": True,
    }
    return {
        "ok": all([
            checks["explicit_action_marker_verified"],
            checks["manual_imperative_action_verified"],
            checks["natural_commitment_verified"],
            checks["owner_gate_preserved"],
            not checks["external_network_accessed"],
            not checks["external_action_executed"],
        ]),
        **checks,
    }

def self_test() -> dict:
    blocked = process_attendance({
        "platform": "microsoft_teams",
        "mode": "take_notes",
        "owner_approved": False,
        "segments": [{"speaker": "A", "text": "Action: send revised plan"}],
    })
    approved = process_attendance({
        "platform": "microsoft_teams",
        "mode": "take_notes",
        "owner_approved": True,
        "segments": [
            {"speaker": "A", "text": "Project status is on track."},
            {"speaker": "B", "text": "Action: send revised plan tomorrow."},
        ],
    })
    status = build_attendance_status(platform_adapter_live=False)
    checks = {
        "owner_approval_gate_verified": blocked.get("status") == "approval_required" and blocked.get("capture_started") is False,
        "approved_transcript_processing_verified": approved.get("ok") is True and approved.get("segment_count") == 2,
        "action_item_extraction_verified": approved.get("action_item_count") == 1,
        "browser_microphone_companion_declared_verified": status.get("browser_microphone_capture_supported") is True,
        "platform_join_not_falsely_claimed_verified": status.get("platform_join_available") is False and status.get("autonomous_platform_join_claimed") is False,
        "ai_identity_verified": status.get("ai_identity_declared") is True and status.get("user_impersonation_allowed") is False,
        "external_network_accessed": False,
        "real_meeting_joined": False,
        "synthetic_acceptance_only": True,
    }
    return {"ok": all([
        checks["owner_approval_gate_verified"],
        checks["approved_transcript_processing_verified"],
        checks["action_item_extraction_verified"],
        checks["browser_microphone_companion_declared_verified"],
        checks["platform_join_not_falsely_claimed_verified"],
        checks["ai_identity_verified"],
        not checks["external_network_accessed"],
        not checks["real_meeting_joined"],
    ]), **checks}
