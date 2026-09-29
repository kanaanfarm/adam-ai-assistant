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
    safe_id = (call_id[:18] + "...") if len(call_id) > 18 else call_id
    print(f"TELNYX_VOICE_ACTION start action={action} call={safe_id}", flush=True)
    try:
        response = requests.post(
            f"{BASE_URL}/{call_id}/actions/{action}",
            headers={"Authorization": f"Bearer {_api_key()}", "Content-Type": "application/json", "Accept": "application/json"},
            json=payload or {}, timeout=timeout,
        )
    except Exception as exc:
        print(f"TELNYX_VOICE_ACTION transport_error action={action} error={type(exc).__name__}:{str(exc)[:300]}", flush=True)
        raise
    try:
        body = response.json()
    except ValueError:
        body = {}
    if not response.ok:
        errors = body.get("errors") if isinstance(body, dict) else None
        detail = errors or response.text[:300]
        print(f"TELNYX_VOICE_ACTION failed action={action} http={response.status_code} detail={str(detail)[:500]}", flush=True)
        raise TelnyxConversationError(f"Telnyx {action} failed ({response.status_code}): {detail}")
    print(f"TELNYX_VOICE_ACTION success action={action} http={response.status_code}", flush=True)
    return body if isinstance(body, dict) else {"ok": True}

def speak(call_control_id: str, text: str):
    message = str(text or "").strip()
    if not message:
        print("TELNYX_VOICE_ACTION skipped action=speak reason=empty_message", flush=True)
        return {"ok": True, "skipped": True}
    voice = str(os.getenv("TELNYX_TTS_VOICE", "Polly.Brian")).strip() or "Polly.Brian"
    language = str(os.getenv("TELNYX_TTS_LANGUAGE", "en-US")).strip() or "en-US"
    print(f"TELNYX_TTS_CONFIG voice={voice} language={language} chars={len(message)}", flush=True)
    return _post(call_control_id, "speak", {
        "payload": message[:3000],
        "payload_type": "text",
        "voice": voice,
        "language": language,
    })

def start_transcription(call_control_id: str):
    language = str(os.getenv("TELNYX_STT_LANGUAGE", "en")).strip() or "en"
    engine = str(os.getenv("TELNYX_STT_ENGINE", "Google")).strip() or "Google"
    # ADAM is the caller; the human on the called handset is the inbound/read track.
    # Fail safe to inbound so a missing Render variable cannot silently transcribe ADAM instead.
    track = str(os.getenv("TELNYX_STT_TRACK", "inbound")).strip().lower() or "inbound"
    allowed_tracks = {"inbound", "outbound", "both"}
    if track not in allowed_tracks:
        print(f"TELNYX_STT_CONFIG invalid_track={track} fallback=inbound", flush=True)
        track = "inbound"
    payload = {
        "transcription_engine": engine,
        "transcription_tracks": track,
    }
    # Telnyx Voice API expects recognition language inside the engine config,
    # not as a top-level transcription_start field.
    if engine.lower() == "google":
        payload["transcription_engine_config"] = {
            "transcription_engine": "Google",
            "language": language,
        }
    # Safe diagnostic: this contains no API key, webhook token, phone number or call ID.
    print(
        f"TELNYX_STT_CONFIG language={language} engine={engine} tracks={track} "
        f"request_payload={payload}",
        flush=True,
    )
    return _post(call_control_id, "transcription_start", payload)

def stop_transcription(call_control_id: str):
    return _post(call_control_id, "transcription_stop", {})

def webhook_token_valid(received: str) -> bool:
    expected = str(os.getenv("TELNYX_WEBHOOK_TOKEN", "")).strip()
    return bool(expected) and hmac.compare_digest(expected, str(received or "").strip())
