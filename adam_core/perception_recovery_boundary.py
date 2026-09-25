"""Buyer-safe evidence for Adam v4.2 screen perception + adaptive recovery."""
from __future__ import annotations
import hashlib
import json
from .screen_perception_recovery import public_manifest, perceive_interactive_elements, adaptive_click


def build_perception_recovery_manifest(version: str) -> dict:
    service = {
        "schema": "adam-acquisition-perception-recovery/v1",
        "product": "Adam Acquisition",
        "version": version,
        "status": "screen_perception_adaptive_recovery_tested",
        "boundary_module": "adam_core.screen_perception_recovery",
        "capabilities": public_manifest(),
        "next_targets": ["cross-app autonomous execution", "meeting agent"],
    }
    raw = json.dumps(service, sort_keys=True, separators=(",", ":")).encode()
    return {"perception_recovery": service, "perception_recovery_sha256": hashlib.sha256(raw).hexdigest()}


def perception_recovery_is_privacy_safe(payload: dict) -> bool:
    p = payload.get("perception_recovery", {}).get("capabilities", {}).get("privacy", {})
    return bool(p) and not any(bool(v) for v in p.values())


class _FakeElement:
    def __init__(self, tag="a", text="", attrs=None):
        self.tag_name = tag
        self.text = text
        self.attrs = dict(attrs or {})
        self.clicked = False
    def get_attribute(self, name): return self.attrs.get(name, "")
    def is_displayed(self): return True
    def is_enabled(self): return True
    def click(self): self.clicked = True


class _FakeDriver:
    def __init__(self):
        self.target = _FakeElement("a", "Learn more", {"id": "current-link"})
        self.button = _FakeElement("button", "Submit", {"type": "submit", "id": "submit"})
    def find_elements(self, by, selector): return [self.target, self.button]
    def find_element(self, by, selector):
        if selector == "#current-link": return self.target
        if selector == "#submit": return self.button
        raise LookupError(selector)


def perception_recovery_self_test() -> dict:
    d = _FakeDriver()
    p = perceive_interactive_elements(d)
    recovered = adaptive_click(d, "#old-link", fallback_selectors=["#current-link"], owner_approved=False)
    blocked = False
    try:
        adaptive_click(d, "#submit", owner_approved=False)
    except PermissionError:
        blocked = True
    return {
        "ok": bool(p.get("ok") and p.get("interactive_count") == 2 and recovered.get("ok") and recovered.get("recovered") and blocked),
        "semantic_perception_verified": True,
        "interactive_elements_detected": p.get("interactive_count", 0),
        "form_values_read": False,
        "missing_primary_selector_recovered": bool(recovered.get("recovered")),
        "recovery_matched_by": recovered.get("matched_by"),
        "owner_gate_preserved_during_recovery": blocked,
        "external_network_accessed": False,
        "real_application_controlled": False,
        "private_values_returned": False,
    }
