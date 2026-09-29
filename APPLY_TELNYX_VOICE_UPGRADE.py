#!/usr/bin/env python3
from pathlib import Path
import shutil

root = Path(__file__).resolve().parent
app_path = root / "app.py"
if not app_path.exists():
    raise SystemExit("app.py not found. Put this package in the ADAM repository root.")
text = app_path.read_text(encoding="utf-8")
backup = root / "app.py.before_telnyx_two_way_voice"
if not backup.exists():
    shutil.copy2(app_path, backup)

anchor = "from adam_core.telnyx_outbound import create_outbound_call as telnyx_create_outbound_call, readiness as telnyx_readiness, TelnyxCallError\n"
new_import = "from adam_core.telnyx_conversation import speak as telnyx_live_speak, start_transcription as telnyx_live_start_transcription, webhook_token_valid as telnyx_webhook_token_valid\n"
if new_import not in text:
    if anchor not in text:
        raise SystemExit("Telnyx outbound import anchor not found; no changes made.")
    text = text.replace(anchor, anchor + new_import, 1)

route_marker = "# ADAM TELNYX TWO-WAY VOICE V1"
routes = '# ADAM TELNYX TWO-WAY VOICE V1\n_TELNYX_LIVE_CALLS = {}\n_TELNYX_LIVE_CALLS_LOCK = threading.Lock()\n\ndef _telnyx_event_v1(body):\n    data = (body or {}).get("data") or {}\n    return str(data.get("event_type") or ""), (data.get("payload") or {})\n\ndef _telnyx_transcript_v1(payload):\n    td = payload.get("transcription_data") or {}\n    text = str(td.get("transcript") or payload.get("transcript") or "").strip()\n    final_value = td.get("is_final")\n    if final_value is None:\n        final_value = payload.get("is_final", True)\n    return text, bool(final_value)\n\ndef _telnyx_live_ai_reply_v1(user_text):\n    prompt = (\n        "You are ADAM speaking on a live telephone call. "\n        "Reply naturally and briefly, normally one or two sentences. "\n        "Do not claim an action was completed unless it really was. "\n        "If the caller asks for a consequential external action, explain that owner approval is required. "\n        "Caller said: " + str(user_text or "")[:2500]\n    )\n    return str(call_ai(prompt, "English", max_tokens=180, timeout=20, reasoning_effort="low") or "").strip()\n\n@app.post("/api/telnyx/voice/webhook")\ndef telnyx_voice_webhook_v1():\n    if not telnyx_webhook_token_valid(request.args.get("token") or ""):\n        return jsonify({"ok": False, "status": "invalid_webhook_token"}), 401\n    body = request.get_json(silent=True) or {}\n    event_type, payload = _telnyx_event_v1(body)\n    call_control_id = str(payload.get("call_control_id") or "").strip()\n    if not event_type:\n        return jsonify({"ok": True, "status": "ignored_empty_event"}), 200\n    try:\n        if event_type == "call.answered" and call_control_id:\n            with _TELNYX_LIVE_CALLS_LOCK:\n                state = _TELNYX_LIVE_CALLS.setdefault(call_control_id, {})\n                if state.get("answered_initialized"):\n                    return jsonify({"ok": True, "status": "duplicate_answer_ignored"}), 200\n                state["answered_initialized"] = True\n            telnyx_live_start_transcription(call_control_id)\n            telnyx_live_speak(call_control_id, "Hello, this is ADAM. I can hear you now. Please speak after this message.")\n            return jsonify({"ok": True, "status": "live_voice_started"}), 200\n\n        if event_type == "call.transcription" and call_control_id:\n            transcript, is_final = _telnyx_transcript_v1(payload)\n            if not is_final or not transcript:\n                return jsonify({"ok": True, "status": "interim_transcription_ignored"}), 200\n            transcript_key = transcript.strip().lower()\n            with _TELNYX_LIVE_CALLS_LOCK:\n                state = _TELNYX_LIVE_CALLS.setdefault(call_control_id, {})\n                if state.get("last_transcript") == transcript_key:\n                    return jsonify({"ok": True, "status": "duplicate_transcript_ignored"}), 200\n                state["last_transcript"] = transcript_key\n            reply = _telnyx_live_ai_reply_v1(transcript) or "I heard you, but I could not prepare a response. Please try again."\n            telnyx_live_speak(call_control_id, reply)\n            return jsonify({"ok": True, "status": "live_voice_reply_sent", "transcript_received": True}), 200\n\n        if event_type == "call.hangup" and call_control_id:\n            with _TELNYX_LIVE_CALLS_LOCK:\n                _TELNYX_LIVE_CALLS.pop(call_control_id, None)\n            return jsonify({"ok": True, "status": "live_voice_call_closed"}), 200\n\n        return jsonify({"ok": True, "status": "event_acknowledged", "event_type": event_type}), 200\n    except Exception as exc:\n        try:\n            audit("TELNYX_LIVE_CALL_ERROR_V1", {"event_type": event_type, "error": str(exc)[:300]})\n        except Exception:\n            pass\n        return jsonify({"ok": False, "status": "live_voice_processing_error"}), 200\n\n@app.get("/api/telnyx/voice/readiness")\ndef telnyx_voice_readiness_v1():\n    return jsonify({\n        "ok": True,\n        "two_way_voice_code_installed": True,\n        "webhook_token_configured": bool(str(os.getenv("TELNYX_WEBHOOK_TOKEN", "")).strip()),\n        "stt_language": str(os.getenv("TELNYX_STT_LANGUAGE", "en")),\n        "tts_voice": str(os.getenv("TELNYX_TTS_VOICE", "Polly.Brian")),\n        "version": VERSION,\n    })\n'
if route_marker not in text:
    main_anchor = '\nif __name__ == "__main__":\n'
    if main_anchor not in text:
        raise SystemExit("__main__ anchor not found; no changes made.")
    text = text.replace(main_anchor, "\n" + routes + "\n" + main_anchor, 1)

app_path.write_text(text, encoding="utf-8")
print("ADAM Telnyx two-way voice upgrade applied successfully.")
print("Backup:", backup.name)
