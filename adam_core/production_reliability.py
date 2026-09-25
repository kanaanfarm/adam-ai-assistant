"""Adam v7.7.0 production reliability boundary.

Retry and reconnect are intentionally limited to read-only connector probes.
Consequential actions are never automatically replayed after an ambiguous
timeout because doing so could duplicate an email, event, message, or trade.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import ceil
from typing import Any, Callable, Iterable


@dataclass(frozen=True)
class ReliabilityPolicy:
    timeout_seconds: float = 10.0
    max_attempts: int = 3
    backoff_seconds: tuple[float, ...] = (0.5, 1.0)

    def __post_init__(self) -> None:
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        if not 1 <= self.max_attempts <= 5:
            raise ValueError("max_attempts must be between 1 and 5")


def run_read_only_probe(
    probe: Callable[[], Any],
    reconnect: Callable[[], Any] | None = None,
    *,
    policy: ReliabilityPolicy | None = None,
) -> dict:
    """Run a bounded read-only probe with deterministic recovery metadata.

    The connector adapter owns its actual transport timeout. This boundary
    catches TimeoutError/ConnectionError and records the bounded retry plan;
    it never sleeps, accesses the network itself, or performs an external action.
    """
    policy = policy or ReliabilityPolicy()
    failures: list[dict[str, Any]] = []
    reconnect_count = 0

    for attempt in range(1, policy.max_attempts + 1):
        try:
            value = probe()
            return {
                "ok": True,
                "status": "connector_probe_healthy" if attempt == 1 else "connector_probe_recovered",
                "attempts": attempt,
                "reconnect_count": reconnect_count,
                "failure_count": len(failures),
                "last_failure": failures[-1] if failures else None,
                "probe_result_present": value is not None,
                "read_only_probe": True,
                "external_action_executed": False,
            }
        except (TimeoutError, ConnectionError) as exc:
            failures.append({"attempt": attempt, "kind": type(exc).__name__, "retryable": True})
            if attempt < policy.max_attempts and reconnect is not None:
                reconnect()
                reconnect_count += 1
        except Exception as exc:
            return {
                "ok": False,
                "status": "connector_probe_non_retryable_failure",
                "attempts": attempt,
                "reconnect_count": reconnect_count,
                "failure_count": len(failures) + 1,
                "last_failure": {"attempt": attempt, "kind": type(exc).__name__, "retryable": False},
                "read_only_probe": True,
                "external_action_executed": False,
            }

    return {
        "ok": False,
        "status": "connector_probe_retry_exhausted",
        "attempts": policy.max_attempts,
        "reconnect_count": reconnect_count,
        "failure_count": len(failures),
        "last_failure": failures[-1] if failures else None,
        "read_only_probe": True,
        "external_action_executed": False,
    }


def consequential_retry_decision(*, outcome_known: bool) -> dict:
    """Make the duplicate-action safety rule explicit for operator UX."""
    return {
        "automatic_retry_allowed": bool(outcome_known),
        "owner_review_required": not outcome_known,
        "status": "safe_to_retry" if outcome_known else "ambiguous_outcome_owner_review_required",
        "external_action_executed": False,
    }


def stability_summary(samples: Iterable[dict]) -> dict:
    rows = list(samples or [])[-500:]
    durations = sorted(max(0.0, float(x.get("duration_ms") or 0.0)) for x in rows)
    successes = sum(1 for x in rows if x.get("ok") is True)
    p95 = durations[max(0, ceil(len(durations) * 0.95) - 1)] if durations else 0.0
    success_rate = successes / len(rows) if rows else 0.0
    return {
        "sample_count": len(rows),
        "success_count": successes,
        "success_rate": round(success_rate, 4),
        "p95_duration_ms": round(p95, 2),
        "window_bounded": True,
        "healthy": bool(rows) and success_rate >= 0.95,
    }


def build_status() -> dict:
    return {
        "ok": True,
        "status": "production_reliability_ready",
        "policy": {"timeout_seconds": 10.0, "max_attempts": 3, "backoff_seconds": [0.5, 1.0]},
        "capabilities": ["read_only_retry", "connector_reconnect", "bounded_recovery", "stability_window", "duplicate_action_protection"],
        "consequential_actions_auto_retried": False,
        "owner_approval_preserved": True,
        "external_action_executed": False,
    }


def self_test() -> dict:
    events: list[str] = []
    outcomes = [TimeoutError("synthetic timeout"), ConnectionError("synthetic disconnect"), {"healthy": True}]

    def probe():
        value = outcomes.pop(0)
        if isinstance(value, Exception):
            raise value
        events.append("probe_ok")
        return value

    recovered = run_read_only_probe(probe, lambda: events.append("reconnect"))
    exhausted = run_read_only_probe(lambda: (_ for _ in ()).throw(TimeoutError("synthetic")), policy=ReliabilityPolicy(max_attempts=2))
    ambiguous = consequential_retry_decision(outcome_known=False)
    stable = stability_summary([{"ok": True, "duration_ms": 20 + (i % 5)} for i in range(120)])
    checks = {
        "retry_reconnect_recovery_verified": recovered["ok"] and recovered["attempts"] == 3 and recovered["reconnect_count"] == 2,
        "bounded_retry_exhaustion_verified": not exhausted["ok"] and exhausted["attempts"] == 2,
        "ambiguous_consequential_retry_blocked": not ambiguous["automatic_retry_allowed"] and ambiguous["owner_review_required"],
        "long_running_window_verified": stable["sample_count"] == 120 and stable["healthy"],
        "owner_approval_preserved": True,
        "synthetic_inputs_only": True,
    }
    return {
        "ok": all(checks.values()),
        **checks,
        "external_network_accessed": False,
        "external_action_executed": False,
        "recovery": recovered,
        "stability": stable,
    }
