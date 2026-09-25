from pathlib import Path
from adam_core.post_meeting_followup import preview_followup, execute_followup


def test_v481_post_meeting_routes_are_declared_before_server_start():
    src = Path("app.py").read_text(encoding="utf-8")
    main_pos = src.index('if __name__ == "__main__":')
    for route in (
        '@app.route("/post-meeting-followup")',
        '@app.route("/api/post-meeting-followup", methods=["POST"])',
        '@app.route("/api/acquisition/post-meeting-followup")',
        '@app.route("/api/acquisition/post-meeting-followup/self-test")',
    ):
        assert src.index(route) < main_pos


def test_v481_acquisition_template_is_validly_wrapped_and_has_v48_controls():
    text = Path("templates/acquisition.html").read_text(encoding="utf-8")
    assert text.count("</html>") == 1
    assert text.count("</body>") == 1
    assert text.rstrip().endswith("</html>")
    assert "Post-Meeting Cross-App Follow-Up — v4.8" in text
    assert 'href="/post-meeting-followup"' in text
    assert "width:min(1500px" in text


def test_v481_post_meeting_interactive_owner_gate_core_contract():
    actions = [
        {"connector":"email","action":"draft","summary":"Prepare follow-up"},
        {"connector":"calendar","action":"invite","summary":"Schedule review","owner_approved":False},
    ]
    preview = preview_followup(actions)
    assert preview["status"] == "followup_preview_ready"
    adapters = {"email": lambda action: True, "calendar": lambda action: True}
    blocked = execute_followup(actions, adapters)
    assert blocked["status"] == "approval_required"
    actions[1]["owner_approved"] = True
    done = execute_followup(actions, adapters)
    assert done["status"] == "followup_completed"
    assert done["owner_gate_preserved"] is True
    assert done["audit_receipts_generated"] is True
