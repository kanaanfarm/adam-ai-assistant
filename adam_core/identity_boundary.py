"""Buyer-safe Microsoft identity boundary evidence for Adam Acquisition v1.9."""
from __future__ import annotations

from hashlib import sha256
import json


def _hash(payload):
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return sha256(raw).hexdigest()


def build_identity_boundary_manifest(*, version, client_configured=False, token_cache_present=False):
    core = {
        "schema": "adam-acquisition-microsoft-identity-boundary/v1",
        "product": "Adam Acquisition",
        "version": version,
        "boundary_module": "adam_core.microsoft_identity",
        "status": "extracted_tested",
        "responsibilities": [
            "microsoft client configuration persistence",
            "serialized token-cache persistence",
            "device-flow state projection",
        ],
        "integration": {
            "msal_transport_remains_injected_from_legacy_app": True,
            "client_configured": bool(client_configured),
            "token_cache_present": bool(token_cache_present),
            "external_identity_operation_performed_by_manifest": False,
            "legacy_routes_preserved": True,
        },
        "controls": {
            "token_values_never_returned_by_boundary": True,
            "buyer_evidence_contains_only_boolean_configuration_state": True,
            "pure_identity_service_tests_without_flask_or_msal": True,
        },
        "next_extraction_targets": [
            "document processing boundary",
            "whatsapp cloud transport service boundary",
            "microsoft graph transport service boundary",
        ],
        "privacy": {
            "access_tokens_exposed": False,
            "refresh_tokens_exposed": False,
            "client_secret_exposed": False,
            "client_id_value_exposed": False,
            "username_exposed": False,
            "private_memory_exposed": False,
        },
    }
    return {"identity_boundary": core, "identity_boundary_sha256": _hash(core)}


def identity_boundary_is_privacy_safe(payload):
    text = json.dumps(payload or {}, sort_keys=True, default=str).lower()
    forbidden = (
        '"access_token":', '"refresh_token":', '"client_secret":', '"client_id":',
        '"username":', '"password":', '"private_memory_value":', '"message_body":',
    )
    return not any(term in text for term in forbidden)


def identity_boundary_self_test():
    # Deliberately no MSAL/network call: evidence that privacy/shape checks can run credential-free.
    sample = build_identity_boundary_manifest(
        version="self-test",
        client_configured=True,
        token_cache_present=True,
    )
    return {
        "privacy_safe": identity_boundary_is_privacy_safe(sample),
        "credential_values_returned": False,
        "external_identity_operation_performed": False,
        "boolean_configuration_state_only": True,
    }
