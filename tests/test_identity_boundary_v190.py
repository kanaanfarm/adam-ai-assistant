from pathlib import Path

from adam_core.identity_boundary import (
    build_identity_boundary_manifest,
    identity_boundary_is_privacy_safe,
    identity_boundary_self_test,
)
from adam_core.microsoft_identity import (
    MicrosoftIdentityState,
    load_client_config,
    save_client_config,
    load_serialized_cache,
    persist_serialized_cache,
    public_identity_state,
)


def test_client_config_roundtrip(tmp_path):
    path = tmp_path / "ms.json"
    save_client_config(path, "client-123")
    assert load_client_config(path)["client_id"] == "client-123"


def test_env_client_id_fills_missing_config(tmp_path):
    path = tmp_path / "missing.json"
    assert load_client_config(path, env_client_id="env-client")["client_id"] == "env-client"


def test_serialized_cache_roundtrip(tmp_path):
    path = tmp_path / "cache.json"
    persist_serialized_cache(path, '{"AccessToken":{"secret":"not-for-manifest"}}')
    assert "AccessToken" in load_serialized_cache(path)


def test_device_state_projection():
    state = MicrosoftIdentityState()
    assert state.status()["status"] == "not_connected"
    state.set_waiting({"user_code": "ABC"})
    assert state.status()["status"] == "waiting"
    state.set_connected("owner@example.test")
    assert state.status()["status"] == "connected"
    state.set_error("test")
    assert state.status()["status"] == "error"


def test_public_identity_state_has_no_identity_values():
    public = public_identity_state(client_configured=True, token_cache_present=True, device_status="connected")
    assert public == {"client_configured": True, "token_cache_present": True, "device_status": "connected"}


def test_identity_manifest_is_privacy_safe_and_fingerprinted():
    payload = build_identity_boundary_manifest(version="v1.9.0", client_configured=True, token_cache_present=True)
    assert payload["identity_boundary"]["status"] == "extracted_tested"
    assert len(payload["identity_boundary_sha256"]) == 64
    assert identity_boundary_is_privacy_safe(payload)


def test_identity_self_test_never_performs_external_operation():
    result = identity_boundary_self_test()
    assert result["privacy_safe"] is True
    assert result["credential_values_returned"] is False
    assert result["external_identity_operation_performed"] is False


def test_app_delegates_microsoft_persistence_to_core_boundary():
    app_source = (Path(__file__).resolve().parents[1] / "app.py").read_text(encoding="utf-8")
    assert 'VERSION = "v8.1.0.1"' in app_source
    assert "core_ms_load_config" in app_source
    assert "core_ms_persist_serialized_cache" in app_source
    assert "/api/acquisition/identity-boundary" in app_source
