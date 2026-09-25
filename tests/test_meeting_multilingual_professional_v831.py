from pathlib import Path
from adam_core.meeting_language_policy import detect_requested_reply_language, tts_locale_for_reply, professional_scope_prompt

ROOT = Path(__file__).resolve().parents[1]
APP = (ROOT / 'app.py').read_text(encoding='utf-8')
HTML = (ROOT / 'templates' / 'real_meeting_attendance.html').read_text(encoding='utf-8')


def test_version_and_multilingual_default():
    assert 'VERSION = "v8.3.1"' in APP
    assert 'Auto — All languages' in HTML
    assert 'value="auto-multilingual" selected' in HTML


def test_default_english_and_language_switches():
    assert detect_requested_reply_language('Adam, speak Arabic please') == 'Lebanese Arabic'
    assert detect_requested_reply_language('آدم احكي بالعربي لو سمحت') == 'Lebanese Arabic'
    assert detect_requested_reply_language('Adam, please answer in French') == 'French'
    assert detect_requested_reply_language('آدم جاوب بالإنجليزي') == 'English'
    assert detect_requested_reply_language('We discussed the Arabic translation yesterday') is None
    assert tts_locale_for_reply('Lebanese Arabic') == 'ar-LB'
    assert tts_locale_for_reply('English') == 'en-US'


def test_cross_disciplinary_professional_policy():
    p = professional_scope_prompt('auto')
    for term in ('engineering', 'project management', 'commercial/contracts', 'procurement', 'finance', 'IT/software', 'sales/business'):
        assert term in p
    assert 'Do not pretend to hold a professional license' in p
    assert 'Auto-detect — cross-disciplinary professional' in HTML


def test_owner_safety_preserved():
    assert 'cannot approve costs, variations, contractual changes' in HTML
    assert 'Never pretend to be the owner or a human.' in APP
    assert 'consequential commitment' in APP
    assert 'real approved platform adapter' in HTML


def test_session_language_memory_and_tts_binding():
    assert '_MEETING_CONVERSATION_LANGUAGE_PREFS' in APP
    assert 'reply_tts_locale' in APP
    assert "j.reply_tts_locale" in HTML
    assert 'meetingIdentityDeclared=true' in HTML


def test_multilingual_transcription_path():
    assert 'meeting_multilingual_transcribed' in APP
    assert "ml==='auto-multilingual'||ml==='auto-bilingual'" in HTML
    assert 'multilingual server transcription' in HTML
