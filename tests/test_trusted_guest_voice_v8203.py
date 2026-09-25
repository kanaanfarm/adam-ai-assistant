from pathlib import Path

def test_v8203_owner_http_and_trusted_guest_routing():
    app=Path('app.py').read_text(encoding='utf-8')
    owner=Path('templates/guest_voice_owner.html').read_text(encoding='utf-8')
    launcher=Path('START_ADAM_ACQUISITION.bat').read_text(encoding='utf-8')
    assert 'VERSION = "v8.2.0.3"' in app
    assert 'os.getenv("ADAM_LOCAL_HTTPS", "false")' in app
    assert 'ADAM_GUEST_PUBLIC_BASE_URL' in app
    assert 'trusted_guest_url' in app
    assert 'd.trusted_guest_url||d.lan_guest_url||d.guest_url' in owner
    assert 'set "ADAM_LOCAL_HTTPS=false"' in launcher
    assert 'http://127.0.0.1:8770' in launcher

def test_v8203_preserves_voice_and_intelligence():
    app=Path('app.py').read_text(encoding='utf-8')
    tpl=Path('templates/guest_voice_session.html').read_text(encoding='utf-8')
    assert 'complete_text_with_web_search' in app
    assert 'startFallbackRecording' in tpl
    assert 'transcribeRecordedAudio' in tpl
    assert 'voiceJobSeq' in tpl
    assert 'microphone_requires_https' in tpl
