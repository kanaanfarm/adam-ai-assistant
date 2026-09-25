from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / 'app.py').read_text(encoding='utf-8')
HTML = (ROOT / 'templates' / 'real_meeting_attendance.html').read_text(encoding='utf-8')


def test_version_bumped():
    assert 'VERSION = "v8.3.1.6"' in APP


def test_adam_reply_history_is_visible_and_clear_screen_does_not_delete_it():
    assert 'id="responseHistory"' in HTML
    assert 'Adam reply history — retained for this meeting' in HTML
    clear = HTML.split("document.getElementById('clear').onclick", 1)[1].split("document.getElementById('endMeeting').onclick", 1)[0]
    assert "responseDraft').value=''" not in clear
    assert "responseHistory').value=''" not in clear
    assert 'reply history' in clear.lower()


def test_end_meeting_resets_reply_history_and_clarification_state():
    end = HTML.split("document.getElementById('endMeeting').onclick", 1)[1].split("document.getElementById('analyze').onclick", 1)[0]
    assert "meetingResponseHistory=[]" in end
    assert "meetingAwaitingClarification=false" in end
    assert "responseHistory').value=''" in end
    assert '/api/personal-assistant/meeting-conversation/reset' in end


def test_speech_recognition_clarity_gate_requires_clarification_instead_of_guessing():
    assert 'IMPORTANT SPEECH-RECOGNITION CLARITY GATE' in APP
    assert 'DO NOT guess and DO NOT answer the uncertain subject' in APP
    assert 'CLARIFY:' in APP
    assert 'ANSWER:' in APP
    assert 'clarification_requested' in APP
    assert 'speech_recognition_clarity_guard' in APP


def test_clarification_followup_routes_without_repeating_wake_name():
    assert 'meetingAwaitingClarification' in HTML
    assert 'clarificationFollowup=representativeMode&&meetingAwaitingClarification' in HTML
    assert '||clarificationFollowup' in HTML
    assert 'clarification requested — listening for the participant to clarify' in HTML


def test_full_duplex_barge_in_and_question_queue_remain_enabled():
    assert 'meetingAdamSpeaking' in HTML
    assert 'stopAdamSpeechForBargeIn' in HTML
    assert 'meetingQuestionQueue' in HTML
    assert 'participant question captured — queued for Adam' in HTML
    assert 'rememberMeetingUtterance(q)' in HTML


def test_owner_consequential_boundaries_remain_locked():
    assert 'must NOT approve variations' in APP
    assert 'accept costs' in APP
    assert 'promise payment' in APP
    assert 'alter committed dates' in APP
    assert 'authorize purchases' in APP
    assert 'owner_gate_preserved' in APP
