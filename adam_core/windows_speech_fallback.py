"""Windows speech fallback transport for Adam Acquisition v3.1."""
from __future__ import annotations

import os
import subprocess
import tempfile
from pathlib import Path

MAX_TEXT_CHARS = 4096
MIN_WAV_BYTES = 100


class WindowsSpeechError(RuntimeError):
    pass


def _powershell_script():
    return (
        "Add-Type -AssemblyName System.Speech; "
        "$s=New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        "$s.Rate=-1; $s.Volume=100; "
        "$s.SetOutputToWaveFile($env:ADAM_TTS_WAV_FILE); "
        "$t=[IO.File]::ReadAllText($env:ADAM_TTS_TEXT_FILE,[Text.Encoding]::UTF8); "
        "$s.Speak($t); $s.Dispose()"
    )


def synthesize_windows_speech(text, *, os_name=None, runner=None, timeout=90, temp_dir=None):
    """Generate WAV bytes with Windows System.Speech using an injected runner for testing."""
    platform_name = os_name if os_name is not None else os.name
    if platform_name != "nt":
        raise WindowsSpeechError("Windows speech is available only on Windows.")

    text = str(text or "").strip()
    if not text:
        raise WindowsSpeechError("There is no text to speak.")
    text = text[:MAX_TEXT_CHARS]
    runner = runner or subprocess.run

    text_path = None
    wav_path = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", encoding="utf-8-sig", delete=False, dir=temp_dir) as text_file:
            text_file.write(text)
            text_path = text_file.name
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False, dir=temp_dir) as wav_file:
            wav_path = wav_file.name

        env = os.environ.copy()
        env["ADAM_TTS_TEXT_FILE"] = text_path
        env["ADAM_TTS_WAV_FILE"] = wav_path
        result = runner(
            ["powershell.exe", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-Command", _powershell_script()],
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        if getattr(result, "returncode", 1) != 0:
            raise WindowsSpeechError("Windows speech failed.")

        audio = Path(wav_path).read_bytes()
        if len(audio) < MIN_WAV_BYTES:
            raise WindowsSpeechError("Windows speech returned no audio.")
        return audio
    finally:
        for path in (text_path, wav_path):
            if path:
                try:
                    Path(path).unlink(missing_ok=True)
                except Exception:
                    pass
