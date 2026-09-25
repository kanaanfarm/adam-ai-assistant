from adam_core.orchestration import new_workflow, mark_approved, mark_completed, public_summary

def test_consequential_steps_are_approval_gated():
    w = new_workflow("review and email", ["analyze_source","prepare_document","email_review"])
    email = next(s for s in w["steps"] if s["name"]=="email_review")
    analysis = next(s for s in w["steps"] if s["name"]=="analyze_source")
    assert email["approval_required"] is True
    assert analysis["approval_required"] is False

def test_approval_and_execution_are_separate_events():
    w = new_workflow("email", ["email_review"])
    assert mark_approved(w,"email_review")
    assert w["steps"][0]["status"] == "approved"
    assert any(e["type"]=="owner_approved" for e in w["events"])
    assert mark_completed(w,"email_review",{"execution_confirmed":True})
    assert w["steps"][0]["status"] == "completed"
    assert w["status"] == "completed"
    assert any(e["type"]=="step_completed" for e in w["events"])

def test_public_summary_does_not_expose_attachment_context():
    w = new_workflow("review", ["analyze_source"], "PRIVATE ATTACHMENT TEXT")
    s = public_summary(w)
    assert "attachment_context" not in s
    assert "PRIVATE ATTACHMENT TEXT" not in str(s)
