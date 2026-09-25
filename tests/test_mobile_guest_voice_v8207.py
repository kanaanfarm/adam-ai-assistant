from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_version():
    assert 'VERSION = "v8.2.0.7"' in (ROOT/'app.py').read_text(encoding='utf-8')

def test_cloudflared_is_not_piped_through_powershell_stderr():
    s=(ROOT/'START_GUEST_TUNNEL.ps1').read_text(encoding='utf-8')
    assert 'Start-Process -FilePath $exe' in s
    assert '-RedirectStandardError $stderrFile' in s
    assert '-RedirectStandardOutput $stdoutFile' in s
    assert '& $exe tunnel --url http://127.0.0.1:8771' not in s

def test_url_detection_and_status_preserved():
    s=(ROOT/'START_GUEST_TUNNEL.ps1').read_text(encoding='utf-8')
    assert 'trycloudflare\\.com' in s
    assert "Write-Status 'ready'" in s
    assert 'MOBILE GUEST VOICE HTTPS READY' in s

def test_gateway_health_boundary_preserved():
    s=(ROOT/'START_GUEST_TUNNEL.ps1').read_text(encoding='utf-8')
    assert 'http://127.0.0.1:8771/health' in s
    g=(ROOT/'guest_gateway.py').read_text(encoding='utf-8')
    assert 'port=8771' in g
