from adam_core.computer_use_agent import ComputerAction, ApprovalRequired, execute_action, synthetic_demo
from adam_core.computer_use_boundary import build_computer_use_manifest, computer_use_is_privacy_safe

def test_computer_use_owner_gate_and_synthetic_driver():
    called=[]
    driver=lambda a: called.append(a.kind)
    execute_action(ComputerAction("read","synthetic"), driver)
    try:
        execute_action(ComputerAction("submit","synthetic","value"), driver)
        assert False
    except ApprovalRequired: pass
    execute_action(ComputerAction("submit","synthetic","value"), driver, owner_approved=True)
    assert called == ["read","submit"]
    assert synthetic_demo()["ok"] is True

def test_computer_use_buyer_evidence_is_private():
    payload=build_computer_use_manifest("v4.1.0")
    assert computer_use_is_privacy_safe(payload)
    assert payload["computer_use_agent"]["capabilities"]["live_desktop_driver_enabled"] is False
