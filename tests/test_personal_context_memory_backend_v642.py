from pathlib import Path


def test_v642_memory_routes_use_defined_buyer_isolated_store():
    src = Path("app.py").read_text(encoding="utf-8")
    assert 'VERSION = "v8.1.0.1"' in src
    assert 'PERSONAL_CONTEXT_FILE = _BUYER_STATE_ROOT / "data" / "personal_context_v640.json"' in src
    assert 'remember_personal_context(PERSONAL_CONTEXT_FILE' in src
    assert 'recall_personal_context(PERSONAL_CONTEXT_FILE' in src
    assert 'ADAM_STATE_DIR / "personal_context_v640.json"' not in src


def test_v642_recall_has_json_error_boundary():
    src = Path("app.py").read_text(encoding="utf-8")
    assert '"status":"memory_store_error"' in src
