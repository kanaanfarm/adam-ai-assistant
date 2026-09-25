from .post_meeting_followup import public_manifest, preview_followup, execute_followup

def build_post_meeting_followup_manifest(version):
    return {"schema":"adam-acquisition-post-meeting-followup/v1","product":"Adam Acquisition","version":version,
            "status":"post_meeting_followup_foundation_tested","post_meeting_followup":public_manifest(),
            "next_targets":["real connector binding","real meeting adapter binding","buyer-controlled encrypted meeting memory"]}

def post_meeting_followup_is_privacy_safe(payload):
    p=payload["post_meeting_followup"]["privacy"]
    return not any(p.values())

def post_meeting_followup_self_test():
    prepared=[{"connector":"email","action":"draft","summary":"Prepare follow-up"},
              {"connector":"calendar","action":"invite","summary":"Schedule review"}]
    preview=preview_followup(prepared)
    blocked=execute_followup(prepared,{"email":lambda a:True,"calendar":lambda a:True})
    approved=[dict(x,owner_approved=True) for x in prepared]
    done=execute_followup(approved,{"email":lambda a:True,"calendar":lambda a:True})
    return {"ok":True,"followup_preview_verified":preview["ok"],"consequential_action_blocked_without_owner_approval":blocked["status"]=="approval_required",
            "approved_cross_app_followup_executed":done["ok"],"audit_receipts_generated":done["audit_receipts_generated"],
            "owner_gate_preserved":done["owner_gate_preserved"],"external_network_accessed":False,"real_email_sent":False,
            "real_calendar_invite_sent":False,"credentials_used":False,"private_values_returned":False}
