from pathlib import Path
from adam_core.runtime_configuration import openai_environment, alpaca_environment, public_runtime_status
from adam_core.runtime_configuration_boundary import build_runtime_configuration_manifest, runtime_configuration_is_privacy_safe, runtime_configuration_self_test

def test_runtime_configuration_manifest_privacy():
    p=build_runtime_configuration_manifest("v3.4.0")
    assert p["runtime_configuration_service"]["status"] == "extracted_tested"
    assert len(p["runtime_configuration_sha256"]) == 64
    assert runtime_configuration_is_privacy_safe(p)

def test_runtime_configuration_self_test():
    r=runtime_configuration_self_test()
    assert r["ok"] and not r["external_network_accessed"] and not r["environment_values_returned_by_evidence"]

def test_runtime_configuration_presence_only():
    env={"OPENAI_API_KEY":"secret-a","ALPACA_API_KEY":"secret-b","ALPACA_SECRET_KEY":"secret-c"}
    status=public_runtime_status(env)
    assert status["openai_api_key_configured"] and status["alpaca_secret_configured"]
    assert all(isinstance(v, bool) for v in status.values())
    assert "secret-a" not in str(status) and "secret-b" not in str(status) and "secret-c" not in str(status)

def test_app_uses_runtime_configuration_boundary():
    src=Path("app.py").read_text()
    assert 'VERSION = "v8.1.0.1"' in src
    assert '/api/acquisition/runtime-configuration-boundary' in src
    assert 'core_runtime_alpaca_environment()' in src
    assert 'core_runtime_ms_client_id()' in src
