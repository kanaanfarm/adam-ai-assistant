"""Screen perception and adaptive browser recovery for Adam Acquisition v4.2.

This service builds a bounded semantic view of the current browser page without
reading form values or credentials. It can recover from a missing CSS selector
by trying explicit fallback selectors or a bounded visible-text match.
Consequential controls remain owner-gated at the moment of click.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Iterable

MAX_INTERACTIVE_ELEMENTS = 80
MAX_ELEMENT_TEXT_CHARS = 160
MAX_TEXT_HINT_CHARS = 200
MAX_FALLBACK_SELECTORS = 8


class PerceptionRecoveryError(RuntimeError):
    pass


def _clean(value: Any, limit: int) -> str:
    return " ".join(str(value or "").split())[:limit]


def _consequential(tag: str, typ: str, role: str) -> bool:
    tag = (tag or "").lower()
    typ = (typ or "").lower()
    role = (role or "").lower()
    return tag == "button" or typ in {"submit", "button", "reset"} or role == "button"


def _selector_for(el: Any) -> str:
    """Generate a bounded best-effort selector without using field values."""
    try:
        element_id = _clean(el.get_attribute("id"), 120)
        if element_id and all(c.isalnum() or c in "-_" for c in element_id):
            return f"#{element_id}"
        name = _clean(el.get_attribute("name"), 120)
        tag = _clean(getattr(el, "tag_name", ""), 30).lower() or "*"
        if name and all(c.isalnum() or c in "-_" for c in name):
            return f'{tag}[name="{name}"]'
        data_target = _clean(el.get_attribute("data-adam-target"), 120)
        if data_target and all(c.isalnum() or c in "-_" for c in data_target):
            return f'[data-adam-target="{data_target}"]'
        return tag
    except Exception:
        return "*"


@dataclass
class PerceivedElement:
    tag: str
    type: str
    role: str
    text: str
    aria_label: str
    placeholder: str
    selector: str
    enabled: bool
    displayed: bool
    consequential: bool

    def to_dict(self) -> dict:
        return {
            "tag": self.tag,
            "type": self.type,
            "role": self.role,
            "text": self.text,
            "aria_label": self.aria_label,
            "placeholder": self.placeholder,
            "selector": self.selector,
            "enabled": self.enabled,
            "displayed": self.displayed,
            "consequential": self.consequential,
        }


def perceive_interactive_elements(driver: Any) -> dict:
    try:
        raw = driver.find_elements(
            "css selector",
            "a,button,input,select,textarea,[role='button'],[onclick]",
        )
    except Exception as exc:
        raise PerceptionRecoveryError("Could not inspect interactive page elements.") from exc

    items: list[PerceivedElement] = []
    for el in list(raw or [])[:MAX_INTERACTIVE_ELEMENTS]:
        try:
            tag = _clean(getattr(el, "tag_name", ""), 30).lower()
            typ = _clean(el.get_attribute("type"), 30).lower()
            role = _clean(el.get_attribute("role"), 30).lower()
            # Never call get_attribute('value'). User-entered values remain private.
            text = _clean(getattr(el, "text", ""), MAX_ELEMENT_TEXT_CHARS)
            aria = _clean(el.get_attribute("aria-label"), MAX_ELEMENT_TEXT_CHARS)
            placeholder = _clean(el.get_attribute("placeholder"), MAX_ELEMENT_TEXT_CHARS)
            displayed = bool(el.is_displayed()) if hasattr(el, "is_displayed") else True
            enabled = bool(el.is_enabled()) if hasattr(el, "is_enabled") else True
            if not displayed:
                continue
            items.append(PerceivedElement(
                tag=tag,
                type=typ,
                role=role,
                text=text,
                aria_label=aria,
                placeholder=placeholder,
                selector=_selector_for(el),
                enabled=enabled,
                displayed=displayed,
                consequential=_consequential(tag, typ, role),
            ))
        except Exception:
            continue

    return {
        "ok": True,
        "action": "perceive",
        "interactive_count": len(items),
        "elements": [x.to_dict() for x in items],
        "bounds": {"max_interactive_elements": MAX_INTERACTIVE_ELEMENTS},
        "input_values_read": False,
    }


def _safe_fallbacks(selectors: Iterable[str] | None) -> list[str]:
    result = []
    for raw in list(selectors or [])[:MAX_FALLBACK_SELECTORS]:
        value = _clean(raw, 500)
        if value and value not in result:
            result.append(value)
    return result


def adaptive_click(
    driver: Any,
    primary_selector: str,
    *,
    fallback_selectors: Iterable[str] | None = None,
    text_hint: str = "",
    owner_approved: bool = False,
) -> dict:
    """Click with bounded selector/text recovery while preserving owner approval."""
    primary = _clean(primary_selector, 500)
    hint = _clean(text_hint, MAX_TEXT_HINT_CHARS)
    selectors = ([primary] if primary else []) + _safe_fallbacks(fallback_selectors)
    attempts = 0
    target = None
    matched_by = ""

    for selector in selectors:
        attempts += 1
        try:
            target = driver.find_element("css selector", selector)
            matched_by = "primary_selector" if selector == primary and attempts == 1 else "fallback_selector"
            break
        except Exception:
            continue

    if target is None and hint:
        try:
            candidates = driver.find_elements(
                "css selector",
                "a,button,input[type='button'],input[type='submit'],[role='button']",
            )
        except Exception as exc:
            raise PerceptionRecoveryError("Adaptive recovery could not inspect page controls.") from exc
        normalized_hint = hint.casefold()
        for el in list(candidates or [])[:MAX_INTERACTIVE_ELEMENTS]:
            attempts += 1
            try:
                visible = _clean(getattr(el, "text", ""), MAX_ELEMENT_TEXT_CHARS)
                aria = _clean(el.get_attribute("aria-label"), MAX_ELEMENT_TEXT_CHARS)
                candidate = f"{visible} {aria}".strip().casefold()
                if candidate and normalized_hint in candidate:
                    target = el
                    matched_by = "visible_text_hint"
                    break
            except Exception:
                continue

    if target is None:
        return {
            "ok": False,
            "action": "adaptive_click",
            "recovered": False,
            "attempts": attempts,
            "reason": "target_not_found",
            "text_hint_used": bool(hint),
            "selector_candidates_tried": len(selectors),
        }

    tag = _clean(getattr(target, "tag_name", ""), 30).lower()
    typ = _clean(target.get_attribute("type"), 30).lower()
    role = _clean(target.get_attribute("role"), 30).lower()
    consequential = _consequential(tag, typ, role)
    if consequential and owner_approved is not True:
        raise PermissionError("Explicit owner approval is required before adaptive-clicking a consequential control.")

    try:
        target.click()
    except Exception as exc:
        raise PerceptionRecoveryError("Recovered target could not be clicked.") from exc

    return {
        "ok": True,
        "action": "adaptive_click",
        "recovered": matched_by != "primary_selector",
        "matched_by": matched_by,
        "attempts": attempts,
        "consequential_control": consequential,
        "text_hint_used": bool(hint),
    }


def public_manifest() -> dict:
    return {
        "semantic_page_perception": True,
        "interactive_element_inventory": True,
        "adaptive_selector_recovery": True,
        "visible_text_hint_recovery": True,
        "owner_gate_preserved_during_recovery": True,
        "bounds": {
            "max_interactive_elements": MAX_INTERACTIVE_ELEMENTS,
            "max_element_text_chars": MAX_ELEMENT_TEXT_CHARS,
            "max_text_hint_chars": MAX_TEXT_HINT_CHARS,
            "max_fallback_selectors": MAX_FALLBACK_SELECTORS,
        },
        "privacy": {
            "form_values_read": False,
            "credentials_exposed_in_buyer_evidence": False,
            "page_contents_exposed_in_buyer_evidence": False,
            "urls_exposed_in_buyer_evidence": False,
            "typed_values_exposed_in_buyer_evidence": False,
        },
    }
