"""Adam v7.5.0 calling & invitations governance layer.

This module prepares owner-reviewed meeting invitations and call launch previews.
It does not claim autonomous PSTN/VoIP calling. Real calendar creation remains bound
to the existing Microsoft Outlook connector and requires explicit owner approval.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Iterable


def _text(value: Any) -> str:
    return str(value or "").strip()


def _find_contact(contacts: Iterable[dict], *, name: str = "", email: str = "", phone: str = "") -> dict:
    name_l, email_l, phone_l = name.lower(), email.lower(), phone.lower()
    for contact in contacts or []:
        if name_l and _text(contact.get("name")).lower() == name_l:
            return dict(contact)
        if email_l and _text(contact.get("email")).lower() == email_l:
            return dict(contact)
        if phone_l and _text(contact.get("phone")).lower() == phone_l:
            return dict(contact)
    return {}


def build_status(*, contacts_count: int = 0, microsoft_connected: bool = False) -> dict:
    return {
        "ok": True,
        "status": "calling_invitations_ready",
        "contacts_count": max(0, int(contacts_count or 0)),
        "microsoft_outlook_connected": bool(microsoft_connected),
        "meeting_invitation_execution_available": bool(microsoft_connected),
        "device_dialer_launch_available": True,
        "autonomous_voice_call_available": False,
        "autonomous_call_claimed": False,
        "owner_approval_required_for_invitation": True,
        "owner_approval_required_for_call_launch": True,
        "ai_identity_required_for_future_voice_agent": True,
    }


def prepare_invitation(payload: dict, contacts: Iterable[dict]) -> dict:
    payload = payload or {}
    contact = _find_contact(
        contacts,
        name=_text(payload.get("contact_name")),
        email=_text(payload.get("attendee_email")),
    )
    attendee_name = _text(payload.get("contact_name")) or _text(contact.get("name"))
    attendee_email = _text(payload.get("attendee_email")) or _text(contact.get("email"))
    title = _text(payload.get("title"))
    date = _text(payload.get("date"))
    start_time = _text(payload.get("start_time"))
    duration_minutes = int(payload.get("duration_minutes") or 30)
    agenda = _text(payload.get("agenda"))
    location = _text(payload.get("location"))
    is_online = bool(payload.get("is_online"))

    missing = []
    if not title:
        missing.append("title")
    if not date:
        missing.append("date")
    if not start_time:
        missing.append("start_time")
    if not attendee_email:
        missing.append("attendee_email")

    return {
        "ok": not missing,
        "status": "invitation_preview_ready" if not missing else "invitation_preview_incomplete",
        "missing": missing,
        "invitation": {
            "title": title,
            "attendee_name": attendee_name,
            "attendee_email": attendee_email,
            "date": date,
            "start_time": start_time,
            "duration_minutes": duration_minutes,
            "agenda": agenda,
            "location": location,
            "is_online": is_online,
        },
        "owner_approval_required": True,
        "external_action_executed": False,
        "real_invitation_sent": False,
    }


def prepare_call(payload: dict, contacts: Iterable[dict]) -> dict:
    payload = payload or {}
    contact = _find_contact(
        contacts,
        name=_text(payload.get("contact_name")),
        phone=_text(payload.get("phone")),
    )
    contact_name = _text(payload.get("contact_name")) or _text(contact.get("name"))
    phone = _text(payload.get("phone")) or _text(contact.get("phone"))
    purpose = _text(payload.get("purpose"))
    return {
        "ok": bool(phone),
        "status": "call_preview_ready" if phone else "phone_required",
        "contact_name": contact_name,
        "phone": phone,
        "purpose": purpose,
        "owner_approval_required": True,
        "device_dialer_only": True,
        "autonomous_voice_call_available": False,
        "autonomous_call_claimed": False,
        "external_action_executed": False,
    }


def self_test() -> dict:
    contacts = [{"name": "Engineer Test", "email": "eng@example.com", "phone": "+971500000000"}]
    inv = prepare_invitation({
        "contact_name": "Engineer Test",
        "title": "HVAC Coordination",
        "date": "2030-01-02",
        "start_time": "10:00",
        "duration_minutes": 30,
        "is_online": True,
    }, contacts)
    call = prepare_call({"contact_name": "Engineer Test", "purpose": "HVAC coordination"}, contacts)
    status = build_status(contacts_count=1, microsoft_connected=False)
    checks = {
        "invitation_preview_verified": inv.get("ok") is True and inv["invitation"]["attendee_email"] == "eng@example.com",
        "invitation_owner_gate_verified": inv.get("owner_approval_required") is True and inv.get("real_invitation_sent") is False,
        "call_preview_verified": call.get("ok") is True and call.get("phone") == "+971500000000",
        "call_owner_gate_verified": call.get("owner_approval_required") is True and call.get("external_action_executed") is False,
        "autonomous_call_not_falsely_claimed_verified": status.get("autonomous_voice_call_available") is False and status.get("autonomous_call_claimed") is False,
        "ai_identity_boundary_verified": status.get("ai_identity_required_for_future_voice_agent") is True,
    }
    return {
        "ok": all(checks.values()),
        **checks,
        "external_network_accessed": False,
        "external_action_executed": False,
        "synthetic_acceptance_only": True,
    }
