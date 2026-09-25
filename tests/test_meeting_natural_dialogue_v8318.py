from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / "app.py").read_text(encoding="utf-8")
HTML = (ROOT / "templates" / "real_meeting_attendance.html").read_text(encoding="utf-8")

def test_version():
    assert 'VERSION = "v8.3.1.8"' in APP

def test_natural_dialogue_policy_present():
    assert "NATURAL PROFESSIONAL DIALOGUE" in APP
    assert "experienced colleague in a real meeting" in APP

def test_direct_answer_and_adaptive_length():
    assert "Start with the actual answer or position" in APP
    assert "Adapt the reply to the moment" in APP

def test_no_robotic_preamble_policy():
    assert "Do not repeat the participant's whole question" in APP
    assert "Do not automatically turn every answer into a bullet list" in APP

def test_contextual_followup_policy():
    assert "Use meeting context actively" in APP
    assert "continue from the prior discussion" in APP

def test_owner_boundaries_preserved():
    assert "must NOT approve variations" in APP
    assert "separate owner approval" in APP

def test_ui_shows_natural_dialogue():
    assert "Natural meeting dialogue:</b> ON" in HTML
