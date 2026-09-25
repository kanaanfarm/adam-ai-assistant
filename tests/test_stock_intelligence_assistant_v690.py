from adam_core.stock_intelligence_assistant import build_stock_intelligence_plan, self_test

PRICES=[100,100.5,101,101.3,101.8,102,102.4,102.8,103.1,103.5,103.9,104.2,104.5,104.9,105.1,105.4,105.8,106,106.3,106.6,106.9,107.1,107.4,107.6,107.9]

def test_v690_self_test_is_safe_and_complete():
    r=self_test()
    assert r["ok"] is True
    assert r["indicator_analysis_verified"] is True
    assert r["portfolio_context_verified"] is True
    assert r["owner_approval_trade_handoff_gate_verified"] is True
    assert r["approved_paper_trade_review_handoff_verified"] is True
    assert r["live_trading_blocked_verified"] is True
    assert r["synthetic_inputs_only"] is True
    assert r["external_network_accessed"] is False
    assert r["real_order_submitted"] is False

def test_v690_trade_instruction_never_executes_without_owner_approval():
    r=build_stock_intelligence_plan("NVDA",PRICES,2,101,"Buy NVDA",False)
    assert r["status"] == "owner_approval_required_for_trade_handoff"
    assert r["owner_approval_required"] is True
    assert r["owner_approved"] is False
    assert r["ready_for_separate_paper_trade_review"] is False
    assert r["live_trading_blocked"] is True
    assert r["order_execution_available"] is False
    assert r["execution_performed"] is False
