from pathlib import Path

HTML = Path('templates/real_meeting_attendance.html').read_text(encoding='utf-8')

def test_simple_voice_uses_same_server_tts_pattern():
    assert "fetch('/api/tts'" in HTML
    assert "const audio=new Audio(url)" in HTML
    assert "audio.play()" in HTML

def test_simple_voice_browser_fallback_present():
    assert "new SpeechSynthesisUtterance(clean)" in HTML
    assert "speechSynthesis.speak(u)" in HTML

def test_meeting_reply_still_calls_voice_automatically():
    assert "const v=await speakAdamText(spoken,replyLocale);" in HTML

def test_voice_state_clears_after_playback():
    assert "meetingSpeakerOutputActive=false" in HTML
    assert "meetingRecorderContainsAdamAudio=false" in HTML
