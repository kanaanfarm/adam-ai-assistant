from adam_core.browser_computer_operator import build_operator_plan, self_test

def test_v670_self_test():
    r=self_test(); assert r["ok"] is True; assert r["real_action_executed"] is False; assert r["external_network_accessed"] is False

def test_v670_owner_gate_and_handoff():
    blocked=build_operator_plan("Submit the synthetic coordination response", False)
    assert blocked["status"] == "owner_approval_required"
    assert blocked["ready_for_browser_boundary"] is False
    assert blocked["execution_performed"] is False
    approved=build_operator_plan("Submit the synthetic coordination response", True)
    assert approved["ready_for_browser_boundary"] is True
