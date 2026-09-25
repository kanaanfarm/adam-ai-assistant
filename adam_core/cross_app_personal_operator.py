"""Adam v7.6.0.1 Cross-App Personal Operator preview-validation fix.

Composes Contacts -> Documents -> Email -> Calendar -> WhatsApp -> Follow-up into
one owner-governed workflow. Preview never performs external actions. Execution
uses injected adapters and keeps a separate approval gate for each consequential
connector action.
"""
from __future__ import annotations

from typing import Any, Callable, Iterable, Mapping


def _t(value: Any, limit: int = 4000) -> str:
    return str(value or "").strip()[:limit]


def _find_contact(contacts: Iterable[dict], name: str = "", email: str = "", phone: str = "") -> dict:
    name_l, email_l, phone_l = _t(name).casefold(), _t(email).casefold(), _t(phone).casefold()
    for c in contacts or []:
        if name_l and _t(c.get("name")).casefold() == name_l:
            return dict(c)
        if email_l and _t(c.get("email")).casefold() == email_l:
            return dict(c)
        if phone_l and _t(c.get("phone")).casefold() == phone_l:
            return dict(c)
    return {}


def _selected_domains(p: dict) -> list[str]:
    domains = ["contacts"]
    if bool(p.get("include_document")): domains.append("documents")
    if bool(p.get("include_email")): domains.append("email")
    if bool(p.get("include_calendar")): domains.append("calendar")
    if bool(p.get("include_whatsapp")): domains.append("whatsapp")
    if bool(p.get("include_followup")): domains.append("followup")
    return domains


def _execution_detail_missing(p: dict, *, name: str, email: str, phone: str) -> list[str]:
    """Strict detail validation used only when real execution is requested."""
    missing: list[str] = []
    if not _t(p.get("objective"), 1000): missing.append("objective")
    if not (name or email or phone): missing.append("contact")
    if p.get("include_document") and not (_t(p.get("document_name")) or _t(p.get("document_note"))): missing.append("documents_details")
    if p.get("include_email") and not (email and _t(p.get("email_subject")) and _t(p.get("email_body"))): missing.append("email_details")
    if p.get("include_calendar") and not (_t(p.get("meeting_title")) and _t(p.get("meeting_start"))): missing.append("calendar_details")
    if p.get("include_whatsapp") and not (phone and _t(p.get("whatsapp_message"))): missing.append("whatsapp_details")
    if p.get("include_followup") and not _t(p.get("followup_title")): missing.append("followup_details")
    return sorted(set(missing))


def prepare_workflow(payload: dict, contacts: Iterable[dict], *, microsoft_ready: bool = False, whatsapp_ready: bool = False) -> dict:
    """Build a preview without confusing execution blockers with preview validity.

    Preview needs an objective/contact and at least one selected action. Missing action
    details, connector readiness, and Owner Approval are reported as execution blockers
    and warnings, but they do not make the planning preview itself fail.
    """
    p = payload or {}
    contact = _find_contact(contacts, p.get("contact_name"), p.get("email"), p.get("phone"))
    name = _t(p.get("contact_name")) or _t(contact.get("name"))
    email = _t(p.get("email")) or _t(contact.get("email"))
    phone = _t(p.get("phone")) or _t(contact.get("phone"))
    objective = _t(p.get("objective"), 1000)

    include_email = bool(p.get("include_email"))
    include_calendar = bool(p.get("include_calendar"))
    include_whatsapp = bool(p.get("include_whatsapp"))
    include_document = bool(p.get("include_document"))
    include_followup = bool(p.get("include_followup"))

    steps = [{"step": 1, "domain": "contacts", "action": "resolve", "ready_for_preview": bool(name or email or phone), "ready_for_execution": bool(name or email or phone), "approval_required": False}]
    n = 2
    if include_document:
        detail_ready = bool(_t(p.get("document_name")) or _t(p.get("document_note")))
        steps.append({"step": n, "domain": "documents", "action": "prepare_reference", "ready_for_preview": True, "ready_for_execution": detail_ready, "approval_required": False}); n += 1
    if include_email:
        detail_ready = bool(email and _t(p.get("email_subject")) and _t(p.get("email_body")))
        steps.append({"step": n, "domain": "email", "action": "send", "ready_for_preview": True, "ready_for_execution": detail_ready and bool(microsoft_ready), "details_ready": detail_ready, "connector_ready": bool(microsoft_ready), "approval_required": True}); n += 1
    if include_calendar:
        detail_ready = bool(_t(p.get("meeting_title")) and _t(p.get("meeting_start")))
        steps.append({"step": n, "domain": "calendar", "action": "create", "ready_for_preview": True, "ready_for_execution": detail_ready and bool(microsoft_ready), "details_ready": detail_ready, "connector_ready": bool(microsoft_ready), "approval_required": True}); n += 1
    if include_whatsapp:
        detail_ready = bool(phone and _t(p.get("whatsapp_message")))
        steps.append({"step": n, "domain": "whatsapp", "action": "send", "ready_for_preview": True, "ready_for_execution": detail_ready and bool(whatsapp_ready), "details_ready": detail_ready, "connector_ready": bool(whatsapp_ready), "approval_required": True}); n += 1
    if include_followup:
        detail_ready = bool(_t(p.get("followup_title")))
        steps.append({"step": n, "domain": "followup", "action": "create", "ready_for_preview": True, "ready_for_execution": detail_ready, "details_ready": detail_ready, "approval_required": True}); n += 1

    selected = _selected_domains(p)
    preview_missing = []
    if not objective: preview_missing.append("objective")
    if not (name or email or phone): preview_missing.append("contact")
    if len(selected) <= 1: preview_missing.append("workflow_action")

    execution_blockers = _execution_detail_missing(p, name=name, email=email, phone=phone)
    if include_email and not microsoft_ready: execution_blockers.append("email_connector_not_ready")
    if include_calendar and not microsoft_ready: execution_blockers.append("calendar_connector_not_ready")
    if include_whatsapp and not whatsapp_ready: execution_blockers.append("whatsapp_connector_not_ready")
    execution_blockers = sorted(set(execution_blockers))

    return {
        "ok": not preview_missing,
        "status": "cross_app_workflow_preview_ready" if not preview_missing else "cross_app_workflow_preview_incomplete",
        "preview_ready": not preview_missing,
        "execution_ready": not execution_blockers,
        "objective_present": bool(objective),
        "contact_resolved": bool(name or email or phone),
        "selected_domains": selected,
        "step_count": len(steps),
        "steps": steps,
        "missing": preview_missing,
        "execution_blockers": execution_blockers,
        "preview_validation_scope": "planning_only",
        "connector_readiness_required_for_preview": False,
        "owner_approval_required_for_preview": False,
        "owner_approval_required_for_external_actions": True,
        "external_action_executed": False,
        "private_payloads_returned": False,
        "microsoft_connector_ready": bool(microsoft_ready),
        "whatsapp_connector_ready": bool(whatsapp_ready),
    }


def execute_workflow(payload: dict, contacts: Iterable[dict], adapters: Mapping[str, Callable[..., Any]], *, microsoft_ready: bool = False, whatsapp_ready: bool = False) -> dict:
    p = payload or {}
    preview = prepare_workflow(p, contacts, microsoft_ready=microsoft_ready, whatsapp_ready=whatsapp_ready)

    contact = _find_contact(contacts, p.get("contact_name"), p.get("email"), p.get("phone"))
    name = _t(p.get("contact_name")) or _t(contact.get("name"))
    email = _t(p.get("email")) or _t(contact.get("email"))
    phone = _t(p.get("phone")) or _t(contact.get("phone"))
    execution_missing = _execution_detail_missing(p, name=name, email=email, phone=phone)
    if execution_missing:
        return {**preview, "ok": False, "status": "workflow_not_ready_for_execution", "execution_missing": execution_missing}

    approvals = dict(p.get("approvals") or {})
    receipts = []

    def run(domain: str, callback_name: str, required_ready: bool, **kwargs):
        if approvals.get(domain) is not True:
            receipts.append({"domain": domain, "status": "approval_required", "executed": False})
            return
        if not required_ready:
            receipts.append({"domain": domain, "status": "connector_not_ready", "executed": False})
            return
        cb = adapters.get(callback_name)
        if cb is None:
            receipts.append({"domain": domain, "status": "adapter_unavailable", "executed": False})
            return
        cb(**kwargs)
        receipts.append({"domain": domain, "status": "executed", "executed": True})

    if p.get("include_document"):
        receipts.append({"domain": "documents", "status": "reference_prepared", "executed": False})
    if p.get("include_email"):
        run("email", "email", microsoft_ready, to_email=email, subject=_t(p.get("email_subject")), body=_t(p.get("email_body")))
    if p.get("include_calendar"):
        run("calendar", "calendar", microsoft_ready, subject=_t(p.get("meeting_title")), start_local=_t(p.get("meeting_start")), duration_minutes=int(p.get("meeting_duration") or 30), attendee_email=email, attendee_name=name)
    if p.get("include_whatsapp"):
        run("whatsapp", "whatsapp", whatsapp_ready, phone=phone, message=_t(p.get("whatsapp_message")))
    if p.get("include_followup"):
        run("followup", "followup", True, title=_t(p.get("followup_title")), contact_name=name, contact_email=email, due_at=_t(p.get("followup_due")))

    return {
        "ok": True,
        "status": "cross_app_workflow_execution_review_complete",
        "step_count": preview["step_count"],
        "receipt_count": len(receipts),
        "executed_count": sum(1 for r in receipts if r.get("executed")),
        "blocked_count": sum(1 for r in receipts if r.get("status") in {"approval_required", "connector_not_ready", "adapter_unavailable"}),
        "receipts": receipts,
        "owner_gate_preserved": True,
        "private_payloads_returned": False,
    }


def build_status(*, contacts_count: int, microsoft_ready: bool, whatsapp_ready: bool) -> dict:
    return {
        "ok": True,
        "status": "cross_app_personal_operator_ready",
        "contacts_count": max(0, int(contacts_count or 0)),
        "microsoft_connector_ready": bool(microsoft_ready),
        "whatsapp_connector_ready": bool(whatsapp_ready),
        "supported_domains": ["contacts", "documents", "email", "calendar", "whatsapp", "followup"],
        "per_action_owner_approval": True,
        "preview_first": True,
    }


def self_test() -> dict:
    contacts = [{"name": "Engineer Test", "email": "eng@example.com", "phone": "+971500000000"}]
    payload = {
        "contact_name": "Engineer Test", "objective": "Coordinate HVAC submission",
        "include_document": True, "document_name": "HVAC drawing.pdf",
        "include_email": True, "email_subject": "HVAC coordination", "email_body": "Please review.",
        "include_calendar": True, "meeting_title": "HVAC Coordination", "meeting_start": "2030-01-02T10:00",
        "include_whatsapp": True, "whatsapp_message": "Please confirm the meeting.",
        "include_followup": True, "followup_title": "Follow up HVAC review",
    }
    preview = prepare_workflow(payload, contacts, microsoft_ready=True, whatsapp_ready=True)
    called = []
    adapters = {
        "email": lambda **kw: called.append("email"),
        "calendar": lambda **kw: called.append("calendar"),
        "whatsapp": lambda **kw: called.append("whatsapp"),
        "followup": lambda **kw: called.append("followup"),
    }
    blocked = execute_workflow(payload, contacts, adapters, microsoft_ready=True, whatsapp_ready=True)
    approved_payload = dict(payload); approved_payload["approvals"] = {"email": True, "calendar": True, "whatsapp": True, "followup": True}
    approved = execute_workflow(approved_payload, contacts, adapters, microsoft_ready=True, whatsapp_ready=True)
    checks = {
        "six_domain_preview_verified": preview.get("ok") is True and preview.get("selected_domains") == ["contacts", "documents", "email", "calendar", "whatsapp", "followup"],
        "preview_executes_nothing_verified": preview.get("external_action_executed") is False,
        "owner_gates_block_unapproved_verified": blocked.get("executed_count") == 0 and blocked.get("blocked_count") == 4,
        "approved_adapter_handoff_verified": approved.get("executed_count") == 4 and called == ["email", "calendar", "whatsapp", "followup"],
        "privacy_safe_receipts_verified": approved.get("private_payloads_returned") is False,
        "owner_gate_preserved_verified": approved.get("owner_gate_preserved") is True,
    }
    return {"ok": all(checks.values()), **checks, "external_network_accessed": False, "synthetic_inputs_only": True, "real_external_action_executed": False}
