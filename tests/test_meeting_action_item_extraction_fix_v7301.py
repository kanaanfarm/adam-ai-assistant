from pathlib import Path

from adam_core.meeting_agent import build_meeting_notes
from adam_core.real_meeting_attendance import process_attendance, action_item_fix_self_test

ROOT = Path(__file__).resolve().parents[1]


def test_v7301_recognizes_explicit_natural_action_sentence():
    result = process_attendance({
        "platform": "microsoft_teams",
        "mode": "take_notes",
        "owner_approved": True,
        "segments": [{"text": "Action: Mohamad will provide the latest HVAC shop drawing tomorrow."}],
    })
    assert result["ok"] is True
    assert result["action_item_count"] == 1
    assert result["action_items"] == ["Action: Mohamad will provide the latest HVAC shop drawing tomorrow."]


def test_v7301_recognizes_manual_imperative_notes_and_commitments():
    notes = build_meeting_notes([
        {"text": "provide latest shop drawing to check the HVAC"},
        {"text": "Mohamad will send the revised report tomorrow."},
        {"text": "Project status is on schedule."},
    ])
    assert notes["action_item_count"] == 2
    assert "provide latest shop drawing to check the HVAC" in notes["action_items"]
    assert "Mohamad will send the revised report tomorrow." in notes["action_items"]


def test_v7301_version_bumped_without_changing_meeting_join_boundary():
    app = (ROOT / "app.py").read_text(encoding="utf-8")
    assert 'VERSION = "v8.1.0.1"' in app
    assert 'build_attendance_status(platform_adapter_live=False)' in app


def test_v7301_fix_specific_self_test():
    result = action_item_fix_self_test()
    assert result["ok"] is True
    assert result["explicit_action_marker_verified"] is True
    assert result["manual_imperative_action_verified"] is True
    assert result["natural_commitment_verified"] is True
    assert result["external_network_accessed"] is False
    assert result["external_action_executed"] is False
