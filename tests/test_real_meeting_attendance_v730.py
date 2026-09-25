from pathlib import Path

from adam_core.real_meeting_attendance import build_attendance_status, process_attendance, self_test

ROOT = Path(__file__).resolve().parents[1]


def test_v730_routes_and_companion_ui_present():
    app = (ROOT / "app.py").read_text(encoding="utf-8")
    ui = (ROOT / "templates" / "real_meeting_attendance.html").read_text(encoding="utf-8")
    assert 'VERSION = "v8.1.0.1"' in app
    assert '/meeting-attendance' in app
    assert '/api/personal-assistant/real-meeting-attendance/status' in app
    assert '/api/personal-assistant/real-meeting-attendance/process' in app
    assert '/api/personal-assistant/real-meeting-attendance/self-test' in app
    assert 'SpeechRecognition||window.webkitSpeechRecognition' in ui
    assert 'Owner Approval' in ui
    assert 'does not falsely claim autonomous Teams/Zoom/Google Meet joining' in ui


def test_owner_gate_and_notes_processing_without_real_join():
    blocked = process_attendance({"platform":"zoom","mode":"take_notes","owner_approved":False,"segments":[{"text":"Action: send report"}]})
    assert blocked["status"] == "approval_required"
    ok = process_attendance({"platform":"zoom","mode":"take_notes","owner_approved":True,"segments":[{"text":"Status good"},{"text":"Action: send report"}]})
    assert ok["ok"] is True
    assert ok["action_item_count"] == 1
    assert ok["real_meeting_joined"] is False
    assert ok["external_network_accessed"] is False


def test_status_is_truthful_and_self_test_safe():
    status = build_attendance_status(platform_adapter_live=False)
    assert status["platform_join_available"] is False
    assert status["autonomous_platform_join_claimed"] is False
    assert status["owner_approval_required_before_capture"] is True
    r = self_test()
    assert r["ok"] is True
    assert r["platform_join_not_falsely_claimed_verified"] is True
    assert r["real_meeting_joined"] is False
    assert r["external_network_accessed"] is False
