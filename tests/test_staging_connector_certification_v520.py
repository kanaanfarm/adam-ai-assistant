from adam_core.staging_connector_certification import REQUIRED_CHECKS,validate_staging_candidate,certify_staging_connector
from adam_core.staging_connector_certification_boundary import build_staging_connector_certification_manifest,staging_connector_certification_is_privacy_safe,staging_connector_certification_self_test

def good(): return {k:True for k in REQUIRED_CHECKS}
def test_manifest_privacy():
    p=build_staging_connector_certification_manifest("v5.2.1")
    assert p["staging_connector_certification"]["capabilities"]["staging_connector_certification"] is True
    assert staging_connector_certification_is_privacy_safe(p)
def test_gate_and_certification():
    assert validate_staging_candidate({"connector":"email","checks":good()})["certification_ready"]
    assert certify_staging_connector(connector="email",checks=good(),owner_approved=False,probe=lambda c:{"ok":True})["status"]=="approval_required"
    r=certify_staging_connector(connector="email",checks=good(),owner_approved=True,probe=lambda c:{"ok":True})
    assert r["status"]=="staging_connector_certified" and r["live_execution_enabled"] is False
def test_self_test(): assert staging_connector_certification_self_test()["ok"] is True
