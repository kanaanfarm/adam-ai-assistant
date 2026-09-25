from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / 'app.py').read_text(encoding='utf-8')
HTML = (ROOT / 'templates' / 'real_meeting_attendance.html').read_text(encoding='utf-8')


def test_version_bumped():
    assert 'VERSION = "v8.3.1.5"' in APP


def test_recorder_marks_end_of_turn_and_passes_final_flag():
    assert "meetingRecorderStopReason='end_of_turn'" in HTML
    assert "transcribeMeetingBlob(blob,captureMs,finalTurn)" in HTML
    assert "handleFinalMeetingText(j.text,{finalTurn:!!finalTurn})" in HTML


def test_completed_turn_dispatch_bypasses_next_recorder_vad_wait():
    assert 'function dispatchCompletedParticipantTurn' in HTML
    assert "if(options.finalTurn)dispatchCompletedParticipantTurn(q)" in HTML
    dispatch = HTML.split('function dispatchCompletedParticipantTurn', 1)[1].split('function handleFinalMeetingText', 1)[0]
    assert 'triggerAutomaticConversation(combined)' in dispatch
    assert 'recorderHasSpeech' not in dispatch


def test_duplicate_transcript_is_filtered():
    assert 'dedupeConsecutiveTranscriptLines' in HTML
    assert 'meetingLastTranscriptText' in HTML
    assert 'duplicate completed turn ignored' in HTML


def test_clear_screen_preserves_memory_and_end_meeting_resets():
    clear = HTML.split("document.getElementById('clear').onclick", 1)[1].split("document.getElementById('endMeeting').onclick", 1)[0]
    assert 'meetingConversationHistory=[]' not in clear
    assert 'Meeting memory retained' in clear
    end = HTML.split("document.getElementById('endMeeting').onclick", 1)[1].split("document.getElementById('analyze').onclick", 1)[0]
    assert '/meeting-conversation/reset' in end
    assert 'meetingLastTranscriptText=' in end


def test_barge_in_and_queue_preserved():
    assert 'stopAdamSpeechForBargeIn' in HTML
    assert 'meetingQuestionQueue' in HTML
    assert 'participant interruption captured' in HTML


def test_owner_consequential_boundaries_preserved():
    assert 'must NOT approve variations' in APP
    assert 'accept costs' in APP
    assert 'promise payment' in APP
    assert 'alter committed dates' in APP
