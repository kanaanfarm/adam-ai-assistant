from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / "app.py").read_text(encoding="utf-8")
HTML = (ROOT / "templates" / "real_meeting_attendance.html").read_text(encoding="utf-8")


def test_release_version_and_new_state_boundaries():
    assert ('VERSION = "v8.4.1.2"' in APP) or ('VERSION = "v8.4.1.3"' in APP)
    assert "_MEETING_ACCEPTED_TURNS = {}" in APP
    assert "_MEETING_AI_INFLIGHT = set()" in APP
    assert "accepted_turn_persisted_before_ai_dispatch" in APP


def test_accepted_focus_is_persisted_before_ai_dispatch():
    focus = APP.split('def meeting_conversation_focus_check_v8330():', 1)[1].split('@app.route("/api/personal-assistant/meeting-conversation/note"', 1)[0]
    assert "_meeting_transcript_trim(memory)" in focus
    assert "_meeting_accepted_turn_upsert(" in focus
    assert 'ai_status="accepted"' in focus
    assert '"accepted_turn_persisted": bool(result.get("accept"))' in focus
    assert focus.find("_meeting_accepted_turn_upsert(") < APP.find('def meeting_conversation_ask_v7411():')


def test_duplicate_completed_stt_is_suppressed_before_focus_and_server_side():
    handler = HTML.split('async function handleFinalMeetingText', 1)[1].split('async function sendTypedMeetingQuery', 1)[0]
    assert "meetingLastFocusCandidateText" in handler
    assert handler.find("meetingLastFocusCandidateText") < handler.find("await checkMeetingFocus")
    focus = APP.split('def meeting_conversation_focus_check_v8330():', 1)[1].split('@app.route("/api/personal-assistant/meeting-conversation/note"', 1)[0]
    assert "normalized_incoming" in focus
    assert "total_seconds() <= 12" in focus
    assert '"duplicate_focus_suppressed": True' in focus


def test_stable_question_id_crosses_focus_note_dispatch_and_pairing():
    handler = HTML.split('async function handleFinalMeetingText', 1)[1].split('async function sendTypedMeetingQuery', 1)[0]
    assert "proposedQuestionId" in handler
    assert "stableQuestionId" in handler
    assert "rememberMeetingUtterance(q,stableQuestionId)" in handler
    assert "dispatchCompletedParticipantTurn(q,stableQuestionId)" in handler
    assert "scheduleAutomaticConversationAfterEndOfTurn(q,stableQuestionId)" in handler
    assert '"single_pairing_id": question_id' in APP
    assert '"question_id": question_id' in APP


def test_provider_single_flight_and_completed_duplicate_guard():
    ask = APP.split('def meeting_conversation_ask_v7411():', 1)[1].split('@app.route("/api/personal-assistant/meeting-conversation/report"', 1)[0]
    assert "existing_coverage_state.startswith(\"Answered\")" in ask
    assert '"status": "duplicate_turn_completed"' in ask
    assert '"status": "duplicate_turn_in_progress"' in ask
    assert "_MEETING_AI_INFLIGHT_LOCK" in ask
    assert "_MEETING_AI_INFLIGHT.add(flight_key)" in ask
    assert "max_tokens=700, timeout=25" in ask
    assert '"status": failure_status' in ask
    assert 'failure_status = "ai_provider_timeout"' in ask


def test_delayed_note_cannot_regress_completed_ai_state():
    helper = APP.split('def _meeting_accepted_turn_upsert', 1)[1].split('def _meeting_strip_wake_prefix', 1)[0]
    assert 'incoming_ai_status == "accepted"' in helper
    assert 'final_ai_statuses = {"answered", "clarification", "ignored"}' in helper
    assert '"provider_response_received"' in helper


def test_discussion_pair_is_idempotent_by_question_id():
    ask = APP.split('def meeting_conversation_ask_v7411():', 1)[1].split('@app.route("/api/personal-assistant/meeting-conversation/report"', 1)[0]
    assert "existing_discussion = next" in ask
    assert 'str(x.get("question_id") or "") == question_id' in ask
    assert "existing_discussion.update(discussion_payload)" in ask
    assert "meetingDiscussionHistory.find" in HTML


def test_processing_state_is_reported_instead_of_false_zero():
    report = APP.split('def meeting_conversation_report_v8319():', 1)[1].split('@app.route("/api/personal-assistant/meeting-conversation/report.docx"', 1)[0]
    assert "coverage_processing" in report
    assert 'str(x.get("state") or "") == "Processing"' in report
    assert "focus_accepted = max" in report
    assert "len(accepted_turns)" in report
    assert '"processing_question_count": coverage_processing' in report
    assert "if coverage_processing:" in report
    assert "accepted direct question(s) are still Processing" in report


def test_visible_reply_trace_matches_failure_diagnostics():
    assert 'id="meetingReplyTrace"' in HTML
    assert "setMeetingReplyTrace(1,'speech accepted'" in HTML
    assert "setMeetingReplyTrace(2,'representative dispatch started'" in HTML
    assert "setMeetingReplyTrace(3,'waiting for AI provider'" in HTML
    assert "setMeetingReplyTrace(4,'AI response received'" in HTML
    assert "setMeetingReplyTrace(5,'spoken reply completed'" in HTML
    assert "AI provider timeout — question retained" in HTML


def test_reset_clears_new_ephemeral_state():
    reset = APP.split('def meeting_conversation_reset_v7412():', 1)[1]
    assert "_MEETING_ACCEPTED_TURNS.pop(sid, None)" in reset
    assert "_MEETING_AI_INFLIGHT.discard(key)" in reset


def test_governance_boundaries_preserved():
    assert "must NOT approve variations" in APP
    assert "consequential commitments" in APP.lower()
    assert '"external_action_executed": False' in APP
    assert "owner_gate_preserved" in APP
