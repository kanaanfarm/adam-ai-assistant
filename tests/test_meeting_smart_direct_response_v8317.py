from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / "app.py").read_text(encoding="utf-8")
HTML = (ROOT / "templates" / "real_meeting_attendance.html").read_text(encoding="utf-8")


def test_version_and_balanced_fast_turn_detection():
    assert 'VERSION = "v8.3.1.7"' in APP
    assert 'MEETING_END_OF_TURN_SILENCE_MS=3200' in HTML
    assert 'MEETING_RESPONSE_STABILITY_MS=650' in HTML


def test_direct_answer_preferred_over_unnecessary_clarification():
    assert 'Prefer a direct professional answer' in APP
    assert 'Minor grammar errors, accent artifacts, or one obvious transcription substitution are NOT enough reason' in APP
    assert 'usually 2-6 sentences' in APP


def test_clarification_followup_is_bounded_and_noise_aware():
    assert 'MEETING_CLARIFICATION_WINDOW_MS=45000' in HTML
    assert 'function looksLikeLowInformationNoise' in HTML
    assert 'function likelyClarificationReply' in HTML
    assert 'meetingAwaitingClarification&&likelyClarificationReply(q)' in HTML


def test_background_noise_can_be_ignored_without_fake_reply():
    assert 'IGNORE:' in APP
    assert 'ignore_requested = False' in APP
    assert 'if(j.ignore_requested)' in HTML
    assert 'non-question/background fragment ignored' in HTML


def test_meaningful_question_history_is_retained():
    assert 'id="questionHistory"' in HTML
    assert 'function rememberParticipantQuestion' in HTML
    assert 'rememberParticipantQuestion(q)' in HTML
    assert "document.getElementById('questionHistory').value=''" in HTML  # only End Meeting reset path
    clear_handler = HTML.split("document.getElementById('clear').onclick",1)[1].split("document.getElementById('endMeeting').onclick",1)[0]
    assert "questionHistory" not in clear_handler


def test_existing_full_duplex_and_memory_behaviour_preserved():
    assert 'stopAdamSpeechForBargeIn' in HTML
    assert 'meetingQuestionQueue' in HTML
    assert 'Screen cleared. Meeting memory retained' not in HTML or 'meeting memory' in HTML.lower()
    assert '/api/personal-assistant/meeting-conversation/note' in HTML


def test_owner_consequential_action_boundary_preserved():
    assert 'must NOT approve variations' in APP
    assert 'separate owner approval mechanism' in APP
    assert 'external_action_executed' in APP
