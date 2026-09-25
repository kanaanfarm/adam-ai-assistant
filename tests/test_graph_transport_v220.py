from adam_core.graph_transport_boundary import build_graph_transport_manifest, graph_transport_is_privacy_safe, graph_transport_self_test

def test_manifest():
    p=build_graph_transport_manifest("v2.2.0")
    assert graph_transport_is_privacy_safe(p)
    assert len(p["graph_transport_sha256"])==64

def test_self_test():
    r=graph_transport_self_test()
    assert r["ok"] and not r["external_network_operation_performed"] and not r["credential_values_returned"]
