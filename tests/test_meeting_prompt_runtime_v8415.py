from pathlib import Path
import ast
import pytest

ROOT = Path(__file__).resolve().parents[1]
APP_TEXT = (ROOT / "app.py").read_text(encoding="utf-8")
HTML = (ROOT / "templates" / "real_meeting_attendance.html").read_text(encoding="utf-8")


def _meeting_prompt_expression():
    tree = ast.parse(APP_TEXT)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "meeting_conversation_ask_v7411":
            for stmt in node.body:
                if isinstance(stmt, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "prompt" for t in stmt.targets):
                    return stmt.value
    raise AssertionError("meeting prompt assignment not found")


def _env(**overrides):
    base = {
        "authority_profile": "Answer and explain only",
        "declared_participants": "Mohamad",
        "direct_question": True,
        "durable_memory_text": "",
        "effective_meeting_context": "Adam, what is the function of a water pump?",
        "focus_agenda": "MEP coordination",
        "followup_priority": False,
        "history_lines": [],
        "immediate_prior_answer": "",
        "immediate_prior_question": "",
        "immediate_prior_topic": "",
        "language_hint": "auto-multilingual",
        "meeting_title": "MEP",
        "owner_briefing": "",
        "participation_style": "balanced",
        "proactive_reason": "",
        "professional_scope": "auto",
        "professional_scope_prompt": lambda scope: "Cross-disciplinary professional mode.",
        "project_reference": "Tower",
        "question": "Adam, what is the function of a water pump?",
        "release_history_text": "",
        "reply_language": "English",
        "representative_mode": True,
        "response_required": True,
        "turn_kind": "question",
    }
    base.update(overrides)
    return base


def test_version_bumped():
    assert 'VERSION = "v8.4.1.5"' in APP_TEXT


def test_prompt_contains_no_unary_plus_operator():
    expr = _meeting_prompt_expression()
    assert not any(isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.UAdd) for n in ast.walk(expr))


def test_generic_diagnostic_correctly_names_meeting_server_path():
    assert "provider test passed; the failure is in the meeting server path" in HTML
    assert "Meeting server-path request failed while the AI provider test passed" in HTML


@pytest.mark.parametrize("env", [
    _env(),
    _env(direct_question=False, response_required=True, turn_kind="correction", question="Adam, correction: use 125 mm."),
    _env(direct_question=False, response_required=True, turn_kind="addressed_comment", proactive_reason="material technical risk", question="Adam, please flag that risk."),
])
def test_real_meeting_prompt_expression_executes_for_supported_turns(env):
    expr = _meeting_prompt_expression()
    compiled = compile(ast.Expression(expr), str(ROOT / "app.py"), "eval")
    prompt = eval(compiled, {}, env)
    assert isinstance(prompt, str)
    assert "Participant interaction:\n" + env["question"] in prompt
    assert "OWNER REPRESENTATIVE" in prompt
