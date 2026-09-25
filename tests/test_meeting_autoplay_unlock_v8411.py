from pathlib import Path
HTML=Path('templates/real_meeting_attendance.html').read_text(encoding='utf-8')

def test_persistent_audio_context_playback_exists():
    assert 'playMeetingBlobWithUnlockedAudioContext' in HTML
    assert 'decodeAudioData' in HTML
    assert 'createBufferSource' in HTML

def test_real_answer_prefers_unlocked_context():
    block=HTML.split('async function speakAdamText',1)[1].split('async function runInteractiveConversation',1)[0]
    assert 'await playMeetingBlobWithUnlockedAudioContext(blob)' in block
    assert "new Audio(url)" in block
    assert 'SpeechSynthesisUtterance' in block

def test_user_gestures_prime_audio_context():
    assert "document.getElementById('start').onclick=async()=>{\n primeMeetingVoice();" in HTML
    assert "async function sendTypedMeetingQuery(){\n primeMeetingVoice();" in HTML
    assert "document.getElementById('testMeetingVoice').onclick=async()=>{primeMeetingVoice();" in HTML

def test_barge_in_stops_context_source():
    assert 'meetingAdamAudioContextSource.stop()' in HTML
