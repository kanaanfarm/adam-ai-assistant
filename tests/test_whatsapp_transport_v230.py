from adam_core.whatsapp_transport_boundary import build_whatsapp_transport_manifest, whatsapp_transport_is_privacy_safe, whatsapp_transport_self_test
from adam_core import whatsapp_cloud_transport as wa

def test_manifest_privacy_and_fingerprint():
    p=build_whatsapp_transport_manifest("v2.3.0")
    assert p["whatsapp_transport"]["status"]=="extracted_tested"
    assert whatsapp_transport_is_privacy_safe(p)
    assert len(p["whatsapp_transport_sha256"])==64

def test_self_test_is_network_free():
    r=whatsapp_transport_self_test()
    assert r["ok"] and r["message_transport_constructed"] and r["identity_transport_constructed"]
    assert r["recipient_normalization_applied"]
    assert not r["credential_values_returned"] and not r["message_values_returned_by_evidence"] and not r["external_network_operation_performed"]

def test_missing_config_rejected():
    class H: pass
    try: wa.get_identity({},H())
    except wa.WhatsAppTransportError: pass
    else: raise AssertionError("missing configuration must be rejected")

def test_app_delegates_whatsapp_cloud_transport():
    src=open('app.py',encoding='utf-8').read()
    assert 'VERSION = "v8.1.0.1"' in src
    assert 'core_wa_cloud_send_text' in src and 'core_wa_cloud_get_identity' in src
    assert '/api/acquisition/whatsapp-transport-boundary' in src
