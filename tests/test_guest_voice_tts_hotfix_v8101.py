from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_v8101_version_and_guest_tts_hotfix_present():
    app = (ROOT / "app.py").read_text(encoding="utf-8")
    guest = (ROOT / "templates" / "guest_voice_session.html").read_text(encoding="utf-8")
    assert 'VERSION = "v8.1.0.1"' in app
    assert 'language_preference' in app
    assert 'voice_language' in app
    assert 'natural everyday Lebanese Arabic' in app
    assert 'if(processing||speaking||currentAudio)return' in guest
    assert "await speak(d.reply,d.voice_language||sessionLanguage)" in guest
    assert "sessionLanguage='ar-LB'" in guest
    assert "rec.lang=recognitionLanguage()" in guest
    assert "Every reply is spoken automatically" in guest


def test_v8101_approval_block_reply_remains_safe_and_speakable():
    app = (ROOT / "app.py").read_text(encoding="utf-8")
    assert 'if decision.get("status") == "owner_approval_required":' in app
    assert '"voice_language": requested_language' in app
    assert 'هالطلب بدّو موافقة منفصلة من المالك' in app
    assert '"external_action_executed": False' in app


def test_v8101_existing_guest_safety_boundary_still_passes():
    from adam_core.guest_voice_session import self_test
    result = self_test()
    assert result['ok'] is True
    assert result['private_owner_data_blocked_verified'] is True
    assert result['consequential_action_blocked_verified'] is True
    assert result['external_action_executed'] is False
