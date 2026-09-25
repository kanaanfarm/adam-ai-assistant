"""Microsoft identity persistence/session boundary for Adam Acquisition.

This module deliberately does not import Flask or MSAL. It owns the local
configuration/cache persistence and device-flow state projection so those
behaviors can be tested independently from external Microsoft credentials.
"""
from __future__ import annotations

import json
from pathlib import Path
import threading


class MicrosoftIdentityState:
    """Thread-safe projection of device-flow state without exposing tokens."""

    def __init__(self):
        self._lock = threading.Lock()
        self._flow = {}
        self._result = {}

    def set_waiting(self, flow):
        with self._lock:
            self._flow = dict(flow or {})
            self._result = {"status": "waiting"}

    def set_connected(self, username=""):
        with self._lock:
            self._flow = {}
            self._result = {"status": "connected", "username": str(username or "")}

    def set_error(self, error=""):
        with self._lock:
            self._flow = {}
            self._result = {"status": "error", "error": str(error or "")}

    def status(self):
        with self._lock:
            return dict(self._result) if self._result else {"status": "not_connected"}

    def reset(self):
        with self._lock:
            self._flow = {}
            self._result = {}

    def flow(self):
        with self._lock:
            return dict(self._flow)


def load_client_config(path, *, env_client_id=""):
    path = Path(path)
    cfg = {}
    if path.exists():
        try:
            loaded = json.loads(path.read_text(encoding="utf-8"))
            cfg = loaded if isinstance(loaded, dict) else {}
        except Exception:
            cfg = {}
    env_client_id = str(env_client_id or "").strip()
    if env_client_id and not cfg.get("client_id"):
        cfg["client_id"] = env_client_id
    return cfg


def save_client_config(path, client_id):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    value = str(client_id or "").strip()
    path.write_text(json.dumps({"client_id": value}, indent=2), encoding="utf-8")
    return {"client_id": value}


def load_serialized_cache(path):
    path = Path(path)
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def persist_serialized_cache(path, serialized):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(str(serialized or ""), encoding="utf-8")
    return True


def public_identity_state(*, client_configured=False, token_cache_present=False, device_status="not_connected"):
    """Return buyer-safe identity state; never includes IDs, usernames or tokens."""
    return {
        "client_configured": bool(client_configured),
        "token_cache_present": bool(token_cache_present),
        "device_status": str(device_status or "not_connected"),
    }
