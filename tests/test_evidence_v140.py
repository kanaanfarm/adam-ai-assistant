from adam_core.evidence import build_evidence_pack, evidence_pack_is_privacy_safe


def sample_acquisition():
    return {
        "positioning": "AI operator",
        "all_core_checks_pass": True,
        "readiness_checks": {"owner_approval_enforced": True, "privacy_safe_governance": True},
        "demo_scenarios": [
            {"id": "email_document_operator", "name": "Email + Document Operator", "approval_required": True, "evidence_endpoints": ["/api/governance"]}
        ],
    }


def sample_governance():
    return {
        "workflow_count": 1,
        "completed_workflows": 0,
        "attention_required": 0,
        "approval_events": 1,
        "completion_events": 0,
        "record_sources": {"followups": 1, "orchestration_workflows": 0},
        "policy": {"credentials_exposed": False, "attachment_context_exposed": False},
        "receipts": [{"workflow_id": "followup_123", "status": "pending", "approval_events": 0, "completion_events": 0, "receipt_sha256": "a" * 64}],
    }


def test_evidence_pack_has_sha256_and_version():
    pack = build_evidence_pack(version="v1.4.0", acquisition=sample_acquisition(), governance=sample_governance())
    assert pack["evidence"]["version"] == "v1.4.0"
    assert len(pack["evidence_sha256"]) == 64


def test_evidence_pack_preserves_only_safe_receipt_metadata():
    pack = build_evidence_pack(version="v1.4.0", acquisition=sample_acquisition(), governance=sample_governance())
    receipt = pack["evidence"]["workflow_receipts"][0]
    assert set(receipt) == {"workflow_id", "status", "approval_events", "completion_events", "receipt_sha256"}


def test_evidence_pack_privacy_boundary_is_false():
    pack = build_evidence_pack(version="v1.4.0", acquisition=sample_acquisition(), governance=sample_governance())
    assert all(v is False for v in pack["evidence"]["privacy"].values())
    assert evidence_pack_is_privacy_safe(pack) is True


def test_evidence_fingerprint_changes_when_governance_changes():
    a = build_evidence_pack(version="v1.4.0", acquisition=sample_acquisition(), governance=sample_governance())
    changed = sample_governance()
    changed["workflow_count"] = 2
    b = build_evidence_pack(version="v1.4.0", acquisition=sample_acquisition(), governance=changed)
    assert a["evidence_sha256"] != b["evidence_sha256"]
