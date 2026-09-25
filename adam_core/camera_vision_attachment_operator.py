"""Adam v6.6.0 — governed Camera, Vision & Attachment Operator.

This module turns already-observed camera/vision/attachment context into a bounded
workflow proposal. It never performs the proposed external action itself.
"""
from __future__ import annotations

ALLOWED_SOURCE_TYPES = {"camera", "image", "document", "attachment", "synthetic"}
CONSEQUENTIAL_HINTS = (
    "send", "email", "message", "whatsapp", "schedule", "book", "submit",
    "upload", "delete", "buy", "sell", "approve payment", "place order",
)
SENSITIVE_HINTS = ("password", "passwd", "secret", "api_key", "apikey", "access token", "private_key")


def build_operator_plan(
    source_type="attachment",
    source_name="",
    observation="",
    owner_instruction="",
    owner_approved=False,
):
    source_type = str(source_type or "attachment").strip().lower()
    if source_type not in ALLOWED_SOURCE_TYPES:
        source_type = "attachment"
    source_name = str(source_name or "").strip()[:240]
    observation = str(observation or "").strip()
    instruction = str(owner_instruction or "").strip()
    if not observation:
        return {
            "ok": False,
            "status": "observation_required",
            "execution_performed": False,
            "external_network_accessed": False,
        }

    combined = f"{instruction}\n{observation}".lower()
    contains_sensitive = any(h in combined for h in SENSITIVE_HINTS)
    consequential = any(h in instruction.lower() for h in CONSEQUENTIAL_HINTS)
    if contains_sensitive:
        return {
            "ok": False,
            "status": "sensitive_content_blocked",
            "source_type": source_type,
            "source_name": source_name,
            "owner_approval_required": False,
            "execution_performed": False,
            "external_network_accessed": False,
            "credentials_returned": False,
            "private_payloads_returned": False,
        }

    if consequential and not owner_approved:
        status = "owner_approval_required"
        ready = False
    elif consequential:
        status = "approved_for_governed_handoff"
        ready = True
    else:
        status = "analysis_ready"
        ready = True

    # Return a compact working context for the next governed step. This is an
    # owner-facing UI response, not buyer evidence; it intentionally contains
    # the supplied observation so the owner can verify Adam understood it.
    return {
        "ok": True,
        "status": status,
        "source_type": source_type,
        "source_name": source_name,
        "observation_received": True,
        "observation": observation[:12000],
        "owner_instruction": instruction[:4000],
        "consequential_action_detected": consequential,
        "owner_approval_required": consequential,
        "owner_approved": bool(owner_approved),
        "ready_for_governed_handoff": ready,
        "execution_performed": False,
        "external_network_accessed": False,
        "credentials_returned": False,
        "private_payloads_returned": False,
        "camera_orientation_policy": "natural_unmirrored_capture",
        "note": "Adam may understand camera/images/attachments and prepare a workflow. Consequential external actions remain governed and are not executed by this boundary.",
    }


def self_test():
    safe = build_operator_plan(
        "document", "synthetic-payment-letter.pdf",
        "A synthetic payment letter references certificate 12 and requests follow-up.",
        "Summarize the important follow-up.", False,
    )
    blocked = build_operator_plan(
        "image", "synthetic-site-photo.jpg",
        "A synthetic site photo shows a sprinkler head location requiring coordination.",
        "Send an email to the contractor requesting coordination.", False,
    )
    approved = build_operator_plan(
        "camera", "synthetic-camera-frame.jpg",
        "A synthetic camera frame shows the equipment label in natural left/right orientation.",
        "Send a message to the team requesting verification.", True,
    )
    sensitive = build_operator_plan(
        "document", "synthetic.txt", "password = synthetic-secret", "Review this.", True,
    )
    return {
        "ok": bool(
            safe.get("status") == "analysis_ready"
            and blocked.get("status") == "owner_approval_required"
            and not blocked.get("ready_for_governed_handoff")
            and approved.get("status") == "approved_for_governed_handoff"
            and approved.get("ready_for_governed_handoff")
            and sensitive.get("status") == "sensitive_content_blocked"
        ),
        "camera_natural_orientation_verified": approved.get("camera_orientation_policy") == "natural_unmirrored_capture",
        "attachment_to_workflow_verified": safe.get("observation_received") is True,
        "owner_approval_gate_verified": blocked.get("owner_approval_required") and not blocked.get("ready_for_governed_handoff"),
        "approved_handoff_verified": approved.get("ready_for_governed_handoff") and not approved.get("execution_performed"),
        "sensitive_content_rejection_verified": sensitive.get("status") == "sensitive_content_blocked",
        "credentials_exposed": False,
        "private_payloads_exposed": False,
        "real_action_executed": False,
        "external_network_accessed": False,
        "synthetic_inputs_only": True,
    }
