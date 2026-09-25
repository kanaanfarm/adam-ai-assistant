from pathlib import Path

APP = Path(__file__).resolve().parents[1] / "app.py"
FOLLOWUPS = Path(__file__).resolve().parents[1] / "templates" / "followups.html"

def test_version_is_current_acquisition_build():
    text=APP.read_text(encoding="utf-8")
    assert 'VERSION = "v8.1.0.1"' in text

def test_followup_creation_resolves_saved_contact():
    text=APP.read_text(encoding="utf-8")
    assert 'def adam_resolve_followup_contact_v113' in text
    assert 'matched=find_contact_in_instruction(instruction,contacts)' in text
    assert 'follow[- ]?up' in text
    assert 'find_contact_by_name_v06919(m.group(1)' in text
    assert 'resolved=adam_resolve_followup_contact_v113(' in text

def test_draft_reply_late_resolves_missing_contact():
    text=APP.read_text(encoding="utf-8")
    assert 'if not str(item.get("contact_email") or "").strip():' in text
    assert 'adam_followups_save_v0700(rows)' in text

def test_followup_ui_shows_contact_link_state():
    text=FOLLOWUPS.read_text(encoding="utf-8")
    assert 'Not linked to Adam Contacts' in text

def test_workflow_api_exposes_safe_status_metadata():
    text=APP.read_text(encoding="utf-8")
    assert '"workflow_count":len(public_rows)' in text
    assert '"privacy":{"attachment_context_exposed":False}' in text
