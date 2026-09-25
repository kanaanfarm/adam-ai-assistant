"""Buyer-safe connector execution boundary evidence for Adam Acquisition v1.9."""
from __future__ import annotations

from hashlib import sha256
import json


def _hash(payload):
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return sha256(raw).hexdigest()


def build_connector_boundary_manifest(*, version):
    core = {
        "schema": "adam-acquisition-connector-boundaries/v1",
        "product": "Adam Acquisition",
        "version": version,
        "adapter_module": "adam_core.connectors",
        "adapters": [
            {
                "connector": "outlook_email",
                "policy": "explicit_owner_approval_before_execution",
                "transport": "injected_existing_outlook_send_callback",
                "status": "extracted_tested",
            },
            {
                "connector": "outlook_calendar",
                "policy": "explicit_owner_approval_before_execution",
                "transport": "injected_existing_calendar_create_callback",
                "status": "extracted_tested",
            },
            {
                "connector": "whatsapp_business",
                "policy": "explicit_owner_approval_before_execution",
                "transport": "injected_existing_whatsapp_cloud_callback",
                "status": "extracted_tested",
            },
        ],
        "adapter_count": 3,
        "controls": {
            "approval_policy_testable_without_credentials": True,
            "transport_credentials_remain_outside_core_adapter": True,
            "existing_transport_callbacks_preserved": True,
            "external_execution_not_performed_by_manifest": True,
            "legacy_routes_preserved": True,
        },
        "next_extraction_targets": [
            "document processing boundary",
            "whatsapp cloud transport service boundary",
            "microsoft graph transport service boundary",
        ],
        "privacy": {
            "credentials_exposed": False,
            "contact_values_exposed": False,
            "message_bodies_exposed": False,
            "attachment_contents_exposed": False,
            "private_memory_exposed": False,
        },
    }
    return {"connector_boundaries": core, "connector_boundaries_sha256": _hash(core)}


def connector_boundaries_are_privacy_safe(payload):
    text = json.dumps(payload or {}, sort_keys=True, default=str).lower()
    forbidden = (
        "api_key", "access_token", "refresh_token", "client_secret", "password",
        "contact_email", "phone_number", "message_body", "attachment_body",
        "private_memory_value", "prompt_text",
    )
    return not any(term in text for term in forbidden)
