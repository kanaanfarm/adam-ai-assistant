from pathlib import Path
from adam_core.workflow_persistence import WorkflowStore
from adam_core.workflow_persistence_boundary import build_workflow_persistence_manifest, workflow_persistence_is_privacy_safe, workflow_persistence_self_test

def test_manifest_privacy_and_hash():
    p=build_workflow_persistence_manifest('v2.7.0')
    assert workflow_persistence_is_privacy_safe(p)
    assert len(p['workflow_persistence_service_sha256'])==64
    assert p['workflow_persistence_service']['status']=='extracted_tested'

def test_self_test():
    r=workflow_persistence_self_test(); assert r['ok']; assert not r['workflow_values_returned_by_evidence']; assert not r['external_application_data_accessed']

def test_store_bounded_and_malformed(tmp_path):
    p=tmp_path/'w.json'; s=WorkflowStore(p,max_records=2); s.save([{'id':1},{'id':2},{'id':3}]); assert [x['id'] for x in s.load()]==[2,3]
    p.write_text('broken'); assert s.load()==[]

def test_app_routes_and_delegation():
    import pytest
    pytest.importorskip("flask")
    import app as m
    c=m.app.test_client()
    j=c.get('/api/acquisition/workflow-persistence-boundary').get_json(); assert j['ok'] and j['privacy_safe'] and j['version']=='v8.1.0'
    j=c.get('/api/acquisition/workflow-persistence-boundary/self-test').get_json(); assert j['ok']
    assert c.get('/api/acquisition/workflow-persistence-boundary/download').status_code==200
    assert isinstance(m.adam_workflows_load_v080(),list)
