from adam_core.enterprise_security_hardening import SECURITY_CHECKS,evaluate_security_readiness,authorize_hardened_deployment
from adam_core.enterprise_security_hardening_boundary import build_enterprise_security_hardening_manifest,enterprise_security_hardening_is_privacy_safe,enterprise_security_hardening_self_test

def test_boundary_and_privacy():
 p=build_enterprise_security_hardening_manifest("v5.7.0"); assert enterprise_security_hardening_is_privacy_safe(p); assert p["enterprise_security_hardening"]["capabilities"]["real_deployment_enabled_by_acceptance_test"] is False

def test_owner_gate_and_self_test():
 good={k:True for k in SECURITY_CHECKS}; r=authorize_hardened_deployment(environment="production",checks=good,owner_approved=False,deployer=lambda e,a:{"ok":True}); assert r["status"]=="approval_required" and not r["deployer_called"]; assert enterprise_security_hardening_self_test()["ok"]
