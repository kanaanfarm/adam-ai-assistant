from adam_core.meeting_agent import build_meeting_notes, execute_meeting_action
from adam_core.meeting_agent_boundary import build_meeting_agent_manifest, meeting_agent_is_privacy_safe, meeting_agent_self_test

def test_manifest_privacy_and_identity():
    p=build_meeting_agent_manifest("v4.5.0"); assert meeting_agent_is_privacy_safe(p)
    c=p["meeting_agent"]["capabilities"]
    assert c["meeting_listen_and_notes"] is True
    assert c["per_action_owner_approval"] is True
    assert c["ai_identity_required_for_speaking"] is True
    assert c["user_impersonation_allowed"] is False
    assert c["live_meeting_join_enabled"] is False

def test_notes_and_owner_gate():
    n=build_meeting_notes([{"speaker":"A","text":"Status good"},{"speaker":"B","text":"Action: send revised schedule"}])
    assert n["action_item_count"]==1
    calls=[]
    def a(x): calls.append(x.action); return True
    b=execute_meeting_action({"action":"speak","content":"x","owner_approved":False},a)
    assert b["status"]=="approval_required" and calls==[]
    ok=execute_meeting_action({"action":"speak","content":"x","owner_approved":True},a)
    assert ok["ok"] and calls==["speak"]

def test_self_test_is_synthetic():
    r=meeting_agent_self_test(); assert r["ok"]
    assert r["speaking_blocked_without_owner_approval"]
    assert r["approved_speaking_executed"]
    assert r["real_meeting_joined"] is False
    assert r["external_network_accessed"] is False
