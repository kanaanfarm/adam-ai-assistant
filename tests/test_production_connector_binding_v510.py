from adam_core.production_connector_binding import validate_binding_request,execute_bound_operation,public_manifest
from adam_core.production_connector_binding_boundary import build_production_connector_binding_manifest,production_connector_binding_is_privacy_safe,production_connector_binding_self_test

def test_binding_contract_and_owner_gate():
    assert validate_binding_request({'connector':'email','operation':'send'})['owner_approval_required'] is True
    blocked=execute_bound_operation(connector='email',operation='send',owner_approved=False,transport=lambda c,o:{'ok':True})
    assert blocked['status']=='approval_required' and blocked['transport_called'] is False
    called=[]
    ok=execute_bound_operation(connector='calendar',operation='invite',owner_approved=True,transport=lambda c,o: called.append((c,o)) or {'ok':True})
    assert ok['status']=='bound_operation_executed' and called

def test_boundary_privacy_and_self_test():
    m=build_production_connector_binding_manifest('v5.2.1')
    assert production_connector_binding_is_privacy_safe(m)
    assert public_manifest()['credentials_stored_by_adam_core'] is False
    st=production_connector_binding_self_test()
    assert st['ok'] and st['approved_injected_transport_executed'] and not st['external_network_accessed']
