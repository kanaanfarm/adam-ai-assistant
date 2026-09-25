from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / 'templates' / 'real_meeting_attendance.html').read_text(encoding='utf-8')
APP = (ROOT / 'app.py').read_text(encoding='utf-8')

def test_universal_panel_present():
    assert 'Adam — Universal AI Assistant' in HTML
    assert 'universalTaskFocus' in HTML
    assert 'universalInput' in HTML
    assert 'universalVoice' in HTML
    assert 'universalNewTask' in HTML

def test_universal_uses_normal_chat_and_task_isolation():
    assert "fetch('/api/chat'" in HTML
    assert 'isolate_task:true' in HTML
    assert 'task_focus:focus' in HTML
    assert 'UNIVERSAL PERSONAL ASSISTANT MODE' in APP
    assert 'Do not import facts, assumptions, decisions, or technical details from an older unrelated subject.' in APP

def test_meeting_focus_remains_separate():
    assert 'Universal Assistant is independent of Meeting Focus Lock' in HTML
    assert 'meetingFocusLock' in HTML
    assert 'project_mismatch_filtered' in HTML

def test_version():
    assert 'VERSION = "v8.3.4.0"' in APP
