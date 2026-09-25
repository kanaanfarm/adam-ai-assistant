from adam_core.voice_first_adam import build_voice_plan, self_test

def test_v650_self_test_is_privacy_safe():
    r=self_test(); assert r['ok']; assert r['multilingual_voice_identity_verified']; assert r['lebanese_arabic_profile_verified']; assert r['consequential_text_confirmation_gate_verified']; assert not r['real_action_executed']; assert not r['external_network_accessed']

def test_v650_consequential_voice_request_requires_text_confirmation():
    r=build_voice_plan('Send an email to the contractor requesting the latest payment letter.','en',True,False)
    assert r['status']=='text_confirmation_required'; assert r['owner_approved']; assert r['text_confirmation_required']; assert not r['text_confirmed']; assert not r['ready_for_execution_boundary']; assert not r['execution_performed']
