import json
import re
import subprocess
from pathlib import Path


def _run_alert_policy(template: str) -> dict:
    text = Path(template).read_text(encoding="utf-8")
    match = re.search(r'<script id="adam-stock-alert-script">(.*?)</script>', text, re.S)
    assert match, f"stock alert script missing from {template}"
    probe = r"""
const first=adamStockAlertsToNotify([
  {symbol:'MSFT',type:'SELL',reason:'Stop-loss reached: -3.16% vs -3% rule.'},
  {symbol:'TSLA',type:'SELL',reason:'Stop-loss reached: -7.13% vs -3% rule.'}
]);
const refresh=adamStockAlertsToNotify([
  {symbol:'MSFT',type:'SELL',reason:'Stop-loss reached: -3.20% vs -3% rule.'},
  {symbol:'TSLA',type:'SELL',reason:'Stop-loss reached: -7.21% vs -3% rule.'}
]);
const next=adamStockAlertsToNotify([
  {symbol:'MSFT',type:'SELL',reason:'Stop-loss reached: -3.25% vs -3% rule.'},
  {symbol:'TSLA',type:'SELL',reason:'Stop-loss reached: -7.25% vs -3% rule.'},
  {symbol:'NVDA',type:'SELL',reason:'Stop-loss reached.'}
]);
console.log(JSON.stringify({first:first.map(adamStockAlertKey),refresh:refresh.map(adamStockAlertKey),next:next.map(adamStockAlertKey)}));
"""
    harness = r"""
const store={};
global.localStorage={getItem:k=>Object.prototype.hasOwnProperty.call(store,k)?store[k]:null,setItem:(k,v)=>{store[k]=String(v)}};
global.document={getElementById:id=>id==='stockNotificationMode'?{value:'once_per_signal'}:null,readyState:'loading',addEventListener:()=>{}};
"""
    result = subprocess.run(
        ["node", "-e", harness + match.group(1) + probe],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def test_v8001_once_per_signal_ignores_changing_market_reason():
    for template in ("templates/stock.html", "templates/index.html"):
        result = _run_alert_policy(template)
        assert result["first"] == ["MSFT|SELL", "TSLA|SELL"]
        assert result["refresh"] == []
        assert result["next"] == ["NVDA|SELL"]


def test_v8001_version_and_stable_persistent_identity_are_wired():
    assert 'VERSION = "v8.1.0.1"' in Path("app.py").read_text(encoding="utf-8")
    for template in ("templates/stock.html", "templates/index.html"):
        text = Path(template).read_text(encoding="utf-8")
        assert "adam_v8001_stock_seen_signals" in text
        assert "String(alert&&alert.symbol" in text
        assert "alert.reason" not in re.search(
            r"function adamStockAlertKey\(alert\)\{(.*?)\n\}", text, re.S
        ).group(1)
        assert ".slice(-200)" in text
