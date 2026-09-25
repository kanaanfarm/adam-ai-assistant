from pathlib import Path
from adam_core.manual_trade_override import review_manual_override, self_test

def test_manual_override_self_test():
    r=self_test()
    assert r["ok"] is True
    assert r["force_buy_review_verified"] is True
    assert r["force_sell_review_verified"] is True
    assert r["owner_approval_gate_verified"] is True
    assert r["final_confirmation_gate_verified"] is True
    assert r["paper_trading_only_verified"] is True
    assert r["real_order_submitted"] is False

def test_manual_override_gates():
    assert review_manual_override("NVDA","buy",100)["status"] == "owner_approval_required"
    assert review_manual_override("NVDA","buy",100,owner_approved=True)["status"] == "final_confirmation_required"
    assert review_manual_override("NVDA","buy",100,owner_approved=True,final_confirmed=True)["ready_for_paper_order"] is True

def test_v7011_ui_and_routes():
    app=Path("app.py").read_text(encoding="utf-8")
    ui=Path("templates/stock.html").read_text(encoding="utf-8")
    assert 'VERSION = "v8.1.0.1"' in app
    assert '/api/personal-assistant/stock-manual-override/self-test' in app
    assert 'id="manualTradeOverride"' in ui
    assert 'FORCE BUY' in ui and 'FORCE SELL' in ui
    assert '/api/stock/order' in ui
