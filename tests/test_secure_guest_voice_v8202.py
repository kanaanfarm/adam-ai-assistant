from pathlib import Path

def test_secure_guest_voice_upgrade():
    app=Path('app.py').read_text(encoding='utf-8')
    req=Path('requirements.txt').read_text(encoding='utf-8')
    tpl=Path('templates/guest_voice_session.html').read_text(encoding='utf-8')
    https=Path('adam_core/local_https.py').read_text(encoding='utf-8')
    assert 'VERSION = "v8.2.0.2"' in app
    assert 'ensure_local_https_certificate' in app
    assert 'ssl_context=ssl_context' in app
    assert 'cryptography>=' in req
    assert 'microphone_requires_https' in tpl
    assert 'x509.IPAddress(ip)' in https
    assert 'Adam Acquisition Local CA' in https
