from adam_core.microsoft_live_execution import execute_action, self_test


def test_v620_self_test_is_safe_and_complete():
    r = self_test()
    assert r['ok']
    assert r['owner_gate_preserved']
    assert r['explicit_live_execute_gate_verified']
    assert r['email_binding_verified']
    assert r['calendar_binding_verified']
    assert r['synthetic_adapters_only']
    assert not r['real_external_network_accessed']
    assert not r['real_action_executed']


def test_live_binding_requires_both_gates():
    calls=[]
    def send(to_email, subject, body): calls.append(('email',to_email)); return True
    p={'to':'test@example.com','subject':'Test','body':'Body'}
    a=execute_action('email',p,False,True,True,email_executor=send)
    b=execute_action('email',p,True,False,True,email_executor=send)
    c=execute_action('email',p,True,True,True,email_executor=send)
    assert a['status']=='blocked_pending_owner_approval'
    assert b['status']=='approved_dry_run'
    assert c['status']=='executed'
    assert calls==[('email','test@example.com')]
