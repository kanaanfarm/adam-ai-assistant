from pathlib import Path
import importlib.util
import pytest

ROOT = Path(__file__).resolve().parents[1]


def test_source_compiles_and_acquisition_markers_exist():
    source = (ROOT / "app.py").read_text(encoding="utf-8")
    compile(source, str(ROOT / "app.py"), "exec")
    assert 'VERSION = "v8.1.0.1"' in source
    assert 'BUILD_CHANNEL = "acquisition"' in source
    assert 'load_or_create_flask_secret(BASE_DIR)' in source
    assert '"/api/health"' in source
    assert 'local-personal-assistant-oauth' not in source


def _runtime_app():
    if importlib.util.find_spec("flask") is None:
        pytest.skip("Flask is not installed in this build container; run after INSTALL_REQUIREMENTS.bat on target Windows PC.")
    import app
    return app


def test_app_imports_when_runtime_dependencies_are_available():
    module = _runtime_app()
    assert module.app is not None
    assert module.VERSION == "v8.1.0"


def test_health_endpoint_contains_no_credential_values():
    module = _runtime_app()
    client = module.app.test_client()
    response = client.get("/api/health")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["ok"] is True
    assert payload["channel"] == "acquisition"
    # Endpoint may describe configuration status, but must never return values.
    serialized = response.get_data(as_text=True).lower()
    for forbidden in ("bearer ", "whatsapp_access_token\":", "ai_api_key\":", "alpaca_secret_key\":"):
        assert forbidden not in serialized
