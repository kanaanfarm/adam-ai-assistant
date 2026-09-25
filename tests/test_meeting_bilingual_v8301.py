from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
APP=(ROOT/'app.py').read_text(encoding='utf-8')
HTML=(ROOT/'templates'/'real_meeting_attendance.html').read_text(encoding='utf-8')

def test_version(): assert 'VERSION = "v8.3.0.1"' in APP
def test_bilingual_default(): assert 'Auto — Lebanese Arabic + English' in HTML and 'value="auto-bilingual" selected' in HTML
def test_mixed_language_prompt(): assert 'mix Lebanese Arabic and English' in APP and 'same sentence' in APP
def test_lebanese_recognition_bias(): assert "ml==='auto-bilingual'||ml==='ar-LB'" in HTML and "?'ar-LB'" in HTML
def test_dynamic_tts(): assert "value==='auto-bilingual'" in HTML and "'ar-LB':'en-US'" in HTML
def test_boundaries_preserved(): assert 'must NOT approve variations' in APP and 'separate owner approval' in APP
