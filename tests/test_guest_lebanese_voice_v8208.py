from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
APP=(ROOT/'app.py').read_text(encoding='utf-8')
TEMPLATE=(ROOT/'templates'/'guest_voice_session.html').read_text(encoding='utf-8')
def test_version(): assert 'VERSION = "v8.2.0.8"' in APP
def test_guest_lebanese_normalizer():
    assert 'Rewrite ONLY the wording of the following answer into natural everyday Lebanese Arabic' in APP
    assert 'Keep exactly the same facts, names, numbers, dates, links, caveats' in APP
def test_lebanese_tts_profile():
    assert 'native Beirut/Lebanese accent' in APP
    assert 'شو، بدّك،' in APP
def test_guest_ar_lb_persistence():
    assert "sessionLanguage='ar-LB'" in TEMPLATE
    assert "language_preference:sessionLanguage" in TEMPLATE
def test_tunnel_preserved():
    ps=(ROOT/'START_GUEST_TUNNEL.ps1').read_text(encoding='utf-8')
    assert 'trycloudflare' in ps and 'cloudflared' in ps
