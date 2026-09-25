"""Adam v8.4.0 — Autonomous Meeting Attendance orchestration.

This module prepares Adam to attend a pre-authorized meeting without the owner
being present at join time. It deliberately separates:

1) standing/pre-authorized attendance permission (join/listen/speak/take notes), and
2) consequential authority (cost, variation, contract, purchase, payment,
   committed schedule changes, external send/submit), which remains blocked.

The module is platform-neutral. A real Teams/Zoom/Meet join requires an injected,
configured live meeting-platform adapter. Until that adapter is actually live,
missions are prepared and monitored but never falsely reported as joined.
"""
from __future__ import annotations

import json
import os
import re
import threading
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

from .runtime import persistent_root

SCHEMA = 1
SUPPORTED_PLATFORMS = {"microsoft_teams", "zoom", "google_meet"}
SUPPORTED_STYLES = {"conservative", "balanced", "proactive"}
MISSION_STATUSES = {
    "scheduled", "preparing", "ready_to_join", "blocked_platform_adapter",
    "joining", "in_meeting", "completed", "cancelled", "missed", "error",
}
SAFE_DEFAULT_AUTHORITY = {
    "listen_and_transcribe": True,
    "answer_professional_questions": True,
    "ask_clarifying_questions": True,
    "record_actions_and_risks": True,
    "make_technical_recommendations": True,
    "approve_variations": False,
    "approve_costs_or_payments": False,
    "make_contractual_commitments": False,
    "make_purchases": False,
    "commit_schedule_dates": False,
    "send_external_messages_or_files": False,
}
CONSEQUENTIAL_KEYS = {
    "approve_variations", "approve_costs_or_payments", "make_contractual_commitments",
    "make_purchases", "commit_schedule_dates", "send_external_messages_or_files",
}
_LOCK = threading.RLock()


def autonomous_meeting_path(base_dir: Path) -> Path:
    root = persistent_root(Path(base_dir)) / "Adam_Acquisition"
    return root / "autonomous_meeting_attendance_v1.json"


def _clean(value: Any, limit: int = 1000) -> str:
    return re.sub(r"\s+", " ", str(value or "").strip())[:limit]


def _bool(value: Any) -> bool:
    return value is True


def _now(now: datetime | None = None) -> datetime:
    dt = now or datetime.now().astimezone()
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _parse_dt(value: Any) -> datetime | None:
    text = _clean(value, 80)
    if not text:
        return None
    try:
        dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.astimezone()
        return dt
    except Exception:
        return None


def _iso(dt: datetime | None) -> str:
    return dt.isoformat(timespec="seconds") if dt else ""


def _empty_state() -> dict:
    return {
        "schema": SCHEMA,
        "standing_policy": {
            "enabled": False,
            "owner_approved": False,
            "online_only": True,
            "default_style": "balanced",
            "join_early_minutes": 2,
            "prepare_early_minutes": 10,
            "calendar_auto_discovery": False,
            "allowed_project_keywords": [],
            "updated_at": "",
        },
        "missions": [],
        "worker": {
            "last_tick_at": "",
            "last_calendar_scan_at": "",
            "last_error": "",
        },
    }


def load_state(path: Path) -> dict:
    path = Path(path)
    with _LOCK:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                raise ValueError("invalid state")
        except Exception:
            data = _empty_state()
        base = _empty_state()
        base["standing_policy"].update(data.get("standing_policy") or {})
        base["worker"].update(data.get("worker") or {})
        missions = data.get("missions") or []
        base["missions"] = [m for m in missions if isinstance(m, dict)][-500:]
        return base


def save_state(path: Path, state: dict) -> None:
    path = Path(path)
    with _LOCK:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(tmp, path)


def sanitize_authority(raw: dict | None) -> dict:
    authority = dict(SAFE_DEFAULT_AUTHORITY)
    for key in authority:
        if key in (raw or {}):
            authority[key] = _bool((raw or {}).get(key))
    # Autonomous attendance never converts standing permission into consequential authority.
    for key in CONSEQUENTIAL_KEYS:
        authority[key] = False
    return authority


def _platform(value: Any) -> str:
    p = _clean(value, 40).lower()
    if p not in SUPPORTED_PLATFORMS:
        raise ValueError("Unsupported meeting platform.")
    return p


def _style(value: Any) -> str:
    s = _clean(value or "balanced", 30).lower()
    return s if s in SUPPORTED_STYLES else "balanced"


def _public_mission(mission: dict, *, include_join_ref: bool = True) -> dict:
    out = dict(mission)
    if not include_join_ref:
        out["meeting_ref"] = ""
        out["meeting_reference_present"] = bool(mission.get("meeting_ref"))
    return out


def create_mission(path: Path, raw: dict | None, *, source: str = "owner") -> dict:
    raw = raw or {}
    if raw.get("owner_preapproved") is not True:
        return {
            "ok": False,
            "status": "owner_preapproval_required",
            "mission_created": False,
            "consequential_authority_granted": False,
        }
    try:
        platform = _platform(raw.get("platform"))
    except ValueError as exc:
        return {"ok": False, "status": "unsupported_platform", "error": str(exc), "mission_created": False}

    title = _clean(raw.get("title"), 220)
    project = _clean(raw.get("project_reference"), 220)
    meeting_ref = _clean(raw.get("meeting_ref"), 2000)
    start = _parse_dt(raw.get("start_at"))
    if not title:
        return {"ok": False, "status": "meeting_title_required", "mission_created": False}
    if not meeting_ref:
        return {"ok": False, "status": "meeting_reference_required", "mission_created": False}
    if not start:
        return {"ok": False, "status": "meeting_start_required", "mission_created": False}

    duration = raw.get("duration_minutes", 60)
    try:
        duration = max(10, min(int(duration), 480))
    except Exception:
        duration = 60
    end = _parse_dt(raw.get("end_at")) or (start + timedelta(minutes=duration))
    if end <= start:
        end = start + timedelta(minutes=duration)

    now = _now()
    mission = {
        "id": "am-" + uuid.uuid4().hex[:12],
        "title": title,
        "project_reference": project,
        "platform": platform,
        "meeting_ref": meeting_ref,
        "start_at": _iso(start),
        "end_at": _iso(end),
        "participants": _clean(raw.get("participants"), 1000),
        "owner_briefing": _clean(raw.get("owner_briefing"), 5000),
        "participation_style": _style(raw.get("participation_style")),
        "owner_preapproved": True,
        "preapproval_scope": "join_listen_speak_notes_professional_discussion_only",
        "authority": sanitize_authority(raw.get("authority") if isinstance(raw.get("authority"), dict) else None),
        "status": "scheduled",
        "status_reason": "waiting_for_preparation_window",
        "brief_ready": False,
        "join_attempted": False,
        "real_meeting_joined": False,
        "owner_attention_required": False,
        "created_at": _iso(now),
        "updated_at": _iso(now),
        "source": _clean(source, 50),
        "last_error": "",
        "ai_identity": "Adam — AI Representative for Mohamad",
    }
    state = load_state(path)
    state["missions"].append(mission)
    state["missions"] = state["missions"][-500:]
    save_state(path, state)
    return {
        "ok": True,
        "status": "autonomous_meeting_mission_scheduled",
        "mission_created": True,
        "mission": _public_mission(mission),
        "owner_preapproval_preserved": True,
        "consequential_authority_granted": False,
    }


def list_missions(path: Path, *, include_completed: bool = True) -> list[dict]:
    missions = load_state(path)["missions"]
    if not include_completed:
        missions = [m for m in missions if m.get("status") not in {"completed", "cancelled", "missed"}]
    def key(m: dict):
        dt = _parse_dt(m.get("start_at"))
        return dt.timestamp() if dt else 0
    return [_public_mission(m) for m in sorted(missions, key=key)]


def get_mission(path: Path, mission_id: str) -> dict | None:
    mid = _clean(mission_id, 80)
    for m in load_state(path)["missions"]:
        if m.get("id") == mid:
            return _public_mission(m)
    return None


def update_mission(path: Path, mission_id: str, **changes: Any) -> dict | None:
    state = load_state(path)
    now = _now()
    found = None
    for m in state["missions"]:
        if m.get("id") == mission_id:
            for key, value in changes.items():
                if key in {"authority", "owner_preapproved", "preapproval_scope", "id", "created_at"}:
                    continue
                m[key] = value
            m["updated_at"] = _iso(now)
            found = m
            break
    if found:
        save_state(path, state)
        return _public_mission(found)
    return None


def cancel_mission(path: Path, mission_id: str) -> dict:
    mission = update_mission(path, mission_id, status="cancelled", status_reason="cancelled_by_owner")
    if not mission:
        return {"ok": False, "status": "mission_not_found"}
    return {"ok": True, "status": "mission_cancelled", "mission": mission}


def set_standing_policy(path: Path, raw: dict | None) -> dict:
    raw = raw or {}
    state = load_state(path)
    enabled = raw.get("enabled") is True
    if enabled and raw.get("owner_approved") is not True:
        return {
            "ok": False,
            "status": "owner_approval_required_for_standing_policy",
            "policy_updated": False,
        }
    policy = state["standing_policy"]
    policy.update({
        "enabled": enabled,
        "owner_approved": bool(enabled and raw.get("owner_approved") is True),
        "online_only": raw.get("online_only") is not False,
        "default_style": _style(raw.get("default_style")),
        "calendar_auto_discovery": bool(enabled and raw.get("calendar_auto_discovery") is True),
        "allowed_project_keywords": [
            _clean(x, 100) for x in (raw.get("allowed_project_keywords") or [])
            if _clean(x, 100)
        ][:30],
        "updated_at": _iso(_now()),
    })
    for key, lo, hi, default in (
        ("join_early_minutes", 0, 15, 2),
        ("prepare_early_minutes", 2, 60, 10),
    ):
        try:
            policy[key] = max(lo, min(int(raw.get(key, policy.get(key, default))), hi))
        except Exception:
            policy[key] = default
    state["standing_policy"] = policy
    save_state(path, state)
    return {
        "ok": True,
        "status": "standing_attendance_policy_updated",
        "policy_updated": True,
        "standing_policy": dict(policy),
        "consequential_authority_granted": False,
    }


def standing_policy(path: Path) -> dict:
    return dict(load_state(path)["standing_policy"])


def calendar_event_matches_policy(event: dict, policy: dict) -> bool:
    if not policy.get("enabled") or not policy.get("owner_approved") or not policy.get("calendar_auto_discovery"):
        return False
    join_ref = _clean(event.get("meeting_ref") or event.get("join_url"), 2000)
    if policy.get("online_only", True) and not join_ref:
        return False
    allowed = [str(x).lower() for x in policy.get("allowed_project_keywords") or [] if str(x).strip()]
    if allowed:
        hay = " ".join([
            _clean(event.get("title"), 300), _clean(event.get("project_reference"), 300),
            _clean(event.get("body_preview"), 1000), _clean(event.get("location"), 300),
        ]).lower()
        if not any(k in hay for k in allowed):
            return False
    return True


def ingest_calendar_events(path: Path, events: Iterable[dict]) -> dict:
    state = load_state(path)
    policy = state["standing_policy"]
    existing_refs = {str(m.get("meeting_ref") or "") for m in state["missions"]}
    created = []
    skipped = 0
    for event in list(events or [])[:100]:
        if not isinstance(event, dict) or not calendar_event_matches_policy(event, policy):
            skipped += 1
            continue
        ref = _clean(event.get("meeting_ref") or event.get("join_url"), 2000)
        if not ref or ref in existing_refs:
            skipped += 1
            continue
        result = create_mission(path, {
            "title": event.get("title") or "Calendar Meeting",
            "project_reference": event.get("project_reference") or "",
            "platform": event.get("platform") or "microsoft_teams",
            "meeting_ref": ref,
            "start_at": event.get("start_at"),
            "end_at": event.get("end_at"),
            "participants": event.get("participants") or "",
            "owner_briefing": event.get("owner_briefing") or "Auto-discovered from owner-approved calendar policy.",
            "participation_style": policy.get("default_style", "balanced"),
            "owner_preapproved": True,
        }, source="calendar_policy")
        if result.get("mission_created"):
            created.append(result["mission"])
            existing_refs.add(ref)
    return {
        "ok": True,
        "status": "calendar_events_processed",
        "created_count": len(created),
        "skipped_count": skipped,
        "created": created,
        "consequential_authority_granted": False,
    }


def build_pre_meeting_brief(mission: dict, *, recalled_context: str = "") -> str:
    title = _clean(mission.get("title"), 220)
    project = _clean(mission.get("project_reference"), 220)
    participants = _clean(mission.get("participants"), 1000)
    briefing = _clean(mission.get("owner_briefing"), 5000)
    context = _clean(recalled_context, 5000)
    style = _style(mission.get("participation_style"))
    authority = sanitize_authority(mission.get("authority") or {})
    blocked = [key.replace("_", " ") for key in CONSEQUENTIAL_KEYS if not authority.get(key)]
    return (
        f"Meeting: {title}\n"
        f"Project/reference: {project or '(not stated)'}\n"
        f"Participants: {participants or '(not stated)'}\n"
        f"Participation style: {style}\n"
        f"AI identity: Adam — AI Representative for Mohamad\n\n"
        f"Owner briefing:\n{briefing or '(none provided)'}\n\n"
        f"Relevant retained owner context:\n{context or '(none)'}\n\n"
        "Attendance authority: listen, understand, answer professional questions, ask clarifying questions, "
        "record actions/risks, and make technical recommendations.\n"
        "Fresh owner approval is still required for: " + ", ".join(sorted(blocked)) + ".\n"
        "Never imply Mohamad personally attended. Never claim an unrecorded approval."
    )


def _set_status(mission: dict, status: str, reason: str, now: datetime) -> None:
    if status not in MISSION_STATUSES:
        status = "error"
    mission["status"] = status
    mission["status_reason"] = reason
    mission["updated_at"] = _iso(now)


def evaluate_mission(mission: dict, *, now: datetime | None = None, platform_adapter_live: bool = False,
                     ai_ready: bool = True, prepare_early_minutes: int = 10,
                     join_early_minutes: int = 2) -> dict:
    now_dt = _now(now)
    start = _parse_dt(mission.get("start_at"))
    end = _parse_dt(mission.get("end_at"))
    if not start or not end:
        return {"status": "error", "reason": "invalid_meeting_time", "due": False}
    if mission.get("status") in {"cancelled", "completed"}:
        return {"status": mission.get("status"), "reason": mission.get("status_reason", ""), "due": False}
    if now_dt > end + timedelta(minutes=20) and not mission.get("real_meeting_joined"):
        return {"status": "missed", "reason": "meeting_window_passed_without_join", "due": False}
    prepare_at = start - timedelta(minutes=max(2, min(int(prepare_early_minutes), 60)))
    join_at = start - timedelta(minutes=max(0, min(int(join_early_minutes), 15)))
    if now_dt < prepare_at:
        return {"status": "scheduled", "reason": "waiting_for_preparation_window", "due": False}
    if now_dt < join_at:
        return {"status": "preparing", "reason": "pre_meeting_briefing_window", "due": False, "prepare": True}
    if not ai_ready:
        return {"status": "error", "reason": "ai_provider_not_ready", "due": True}
    if not platform_adapter_live:
        return {"status": "blocked_platform_adapter", "reason": "live_meeting_platform_adapter_not_configured", "due": True}
    return {"status": "ready_to_join", "reason": "preauthorized_and_join_window_open", "due": True, "ready_to_join": True}


def tick(path: Path, *, now: datetime | None = None, platform_adapter_live: bool = False,
         ai_ready: bool = True) -> dict:
    now_dt = _now(now)
    state = load_state(path)
    policy = state["standing_policy"]
    prep = int(policy.get("prepare_early_minutes", 10) or 10)
    join = int(policy.get("join_early_minutes", 2) or 2)
    changed = 0
    ready = []
    blocked = []
    preparing = []
    for mission in state["missions"]:
        decision = evaluate_mission(
            mission, now=now_dt, platform_adapter_live=platform_adapter_live,
            ai_ready=ai_ready, prepare_early_minutes=prep, join_early_minutes=join,
        )
        status = decision["status"]
        reason = decision["reason"]
        if mission.get("status") != status or mission.get("status_reason") != reason:
            _set_status(mission, status, reason, now_dt)
            changed += 1
        if status == "preparing":
            mission["brief_ready"] = True
            preparing.append(mission.get("id"))
        elif status == "ready_to_join":
            mission["brief_ready"] = True
            ready.append(mission.get("id"))
        elif status == "blocked_platform_adapter":
            mission["brief_ready"] = True
            blocked.append(mission.get("id"))
    state["worker"]["last_tick_at"] = _iso(now_dt)
    state["worker"]["last_error"] = ""
    save_state(path, state)
    return {
        "ok": True,
        "status": "autonomous_meeting_worker_tick_complete",
        "missions_changed": changed,
        "preparing_count": len(preparing),
        "ready_to_join_count": len(ready),
        "blocked_platform_adapter_count": len(blocked),
        "ready_mission_ids": ready,
        "blocked_mission_ids": blocked,
        "real_meeting_joined": False,
        "external_action_executed": False,
    }


def mark_join_started(path: Path, mission_id: str) -> dict:
    mission = get_mission(path, mission_id)
    if not mission:
        return {"ok": False, "status": "mission_not_found"}
    if not mission.get("owner_preapproved"):
        return {"ok": False, "status": "owner_preapproval_required", "join_started": False}
    updated = update_mission(path, mission_id, status="joining", status_reason="live_adapter_execution_started", join_attempted=True)
    return {"ok": True, "status": "joining", "mission": updated, "consequential_authority_granted": False}


def mark_join_result(path: Path, mission_id: str, *, joined: bool, error: str = "") -> dict:
    if joined:
        updated = update_mission(
            path, mission_id, status="in_meeting", status_reason="live_meeting_join_confirmed",
            real_meeting_joined=True, last_error="",
        )
        return {"ok": bool(updated), "status": "in_meeting" if updated else "mission_not_found", "mission": updated}
    updated = update_mission(
        path, mission_id, status="error", status_reason="live_meeting_join_failed",
        real_meeting_joined=False, last_error=_clean(error, 500),
    )
    return {"ok": False, "status": "live_meeting_join_failed", "mission": updated}


def complete_mission(path: Path, mission_id: str) -> dict:
    updated = update_mission(path, mission_id, status="completed", status_reason="meeting_completed")
    return {"ok": bool(updated), "status": "meeting_completed" if updated else "mission_not_found", "mission": updated}


def build_status(path: Path, *, calendar_connected: bool, platform_adapter_live: bool,
                 ai_ready: bool, worker_running: bool = False) -> dict:
    state = load_state(path)
    active = [m for m in state["missions"] if m.get("status") not in {"completed", "cancelled", "missed"}]
    blocked = [m for m in active if m.get("status") == "blocked_platform_adapter"]
    return {
        "ok": True,
        "status": "autonomous_meeting_attendance_prepared" if not platform_adapter_live else "autonomous_meeting_attendance_live_ready",
        "worker_running": bool(worker_running),
        "calendar_connected": bool(calendar_connected),
        "calendar_auto_discovery_enabled": bool(state["standing_policy"].get("calendar_auto_discovery")),
        "ai_provider_ready": bool(ai_ready),
        "live_meeting_platform_adapter_ready": bool(platform_adapter_live),
        "active_mission_count": len(active),
        "platform_blocked_mission_count": len(blocked),
        "owner_preapproval_supported": True,
        "standing_attendance_policy_supported": True,
        "pre_meeting_briefing_supported": True,
        "unattended_scheduler_supported": True,
        "autonomous_platform_join_claimed": bool(platform_adapter_live),
        "ai_identity_declared": True,
        "user_impersonation_allowed": False,
        "consequential_authority_granted_by_attendance_policy": False,
        "owner_approval_still_required_for_consequential_commitments": True,
        "worker": dict(state["worker"]),
        "standing_policy": dict(state["standing_policy"]),
    }


def self_test() -> dict:
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / "auto.json"
        start = datetime(2026, 9, 8, 10, 0, tzinfo=timezone.utc)
        no_approval = create_mission(path, {
            "title": "MEP Coordination", "platform": "microsoft_teams",
            "meeting_ref": "https://teams.example/test", "start_at": _iso(start),
            "owner_preapproved": False,
        })
        scheduled = create_mission(path, {
            "title": "MEP Coordination", "project_reference": "Tower",
            "platform": "microsoft_teams", "meeting_ref": "https://teams.example/test",
            "start_at": _iso(start), "owner_preapproved": True,
            "authority": {"approve_variations": True, "approve_costs_or_payments": True},
        })
        mission = scheduled.get("mission") or {}
        pre = evaluate_mission(mission, now=start-timedelta(minutes=5), platform_adapter_live=False, ai_ready=True)
        due_blocked = evaluate_mission(mission, now=start-timedelta(minutes=1), platform_adapter_live=False, ai_ready=True)
        due_ready = evaluate_mission(mission, now=start-timedelta(minutes=1), platform_adapter_live=True, ai_ready=True)
        policy_blocked = set_standing_policy(path, {"enabled": True, "owner_approved": False, "calendar_auto_discovery": True})
        policy_ok = set_standing_policy(path, {"enabled": True, "owner_approved": True, "calendar_auto_discovery": True})
        ingested = ingest_calendar_events(path, [{
            "title": "Tower MEP", "project_reference": "Tower", "platform": "microsoft_teams",
            "meeting_ref": "https://teams.example/auto", "start_at": _iso(start+timedelta(hours=1)),
        }])
        checks = {
            "owner_preapproval_gate_verified": no_approval.get("mission_created") is False,
            "mission_schedule_verified": scheduled.get("mission_created") is True,
            "consequential_authority_not_granted_verified": all(not mission.get("authority", {}).get(k) for k in CONSEQUENTIAL_KEYS),
            "preparation_window_verified": pre.get("status") == "preparing",
            "platform_block_verified": due_blocked.get("status") == "blocked_platform_adapter",
            "live_adapter_readiness_verified": due_ready.get("status") == "ready_to_join",
            "standing_policy_owner_gate_verified": policy_blocked.get("policy_updated") is False and policy_ok.get("policy_updated") is True,
            "calendar_auto_discovery_verified": ingested.get("created_count") == 1,
            "ai_identity_declared": mission.get("ai_identity") == "Adam — AI Representative for Mohamad",
            "external_network_accessed": False,
            "real_meeting_joined": False,
        }
        return {"ok": all([
            checks["owner_preapproval_gate_verified"], checks["mission_schedule_verified"],
            checks["consequential_authority_not_granted_verified"], checks["preparation_window_verified"],
            checks["platform_block_verified"], checks["live_adapter_readiness_verified"],
            checks["standing_policy_owner_gate_verified"], checks["calendar_auto_discovery_verified"],
            checks["ai_identity_declared"], not checks["external_network_accessed"], not checks["real_meeting_joined"],
        ]), **checks}
