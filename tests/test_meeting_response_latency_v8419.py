from pathlib import Path
import ast
import re

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / "app.py").read_text(encoding="utf-8")
HTML = (ROOT / "templates" / "real_meeting_attendance.html").read_text(encoding="utf-8")


def _load_fast_helper():
    tree = ast.parse(APP)
    node = next(
        n for n in tree.body
        if isinstance(n, ast.FunctionDef) and n.name == "_meeting_latency_fast_factual_turn"
    )
    module = ast.Module(body=[node], type_ignores=[])
    ast.fix_missing_locations(module)
    ns = {"re": re}
    exec(compile(module, str(ROOT / "app.py"), "exec"), ns, ns)
    return ns["_meeting_latency_fast_factual_turn"]


def test_version_bumped():
    assert 'VERSION = "v8.4.1.9"' in APP


def test_locked_end_of_turn_boundaries_are_preserved():
    # v8.4.1.6 owner-approved protection remains unchanged.
    assert "MEETING_END_OF_TURN_SILENCE_MS=4200" in HTML
    assert "MEETING_FINAL_TURN_MERGE_GRACE_MS=1500" in HTML
    assert "MEETING_CONTINUATION_SPEECH_HOLD_MS=900" in HTML


def test_adaptive_fast_end_of_turn_preserves_full_pause_guard():
    assert 'id="meetingFastResponse" type="checkbox" checked' in HTML
    assert "MEETING_FAST_END_OF_TURN_SILENCE_MS=2400" in HTML
    assert "MEETING_FAST_TURN_MAX_SPEECH_MS=6500" in HTML
    assert "MEETING_END_OF_TURN_SILENCE_MS=4200" in HTML
    assert "endOfTurnSilenceMs=(fastResponseEnabled&&spokenSpan>0&&spokenSpan<=MEETING_FAST_TURN_MAX_SPEECH_MS)?MEETING_FAST_END_OF_TURN_SILENCE_MS:MEETING_END_OF_TURN_SILENCE_MS" in HTML


def test_fast_post_stt_grace_is_only_for_complete_direct_questions():
    assert "MEETING_FINAL_TURN_FAST_COMPLETE_GRACE_MS=350" in HTML
    assert "function meetingTextLooksCompleteForFastReply" in HTML
    assert "!likelyDirectQuestion(t)" in HTML
    assert "fastComplete=finalBoundary&&meetingTextLooksCompleteForFastReply" in HTML
    assert "fastComplete?MEETING_FINAL_TURN_FAST_COMPLETE_GRACE_MS:MEETING_FINAL_TURN_MERGE_GRACE_MS" in HTML


def test_latency_diagnostics_cover_all_major_stages():
    assert 'id="meetingLatencyStatus"' in HTML
    for token in (
        "speechEndAt", "sttStartAt", "sttEndAt", "dispatchAt",
        "aiStartAt", "aiEndAt", "voiceStartAt", "providerMs",
    ):
        assert token in HTML
    for label in ("total to voice start", "end-turn", "STT", "focus/merge", "AI", "voice prep", "provider"):
        assert label in HTML


def test_short_factual_question_uses_fast_server_path():
    helper = _load_fast_helper()
    assert helper("Adam, what is the function of a balancing valve?", True, False, False, "question", "") is True
    assert helper("What is the purpose of an expansion tank?", True, False, False, "question", "") is True


def test_approval_and_change_questions_never_use_fast_server_path():
    helper = _load_fast_helper()
    assert helper("Can you approve us to proceed with the 100 mm chilled-water pipe?", True, False, False, "question", "") is False
    assert helper("Should we change the chilled-water pump?", True, False, False, "question", "") is False
    assert helper("What is the approved static pressure for this project?", True, False, False, "question", "") is False


def test_contextual_and_clarification_turns_keep_full_path():
    helper = _load_fast_helper()
    q = "What is the function of the balancing valve?"
    assert helper(q, True, True, False, "question", "") is False
    assert helper(q, True, False, True, "question", "") is False
    assert helper(q, True, False, False, "question", "risk intervention") is False


def test_fast_prompt_has_compact_budget_without_touching_provider_transport():
    assert "latency_fast_path = _meeting_latency_fast_factual_turn" in APP
    assert "meeting_max_tokens = 320 if latency_fast_path else 700" in APP
    assert "raw_answer = call_ai(prompt, reply_language, max_tokens=meeting_max_tokens, timeout=25).strip()" in APP
    assert "provider_elapsed_ms" in APP
    assert '"latency_fast_path": latency_fast_path' in APP
    assert '"meeting_max_tokens": meeting_max_tokens' in APP


def test_fast_prompt_preserves_owner_governance():
    fast_block = APP[APP.index('if latency_fast_path:'):APP.index('# v8.4.1.8 — deterministic decision-critical clarification gate')]
    assert "Never invent approvals" in fast_block
    assert "Never approve, authorize" in fast_block
    assert "Mohamad's behalf" in fast_block


def test_fast_voice_uses_short_chunks_and_starts_timing_on_actual_playback():
    assert "MEETING_FAST_VOICE_CHUNK_CHARS=140" in HTML
    assert "splitMeetingSpeechChunks(clean,MEETING_FAST_VOICE_CHUNK_CHARS)" in HTML
    assert "fast voice — preparing first short speech chunk" in HTML
    assert "playServerMeetingChunk(chunk,locale,jobId,i+1,voiceChunks.length)" in HTML
    assert "meetingLatencyTrace.voiceStartAt=Date.now()" in HTML


def test_chunked_voice_keeps_speaker_protection_until_final_chunk():
    assert "const finalChunk=Number(chunkIndex)>=Number(chunkCount);" in HTML
    assert "if(finalChunk)restartCleanMeetingCaptureAfterAdamSpeech();else meetingSpeakerOutputActive=true" in HTML
    assert "browserSpeakMeetingText(text,language,jobId=meetingVoiceJobSeq,finalChunk=true)" in HTML


def test_existing_reply_trace_contract_is_preserved():
    for label in (
        "speech accepted", "representative dispatch started", "waiting for AI provider",
        "AI response received", "spoken reply completed",
    ):
        assert label in HTML


def test_prior_clarification_and_session_isolation_guards_remain_present():
    assert "_meeting_material_change_clarification" in APP
    assert "approval_status_consistency_guard" in APP
    assert "meeting_session_closed" in APP
    assert "stale prior-meeting response ignored" in HTML
    assert "meetingSessionEpoch" in HTML
