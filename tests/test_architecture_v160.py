from adam_core.architecture import build_architecture_manifest, architecture_is_privacy_safe
from adam_core.acquisition_facade import build_acquisition_outputs
from pathlib import Path


def test_architecture_manifest_is_versioned_and_fingerprinted():
    p = build_architecture_manifest(version="v1.6.0")
    assert p["architecture"]["version"] == "v1.6.0"
    assert p["architecture"]["schema"] == "adam-acquisition-architecture/v1"
    assert len(p["architecture_sha256"]) == 64


def test_architecture_manifest_has_extracted_modules_and_honest_legacy_boundary():
    p = build_architecture_manifest(version="v1.6.0")["architecture"]
    assert p["module_count"] >= 9
    assert p["migration_controls"]["thin_acquisition_routes"] is True
    assert p["legacy_boundary"]["status"] == "migration_in_progress"
    assert "workflow persistence service boundary" in p["next_extraction_targets"]


def test_architecture_manifest_privacy_safe():
    assert architecture_is_privacy_safe(build_architecture_manifest(version="v1.6.0")) is True
    assert architecture_is_privacy_safe({"client_secret": "bad"}) is False


def test_acquisition_facade_builds_all_buyer_outputs(tmp_path):
    out = build_acquisition_outputs(
        version="v1.6.0",
        app_name="Adam Acquisition",
        base_dir=Path(tmp_path),
        governance_rows=[],
        workflow_only_count=0,
        followup_count=0,
    )
    assert set(out) == {"governance", "runtime", "acquisition", "evidence_pack", "diligence"}
    assert out["acquisition"]["version"] == "v1.6.0"
    assert len(out["evidence_pack"]["evidence_sha256"]) == 64
    assert len(out["diligence"]["manifest_sha256"]) == 64
