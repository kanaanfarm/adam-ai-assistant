from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / 'app.py').read_text(encoding='utf-8')
HTML = (ROOT / 'templates' / 'real_meeting_attendance.html').read_text(encoding='utf-8')


def test_version_bumped():
    assert 'VERSION = "v8.4.1.13.1"' in APP


def test_analyze_still_runs_attendance_processing_first():
    assert "document.getElementById('analyze').onclick=async()=>" in HTML
    assert "/api/personal-assistant/real-meeting-attendance/process" in HTML


def test_analyze_now_generates_professional_report():
    block = HTML.split("document.getElementById('analyze').onclick=async()=>",1)[1].split("function meetingFocusLocked",1)[0]
    assert "/api/personal-assistant/meeting-conversation/report" in block
    assert "reportBox.value=reportJson.report||''" in block


def test_analyze_passes_active_session_and_metadata():
    block = HTML.split("document.getElementById('analyze').onclick=async()=>",1)[1].split("function meetingFocusLocked",1)[0]
    assert "session_id:meetingConversationSessionId" in block
    assert "meeting_title:document.getElementById('meetingTitle').value" in block
    assert "project_reference:document.getElementById('projectReference').value" in block
    assert "participants:document.getElementById('meetingParticipants').value" in block
    assert "meeting_datetime:document.getElementById('meetingDateTime').value" in block


def test_analyze_surfaces_report_not_raw_attendance_json():
    block = HTML.split("document.getElementById('analyze').onclick=async()=>",1)[1].split("function meetingFocusLocked",1)[0]
    assert "JSON.stringify(await r.json(),null,2)" not in block
    assert "Meeting report ready from" in block


def test_report_is_brought_into_view():
    block = HTML.split("document.getElementById('analyze').onclick=async()=>",1)[1].split("function meetingFocusLocked",1)[0]
    assert "reportBox.scrollIntoView" in block


def test_action_attribution_fix_preserved():
    assert 'No participant-assigned actions were recorded.' in APP
    assert 'Recommended follow-up only — not a participant-assigned action.' in APP
    assert '"action_attribution_consistent": True' in APP


def test_fast_factual_reasoning_compatibility_preserved():
    assert 'meeting_reasoning_effort = "none" if latency_fast_path else "low"' in APP


def test_locked_end_turn_constants_preserved():
    assert 'MEETING_END_OF_TURN_SILENCE_MS=4200' in HTML
    assert 'MEETING_FAST_END_OF_TURN_SILENCE_MS=2400' in HTML
    assert 'MEETING_FAST_TURN_MAX_SPEECH_MS=12000' in HTML
