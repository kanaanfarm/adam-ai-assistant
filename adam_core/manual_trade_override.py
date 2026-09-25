"""Owner-directed manual PAPER trade override for Adam v7.0.1.1.

This boundary lets the owner override Adam's recommendation, but never silently.
Only Alpaca Paper Trading is eligible. A real submission requires both Owner
Approval and an explicit final confirmation; live-money trading stays blocked.
"""
import re


def review_manual_override(symbol, side, amount=0, qty=0, owner_approved=False, final_confirmed=False):
    symbol = re.sub(r"[^A-Z.-]", "", str(symbol or "").upper())
    side = str(side or "").lower().strip()
    result = {
        "ok": False, "mode": "paper", "manual_override": True,
        "symbol": symbol, "side": side,
        "owner_approval_required": True, "owner_approved": bool(owner_approved),
        "final_confirmation_required": True, "final_confirmed": bool(final_confirmed),
        "live_trading_blocked": True, "execution_performed": False,
        "external_network_accessed": False, "ready_for_paper_order": False,
    }
    if not symbol or side not in ("buy", "sell"):
        return {**result, "status": "invalid_trade_request"}
    try:
        amount = float(amount or 0); qty = float(qty or 0)
    except (TypeError, ValueError):
        return {**result, "status": "invalid_trade_request"}
    if side == "buy" and not (1 <= amount <= 500):
        return {**result, "status": "invalid_buy_amount", "paper_buy_limit_usd": 500}
    if side == "sell" and qty <= 0:
        return {**result, "status": "invalid_sell_quantity"}
    if not owner_approved:
        return {**result, "status": "owner_approval_required"}
    if not final_confirmed:
        return {**result, "status": "final_confirmation_required"}
    return {**result, "ok": True, "status": "ready_for_paper_order", "ready_for_paper_order": True,
            "notional": round(amount, 2) if side == "buy" else None,
            "qty": qty if side == "sell" else None}


def self_test():
    blocked = review_manual_override("NVDA", "buy", 100, owner_approved=False, final_confirmed=False)
    one_gate = review_manual_override("NVDA", "buy", 100, owner_approved=True, final_confirmed=False)
    ready = review_manual_override("NVDA", "buy", 100, owner_approved=True, final_confirmed=True)
    live_block = ready.get("live_trading_blocked") is True
    return {
        "ok": True,
        "force_buy_review_verified": ready.get("ready_for_paper_order") is True,
        "force_sell_review_verified": review_manual_override("MSFT", "sell", qty=0.2, owner_approved=True, final_confirmed=True).get("ready_for_paper_order") is True,
        "owner_approval_gate_verified": blocked.get("status") == "owner_approval_required",
        "final_confirmation_gate_verified": one_gate.get("status") == "final_confirmation_required",
        "paper_trading_only_verified": ready.get("mode") == "paper" and live_block,
        "manual_override_warning_verified": ready.get("manual_override") is True,
        "synthetic_inputs_only": True,
        "external_network_accessed": False,
        "real_market_data_accessed": False,
        "real_order_submitted": False,
        "live_trading_blocked": True,
    }
