from adam_core.camera_vision_attachment_operator import build_operator_plan, self_test


def test_v660_self_test_is_synthetic_and_safe():
    r = self_test()
    assert r["ok"]
    assert r["camera_natural_orientation_verified"]
    assert r["attachment_to_workflow_verified"]
    assert r["owner_approval_gate_verified"]
    assert r["sensitive_content_rejection_verified"]
    assert r["synthetic_inputs_only"]
    assert not r["real_action_executed"]
    assert not r["external_network_accessed"]


def test_v660_consequential_attachment_handoff_requires_owner_approval():
    r = build_operator_plan(
        "image", "synthetic-site-photo.jpg",
        "A synthetic site photo shows a sprinkler head location requiring coordination.",
        "Send an email to the contractor requesting coordination.", False,
    )
    assert r["status"] == "owner_approval_required"
    assert r["consequential_action_detected"]
    assert r["owner_approval_required"]
    assert not r["owner_approved"]
    assert not r["ready_for_governed_handoff"]
    assert not r["execution_performed"]
    assert r["camera_orientation_policy"] == "natural_unmirrored_capture"
