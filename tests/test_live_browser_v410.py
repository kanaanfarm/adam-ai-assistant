from adam_core.live_browser_boundary import build_live_browser_manifest, live_browser_is_privacy_safe, live_browser_self_test
from adam_core.live_browser_driver import validate_url, LiveBrowserError

def test_manifest_privacy_and_gates():
    p=build_live_browser_manifest('v4.1.0')
    assert live_browser_is_privacy_safe(p)
    c=p['live_browser']['capabilities']
    assert c['owner_gate']['typing'] is True
    assert c['owner_gate']['button_or_submit_click'] is True
    assert c['bounds']['http_https_only'] is True

def test_self_test_no_network():
    r=live_browser_self_test()
    assert r['ok'] and r['unsafe_scheme_blocked']
    assert r['external_network_accessed'] is False
    assert r['real_application_controlled'] is False

def test_unsafe_url_blocked():
    try: validate_url('file:///etc/passwd')
    except LiveBrowserError: pass
    else: raise AssertionError('unsafe scheme accepted')
