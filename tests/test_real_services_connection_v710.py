from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_v710_real_services_connection_boundary():
    app=(ROOT/'app.py').read_text(encoding='utf-8')
    mod=(ROOT/'adam_core'/'real_services_connection.py').read_text(encoding='utf-8')
    assert 'VERSION = "v8.1.0.1"' in app
    assert '/api/personal-assistant/real-services-connection/self-test' in app
    assert '/api/personal-assistant/real-services-connection/status' in app
    assert 'ms_status()' in app and 'whatsapp_connection_status()' in app
    assert 'credentials_exposed' in mod and 'consequential_action_executed' in mod
