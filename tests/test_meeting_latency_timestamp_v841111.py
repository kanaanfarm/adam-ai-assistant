from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / "app.py").read_text(encoding="utf-8")
HTML = (ROOT / "templates" / "real_meeting_attendance.html").read_text(encoding="utf-8")

def test_version_bumped():
    assert 'VERSION = "v8.4.1.11.1"' in APP

def test_speech_end_timestamp_freezes_after_stt_or_dispatch():
    needle = "if(!meetingLatencyTrace.sttStartAt&&!meetingLatencyTrace.aiStartAt&&!meetingAutoResponseBusy&&!meetingSpeakerOutputActive){meetingLatencyTrace.speechEndAt=now;}"
    assert needle in HTML

def test_total_latency_still_uses_voice_start_minus_participant_speech_end():
    assert "const total=(t.voiceStartAt&&t.speechEndAt)?t.voiceStartAt-t.speechEndAt:0;" in HTML

def test_voice_start_still_comes_from_actual_playback_start():
    assert "u.onstart=markStarted" in HTML
    assert "markAdamSpeakerPlaybackStart()" in HTML
