"""Adam v8.1.0 production and commercial dual-use release boundary.

Certifies release metadata and mode isolation with synthetic inputs. No
connector is activated and no external action is performed by this module.
"""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any


OPERATING_MODES = {
    "personal_operation": {
        "description": "Owner-controlled personal assistant operation",
        "synthetic_only": False,
        "private_owner_data_allowed": True,
        "production_connectors_allowed_when_configured": True,
        "owner_approval_required_for_external_actions": True,
        "live_trading_blocked": True,
    },
    "buyer_presentation": {
        "description": "Buyer-safe product demonstration",
        "synthetic_only": True,
        "private_owner_data_allowed": False,
        "production_connectors_allowed_when_configured": False,
        "owner_approval_required_for_external_actions": True,
        "live_trading_blocked": True,
    },
}

RELEASE_CONTROLS = (
    "single_codebase_verified",
    "operating_modes_isolated",
    "buyer_mode_synthetic_only",
    "buyer_mode_private_data_blocked",
    "buyer_mode_connectors_blocked",
    "personal_mode_owner_controlled",
    "owner_approval_preserved",
    "credentials_externalized",
    "live_trading_blocked",
    "release_evidence_complete",
)


def select_mode(mode: str | None) -> dict:
    requested = str(mode or "").strip().casefold()
    config = OPERATING_MODES.get(requested)
    if config is None:
        return {
            "ok": False,
            "status": "invalid_operating_mode",
            "allowed_modes": sorted(OPERATING_MODES),
            "external_action_executed": False,
        }
    return {
        "ok": True,
        "status": "operating_mode_selected",
        "mode": requested,
        **config,
        "mode_selection_changed_runtime_configuration": False,
        "external_network_accessed": False,
        "external_action_executed": False,
    }


def build_release_manifest() -> dict:
    return {
        "ok": True,
        "status": "production_commercial_release_manifest_ready",
        "product": "Adam Acquisition",
        "release": "v8.1.0",
        "release_class": "dual_use_production_commercial",
        "single_codebase": True,
        "operating_modes": {name: dict(config) for name, config in OPERATING_MODES.items()},
        "required_owner_runtime_activation_for_live_connectors": True,
        "automatic_connector_activation": False,
        "automatic_buyer_outreach": False,
        "live_trading_blocked": True,
        "credentials_returned": False,
        "private_values_returned": False,
        "external_network_accessed": False,
        "external_action_executed": False,
    }


def certify_release(controls: Mapping[str, Any] | None) -> dict:
    source = controls if isinstance(controls, Mapping) else {}
    normalized = {name: source.get(name) is True for name in RELEASE_CONTROLS}
    missing = [name for name, passed in normalized.items() if not passed]
    return {
        "ok": not missing,
        "status": "production_commercial_release_certified" if not missing else "production_commercial_release_incomplete",
        "control_count": len(RELEASE_CONTROLS),
        "passed_control_count": len(RELEASE_CONTROLS) - len(missing),
        "missing_controls": missing,
        "controls": normalized,
        "owner_approval_preserved": normalized["owner_approval_preserved"],
        "live_trading_blocked": normalized["live_trading_blocked"],
        "credentials_returned": False,
        "private_values_returned": False,
        "external_network_accessed": False,
        "external_action_executed": False,
        "synthetic_inputs_only": True,
    }


def build_status() -> dict:
    return {
        "ok": True,
        "status": "production_commercial_release_certification_ready",
        "release": "v8.1.0",
        "release_controls": list(RELEASE_CONTROLS),
        "operating_modes": sorted(OPERATING_MODES),
        "single_codebase": True,
        "owner_approval_required_for_external_actions": True,
        "live_trading_blocked": True,
        "automatic_connector_activation": False,
        "external_network_accessed": False,
        "external_action_executed": False,
    }


def self_test() -> dict:
    manifest = build_release_manifest()
    personal = select_mode("personal_operation")
    buyer = select_mode("buyer_presentation")
    certification = certify_release({name: True for name in RELEASE_CONTROLS})
    missing_isolation = certify_release({
        name: True for name in RELEASE_CONTROLS if name != "operating_modes_isolated"
    })
    checks = {
        "single_codebase_verified": manifest["single_codebase"],
        "dual_mode_selection_verified": personal["ok"] and buyer["ok"],
        "operating_modes_isolated_verified": buyer["synthetic_only"] and not buyer["private_owner_data_allowed"] and not buyer["production_connectors_allowed_when_configured"] and not missing_isolation["ok"],
        "personal_mode_owner_control_verified": personal["owner_approval_required_for_external_actions"],
        "buyer_mode_safety_verified": buyer["owner_approval_required_for_external_actions"] and buyer["live_trading_blocked"],
        "automatic_activation_blocked_verified": manifest["automatic_connector_activation"] is False,
        "owner_approval_gate_verified": certification["owner_approval_preserved"],
        "live_trading_block_verified": certification["live_trading_blocked"],
        "synthetic_inputs_only": True,
    }
    return {
        "ok": all(checks.values()) and certification["ok"],
        **checks,
        "release_manifest": manifest,
        "release_certification": certification,
        "credentials_returned": False,
        "private_values_returned": False,
        "external_network_accessed": False,
        "external_action_executed": False,
    }
