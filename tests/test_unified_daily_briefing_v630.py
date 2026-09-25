from adam_core.unified_daily_briefing import build_briefing, self_test


def test_v630_self_test_is_safe_and_complete():
    r = self_test()
    assert r['ok']
    assert r['five_briefing_sections_verified']
    assert r['read_only_boundary_verified']
    assert r['source_readiness_verified']
    assert r['owner_gate_not_required_for_read_only_briefing']
    assert not r['external_network_accessed']
    assert not r['real_action_executed']


def test_v630_briefing_combines_sections_without_execution():
    payload={
        'calendar':[{'time':'10:00','title':'Meeting','with':'Team'}],
        'priority_messages':[{'from':'Contractor','subject':'Letter','reason':'Reply'}],
        'followups':[{'title':'Follow up','due':'Today','contact':'Contractor'}],
        'documents':[{'name':'Letter','status':'Draft','next_action':'Review'}],
        'tasks':[{'title':'Reply','priority':'High','due':'Today'}],
    }
    r=build_briefing(payload, {'microsoft':False})
    assert r['status']=='briefing_ready'
    assert r['summary']['total_items']==5
    assert len(r['sections'])==5
    assert r['owner_approval_required'] is False
    assert r['execution_performed'] is False
    assert r['external_network_accessed'] is False
