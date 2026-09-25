from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / 'app.py').read_text(encoding='utf-8')
HTML = (ROOT / 'templates' / 'real_meeting_attendance.html').read_text(encoding='utf-8')


def test_version_bumped():
    assert 'VERSION = "v8.4.0.2"' in APP


def test_typed_meeting_query_is_visible_near_transcript():
    assert 'Typed meeting query / comment / order' in HTML
    assert 'id="meetingTextQuery"' in HTML
    assert 'id="sendMeetingTextQuery"' in HTML


def test_typed_query_enters_same_meeting_pipeline():
    assert "await handleFinalMeetingText(text,{finalTurn:true,source:'typed'})" in HTML
    assert "document.getElementById('sendMeetingTextQuery').onclick=sendTypedMeetingQuery" in HTML


def test_enter_key_sends_typed_meeting_query():
    assert "e.key==='Enter'" in HTML
    assert "sendTypedMeetingQuery()" in HTML


def test_existing_meeting_guards_remain_in_pipeline():
    assert 'const focus=await checkMeetingFocus(q,options);' in HTML
    assert "if(isWakeOnly(q)){armMeetingAddressHold" in HTML
    assert "if(isQuestionPreamble(q)){armMeetingAddressHold" in HTML
    assert "const representativeArmed=representativeMode && approved();" in HTML
    assert "likelyDirectQuestion(q)||conversationalInteraction" in HTML


def test_clear_and_end_reset_typed_query_ui():
    assert HTML.count("meetingTextQueryStatus')") >= 3
    assert "Typed meeting input: ready" in HTML
