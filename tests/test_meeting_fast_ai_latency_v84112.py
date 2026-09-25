from pathlib import Path
import ast
import re

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / 'app.py').read_text(encoding='utf-8')
TRANSPORT = (ROOT / 'adam_core' / 'ai_provider_transport.py').read_text(encoding='utf-8')
HTML = (ROOT / 'templates' / 'real_meeting_attendance.html').read_text(encoding='utf-8')


def _load_fast_helper():
    tree = ast.parse(APP)
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == '_meeting_latency_fast_factual_turn')
    module = ast.Module(body=[node], type_ignores=[])
    ast.fix_missing_locations(module)
    ns = {'re': re}
    exec(compile(module, str(ROOT / 'app.py'), 'exec'), ns, ns)
    return ns['_meeting_latency_fast_factual_turn']


def test_version_bumped():
    assert 'VERSION = "v8.4.1.12.1"' in APP


def test_fast_factual_profile_uses_smaller_output_budget():
    assert 'meeting_max_tokens = 160 if latency_fast_path else 700' in APP


def test_fast_factual_profile_uses_minimal_reasoning_only_for_fast_path():
    assert 'meeting_reasoning_effort = "none" if latency_fast_path else "low"' in APP
    assert 'reasoning_effort=meeting_reasoning_effort' in APP


def test_normal_call_ai_default_remains_low_reasoning():
    assert 'def call_ai(prompt, language="English", max_tokens=1200, timeout=60, reasoning_effort="low")' in APP
    assert 'def complete_text(api_base, api_key, model, prompt, language, master_prompt, *, http, max_tokens=1200, timeout=60, reasoning_effort="low")' in TRANSPORT


def test_transport_threads_reasoning_effort_to_responses_payload():
    assert 'reasoning_effort=reasoning_effort' in TRANSPORT
    assert 'def _post_responses' in TRANSPORT and 'reasoning_effort="low"' in TRANSPORT


def test_fast_prompt_does_not_send_meeting_history_or_briefing():
    start = APP.index('if latency_fast_path:')
    end = APP.index('# v8.4.1.8 — deterministic decision-critical clarification gate', start)
    block = APP[start:end]
    assert 'Owner briefing' not in block
    assert 'Recent live meeting context' not in block
    assert 'Meeting context retained' not in block
    assert 'Question:\\n' in block


def test_fast_prompt_preserves_owner_authority():
    start = APP.index('if latency_fast_path:')
    end = APP.index('# v8.4.1.8 — deterministic decision-critical clarification gate', start)
    block = APP[start:end]
    assert 'never approve or authorize anything on Mohamad' in block
    assert 'Do not invent project facts' in block


def test_fast_eligibility_stays_narrow():
    helper = _load_fast_helper()
    assert helper('Adam, what is the function of a balancing valve?', True, False, False, 'question', '') is True
    assert helper('Can you approve us to proceed with the 100 mm chilled-water pipe?', True, False, False, 'question', '') is False
    assert helper('Should we change the chilled-water pump?', True, False, False, 'question', '') is False
    assert helper('What is the approved static pressure for this project?', True, False, False, 'question', '') is False
    assert helper('What is the function of the balancing valve?', True, False, True, 'question', '') is False


def test_locked_end_turn_and_voice_paths_unchanged():
    assert 'MEETING_FAST_END_OF_TURN_SILENCE_MS=2400' in HTML
    assert 'MEETING_END_OF_TURN_SILENCE_MS=4200' in HTML
    assert 'meetingInstantFactualVoice' in HTML
    assert "instantFactualVoice&&meetingLatencyTrace.fastPath&&('speechSynthesis' in window)" in HTML


def test_response_exposes_fast_ai_profile_for_diagnostics():
    assert '"meeting_reasoning_effort": meeting_reasoning_effort' in APP
    assert '"meeting_max_tokens": meeting_max_tokens' in APP
