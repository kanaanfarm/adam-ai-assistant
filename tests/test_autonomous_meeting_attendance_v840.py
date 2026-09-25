from datetime import datetime, timedelta, timezone
from pathlib import Path

from adam_core.autonomous_meeting_attendance import (
    CONSEQUENTIAL_KEYS,
    build_pre_meeting_brief,
    create_mission,
    evaluate_mission,
    get_mission,
    ingest_calendar_events,
    self_test,
    set_standing_policy,
)
from adam_core.microsoft_graph_transport import list_calendar_view


def test_v840_core_self_test():
    result = self_test()
    assert result["ok"] is True
    assert result["owner_preapproval_gate_verified"] is True
    assert result["consequential_authority_not_granted_verified"] is True
    assert result["platform_block_verified"] is True
    assert result["live_adapter_readiness_verified"] is True
    assert result["calendar_auto_discovery_verified"] is True
    assert result["real_meeting_joined"] is False


def test_v840_preapproval_does_not_grant_cost_or_variation_authority(tmp_path):
    path = tmp_path / "auto.json"
    start = datetime.now(timezone.utc) + timedelta(hours=1)
    result = create_mission(path, {
        "title": "Tower MEP Coordination",
        "project_reference": "Tower",
        "platform": "microsoft_teams",
        "meeting_ref": "https://teams.example/join",
        "start_at": start.isoformat(),
        "owner_preapproved": True,
        "authority": {key: True for key in CONSEQUENTIAL_KEYS},
    })
    assert result["ok"] is True
    mission = result["mission"]
    assert all(mission["authority"][key] is False for key in CONSEQUENTIAL_KEYS)
    assert mission["owner_preapproved"] is True
    assert mission["ai_identity"] == "Adam — AI Representative for Mohamad"


def test_v840_due_meeting_is_blocked_until_live_platform_adapter(tmp_path):
    path = tmp_path / "auto.json"
    start = datetime(2026, 9, 8, 12, 0, tzinfo=timezone.utc)
    result = create_mission(path, {
        "title": "MEP Coordination",
        "platform": "microsoft_teams",
        "meeting_ref": "https://teams.example/join",
        "start_at": start.isoformat(),
        "owner_preapproved": True,
    })
    mission = result["mission"]
    blocked = evaluate_mission(mission, now=start-timedelta(minutes=1), platform_adapter_live=False, ai_ready=True)
    ready = evaluate_mission(mission, now=start-timedelta(minutes=1), platform_adapter_live=True, ai_ready=True)
    assert blocked["status"] == "blocked_platform_adapter"
    assert ready["status"] == "ready_to_join"


def test_v840_standing_policy_can_autodiscover_only_after_owner_approval(tmp_path):
    path = tmp_path / "auto.json"
    denied = set_standing_policy(path, {"enabled": True, "owner_approved": False, "calendar_auto_discovery": True})
    assert denied["ok"] is False
    approved = set_standing_policy(path, {
        "enabled": True,
        "owner_approved": True,
        "calendar_auto_discovery": True,
        "allowed_project_keywords": ["Tower"],
    })
    assert approved["ok"] is True
    start = datetime.now(timezone.utc)+timedelta(hours=2)
    rows = [
        {"title":"Tower MEP","project_reference":"Tower","platform":"microsoft_teams","meeting_ref":"https://teams.example/a","start_at":start.isoformat()},
        {"title":"Marina MEP","project_reference":"Marina","platform":"microsoft_teams","meeting_ref":"https://teams.example/b","start_at":start.isoformat()},
    ]
    ingested = ingest_calendar_events(path, rows)
    assert ingested["created_count"] == 1
    assert ingested["created"][0]["project_reference"] == "Tower"


def test_v840_pre_meeting_brief_preserves_owner_boundary(tmp_path):
    path = tmp_path / "auto.json"
    start = datetime.now(timezone.utc)+timedelta(hours=1)
    result = create_mission(path, {
        "title": "Tower MEP Coordination", "project_reference": "Tower",
        "platform": "microsoft_teams", "meeting_ref": "https://teams.example/a",
        "start_at": start.isoformat(), "owner_preapproved": True,
        "owner_briefing": "Obtain the revised hydraulic calculation. Do not approve the variation.",
    })
    brief = build_pre_meeting_brief(result["mission"], recalled_context="Empower chilled-water correction retained.")
    assert "Adam — AI Representative for Mohamad" in brief
    assert "Do not approve the variation" in brief
    assert "approve variations" in brief
    assert "Empower chilled-water correction retained" in brief


def test_v840_graph_calendar_view_is_read_only_and_bounded():
    class Resp:
        ok = True
        status_code = 200
        text = "json"
        def json(self):
            return {"value":[{"id":"1","subject":"Meeting"}]}
    class Http:
        def __init__(self): self.calls=[]
        def get(self, url, **kwargs): self.calls.append((url, kwargs)); return Resp()
    http = Http()
    rows = list_calendar_view(lambda:"token", http, "2026-09-08T00:00:00Z", "2026-09-09T00:00:00Z", top=500)
    assert len(rows) == 1
    assert http.calls[0][0].endswith("/me/calendarView")
    assert http.calls[0][1]["params"]["$top"] == 100
    assert "Authorization" in http.calls[0][1]["headers"]


def test_v840_template_exposes_autonomous_controls():
    template = (Path(__file__).resolve().parents[1] / "templates" / "autonomous_meeting_attendance.html").read_text(encoding="utf-8")
    assert "Owner pre-approval" in template
    assert "Standing Calendar Attendance Policy" in template
    assert "Live Meeting Adapter" in template
    assert "Real unattended Teams/Zoom/Meet joining is still blocked" in template
