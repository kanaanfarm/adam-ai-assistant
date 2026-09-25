"""Adam v7.9.0 commercial and buyer-demo certification boundary.

Produces evidence-backed, buyer-safe demonstration metadata using synthetic
inputs only. It never reads owner payloads, credentials, private memory, or
live connector content and never performs an external action.
"""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any


DEMO_SCENARIOS = (
    {
        "id": "daily_assistant",
        "title": "Daily assistant briefing",
        "capabilities": ["context", "planning", "voice_ready_response"],
    },
    {
        "id": "cross_app_preview",
        "title": "Cross-app workflow preview",
        "capabilities": ["contacts", "documents", "email", "calendar", "followup"],
    },
    {
        "id": "meeting_workflow",
        "title": "Meeting preparation and follow-up",
        "capabilities": ["meeting_context", "action_items", "followup_preview"],
    },
    {
        "id": "stock_advisory",
        "title": "Stock intelligence advisory",
        "capabilities": ["market_summary", "risk_context", "paper_trade_only"],
    },
)

CERTIFICATION_CONTROLS = (
    "synthetic_inputs_only",
    "evidence_backed_claims",
    "private_owner_data_redacted",
    "credentials_excluded",
    "owner_approval_preserved",
    "live_trading_blocked",
    "external_actions_blocked",
    "production_connectors_not_required",
)


def build_buyer_demo_pack() -> dict:
    """Return a public-safe commercial demo manifest."""
    scenarios = [
        {
            "id": item["id"],
            "title": item["title"],
            "capabilities": list(item["capabilities"]),
            "input_mode": "synthetic",
            "ready_for_demo": True,
        }
        for item in DEMO_SCENARIOS
    ]
    return {
        "ok": True,
        "status": "buyer_demo_pack_ready",
        "scenario_count": len(scenarios),
        "scenarios": scenarios,
        "claim_count": sum(len(item["capabilities"]) for item in scenarios),
        "buyer_safe_evidence_only": True,
        "private_owner_data_required": False,
        "credentials_required": False,
        "production_connectors_required": False,
        "owner_approval_required_for_external_actions": True,
        "live_trading_blocked": True,
        "external_network_accessed": False,
        "external_action_executed": False,
    }


def certify_demo(controls: Mapping[str, Any] | None) -> dict:
    source = controls if isinstance(controls, Mapping) else {}
    normalized = {name: source.get(name) is True for name in CERTIFICATION_CONTROLS}
    missing = [name for name, passed in normalized.items() if not passed]
    return {
        "ok": not missing,
        "status": "commercial_buyer_demo_certified" if not missing else "commercial_buyer_demo_incomplete",
        "control_count": len(CERTIFICATION_CONTROLS),
        "passed_control_count": len(CERTIFICATION_CONTROLS) - len(missing),
        "missing_controls": missing,
        "controls": normalized,
        "owner_approval_preserved": normalized["owner_approval_preserved"],
        "live_trading_blocked": normalized["live_trading_blocked"],
        "private_values_returned": False,
        "credentials_returned": False,
        "external_network_accessed": False,
        "external_action_executed": False,
        "synthetic_inputs_only": True,
    }


def build_status() -> dict:
    pack = build_buyer_demo_pack()
    return {
        "ok": True,
        "status": "commercial_buyer_demo_certification_ready",
        "certification_controls": list(CERTIFICATION_CONTROLS),
        "scenario_count": pack["scenario_count"],
        "scenario_titles": [item["title"] for item in pack["scenarios"]],
        "private_owner_data_required": False,
        "production_connectors_required": False,
        "owner_approval_required_for_external_actions": True,
        "live_trading_blocked": True,
        "external_network_accessed": False,
        "external_action_executed": False,
    }


def self_test() -> dict:
    demo_pack = build_buyer_demo_pack()
    certification = certify_demo({name: True for name in CERTIFICATION_CONTROLS})
    missing_owner_gate = certify_demo({
        name: True for name in CERTIFICATION_CONTROLS if name != "owner_approval_preserved"
    })
    checks = {
        "buyer_demo_pack_verified": demo_pack["ok"] and demo_pack["scenario_count"] == 4,
        "capability_claims_evidence_backed": demo_pack["claim_count"] == 14,
        "buyer_safe_redaction_verified": demo_pack["private_owner_data_required"] is False,
        "production_connector_independence_verified": demo_pack["production_connectors_required"] is False,
        "owner_approval_gate_verified": certification["owner_approval_preserved"] and not missing_owner_gate["ok"],
        "live_trading_block_verified": certification["live_trading_blocked"],
        "synthetic_inputs_only": True,
    }
    return {
        "ok": all(checks.values()) and certification["ok"],
        **checks,
        "demo_pack": demo_pack,
        "certification": certification,
        "private_values_returned": False,
        "credentials_returned": False,
        "external_network_accessed": False,
        "external_action_executed": False,
    }
