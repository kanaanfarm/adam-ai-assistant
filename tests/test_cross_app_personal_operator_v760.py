from adam_core.cross_app_personal_operator import prepare_workflow, execute_workflow, self_test

CONTACTS=[{"name":"Engineer Test","email":"eng@example.com","phone":"+971500000000"}]

def payload():
    return {"contact_name":"Engineer Test","objective":"Coordinate HVAC submission","include_document":True,"document_name":"HVAC.pdf","include_email":True,"email_subject":"HVAC","email_body":"Please review","include_calendar":True,"meeting_title":"HVAC","meeting_start":"2030-01-02T10:00","include_whatsapp":True,"whatsapp_message":"Please confirm","include_followup":True,"followup_title":"Follow up"}

def test_cross_app_preview_is_six_domains_and_safe():
    r=prepare_workflow(payload(), CONTACTS, microsoft_ready=True, whatsapp_ready=True)
    assert r["ok"] is True
    assert r["selected_domains"] == ["contacts","documents","email","calendar","whatsapp","followup"]
    assert r["external_action_executed"] is False
    assert r["private_payloads_returned"] is False

def test_cross_app_execution_requires_per_action_approval():
    calls=[]
    adapters={"email":lambda **kw:calls.append("email"),"calendar":lambda **kw:calls.append("calendar"),"whatsapp":lambda **kw:calls.append("whatsapp"),"followup":lambda **kw:calls.append("followup")}
    r=execute_workflow(payload(), CONTACTS, adapters, microsoft_ready=True, whatsapp_ready=True)
    assert r["executed_count"] == 0
    assert calls == []
    p=payload(); p["approvals"]={"email":True,"calendar":True,"whatsapp":True,"followup":True}
    r=execute_workflow(p, CONTACTS, adapters, microsoft_ready=True, whatsapp_ready=True)
    assert r["executed_count"] == 4
    assert calls == ["email","calendar","whatsapp","followup"]

def test_cross_app_personal_operator_self_test():
    assert self_test()["ok"] is True
