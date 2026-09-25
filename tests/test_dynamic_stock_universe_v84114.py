from pathlib import Path
import ast, re

APP = Path('app.py').read_text(encoding='utf-8')

def _load_universe_parts():
    tree=ast.parse(APP)
    env={'re':re}
    keep=[]
    names={'STOCK_UNIVERSE_CORE10','STOCK_UNIVERSE_50','STOCK_UNIVERSE_100'}
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t,ast.Name) and t.id in names for t in node.targets):
            keep.append(node)
        if isinstance(node, ast.FunctionDef) and node.name=='resolve_stock_universe':
            keep.append(node)
    mod=ast.Module(body=keep,type_ignores=[])
    exec(compile(mod,'<universe>','exec'),env)
    return env

def test_version_and_universe_sizes():
    assert 'VERSION = "v8.4.1.14"' in APP
    e=_load_universe_parts()
    assert len(e['STOCK_UNIVERSE_CORE10'])==10
    assert len(e['STOCK_UNIVERSE_50'])==50
    assert len(e['STOCK_UNIVERSE_100'])==100

def test_custom_symbols_are_added_and_not_hard_limited_to_old_four():
    e=_load_universe_parts()
    symbols=e['resolve_stock_universe']('PLTR,SHOP,CRWD','core10')
    for sym in ('PLTR','SHOP','CRWD','AMZN','META','SPY'):
        assert sym in symbols
    assert len(symbols)>5

def test_broad_50_and_100_are_resolved():
    e=_load_universe_parts()
    s50=e['resolve_stock_universe']('', 'top50')
    s100=e['resolve_stock_universe']('', 'top100')
    assert len([x for x in s50 if x!='SPY'])==50
    assert len([x for x in s100 if x!='SPY'])==100
    assert 'SPY' in s50 and 'SPY' in s100

def test_owner_approval_and_paper_limits_still_present():
    assert 'Owner approval is required before a paper order.' in APP
    assert 'Paper order amount must be between $1 and the $500 safety limit.' in APP
    assert '"status": "PENDING_OWNER_APPROVAL"' in APP

def test_stock_ui_exposes_dynamic_universe_and_custom_tickers():
    for name in ('templates/stock.html','templates/index.html'):
        ui=Path(name).read_text(encoding='utf-8')
        assert 'id="adamStockUniverse"' in ui
        assert 'value="top50"' in ui and 'value="top100"' in ui
        assert 'id="adamCustomSymbols"' in ui
        assert 'adamStockScanUrl' in ui
        assert "params.set('watchlist',custom.value.trim())" in ui

def test_main_summary_and_agent_cycle_accept_universe_selection_and_parallel_scan():
    assert 'request.args.get("universe") or "core10"' in APP
    assert 'body.get("universe") or "core10"' in APP
    assert '"scan_symbol_count": len(symbols)' in APP
    assert 'ThreadPoolExecutor' in APP and 'as_completed' in APP
