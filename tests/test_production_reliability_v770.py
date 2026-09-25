from pathlib import Path

from adam_core.production_reliability import (
    ReliabilityPolicy,
    build_status,
    consequential_retry_decision,
    run_read_only_probe,
    self_test,
    stability_summary,
)


def test_v770_retries_only_bounded_read_only_probe_and_recovers():
    calls = []
    outcomes = [TimeoutError(), ConnectionError(), {"ok": True}]
    def probe():
        calls.append("probe")
        value = outcomes.pop(0)
        if isinstance(value, Exception):
            raise value
        return value
    r = run_read_only_probe(probe, lambda: calls.append("reconnect"), policy=ReliabilityPolicy(max_attempts=3))
    assert r["ok"] is True and r["status"] == "connector_probe_recovered"
    assert r["attempts"] == 3 and r["reconnect_count"] == 2
    assert r["external_action_executed"] is False


def test_v770_ambiguous_consequential_outcome_requires_owner_review():
    r = consequential_retry_decision(outcome_known=False)
    assert r["automatic_retry_allowed"] is False
    assert r["owner_review_required"] is True
    assert r["external_action_executed"] is False


def test_v770_stability_window_is_bounded_and_reports_p95():
    r = stability_summary([{"ok": True, "duration_ms": i} for i in range(600)])
    assert r["sample_count"] == 500 and r["window_bounded"] is True
    assert r["success_rate"] == 1.0 and r["p95_duration_ms"] == 574.0


def test_v770_boundary_self_test_and_runtime_routes():
    assert build_status()["owner_approval_preserved"] is True
    assert self_test()["ok"] is True
    app = Path("app.py").read_text()
    html = Path("templates/production_reliability.html").read_text()
    assert 'VERSION = "v8.1.0.1"' in app
    assert "/api/personal-assistant/production-reliability/status" in app
    assert "/api/personal-assistant/production-reliability/self-test" in app
    assert "Run Safe Reliability Check" in html
    assert "never automatically repeated" in html
