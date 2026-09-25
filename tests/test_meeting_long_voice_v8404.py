from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT/'app.py').read_text(encoding='utf-8')
HTML = (ROOT/'templates'/'real_meeting_attendance.html').read_text(encoding='utf-8')

def test_version():
    assert 'VERSION = "v8.4.0.4"' in APP

def test_long_meeting_voice_is_chunked_and_fast_mode_on():
    assert 'id="meetingFastVoice" type="checkbox" checked' in HTML
    assert 'function splitMeetingSpeechChunks' in HTML
    assert 'maxChars=420' in HTML

def test_tts_chunk_has_bounded_wait_and_browser_fallback():
    assert "new AbortController()" in HTML
    assert "},12000);" in HTML
    assert "await browserSpeakMeetingText(part,locale,jobId)" in HTML

def test_real_answer_invokes_streaming_voice():
    convo = HTML.split('async function runInteractiveConversation',1)[1].split("document.getElementById('generateReport').onclick",1)[0]
    assert 'await speakAdamText(spoken,replyLocale)' in convo
    assert "Conversation: speaking in " in convo

def test_typed_query_awaits_representative_delivery():
    typed=HTML.split('async function sendTypedMeetingQuery()',1)[1].split('function setupRecognition',1)[0]
    assert "const handled=await handleFinalMeetingText(text,{finalTurn:true,source:'typed'})" in typed
    assert 'answered by Meeting Representative' in typed

def test_final_mic_turn_awaits_dispatch():
    assert 'if(options.finalTurn)return await dispatchCompletedParticipantTurn(q);' in HTML
    assert 'async function dispatchCompletedParticipantTurn(q)' in HTML
    assert 'return await triggerAutomaticConversation(combined);' in HTML

def test_barge_in_cancels_remaining_chunks():
    assert 'let meetingVoiceJobSeq=0;' in HTML
    barge=HTML.split('function stopAdamSpeechForBargeIn()',1)[1].split('function dedupeConsecutiveTranscriptLines',1)[0]
    assert 'meetingVoiceJobSeq++;' in barge

def test_meeting_panel_precedes_universal_visually():
    sync=HTML.split('function syncParticipant()',1)[1].split('function approved()',1)[0]
    assert "insertBefore(participant,universalPanel)" in sync

def test_authority_boundaries_unchanged():
    assert 'must NOT approve variations' in APP
    assert 'accept costs' in APP
    assert 'promise payment' in APP
    assert 'alter committed dates' in APP
    assert 'authorize purchases' in APP
