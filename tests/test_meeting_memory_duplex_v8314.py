from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / 'app.py').read_text(encoding='utf-8')
HTML = (ROOT / 'templates' / 'real_meeting_attendance.html').read_text(encoding='utf-8')


def test_version_and_memory_survives_screen_clear():
    assert 'VERSION = "v8.3.1.4"' in APP
    assert '>Clear Screen</button>' in HTML
    clear = HTML.split("document.getElementById('clear').onclick", 1)[1].split("document.getElementById('endMeeting').onclick", 1)[0]
    assert 'meetingConversationHistory=[]' not in clear
    assert '/meeting-conversation/reset' not in clear
    assert 'Meeting memory retained' in clear


def test_explicit_end_meeting_resets_temporary_session_memory():
    end = HTML.split("document.getElementById('endMeeting').onclick", 1)[1].split("document.getElementById('analyze').onclick", 1)[0]
    assert '/api/personal-assistant/meeting-conversation/reset' in end
    assert 'meetingConversationHistory=[]' in end
    assert 'meetingConversationSessionId=' in end
    assert '_MEETING_TRANSCRIPT_MEMORY.pop(sid, None)' in APP


def test_ambient_transcript_is_kept_server_side():
    assert '_MEETING_TRANSCRIPT_MEMORY = {}' in APP
    assert '/api/personal-assistant/meeting-conversation/note' in HTML
    assert 'meeting_conversation_note_v8314' in APP
    assert 'effective_meeting_context' in APP
    assert 'retained_transcript_items' in APP


def test_end_of_turn_waits_for_full_turn_and_pending_transcriptions():
    assert 'MEETING_END_OF_TURN_SILENCE_MS=5000' in HTML
    assert 'MEETING_RESPONSE_STABILITY_MS=1800' in HTML
    assert 'meetingTranscriptionsPending>0' in HTML
    assert 'recorderHasSpeech' in HTML
    assert 'Adam is waiting for the participant to finish the full turn' in HTML


def test_adam_keeps_listening_and_handles_barge_in():
    assert 'echoCancellation:true' in HTML
    assert 'meetingAdamSpeaking' in HTML
    assert 'stopAdamSpeechForBargeIn' in HTML
    assert 'participant interruption captured' in HTML
    assert 'meetingQuestionQueue' in HTML
    assert 'participant question captured — queued for Adam' in HTML


def test_tts_waits_until_playback_finishes_before_next_answer():
    speak = HTML.split('async function speakAdamText', 1)[1].split('async function runInteractiveConversation', 1)[0]
    assert "meetingAdamAudio.onended=()=>finish('voice completed')" in speak
    assert 'return await new Promise' in speak
    assert 'meetingAdamSpeechResolve=finish' in speak


def test_owner_consequential_boundaries_remain_locked():
    assert 'must NOT approve variations' in APP
    assert 'accept costs' in APP
    assert 'promise payment' in APP
    assert 'alter committed dates' in APP
    assert 'authorize purchases' in APP
    assert 'owner_gate_preserved' in APP
