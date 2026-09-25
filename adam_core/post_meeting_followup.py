"""Governed post-meeting cross-app follow-up foundation for Adam Acquisition v4.8."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Mapping

MAX_ACTIONS = 12
MAX_TEXT_CHARS = 500
SUPPORTED_CONNECTORS = {"email", "calendar", "documents", "whatsapp"}
CONSEQUENTIAL_ACTIONS = {"send", "invite", "upload", "submit"}
PREPARE_ACTIONS = {"draft", "prepare", "create_draft", "create_event_draft", "create_task_draft"}

class PostMeetingFollowupError(RuntimeError): pass

def _clean(v: Any, n: int=MAX_TEXT_CHARS) -> str:
    return " ".join(str(v or "").split())[:n]

@dataclass(frozen=True)
class FollowupAction:
    connector: str
    action: str
    summary: str = ""
    owner_approved: bool = False
    @property
    def consequential(self): return self.action in CONSEQUENTIAL_ACTIONS
    def public_dict(self):
        return {"connector":self.connector,"action":self.action,"summary_present":bool(self.summary),
                "consequential":self.consequential,"owner_approved":self.owner_approved}

def normalize_actions(raw_actions):
    out=[]
    for raw in list(raw_actions or [])[:MAX_ACTIONS]:
        connector=_clean(raw.get("connector"),40).lower(); action=_clean(raw.get("action"),40).lower()
        if connector not in SUPPORTED_CONNECTORS: raise PostMeetingFollowupError("Unsupported follow-up connector.")
        if action not in (CONSEQUENTIAL_ACTIONS|PREPARE_ACTIONS): raise PostMeetingFollowupError("Unsupported follow-up action.")
        out.append(FollowupAction(connector,action,_clean(raw.get("summary")),raw.get("owner_approved") is True))
    if not out: raise PostMeetingFollowupError("At least one follow-up action is required.")
    return out

def preview_followup(raw_actions):
    actions=normalize_actions(raw_actions)
    return {"ok":True,"status":"followup_preview_ready","action_count":len(actions),
            "approval_required_actions":[i+1 for i,a in enumerate(actions) if a.consequential and not a.owner_approved],
            "actions":[a.public_dict() for a in actions],"private_values_returned":False}

def execute_followup(raw_actions, adapters: Mapping[str,Callable[[FollowupAction],Any]]):
    actions=normalize_actions(raw_actions); receipts=[]
    for i,a in enumerate(actions,1):
        if a.consequential and not a.owner_approved:
            return {"ok":False,"status":"approval_required","blocked_action":i,"completed_actions":len(receipts),
                    "owner_gate_preserved":True,"private_values_returned":False,"receipts":receipts}
        adapter=adapters.get(a.connector)
        if adapter is None: raise PostMeetingFollowupError("Missing follow-up adapter.")
        result=adapter(a)
        receipts.append({"action":i,"connector":a.connector,"operation":a.action,"consequential":a.consequential,
                         "executed":True,"adapter_ok":result is not False})
    return {"ok":True,"status":"followup_completed","completed_actions":len(receipts),"owner_gate_preserved":True,
            "audit_receipts_generated":True,"private_values_returned":False,"receipts":receipts}

def public_manifest():
    return {"post_meeting_cross_app_followup":True,"structured_meeting_outcomes_input":True,"followup_preview":True,
            "injected_connector_adapters":True,"per_action_owner_approval":True,"audit_receipts":True,
            "supported_connectors":sorted(SUPPORTED_CONNECTORS),"prepare_actions":sorted(PREPARE_ACTIONS),
            "consequential_actions":sorted(CONSEQUENTIAL_ACTIONS),"bounds":{"max_actions":MAX_ACTIONS,"max_text_chars":MAX_TEXT_CHARS},
            "privacy":{"credentials_stored":False,"message_bodies_exposed_in_buyer_evidence":False,
                       "contact_values_exposed_in_buyer_evidence":False,"meeting_memory_contents_exposed_in_buyer_evidence":False}}
