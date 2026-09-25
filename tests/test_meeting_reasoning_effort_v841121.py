from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / "app.py").read_text(encoding="utf-8")
TRANSPORT = (ROOT / "adam_core" / "ai_provider_transport.py").read_text(encoding="utf-8")


def test_fast_factual_path_uses_supported_none_effort():
    assert 'meeting_reasoning_effort = "none" if latency_fast_path else "low"' in APP
    assert '"minimal" if latency_fast_path' not in APP


def test_governed_path_keeps_low_reasoning():
    assert 'meeting_reasoning_effort = "none" if latency_fast_path else "low"' in APP


def test_reasoning_effort_is_forwarded_to_provider():
    assert 'reasoning_effort=meeting_reasoning_effort' in APP
    assert 'payload["reasoning"] = {"effort": str(reasoning_effort)}' in TRANSPORT


def test_fast_output_budget_remains_160_tokens():
    assert 'meeting_max_tokens = 160 if latency_fast_path else 700' in APP


def test_version_bumped():
    assert 'VERSION = "v8.4.1.12.1"' in APP
