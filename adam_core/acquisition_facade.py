"""Acquisition output facade for Adam Acquisition v1.6.

This module centralizes buyer-facing acquisition payload assembly so Flask routes
remain thin adapters. It deliberately returns only privacy-safe metadata.
"""
from __future__ import annotations

from adam_core.acquisition import acquisition_readiness
from adam_core.diagnostics import build_health_payload
from adam_core.diligence import build_diligence_manifest
from adam_core.evidence import build_evidence_pack
from adam_core.governance import governance_summary


def build_acquisition_outputs(*, version, app_name, base_dir, governance_rows, workflow_only_count, followup_count):
    gov = governance_summary(list(governance_rows or []))
    gov["record_sources"] = {
        "orchestration_workflows": int(workflow_only_count or 0),
        "followups": int(followup_count or 0),
    }
    runtime = build_health_payload(app_name=app_name, version=version, base_dir=base_dir)
    acq = acquisition_readiness(
        version=version,
        governance=gov,
        runtime=runtime,
        record_sources=gov["record_sources"],
    )
    evidence = build_evidence_pack(version=version, acquisition=acq, governance=gov)
    diligence = build_diligence_manifest(version=version, acquisition=acq, governance=gov)
    return {
        "governance": gov,
        "runtime": runtime,
        "acquisition": acq,
        "evidence_pack": evidence,
        "diligence": diligence,
    }
