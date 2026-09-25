"""WhatsApp configuration and webhook service boundary for Adam Acquisition v2.0."""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path
import hashlib
import hmac
import json
import os
import re
import secrets

DEFAULT_API_VERSION = "v21.0"
ENV_MAP = {
    "access_token": "WHATSAPP_ACCESS_TOKEN",
    "phone_number_id": "WHATSAPP_PHONE_NUMBER_ID",
    "business_account_id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
    "api_version": "WHATSAPP_API_VERSION",
    "verify_token": "WHATSAPP_VERIFY_TOKEN",
    "app_secret": "WHATSAPP_APP_SECRET",
}


def load_config(path: Path, env=None):
    env = os.environ if env is None else env
    cfg = {}
    path = Path(path)
    if path.exists():
        try:
            cfg = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            cfg = {}
    for key, env_name in ENV_MAP.items():
        value = str(env.get(env_name, "") or "").strip()
        if value:
            cfg[key] = value
    if not cfg.get("api_version"):
        cfg["api_version"] = DEFAULT_API_VERSION
    return cfg


def save_config(path: Path, data, *, existing=None, verify_token_factory=None):
    path = Path(path)
    if existing is None:
        existing = {}
        if path.exists():
            try:
                existing = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                existing = {}
    verify_token_factory = verify_token_factory or (lambda: secrets.token_urlsafe(32))
    token = str((data or {}).get("access_token") or "").strip() or str(existing.get("access_token") or "")
    cfg = {
        "access_token": token,
        "phone_number_id": str((data or {}).get("phone_number_id") or existing.get("phone_number_id") or "").strip(),
        "business_account_id": str((data or {}).get("business_account_id") or existing.get("business_account_id") or "").strip(),
        "api_version": str((data or {}).get("api_version") or existing.get("api_version") or DEFAULT_API_VERSION).strip(),
        "verify_token": str((data or {}).get("verify_token") or existing.get("verify_token") or "").strip(),
        "app_secret": str((data or {}).get("app_secret") or existing.get("app_secret") or "").strip(),
    }
    if not cfg["verify_token"]:
        cfg["verify_token"] = verify_token_factory()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")
    return cfg


def public_status(cfg):
    cfg = cfg or {}
    return {
        "configured": bool(cfg.get("access_token") and cfg.get("phone_number_id")),
        "phone_number_id": cfg.get("phone_number_id", ""),
        "business_account_id": cfg.get("business_account_id", ""),
        "api_version": cfg.get("api_version", DEFAULT_API_VERSION),
        "token_saved": bool(cfg.get("access_token")),
        "verify_token_saved": bool(cfg.get("verify_token")),
        "app_secret_saved": bool(cfg.get("app_secret")),
    }


def normalize_number(value):
    digits = re.sub(r"\D+", "", str(value or ""))
    if digits.startswith("00"):
        digits = digits[2:]
    return digits


def verify_challenge(*, mode, supplied_token, challenge, expected_token):
    ok = bool(mode == "subscribe" and expected_token and secrets.compare_digest(str(supplied_token or ""), str(expected_token)))
    return {"ok": ok, "challenge": str(challenge or "") if ok else ""}


def verify_signature(*, app_secret, raw_body, supplied_signature):
    if not app_secret:
        return True
    expected = "sha256=" + hmac.new(str(app_secret).encode("utf-8"), raw_body or b"", hashlib.sha256).hexdigest()
    return hmac.compare_digest(str(supplied_signature or ""), expected)


def project_incoming_messages(event, *, received_at_utc):
    records = []
    event = event or {}
    for entry in event.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {}) or {}
            contacts = value.get("contacts", []) or []
            contact_name = ""
            if contacts:
                contact_name = ((contacts[0].get("profile") or {}).get("name") or "")
            for message in value.get("messages", []) or []:
                records.append({
                    "id": message.get("id", ""),
                    "from": message.get("from", ""),
                    "contact_name": contact_name,
                    "timestamp": message.get("timestamp", ""),
                    "type": message.get("type", ""),
                    "text": ((message.get("text") or {}).get("body") or ""),
                    "received_at_utc": received_at_utc,
                })
    return records


def append_jsonl(path: Path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def public_boundary_state(cfg):
    cfg = cfg or {}
    return {
        "configured": bool(cfg.get("access_token") and cfg.get("phone_number_id")),
        "api_version": cfg.get("api_version", DEFAULT_API_VERSION),
        "token_saved": bool(cfg.get("access_token")),
        "verify_token_saved": bool(cfg.get("verify_token")),
        "app_secret_saved": bool(cfg.get("app_secret")),
    }
