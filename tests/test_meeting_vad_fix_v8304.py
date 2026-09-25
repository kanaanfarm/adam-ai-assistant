from pathlib import Path
APP=Path('app.py').read_text(encoding='utf-8')
HTML=Path('templates/real_meeting_attendance.html').read_text(encoding='utf-8')

def test_version(): assert 'VERSION = "v8.3.0.4"' in APP

def test_vad_state_is_explicitly_initialized():
    assert 'let meetingChunkSpeechFrames=0; let meetingNoiseFloor=0.003;' in HTML
    assert 'let meetingAudioContext=null;' in HTML
    assert 'let meetingVadAvailable=false;' in HTML

def test_vad_adaptive_threshold_and_detection():
    assert 'Math.max(0.006,meetingNoiseFloor*2.2)' in HTML
    assert "meetingChunkSpeechFrames===2" in HTML
    assert 'speech detected' in HTML

def test_vad_unavailable_does_not_make_adam_deaf():
    assert 'const hadSpeech=!meetingVadAvailable||meetingChunkSpeechFrames>=2;' in HTML
    assert 'bilingual server transcription (VAD fallback)' in HTML

def test_hallucination_guard_preserved():
    assert 'prompt_leak_filtered' in APP
    assert 'glossary_echo_filtered' in APP
    assert 'implausible_chunk_filtered' in APP
    assert 'provider_data = {"model": "gpt-4o-transcribe", "temperature": "0"}' in APP

def test_owner_gate_preserved():
    block=APP[APP.find('def real_meeting_attendance_transcribe_v8304'):APP.find('@app.route("/api/personal-assistant/real-meeting-attendance/self-test"')]
    assert 'owner_approved' in block and 'approval_required' in block
