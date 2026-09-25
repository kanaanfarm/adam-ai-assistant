"""Central runtime environment configuration for Adam Acquisition.

This module consolidates environment reads behind small typed helpers while
never exposing secret values through buyer-facing evidence.
"""
from __future__ import annotations
import os

DEFAULT_OPENAI_BASE = "https://api.openai.com/v1"
DEFAULT_OPENAI_MODEL = "gpt-5.6"


def _env(name: str, environ=None) -> str:
    source = os.environ if environ is None else environ
    return str(source.get(name, "") or "").strip()


def openai_environment(environ=None):
    return {
        "api_key": _env("OPENAI_API_KEY", environ),
        "api_base": (_env("OPENAI_API_BASE", environ) or DEFAULT_OPENAI_BASE).rstrip("/"),
        "model": _env("OPENAI_MODEL", environ) or DEFAULT_OPENAI_MODEL,
    }


def vision_model_environment(environ=None) -> str:
    return _env("AI_VISION_MODEL", environ)


def alpaca_environment(environ=None):
    # Preserve both historical secret variable names without exposing either.
    secret = _env("ALPACA_SECRET_KEY", environ) or _env("ALPACA_API_SECRET", environ)
    return {"api_key": _env("ALPACA_API_KEY", environ), "secret_key": secret}


def microsoft_client_id_environment(environ=None) -> str:
    return _env("MICROSOFT_CLIENT_ID", environ)


def public_runtime_status(environ=None):
    ai = openai_environment(environ)
    alpaca = alpaca_environment(environ)
    return {
        "openai_api_key_configured": bool(ai["api_key"]),
        "openai_api_base_configured": bool(_env("OPENAI_API_BASE", environ)),
        "openai_model_configured": bool(_env("OPENAI_MODEL", environ)),
        "vision_model_configured": bool(vision_model_environment(environ)),
        "alpaca_api_key_configured": bool(alpaca["api_key"]),
        "alpaca_secret_configured": bool(alpaca["secret_key"]),
        "microsoft_client_id_configured": bool(microsoft_client_id_environment(environ)),
    }
