"""Privacy-safe Alpaca Paper account projection for Adam v8.0.1."""
from __future__ import annotations


CANCELABLE_ORDER_STATUSES = {
    "new", "accepted", "pending_new", "partially_filled", "held", "calculated"
}


def _number(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def mask_account_number(value) -> str:
    text = str(value or "").strip()
    return f"••••{text[-4:]}" if text else "Paper account"


def project_position(position: dict) -> dict:
    return {
        "symbol": str(position.get("symbol") or "").upper(),
        "qty": _number(position.get("qty")),
        "qty_available": _number(position.get("qty_available", position.get("qty"))),
        "avg_entry_price": _number(position.get("avg_entry_price")),
        "current_price": _number(position.get("current_price")),
        "market_value": _number(position.get("market_value")),
        "unrealized_pl": _number(position.get("unrealized_pl")),
        "unrealized_plpc": _number(position.get("unrealized_plpc")),
    }


def project_order(order: dict) -> dict:
    status = str(order.get("status") or "unknown").lower()
    return {
        "order_id": str(order.get("id") or ""),
        "symbol": str(order.get("symbol") or "").upper(),
        "side": str(order.get("side") or "").lower(),
        "type": str(order.get("type") or "").lower(),
        "status": status,
        "qty": _number(order.get("qty")),
        "notional": _number(order.get("notional")),
        "filled_qty": _number(order.get("filled_qty")),
        "filled_avg_price": _number(order.get("filled_avg_price")),
        "submitted_at": order.get("submitted_at"),
        "filled_at": order.get("filled_at"),
        "cancelable": status in CANCELABLE_ORDER_STATUSES,
    }


def build_paper_overview(account: dict, positions: list, orders: list) -> dict:
    return {
        "ok": True,
        "mode": "paper",
        "live_trading_blocked": True,
        "account": {
            "label": mask_account_number(account.get("account_number")),
            "status": str(account.get("status") or "unknown"),
            "cash": _number(account.get("cash")),
            "portfolio_value": _number(account.get("portfolio_value")),
            "buying_power": _number(account.get("buying_power")),
        },
        "positions": [project_position(p) for p in positions if isinstance(p, dict)],
        "orders": [project_order(o) for o in orders if isinstance(o, dict)],
        "credentials_returned": False,
    }


def self_test() -> dict:
    result = build_paper_overview(
        {"account_number": "PA12345678", "status": "ACTIVE", "cash": "99999", "api_key": "secret"},
        [{"symbol": "AAPL", "qty": "0.0031", "qty_available": "0.0031", "market_value": "1.00"}],
        [{"id": "order-1", "symbol": "AAPL", "side": "buy", "notional": "1", "status": "accepted"}],
    )
    serialized = repr(result)
    return {
        "ok": result["account"]["label"] == "••••5678" and result["orders"][0]["cancelable"],
        "masked_account_verified": result["account"]["label"] == "••••5678",
        "position_quantity_verified": result["positions"][0]["qty"] == 0.0031,
        "order_status_verified": result["orders"][0]["status"] == "accepted",
        "cancelable_status_verified": result["orders"][0]["cancelable"] is True,
        "credentials_excluded_verified": "api_key" not in serialized and "secret" not in serialized,
        "live_trading_blocked": True,
        "external_network_accessed": False,
        "external_action_executed": False,
        "synthetic_inputs_only": True,
    }
