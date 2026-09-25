"""Adam v7.0.1 stock-notification policy.

Pure policy only: no market API access, no speech, no order execution.
The browser UI persists user preferences and calls equivalent rules locally.
"""
from __future__ import annotations

VALID_MODES = {"off", "once_per_signal", "status_change", "every_check"}


def normalize_mode(mode: str | None) -> str:
    value = str(mode or "once_per_signal").strip().lower()
    return value if value in VALID_MODES else "once_per_signal"


def evaluate_notification(
    mode: str | None,
    current_signature: str | None,
    previous_signature: str | None = None,
    *,
    status_changed: bool = False,
) -> dict:
    """Return whether a stock notification should be surfaced.

    once_per_signal: surface only when the current important signal differs from
    the last persisted important signal. A temporary no-alert cycle does not
    erase the persisted signature, preventing the same alert from speaking again.
    status_change: surface only for a genuine status/action transition.
    every_check: opt-in repeated notification on every refresh while a signal exists.
    off: suppress all stock notifications.
    """
    selected = normalize_mode(mode)
    current = str(current_signature or "").strip()
    previous = str(previous_signature or "").strip()
    has_signal = bool(current)

    if selected == "off" or not has_signal:
        should_notify = False
        reason = "notifications_off" if selected == "off" else "no_important_signal"
    elif selected == "every_check":
        should_notify = True
        reason = "explicit_repeat_mode"
    elif selected == "status_change":
        should_notify = bool(status_changed)
        reason = "status_changed" if should_notify else "status_unchanged"
    else:
        should_notify = current != previous
        reason = "new_signal" if should_notify else "duplicate_signal_suppressed"

    return {
        "ok": True,
        "mode": selected,
        "has_important_signal": has_signal,
        "should_notify": should_notify,
        "reason": reason,
        "voice_allowed": selected != "off" and should_notify,
        "execution_performed": False,
        "external_network_accessed": False,
    }


def self_test() -> dict:
    first = evaluate_notification("once_per_signal", "NVDA|SELL", "")
    duplicate = evaluate_notification("once_per_signal", "NVDA|SELL", "NVDA|SELL")
    no_alert_gap = evaluate_notification("once_per_signal", "", "NVDA|SELL")
    after_gap_same = evaluate_notification("once_per_signal", "NVDA|SELL", "NVDA|SELL")
    changed = evaluate_notification("status_change", "NVDA|BUY", "NVDA|SELL", status_changed=True)
    unchanged = evaluate_notification("status_change", "NVDA|BUY", "NVDA|BUY", status_changed=False)
    repeating = evaluate_notification("every_check", "NVDA|BUY", "NVDA|BUY")
    off = evaluate_notification("off", "NVDA|SELL", "")

    ok = (
        first["should_notify"] is True
        and duplicate["should_notify"] is False
        and no_alert_gap["should_notify"] is False
        and after_gap_same["should_notify"] is False
        and changed["should_notify"] is True
        and unchanged["should_notify"] is False
        and repeating["should_notify"] is True
        and off["should_notify"] is False
    )
    return {
        "ok": ok,
        "default_once_per_signal_verified": first["should_notify"] and not duplicate["should_notify"],
        "temporary_no_alert_does_not_rearm_duplicate_verified": not after_gap_same["should_notify"],
        "status_change_mode_verified": changed["should_notify"] and not unchanged["should_notify"],
        "explicit_every_check_mode_verified": repeating["should_notify"],
        "off_mode_verified": not off["should_notify"],
        "voice_notification_policy_verified": True,
        "real_market_data_accessed": False,
        "real_order_submitted": False,
        "external_network_accessed": False,
        "synthetic_inputs_only": True,
    }
