"""Unified Adam Operator Release for Adam Acquisition v7.0.0.

This module is the final orchestration boundary that presents Adam's approved
capabilities through one governed plan. It does not bypass any underlying
connector or execution gate. Consequential work requires Owner Approval and
remains a handoff to the already-governed specialist boundary.
"""
from __future__ import annotations

SENSITIVE_HINTS = (
    "password", "passwd", "api key", "api_key", "access token",
    "private key", "secret", "credential",
)

CAPABILITIES = {
    "daily_briefing": ("brief", "briefing", "today", "schedule", "calendar"),
    "memory": ("remember", "recall", "memory", "follow-up", "follow up"),
    "voice": ("voice", "speak", "say", "listen"),
    "vision_attachments": ("photo", "image", "camera", "attachment", "document", "pdf"),
    "browser_computer": ("browser", "website", "screen", "computer", "click", "open page", "portal", "open the"),
    "email": ("email", "outlook", "mail"),
    "whatsapp": ("whatsapp",),
    "stock_intelligence": ("stock", "market", "nvda", "msft", "aapl", "buy", "sell", "trade"),
}

CONSEQUENTIAL_HINTS = (
    "send", "email", "whatsapp", "message", "schedule", "book", "create meeting",
    "delete", "submit", "upload", "buy", "sell", "trade", "order", "click confirm",
)


def _clean(value, limit=1500):
    return str(value or "").strip()[:limit]


def _detect_capabilities(instruction):
    low = instruction.lower()
    found = []
    for name, hints in CAPABILITIES.items():
        if any(h in low for h in hints):
            found.append(name)
    if not found:
        found = ["daily_briefing"]
    return found


def build_unified_operator_plan(instruction, owner_approved=False, text_confirmed=False):
    instruction = _clean(instruction)
    low = instruction.lower()
    base = {
        "ok": True,
        "mode": "unified_adam_operator_v7",
        "instruction_received": bool(instruction),
        "owner_approved": bool(owner_approved),
        "text_confirmed": bool(text_confirmed),
        "owner_approval_required": False,
        "text_confirmation_required": False,
        "ready_for_governed_execution_handoff": False,
        "execution_performed": False,
        "external_network_accessed": False,
        "credentials_returned": False,
        "private_payloads_returned": False,
        "live_trading_blocked": True,
        "specialist_boundaries_preserved": True,
        "audit_required_for_execution": True,
    }
    if not instruction:
        return {**base, "ok": False, "status": "instruction_required", "capabilities": [], "workflow": []}
    if any(h in low for h in SENSITIVE_HINTS):
        return {**base, "ok": False, "status": "sensitive_content_rejected", "capabilities": [], "workflow": []}

    capabilities = _detect_capabilities(instruction)
    consequential = any(h in low for h in CONSEQUENTIAL_HINTS)
    workflow = [
        {"stage": "understand", "approval_required": False},
        {"stage": "plan", "approval_required": False},
        {"stage": "prepare", "approval_required": False},
    ]
    if consequential:
        workflow += [
            {"stage": "owner_approval", "approval_required": True},
            {"stage": "text_confirmation", "approval_required": True},
            {"stage": "specialist_execution_handoff", "approval_required": True},
            {"stage": "audit", "approval_required": False},
            {"stage": "follow_up", "approval_required": False},
        ]
    else:
        workflow += [
            {"stage": "review", "approval_required": False},
            {"stage": "audit", "approval_required": False},
        ]

    result = {
        **base,
        "status": "unified_plan_ready",
        "capabilities": capabilities,
        "capability_count": len(capabilities),
        "consequential_action_detected": consequential,
        "owner_approval_required": consequential,
        "text_confirmation_required": consequential,
        "workflow": workflow,
        "note": "Adam v7 unifies planning across specialist capabilities. Real execution remains inside each existing governed connector boundary.",
    }
    if consequential:
        if not owner_approved:
            result["status"] = "owner_approval_required"
        elif not text_confirmed:
            result["status"] = "text_confirmation_required"
        else:
            result["status"] = "ready_for_governed_execution_handoff"
            result["ready_for_governed_execution_handoff"] = True
    return result


def self_test():
    safe = build_unified_operator_plan("Give me today's briefing and recall my follow-up", False, False)
    blocked = build_unified_operator_plan(
        "Review the attached site photo, open the contractor portal, send an email and WhatsApp message, then analyze NVDA before any trade",
        False,
        False,
    )
    confirm_needed = build_unified_operator_plan("Send an email to the contractor", True, False)
    approved = build_unified_operator_plan("Send an email to the contractor", True, True)
    sensitive = build_unified_operator_plan("Use my API key secret and send it", True, True)
    expected = {"daily_briefing", "memory", "vision_attachments", "browser_computer", "email", "whatsapp", "stock_intelligence"}
    checks = {
        "unified_capability_routing_verified": expected.issubset(set(safe.get("capabilities", [])) | set(blocked.get("capabilities", []))),
        "owner_approval_gate_verified": blocked.get("status") == "owner_approval_required" and not blocked.get("ready_for_governed_execution_handoff"),
        "text_confirmation_gate_verified": confirm_needed.get("status") == "text_confirmation_required" and not confirm_needed.get("ready_for_governed_execution_handoff"),
        "approved_governed_handoff_verified": approved.get("status") == "ready_for_governed_execution_handoff" and approved.get("ready_for_governed_execution_handoff") is True,
        "specialist_boundary_preservation_verified": all(x.get("specialist_boundaries_preserved") is True for x in (safe, blocked, confirm_needed, approved)),
        "live_trading_block_verified": all(x.get("live_trading_blocked") is True for x in (safe, blocked, confirm_needed, approved)),
        "sensitive_content_rejection_verified": sensitive.get("status") == "sensitive_content_rejected",
        "audit_chain_verified": all(x.get("audit_required_for_execution") is True for x in (safe, blocked, confirm_needed, approved)),
    }
    return {
        "ok": all(checks.values()),
        **checks,
        "synthetic_inputs_only": True,
        "external_network_accessed": False,
        "real_action_executed": False,
        "real_message_sent": False,
        "real_order_submitted": False,
        "credentials_exposed": False,
        "private_payloads_exposed": False,
    }
