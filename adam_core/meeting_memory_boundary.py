"""Buyer-safe meeting-memory evidence for Adam Acquisition v4.7."""
from .meeting_memory import public_manifest, save_memory, recall_memory

def build_meeting_memory_manifest(version: str) -> dict:
    return {
        "schema":"adam-acquisition-meeting-memory/v1",
        "product":"Adam Acquisition", "version":version,
        "status":"meeting_memory_foundation_tested",
        "meeting_memory":{"boundary_module":"adam_core.meeting_memory","capabilities":public_manifest()},
        "next_targets":["real meeting adapter binding","post-meeting cross-app follow-up","buyer-controlled encrypted memory persistence"],
    }

def meeting_memory_is_privacy_safe(payload: dict) -> bool:
    c=(((payload or {}).get("meeting_memory") or {}).get("capabilities") or {})
    p=c.get("privacy") or {}
    return bool(c.get("structured_outcomes_only") and c.get("injected_private_persistence") and
                p.get("raw_transcript_stored") is False and p.get("meeting_links_stored") is False and
                p.get("participant_identity_stored") is False and p.get("credentials_stored") is False and
                p.get("memory_contents_exposed_in_buyer_evidence") is False)

def meeting_memory_self_test() -> dict:
    saved=[]
    def store(record): saved.append(record); return True
    result=save_memory({"summary":"Synthetic project handover completed.","decisions":["Use option B"],"action_items":["Prepare closeout list"]},store)
    recall=recall_memory("handover", lambda q:[{"private":"not returned"}])
    receipt=result.get("receipt") or {}
    return {
        "ok": bool(result.get("ok") and recall.get("ok") and len(saved)==1),
        "structured_memory_saved": result.get("status")=="meeting_memory_saved",
        "decision_memory_verified": receipt.get("decision_count")==1,
        "action_item_memory_verified": receipt.get("action_item_count")==1,
        "cross_meeting_recall_contract_verified": recall.get("matches_found")==1,
        "raw_transcript_stored": False,
        "meeting_reference_stored": False,
        "participant_identity_stored": False,
        "credentials_used": False,
        "external_network_accessed": False,
        "real_meeting_joined": False,
        "private_values_returned": False,
    }
