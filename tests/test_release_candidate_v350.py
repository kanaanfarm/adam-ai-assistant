from adam_core.release_candidate import build_release_candidate_manifest, release_candidate_is_privacy_safe, release_candidate_self_test

def test_release_candidate_manifest_contract():
    p=build_release_candidate_manifest("v3.5.0")
    rc=p["release_candidate"]
    assert rc["version"]=="v3.5.0"
    assert rc["status"]=="release_candidate_tested"
    assert rc["candidate_label"]=="RC1"
    assert len(rc["handoff_artifacts"])==5
    assert len(rc["release_gates"])==4
    assert len(p["release_candidate_sha256"])==64
    assert release_candidate_is_privacy_safe(p)

def test_release_candidate_self_test_contract():
    r=release_candidate_self_test()
    assert r["ok"]
    assert r["rc1_label_verified"]
    assert r["five_handoff_artifacts_verified"]
    assert r["four_release_gates_verified"]
    assert r["credential_free_distribution_verified"]
    assert r["personal_data_free_distribution_verified"]
    assert r["owner_controls_retained_verified"]
    assert r["diligence_disclosures_retained_verified"]
    assert r["privacy_projection_verified"]
    assert not r["external_network_accessed"]
    assert not r["external_application_data_accessed"]
    assert not r["private_values_returned"]
