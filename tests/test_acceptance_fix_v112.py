from pathlib import Path
import re

APP = Path(__file__).resolve().parents[1] / 'app.py'
FOLLOWUPS = Path(__file__).resolve().parents[1] / 'templates' / 'followups.html'

def test_ai_text_compatibility_helper_restored():
    text=APP.read_text(encoding='utf-8')
    assert 'def ai_text(prompt, max_tokens=1200, language="English"):' in text
    assert 'return call_ai(prompt, language)' in text

def test_test13_phrases_are_covered_by_planner():
    text=APP.read_text(encoding='utf-8')
    assert '"review material"' in text
    assert '"prepare a response"' in text
    assert '"email it"' in text

def test_followup_ui_has_error_handling_and_body_fallback():
    text=FOLLOWUPS.read_text(encoding='utf-8')
    assert "try{d=JSON.parse(raw)}catch(_)" in text
    assert "d.body||d.draft||''" in text
