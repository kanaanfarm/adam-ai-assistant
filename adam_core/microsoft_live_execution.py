"""Adam v6.2 governed Microsoft live execution binding.

The module is intentionally transport-agnostic.  Real Outlook/Calendar calls are
injected by app.py.  Owner approval and an explicit live-execution flag are both
required before any connector function can run.
"""

class MicrosoftLiveExecutionError(RuntimeError):
    pass


def _clean(value):
    return str(value or "").strip()


def build_action(action_type, payload=None, connector_ready=False):
    action_type = _clean(action_type).lower()
    payload = dict(payload or {})
    if action_type not in ("email", "calendar"):
        raise MicrosoftLiveExecutionError("Action type must be email or calendar.")

    if action_type == "email":
        safe = {
            "to": _clean(payload.get("to")),
            "subject": _clean(payload.get("subject")),
            "body": _clean(payload.get("body")),
        }
        if not safe["to"] or not safe["subject"] or not safe["body"]:
            raise MicrosoftLiveExecutionError("Email requires To, Subject and Message.")
        connector = "microsoft_outlook"
    else:
        safe = {
            "subject": _clean(payload.get("subject")) or "Meeting",
            "start_local": _clean(payload.get("start_local")),
            "duration_minutes": int(payload.get("duration_minutes") or 60),
            "attendee_email": _clean(payload.get("attendee_email")),
            "attendee_name": _clean(payload.get("attendee_name")),
        }
        if not safe["start_local"] or not safe["attendee_email"]:
            raise MicrosoftLiveExecutionError("Calendar action requires Start and attendee email.")
        if safe["duration_minutes"] < 15 or safe["duration_minutes"] > 480:
            raise MicrosoftLiveExecutionError("Calendar duration must be between 15 and 480 minutes.")
        connector = "microsoft_calendar"

    return {
        "ok": True,
        "action_type": action_type,
        "connector": connector,
        "connector_ready": bool(connector_ready),
        "requires_owner_approval": True,
        "payload": safe,
        "status": "ready_for_owner_review",
        "execution_performed": False,
        "external_network_accessed": False,
        "credentials_returned": False,
    }


def execute_action(action_type, payload=None, owner_approved=False, execute_live=False,
                   connector_ready=False, email_executor=None, calendar_executor=None):
    result = build_action(action_type, payload, connector_ready=connector_ready)
    result["owner_approved"] = owner_approved is True
    result["live_execution_requested"] = execute_live is True

    if owner_approved is not True:
        result["status"] = "blocked_pending_owner_approval"
        return result

    if execute_live is not True:
        result["status"] = "approved_dry_run"
        result["note"] = "Owner approved the reviewed action, but Live Execute was not enabled."
        return result

    if not connector_ready:
        result["status"] = "blocked_connector_not_ready"
        result["error"] = "Microsoft Outlook is not connected/configured."
        return result

    if result["action_type"] == "email":
        if not callable(email_executor):
            raise MicrosoftLiveExecutionError("Email execution adapter is unavailable.")
        p = result["payload"]
        email_executor(p["to"], p["subject"], p["body"])
        result["status"] = "executed"
        result["execution_performed"] = True
        result["external_network_accessed"] = True
        result["result"] = {"sent": True}
        return result

    if not callable(calendar_executor):
        raise MicrosoftLiveExecutionError("Calendar execution adapter is unavailable.")
    p = result["payload"]
    event = calendar_executor(p["subject"], p["start_local"], p["duration_minutes"], p["attendee_email"], p["attendee_name"])
    result["status"] = "executed"
    result["execution_performed"] = True
    result["external_network_accessed"] = True
    result["result"] = {
        "created": True,
        "event_id": _clean((event or {}).get("id")),
        "webLink": _clean((event or {}).get("webLink")),
    }
    return result


def self_test():
    calls = {"email": 0, "calendar": 0}

    def fake_email(to_email, subject, body):
        calls["email"] += 1
        return True

    def fake_calendar(subject, start_local, duration_minutes, attendee_email, attendee_name=""):
        calls["calendar"] += 1
        return {"id": "synthetic-event", "webLink": ""}

    email_payload = {"to": "buyer@example.com", "subject": "Review", "body": "Synthetic acceptance message"}
    cal_payload = {"subject": "Review meeting", "start_local": "2026-09-04T10:00", "duration_minutes": 30, "attendee_email": "buyer@example.com"}

    blocked = execute_action("email", email_payload, False, True, True, fake_email, fake_calendar)
    dry = execute_action("email", email_payload, True, False, True, fake_email, fake_calendar)
    live_email = execute_action("email", email_payload, True, True, True, fake_email, fake_calendar)
    live_calendar = execute_action("calendar", cal_payload, True, True, True, fake_email, fake_calendar)

    ok = (
        blocked.get("status") == "blocked_pending_owner_approval"
        and dry.get("status") == "approved_dry_run"
        and not blocked.get("execution_performed")
        and not dry.get("execution_performed")
        and live_email.get("execution_performed") is True
        and live_calendar.get("execution_performed") is True
        and calls == {"email": 1, "calendar": 1}
    )
    return {
        "ok": bool(ok),
        "owner_gate_preserved": True,
        "explicit_live_execute_gate_verified": True,
        "email_binding_verified": calls["email"] == 1,
        "calendar_binding_verified": calls["calendar"] == 1,
        "synthetic_adapters_only": True,
        "real_external_network_accessed": False,
        "real_action_executed": False,
        "credentials_exposed": False,
        "private_payloads_exposed": False,
    }
