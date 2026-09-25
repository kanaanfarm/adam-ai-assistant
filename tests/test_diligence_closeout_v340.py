from adam_core.diligence_closeout import build_diligence_closeout, diligence_closeout_is_privacy_safe, diligence_closeout_self_test

def test_closeout_manifest_is_buyer_safe_and_complete():
    p=build_diligence_closeout("v3.4.0")
    c=p["technical_diligence_closeout"]
    assert c["status"]=="closeout_tested"
    assert len(c["closeout_domains"])==6
    assert len(c["remaining_disclosures"])==3
    assert diligence_closeout_is_privacy_safe(p)
    assert len(p["technical_diligence_closeout_sha256"])==64

def test_closeout_self_test_is_network_free():
    r=diligence_closeout_self_test()
    assert r["ok"] and r["six_closeout_domains_verified"] and r["remaining_disclosures_visible_verified"]
    assert r["owner_gate_control_verified"] and r["live_trading_block_verified"] and r["synthetic_diligence_verified"]
    assert r["privacy_projection_verified"] and not r["external_network_accessed"] and not r["external_application_data_accessed"] and not r["private_values_returned"]
