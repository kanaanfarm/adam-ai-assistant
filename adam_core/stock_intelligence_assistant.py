"""Governed Stock Intelligence Assistant for Adam Acquisition v6.9.0.

This layer performs deterministic, read-only market/portfolio reasoning from
supplied price data. It never submits an order. Any buy/sell instruction can
only become a handoff to Adam's existing separately governed PAPER-trading
boundary after Owner Approval. Live trading remains blocked.
"""
from __future__ import annotations

from math import isfinite

SENSITIVE_HINTS = ("password", "passwd", "api key", "api_key", "access token", "private key", "secret")
TRADE_HINTS = ("buy", "sell", "trade", "order", "purchase", "بيع", "شراء", "اشتري")


def _clean_symbol(value):
    symbol = "".join(ch for ch in str(value or "").upper().strip() if ch.isalnum() or ch in {".", "-"})
    return symbol[:12]


def _clean_prices(values):
    out = []
    for value in values or []:
        try:
            number = float(value)
        except (TypeError, ValueError):
            continue
        if isfinite(number) and number > 0:
            out.append(number)
    return out[-120:]


def _rsi14(prices):
    if len(prices) < 15:
        return None
    changes = [prices[i] - prices[i - 1] for i in range(len(prices) - 14, len(prices))]
    gains = sum(max(x, 0.0) for x in changes) / 14
    losses = sum(max(-x, 0.0) for x in changes) / 14
    if losses == 0:
        return 100.0
    rs = gains / losses
    return round(100.0 - (100.0 / (1.0 + rs)), 2)


def calculate_indicators(prices):
    prices = _clean_prices(prices)
    if len(prices) < 20:
        return {"ok": False, "status": "insufficient_price_history", "price_points": len(prices)}
    sma5 = sum(prices[-5:]) / 5
    sma20 = sum(prices[-20:]) / 20
    rsi = _rsi14(prices)
    last = prices[-1]
    if sma5 > sma20 and (rsi is None or rsi < 70):
        signal, reason = "POSITIVE", "Short-term trend is above the 20-period trend without an overbought RSI condition."
    elif sma5 < sma20:
        signal, reason = "WEAK", "Short-term trend is below the 20-period trend."
    else:
        signal, reason = "MIXED", "Trend signals are not decisive."
    if rsi is not None and rsi >= 70:
        signal, reason = "CAUTION", "Momentum is elevated and RSI is in an overbought range."
    elif rsi is not None and rsi <= 30:
        signal, reason = "WATCH", "RSI is in an oversold range; confirmation is still required before any trade decision."
    return {
        "ok": True,
        "status": "indicators_ready",
        "last_price": round(last, 4),
        "sma5": round(sma5, 4),
        "sma20": round(sma20, 4),
        "rsi14": rsi,
        "signal": signal,
        "reason": reason,
        "price_points": len(prices),
    }


def build_stock_intelligence_plan(symbol, prices, position_qty=0, average_entry=0, owner_instruction="", owner_approved=False):
    symbol = _clean_symbol(symbol)
    instruction = str(owner_instruction or "").strip()
    low = instruction.lower()
    base = {
        "ok": True,
        "mode": "read_only_stock_intelligence",
        "symbol": symbol,
        "owner_instruction_received": bool(instruction),
        "owner_approved": bool(owner_approved),
        "owner_approval_required": False,
        "trade_intent_detected": False,
        "ready_for_separate_paper_trade_review": False,
        "paper_trading_only": True,
        "live_trading_blocked": True,
        "order_execution_available": False,
        "execution_performed": False,
        "external_network_accessed": False,
        "credentials_returned": False,
        "private_payloads_returned": False,
    }
    if any(x in low for x in SENSITIVE_HINTS):
        return {**base, "ok": False, "status": "sensitive_content_rejected"}
    if not symbol:
        return {**base, "ok": False, "status": "symbol_required"}
    indicators = calculate_indicators(prices)
    if not indicators.get("ok"):
        return {**base, "ok": False, "status": indicators["status"], "price_points": indicators.get("price_points", 0)}
    try:
        qty = max(float(position_qty or 0), 0.0)
        entry = max(float(average_entry or 0), 0.0)
    except (TypeError, ValueError):
        qty, entry = 0.0, 0.0
    last = indicators["last_price"]
    unrealized = round((last - entry) * qty, 2) if qty > 0 and entry > 0 else 0.0
    portfolio = {
        "held": qty > 0,
        "position_qty": round(qty, 6),
        "average_entry": round(entry, 4) if entry else 0.0,
        "estimated_market_value": round(last * qty, 2),
        "estimated_unrealized_pl": unrealized,
    }
    signal = indicators["signal"]
    if portfolio["held"] and signal in {"WEAK", "CAUTION"}:
        advice = "REVIEW"
        advice_reason = "Existing position should be reviewed because current technical conditions are not strongly positive."
    elif signal == "POSITIVE":
        advice = "WATCH_POSITIVE"
        advice_reason = "Technical trend is positive, but Adam is providing intelligence only and will not trade automatically."
    else:
        advice = "WAIT"
        advice_reason = "Current indicators do not justify an automatic action. Continue monitoring and use owner judgment."
    trade_intent = any(x in low for x in TRADE_HINTS)
    result = {
        **base,
        "status": "intelligence_ready",
        "indicators": indicators,
        "portfolio_context": portfolio,
        "advice": advice,
        "advice_reason": advice_reason,
        "trade_intent_detected": trade_intent,
    }
    if trade_intent:
        result["owner_approval_required"] = True
        if not owner_approved:
            result["status"] = "owner_approval_required_for_trade_handoff"
        else:
            result["status"] = "ready_for_separate_paper_trade_review"
            result["ready_for_separate_paper_trade_review"] = True
    return result


def self_test():
    prices = [100, 100.5, 101, 101.3, 101.8, 102.0, 102.4, 102.8, 103.1, 103.5,
              103.9, 104.2, 104.5, 104.9, 105.1, 105.4, 105.8, 106.0, 106.3, 106.6,
              106.9, 107.1, 107.4, 107.6, 107.9]
    analysis = build_stock_intelligence_plan("NVDA", prices, 2, 101, "Analyze NVDA", False)
    denied = build_stock_intelligence_plan("NVDA", prices, 2, 101, "Buy NVDA", False)
    approved = build_stock_intelligence_plan("NVDA", prices, 2, 101, "Buy NVDA", True)
    sensitive = build_stock_intelligence_plan("NVDA", prices, 2, 101, "Use my API key secret to trade", True)
    checks = {
        "indicator_analysis_verified": analysis.get("status") == "intelligence_ready" and analysis.get("indicators", {}).get("sma5") is not None,
        "portfolio_context_verified": analysis.get("portfolio_context", {}).get("held") is True,
        "owner_approval_trade_handoff_gate_verified": denied.get("status") == "owner_approval_required_for_trade_handoff" and not denied.get("ready_for_separate_paper_trade_review"),
        "approved_paper_trade_review_handoff_verified": approved.get("status") == "ready_for_separate_paper_trade_review" and approved.get("ready_for_separate_paper_trade_review") is True,
        "live_trading_blocked_verified": all(x.get("live_trading_blocked") is True and x.get("order_execution_available") is False for x in (analysis, denied, approved)),
        "sensitive_content_rejection_verified": sensitive.get("status") == "sensitive_content_rejected",
    }
    return {
        "ok": all(checks.values()),
        **checks,
        "synthetic_inputs_only": True,
        "external_network_accessed": False,
        "real_market_data_accessed": False,
        "real_order_submitted": False,
        "credentials_exposed": False,
        "private_payloads_exposed": False,
    }
