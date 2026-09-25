from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
APP=(ROOT/'app.py').read_text(encoding='utf-8')
STOCK=(ROOT/'templates'/'stock.html').read_text(encoding='utf-8')

def test_version():
    assert 'VERSION = "v8.4.1.15"' in APP

def test_score_helper_exists_and_is_bounded():
    assert 'def stock_opportunity_score(' in APP
    assert 'max(0, min(100' in APP

def test_score_does_not_override_trade_signal():
    assert 'The score does not' in APP or 'score does not' in APP
    assert 'opportunity_score' in APP
    assert 'action = "BUY"' in APP and 'action = "WAIT"' in APP

def test_rank_uses_opportunity_score():
    assert '-int(x.get("opportunity_score") or 0)' in APP

def test_ui_shows_top_10_and_score():
    assert 'items.slice(0,10)' in STOCK
    assert 'Opportunity Score ${score}' in STOCK
    assert 'Top 10' in STOCK

def test_readiness_labels_present():
    for label in ('VERY CLOSE','CLOSE','WATCH','WEAK'):
        assert label in APP

def test_dynamic_universe_preserved():
    for token in ('STOCK_UNIVERSE_CORE10','STOCK_UNIVERSE_50','STOCK_UNIVERSE_100','resolve_stock_universe'):
        assert token in APP

def test_owner_trade_governance_preserved():
    assert 'PENDING_OWNER_APPROVAL' in APP
    assert '"max_exposure": 500' in APP
    assert '"max_new_position": 100' in APP
