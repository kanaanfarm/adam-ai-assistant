#!/usr/bin/env python3
from pathlib import Path

p = Path(__file__).resolve().parent / "app.py"
text = p.read_text(encoding="utf-8")
backup = p.with_name("app.py.before_telnyx_stt_diagnostics_v5")
if not backup.exists():
    backup.write_text(text, encoding="utf-8")

old = '''    call_control_id = str(payload.get("call_control_id") or "").strip()\n    try:\n'''
new = '''    call_control_id = str(payload.get("call_control_id") or "").strip()\n    # TELNYX V5 diagnostics: log event metadata only; never log webhook token.\n    td_debug = payload.get("transcription_data") or {}\n    transcript_debug = str(td_debug.get("transcript") or payload.get("transcript") or "").strip()\n    print(\n        f"TELNYX_WEBHOOK_EVENT event={event_type or 'unknown'} "\n        f"call_present={bool(call_control_id)} "\n        f"transcription_data_present={bool(td_debug)} "\n        f"transcript_chars={len(transcript_debug)} "\n        f"is_final={td_debug.get('is_final', payload.get('is_final', 'n/a'))}",\n        flush=True,\n    )\n    try:\n'''
if "TELNYX_WEBHOOK_EVENT event=" not in text:
    if old not in text:
        raise SystemExit("Expected Telnyx webhook insertion point not found; no changes made.")
    text = text.replace(old, new, 1)

old2 = '''        "stt_language": str(os.getenv("TELNYX_STT_LANGUAGE", "en")),\n        "tts_language": str(os.getenv("TELNYX_TTS_LANGUAGE", "en-US")),\n'''
new2 = '''        "stt_language": str(os.getenv("TELNYX_STT_LANGUAGE", "en")),\n        "stt_track": str(os.getenv("TELNYX_STT_TRACK", "inbound")).strip().lower() or "inbound",\n        "stt_engine": str(os.getenv("TELNYX_STT_ENGINE", "Google")).strip() or "Google",\n        "tts_language": str(os.getenv("TELNYX_TTS_LANGUAGE", "en-US")),\n'''
if '"stt_track": str(os.getenv("TELNYX_STT_TRACK"' not in text:
    if old2 not in text:
        raise SystemExit("Expected readiness insertion point not found; no changes made.")
    text = text.replace(old2, new2, 1)

p.write_text(text, encoding="utf-8")
print("V5 Telnyx STT diagnostics applied successfully to app.py")
print("Backup:", backup.name)
