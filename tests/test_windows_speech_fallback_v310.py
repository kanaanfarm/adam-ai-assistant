from pathlib import Path
from types import SimpleNamespace

from adam_core.windows_speech_fallback import MAX_TEXT_CHARS, WindowsSpeechError, synthesize_windows_speech
from adam_core.windows_speech_fallback_boundary import build_windows_speech_manifest, windows_speech_is_privacy_safe, windows_speech_self_test


def test_manifest_privacy_and_hash():
    payload = build_windows_speech_manifest("v3.1.0")
    assert windows_speech_is_privacy_safe(payload)
    assert len(payload["windows_speech_fallback_sha256"]) == 64


def test_self_test_without_powershell_or_network():
    result = windows_speech_self_test()
    assert result["ok"]
    assert result["powershell_required_by_self_test"] is False
    assert result["external_network_accessed"] is False


def test_injected_runner_and_cleanup(tmp_path):
    seen = {}
    def runner(args, env=None, **kwargs):
        seen["text"] = Path(env["ADAM_TTS_TEXT_FILE"]).read_text(encoding="utf-8-sig")
        Path(env["ADAM_TTS_WAV_FILE"]).write_bytes(b"RIFF" + b"0" * 196)
        return SimpleNamespace(returncode=0, stdout="", stderr="private detail")
    audio = synthesize_windows_speech("x" * (MAX_TEXT_CHARS + 20), os_name="nt", runner=runner, temp_dir=tmp_path)
    assert len(seen["text"]) == MAX_TEXT_CHARS
    assert len(audio) >= 100
    assert list(tmp_path.iterdir()) == []


def test_platform_guard():
    try:
        synthesize_windows_speech("hello", os_name="posix", runner=lambda *a, **k: None)
    except WindowsSpeechError:
        return
    assert False


def test_app_integration_source():
    src = Path("app.py").read_text(encoding="utf-8")
    assert 'VERSION = "v8.1.0.1"' in src
    assert 'return core_windows_speech_synthesize(text=text, os_name=os.name, runner=subprocess.run, timeout=90)' in src
    assert '/api/acquisition/windows-speech-fallback-boundary' in src
