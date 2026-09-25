from adam_core.production_activation_gate import REQUIRED_GATES, validate_activation_candidate, activate_production_connector
from adam_core.production_activation_gate_boundary import build_production_activation_gate_manifest, production_activation_gate_is_privacy_safe, production_activation_gate_self_test


def test_activation_candidate_and_owner_gate():
    gates={k:True for k in REQUIRED_GATES}
    preview=validate_activation_candidate({"connector":"email","gates":gates})
    assert preview["activation_ready"] is True
    blocked=activate_production_connector(connector="email",gates=gates,owner_approved=False,activator=lambda c:{"ok":True})
    assert blocked["status"]=="approval_required"
    assert blocked["activator_called"] is False
    approved=activate_production_connector(connector="email",gates=gates,owner_approved=True,activator=lambda c:{"ok":True})
    assert approved["status"]=="production_activation_authorized"
    assert approved["production_activation_authorized"] is True
    assert approved["live_execution_enabled"] is False


def test_boundary_privacy_and_self_test():
    payload=build_production_activation_gate_manifest("v5.3.0")
    assert production_activation_gate_is_privacy_safe(payload) is True
    st=production_activation_gate_self_test()
    assert st["ok"] is True
    assert st["incomplete_activation_gates_blocked"] is True
    assert st["activation_blocked_without_owner_approval"] is True
    assert st["approved_activation_adapter_authorized"] is True
    assert st["live_execution_enabled"] is False
