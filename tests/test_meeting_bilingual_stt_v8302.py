from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
APP=(ROOT/'app.py').read_text(encoding='utf-8')
HTML=(ROOT/'templates'/'real_meeting_attendance.html').read_text(encoding='utf-8')

def test_version(): assert 'VERSION = "v8.3.0.2"' in APP
def test_bilingual_server_endpoint(): assert '/api/personal-assistant/real-meeting-attendance/transcribe' in APP
def test_owner_gate_on_stt(): assert 'owner_approved' in APP[APP.find('def real_meeting_attendance_transcribe_v8302'):APP.find('@app.route("/api/personal-assistant/real-meeting-attendance/self-test"')]
def test_code_switch_prompt(): assert 'code-switch freely' in APP and 'mechanical drawing' in APP and 'consultant' in APP
def test_auto_bilingual_prefers_mediarecorder(): assert "if(ml==='auto-bilingual')" in HTML and 'startBilingualServerListening' in HTML and 'MediaRecorder' in HTML
def test_ordered_chunk_queue(): assert 'meetingTranscriptionQueue=meetingTranscriptionQueue.then' in HTML
def test_browser_fallback_preserved(): assert 'SpeechRecognition||window.webkitSpeechRecognition' in HTML
def test_representative_boundaries_preserved(): assert 'must NOT approve variations' in APP and 'separate owner approval' in APP
