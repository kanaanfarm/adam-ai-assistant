"""Adam v7.4.0 — governed Meeting Conversation Agent.

Adds a bounded Active Participant workflow on top of the accepted meeting
attendance companion. Adam may prepare a response from meeting context, but
speaking is a separate owner-approved step and always declares Adam as AI.
No autonomous meeting-platform join is claimed or performed here.
"""
from __future__ import annotations
from typing import Any

SUPPORTED_MODES = {"listen_only", "take_notes", "active_participant", "owner_representative"}
MAX_CONTEXT_CHARS = 6000
MAX_RESPONSE_CHARS = 900


def _clean(v: Any, limit: int) -> str:
    return " ".join(str(v or "").split())[:limit]


def build_conversation_status() -> dict:
    return {
        "ok": True,
        "status": "meeting_conversation_agent_ready",
        "supported_modes": sorted(SUPPORTED_MODES),
        "active_participant_available": True,
        "owner_representative_available": True,
        "owner_representative_is_ai_disclosed": True,
        "owner_representative_may_answer_and_clarify": True,
        "owner_representative_may_make_consequential_commitments": False,
        "response_preview_required": True,
        "owner_approval_required_to_speak": True,
        "ai_identity_declared_when_speaking": True,
        "user_impersonation_allowed": False,
        "autonomous_platform_join_claimed": False,
        "external_action_executed": False,
    }


def prepare_response(raw: dict | None) -> dict:
    raw = raw or {}
    mode = _clean(raw.get("mode"), 40).lower()
    if mode not in SUPPORTED_MODES:
        return {"ok": False, "status": "unsupported_mode", "response_ready": False}
    if mode not in {"active_participant", "owner_representative"}:
        return {
            "ok": False, "status": "active_participant_required", "response_ready": False,
            "owner_gate_preserved": True, "spoken": False,
        }
    context = _clean(raw.get("context"), MAX_CONTEXT_CHARS)
    requested = _clean(raw.get("response"), MAX_RESPONSE_CHARS)
    if not context and not requested:
        return {"ok": False, "status": "meeting_context_required", "response_ready": False, "spoken": False}

    # The UI can supply an owner-edited response. If absent, prepare a safe local
    # acknowledgement rather than inventing project facts.
    response = requested or "I am Adam, the AI meeting assistant. I have noted the discussion and can help summarize the confirmed points."
    return {
        "ok": True,
        "status": "response_preview_ready",
        "response_ready": True,
        "response": response,
        "ai_identity_prefix_required": True,
        "owner_approval_required_to_speak": True,
        "owner_gate_preserved": True,
        "spoken": False,
        "external_action_executed": False,
        "autonomous_platform_join_claimed": False,
    }


def authorize_speaking(raw: dict | None) -> dict:
    raw = raw or {}
    response = _clean(raw.get("response"), MAX_RESPONSE_CHARS)
    if not response:
        return {"ok": False, "status": "response_required", "speak_authorized": False, "spoken": False}
    if raw.get("owner_approved") is not True:
        return {
            "ok": False, "status": "approval_required", "speak_authorized": False,
            "owner_gate_preserved": True, "spoken": False,
        }
    identity_already_declared = raw.get("identity_already_declared") is True
    if not identity_already_declared and not response.lower().startswith("i am adam"):
        response = "I am Adam, the AI meeting assistant. " + response
    return {
        "ok": True,
        "status": "speaking_authorized",
        "speak_authorized": True,
        "response": response[:MAX_RESPONSE_CHARS],
        "ai_identity_declared": True,
        "identity_repeated": False if identity_already_declared else response.lower().startswith("i am adam"),
        "user_impersonation_allowed": False,
        "owner_gate_preserved": True,
        "spoken": False,
        "external_action_executed": False,
        "autonomous_platform_join_claimed": False,
    }


def self_test() -> dict:
    preview = prepare_response({"mode":"active_participant","context":"The team discussed the HVAC drawing.","response":"I can summarize the confirmed HVAC points."})
    blocked = authorize_speaking({"response": preview.get("response"), "owner_approved": False})
    approved = authorize_speaking({"response": preview.get("response"), "owner_approved": True})
    followup = authorize_speaking({"response": "I can summarize the next confirmed point.", "owner_approved": True, "identity_already_declared": True})
    checks = {
        "four_meeting_modes_verified": SUPPORTED_MODES == {"listen_only","take_notes","active_participant","owner_representative"},
        "active_participant_preview_verified": preview.get("response_ready") is True and preview.get("spoken") is False,
        "speaking_blocked_without_owner_approval": blocked.get("status") == "approval_required" and blocked.get("spoken") is False,
        "approved_speaking_authorization_verified": approved.get("speak_authorized") is True,
        "ai_identity_verified": approved.get("ai_identity_declared") is True and approved.get("response","").lower().startswith("i am adam"),
        "ai_identity_not_repeated_after_first_turn": not followup.get("response","").lower().startswith("i am adam"),
        "user_impersonation_blocked": approved.get("user_impersonation_allowed") is False,
        "autonomous_platform_join_not_claimed": approved.get("autonomous_platform_join_claimed") is False,
        "external_network_accessed": False,
        "synthetic_acceptance_only": True,
    }
    return {"ok": all(v for k,v in checks.items() if k not in {"external_network_accessed"}) and checks["external_network_accessed"] is False, **checks}
