from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / 'app.py').read_text(encoding='utf-8')
HTML = (ROOT / 'templates' / 'real_meeting_attendance.html').read_text(encoding='utf-8')


def test_version_bumped():
    assert 'VERSION = "v8.4.0.3"' in APP


def test_meeting_auto_speak_is_visible_and_on_by_default():
    assert 'id="meetingAutoSpeak" type="checkbox" checked' in HTML
    assert "Speak Adam's meeting answers automatically" in HTML
    assert 'id="meetingVoiceStatus"' in HTML


def test_voice_is_primed_from_user_gestures():
    assert 'function primeMeetingVoice()' in HTML
    typed = HTML.split('async function sendTypedMeetingQuery()', 1)[1].split('function setupRecognition', 1)[0]
    assert 'primeMeetingVoice();' in typed
    start = HTML.split("document.getElementById('start').onclick=async()=>", 1)[1].split("document.getElementById('stop').onclick", 1)[0]
    assert 'primeMeetingVoice();' in start
    assert "document.getElementById('askAdam').onclick=()=>{primeMeetingVoice();" in HTML


def test_server_tts_has_browser_fallback_and_locale_binding():
    speak = HTML.split('async function speakAdamText', 1)[1].split('async function runInteractiveConversation', 1)[0]
    assert "fetch('/api/tts'" in speak
    assert 'browserSpeakMeetingText(text,locale)' in speak
    assert 'u.lang=String(language' in HTML
    assert 'preferredBrowserMeetingVoice' in HTML


def test_meeting_answer_still_invokes_voice_path():
    convo = HTML.split('async function runInteractiveConversation', 1)[1].split("document.getElementById('generateReport').onclick", 1)[0]
    assert 'await speakAdamText(spoken,replyLocale)' in convo
    assert "audio unavailable — use Test / Enable Meeting Voice" in convo


def test_test_voice_button_is_wired():
    assert 'id="testMeetingVoice"' in HTML
    assert "document.getElementById('testMeetingVoice').onclick=async()=>" in HTML
    assert 'Adam meeting voice is ready.' in HTML


def test_owner_consequential_boundaries_preserved():
    assert 'must NOT approve variations' in APP
    assert 'accept costs' in APP
    assert 'promise payment' in APP
    assert 'alter committed dates' in APP
    assert 'authorize purchases' in APP
