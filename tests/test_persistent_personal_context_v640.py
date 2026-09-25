from adam_core.persistent_personal_context import remember, recall, self_test

def test_v640_self_test_is_safe_and_persistent():
    r=self_test(); assert r['ok']; assert r['owner_approval_before_write_verified']; assert r['persistent_recall_verified']; assert r['sensitive_memory_rejection_verified']; assert not r['external_network_accessed']; assert not r['real_action_executed']

def test_v640_memory_requires_approval_and_recalls(tmp_path):
    p=tmp_path/'context.json'
    a=remember(p,'project_context','Payment','Follow up payment letter',False); assert a['status']=='approval_required'; assert not a['stored']
    b=remember(p,'project_context','Payment','Follow up payment letter',True); assert b['status']=='remembered'; assert b['stored']
    c=recall(p); assert c['count']==1; assert c['items'][0]['title']=='Payment'; assert c['execution_performed'] is False
