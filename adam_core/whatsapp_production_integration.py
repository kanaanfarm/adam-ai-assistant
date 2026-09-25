"""Governed WhatsApp Production Integration for Adam Acquisition v6.8.0.

This layer prepares a WhatsApp action for the existing Cloud API transport while
keeping Owner Approval and Live Execute as separate gates. Acceptance tests use
injected/synthetic state and never contact Meta.
"""
from __future__ import annotations

import re

SENSITIVE_HINTS = ("password", "passwd", "api key", "api_key", "access token", "private key", "secret")


def _normalize_phone(value):
    digits = re.sub(r"\D+", "", str(value or ""))
    if digits.startswith("00"):
        digits = digits[2:]
    return digits


def build_execution_plan(phone, message, owner_approved=False, live_execute=False, connector_ready=False):
    phone_raw = str(phone or "").strip()
    message = str(message or "").strip()
    low = message.lower()
    base = {
        "ok": True,
        "connector": "whatsapp_cloud",
        "connector_ready": bool(connector_ready),
        "owner_approved": bool(owner_approved),
        "live_execution_requested": bool(live_execute),
        "execution_performed": False,
        "external_network_accessed": False,
        "credentials_returned": False,
        "private_payloads_returned": False,
        "ready_for_whatsapp_transport": False,
        "phone_received": bool(phone_raw),
        "message_received": bool(message),
        "two_gate_policy": "owner_approval_then_live_execute",
    }
    if any(x in low for x in SENSITIVE_HINTS):
        return {**base, "ok": False, "status": "sensitive_content_rejected"}
    if not _normalize_phone(phone_raw) or not message:
        return {**base, "ok": False, "status": "recipient_and_message_required"}
    if not owner_approved:
        return {**base, "status": "owner_approval_required"}
    if not live_execute:
        return {**base, "status": "live_execute_confirmation_required"}
    if not connector_ready:
        return {**base, "status": "blocked_connector_not_ready"}
    return {**base, "status": "ready_for_whatsapp_transport", "ready_for_whatsapp_transport": True}


def self_test():
    denied = build_execution_plan("+971500000000", "Please confirm the coordination meeting.", False, False, True)
    confirmation = build_execution_plan("+971500000000", "Please confirm the coordination meeting.", True, False, True)
    ready = build_execution_plan("+971500000000", "Please confirm the coordination meeting.", True, True, True)
    blocked = build_execution_plan("+971500000000", "Please confirm the coordination meeting.", True, True, False)
    sensitive = build_execution_plan("+971500000000", "Send my access token secret", True, True, True)
    checks = {
        "owner_approval_gate_verified": denied["status"] == "owner_approval_required" and not denied["ready_for_whatsapp_transport"],
        "explicit_live_execute_gate_verified": confirmation["status"] == "live_execute_confirmation_required" and not confirmation["ready_for_whatsapp_transport"],
        "connector_readiness_gate_verified": blocked["status"] == "blocked_connector_not_ready" and not blocked["ready_for_whatsapp_transport"],
        "approved_handoff_verified": ready["status"] == "ready_for_whatsapp_transport" and ready["ready_for_whatsapp_transport"],
        "sensitive_content_rejection_verified": sensitive["status"] == "sensitive_content_rejected",
    }
    return {
        "ok": all(checks.values()), **checks,
        "synthetic_inputs_only": True,
        "external_network_accessed": False,
        "real_whatsapp_sent": False,
        "credentials_exposed": False,
        "private_payloads_exposed": False,
    }
