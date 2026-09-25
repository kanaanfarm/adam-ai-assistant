from adam_core.governance import policy_manifest, workflow_receipt, governance_summary
from adam_core.orchestration import new_workflow, mark_approved, mark_completed


def test_policy_keeps_consequential_actions_gated():
    p=policy_manifest()
    assert set(p["owner_approval_required_for"]) == {"email_review","whatsapp_review","calendar_review"}
    assert p["execution_confirmation_required"] is True
    assert p["attachment_context_exposed"] is False


def test_receipt_excludes_sensitive_context_and_details():
    w=new_workflow("Email the approved response", ["email_review"], "SECRET ATTACHMENT BODY")
    mark_approved(w,"email_review")
    mark_completed(w,"email_review", {"email":"secret@example.com","body":"SECRET EMAIL BODY"})
    r=workflow_receipt(w)
    text=str(r)
    assert "SECRET ATTACHMENT BODY" not in text
    assert "SECRET EMAIL BODY" not in text
    assert "secret@example.com" not in text
    assert len(r["receipt_sha256"]) == 64


def test_receipt_is_stable_for_same_safe_state():
    w=new_workflow("Review and email", ["prepare_document","email_review"])
    assert workflow_receipt(w)["receipt_sha256"] == workflow_receipt(w)["receipt_sha256"]


def test_summary_counts_governance_events():
    w=new_workflow("Email", ["email_review"])
    mark_approved(w,"email_review"); mark_completed(w,"email_review", {"execution_confirmed":True})
    s=governance_summary([w])
    assert s["workflow_count"] == 1
    assert s["completed_workflows"] == 1
    assert s["approval_events"] == 1
    assert s["completion_events"] == 1
