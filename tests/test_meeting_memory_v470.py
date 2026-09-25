from adam_core.meeting_memory import public_manifest, save_memory, recall_memory
from adam_core.meeting_memory_boundary import build_meeting_memory_manifest, meeting_memory_is_privacy_safe, meeting_memory_self_test

def test_manifest_privacy():
    m=build_meeting_memory_manifest("v4.7.0"); c=m["meeting_memory"]["capabilities"]
    assert meeting_memory_is_privacy_safe(m)
    assert c["meeting_memory_foundation"] is True
    assert c["structured_outcomes_only"] is True
    assert c["privacy"]["raw_transcript_stored"] is False
    assert c["privacy"]["memory_contents_exposed_in_buyer_evidence"] is False

def test_save_receipt_excludes_contents():
    calls=[]
    r=save_memory({"summary":"private summary","decisions":["private decision"],"action_items":["private action"]},lambda rec:calls.append(rec) or True)
    assert r["ok"] is True and len(calls)==1
    assert r["receipt"]["decision_count"]==1
    assert "private summary" not in str(r)
    assert "private decision" not in str(r)

def test_recall_is_buyer_safe_and_self_test_passes():
    r=recall_memory("handover",lambda q:[{"secret":"x"}])
    assert r["matches_found"]==1 and r["private_values_returned"] is False
    assert "secret" not in str(r)
    assert meeting_memory_self_test()["ok"] is True
