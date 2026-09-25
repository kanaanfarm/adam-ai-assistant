"""Governed cross-application workflow orchestration for Adam Acquisition v4.3.

The orchestrator separates planning from execution. Read/prepare steps may run
through injected adapters, while consequential steps require explicit owner
approval at the exact step. The core never owns credentials or transport state.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Mapping

MAX_WORKFLOW_STEPS = 12
MAX_STEP_TEXT_CHARS = 500
ALLOWED_CONNECTORS = {"browser", "documents", "email", "calendar", "whatsapp"}
CONSEQUENTIAL_ACTIONS = {"send", "submit", "delete", "purchase", "confirm", "upload", "invite", "financial_action"}
READ_PREPARE_ACTIONS = {"observe", "read", "search", "extract", "draft", "prepare", "lookup", "navigate"}

class CrossAppExecutionError(RuntimeError):
    pass


def _clean(value: Any, limit: int = MAX_STEP_TEXT_CHARS) -> str:
    return " ".join(str(value or "").split())[:limit]


@dataclass(frozen=True)
class WorkflowStep:
    connector: str
    action: str
    target: str = ""
    summary: str = ""
    owner_approved: bool = False

    @property
    def consequential(self) -> bool:
        return self.action in CONSEQUENTIAL_ACTIONS

    def public_dict(self) -> dict:
        # No values, addresses, message bodies, URLs or credentials are exposed.
        return {
            "connector": self.connector,
            "action": self.action,
            "consequential": self.consequential,
            "owner_approved": bool(self.owner_approved),
            "target_present": bool(self.target),
            "summary_present": bool(self.summary),
        }


def normalize_plan(raw_steps: list[dict] | None) -> list[WorkflowStep]:
    steps: list[WorkflowStep] = []
    for raw in list(raw_steps or [])[:MAX_WORKFLOW_STEPS]:
        connector = _clean(raw.get("connector"), 40).lower()
        action = _clean(raw.get("action"), 40).lower()
        if connector not in ALLOWED_CONNECTORS:
            raise CrossAppExecutionError("Unsupported cross-app connector.")
        if action not in (READ_PREPARE_ACTIONS | CONSEQUENTIAL_ACTIONS):
            raise CrossAppExecutionError("Unsupported cross-app action.")
        steps.append(WorkflowStep(
            connector=connector,
            action=action,
            target=_clean(raw.get("target")),
            summary=_clean(raw.get("summary")),
            owner_approved=raw.get("owner_approved") is True,
        ))
    if not steps:
        raise CrossAppExecutionError("Workflow must contain at least one step.")
    return steps


def preview_plan(raw_steps: list[dict] | None) -> dict:
    steps = normalize_plan(raw_steps)
    return {
        "ok": True,
        "mode": "preview",
        "step_count": len(steps),
        "consequential_steps": sum(1 for s in steps if s.consequential),
        "approval_required_steps": [i + 1 for i, s in enumerate(steps) if s.consequential and not s.owner_approved],
        "steps": [s.public_dict() for s in steps],
        "private_values_returned": False,
    }


def execute_plan(raw_steps: list[dict] | None, adapters: Mapping[str, Callable[[WorkflowStep], Any]]) -> dict:
    steps = normalize_plan(raw_steps)
    receipts: list[dict] = []
    for index, step in enumerate(steps, start=1):
        if step.consequential and not step.owner_approved:
            return {
                "ok": False,
                "status": "approval_required",
                "blocked_step": index,
                "connector": step.connector,
                "action": step.action,
                "completed_steps": len(receipts),
                "owner_gate_preserved": True,
                "private_values_returned": False,
                "receipts": receipts,
            }
        adapter = adapters.get(step.connector)
        if adapter is None:
            raise CrossAppExecutionError("No execution adapter is available for a requested connector.")
        result = adapter(step)
        receipts.append({
            "step": index,
            "connector": step.connector,
            "action": step.action,
            "consequential": step.consequential,
            "executed": True,
            "adapter_ok": bool(result is not False),
        })
    return {
        "ok": True,
        "status": "completed",
        "completed_steps": len(receipts),
        "owner_gate_preserved": True,
        "private_values_returned": False,
        "receipts": receipts,
    }


def public_manifest() -> dict:
    return {
        "plan_preview": True,
        "cross_app_execution": True,
        "injected_connector_adapters": True,
        "per_step_owner_approval": True,
        "supported_connectors": sorted(ALLOWED_CONNECTORS),
        "read_prepare_actions": sorted(READ_PREPARE_ACTIONS),
        "consequential_actions": sorted(CONSEQUENTIAL_ACTIONS),
        "bounds": {"max_workflow_steps": MAX_WORKFLOW_STEPS, "max_step_text_chars": MAX_STEP_TEXT_CHARS},
        "privacy": {
            "credentials_stored_in_orchestrator": False,
            "message_bodies_exposed_in_buyer_evidence": False,
            "contact_values_exposed_in_buyer_evidence": False,
            "urls_exposed_in_buyer_evidence": False,
            "document_contents_exposed_in_buyer_evidence": False,
        },
    }
