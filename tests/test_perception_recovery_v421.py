from pathlib import Path


def test_v421_has_deterministic_local_recovery_fixture():
    src = Path("app.py").read_text()
    assert 'VERSION = "v8.1.0.1"' in src
    assert '/computer-use-recovery-fixture' in src
    assert "id='current-link'" in src
    assert '>Learn more</a>' in src


def test_v421_browser_ui_defaults_to_local_fixture():
    html = Path("templates/computer_use_browser.html").read_text()
    assert '{{ recovery_fixture_url }}' in html
    assert 'v4.3:' in html
