from adam_core.post_meeting_followup import preview_followup, execute_followup, public_manifest
from adam_core.post_meeting_followup_boundary import build_post_meeting_followup_manifest, post_meeting_followup_is_privacy_safe, post_meeting_followup_self_test

def test_manifest_privacy():
    p=build_post_meeting_followup_manifest("v4.8.0")
    assert p["post_meeting_followup"]["post_meeting_cross_app_followup"] is True
    assert post_meeting_followup_is_privacy_safe(p)

def test_owner_gate_and_approved_execution():
    raw=[{"connector":"email","action":"draft","summary":"draft"},{"connector":"calendar","action":"invite","summary":"invite"}]
    assert preview_followup(raw)["approval_required_actions"]==[2]
    assert execute_followup(raw,{"email":lambda a:True,"calendar":lambda a:True})["status"]=="approval_required"
    raw[1]["owner_approved"]=True
    assert execute_followup(raw,{"email":lambda a:True,"calendar":lambda a:True})["ok"] is True

def test_self_test_is_synthetic():
    r=post_meeting_followup_self_test()
    assert r["ok"] and r["consequential_action_blocked_without_owner_approval"] and r["approved_cross_app_followup_executed"]
    assert not r["external_network_accessed"] and not r["real_email_sent"] and not r["real_calendar_invite_sent"]
