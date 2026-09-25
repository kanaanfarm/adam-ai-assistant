from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
APP=(ROOT/'app.py').read_text(encoding='utf-8')
HTML=(ROOT/'templates'/'real_meeting_attendance.html').read_text(encoding='utf-8')

def test_version():
    assert 'VERSION = "v8.4.1.0"' in APP

def test_speaker_protection_visible_on_by_default():
    assert 'id="meetingSpeakerProtection" type="checkbox" checked' in HTML
    assert 'Laptop speaker protection' in HTML

def test_vad_does_not_treat_adam_speaker_as_participant():
    assert 'meetingSpeakerProtectionEnabled()&&meetingSpeakerOutputActive' in HTML
    assert 'meetingRecorderContainsAdamAudio=true' in HTML
    assert 'meetingUtteranceSpeechStarted=false' in HTML

def test_contaminated_recorder_chunk_is_not_transcribed():
    assert 'const hadSpeech=(!meetingRecorderContainsAdamAudio)&&' in HTML
    assert "meetingRecorderStopReason='adam_speaker_guard'" in HTML

def test_browser_recognition_has_same_speaker_guard():
    assert "Adam speaker echo protected" in HTML

def test_real_playback_marks_speaker_start_and_end():
    assert 'markAdamSpeakerPlaybackStart();speakerStarted=true' in HTML
    assert 'restartCleanMeetingCaptureAfterAdamSpeech();' in HTML

def test_voice_chunks_are_shorter_for_fast_start():
    assert 'function splitMeetingSpeechChunks(text,maxChars=180)' in HTML

def test_typed_status_only_claims_voice_when_completed():
    assert 'meetingLastVoiceDeliveryOk?' in HTML
    assert 'voice playback did not complete' in HTML

def test_owner_boundaries_preserved():
    assert 'must NOT approve variations' in APP
    assert 'accept costs' in APP
    assert 'promise payment' in APP
    assert 'alter committed dates' in APP
    assert 'authorize purchases' in APP
