from pathlib import Path

from adam_core.correction_context_guard import (
    build_correction_isolation_instruction,
    is_explicit_correction,
    latest_owner_correction,
    self_test,
)

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / "app.py").read_text(encoding="utf-8")

CORRECTION = "I didn't say third-water part. I said Empower request channel for chilled water."


def test_exact_owner_correction_is_detected_without_importing_prior_pipe_sizes():
    history = [
        {"role": "user", "content": "The chilled water pipe is 100 mm and contractor wants 125 mm."},
        {"role": "assistant", "content": "We should review the 100 to 125 mm request."},
    ]
    guard = build_correction_isolation_instruction(CORRECTION, history)
    assert is_explicit_correction(CORRECTION)
    assert "Empower request channel for chilled water" in guard
    assert "100 mm" not in guard
    assert "125 mm" not in guard
    assert "Conversation adjacency is not confirmation" in guard


def test_followup_summary_keeps_recent_correction_boundary():
    history = [
        {"role": "user", "content": "The chilled water pipe is 100 mm and contractor wants 125 mm."},
        {"role": "assistant", "content": "The request is 100 to 125 mm."},
        {"role": "user", "content": CORRECTION},
        {"role": "assistant", "content": "Understood."},
    ]
    assert latest_owner_correction(history) == CORRECTION
    guard = build_correction_isolation_instruction("Separate the three subjects and summarize them.", history)
    assert "A RECENT OWNER CORRECTION REMAINS ACTIVE" in guard
    assert "do not reintroduce the superseded or unconfirmed association" in guard.lower()


def test_no_correction_guard_on_unrelated_history():
    history = [{"role": "user", "content": "What is the capital of Australia?"}]
    assert build_correction_isolation_instruction("Explain a fire pump.", history) == ""


def test_app_wires_guard_into_main_chat_and_version():
    assert 'VERSION = "v8.4.0.1"' in APP
    assert 'build_correction_isolation_instruction(str(body.get("text") or ""), history)' in APP
    assert 'if correction_guard:' in APP
    assert '/api/personal-assistant/correction-context-guard/self-test' in APP


def test_module_self_test():
    assert self_test()["ok"] is True
