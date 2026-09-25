from adam_core.whatsapp_production_integration import build_execution_plan, self_test

def test_v680_self_test_is_safe_and_complete():
    r=self_test()
    assert r["ok"] is True
    assert r["synthetic_inputs_only"] is True
    assert r["external_network_accessed"] is False
    assert r["real_whatsapp_sent"] is False
    assert r["owner_approval_gate_verified"] is True
    assert r["explicit_live_execute_gate_verified"] is True
    assert r["connector_readiness_gate_verified"] is True

def test_v680_owner_approval_blocks_safe_acceptance():
    r=build_execution_plan("+971500000000","Please confirm the coordination meeting.",False,False,True)
    assert r["status"] == "owner_approval_required"
    assert r["ready_for_whatsapp_transport"] is False
    assert r["execution_performed"] is False
