from pathlib import Path

def test_v641_memory_ui_has_explicit_button_wiring_and_safe_ids():
    html = Path('templates/personal_context_memory.html').read_text(encoding='utf-8')
    assert 'id="rememberBtn"' in html
    assert 'id="recallBtn"' in html
    assert 'id="memoryValue"' in html
    assert "rememberBtn.addEventListener('click', rememberContext)" in html
    assert "recallBtn.addEventListener('click', recallContext)" in html
    assert "fetch('/api/personal-assistant/context-memory/remember'" in html
    assert "fetch('/api/personal-assistant/context-memory/recall?category='" in html
    assert 'ui_request_failed' in html
