from pathlib import Path
import ast

ROOT=Path(__file__).resolve().parents[1]
APP_TEXT=(ROOT/'app.py').read_text(encoding='utf-8')


def load_score_function():
    tree=ast.parse(APP_TEXT)
    fn=next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name=="stock_opportunity_score")
    mod=ast.Module(body=[fn], type_ignores=[])
    ns={}
    exec(compile(mod, "<score>", "exec"), ns)
    return ns["stock_opportunity_score"]


def test_version():
    assert 'VERSION = "v8.4.1.15.1"' in APP_TEXT


def test_score_uses_bounded_components():
    for token in ('confidence_points = confidence * 0.55','trend_points','rsi_points','signal_points','regime_points'):
        assert token in APP_TEXT


def test_strong_candidates_do_not_all_saturate():
    score_fn=load_score_function()
    a={'signal':'BUY','confidence':85,'rsi':61.75,'sma5':263.04,'sma20':259.69}
    b={'signal':'BUY','confidence':85,'rsi':56.34,'sma5':514.03,'sma20':507.17}
    c={'signal':'BUY','confidence':85,'rsi':51.34,'sma5':342.89,'sma20':338.43}
    scores=[score_fn(x,'BEARISH') for x in (a,b,c)]
    assert max(scores) < 100
    assert len(set(scores)) >= 2


def test_score_stays_bounded():
    score_fn=load_score_function()
    extreme={'signal':'BUY','confidence':100,'rsi':55,'sma5':200,'sma20':100}
    weak={'signal':'WAIT','confidence':0,'rsi':90,'sma5':50,'sma20':100}
    assert 0 <= score_fn(extreme,'BULLISH') <= 100
    assert 0 <= score_fn(weak,'BEARISH') <= 100


def test_bearish_regime_does_not_force_buy():
    assert 'elif item.get("signal") == "BUY":\n            action = "WAIT"' in APP_TEXT


def test_trade_governance_preserved():
    assert 'PENDING_OWNER_APPROVAL' in APP_TEXT
    assert '"max_exposure": 500' in APP_TEXT
    assert '"max_new_position": 100' in APP_TEXT
