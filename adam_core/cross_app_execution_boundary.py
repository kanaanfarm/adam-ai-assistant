"""Buyer-safe boundary evidence and self-test for cross-app execution v4.3."""
from __future__ import annotations
from .cross_app_orchestrator import public_manifest, preview_plan, execute_plan


def build_cross_app_execution_manifest(version: str) -> dict:
    return {
        "schema": "adam-acquisition-cross-app-execution/v1",
        "product": "Adam Acquisition",
        "version": version,
        "status": "cross_app_execution_foundation_tested",
        "cross_app_execution": {
            "boundary_module": "adam_core.cross_app_orchestrator",
            "capabilities": public_manifest(),
        },
        "next_targets": ["meeting agent", "cross-app live connector binding", "workflow learning"],
    }


def cross_app_execution_is_privacy_safe(payload: dict) -> bool:
    caps = (((payload or {}).get("cross_app_execution") or {}).get("capabilities") or {})
    p = caps.get("privacy") or {}
    return bool(
        caps.get("per_step_owner_approval")
        and not p.get("credentials_stored_in_orchestrator")
        and not p.get("message_bodies_exposed_in_buyer_evidence")
        and not p.get("contact_values_exposed_in_buyer_evidence")
        and not p.get("urls_exposed_in_buyer_evidence")
        and not p.get("document_contents_exposed_in_buyer_evidence")
    )


def cross_app_execution_self_test() -> dict:
    calls = []
    def synthetic(step):
        calls.append((step.connector, step.action))
        return True

    adapters = {k: synthetic for k in ["browser", "documents", "email", "calendar", "whatsapp"]}
    blocked_plan = [
        {"connector":"documents","action":"read","target":"synthetic.docx"},
        {"connector":"email","action":"draft","summary":"synthetic draft"},
        {"connector":"email","action":"send","target":"synthetic recipient","owner_approved":False},
    ]
    blocked = execute_plan(blocked_plan, adapters)
    blocked_calls = list(calls)
    calls.clear()
    approved_plan = [dict(x) for x in blocked_plan]
    approved_plan[-1] = dict(approved_plan[-1], owner_approved=True)
    approved = execute_plan(approved_plan, adapters)
    preview = preview_plan(blocked_plan)
    return {
        "ok": bool(
            blocked.get("status") == "approval_required"
            and blocked.get("blocked_step") == 3
            and blocked.get("completed_steps") == 2
            and len(blocked_calls) == 2
            and approved.get("ok") is True
            and approved.get("completed_steps") == 3
            and len(calls) == 3
            and preview.get("approval_required_steps") == [3]
        ),
        "cross_app_steps_planned": 3,
        "read_prepare_steps_executed_before_gate": len(blocked_calls),
        "consequential_step_blocked_without_approval": blocked.get("blocked_step") == 3,
        "approved_consequential_step_executed": approved.get("ok") is True and len(calls) == 3,
        "owner_gate_preserved_per_step": bool(blocked.get("owner_gate_preserved") and approved.get("owner_gate_preserved")),
        "preview_identified_approval_step": preview.get("approval_required_steps") == [3],
        "external_network_accessed": False,
        "real_application_controlled": False,
        "credentials_used": False,
        "private_values_returned": False,
    }
