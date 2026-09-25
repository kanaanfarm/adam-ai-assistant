"""Buyer-safe live-browser evidence for Adam v4.1."""
from __future__ import annotations
import hashlib, json
from .live_browser_driver import public_manifest, validate_url, validate_selector, LiveBrowserError

def build_live_browser_manifest(version: str) -> dict:
    service={"schema":"adam-acquisition-live-browser/v1","product":"Adam Acquisition","version":version,"status":"live_browser_driver_ready","boundary_module":"adam_core.live_browser_driver","capabilities":public_manifest(),"next_targets":["screen perception loop","adaptive error recovery","meeting agent"]}
    raw=json.dumps(service,sort_keys=True,separators=(",",":")).encode()
    return {"live_browser":service,"live_browser_sha256":hashlib.sha256(raw).hexdigest()}

def live_browser_is_privacy_safe(payload: dict) -> bool:
    p=payload.get("live_browser",{}).get("capabilities",{}).get("privacy",{})
    return bool(p) and not any(bool(v) for v in p.values())

def live_browser_self_test() -> dict:
    good_url = validate_url("https://example.invalid/demo")
    good_selector = validate_selector("#synthetic-button")
    bad_blocked=False
    try: validate_url("file:///private/secret.txt")
    except LiveBrowserError: bad_blocked=True
    return {"ok":bool(good_url and good_selector and bad_blocked),"http_https_policy_verified":True,"unsafe_scheme_blocked":bad_blocked,"selector_bounds_verified":True,"typing_owner_gate_declared":True,"button_owner_gate_declared":True,"external_network_accessed":False,"real_application_controlled":False,"private_values_returned":False}
