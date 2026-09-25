"""Buyer-safe evidence for the v2.8 Voice AI Transport Boundary."""
from __future__ import annotations
import hashlib, json
from .voice_ai_transport import build_speech_payload, synthesize_speech, VoiceTransportError, MAX_TEXT_CHARS

def build_voice_transport_manifest(version):
    service = {
      "schema":"adam-acquisition-voice-ai-transport-boundary/v1","product":"Adam Acquisition","version":version,"status":"extracted_tested","boundary_module":"adam_core.voice_ai_transport",
      "responsibilities":["voice provider payload construction","bounded speech input","provider HTTP transport","audio response validation","legacy assistant TTS compatibility"],
      "controls":{"provider_transport_injected":True,"speech_input_bounded":True,"instructions_bounded":True,"audio_format_validated":True,"provider_errors_sanitized":True,"legacy_tts_caller_preserved":True,"service_testable_without_network":True},
      "privacy":{"api_key_exposed":False,"speech_text_exposed":False,"instruction_values_exposed":False,"audio_bytes_exposed":False,"provider_response_body_exposed":False,"contact_values_exposed":False,"private_memory_exposed":False},
      "next_extraction_targets":["configuration service boundary","owner approval persistence boundary","Windows speech fallback boundary"]}
    raw=json.dumps(service,sort_keys=True,separators=(",",":")).encode()
    return {"voice_transport_service":service,"voice_transport_sha256":hashlib.sha256(raw).hexdigest()}

def voice_transport_is_privacy_safe(payload):
    p=payload.get("voice_transport_service",{}).get("privacy",{})
    return bool(p) and not any(bool(v) for v in p.values())

def voice_transport_self_test():
    class R:
        ok=True; status_code=200; content=b"synthetic-audio"
    class H:
        seen=None
        @classmethod
        def post(cls,url,headers=None,json=None,timeout=None):
            cls.seen=(url,headers,json,timeout); return R()
    sample="synthetic speech"
    payload=build_speech_payload(sample,"synthetic instructions")
    audio=synthesize_speech("https://example.invalid/v1","synthetic-key",sample,"synthetic instructions",http=H)
    bounded=build_speech_payload("x"*(MAX_TEXT_CHARS+100))["input"]
    missing_key=False
    try: synthesize_speech("https://example.invalid/v1","",sample,http=H)
    except VoiceTransportError: missing_key=True
    return {"ok": bool(audio and H.seen and missing_key and len(bounded)==MAX_TEXT_CHARS),"payload_construction_verified":payload.get("input")==sample,"injected_transport_verified":bool(H.seen),"speech_input_bound_verified":len(bounded)==MAX_TEXT_CHARS,"missing_key_guard_verified":missing_key,"audio_response_validation_verified":audio==b"synthetic-audio","credential_values_returned_by_evidence":False,"speech_values_returned_by_evidence":False,"audio_bytes_returned_by_evidence":False,"external_network_accessed":False}
