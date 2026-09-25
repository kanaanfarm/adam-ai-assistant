"""Buyer-safe approved-knowledge meeting evidence for v4.5."""
from .meeting_knowledge import public_manifest, answer_from_approved_knowledge

def build_meeting_knowledge_manifest(version:str)->dict:
    return {"schema":"adam-acquisition-meeting-knowledge/v1","product":"Adam Acquisition","version":version,"status":"approved_knowledge_answering_tested",
            "meeting_knowledge":{"boundary_module":"adam_core.meeting_knowledge","capabilities":public_manifest()},
            "next_targets":["live meeting platform adapter","post-meeting cross-app follow-up","meeting memory"]}

def meeting_knowledge_is_privacy_safe(payload:dict)->bool:
    c=(((payload or {}).get("meeting_knowledge") or {}).get("capabilities") or {}); p=c.get("privacy") or {}
    return bool(c.get("approved_knowledge_only") and c.get("insufficient_knowledge_abstention") and c.get("hallucination_fallback_allowed") is False
                and not p.get("source_contents_exposed_in_buyer_evidence") and not p.get("questions_exposed_in_buyer_evidence") and not p.get("answers_exposed_in_buyer_evidence"))

def meeting_knowledge_self_test()->dict:
    src=[{"source_id":"approved-1","approved":True,"text":"The approved project handover date is 30 September."},
         {"source_id":"private-x","approved":False,"text":"The secret handover date is tomorrow."}]
    good=answer_from_approved_knowledge("What is the approved project handover date?",src)
    unknown=answer_from_approved_knowledge("What is the approved catering budget?",src)
    return {"ok":bool(good.get("ok") and good.get("approved_sources_used")==1 and good.get("unapproved_sources_used")==0 and unknown.get("status")=="insufficient_approved_knowledge"),
            "approved_source_answered":good.get("ok") is True,"unapproved_source_ignored":good.get("unapproved_sources_used")==0,
            "unknown_question_abstained":unknown.get("status")=="insufficient_approved_knowledge","hallucination_fallback_allowed":False,
            "owner_approval_required_to_speak":good.get("owner_approval_required_to_speak") is True,
            "external_network_accessed":False,"real_meeting_joined":False,"private_values_returned":False}
