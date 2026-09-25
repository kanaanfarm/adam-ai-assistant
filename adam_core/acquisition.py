"""Buyer-facing acquisition readiness helpers for Adam Acquisition v1.3.

The output is deliberately capability-level only. It does not expose credentials,
contact details, message bodies, attachment contents, prompts, or private memory.
"""
from __future__ import annotations


def demo_scenarios():
    return [
        {
            "id": "email_document_operator",
            "name": "Email + Document Operator",
            "goal": "Review material, prepare a response, request owner approval, execute only after approval, and support follow-up.",
            "approval_required": True,
            "evidence_endpoints": ["/api/workflows", "/api/governance"],
        },
        {
            "id": "meeting_operator",
            "name": "Cross-App Meeting Operator",
            "goal": "Resolve a contact, prepare communication and calendar actions, and keep consequential execution owner-controlled.",
            "approval_required": True,
            "evidence_endpoints": ["/api/governance/policy", "/api/governance"],
        },
        {
            "id": "controlled_business_operator",
            "name": "Controlled Business Operator",
            "goal": "Prepare business actions from approved context while enforcing owner policy and producing privacy-safe audit evidence.",
            "approval_required": True,
            "evidence_endpoints": ["/api/acquisition/readiness", "/api/governance"],
        },
    ]


def acquisition_readiness(*, version, governance, runtime, record_sources):
    safety = dict((runtime or {}).get("safety") or {})
    runtime_state = dict((runtime or {}).get("runtime") or {})
    policy = dict((governance or {}).get("policy") or {})
    controls = {
        "owner_approval_model": bool(safety.get("owner_approval_model")),
        "live_trading_blocked": bool(safety.get("live_trading_blocked")),
        "hardcoded_flask_secret": bool(safety.get("hardcoded_flask_secret")),
        "execution_confirmation_required": bool(policy.get("execution_confirmation_required")),
        "attachment_context_exposed": bool(policy.get("attachment_context_exposed")),
        "credentials_exposed": bool(policy.get("credentials_exposed")),
    }
    checks = {
        "secure_runtime_secret": controls["hardcoded_flask_secret"] is False,
        "owner_approval_enforced": controls["owner_approval_model"] is True and controls["execution_confirmation_required"] is True,
        "live_trading_safety": controls["live_trading_blocked"] is True,
        "privacy_safe_governance": controls["attachment_context_exposed"] is False and controls["credentials_exposed"] is False,
        "data_directory_available": bool(runtime_state.get("data_dir_available")),
    }
    return {
        "product": "Adam Acquisition",
        "version": version,
        "positioning": "Personal and business AI operator with owner-controlled execution and privacy-safe audit evidence.",
        "readiness_checks": checks,
        "all_core_checks_pass": all(checks.values()),
        "governance_evidence": {
            "workflow_count": int((governance or {}).get("workflow_count") or 0),
            "approval_events": int((governance or {}).get("approval_events") or 0),
            "completion_events": int((governance or {}).get("completion_events") or 0),
            "record_sources": dict(record_sources or {}),
        },
        "integration_configuration": {
            "ai_provider_configured": bool(runtime_state.get("ai_provider_configured")),
            "microsoft_client_configured": bool(runtime_state.get("microsoft_client_configured")),
            "whatsapp_configured": bool(runtime_state.get("whatsapp_configured")),
            "alpaca_paper_configured": bool(runtime_state.get("alpaca_paper_configured")),
        },
        "demo_scenarios": demo_scenarios(),
        "privacy": {
            "credentials_exposed": False,
            "contact_details_exposed": False,
            "message_bodies_exposed": False,
            "attachment_contents_exposed": False,
            "private_memory_exposed": False,
        },
    }
