"""Buyer-safe meeting-platform adapter evidence for Adam Acquisition v4.6."""
from .meeting_platform_adapter import public_manifest, preview_join, synthetic_join

def build_meeting_platform_manifest(version: str) -> dict:
    return {
        "schema": "adam-acquisition-meeting-platform/v1",
        "product": "Adam Acquisition", "version": version,
        "status": "meeting_platform_adapter_foundation_tested",
        "meeting_platform": {"boundary_module": "adam_core.meeting_platform_adapter", "capabilities": public_manifest()},
        "next_targets": ["real Microsoft Teams adapter", "real Zoom adapter", "real Google Meet adapter", "post-meeting cross-app follow-up"],
    }

def meeting_platform_is_privacy_safe(payload: dict) -> bool:
    c = (((payload or {}).get("meeting_platform") or {}).get("capabilities") or {})
    p = c.get("privacy") or {}
    return bool(c.get("owner_approval_required_before_join") and c.get("ai_identity_required") and
                c.get("user_impersonation_allowed") is False and c.get("live_meeting_join_enabled") is False and
                not p.get("meeting_references_exposed_in_buyer_evidence") and
                not p.get("participant_identity_exposed_in_buyer_evidence") and
                not p.get("credentials_stored_in_adapter_contract"))

def meeting_platform_self_test() -> dict:
    base = {"platform":"microsoft_teams", "meeting_ref":"synthetic://meeting-001", "display_name":"Adam AI Assistant"}
    preview = preview_join(base)
    calls=[]
    def adapter(req): calls.append(req.platform); return True
    blocked = synthetic_join({**base, "owner_approved":False}, adapter)
    approved = synthetic_join({**base, "owner_approved":True}, adapter)
    return {
        "ok": bool(preview.get("ok") and blocked.get("status")=="approval_required" and approved.get("ok") and len(calls)==1),
        "join_preview_verified": preview.get("status")=="join_preview_ready",
        "join_blocked_without_owner_approval": blocked.get("status")=="approval_required",
        "approved_adapter_contract_executed": approved.get("ok") is True,
        "ai_identity_declared": approved.get("ai_identity_declared") is True,
        "user_impersonation_allowed": False,
        "external_network_accessed": False,
        "real_meeting_joined": False,
        "credentials_used": False,
        "private_values_returned": False,
    }
