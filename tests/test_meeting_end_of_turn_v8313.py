from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'templates'/'real_meeting_attendance.html').read_text(encoding='utf-8')
APP=(ROOT/'app.py').read_text(encoding='utf-8')

def test_version():
    assert 'VERSION = "v8.3.1.3"' in APP

def test_no_fixed_eight_second_cut_for_spoken_turn():
    assert 'MEETING_END_OF_TURN_SILENCE_MS=4000' in HTML
    assert 'MEETING_MAX_UTTERANCE_MS=60000' in HTML
    assert 'endOfTurn=' in HTML
    assert "},8000);" not in HTML

def test_silent_capture_stays_bounded():
    assert 'MEETING_SILENT_CHUNK_MS=8000' in HTML
    assert 'silentBound=' in HTML

def test_response_waits_for_stable_end_of_turn():
    assert 'scheduleAutomaticConversationAfterEndOfTurn' in HTML
    assert 'participant still speaking; Adam is waiting for the end of the turn' in HTML
    assert 'meetingLastParticipantSpeechAt=now' in HTML

def test_adjacent_partial_transcripts_are_combined():
    assert 'meetingPendingAutoParts.push(part)' in HTML
    assert "meetingPendingAutoParts.join(' ')" in HTML

def test_capture_duration_sent_to_server():
    assert "fd.append('capture_ms'" in HTML
    assert 'capture_ms = max(0, min(60000' in APP
    assert 'max_words = max(60, min(420' in APP

def test_representative_and_multilingual_controls_preserved():
    assert 'Owner Representative — Rehearsal' in HTML
    assert 'Auto — All languages' in HTML
    assert 'Professional representative — Adam / direct questions' in HTML
    assert 'Owner Approval — allow Adam to listen/capture and act as my disclosed AI representative for this meeting session' in HTML
