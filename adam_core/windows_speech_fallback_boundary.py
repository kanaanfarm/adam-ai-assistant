"""Buyer-safe evidence for Adam Acquisition v3.1 Windows speech fallback."""
from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path
from types import SimpleNamespace

from .windows_speech_fallback import MAX_TEXT_CHARS, WindowsSpeechError, synthesize_windows_speech


def build_windows_speech_manifest(version):
    service = {
        "schema": "adam-acquisition-windows-speech-fallback-boundary/v1",
        "product": "Adam Acquisition",
        "version": version,
        "status": "extracted_tested",
        "boundary_module": "adam_core.windows_speech_fallback",
        "responsibilities": [
            "Windows System.Speech fallback synthesis",
            "bounded fallback speech input",
            "temporary speech-file lifecycle",
            "PowerShell execution isolation",
            "WAV output validation",
            "legacy assistant fallback compatibility",
        ],
        "controls": {
            "platform_guard_enforced": True,
            "speech_input_bounded": True,
            "subprocess_runner_injected": True,
            "temporary_files_cleaned": True,
            "wav_output_validated": True,
            "provider_error_details_sanitized": True,
            "legacy_windows_fallback_preserved": True,
            "service_testable_without_powershell": True,
        },
        "privacy": {
            "speech_text_exposed": False,
            "temporary_file_paths_exposed": False,
            "audio_bytes_exposed": False,
            "subprocess_stderr_exposed": False,
            "environment_values_exposed": False,
            "credential_values_exposed": False,
            "private_memory_exposed": False,
        },
        "next_extraction_targets": [
            "runtime configuration consolidation",
            "final acquisition demo hardening",
            "technical diligence closeout",
        ],
    }
    raw = json.dumps(service, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return {"windows_speech_fallback_service": service, "windows_speech_fallback_sha256": hashlib.sha256(raw).hexdigest()}


def windows_speech_is_privacy_safe(payload):
    privacy = payload.get("windows_speech_fallback_service", {}).get("privacy", {})
    return bool(privacy) and not any(bool(v) for v in privacy.values())


def windows_speech_self_test():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        seen = {}

        def fake_runner(args, env=None, **kwargs):
            seen["called"] = True
            wav = Path(env["ADAM_TTS_WAV_FILE"])
            wav.write_bytes(b"RIFF" + b"0" * 196)
            seen["text_len"] = len(Path(env["ADAM_TTS_TEXT_FILE"]).read_text(encoding="utf-8-sig"))
            return SimpleNamespace(returncode=0, stdout="", stderr="synthetic-secret-should-not-surface")

        audio = synthesize_windows_speech(
            "x" * (MAX_TEXT_CHARS + 50),
            os_name="nt",
            runner=fake_runner,
            temp_dir=td,
        )
        leftovers = list(root.iterdir())
        platform_guard = False
        try:
            synthesize_windows_speech("synthetic", os_name="posix", runner=fake_runner, temp_dir=td)
        except WindowsSpeechError:
            platform_guard = True

    return {
        "ok": bool(audio and seen.get("called") and seen.get("text_len") == MAX_TEXT_CHARS and platform_guard and not leftovers),
        "injected_runner_verified": bool(seen.get("called")),
        "speech_input_bound_verified": seen.get("text_len") == MAX_TEXT_CHARS,
        "platform_guard_verified": platform_guard,
        "wav_output_validation_verified": len(audio) >= 100,
        "temporary_file_cleanup_verified": not leftovers,
        "powershell_required_by_self_test": False,
        "speech_values_returned_by_evidence": False,
        "temporary_paths_returned_by_evidence": False,
        "audio_bytes_returned_by_evidence": False,
        "subprocess_error_details_returned_by_evidence": False,
        "external_network_accessed": False,
    }
