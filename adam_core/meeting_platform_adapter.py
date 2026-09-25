"""Governed meeting-platform adapter contract for Adam Acquisition v4.6.

This is an integration boundary, not a claim of live Teams/Zoom/Meet access.
Adapters are injected. Real meeting join stays disabled until credentials,
platform permissions and a buyer-approved deployment are configured.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable

SUPPORTED_PLATFORMS = {"microsoft_teams", "zoom", "google_meet"}
MAX_MEETING_REF_CHARS = 500
MAX_DISPLAY_NAME_CHARS = 80

class MeetingPlatformError(RuntimeError):
    pass

def _clean(v: Any, limit: int) -> str:
    return " ".join(str(v or "").split())[:limit]

@dataclass(frozen=True)
class MeetingJoinRequest:
    platform: str
    meeting_ref: str
    display_name: str = "Adam AI Assistant"
    owner_approved: bool = False

    def public_dict(self) -> dict:
        return {
            "platform": self.platform,
            "meeting_reference_present": bool(self.meeting_ref),
            "display_name_present": bool(self.display_name),
            "owner_approved": self.owner_approved,
            "ai_identity_declared": True,
        }

def normalize_join_request(raw: dict | None) -> MeetingJoinRequest:
    raw = raw or {}
    platform = _clean(raw.get("platform"), 40).lower()
    if platform not in SUPPORTED_PLATFORMS:
        raise MeetingPlatformError("Unsupported meeting platform.")
    meeting_ref = _clean(raw.get("meeting_ref"), MAX_MEETING_REF_CHARS)
    if not meeting_ref:
        raise MeetingPlatformError("Meeting reference is required.")
    return MeetingJoinRequest(
        platform=platform,
        meeting_ref=meeting_ref,
        display_name=_clean(raw.get("display_name") or "Adam AI Assistant", MAX_DISPLAY_NAME_CHARS),
        owner_approved=raw.get("owner_approved") is True,
    )

def preview_join(raw: dict | None) -> dict:
    req = normalize_join_request(raw)
    return {
        "ok": True,
        "status": "join_preview_ready",
        "platform": req.platform,
        "owner_approval_required": True,
        "ai_identity_declared": True,
        "user_impersonation_allowed": False,
        "meeting_reference_present": True,
        "meeting_reference_returned": False,
        "real_meeting_joined": False,
    }

def execute_join(raw: dict | None, adapter: Callable[[MeetingJoinRequest], Any], *, live_enabled: bool = False) -> dict:
    req = normalize_join_request(raw)
    if not req.owner_approved:
        return {
            "ok": False, "status": "approval_required", "platform": req.platform,
            "owner_gate_preserved": True, "executed": False,
            "ai_identity_declared": True, "real_meeting_joined": False,
            "private_values_returned": False,
        }
    if not live_enabled:
        return {
            "ok": False, "status": "live_adapter_disabled", "platform": req.platform,
            "owner_gate_preserved": True, "executed": False,
            "ai_identity_declared": True, "real_meeting_joined": False,
            "private_values_returned": False,
        }
    result = adapter(req)
    return {
        "ok": bool(result is not False), "status": "join_executed", "platform": req.platform,
        "owner_gate_preserved": True, "executed": True,
        "ai_identity_declared": True, "real_meeting_joined": True,
        "private_values_returned": False,
    }

def synthetic_join(raw: dict | None, adapter: Callable[[MeetingJoinRequest], Any]) -> dict:
    """Acceptance-test path: exercises approval + adapter contract without a real meeting."""
    req = normalize_join_request(raw)
    if not req.owner_approved:
        return {
            "ok": False, "status": "approval_required", "platform": req.platform,
            "owner_gate_preserved": True, "executed": False, "synthetic_only": True,
            "ai_identity_declared": True, "real_meeting_joined": False,
            "external_network_accessed": False, "private_values_returned": False,
        }
    result = adapter(req)
    return {
        "ok": bool(result is not False), "status": "synthetic_join_executed", "platform": req.platform,
        "owner_gate_preserved": True, "executed": True, "synthetic_only": True,
        "ai_identity_declared": True, "real_meeting_joined": False,
        "external_network_accessed": False, "private_values_returned": False,
    }

def public_manifest() -> dict:
    return {
        "meeting_platform_adapter_foundation": True,
        "supported_platforms": sorted(SUPPORTED_PLATFORMS),
        "injected_platform_adapters": True,
        "join_preview": True,
        "owner_approval_required_before_join": True,
        "ai_identity_required": True,
        "user_impersonation_allowed": False,
        "live_meeting_join_enabled": False,
        "bounds": {"max_meeting_ref_chars": MAX_MEETING_REF_CHARS, "max_display_name_chars": MAX_DISPLAY_NAME_CHARS},
        "privacy": {
            "meeting_references_exposed_in_buyer_evidence": False,
            "participant_identity_exposed_in_buyer_evidence": False,
            "credentials_stored_in_adapter_contract": False,
        },
    }
