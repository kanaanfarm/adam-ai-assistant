from adam_core.buyer_handoff import build_buyer_handoff_manifest, buyer_handoff_is_privacy_safe, buyer_handoff_self_test

def test_buyer_handoff_manifest():
    p=build_buyer_handoff_manifest("v3.6.0")
    h=p["buyer_handoff"]
    assert h["version"]=="v3.6.0"
    assert h["status"]=="buyer_handoff_tested"
    assert h["source_release"]=="v3.5.0 RC1"
    assert len(h["review_components"])==7
    assert len(h["review_gates"])==5
    assert len(p["buyer_handoff_sha256"])==64
    assert buyer_handoff_is_privacy_safe(p)

def test_buyer_handoff_self_test():
    s=buyer_handoff_self_test()
    assert s["ok"]
    assert s["seven_review_components_verified"]
    assert s["five_review_gates_verified"]
    assert s["privacy_projection_verified"]
    assert not s["external_network_accessed"]
    assert not s["private_values_returned"]
