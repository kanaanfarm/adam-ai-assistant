from adam_core.meeting_knowledge import answer_from_approved_knowledge
from adam_core.meeting_knowledge_boundary import build_meeting_knowledge_manifest, meeting_knowledge_is_privacy_safe, meeting_knowledge_self_test

def test_manifest_privacy():
    p=build_meeting_knowledge_manifest("v4.5.0"); assert meeting_knowledge_is_privacy_safe(p)

def test_approved_only_and_abstention():
    src=[{"source_id":"a","approved":True,"text":"Project handover date is 30 September."},{"source_id":"x","approved":False,"text":"Catering budget is 999."}]
    a=answer_from_approved_knowledge("What is project handover date?",src); assert a["ok"] and a["unapproved_sources_used"]==0
    b=answer_from_approved_knowledge("What is catering budget?",src); assert not b["ok"] and b["status"]=="insufficient_approved_knowledge"

def test_self_test():
    r=meeting_knowledge_self_test(); assert r["ok"] and r["unknown_question_abstained"] and r["owner_approval_required_to_speak"]
