from pathlib import Path
import hashlib
import hmac

from adam_core.whatsapp_boundary import (
    load_config, save_config, public_status, normalize_number,
    verify_challenge, verify_signature, project_incoming_messages,
    public_boundary_state,
)
from adam_core.whatsapp_boundary_evidence import (
    build_whatsapp_boundary_manifest,
    whatsapp_boundary_is_privacy_safe,
    whatsapp_boundary_self_test,
)


def test_config_roundtrip_preserves_masked_token(tmp_path):
    path = tmp_path / "wa.json"
    first = save_config(path, {"access_token":"secret-token", "phone_number_id":"123"}, verify_token_factory=lambda:"verify")
    second = save_config(path, {"access_token":"", "business_account_id":"456"})
    assert first["access_token"] == "secret-token"
    assert second["access_token"] == "secret-token"
    assert second["business_account_id"] == "456"


def test_environment_overrides_stored_values(tmp_path):
    path = tmp_path / "wa.json"
    save_config(path, {"access_token":"stored", "phone_number_id":"111"}, verify_token_factory=lambda:"verify")
    cfg = load_config(path, env={"WHATSAPP_ACCESS_TOKEN":"env-token", "WHATSAPP_PHONE_NUMBER_ID":"999"})
    assert cfg["access_token"] == "env-token"
    assert cfg["phone_number_id"] == "999"


def test_public_status_only_exposes_safe_state():
    cfg = {"access_token":"secret", "phone_number_id":"123", "business_account_id":"456", "verify_token":"verify", "app_secret":"secret2"}
    status = public_status(cfg)
    assert status["configured"] is True
    assert status["token_saved"] is True
    assert "access_token" not in status
    assert "verify_token" not in status
    assert "app_secret" not in status


def test_normalize_number():
    assert normalize_number("+971 (50) 123-4567") == "971501234567"
    assert normalize_number("00971501234567") == "971501234567"


def test_webhook_verification_and_signature():
    result = verify_challenge(mode="subscribe", supplied_token="abc", challenge="42", expected_token="abc")
    assert result == {"ok": True, "challenge": "42"}
    assert verify_challenge(mode="subscribe", supplied_token="bad", challenge="42", expected_token="abc")["ok"] is False
    secret = "app-secret"
    body = b"hello"
    sig = "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    assert verify_signature(app_secret=secret, raw_body=body, supplied_signature=sig) is True
    assert verify_signature(app_secret=secret, raw_body=body, supplied_signature="sha256=bad") is False


def test_event_projection_preserves_legacy_inbox_shape():
    event={"entry":[{"changes":[{"value":{"contacts":[{"profile":{"name":"Amjad"}}],"messages":[{"id":"1","from":"9715","timestamp":"2","type":"text","text":{"body":"Hello"}}]}}]}]}
    rows=project_incoming_messages(event, received_at_utc="2026-08-31T10:00:00+00:00")
    assert rows == [{"id":"1","from":"9715","contact_name":"Amjad","timestamp":"2","type":"text","text":"Hello","received_at_utc":"2026-08-31T10:00:00+00:00"}]


def test_manifest_is_privacy_safe_and_fingerprinted():
    state = public_boundary_state({"access_token":"secret", "phone_number_id":"123", "verify_token":"verify", "app_secret":"app"})
    payload = build_whatsapp_boundary_manifest(version="v2.0.0", public_state=state)
    assert payload["whatsapp_boundary"]["status"] == "extracted_tested"
    assert len(payload["whatsapp_boundary_sha256"]) == 64
    assert whatsapp_boundary_is_privacy_safe(payload)


def test_self_test_is_credential_free_and_network_free():
    result = whatsapp_boundary_self_test()
    assert result["ok"] is True
    assert result["credential_values_returned"] is False
    assert result["message_values_returned_by_evidence"] is False
    assert result["external_network_operation_performed"] is False


def test_app_delegates_whatsapp_config_and_webhook_to_core():
    source=(Path(__file__).resolve().parents[1]/"app.py").read_text(encoding="utf-8")
    assert 'VERSION = "v8.1.0.1"' in source
    assert "core_wa_load_config" in source
    assert "core_wa_verify_signature" in source
    assert "core_wa_project_incoming_messages" in source
    assert "/api/acquisition/whatsapp-boundary" in source
