from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_v720_source_and_routes():
    app=(ROOT/'app.py').read_text(encoding='utf-8')
    core=(ROOT/'adam_core'/'real_daily_assistant.py').read_text(encoding='utf-8')
    assert 'VERSION = "v8.1.0.1"' in app
    assert '/api/personal-assistant/real-daily-assistant' in app
    assert '/api/personal-assistant/real-daily-assistant/self-test' in app
    for marker in ['read_only_real_daily_assistant','priority_messages','open_followups','memory_context_present','voice_ready']:
        assert marker in core
    for marker in ['credentials_exposed','message_bodies_exposed','execution_performed']:
        assert marker in core
