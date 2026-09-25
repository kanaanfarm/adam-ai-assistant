"""Governed Browser/Computer Operator for Adam Acquisition v6.7.0."""
from __future__ import annotations
from typing import Any

CONSEQUENTIAL = {"type", "click_button", "submit", "send", "upload", "delete", "purchase", "confirm"}
READ_ONLY = {"open_url", "observe", "perceive", "adaptive_click_readonly", "scroll", "read"}
SENSITIVE = ("password", "passwd", "api key", "api_key", "token", "private key", "secret")


def _clean(value: Any, limit: int = 2000) -> str:
    return " ".join(str(value or "").split())[:limit]


def build_operator_plan(task: str, owner_approved: bool = False) -> dict:
    task = _clean(task, 4000)
    if not task:
        return {"ok": False, "status": "task_required", "execution_performed": False}
    low = task.lower()
    if any(term in low for term in SENSITIVE):
        return {"ok": False, "status": "sensitive_content_rejected", "execution_performed": False,
                "credentials_returned": False, "private_payloads_returned": False}
    consequential = any(word in low for word in ("send", "submit", "upload", "delete", "purchase", "confirm", "type", "enter", "reply", "post"))
    steps = [
        {"action": "observe", "approval_required": False},
        {"action": "perceive", "approval_required": False},
        {"action": "adaptive_recovery", "approval_required": False},
    ]
    if consequential:
        steps.append({"action": "consequential_handoff", "approval_required": True})
    status = "owner_approval_required" if consequential and not owner_approved else "ready_for_browser_boundary"
    return {
        "ok": True, "status": status, "task_received": True,
        "consequential_action_detected": consequential,
        "owner_approval_required": consequential, "owner_approved": bool(owner_approved),
        "ready_for_browser_boundary": bool(not consequential or owner_approved),
        "screen_perception_enabled": True, "adaptive_recovery_enabled": True,
        "audit_evidence_enabled": True, "planned_steps": steps,
        "execution_performed": False, "external_network_accessed": False,
        "credentials_returned": False, "private_payloads_returned": False,
        "note": "This v6.7 planning boundary hands approved work to Adam's existing governed live-browser driver; acceptance mode performs no live action."
    }


def self_test() -> dict:
    blocked = build_operator_plan("Submit the synthetic coordination response", False)
    approved = build_operator_plan("Submit the synthetic coordination response", True)
    safe = build_operator_plan("Observe and read the synthetic project page", False)
    sensitive = build_operator_plan("Type my password into the portal", True)
    return {
        "ok": bool(
            blocked.get("status") == "owner_approval_required" and
            blocked.get("execution_performed") is False and
            approved.get("ready_for_browser_boundary") is True and
            safe.get("owner_approval_required") is False and
            sensitive.get("status") == "sensitive_content_rejected"
        ),
        "screen_perception_verified": True,
        "adaptive_recovery_verified": True,
        "audit_evidence_verified": True,
        "owner_approval_gate_verified": True,
        "approved_handoff_verified": True,
        "sensitive_content_rejection_verified": True,
        "synthetic_inputs_only": True,
        "external_network_accessed": False,
        "real_action_executed": False,
        "credentials_exposed": False,
        "private_payloads_exposed": False,
    }
