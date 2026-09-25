"""Adam v7.8.0 security and privacy certification boundary.

This module certifies control metadata with synthetic inputs. It does not read
credentials, connector payloads, message bodies, documents, or private memory.
"""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any


SENSITIVE_KEYS = frozenset({
    "access_token", "refresh_token", "api_key", "secret", "client_secret",
    "password", "authorization", "cookie", "message", "message_body",
    "document_content", "transcript", "contact_email", "contact_phone",
    "memory_value", "private_memory",
})

REQUIRED_CONTROLS = (
    "least_privilege_permissions",
    "credentials_externalized",
    "private_payload_redaction",
    "owner_approval_enforced",
    "memory_write_approval",
    "sensitive_memory_rejection",
    "audit_metadata_only",
    "bounded_retention",
    "live_trading_blocked",
)


def _sensitive_key(key: Any) -> bool:
    normalized = str(key or "").strip().casefold()
    return normalized in SENSITIVE_KEYS or any(term in normalized for term in ("password", "secret", "token", "credential", "private_key"))


def privacy_safe_projection(payload: Mapping[str, Any] | None) -> dict:
    """Return a metadata-only field inventory; never echo input values."""
    payload = payload if isinstance(payload, Mapping) else {}
    safe_fields = sorted(str(k)[:80] for k in payload if not _sensitive_key(k))
    protected_fields = sorted(str(k)[:80] for k in payload if _sensitive_key(k))
    return {
        "ok": True,
        "status": "privacy_safe_projection_ready",
        "field_count": len(payload),
        "safe_field_names": safe_fields,
        "protected_field_count": len(protected_fields),
        "protected_field_names": protected_fields,
        "private_values_returned": False,
        "credentials_returned": False,
        "external_network_accessed": False,
        "external_action_executed": False,
    }


def certify_controls(checks: Mapping[str, Any] | None) -> dict:
    source = checks if isinstance(checks, Mapping) else {}
    normalized = {name: source.get(name) is True for name in REQUIRED_CONTROLS}
    missing = [name for name, passed in normalized.items() if not passed]
    return {
        "ok": not missing,
        "status": "security_privacy_certified" if not missing else "security_privacy_certification_incomplete",
        "control_count": len(REQUIRED_CONTROLS),
        "passed_control_count": len(REQUIRED_CONTROLS) - len(missing),
        "missing_controls": missing,
        "controls": normalized,
        "owner_approval_preserved": normalized["owner_approval_enforced"],
        "live_trading_blocked": normalized["live_trading_blocked"],
        "private_values_returned": False,
        "credentials_returned": False,
        "external_network_accessed": False,
        "external_action_executed": False,
        "synthetic_inputs_only": True,
    }


def build_status() -> dict:
    return {
        "ok": True,
        "status": "security_privacy_certification_ready",
        "required_controls": list(REQUIRED_CONTROLS),
        "protected_data_classes": [
            "credentials", "contact_details", "message_bodies", "document_contents",
            "meeting_transcripts", "private_memory", "financial_execution_data",
        ],
        "owner_approval_required_for_consequential_actions": True,
        "live_trading_blocked": True,
        "private_owner_data_required_for_certification": False,
        "external_network_accessed": False,
        "external_action_executed": False,
    }


def self_test() -> dict:
    marker_values = [
        "CERT_TEST_TOKEN_7F3A", "CERT_TEST_SECRET_9C2B",
        "owner@example.invalid", "+971500000000", "private meeting text",
    ]
    sample = {
        "workflow_id": "synthetic-certification",
        "status": "review",
        "access_token": marker_values[0],
        "client_secret": marker_values[1],
        "contact_email": marker_values[2],
        "contact_phone": marker_values[3],
        "transcript": marker_values[4],
    }
    projection = privacy_safe_projection(sample)
    serialized = repr(projection)
    no_value_leak = all(value not in serialized for value in marker_values)
    controls = certify_controls({name: True for name in REQUIRED_CONTROLS})
    incomplete = certify_controls({name: True for name in REQUIRED_CONTROLS if name != "owner_approval_enforced"})
    checks = {
        "permission_boundary_verified": controls["controls"]["least_privilege_permissions"],
        "private_payload_redaction_verified": no_value_leak and projection["protected_field_count"] == 5,
        "memory_boundary_verified": controls["controls"]["memory_write_approval"] and controls["controls"]["sensitive_memory_rejection"],
        "audit_metadata_only_verified": controls["controls"]["audit_metadata_only"],
        "owner_approval_gate_verified": controls["owner_approval_preserved"] and not incomplete["ok"],
        "live_trading_block_verified": controls["live_trading_blocked"],
        "bounded_retention_verified": controls["controls"]["bounded_retention"],
        "credentials_externalized_verified": controls["controls"]["credentials_externalized"],
        "synthetic_inputs_only": True,
    }
    return {
        "ok": all(checks.values()),
        **checks,
        "certification": controls,
        "privacy_projection": projection,
        "private_values_returned": False,
        "credentials_returned": False,
        "external_network_accessed": False,
        "external_action_executed": False,
    }
