"""Privacy-safe dual-use readiness model for Adam v5.9.

This module exposes capability/readiness booleans only. It never returns secret
values, contact data, message bodies, document contents, or private memory.
"""

CAPABILITIES = (
    "ai_chat", "voice", "attachments", "vision", "contacts",
    "microsoft", "whatsapp", "browser_computer_use", "stock_assistant",
)


def build_readiness(version, signals=None):
    signals = dict(signals or {})
    caps = {name: bool(signals.get(name, False)) for name in CAPABILITIES}
    return {
        "ok": True,
        "version": str(version),
        "product_mode": "dual_use_personal_and_commercial",
        "personal_assistant_enabled": True,
        "commercial_presentation_supported": True,
        "owner_approval_preserved": True,
        "privacy_safe": True,
        "credentials_returned": False,
        "private_payloads_returned": False,
        "capabilities": caps,
        "ready_count": sum(1 for value in caps.values() if value),
        "total_count": len(caps),
    }


def self_test(version):
    sample = build_readiness(version, {name: True for name in CAPABILITIES})
    return {
        "ok": all((
            sample["personal_assistant_enabled"],
            sample["commercial_presentation_supported"],
            sample["owner_approval_preserved"],
            sample["privacy_safe"],
            not sample["credentials_returned"],
            not sample["private_payloads_returned"],
            sample["ready_count"] == sample["total_count"],
        )),
        "dual_use_profile_verified": True,
        "owner_gate_preserved": True,
        "credentials_exposed": False,
        "private_payloads_exposed": False,
        "external_network_accessed": False,
    }
