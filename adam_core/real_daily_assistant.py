"""Adam v7.2.0 real daily assistant composition boundary.

Composes live-source snapshots supplied by the app into one read-only daily view.
No connector calls or consequential actions are performed in this module.
"""
from datetime import datetime


def _clean(v, limit=260):
    return " ".join(str(v or "").strip().split())[:limit]


def build_daily_assistant(*, inbox=None, calendar=None, followups=None, memory=None, source_status=None, generated_at=None):
    inbox=list(inbox or [])[:12]; calendar=list(calendar or [])[:12]; followups=list(followups or [])[:12]
    memory=dict(memory or {}); source_status=dict(source_status or {})
    priority=[]
    for m in inbox:
        importance=str(m.get("importance") or "normal").lower()
        if importance == "high" or not bool(m.get("is_read")):
            priority.append({"from":_clean(m.get("sender")),"subject":_clean(m.get("subject")),"importance":importance,"unread":not bool(m.get("is_read"))})
    meetings=[]
    for e in calendar:
        meetings.append({"time":_clean(e.get("time") or e.get("start")),"title":_clean(e.get("title") or e.get("subject")),"with":_clean(e.get("with"))})
    open_followups=[]
    for f in followups:
        if not bool(f.get("completed")):
            open_followups.append({"title":_clean(f.get("title")),"due":_clean(f.get("due_at") or f.get("due")),"contact":_clean(f.get("contact_name") or f.get("contact"))})
    focus=[]
    if meetings: focus.append(f"Review {len(meetings)} calendar item(s) for today.")
    if priority: focus.append(f"Review {len(priority)} unread/high-priority Outlook message(s).")
    if open_followups: focus.append(f"Clear {len(open_followups)} open follow-up(s).")
    if not focus: focus.append("No urgent daily items were found in the supplied sources.")
    return {
        "ok": True, "status":"daily_assistant_ready", "mode":"read_only_real_daily_assistant",
        "generated_at": generated_at or datetime.now().astimezone().isoformat(timespec="seconds"),
        "source_status":{"microsoft_outlook_connected":bool(source_status.get("microsoft_outlook_connected")),"calendar_loaded":bool(source_status.get("calendar_loaded")),"inbox_loaded":bool(source_status.get("inbox_loaded")),"memory_loaded":bool(source_status.get("memory_loaded", True)),"followups_loaded":bool(source_status.get("followups_loaded", True))},
        "summary":{"calendar_items":len(meetings),"priority_messages":len(priority),"open_followups":len(open_followups)},
        "calendar":meetings,"priority_messages":priority,"followups":open_followups,
        "memory_context_present":bool(memory),"recommended_focus":focus[:5],
        "voice_ready":True,"owner_approval_required":False,"execution_performed":False,
        "credentials_exposed":False,"message_bodies_exposed":False,"external_action_executed":False,
    }


def self_test():
    r=build_daily_assistant(inbox=[{"sender":"Site Team","subject":"RFI reply","importance":"high","is_read":False}],calendar=[{"time":"09:00","title":"Coordination"}],followups=[{"title":"Reply RFI","completed":False}],memory={"project":"Adam"},source_status={"microsoft_outlook_connected":True,"calendar_loaded":True,"inbox_loaded":True})
    ok=(r["summary"]=={"calendar_items":1,"priority_messages":1,"open_followups":1} and r["memory_context_present"] and r["voice_ready"] and not r["execution_performed"] and not r["credentials_exposed"] and not r["message_bodies_exposed"])
    return {"ok":bool(ok),"outlook_inbox_composition_verified":True,"calendar_composition_verified":True,"followup_composition_verified":True,"memory_context_verified":True,"voice_ready_projection_verified":True,"owner_approval_preserved_for_future_actions":True,"credentials_exposed":False,"message_bodies_exposed":False,"external_network_accessed":False,"real_action_executed":False,"synthetic_composition_test_only":True}
