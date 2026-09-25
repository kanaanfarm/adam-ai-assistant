from pathlib import Path
from adam_core.ai_provider_transport import complete_text, build_responses_payload

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / 'app.py').read_text(encoding='utf-8')
HTML = (ROOT / 'templates' / 'real_meeting_attendance.html').read_text(encoding='utf-8')


class _Resp:
    def __init__(self, payload, status=200):
        self._payload = payload
        self.status_code = status
        self.ok = 200 <= status < 300
        self.text = 'synthetic-error' if not self.ok else 'synthetic-ok'
    def json(self):
        return self._payload


class _Http:
    def __init__(self, response):
        self.response = response
        self.calls = []
    def post(self, url, **kwargs):
        self.calls.append((url, kwargs))
        return self.response


def test_release_version():
    assert 'VERSION = "v8.4.1.3"' in APP


def test_gpt56_official_openai_uses_responses_api():
    h = _Http(_Resp({'output_text': 'ANSWER: pump circulates chilled water'}))
    out = complete_text('https://api.openai.com/v1', 'secret', 'gpt-5.6', 'question', 'English', 'system', http=h, max_tokens=400, timeout=25)
    assert out == 'ANSWER: pump circulates chilled water'
    url, kwargs = h.calls[0]
    assert url.endswith('/responses')
    assert kwargs['timeout'] == 25
    assert kwargs['json']['model'] == 'gpt-5.6'
    assert kwargs['json']['reasoning']['effort'] == 'low'
    assert kwargs['json']['max_output_tokens'] == 400
    assert 'input' in kwargs['json'] and 'messages' not in kwargs['json']


def test_custom_provider_keeps_chat_completions_compatibility():
    h = _Http(_Resp({'choices': [{'message': {'content': 'legacy answer'}}]}))
    out = complete_text('https://provider.example/v1', 'secret', 'gpt-5.6', 'question', 'English', 'system', http=h, max_tokens=300, timeout=12)
    assert out == 'legacy answer'
    url, kwargs = h.calls[0]
    assert url.endswith('/chat/completions')
    assert kwargs['timeout'] == 12


def test_responses_payload_is_bounded_and_low_latency_reasoning():
    p = build_responses_payload('q', 'English', 'gpt-5.6', 'system', 999999)
    assert p['max_output_tokens'] == 8192
    assert p['reasoning'] == {'effort': 'low'}


def test_meeting_browser_has_provider_watchdog_and_visible_failure_state():
    run = HTML.split('async function runInteractiveConversation', 1)[1].split("document.getElementById('generateReport')", 1)[0]
    assert 'AbortController' in run
    assert 'setTimeout(()=>providerController.abort(),30000)' in run
    assert "j.status==='client_ai_provider_timeout'" in run
    assert "AI provider error — question retained" in run
    assert 'Open AI Settings and run Test AI Connection' in run


def test_meeting_server_provider_timeout_remains_bounded():
    ask = APP.split('def meeting_conversation_ask_v7411():', 1)[1].split('@app.route("/api/personal-assistant/meeting-conversation/report"', 1)[0]
    assert 'max_tokens=700, timeout=25' in ask
    assert 'ai_provider_timeout' in ask
    assert 'ai_provider_error' in ask
