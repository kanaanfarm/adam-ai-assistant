"""Adam v8.2.0.4 Guest Voice-only public gateway.

This gateway intentionally exposes only temporary Guest Voice routes to a
trusted HTTPS tunnel. The owner UI, connectors, files, contacts, email,
trading, and all other Adam routes are not reachable through this port.
"""
from __future__ import annotations

import os
from flask import Flask, Response, request
import requests

UPSTREAM = os.getenv("ADAM_OWNER_UPSTREAM", "http://127.0.0.1:8770").rstrip("/")
TIMEOUT = 75
app = Flask(__name__)


def _forward(path: str) -> Response:
    url = UPSTREAM + path
    headers = {}
    for key in ("Content-Type", "Accept", "User-Agent", "X-Adam-Guest-Token"):
        if request.headers.get(key):
            headers[key] = request.headers[key]
    try:
        resp = requests.request(
            request.method,
            url,
            params=request.args,
            data=request.get_data(),
            headers=headers,
            timeout=TIMEOUT,
            allow_redirects=False,
        )
    except requests.RequestException as exc:
        return Response(f"Guest gateway upstream unavailable: {exc}", status=502, content_type="text/plain")
    excluded = {"content-encoding", "content-length", "transfer-encoding", "connection"}
    out_headers = [(k, v) for k, v in resp.headers.items() if k.lower() not in excluded]
    out_headers.extend([
        ("Cache-Control", "no-store"),
        ("X-Content-Type-Options", "nosniff"),
        ("Referrer-Policy", "no-referrer"),
        ("Permissions-Policy", "microphone=(self)"),
    ])
    return Response(resp.content, status=resp.status_code, headers=out_headers)


def _active_token(token: str) -> bool:
    if not token or len(token) < 20:
        return False
    try:
        r = requests.get(
            f"{UPSTREAM}/api/personal-assistant/guest-voice/sessions/{token}",
            timeout=8,
        )
        if not r.ok:
            return False
        data = r.json()
        return bool(data.get("ok") and data.get("active"))
    except Exception:
        return False


@app.get("/health")
def health():
    return {"ok": True, "service": "adam_guest_voice_gateway", "owner_ui_exposed": False}


@app.route("/guest/<token>", methods=["GET"])
def guest_page(token: str):
    if not _active_token(token):
        return Response("Guest session unavailable", status=410)
    return _forward(f"/guest/{token}")


@app.route("/api/personal-assistant/guest-voice/sessions/<token>", methods=["GET"])
def guest_status(token: str):
    return _forward(f"/api/personal-assistant/guest-voice/sessions/{token}")


@app.route("/api/personal-assistant/guest-voice/sessions/<token>/ask", methods=["POST"])
def guest_ask(token: str):
    if not _active_token(token):
        return Response("Guest session unavailable", status=410)
    return _forward(f"/api/personal-assistant/guest-voice/sessions/{token}/ask")


@app.route("/api/personal-assistant/guest-voice/sessions/<token>/transcribe", methods=["POST"])
def guest_transcribe(token: str):
    if not _active_token(token):
        return Response("Guest session unavailable", status=410)
    # Preserve multipart form upload exactly enough for Flask upstream.
    audio = request.files.get("audio")
    if not audio:
        return Response("audio_required", status=400)
    try:
        files = {"audio": (audio.filename or "guest-voice.webm", audio.stream, audio.mimetype or "application/octet-stream")}
        r = requests.post(
            f"{UPSTREAM}/api/personal-assistant/guest-voice/sessions/{token}/transcribe",
            files=files,
            timeout=TIMEOUT,
        )
    except requests.RequestException as exc:
        return Response(f"Guest gateway upstream unavailable: {exc}", status=502)
    return Response(r.content, status=r.status_code, content_type=r.headers.get("Content-Type", "application/json"), headers={"Cache-Control":"no-store"})


@app.route("/api/tts", methods=["POST"])
def guest_tts():
    token = (request.headers.get("X-Adam-Guest-Token") or "").strip()
    if not _active_token(token):
        return Response("guest_token_required", status=403)
    return _forward("/api/tts")


@app.errorhandler(404)
def blocked(_):
    return Response("Not available on Guest Voice gateway", status=404, headers={"X-Adam-Gateway-Scope":"guest_voice_only"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8771, debug=False, threaded=True)
