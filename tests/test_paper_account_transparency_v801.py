from pathlib import Path
from unittest.mock import patch

import app as adam_app
from adam_core.paper_account_transparency import build_paper_overview, self_test


class _Response:
    def __init__(self, payload=None, status_code=200):
        self._payload = payload
        self.status_code = status_code
        self.ok = 200 <= status_code < 300
        self.text = ""

    def json(self):
        return self._payload


def test_v801_safe_projection_masks_account_and_excludes_credentials():
    result = build_paper_overview(
        {"account_number": "PA12345678", "status": "ACTIVE", "cash": "99", "api_key": "never-return"},
        [{"symbol": "AAPL", "qty": "0.0031", "qty_available": "0.0031"}],
        [{"id": "order-1", "symbol": "AAPL", "side": "buy", "notional": "1", "status": "accepted"}],
    )
    assert result["account"]["label"] == "••••5678"
    assert result["positions"][0]["qty"] == 0.0031
    assert result["orders"][0]["cancelable"] is True
    assert "api_key" not in repr(result) and "never-return" not in repr(result)
    assert self_test()["ok"] is True


def test_v801_overview_route_returns_positions_and_recent_orders_without_secrets():
    responses = [
        _Response({"account_number": "PA12345678", "status": "ACTIVE", "cash": "99999", "portfolio_value": "100000", "buying_power": "199998"}),
        _Response([{"symbol": "AAPL", "qty": "0.0031", "qty_available": "0.0031", "market_value": "1"}]),
        _Response([{"id": "abc-123", "symbol": "AAPL", "side": "buy", "notional": "1", "status": "filled"}]),
    ]
    with patch.object(adam_app, "require_paper_alpaca", return_value={"base_url": "https://paper-api.alpaca.markets", "api_key": "key", "secret_key": "secret"}), patch.object(adam_app.requests, "get", side_effect=responses):
        data = adam_app.app.test_client().get("/api/stock/paper-overview").get_json()
    assert data["ok"] is True and data["mode"] == "paper"
    assert data["positions"][0]["qty"] == 0.0031
    assert data["orders"][0]["status"] == "filled"
    assert "key" not in repr(data) and "secret" not in repr(data)


def test_v801_cancel_requires_both_owner_gates_and_targets_paper_only():
    client = adam_app.app.test_client()
    assert client.post("/api/stock/paper-order/abc-123/cancel", json={}).status_code == 403
    with patch.object(adam_app, "require_paper_alpaca", return_value={"base_url": "https://paper-api.alpaca.markets", "api_key": "key", "secret_key": "secret"}), patch.object(adam_app.requests, "delete", return_value=_Response(None, 204)) as delete:
        response = client.post("/api/stock/paper-order/abc-123/cancel", json={"owner_approved": True, "final_confirmed": True})
    assert response.status_code == 200 and response.get_json()["mode"] == "paper"
    assert delete.call_args.args[0] == "https://paper-api.alpaca.markets/v2/orders/abc-123"


def test_v801_stock_ui_exposes_activity_without_credentials():
    ui = Path("templates/stock.html").read_text(encoding="utf-8")
    app_source = Path("app.py").read_text(encoding="utf-8")
    assert 'VERSION = "v8.1.0.1"' in app_source
    for value in ("paperAccountActivity", "paperPositionDetails", "paperOrderDetails", "REFRESH PAPER ACTIVITY"):
        assert value in ui
    assert "/api/stock/paper-overview" in ui
    assert "FINAL CONFIRMATION" in ui and "owner_approved:true" in ui and "final_confirmed:true" in ui

