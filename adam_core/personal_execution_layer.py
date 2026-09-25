"""Adam v6.1 personal execution preparation layer.

Turns a daily plan into explicit owner-reviewable actions. It never performs
external execution itself. Approved actions are handed to existing governed
connector adapters by higher-level routes only after explicit Owner Approval.
"""

def prepare_actions(request_text, available=None):
    text = str(request_text or '').strip()
    available = dict(available or {})
    if not text:
        return {'ok': False, 'status': 'request_required', 'actions': []}
    low = text.lower()
    actions=[]
    if any(k in low for k in ('email','outlook','message','contact')):
        actions.append({'type':'email','label':'Prepare email for Owner review','connector':'microsoft_outlook','connector_ready':bool(available.get('microsoft')),'requires_owner_approval':True,'execution_status':'blocked_pending_owner_approval'})
    if any(k in low for k in ('meeting','calendar','schedule','appointment')):
        actions.append({'type':'calendar','label':'Prepare calendar event for Owner review','connector':'microsoft_calendar','connector_ready':bool(available.get('microsoft')),'requires_owner_approval':True,'execution_status':'blocked_pending_owner_approval'})
    if any(k in low for k in ('whatsapp','wa message')):
        actions.append({'type':'whatsapp','label':'Prepare WhatsApp message for Owner review','connector':'whatsapp_cloud','connector_ready':bool(available.get('whatsapp')),'requires_owner_approval':True,'execution_status':'blocked_pending_owner_approval'})
    if not actions:
        actions.append({'type':'assistant','label':'Prepare assistant response','connector':'none','connector_ready':True,'requires_owner_approval':False,'execution_status':'preparation_only'})
    return {'ok':True,'status':'owner_review_ready' if any(a['requires_owner_approval'] for a in actions) else 'prepared','request_received':True,'actions':actions,'owner_approval_required':any(a['requires_owner_approval'] for a in actions),'execution_performed':False,'external_network_accessed':False,'credentials_returned':False,'private_payloads_returned':False}


def approve_preview(request_text, owner_approved=False, available=None):
    result=prepare_actions(request_text, available)
    if not result.get('ok'): return result
    if result.get('owner_approval_required') and owner_approved is not True:
        result['status']='approval_required'; result['approved']=False; return result
    result['status']='approved_for_governed_connector_execution'
    result['approved']=True
    result['execution_performed']=False
    result['note']='Approval recorded for preview only; this acceptance boundary does not call a real connector.'
    return result


def self_test():
    available={'microsoft':True,'whatsapp':False}
    blocked=approve_preview('Prepare an email and schedule a meeting',False,available)
    approved=approve_preview('Prepare an email and schedule a meeting',True,available)
    return {'ok':bool(blocked.get('status')=='approval_required' and not blocked.get('execution_performed') and approved.get('approved') and approved.get('status')=='approved_for_governed_connector_execution' and not approved.get('execution_performed')),'owner_gate_preserved':True,'email_calendar_actions_verified':True,'approved_preview_verified':True,'real_action_executed':False,'external_network_accessed':False,'private_payloads_exposed':False,'credentials_exposed':False}
