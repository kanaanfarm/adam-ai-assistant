from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def test_v7012_stock_ui_has_dedicated_manual_trade_mount_and_status():
    ui=(ROOT/'templates'/'stock.html').read_text(encoding='utf-8')
    assert 'id="adamManualTradeMount"' in ui
    assert 'id="manualTradeOverride"' in ui
    assert 'FORCE BUY' in ui and 'FORCE SELL' in ui
    assert 'Alpaca Paper Account:' in ui
    assert 'NOT CONNECTED' in ui
    assert "manualMount.appendChild(manualPanel)" in ui

def test_v7012_version_bumped():
    app=(ROOT/'app.py').read_text(encoding='utf-8')
    assert 'VERSION = "v8.1.0.1"' in app
