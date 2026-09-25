from pathlib import Path
from adam_core.stock_notification_policy import evaluate_notification, self_test


def test_v701_policy_self_test():
    result = self_test()
    assert result["ok"] is True
    assert result["default_once_per_signal_verified"] is True
    assert result["temporary_no_alert_does_not_rearm_duplicate_verified"] is True
    assert result["status_change_mode_verified"] is True
    assert result["explicit_every_check_mode_verified"] is True
    assert result["off_mode_verified"] is True
    assert result["real_order_submitted"] is False
    assert result["external_network_accessed"] is False


def test_v701_ui_and_routes_are_wired():
    app = Path("app.py").read_text(encoding="utf-8")
    assert 'VERSION = "v8.1.0.1"' in app
    assert '/api/personal-assistant/stock-notifications/self-test' in app
    assert '/api/personal-assistant/stock-notifications/review' in app
    for name in ("templates/index.html", "templates/stock.html"):
        text = Path(name).read_text(encoding="utf-8")
        assert 'id="stockNotificationMode"' in text
        assert 'once_per_signal' in text
        assert 'status_change' in text
        assert 'every_check' in text
        assert 'adam_v701_stock_notification_mode' in text
        assert 'temporary no-alert cycles do not re-arm the same signal' in text
        assert 'setInterval(()=>refreshStockDashboard(false),120000)' in text
        assert 'setInterval(()=>refreshStockDashboard(true),120000)' not in text


def test_v701_duplicate_suppression_semantics():
    assert evaluate_notification("once_per_signal", "NVDA|SELL", "")["should_notify"] is True
    assert evaluate_notification("once_per_signal", "NVDA|SELL", "NVDA|SELL")["should_notify"] is False
    assert evaluate_notification("off", "NVDA|SELL", "")["should_notify"] is False
    assert evaluate_notification("every_check", "NVDA|SELL", "NVDA|SELL")["should_notify"] is True
