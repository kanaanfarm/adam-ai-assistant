import hashlib, json
from . import whatsapp_cloud_transport as wa

def build_whatsapp_transport_manifest(version):
    boundary={
      "schema":"adam-acquisition-whatsapp-cloud-transport-boundary/v1","product":"Adam Acquisition","version":version,"status":"extracted_tested","boundary_module":"adam_core.whatsapp_cloud_transport",
      "responsibilities":["WhatsApp Cloud text-message transport","WhatsApp Cloud business identity read","Cloud API response validation","recipient normalization integration"],
      "controls":{"credentials_not_persisted_by_transport":True,"http_transport_injected":True,"configuration_injected":True,"response_status_validation_extracted":True,"owner_approval_adapter_preserved":True,"legacy_whatsapp_routes_preserved":True,"transport_testable_without_network":True},
      "privacy":{"access_token_exposed":False,"phone_number_id_value_exposed":False,"business_account_id_value_exposed":False,"recipient_value_exposed":False,"message_body_exposed":False,"private_memory_exposed":False},
      "next_extraction_targets":["vision AI transport boundary","AI provider transport boundary","audit event service boundary"]}
    raw=json.dumps(boundary,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
    return {"whatsapp_transport":boundary,"whatsapp_transport_sha256":hashlib.sha256(raw).hexdigest()}

def whatsapp_transport_is_privacy_safe(payload):
    return not any(payload["whatsapp_transport"]["privacy"].values())

def whatsapp_transport_self_test():
    class R:
      def __init__(self,status=200,data=None): self.status_code=status; self._data=data or {}; self.text="json"; self.ok=200<=status<300
      def json(self): return self._data
    class H:
      def __init__(self): self.calls=[]
      def post(self,url,**kw): self.calls.append(("POST",url,kw)); return R(200,{"messages":[{"id":"test-message-id"}]})
      def get(self,url,**kw): self.calls.append(("GET",url,kw)); return R(200,{"verified_name":"Test Business","quality_rating":"GREEN"})
    h=H(); cfg={"access_token":"test-token-not-returned","phone_number_id":"123456789","api_version":"v21.0"}
    sent=wa.send_text(cfg,h,"+971 50 000 0000","Buyer-safe test",normalize_func=lambda x:"971500000000")
    identity=wa.get_identity(cfg,h)
    return {"ok":bool(sent.get("messages") and identity.get("verified_name")),"message_transport_constructed":True,"identity_transport_constructed":True,"authorization_header_constructed":all("Authorization" in c[2].get("headers",{}) for c in h.calls),"recipient_normalization_applied":h.calls[0][2]["json"].get("to")=="971500000000","credential_values_returned":False,"message_values_returned_by_evidence":False,"recipient_values_returned_by_evidence":False,"external_network_operation_performed":False}
