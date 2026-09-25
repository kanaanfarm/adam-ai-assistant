"""Pure owner-controlled connector execution adapters for Adam Acquisition v1.8.

These helpers intentionally know nothing about Flask, Microsoft Graph, Meta, or
credential storage. Routes inject the proven transport callbacks. This keeps
approval/validation policy testable without external credentials while
preserving the existing transport implementations.
"""
from __future__ import annotations

import re
from typing import Callable, Any

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class ConnectorValidationError(ValueError):
    """Input or approval validation failed before external execution."""


def _require_approval(approved: bool, message: str) -> None:
    if approved is not True:
        raise ConnectorValidationError(message)


def _split_addresses(raw: str) -> list[str]:
    return [x.strip() for x in re.split(r"[;,]", str(raw or "")) if x.strip()]


def execute_email(*, approved: bool, to_email: str, subject: str, body: str,
                  cc_raw: str = "", bcc_raw: str = "", send_func: Callable[..., Any]):
    _require_approval(approved, "Owner approval is required before sending.")
    to_email = str(to_email or "").strip()
    subject = str(subject or "").strip()
    body = str(body or "").strip()
    if not to_email or not subject or not body:
        raise ConnectorValidationError("To, Subject and Message are required.")
    if not _EMAIL_RE.match(to_email):
        raise ConnectorValidationError("Recipient email address is invalid.")
    cc = _split_addresses(cc_raw)
    bcc = _split_addresses(bcc_raw)
    result = send_func(to_email=to_email, subject=subject, body=body, cc=cc, bcc=bcc)
    return {
        "sent": True,
        "to": to_email,
        "subject": subject,
        "cc": cc,
        "bcc": bcc,
        "transport_result": result,
    }


def execute_calendar(*, approved: bool, subject: str, start_local: str,
                     duration_minutes: int, attendee_email: str, attendee_name: str,
                     create_func: Callable[..., dict]):
    _require_approval(approved, "Owner approval is required before creating the meeting.")
    subject = str(subject or "Meeting").strip() or "Meeting"
    start_local = str(start_local or "").strip()
    attendee_email = str(attendee_email or "").strip()
    attendee_name = str(attendee_name or "").strip()
    if not start_local or not attendee_email:
        raise ConnectorValidationError("Meeting date/time and attendee email are required.")
    try:
        duration = int(duration_minutes or 60)
    except Exception:
        duration = 60
    if duration <= 0:
        raise ConnectorValidationError("Meeting duration must be greater than zero.")
    event = create_func(subject, start_local, duration, attendee_email, attendee_name)
    event = event if isinstance(event, dict) else {}
    return {
        "created": True,
        "subject": subject,
        "start_local": start_local,
        "duration_minutes": duration,
        "attendee_email": attendee_email,
        "event_id": event.get("id"),
        "webLink": event.get("webLink"),
        "transport_result": event,
    }


def normalize_whatsapp_number(value: str) -> str:
    digits = re.sub(r"\D+", "", str(value or ""))
    if digits.startswith("00"):
        digits = digits[2:]
    return digits


def execute_whatsapp(*, approved: bool, phone: str, message: str,
                     send_func: Callable[[str, str], Any]):
    _require_approval(approved, "Owner approval is required before sending.")
    phone = str(phone or "").strip()
    message = str(message or "").strip()
    if not phone:
        raise ConnectorValidationError("Recipient WhatsApp number is required.")
    if not message:
        raise ConnectorValidationError("Message text is empty.")
    normalized = normalize_whatsapp_number(phone)
    if not normalized:
        raise ConnectorValidationError("Recipient WhatsApp number is required.")
    result = send_func(phone, message)
    message_id = ""
    if isinstance(result, dict):
        messages = result.get("messages") or []
        if messages and isinstance(messages[0], dict):
            message_id = str(messages[0].get("id") or "")
    return {
        "sent": True,
        "phone_normalized": normalized,
        "message_id": message_id,
        "transport_result": result,
    }


def self_test():
    """Run credential-free execution-adapter checks using injected local callbacks."""
    checks = {
        "email_denied_without_approval": False,
        "email_executes_after_approval": False,
        "calendar_denied_without_approval": False,
        "calendar_executes_after_approval": False,
        "whatsapp_denied_without_approval": False,
        "whatsapp_executes_after_approval": False,
    }

    email_calls = []
    try:
        execute_email(approved=False, to_email="test@example.invalid", subject="Test", body="Test", send_func=lambda **k: email_calls.append(k))
    except ConnectorValidationError:
        checks["email_denied_without_approval"] = not email_calls
    execute_email(approved=True, to_email="test@example.invalid", subject="Test", body="Test", send_func=lambda **k: email_calls.append(k))
    checks["email_executes_after_approval"] = len(email_calls) == 1

    calendar_calls = []
    try:
        execute_calendar(approved=False, subject="Test", start_local="2026-09-01T10:00", duration_minutes=30, attendee_email="test@example.invalid", attendee_name="Test", create_func=lambda *a: calendar_calls.append(a) or {})
    except ConnectorValidationError:
        checks["calendar_denied_without_approval"] = not calendar_calls
    execute_calendar(approved=True, subject="Test", start_local="2026-09-01T10:00", duration_minutes=30, attendee_email="test@example.invalid", attendee_name="Test", create_func=lambda *a: calendar_calls.append(a) or {"id": "local-test"})
    checks["calendar_executes_after_approval"] = len(calendar_calls) == 1

    whatsapp_calls = []
    try:
        execute_whatsapp(approved=False, phone="+971500000000", message="Test", send_func=lambda p,m: whatsapp_calls.append((p,m)) or {})
    except ConnectorValidationError:
        checks["whatsapp_denied_without_approval"] = not whatsapp_calls
    execute_whatsapp(approved=True, phone="+971500000000", message="Test", send_func=lambda p,m: whatsapp_calls.append((p,m)) or {"messages": [{"id": "local-test"}]})
    checks["whatsapp_executes_after_approval"] = len(whatsapp_calls) == 1

    return {"ok": all(checks.values()), "checks": checks, "external_execution_performed": False}
