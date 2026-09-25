from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / "app.py").read_text(encoding="utf-8")
HTML = (ROOT / "templates" / "real_meeting_attendance.html").read_text(encoding="utf-8")

def test_version_and_watchdog_present():
    assert 'VERSION = "v8.3.4.2"' in APP
    assert 'const MEETING_MAX_AUTOREPLY_WAIT_MS=6000;' in HTML
    assert 'meetingLastAcceptedTranscriptAt' in HTML

def test_reply_stability_uses_accepted_transcript_not_raw_vad():
    start = HTML.index('function scheduleAutomaticConversationAfterEndOfTurn(q){')
    end = HTML.index('function normalizeEchoText', start)
    block = HTML[start:end]
    assert 'acceptedQuietFor' in block
    assert 'meetingLastAcceptedTranscriptAt' in block
    assert 'recorderHasSpeech' not in block
    assert 'meetingLastParticipantSpeechAt' not in block

def test_meaningful_turn_has_bounded_reply_wait():
    assert 'waitedFor>=MEETING_MAX_AUTOREPLY_WAIT_MS' in HTML
    assert 'response watchdog — Adam is answering captured interaction' in HTML
    assert 'triggerAutomaticConversation(combined)' in HTML

def test_existing_conversation_and_safety_boundaries_preserved():
    assert 'function likelyMeetingCorrection' in HTML
    assert 'function likelyMeetingOrder' in HTML
    assert 'if(isWakeOnly(q)){armMeetingAddressHold' in HTML
    assert 'explicit other-project speech ignored' in HTML
    assert 'must NOT approve variations' in APP
