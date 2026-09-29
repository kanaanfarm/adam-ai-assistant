from __future__ import annotations
import os, hmac
from typing import Any, Dict
import requests

BASE_URL = "https://api.telnyx.com/v2/calls"

class TelnyxConversationError(RuntimeError):
    pass

def _api_key() -> str:
    value = str(os.getenv("TELNYX_API_KEY", "")).strip()
    if not value:
        raise TelnyxConversationError("TELNYX_API_KEY is not configured")
    return value

def _post(call_control_id: str, action: str, payload: Dict[str, Any] | None = None, timeout: int = 15):
    call_id = str(call_control_id or "").strip()
    if not call_id:
        raise TelnyxConversationError("Missing call_control_id")
    response = requests.post(
        f"{BASE_URL}/{call_id}/actions/{action}",
        headers={"Authorization": f"Bearer {_api_key()}", "Content-Type": "application/json", "Accept": "application/json"},
        json=payload or {}, timeout=timeout,
    )
    try:
        body = response.json()
    except ValueError:
        body = {}
    if not response.ok:
        errors = body.get("errors") if isinstance(body, dict) else None
        raise TelnyxConversationError(f"Telnyx {action} failed ({response.status_code}): {errors or response.text[:300]}")
    return body if isinstance(body, dict) else {"ok": True}

def speak(call_control_id: str, text: str):
    message = str(text or "").strip()
    if not message:
        return {"ok": True, "skipped": True}
    return _post(call_control_id, "speak", {
        "payload": message[:3000],
        "payload_type": "text",
        "voice": str(os.getenv("TELNYX_TTS_VOICE", "Polly.Brian")).strip() or "Polly.Brian",
        "language": str(os.getenv("TELNYX_TTS_LANGUAGE", "en-US")).strip() or "en-US",
    })

def start_transcription(call_control_id: str):
    return _post(call_control_id, "transcription_start", {
        "language": str(os.getenv("TELNYX_STT_LANGUAGE", "en")).strip() or "en",
        "transcription_engine": str(os.getenv("TELNYX_STT_ENGINE", "Google")).strip() or "Google",
        "transcription_tracks": "inbound",
    })

def stop_transcription(call_control_id: str):
    return _post(call_control_id, "transcription_stop", {})

def webhook_token_valid(received: str) -> bool:
    expected = str(os.getenv("TELNYX_WEBHOOK_TOKEN", "")).strip()
    return bool(expected) and hmac.compare_digest(expected, str(received or "").strip())
