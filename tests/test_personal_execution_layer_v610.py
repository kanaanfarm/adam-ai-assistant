from adam_core.personal_execution_layer import prepare_actions, approve_preview, self_test

def test_self_test_safe():
    r=self_test(); assert r['ok']; assert r['owner_gate_preserved']; assert not r['real_action_executed']; assert not r['external_network_accessed']

def test_email_calendar_owner_gate():
    a=prepare_actions('Prepare email and schedule meeting', {'microsoft':True})
    assert [x['type'] for x in a['actions']] == ['email','calendar']
    blocked=approve_preview('Prepare email and schedule meeting', False, {'microsoft':True})
    assert blocked['status']=='approval_required' and not blocked['execution_performed']
    approved=approve_preview('Prepare email and schedule meeting', True, {'microsoft':True})
    assert approved['status']=='approved_for_governed_connector_execution' and not approved['execution_performed']
