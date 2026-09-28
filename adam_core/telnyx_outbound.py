"""Telnyx outbound calling foundation for ADAM.

Secrets/configuration are read from Render environment variables:
TELNYX_API_KEY, TELNYX_OUTBOUND_PROFILE_ID, TELNYX_FROM_NUMBER.

This module deliberately requires explicit approval from the caller.  It does
not expose secrets and can be wired into ADAM's approval/UI layer separately.
"""
from __future__ import annotations

import os
import re
from typing import Any, Dict

import requests

TELNYX_CALLS_URL = "https://api.telnyx.com/v2/calls"


class TelnyxCallError(RuntimeError):
    pass


def _env(name: str) -> str:
    value = str(os.getenv(name, "")).strip()
    if not value:
        raise TelnyxCallError(f"Missing required environment variable: {name}")
    return value


def normalize_e164(number: str) -> str:
    """Validate/normalize an international E.164-style number."""
    raw = str(number or "").strip()
    cleaned = "+" + re.sub(r"\D", "", raw[1:]) if raw.startswith("+") else re.sub(r"\D", "", raw)
    if not cleaned.startswith("+"):
        raise TelnyxCallError("Destination must include country code, e.g. +971...")
    digits = cleaned[1:]
    if not (8 <= len(digits) <= 15):
        raise TelnyxCallError("Invalid international phone number")
    return cleaned


def readiness() -> Dict[str, Any]:
    """Return configuration status without ever returning secret values."""
    names = ("TELNYX_API_KEY", "TELNYX_OUTBOUND_PROFILE_ID", "TELNYX_FROM_NUMBER")
    configured = {name: bool(str(os.getenv(name, "")).strip()) for name in names}
    return {"configured": all(configured.values()), "environment": configured}


def create_outbound_call(to_number: str, *, approved: bool = False, timeout: int = 20) -> Dict[str, Any]:
    """Create a Telnyx outbound call after explicit approval.

    This is only the call-origination foundation. Two-way ADAM conversation
    audio/media is intentionally a separate integration step.
    """
    if approved is not True:
        raise TelnyxCallError("Call requires explicit approval")

    api_key = _env("TELNYX_API_KEY")
    connection_id = _env("TELNYX_OUTBOUND_PROFILE_ID")
    from_number = normalize_e164(_env("TELNYX_FROM_NUMBER"))
    to_number = normalize_e164(to_number)

    payload = {
        "connection_id": connection_id,
        "to": to_number,
        "from": from_number,
    }
    try:
        response = requests.post(
            TELNYX_CALLS_URL,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json=payload,
            timeout=timeout,
        )
    except requests.RequestException as exc:
        raise TelnyxCallError(f"Telnyx request failed: {exc}") from exc

    try:
        body = response.json()
    except ValueError:
        body = {}

    if not response.ok:
        detail = body.get("errors") if isinstance(body, dict) else None
        raise TelnyxCallError(f"Telnyx rejected call ({response.status_code}): {detail or 'unknown error'}")

    data = body.get("data", {}) if isinstance(body, dict) else {}
    return {
        "ok": True,
        "call_control_id": data.get("call_control_id"),
        "call_leg_id": data.get("call_leg_id"),
        "call_session_id": data.get("call_session_id"),
        "to": to_number,
        "from": from_number,
    }
