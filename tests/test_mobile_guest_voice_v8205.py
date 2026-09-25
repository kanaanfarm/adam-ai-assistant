from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_version():
    assert 'VERSION = "v8.2.0.5"' in (ROOT/'app.py').read_text(encoding='utf-8')

def test_visible_robust_tunnel_launcher():
    bat=(ROOT/'START_ADAM_ACQUISITION.bat').read_text(encoding='utf-8')
    ps=(ROOT/'START_GUEST_TUNNEL.ps1').read_text(encoding='utf-8')
    assert 'Adam Guest HTTPS Tunnel v8.2.0.5' in bat
    assert '/min powershell.exe' not in bat.split('Adam Guest HTTPS Tunnel')[1].splitlines()[0]
    assert 'curl.exe' in ps and 'Invoke-WebRequest' in ps
    assert 'guest_tunnel_status.json' in ps
    assert '127.0.0.1:8771/health' in ps
    assert 'MOBILE GUEST VOICE HTTPS READY' in ps

def test_owner_ui_reports_tunnel_error_and_waits_for_ready():
    html=(ROOT/'templates'/'guest_voice_owner.html').read_text(encoding='utf-8')
    assert "d.tunnel_state==='error'" in html
    assert 'Mobile HTTPS must show READY' in html

def test_public_access_exposes_status():
    app=(ROOT/'app.py').read_text(encoding='utf-8')
    assert 'guest_tunnel_status_v8205' in app
    assert '"tunnel_state"' in app and '"tunnel_message"' in app
