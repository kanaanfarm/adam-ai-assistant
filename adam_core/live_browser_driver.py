"""Governed live browser driver for Adam Acquisition v4.1.

Uses an installed Chrome/Edge browser through Selenium. No browser is launched at
import time. The driver is intentionally explicit and bounded; consequential
button/form actions remain owner-gated by the caller.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlparse

MAX_TEXT_CHARS = 12000
MAX_SELECTOR_CHARS = 500
ALLOWED_SCHEMES = {"http", "https"}

class LiveBrowserError(RuntimeError): pass


def validate_url(url: str) -> str:
    value = str(url or "").strip()
    parsed = urlparse(value)
    if parsed.scheme not in ALLOWED_SCHEMES or not parsed.netloc:
        raise LiveBrowserError("Only absolute http/https URLs are allowed.")
    if len(value) > 2000:
        raise LiveBrowserError("URL exceeds safety bound.")
    return value


def validate_selector(selector: str) -> str:
    value = str(selector or "").strip()
    if not value or len(value) > MAX_SELECTOR_CHARS:
        raise LiveBrowserError("A bounded CSS selector is required.")
    return value


def selenium_available() -> bool:
    try:
        import selenium  # noqa:F401
        return True
    except Exception:
        return False

@dataclass
class BrowserObservation:
    title: str
    url_present: bool
    text: str

    def public_summary(self) -> dict:
        return {"title_present": bool(self.title), "url_present": bool(self.url_present), "text_present": bool(self.text), "text_chars": len(self.text)}

class SeleniumBrowserDriver:
    def __init__(self, *, browser: str = "edge", headless: bool = False):
        if not selenium_available():
            raise LiveBrowserError("Selenium is not installed. Run pip install -r requirements.txt.")
        from selenium import webdriver
        browser = (browser or "edge").strip().lower()
        try:
            if browser == "chrome":
                opts = webdriver.ChromeOptions()
                if headless: opts.add_argument("--headless=new")
                opts.add_argument("--disable-notifications")
                self.driver = webdriver.Chrome(options=opts)
            else:
                opts = webdriver.EdgeOptions()
                if headless: opts.add_argument("--headless=new")
                opts.add_argument("--disable-notifications")
                self.driver = webdriver.Edge(options=opts)
        except Exception as exc:
            raise LiveBrowserError("Could not start the local browser driver. Ensure Chrome or Edge is installed.") from exc

    def open_url(self, url: str) -> dict:
        self.driver.get(validate_url(url))
        return {"ok": True, "action": "open_url"}

    def observe(self) -> BrowserObservation:
        text = str(self.driver.find_element("tag name", "body").text or "")[:MAX_TEXT_CHARS]
        return BrowserObservation(str(self.driver.title or "")[:500], bool(self.driver.current_url), text)

    def click_css(self, selector: str, *, owner_approved: bool = False) -> dict:
        el = self.driver.find_element("css selector", validate_selector(selector))
        tag = str(el.tag_name or "").lower()
        typ = str(el.get_attribute("type") or "").lower()
        role = str(el.get_attribute("role") or "").lower()
        # Buttons and submit-like controls can change external state.
        if (tag == "button" or typ in {"submit", "button", "reset"} or role == "button") and owner_approved is not True:
            raise PermissionError("Explicit owner approval is required before clicking a consequential control.")
        el.click()
        return {"ok": True, "action": "click", "consequential_control": tag == "button" or typ in {"submit","button","reset"} or role == "button"}

    def type_css(self, selector: str, value: str, *, owner_approved: bool = False) -> dict:
        if owner_approved is not True:
            raise PermissionError("Explicit owner approval is required before typing into a live application.")
        value = str(value or "")
        if len(value) > 4000: raise LiveBrowserError("Typed value exceeds safety bound.")
        el = self.driver.find_element("css selector", validate_selector(selector))
        el.send_keys(value)
        return {"ok": True, "action": "type_sensitive", "typed_chars": len(value)}

    def close(self) -> None:
        try: self.driver.quit()
        except Exception: pass


def public_manifest() -> dict:
    return {
        "driver":"selenium_local_browser",
        "selenium_available":selenium_available(),
        "supported_browsers":["Microsoft Edge","Google Chrome"],
        "supported_actions":["open_url","observe","click_css","type_css","close"],
        "owner_gate":{"typing":True,"button_or_submit_click":True},
        "bounds":{"max_observed_text_chars":MAX_TEXT_CHARS,"max_selector_chars":MAX_SELECTOR_CHARS,"http_https_only":True},
        "privacy":{"page_text_exposed_in_buyer_evidence":False,"urls_exposed_in_buyer_evidence":False,"typed_values_exposed_in_buyer_evidence":False,"credentials_exposed":False},
    }
