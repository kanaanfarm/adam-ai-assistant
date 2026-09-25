from adam_core.daily_assistant_workflow import build_daily_plan, self_test

def test_daily_plan_owner_gate_and_privacy():
    r=build_daily_plan("Prepare an email and schedule a meeting")
    assert r["ok"] and r["owner_approval_required"]
    assert not r["execution_performed"] and not r["external_network_accessed"]
    assert not r["credentials_returned"] and not r["private_payloads_returned"]

def test_daily_plan_self_test():
    r=self_test(); assert r["ok"] and r["owner_gate_preserved"] and not r["real_action_executed"]
