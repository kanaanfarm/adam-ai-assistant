from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / 'app.py').read_text(encoding='utf-8')
HTML = (ROOT / 'templates' / 'real_meeting_attendance.html').read_text(encoding='utf-8')


def test_version_bumped():
    assert 'VERSION = "v8.4.1.11.1"' in APP


def test_instant_factual_voice_is_enabled_by_default():
    assert 'id="meetingInstantFactualVoice" type="checkbox" checked' in HTML
    assert 'Instant factual voice' in HTML


def test_instant_voice_is_narrowly_scoped_to_existing_fast_factual_path():
    assert "fastVoice&&instantFactualVoice&&meetingLatencyTrace.fastPath&&('speechSynthesis' in window)" in HTML
    assert "instant factual voice — starting device speech without server-TTS wait" in HTML


def test_fast_factual_voice_bypasses_server_tts_before_speaking():
    start = HTML.index("if(fastVoice&&instantFactualVoice&&meetingLatencyTrace.fastPath")
    end = HTML.index("const voiceChunks=", start)
    block = HTML[start:end]
    assert "await browserSpeakMeetingText(clean,locale,instantJobId,true)" in block
    assert "fetch('/api/tts'" not in block


def test_professional_server_tts_path_is_still_present():
    assert "playServerMeetingChunk(chunk,locale,jobId,i+1,voiceChunks.length)" in HTML
    assert "fetch('/api/tts'" in HTML
    assert "instant device voice unavailable — using professional server voice" in HTML


def test_browser_telemetry_marks_actual_speech_start():
    assert "u.onstart=markStarted" in HTML
    assert "startFallback=setTimeout" in HTML
    assert "meetingLatencyTrace.voiceStartAt=Date.now()" in HTML


def test_locked_end_turn_protection_is_unchanged():
    assert "MEETING_END_OF_TURN_SILENCE_MS=4200" in HTML
    assert "MEETING_FAST_END_OF_TURN_SILENCE_MS=2400" in HTML
    assert "MEETING_FAST_TURN_MAX_SPEECH_MS=12000" in HTML


def test_existing_clarification_and_approval_guards_remain():
    assert "_meeting_material_change_clarification" in APP
    assert "approval_status_consistency_guard" in APP
    assert "meeting_session_closed" in APP
