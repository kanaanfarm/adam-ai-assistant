from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
APP=(ROOT/'app.py').read_text(encoding='utf-8')
HTML=(ROOT/'templates'/'real_meeting_attendance.html').read_text(encoding='utf-8')

def test_version(): assert 'VERSION = "v8.3.0.3"' in APP
def test_long_prompt_removed_from_provider_data():
    block=APP[APP.find('def real_meeting_attendance_transcribe_v8303'):APP.find('@app.route("/api/personal-assistant/real-meeting-attendance/self-test"')]
    assert 'provider_data = {"model": "gpt-4o-transcribe", "temperature": "0"}' in block
    assert '"prompt": prompt' not in block
def test_prompt_leak_guard(): assert 'context: ###' in APP and 'prompt_leak_filtered' in APP
def test_implausible_chunk_guard(): assert 'len(words) > 60' in APP and 'implausible_chunk_filtered' in APP
def test_glossary_echo_guard(): assert 'glossary_hits >= 7' in APP
def test_client_voice_activity_gate(): assert 'meetingChunkSpeechFrames>=3' in HTML and 'waiting for speech' in HTML
def test_audio_rms_monitor(): assert 'Math.sqrt(sum/samples.length)' in HTML and 'meetingNoiseFloor*2.8' in HTML
def test_owner_gate_preserved(): assert 'owner_approved' in APP and 'Owner Approval — allow Adam to listen/capture this meeting' in HTML

