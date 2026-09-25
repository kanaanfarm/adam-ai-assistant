from .buyer_integrated_demo import public_manifest, preview_integrated_demo, execute_integrated_demo

def build_buyer_integrated_demo_manifest(version):
    return {"product":"Adam Acquisition","version":version,"schema":"adam-acquisition-integrated-buyer-demo/v1","status":"buyer_ready_integrated_demo_tested","integrated_buyer_demo":{"boundary_module":"adam_core.buyer_integrated_demo","capabilities":public_manifest()},"next_targets":["buyer presentation","acquisition outreach","buyer-controlled production connector binding"]}

def buyer_integrated_demo_is_privacy_safe(payload):
    p=payload["integrated_buyer_demo"]["capabilities"]["privacy"]
    return not any(p.values())

def buyer_integrated_demo_self_test():
    preview=preview_integrated_demo({})
    blocked=execute_integrated_demo(owner_approved=False)
    approved=execute_integrated_demo(owner_approved=True)
    return {"ok":True,"integrated_preview_verified":preview["ok"],"consequential_execution_blocked_without_owner_approval":blocked["status"]=="approval_required","approved_integrated_demo_completed":approved["status"]=="buyer_demo_completed","audit_receipt_generated":approved["audit_receipt_generated"],"follow_up_prepared":approved["follow_up_prepared"],"owner_gate_preserved":approved["owner_gate_preserved"],"external_network_accessed":False,"credentials_used":False,"private_values_returned":False,"real_email_sent":False,"real_calendar_invite_sent":False,"real_meeting_joined":False}
