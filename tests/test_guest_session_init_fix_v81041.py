from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_guest_javascript_has_fixed_delivery_controller_and_load_guard():
    s=(ROOT/'templates/guest_voice_session.html').read_text(encoding='utf-8')
    assert "credentials:'same-origin'" in s
    assert "cache:'no-store'" in s
    assert 'Session check error' in s
    assert "return 'browser';" in s

def test_version_81041():
    s=(ROOT/'app.py').read_text(encoding='utf-8')
    assert 'VERSION = "v8.1.0.4.1"' in s
