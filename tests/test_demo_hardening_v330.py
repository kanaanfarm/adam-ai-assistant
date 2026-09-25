from adam_core.demo_hardening import build_demo_hardening_manifest, demo_hardening_is_privacy_safe, demo_hardening_self_test

def test_manifest_has_three_buyer_demos_and_is_private():
    p=build_demo_hardening_manifest("v3.4.0")
    assert demo_hardening_is_privacy_safe(p)
    s=p["demo_hardening"]
    assert s["status"]=="hardened_tested"
    assert len(s["scenarios"])==3
    assert len(p["demo_hardening_sha256"])==64
    assert all(x["owner_approval_required"] for x in s["scenarios"])
    assert all(not x["live_execution_required_for_demo"] for x in s["scenarios"])

def test_self_test_is_network_and_app_data_free():
    r=demo_hardening_self_test()
    assert r["ok"] is True
    assert r["external_network_accessed"] is False
    assert r["external_application_data_accessed"] is False
    assert r["private_values_returned"] is False

def test_app_routes_present():
    from pathlib import Path
    src=(Path(__file__).resolve().parents[1]/"app.py").read_text(encoding="utf-8")
    assert '/api/acquisition/demo-hardening' in src
    assert '/api/acquisition/demo-hardening/self-test' in src
