"""Bounded local configuration persistence for Adam Acquisition.

Keeps secret-bearing configuration behind an injected path while public projections
return configuration state only, never secret values.
"""
from __future__ import annotations
import json, os, tempfile
from pathlib import Path

MAX_CONFIG_BYTES = 64 * 1024
ALLOWED_AI_KEYS = ("api_base", "api_key", "model")

def normalize_ai_api_base(value):
    """Return a provider API root, not a concrete completion endpoint.

    Older Adam builds/users may have saved a full endpoint such as
    https://api.openai.com/v1/chat/completions. New transports append their own
    endpoint, so retaining that suffix would create an invalid URL.
    """
    base = str(value or "").strip().rstrip("/")
    low = base.lower()
    for suffix in ("/chat/completions", "/responses", "/completions"):
        if low.endswith(suffix):
            base = base[:-len(suffix)].rstrip("/")
            low = base.lower()
            break
    if low in {"https://api.openai.com", "http://api.openai.com"}:
        base += "/v1"
    return base

def load_ai_settings(path, *, environ=None):
    env = os.environ if environ is None else environ
    settings={"api_base":normalize_ai_api_base(env.get("AI_API_BASE","")),"api_key":str(env.get("AI_API_KEY","")).strip(),"model":str(env.get("AI_MODEL","")).strip()}
    p=Path(path)
    try:
        if p.exists() and p.stat().st_size <= MAX_CONFIG_BYTES:
            stored=json.loads(p.read_text(encoding="utf-8"))
            if isinstance(stored,dict):
                for k in ALLOWED_AI_KEYS:
                    if stored.get(k): settings[k]=str(stored[k]).strip()
    except Exception: pass
    settings["api_base"]=normalize_ai_api_base(settings["api_base"])
    return settings

def save_ai_settings(path, api_base, api_key, model):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    record={"api_base":normalize_ai_api_base(api_base),"api_key":str(api_key or "").strip(),"model":str(model or "").strip()}
    raw=json.dumps(record,indent=2).encode("utf-8")
    if len(raw)>MAX_CONFIG_BYTES: raise ValueError("Configuration exceeds size limit.")
    fd,tmp=tempfile.mkstemp(prefix=p.name+".",suffix=".tmp",dir=str(p.parent))
    try:
        with os.fdopen(fd,"wb") as f: f.write(raw); f.flush(); os.fsync(f.fileno())
        os.replace(tmp,p)
    finally:
        try:
            if os.path.exists(tmp): os.unlink(tmp)
        except OSError: pass
    return record

def public_ai_status(settings):
    s=settings or {}
    return {"api_base_configured":bool(s.get("api_base")),"api_key_configured":bool(s.get("api_key")),"model_configured":bool(s.get("model")),"configuration_complete":all(bool(s.get(k)) for k in ALLOWED_AI_KEYS)}
