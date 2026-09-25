from adam_core.vision_transport_boundary import build_vision_transport_manifest, vision_transport_is_privacy_safe, vision_transport_self_test
from adam_core.vision_ai_transport import select_vision_model, build_vision_payload
from pathlib import Path

def test_manifest_privacy_and_hash():
    p=build_vision_transport_manifest("v2.4.0")
    assert vision_transport_is_privacy_safe(p)
    assert p["vision_transport"]["status"]=="extracted_tested"
    assert len(p["vision_transport_sha256"])==64

def test_network_free_self_test():
    r=vision_transport_self_test()
    assert r["ok"] and r["multimodal_payload_constructed"]
    assert not r["credential_values_returned"]
    assert not r["image_values_returned_by_evidence"]
    assert not r["external_network_operation_performed"]

def test_model_selection_and_payload():
    assert select_vision_model("text-only-model")=="gpt-4o-mini"
    assert select_vision_model("gpt-5.6") == "gpt-5.6"
    p=build_vision_payload([{"bytes":b"abc","mime":"image/png"}],"look","gpt-5.6")
    assert "max_completion_tokens" in p and "max_tokens" not in p
    assert p["messages"][0]["content"][1]["image_url"]["url"].startswith("data:image/png;base64,")

def test_app_routes_and_delegation_present():
    src=Path(__file__).resolve().parents[1].joinpath("app.py").read_text()
    assert 'VERSION = "v8.1.0.1"' in src
    assert '/api/acquisition/vision-transport-boundary' in src
    assert 'core_vision_analyze_images' in src
    assert 'requests.post(\n        api_base + "/chat/completions"' not in src
