"""Governed Computer Use foundation for Adam Acquisition v4.0."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable

READ_ACTIONS = frozenset({"observe", "open_url", "click", "scroll", "read", "search", "download_preview"})
CONSEQUENTIAL_ACTIONS = frozenset({"type_sensitive", "submit", "send", "delete", "purchase", "confirm", "upload", "financial_action"})
MAX_TASK_CHARS = 4000
MAX_STEPS = 40

class ComputerUseError(ValueError): pass
class ApprovalRequired(PermissionError): pass

@dataclass(frozen=True)
class ComputerAction:
    kind: str
    target: str = ""
    value: str = ""

    @property
    def approval_required(self) -> bool:
        return self.kind in CONSEQUENTIAL_ACTIONS


def normalize_task(task: str) -> str:
    text = " ".join(str(task or "").split())
    if not text: raise ComputerUseError("A computer-use task is required.")
    if len(text) > MAX_TASK_CHARS: raise ComputerUseError("Computer-use task is too long.")
    return text


def validate_action(action: ComputerAction) -> ComputerAction:
    if action.kind not in READ_ACTIONS | CONSEQUENTIAL_ACTIONS:
        raise ComputerUseError("Unsupported computer-use action.")
    if len(action.target) > 1000 or len(action.value) > 4000:
        raise ComputerUseError("Computer-use action exceeds safety bounds.")
    return action


def execute_action(action: ComputerAction, driver: Callable[[ComputerAction], Any], *, owner_approved: bool = False) -> Any:
    action = validate_action(action)
    if action.approval_required and owner_approved is not True:
        raise ApprovalRequired("Explicit owner approval is required before this computer action.")
    return driver(action)


def public_action(action: ComputerAction) -> dict:
    action = validate_action(action)
    return {"kind": action.kind, "approval_required": action.approval_required, "target_present": bool(action.target), "value_present": bool(action.value)}


def synthetic_demo() -> dict:
    actions = [
        ComputerAction("open_url", "synthetic supplier portal"),
        ComputerAction("search", "project register"),
        ComputerAction("read", "latest submission"),
        ComputerAction("submit", "response form", "synthetic response"),
    ]
    executed=[]; blocked=False
    def fake_driver(a): executed.append(a.kind); return {"ok": True, "kind": a.kind}
    for a in actions[:-1]: execute_action(a, fake_driver)
    try: execute_action(actions[-1], fake_driver)
    except ApprovalRequired: blocked=True
    execute_action(actions[-1], fake_driver, owner_approved=True)
    return {"ok": blocked and executed == ["open_url","search","read","submit"], "read_actions_executed":3, "consequential_action_blocked_without_approval":blocked, "approved_action_executed":executed[-1]=="submit", "external_network_accessed":False, "real_application_controlled":False, "private_values_returned":False}
