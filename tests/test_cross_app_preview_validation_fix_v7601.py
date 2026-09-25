from pathlib import Path
from adam_core.cross_app_personal_operator import prepare_workflow, execute_workflow


def _base():
    return {
        "contact_name":"Mohad", "email":"mohad@example.com", "phone":"+971500000000",
        "objective":"Send HVAC drawing, arrange meeting, notify WhatsApp, create follow-up",
        "include_document":True, "document_name":"HVAC Shop Drawing.pdf",
        "include_email":True, "email_subject":"HVAC coordination", "email_body":"Please review.",
        "include_calendar":True, "meeting_title":"HVAC coordination", "meeting_start":"2030-01-02T10:00",
        "include_whatsapp":True, "whatsapp_message":"Please confirm",
        "include_followup":True, "followup_title":"Follow Up",
    }


def test_preview_is_valid_even_when_execution_connectors_are_not_ready():
    r=prepare_workflow(_base(), [], microsoft_ready=False, whatsapp_ready=False)
    assert r["ok"] is True
    assert r["preview_ready"] is True
    assert r["status"] == "cross_app_workflow_preview_ready"
    assert r["external_action_executed"] is False
    assert r["connector_readiness_required_for_preview"] is False
    assert "email_connector_not_ready" in r["execution_blockers"]
    assert "whatsapp_connector_not_ready" in r["execution_blockers"]


def test_preview_can_plan_selected_action_with_execution_detail_warning():
    p=_base(); p["email_body"]=""
    r=prepare_workflow(p, [], microsoft_ready=False, whatsapp_ready=False)
    assert r["ok"] is True
    assert "email_details" in r["execution_blockers"]
    assert r["missing"] == []


def test_execute_still_requires_execution_details():
    p=_base(); p["email_body"]=""; p["approvals"]={"email":True}
    r=execute_workflow(p, [], {}, microsoft_ready=True, whatsapp_ready=True)
    assert r["ok"] is False
    assert r["status"] == "workflow_not_ready_for_execution"
    assert "email_details" in r["execution_missing"]


def test_version_bumped():
    app=Path("app.py").read_text()
    assert 'VERSION = "v8.1.0.1"' in app
