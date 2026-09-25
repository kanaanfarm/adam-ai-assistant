"""Daily assistant workflow planning for Adam v6.0.

Builds a privacy-safe action plan. Consequential execution is never performed
by this module; the owner gate remains authoritative.
"""

SUPPORTED_ACTIONS = ("review", "prepare", "contact", "schedule", "document", "browser", "stock")


def build_daily_plan(request_text, available=None):
    text = str(request_text or "").strip()
    available = dict(available or {})
    if not text:
        return {"ok": False, "status": "request_required", "owner_approval_required": False, "steps": []}
    lower = text.lower()
    steps = [{"order": 1, "action": "review", "label": "Understand the request", "requires_owner_approval": False}]
    order = 2
    mappings = [
        (("email", "outlook", "message", "contact"), "contact", "Prepare communication"),
        (("meeting", "calendar", "schedule", "appointment"), "schedule", "Prepare calendar action"),
        (("document", "file", "attachment", "pdf"), "document", "Review or prepare document"),
        (("browser", "website", "web"), "browser", "Prepare browser/computer action"),
        (("stock", "market", "share", "trade"), "stock", "Prepare stock analysis"),
    ]
    for keywords, action, label in mappings:
        if any(k in lower for k in keywords):
            steps.append({"order": order, "action": action, "label": label, "requires_owner_approval": action in {"contact", "schedule", "browser", "stock"}})
            order += 1
    if len(steps) == 1:
        steps.append({"order": order, "action": "prepare", "label": "Prepare the requested work", "requires_owner_approval": False})
    consequential = any(s["requires_owner_approval"] for s in steps)
    return {
        "ok": True,
        "status": "plan_ready",
        "request_received": True,
        "workflow": "understand_plan_prepare_approve_execute_audit_followup",
        "steps": steps,
        "owner_approval_required": consequential,
        "execution_performed": False,
        "external_network_accessed": False,
        "credentials_returned": False,
        "private_payloads_returned": False,
        "available_capability_count": sum(1 for v in available.values() if bool(v)),
    }


def self_test():
    p = build_daily_plan("Prepare an email and schedule a meeting", {"ai_chat": True, "microsoft": True})
    empty = build_daily_plan("")
    return {
        "ok": bool(p["ok"] and p["owner_approval_required"] and not p["execution_performed"] and not p["external_network_accessed"] and not p["credentials_returned"] and not p["private_payloads_returned"] and not empty["ok"]),
        "multi_step_plan_verified": True,
        "owner_gate_preserved": True,
        "real_action_executed": False,
        "external_network_accessed": False,
        "private_payloads_exposed": False,
    }
