from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
APP=(ROOT/"app.py").read_text(encoding="utf-8")
TPL=(ROOT/"templates"/"real_meeting_attendance.html").read_text(encoding="utf-8")

def test_version():
    assert 'VERSION = "v8.3.0.5"' in APP

def test_canonical_mechanical_drawing_mapping_present():
    assert 'mechanical drawing' in APP
    assert 'ميكانيك' in APP and 'دروين' in APP

def test_common_project_terms_preserved():
    for term in ['shop drawing','RFI','HVAC','MEP','consultant','approved','revision','submission','contractor','variation']:
        assert term in APP

def test_no_transcription_prompt_reintroduced():
    start=APP.index('provider_data =')
    block=APP[start:APP.index('def clean_provider_text', start)]
    assert 'prompt' not in block.lower()

def test_vad_path_preserved():
    assert 'speech detected' in TPL
    assert 'meetingChunkSpeechFrames>=2' in TPL

def test_owner_gate_preserved():
    assert 'approval_required' in APP
    assert 'owner_gate_preserved' in APP
