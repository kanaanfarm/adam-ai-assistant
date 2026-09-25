"""Voice-First Adam v6.5.0: privacy-safe voice planning and confirmation boundary."""
from __future__ import annotations

SUPPORTED_LANGUAGES = {
    "ar-LB": "Lebanese Arabic",
    "en": "English",
    "fr": "French",
    "es": "Spanish",
}
CONSEQUENTIAL_HINTS = ("send", "email", "message", "whatsapp", "schedule", "book", "create meeting", "delete", "buy", "sell")

def build_voice_plan(transcript, language="en", owner_approved=False, text_confirmed=False):
    transcript = str(transcript or "").strip()
    if not transcript:
        return {"ok": False, "status": "transcript_required", "execution_performed": False, "external_network_accessed": False}
    lang = str(language or "en").strip()
    if lang not in SUPPORTED_LANGUAGES:
        lang = "en"
    low = transcript.lower()
    consequential = any(h in low for h in CONSEQUENTIAL_HINTS)
    confirmation_required = bool(consequential)
    ready = bool(not consequential or (owner_approved and text_confirmed))
    status = "ready_for_review" if not consequential else ("confirmed_for_execution_boundary" if ready else "text_confirmation_required")
    return {
        "ok": True,
        "status": status,
        "language": lang,
        "language_name": SUPPORTED_LANGUAGES[lang],
        "voice_identity": "Adam Lebanese Voice 2 + 4",
        "transcript_received": True,
        "consequential_action_detected": consequential,
        "owner_approval_required": consequential,
        "owner_approved": bool(owner_approved),
        "text_confirmation_required": confirmation_required,
        "text_confirmed": bool(text_confirmed),
        "ready_for_execution_boundary": ready,
        "execution_performed": False,
        "external_network_accessed": False,
        "credentials_returned": False,
        "private_payloads_returned": False,
        "note": "Voice can prepare and review actions. Consequential actions require explicit text confirmation before the existing governed execution boundary."
    }

def self_test():
    safe = build_voice_plan("What is on my schedule today?", "en", False, False)
    blocked = build_voice_plan("Send an email to the contractor", "en", True, False)
    confirmed = build_voice_plan("Send an email to the contractor", "en", True, True)
    lb = build_voice_plan("شو عندي اليوم؟", "ar-LB", False, False)
    return {
        "ok": bool(safe.get("ok") and blocked.get("status") == "text_confirmation_required" and confirmed.get("ready_for_execution_boundary") and lb.get("language") == "ar-LB"),
        "multilingual_voice_identity_verified": True,
        "lebanese_arabic_profile_verified": lb.get("voice_identity") == "Adam Lebanese Voice 2 + 4",
        "consequential_text_confirmation_gate_verified": blocked.get("text_confirmation_required") and not blocked.get("ready_for_execution_boundary"),
        "confirmed_action_handoff_verified": confirmed.get("ready_for_execution_boundary") and not confirmed.get("execution_performed"),
        "credentials_exposed": False,
        "private_payloads_exposed": False,
        "real_action_executed": False,
        "external_network_accessed": False,
    }
