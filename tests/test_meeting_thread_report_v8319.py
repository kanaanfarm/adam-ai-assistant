from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
APP_SRC = (ROOT / 'app.py').read_text(encoding='utf-8')
HTML = (ROOT / 'templates' / 'real_meeting_attendance.html').read_text(encoding='utf-8')


def test_version_and_thread_policy_present():
    assert 'VERSION = "v8.3.1.9"' in APP_SRC
    assert 'IMMEDIATE THREAD PRIORITY' in APP_SRC
    assert 'followup_bound_to_immediate_thread' in APP_SRC


def test_followup_examples_are_bound_to_immediate_thread():
    assert '_meeting_is_contextual_followup' in APP_SRC
    assert 'the\\s+(?:client|contractor)\\s+(?:is\\s+)?asking\\s+why' in APP_SRC
    assert 'did\\s+you\\s+check' in APP_SRC


def test_paired_discussion_record_ui_present():
    assert 'id="discussionRecord"' in HTML
    assert 'function rememberDiscussionRecord' in HTML
    assert 'Participant: ' in HTML and 'Adam: ' in HTML
    assert 'followup_bound_to_immediate_thread' in HTML


def test_report_ui_and_endpoint_present():
    assert 'id="generateReport"' in HTML
    assert 'id="meetingReport"' in HTML
    assert 'Download Word-compatible Report' in HTML
    assert 'Print / Save PDF' in HTML
    assert '/api/personal-assistant/meeting-conversation/report' in APP_SRC
    assert 'PAIRED MEETING DISCUSSION RECORD' in APP_SRC


def test_clear_preserves_and_end_meeting_resets_record():
    clear_handler = HTML.split("document.getElementById('clear').onclick",1)[1].split("document.getElementById('endMeeting').onclick",1)[0]
    assert "discussionRecord').value=''" not in clear_handler
    end_handler = HTML.split("document.getElementById('endMeeting').onclick",1)[1].split("document.getElementById('analyze').onclick",1)[0]
    assert "discussionRecord').value=''" in end_handler
    assert '_MEETING_DISCUSSION_RECORDS.pop(sid, None)' in APP_SRC


def test_owner_boundaries_preserved():
    assert 'must NOT approve variations' in APP_SRC
    assert 'separate owner approval mechanism' in APP_SRC
    assert 'owner_gate_preserved' in APP_SRC
