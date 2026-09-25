"""Provider-neutral voice synthesis transport for Adam Acquisition v2.8."""
from __future__ import annotations

MAX_TEXT_CHARS = 4096
MAX_INSTRUCTIONS_CHARS = 4000
ALLOWED_FORMATS = {"wav", "mp3", "opus", "aac", "flac", "pcm"}

class VoiceTransportError(RuntimeError):
    pass

def build_speech_payload(text, instructions="", model="gpt-4o-mini-tts", voice="onyx", response_format="wav"):
    text = str(text or "").strip()
    if not text:
        raise VoiceTransportError("There is no assistant text to speak.")
    text = text[:MAX_TEXT_CHARS]
    instructions = str(instructions or "").strip()[:MAX_INSTRUCTIONS_CHARS]
    fmt = str(response_format or "wav").lower().strip()
    if fmt not in ALLOWED_FORMATS:
        raise VoiceTransportError("Unsupported audio response format.")
    payload = {"model": str(model or "gpt-4o-mini-tts").strip(), "voice": str(voice or "onyx").strip(), "input": text, "response_format": fmt}
    if instructions:
        payload["instructions"] = instructions
    return payload

def synthesize_speech(api_base, api_key, text, instructions="", model="gpt-4o-mini-tts", voice="onyx", response_format="wav", http=None, timeout=90):
    if not str(api_key or "").strip():
        raise VoiceTransportError("No voice API key is configured. Using the device voice instead.")
    if http is None:
        import requests as http
    base = str(api_base or "https://api.openai.com/v1").rstrip("/")
    payload = build_speech_payload(text, instructions, model, voice, response_format)
    response = http.post(base + "/audio/speech", headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}, json=payload, timeout=timeout)
    if not getattr(response, "ok", False):
        code = getattr(response, "status_code", "unknown")
        raise VoiceTransportError(f"Voice provider error {code}")
    audio = bytes(getattr(response, "content", b"") or b"")
    if not audio:
        raise VoiceTransportError("Voice provider returned no audio.")
    return audio
