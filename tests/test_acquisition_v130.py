from adam_core.acquisition import acquisition_readiness, demo_scenarios


def runtime_ok():
    return {
        "runtime": {"data_dir_available": True, "ai_provider_configured": True, "microsoft_client_configured": False, "whatsapp_configured": False, "alpaca_paper_configured": False},
        "safety": {"owner_approval_model": True, "live_trading_blocked": True, "hardcoded_flask_secret": False},
    }


def governance_ok():
    return {
        "workflow_count": 2,
        "approval_events": 1,
        "completion_events": 1,
        "policy": {"execution_confirmation_required": True, "attachment_context_exposed": False, "credentials_exposed": False},
    }


def test_three_buyer_demo_scenarios():
    scenarios = demo_scenarios()
    assert len(scenarios) == 3
    assert all(x["approval_required"] for x in scenarios)


def test_readiness_core_checks_pass():
    out = acquisition_readiness(version="v1.3.0", governance=governance_ok(), runtime=runtime_ok(), record_sources={"orchestration_workflows": 1, "followups": 1})
    assert out["all_core_checks_pass"] is True
    assert out["version"] == "v1.3.0"


def test_readiness_is_privacy_safe():
    out = acquisition_readiness(version="v1.3.0", governance=governance_ok(), runtime=runtime_ok(), record_sources={})
    assert all(v is False for v in out["privacy"].values())
    raw = repr(out).lower()
    for forbidden in ("api_key", "phone_number", "message_body", "attachment_body", "private_memory_value"):
        assert forbidden not in raw


def test_failed_security_control_blocks_all_core_checks_pass():
    r = runtime_ok()
    r["safety"]["hardcoded_flask_secret"] = True
    out = acquisition_readiness(version="v1.3.0", governance=governance_ok(), runtime=r, record_sources={})
    assert out["all_core_checks_pass"] is False
