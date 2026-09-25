"""Buyer-safe service-boundary extraction evidence for v1.8."""
from __future__ import annotations

from hashlib import sha256
import json


def _hash(payload):
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return sha256(raw).hexdigest()


def build_service_boundary_manifest(*, version):
    core = {
        "schema": "adam-acquisition-service-boundaries/v1",
        "product": "Adam Acquisition",
        "version": version,
        "extracted_boundaries": [
            {
                "module": "adam_core.contacts",
                "responsibility": "contact persistence validation and safe upsert",
                "external_credentials_required": False,
                "status": "extracted_tested",
            },
            {
                "module": "adam_core.followups",
                "responsibility": "follow-up persistence, due parsing, status and public projection",
                "external_credentials_required": False,
                "status": "extracted_tested",
            },
        ],
        "boundary_count": 2,
        "migration_controls": {
            "legacy_routes_preserved": True,
            "approved_user_behavior_preserved": True,
            "pure_service_tests_without_flask": True,
            "connector_execution_separated_from_data_services": True,
        },
        "next_extraction_targets": [
            "microsoft token/session service boundary",
            "document processing boundary",
            "whatsapp cloud transport service boundary",
        ],
        "privacy": {
            "credentials_exposed": False,
            "contact_values_exposed": False,
            "message_bodies_exposed": False,
            "attachment_contents_exposed": False,
            "private_memory_exposed": False,
        },
    }
    return {"service_boundaries": core, "service_boundaries_sha256": _hash(core)}


def service_boundaries_are_privacy_safe(payload):
    text = json.dumps(payload or {}, sort_keys=True, default=str).lower()
    forbidden = (
        "api_key", "access_token", "refresh_token", "client_secret", "password",
        "contact_email", "phone_number", "message_body", "attachment_body",
        "private_memory_value", "prompt_text",
    )
    return not any(term in text for term in forbidden)
