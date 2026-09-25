from adam_core.personal_assistant_readiness import CAPABILITIES, build_readiness, self_test

def test_dual_use_readiness_is_privacy_safe():
    r=build_readiness('v5.9.0', {name: True for name in CAPABILITIES})
    assert r['product_mode']=='dual_use_personal_and_commercial'
    assert r['personal_assistant_enabled'] is True
    assert r['commercial_presentation_supported'] is True
    assert r['owner_approval_preserved'] is True
    assert r['credentials_returned'] is False
    assert r['private_payloads_returned'] is False

def test_self_test_has_no_external_execution():
    r=self_test('v5.9.0')
    assert r['ok'] is True
    assert r['external_network_accessed'] is False
    assert r['owner_gate_preserved'] is True
