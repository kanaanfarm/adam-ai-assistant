from pathlib import Path
import ast
import re

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / "app.py").read_text(encoding="utf-8")
HTML = (ROOT / "templates" / "real_meeting_attendance.html").read_text(encoding="utf-8")


def _load_material_change_helper():
    tree = ast.parse(APP)
    node = next(
        n for n in tree.body
        if isinstance(n, ast.FunctionDef) and n.name == "_meeting_material_change_clarification"
    )
    module = ast.Module(body=[node], type_ignores=[])
    ast.fix_missing_locations(module)
    ns = {"re": re}
    exec(compile(module, str(ROOT / "app.py"), "exec"), ns, ns)
    return ns["_meeting_material_change_clarification"]


def test_version_bumped():
    assert 'VERSION = "v8.4.1.8"' in APP


def test_under_specified_pump_change_requires_clarification():
    gate = _load_material_change_helper()
    result = gate(
        "Adam, the contractor wants to change the chilled-water pump. Can they proceed?",
        True,
    )
    assert result["required"] is True
    assert result["reason"] == "material_pump_change_missing_decision_data"
    assert any("flow and head" in item for item in result["missing"])


def test_complete_pump_change_data_does_not_force_clarification():
    gate = _load_material_change_helper()
    result = gate(
        "Can they proceed with the replacement pump at 25 l/s and 180 kPa head per the approved pump schedule and proposed submittal?",
        True,
    )
    assert result["required"] is False
    assert result["reason"] == "decision_data_present"


def test_normal_pump_explanation_does_not_force_clarification():
    gate = _load_material_change_helper()
    result = gate("What is the function of a chilled-water pump?", True)
    assert result["required"] is False


def test_material_change_gate_runs_before_provider_and_routes_clarify():
    gate_pos = APP.index("material_change_clarity = _meeting_material_change_clarification")
    provider_pos = APP.index("raw_answer = call_ai(prompt, reply_language, max_tokens=700, timeout=25).strip()")
    assert gate_pos < provider_pos
    assert 'raw_answer = "CLARIFY:' in APP
    assert '"material_change_clarification_gate": forced_material_clarification' in APP
    assert "MATERIAL-CHANGE EXCEPTION" in APP


def test_clarification_reply_is_not_automatically_counted_as_direct_question():
    assert "const clarificationFollowup=meetingAwaitingClarification&&likelyClarificationReply(question);" in HTML
    assert "?options.directQuestion:likelyDirectQuestion(question);" in HTML
    assert "likelyDirectQuestion(question)||meetingAwaitingClarification" not in HTML
    assert "directQuestion||clarificationFollowup||turnKind==='correction'" in HTML


def test_clarification_followup_is_bound_to_parent_without_resolving_by_guess():
    assert "meetingClarificationQuestionId" in HTML
    assert "clarification_parent_question_id:meetingClarificationQuestionId" in HTML
    assert "CLARIFICATION FOLLOW-UP" in APP
    assert "do not treat the original decision question as resolved" in APP


def test_new_meeting_uses_client_session_epoch_and_stale_audio_guard():
    assert "let meetingConversationHistorySessionId=meetingConversationSessionId;let meetingSessionEpoch=1" in HTML
    assert "stale prior-meeting audio ignored" in HTML
    assert "sourceSessionId!==meetingConversationSessionId||sourceSessionEpoch!==meetingSessionEpoch" in HTML
    assert "recorderSessionId=meetingConversationSessionId" in HTML
    assert "recorderSessionEpoch=meetingSessionEpoch" in HTML


def test_late_ai_response_cannot_rebind_new_session():
    assert "const sessionIdAtDispatch=meetingConversationSessionId;const sessionEpochAtDispatch=meetingSessionEpoch;" in HTML
    assert "stale prior-meeting response ignored" in HTML
    assert "mismatched meeting-session response ignored" in HTML
    assert "session_id:sessionIdAtDispatch" in HTML


def test_end_meeting_waits_for_old_transcription_then_resets_and_rotates_session():
    end = HTML.split("document.getElementById('endMeeting').onclick", 1)[1].split("document.getElementById('analyze').onclick", 1)[0]
    assert "const closingSessionId=meetingConversationSessionId" in end
    assert "meetingSessionEpoch++" in end
    assert "await meetingTranscriptionQueue.catch(()=>{})" in end
    assert "session_id:closingSessionId" in end
    assert "meetingConversationHistorySessionId=meetingConversationSessionId" in end
    assert "Late audio/AI callbacks from it will be ignored" in end


def test_server_tombstones_closed_sessions_and_rejects_late_callbacks():
    assert "_MEETING_CLOSED_SESSIONS = {}" in APP
    assert "def _meeting_session_is_closed" in APP
    assert "_meeting_mark_session_closed(sid)" in APP
    assert APP.count('"status": "meeting_session_closed"') >= 3
    assert '"stale_callback_rejected": True' in APP


def test_client_history_recovery_cannot_cross_session_boundary():
    assert "client_history_session_id = str(body.get(\"client_history_session_id\") or \"\").strip()" in APP
    assert "client_history_session_id == session_id" in APP
    assert "client_history_session_id:meetingConversationHistorySessionId" in HTML


def test_existing_owner_governance_boundaries_remain_present():
    assert "must NOT approve variations" in APP
    assert "owner_gate_preserved" in APP
    assert "consequential_commitments_blocked" in APP
    assert "approval_status_consistency_guard" in APP
