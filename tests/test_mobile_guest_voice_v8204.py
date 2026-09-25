from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_version_and_dynamic_https_url():
    app=(ROOT/'app.py').read_text(encoding='utf-8')
    assert 'VERSION = "v8.2.0.4"' in app
    assert 'guest_public_base_url_v8204' in app
    assert 'guest_public_base_url.txt' in app
    assert '"mobile_voice_ready": bool(public_base)' in app

def test_guest_only_gateway_boundary():
    g=(ROOT/'guest_gateway.py').read_text(encoding='utf-8')
    assert 'port=8771' in g
    assert 'owner_ui_exposed' in g
    assert '@app.route("/api/tts"' in g
    assert 'X-Adam-Guest-Token' in g
    assert 'Not available on Guest Voice gateway' in g

def test_trusted_tunnel_launcher():
    ps=(ROOT/'START_GUEST_TUNNEL.ps1').read_text(encoding='utf-8')
    assert 'cloudflared-windows-amd64.exe' in ps
    assert 'trycloudflare' in ps
    assert 'guest_public_base_url.txt' in ps
    bat=(ROOT/'START_ADAM_ACQUISITION.bat').read_text(encoding='utf-8')
    assert 'guest_gateway.py' in bat
    assert 'START_GUEST_TUNNEL.ps1' in bat
    assert 'http://127.0.0.1:8770' in bat

def test_guest_page_sends_token_for_tts():
    html=(ROOT/'templates'/'guest_voice_session.html').read_text(encoding='utf-8')
    assert "'X-Adam-Guest-Token':token" in html
    assert 'microphone_requires_https' in html
    assert '/transcribe' in html


def test_owner_opens_trusted_url_and_shows_ready_state():
    html=(ROOT/'templates'/'guest_voice_owner.html').read_text(encoding='utf-8')
    assert "q('open').href=url" in html
    assert 'mobileHttpsStatus' in html
    assert '/guest-voice/public-access' in html
