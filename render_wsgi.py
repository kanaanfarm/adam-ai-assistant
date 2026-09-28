"""Owner login for the temporary Render deployment of Adam."""
import hashlib
import hmac
import os
import secrets
import time
from threading import Lock

from flask import abort, redirect, render_template_string, request, session, url_for
from app import app

app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SECURE=True,
                  SESSION_COOKIE_SAMESITE="Lax", PERMANENT_SESSION_LIFETIME=12 * 60 * 60)
_failures = {}
_failure_lock = Lock()

_login_page = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Adam AI Assistant · Owner login</title><style>
body{font:16px system-ui,sans-serif;background:#f4f6fa;color:#172032;margin:0;min-height:100vh;display:grid;place-items:center}
main{width:min(420px,calc(100vw - 48px));background:white;border-radius:16px;padding:32px;box-shadow:0 12px 32px #14203920}
h1{font-size:24px;margin:0 0 6px}p{color:#526078;margin:0 0 24px}label{display:block;margin:16px 0 6px;font-weight:600}
input[type=text],input[type=password]{box-sizing:border-box;width:100%;font:inherit;border:1px solid #aeb9c9;border-radius:8px;padding:12px}
.show{display:flex;align-items:center;gap:8px;margin:12px 0 20px}.show label{margin:0;font-weight:400}
button{width:100%;background:#2244a4;color:white;border:0;border-radius:8px;padding:12px;font:inherit;cursor:pointer}
.error{color:#a22020;margin:0 0 12px}</style></head><body><main>
<h1>Adam AI Assistant</h1><p>Owner sign in</p>
{% if error %}<div class="error" role="alert">{{ error }}</div>{% endif %}
<form method="post" action="{{ url_for('owner_login') }}">
<input type="hidden" name="csrf" value="{{ csrf }}"><input type="hidden" name="next" value="{{ next_path }}">
<label for="username">Username</label><input id="username" name="username" type="text" autocomplete="username" required>
<label for="password">Password</label><input id="password" name="password" type="password" autocomplete="current-password" required>
<div class="show"><input id="show" type="checkbox"><label for="show">Show password</label></div>
<button type="submit">Sign in</button></form></main>
<script>document.getElementById('show').addEventListener('change',function(){document.getElementById('password').type=this.checked?'text':'password'})</script>
</body></html>"""

def _safe_next(value):
    return value if value and value.startswith("/") and not value.startswith("//") else "/"

def _password_fingerprint(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

@app.before_request
def require_owner_login():
    password = os.environ.get("ADAM_OWNER_PASSWORD", "")
    if len(password) < 20:
        return "Owner password is not configured (minimum 20 characters).", 503
    if request.path == "/owner-login":
        return None
    if hmac.compare_digest(str(session.get("owner_auth", "")), _password_fingerprint(password)):
        return None
    if request.method == "GET" and not request.path.startswith("/api/"):
        return redirect(url_for("owner_login", next=request.full_path.rstrip("?")))
    abort(401)

@app.route("/owner-login", methods=["GET", "POST"])
def owner_login():
    next_path = _safe_next(request.values.get("next", "/"))
    error = ""
    if request.method == "POST":
        token = str(session.get("login_csrf", ""))
        if not token or not hmac.compare_digest(str(request.form.get("csrf", "")), token):
            abort(400)
        remote = request.remote_addr or "unknown"
        now = time.monotonic()
        with _failure_lock:
            attempts = [t for t in _failures.get(remote, []) if now - t < 300]
            _failures[remote] = attempts
            blocked = len(attempts) >= 10
        if blocked:
            error = "Too many attempts. Try again in a few minutes."
        else:
            expected_user = os.environ.get("ADAM_OWNER_USER", "adam")
            expected_password = os.environ.get("ADAM_OWNER_PASSWORD", "")
            valid = hmac.compare_digest(request.form.get("username", ""), expected_user)
            valid &= hmac.compare_digest(request.form.get("password", ""), expected_password)
            if valid:
                session.clear()
                session.permanent = True
                session["owner_auth"] = _password_fingerprint(expected_password)
                with _failure_lock:
                    _failures.pop(remote, None)
                return redirect(next_path)
            with _failure_lock:
                _failures.setdefault(remote, []).append(now)
            error = "Incorrect username or password."
    session.setdefault("login_csrf", secrets.token_urlsafe(32))
    response = app.make_response(render_template_string(_login_page, error=error,
                                                       csrf=session["login_csrf"], next_path=next_path))
    response.headers["Cache-Control"] = "no-store"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response
