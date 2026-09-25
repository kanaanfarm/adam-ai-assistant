from adam_core.cross_app_orchestrator import preview_plan, execute_plan
from adam_core.cross_app_execution_boundary import build_cross_app_execution_manifest, cross_app_execution_is_privacy_safe, cross_app_execution_self_test


def test_v430_manifest_and_privacy_boundary():
    payload = build_cross_app_execution_manifest("v4.3.0")
    assert cross_app_execution_is_privacy_safe(payload)
    caps = payload["cross_app_execution"]["capabilities"]
    assert caps["cross_app_execution"] is True
    assert caps["per_step_owner_approval"] is True
    assert caps["privacy"]["credentials_stored_in_orchestrator"] is False


def test_v430_preview_marks_only_consequential_unapproved_steps():
    p = preview_plan([
        {"connector":"documents","action":"read"},
        {"connector":"email","action":"draft"},
        {"connector":"email","action":"send"},
    ])
    assert p["approval_required_steps"] == [3]
    assert p["private_values_returned"] is False


def test_v430_execution_stops_exactly_at_owner_gate():
    calls=[]
    adapters={"documents":lambda s:calls.append((s.connector,s.action)) or True,
              "email":lambda s:calls.append((s.connector,s.action)) or True}
    r=execute_plan([
        {"connector":"documents","action":"read"},
        {"connector":"email","action":"draft"},
        {"connector":"email","action":"send","owner_approved":False},
    ], adapters)
    assert r["status"] == "approval_required"
    assert r["blocked_step"] == 3
    assert len(calls) == 2


def test_v430_self_test_no_network_or_real_apps():
    r=cross_app_execution_self_test()
    assert r["ok"] is True
    assert r["external_network_accessed"] is False
    assert r["real_application_controlled"] is False
    assert r["consequential_step_blocked_without_approval"] is True
    assert r["approved_consequential_step_executed"] is True
