"""Telnyx outbound calling foundation for ADAM.

Secrets/configuration are read from Render environment variables:
TELNYX_API_KEY, TELNYX_CONNECTION_ID, TELNYX_FROM_NUMBER.
TELNYX_OUTBOUND_PROFILE_ID is accepted only as a temporary legacy fallback.

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


def _api_key_diagnostics(value: str) -> Dict[str, Any]:
    """Return safe Telnyx API-key diagnostics without exposing the secret."""
    raw = str(value or "")
    stripped = raw.strip()
    return {
        "present": bool(stripped),
        "starts_with_KEY": stripped.startswith("KEY"),
        "length": len(stripped),
        "has_whitespace": any(ch.isspace() for ch in stripped),
        "has_quotes": stripped.startswith(("\"", "'")) or stripped.endswith(("\"", "'")),
        "has_bearer_prefix": stripped.lower().startswith("bearer "),
    }


def readiness() -> Dict[str, Any]:
    """Return configuration status and safe API-key diagnostics; never return secrets."""
    names = ("TELNYX_API_KEY", "TELNYX_CONNECTION_ID", "TELNYX_FROM_NUMBER")
    configured = {name: bool(str(os.getenv(name, "")).strip()) for name in names}
    legacy_connection = bool(str(os.getenv("TELNYX_OUTBOUND_PROFILE_ID", "")).strip())
    connection_ready = configured["TELNYX_CONNECTION_ID"] or legacy_connection
    return {
        "configured": configured["TELNYX_API_KEY"] and connection_ready and configured["TELNYX_FROM_NUMBER"],
        "environment": configured,
        "legacy_outbound_profile_fallback_present": legacy_connection,
        "telnyx_api_key": _api_key_diagnostics(os.getenv("TELNYX_API_KEY", "")),
    }


def create_outbound_call(to_number: str, *, approved: bool = False, timeout: int = 20) -> Dict[str, Any]:
    """Create a Telnyx outbound call after explicit approval.

    This is only the call-origination foundation. Two-way ADAM conversation
    audio/media is intentionally a separate integration step.
    """
    if approved is not True:
        raise TelnyxCallError("Call requires explicit approval")

    api_key = _env("TELNYX_API_KEY")
    key_diag = _api_key_diagnostics(api_key)
    if key_diag["has_bearer_prefix"]:
        raise TelnyxCallError("TELNYX_API_KEY must contain only the API key; remove the 'Bearer ' prefix")
    if key_diag["has_quotes"]:
        raise TelnyxCallError("TELNYX_API_KEY contains quote characters; paste the raw API key only")
    if key_diag["has_whitespace"]:
        raise TelnyxCallError("TELNYX_API_KEY contains whitespace; paste the API key again without spaces or line breaks")
    if not key_diag["starts_with_KEY"]:
        raise TelnyxCallError("TELNYX_API_KEY has an unexpected format (expected it to start with KEY)")
    connection_id = str(os.getenv("TELNYX_CONNECTION_ID", "")).strip() or str(os.getenv("TELNYX_OUTBOUND_PROFILE_ID", "")).strip()
    if not connection_id:
        raise TelnyxCallError("Missing required environment variable: TELNYX_CONNECTION_ID")
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
        safe_diag = {k: v for k, v in key_diag.items() if k != 'present'}
        raise TelnyxCallError(f"Telnyx rejected call ({response.status_code}): {detail or 'unknown error'}; API key diagnostics: {safe_diag}")

    data = body.get("data", {}) if isinstance(body, dict) else {}
    return {
        "ok": True,
        "call_control_id": data.get("call_control_id"),
        "call_leg_id": data.get("call_leg_id"),
        "call_session_id": data.get("call_session_id"),
        "to": to_number,
        "from": from_number,
    }
