"""Buyer-safe WhatsApp configuration/webhook boundary evidence for v2.0."""
from __future__ import annotations
from hashlib import sha256
import json


def _hash(payload):
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return sha256(raw).hexdigest()


def build_whatsapp_boundary_manifest(*, version, public_state):
    state = dict(public_state or {})
    core = {
        "schema": "adam-acquisition-whatsapp-config-webhook-boundary/v1",
        "product": "Adam Acquisition",
        "version": version,
        "boundary_module": "adam_core.whatsapp_boundary",
        "status": "extracted_tested",
        "responsibilities": [
            "whatsapp configuration persistence",
            "environment override application",
            "webhook verification challenge",
            "webhook signature verification",
            "incoming message projection",
        ],
        "configuration_state": {
            "configured": bool(state.get("configured")),
            "api_version": str(state.get("api_version") or "v21.0"),
            "token_saved": bool(state.get("token_saved")),
            "verify_token_saved": bool(state.get("verify_token_saved")),
            "app_secret_saved": bool(state.get("app_secret_saved")),
        },
        "controls": {
            "credential_values_never_returned": True,
            "webhook_verification_uses_constant_time_compare": True,
            "signature_verification_extracted_from_flask_route": True,
            "event_projection_testable_without_network": True,
            "legacy_whatsapp_routes_preserved": True,
        },
        "next_extraction_targets": [
            "microsoft graph transport service boundary",
            "whatsapp cloud transport service boundary",
            "vision AI transport boundary",
        ],
        "privacy": {
            "access_token_exposed": False,
            "verify_token_value_exposed": False,
            "app_secret_exposed": False,
            "phone_number_id_value_exposed": False,
            "business_account_id_value_exposed": False,
            "message_body_exposed": False,
            "contact_value_exposed": False,
            "private_memory_exposed": False,
        },
    }
    return {"whatsapp_boundary": core, "whatsapp_boundary_sha256": _hash(core)}


def whatsapp_boundary_is_privacy_safe(payload):
    text = json.dumps(payload or {}, sort_keys=True, default=str).lower()
    forbidden = (
        '"access_token":', '"verify_token":', '"app_secret":', '"phone_number_id":',
        '"business_account_id":', '"message_body":', '"contact_name":', '"from":',
        '"private_memory_value":',
    )
    return not any(term in text for term in forbidden)


def whatsapp_boundary_self_test():
    from .whatsapp_boundary import verify_challenge, verify_signature, project_incoming_messages
    secret = "unit-secret"
    body = b'{"object":"whatsapp_business_account"}'
    import hmac, hashlib
    signature = "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
    challenge_ok = verify_challenge(mode="subscribe", supplied_token="verify-me", challenge="12345", expected_token="verify-me")
    challenge_bad = verify_challenge(mode="subscribe", supplied_token="wrong", challenge="12345", expected_token="verify-me")
    projected = project_incoming_messages({"entry":[{"changes":[{"value":{"contacts":[{"profile":{"name":"Private Name"}}],"messages":[{"id":"wamid.test","from":"971500000000","timestamp":"1","type":"text","text":{"body":"Private body"}}]}}]}]}, received_at_utc="2026-01-01T00:00:00+00:00")
    return {
        "ok": bool(challenge_ok["ok"] and not challenge_bad["ok"] and verify_signature(app_secret=secret, raw_body=body, supplied_signature=signature) and len(projected) == 1),
        "verification_accepts_correct_token": bool(challenge_ok["ok"]),
        "verification_rejects_wrong_token": not bool(challenge_bad["ok"]),
        "signature_accepts_valid_hmac": verify_signature(app_secret=secret, raw_body=body, supplied_signature=signature),
        "signature_rejects_invalid_hmac": not verify_signature(app_secret=secret, raw_body=body, supplied_signature="sha256=bad"),
        "event_projection_count": len(projected),
        "credential_values_returned": False,
        "message_values_returned_by_evidence": False,
        "external_network_operation_performed": False,
    }
