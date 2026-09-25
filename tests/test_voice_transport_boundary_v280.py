from adam_core.voice_ai_transport import build_speech_payload, synthesize_speech, VoiceTransportError
from adam_core.voice_transport_boundary import build_voice_transport_manifest, voice_transport_is_privacy_safe, voice_transport_self_test

def test_payload_and_privacy():
    assert build_speech_payload("hello")["input"] == "hello"
    m=build_voice_transport_manifest("v2.8.0")
    assert voice_transport_is_privacy_safe(m)
    assert len(m["voice_transport_sha256"]) == 64

def test_self_test():
    r=voice_transport_self_test(); assert r["ok"] and not r["external_network_accessed"]

def test_missing_key():
    try: synthesize_speech("https://example.invalid/v1","","hello")
    except VoiceTransportError: return
    assert False
