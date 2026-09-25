from adam_core.meeting_platform_adapter import public_manifest, preview_join, synthetic_join
from adam_core.meeting_platform_boundary import build_meeting_platform_manifest, meeting_platform_is_privacy_safe, meeting_platform_self_test

def test_manifest_privacy_and_no_live_claim():
    m=build_meeting_platform_manifest("v4.7.0")
    c=m["meeting_platform"]["capabilities"]
    assert meeting_platform_is_privacy_safe(m)
    assert c["meeting_platform_adapter_foundation"] is True
    assert c["live_meeting_join_enabled"] is False
    assert c["user_impersonation_allowed"] is False
    assert set(c["supported_platforms"])=={"microsoft_teams","zoom","google_meet"}

def test_preview_does_not_return_meeting_reference():
    r=preview_join({"platform":"zoom","meeting_ref":"secret-meeting-link"})
    assert r["ok"] and r["meeting_reference_returned"] is False and "secret-meeting-link" not in str(r)

def test_synthetic_owner_gate_and_self_test():
    calls=[]
    def adapter(req): calls.append(req.platform); return True
    base={"platform":"google_meet","meeting_ref":"synthetic://x"}
    blocked=synthetic_join({**base,"owner_approved":False},adapter)
    approved=synthetic_join({**base,"owner_approved":True},adapter)
    assert blocked["status"]=="approval_required" and not calls[:-1]
    assert approved["ok"] and approved["synthetic_only"] and approved["real_meeting_joined"] is False
    assert meeting_platform_self_test()["ok"] is True
