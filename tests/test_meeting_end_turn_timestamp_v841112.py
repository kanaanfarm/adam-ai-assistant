from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "templates" / "real_meeting_attendance.html").read_text(encoding="utf-8")
APP = (ROOT / "app.py").read_text(encoding="utf-8")


def test_version_bumped():
    assert 'VERSION = "v8.4.1.11.2"' in APP


def test_prior_completed_turn_starts_fresh_latency_trace():
    assert "const priorTurnComplete=!!(meetingLatencyTrace.voiceStartAt||meetingLatencyTrace.aiEndAt);" in HTML
    assert "const freshParticipantTurn=priorTurnComplete&&!meetingAutoResponseBusy&&!meetingSpeakerOutputActive&&!meetingAdamSpeaking;" in HTML
    assert "if(freshParticipantTurn||(!meetingAutoResponseBusy&&!meetingLatencyTrace.aiStartAt&&!meetingLatencyTrace.questionId))" in HTML


def test_fresh_trace_uses_current_speech_timestamp():
    expected="meetingLatencyTrace={speechEndAt:now,sttStartAt:0,sttEndAt:0,dispatchAt:0,aiStartAt:0,aiEndAt:0,voiceStartAt:0,questionId:'',providerMs:0,fastPath:false,endTurnMode:''};"
    assert expected in HTML


def test_v841111_freeze_remains():
    assert "if(!meetingLatencyTrace.sttStartAt&&!meetingLatencyTrace.aiStartAt&&!meetingAutoResponseBusy&&!meetingSpeakerOutputActive){meetingLatencyTrace.speechEndAt=now;}" in HTML


def test_fast_and_protected_boundaries_unchanged():
    assert "MEETING_END_OF_TURN_SILENCE_MS=4200" in HTML
    assert "MEETING_FAST_END_OF_TURN_SILENCE_MS=2400" in HTML


def test_no_provider_or_voice_transport_change_marker():
    assert "instant factual voice — starting device speech without server-TTS wait" in HTML
    assert "meetingLatencyTrace.aiStartAt=Date.now()" in HTML
