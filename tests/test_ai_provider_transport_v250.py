from pathlib import Path
from adam_core.ai_provider_boundary import build_ai_provider_manifest, ai_provider_is_privacy_safe, ai_provider_self_test
from adam_core.ai_provider_transport import build_chat_payload

ROOT=Path(__file__).resolve().parents[1]

def test_manifest_privacy_and_hash():
    p=build_ai_provider_manifest("v2.7.0")
    assert ai_provider_is_privacy_safe(p)
    assert p["ai_provider_transport"]["status"]=="extracted_tested"
    assert len(p["ai_provider_transport_sha256"])==64

def test_network_free_self_test():
    r=ai_provider_self_test()
    assert r["ok"] and r["chat_payload_constructed"] and r["response_validation_passed"]
    assert not r["credential_values_returned"] and not r["prompt_values_returned_by_evidence"]
    assert not r["external_network_operation_performed"]

def test_gpt5_token_field_and_bound():
    p=build_chat_payload("x","English","gpt-5-mini","system",999999)
    assert p["max_completion_tokens"]==8192
    assert "max_tokens" not in p

def test_app_delegates_text_ai_and_exposes_evidence_routes():
    src=(ROOT/"app.py").read_text(encoding="utf-8")
    assert 'VERSION = "v8.1.0.1"' in src
    assert "core_ai_complete_text" in src
    assert "/api/acquisition/ai-provider-boundary" in src
    html=(ROOT/"templates"/"acquisition.html").read_text(encoding="utf-8")
    assert "AI Provider Transport Boundary" in html
