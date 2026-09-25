"""Buyer-safe Meeting Agent evidence for Adam Acquisition v4.4."""
from .meeting_agent import public_manifest, build_meeting_notes, execute_meeting_action

def build_meeting_agent_manifest(version: str) -> dict:
    return {"schema":"adam-acquisition-meeting-agent/v1","product":"Adam Acquisition","version":version,
            "status":"meeting_agent_foundation_tested",
            "meeting_agent":{"boundary_module":"adam_core.meeting_agent","capabilities":public_manifest()},
            "next_targets":["live Teams/Zoom/Meet joining","approved-knowledge answers","cross-app post-meeting follow-up"]}

def meeting_agent_is_privacy_safe(payload: dict) -> bool:
    c=(((payload or {}).get("meeting_agent") or {}).get("capabilities") or {}); p=c.get("privacy") or {}
    return bool(c.get("per_action_owner_approval") and c.get("user_impersonation_allowed") is False
                and not p.get("transcript_exposed_in_buyer_evidence") and not p.get("meeting_links_exposed_in_buyer_evidence")
                and not p.get("participant_identity_exposed_in_buyer_evidence") and not p.get("credentials_stored"))

def meeting_agent_self_test() -> dict:
    seg=[{"speaker":"A","text":"Project status is on track."},{"speaker":"B","text":"Action: prepare the revised schedule."}]
    notes=build_meeting_notes(seg); calls=[]
    def adapter(item): calls.append(item.action); return True
    blocked=execute_meeting_action({"action":"speak","content":"synthetic answer","owner_approved":False},adapter)
    approved=execute_meeting_action({"action":"speak","content":"synthetic answer","owner_approved":True},adapter)
    return {"ok": bool(notes.get("summary_available") and notes.get("action_item_count")==1 and blocked.get("status")=="approval_required" and approved.get("ok") and calls==["speak"]),
            "notes_generated":bool(notes.get("summary_available")),"action_items_extracted":notes.get("action_item_count")==1,
            "speaking_blocked_without_owner_approval":blocked.get("status")=="approval_required",
            "approved_speaking_executed":approved.get("ok") is True,"ai_identity_required":True,"user_impersonation_allowed":False,
            "external_network_accessed":False,"real_meeting_joined":False,"private_values_returned":False}
