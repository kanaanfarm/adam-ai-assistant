"""Approved-knowledge answer boundary for Adam Acquisition v4.5."""
from __future__ import annotations
from typing import Any

MAX_SOURCES=12
MAX_SOURCE_CHARS=4000
MAX_QUESTION_CHARS=500
MAX_ANSWER_CHARS=1200

class MeetingKnowledgeError(RuntimeError): pass

def _clean(v: Any, limit: int)->str:
    return " ".join(str(v or "").split())[:limit]

def prepare_approved_knowledge(sources: list[dict] | None)->list[dict]:
    out=[]
    for raw in list(sources or [])[:MAX_SOURCES]:
        if raw.get("approved") is not True: continue
        text=_clean(raw.get("text"),MAX_SOURCE_CHARS)
        if text: out.append({"source_id":_clean(raw.get("source_id"),80) or f"source-{len(out)+1}","text":text})
    return out

def answer_from_approved_knowledge(question: str, sources: list[dict] | None)->dict:
    q=_clean(question,MAX_QUESTION_CHARS)
    approved=prepare_approved_knowledge(sources)
    if not q: raise MeetingKnowledgeError("Question is required.")
    if not approved:
        return {"ok":False,"status":"insufficient_approved_knowledge","answer_available":False,
                "approved_sources_used":0,"unapproved_sources_used":0,"hallucination_fallback_allowed":False}
    stop={"what","when","where","which","approved","project","please","tell"}
    words=[w.strip(".,?!:;()[]{}\"'").lower() for w in q.split() if len(w)>3]
    words=[w for w in words if w not in stop]
    ranked=[]
    for s in approved:
        low=s["text"].lower(); score=sum(1 for w in words if w in low)
        ranked.append((score,s))
    ranked.sort(key=lambda x:x[0], reverse=True)
    score,best=ranked[0]
    if score<=0:
        return {"ok":False,"status":"insufficient_approved_knowledge","answer_available":False,
                "approved_sources_used":0,"unapproved_sources_used":0,"hallucination_fallback_allowed":False}
    answer=best["text"][:MAX_ANSWER_CHARS]
    return {"ok":True,"status":"grounded_answer_ready","answer_available":True,"answer":answer,
            "approved_sources_used":1,"source_ids":[best["source_id"]],"unapproved_sources_used":0,
            "hallucination_fallback_allowed":False,"owner_approval_required_to_speak":True}

def public_manifest()->dict:
    return {"approved_knowledge_only":True,"unapproved_knowledge_ignored":True,"insufficient_knowledge_abstention":True,
            "hallucination_fallback_allowed":False,"owner_approval_required_to_speak_answer":True,
            "bounds":{"max_sources":MAX_SOURCES,"max_source_chars":MAX_SOURCE_CHARS,"max_question_chars":MAX_QUESTION_CHARS,"max_answer_chars":MAX_ANSWER_CHARS},
            "privacy":{"source_contents_exposed_in_buyer_evidence":False,"questions_exposed_in_buyer_evidence":False,"answers_exposed_in_buyer_evidence":False}}
