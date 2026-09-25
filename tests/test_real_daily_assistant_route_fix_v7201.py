from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_v7201_daily_route_is_registered_before_server_start_and_health_uses_persisted_ms_config():
    app=(ROOT/'app.py').read_text(encoding='utf-8')
    assert 'VERSION = "v8.1.0.1"' in app
    route_pos=app.index('@app.route("/api/personal-assistant/real-daily-assistant", methods=["GET"])')
    main_pos=app.index('if __name__ == "__main__":')
    assert route_pos < main_pos
    assert 'payload["runtime"]["microsoft_client_configured"] = bool(ms_load_config().get("client_id"))' in app
    assert '@app.route("/api/personal-assistant/real-daily-assistant/self-test", methods=["GET"])' in app
