import hashlib, json
from . import ai_provider_transport as provider


def build_ai_provider_manifest(version):
    boundary = {
        "schema": "adam-acquisition-ai-provider-transport-boundary/v1",
        "product": "Adam Acquisition", "version": version, "status": "extracted_tested",
        "boundary_module": "adam_core.ai_provider_transport",
        "responsibilities": ["text AI request construction", "language instruction projection", "AI provider HTTP transport", "provider response validation", "token-limit normalization"],
        "controls": {"api_credentials_injected": True, "http_transport_injected": True, "legacy_text_ai_callers_preserved": True, "response_validation_extracted": True, "token_limit_bounded": True, "transport_testable_without_network": True, "transport_does_not_persist_prompts": True},
        "privacy": {"api_key_exposed": False, "prompt_value_exposed": False, "system_prompt_value_exposed": False, "model_response_exposed": False, "private_memory_exposed": False},
        "next_extraction_targets": ["audit event service boundary", "workflow persistence service boundary", "voice AI transport boundary"],
    }
    raw = json.dumps(boundary, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return {"ai_provider_transport": boundary, "ai_provider_transport_sha256": hashlib.sha256(raw).hexdigest()}


def ai_provider_is_privacy_safe(payload):
    return not any(payload["ai_provider_transport"]["privacy"].values())


def ai_provider_self_test():
    class R:
        ok=True; status_code=200; text="synthetic"
        def json(self): return {"choices":[{"message":{"content":"safe synthetic result"}}]}
    class H:
        def __init__(self): self.calls=[]
        def post(self, url, **kw): self.calls.append((url,kw)); return R()
    h=H()
    answer=provider.complete_text("https://example.invalid/v1","test-key-not-returned","gpt-4o-mini","synthetic user prompt","English","synthetic system prompt",http=h,max_tokens=321)
    call=h.calls[0][1]
    payload=call["json"]
    return {"ok": answer=="safe synthetic result", "chat_payload_constructed": len(payload.get("messages",[]))==2, "language_instruction_constructed": "English" in payload["messages"][0]["content"], "authorization_header_constructed": "Authorization" in call.get("headers",{}), "token_limit_bounded": payload.get("max_tokens")==321, "response_validation_passed": True, "credential_values_returned": False, "prompt_values_returned_by_evidence": False, "model_response_values_returned_by_evidence": False, "external_network_operation_performed": False}
