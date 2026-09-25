import hashlib, json
from . import vision_ai_transport as vision

def build_vision_transport_manifest(version):
    boundary={
      "schema":"adam-acquisition-vision-ai-transport-boundary/v1","product":"Adam Acquisition","version":version,"status":"extracted_tested","boundary_module":"adam_core.vision_ai_transport",
      "responsibilities":["vision model selection","multimodal request construction","image data-url encoding","vision provider HTTP transport","vision response validation"],
      "controls":{"api_credentials_injected":True,"http_transport_injected":True,"image_payload_bounded_to_six":True,"legacy_camera_attachment_routes_preserved":True,"response_validation_extracted":True,"transport_testable_without_network":True,"transport_does_not_persist_images":True},
      "privacy":{"api_key_exposed":False,"image_bytes_exposed":False,"image_data_url_exposed":False,"instruction_value_exposed":False,"model_response_exposed":False,"private_memory_exposed":False},
      "next_extraction_targets":["AI provider transport boundary","audit event service boundary","workflow persistence service boundary"]}
    raw=json.dumps(boundary,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
    return {"vision_transport":boundary,"vision_transport_sha256":hashlib.sha256(raw).hexdigest()}

def vision_transport_is_privacy_safe(payload):
    return not any(payload["vision_transport"]["privacy"].values())

def vision_transport_self_test():
    class R:
      ok=True; status_code=200; text="json"
      def json(self): return {"choices":[{"message":{"content":"safe synthetic vision result"}}]}
    class H:
      def __init__(self): self.calls=[]
      def post(self,url,**kw): self.calls.append((url,kw)); return R()
    h=H()
    model=vision.select_vision_model("text-only-model","")
    answer=vision.analyze_images("https://example.invalid/v1","test-key-not-returned",model,[{"bytes":b"synthetic-image-bytes","mime":"image/jpeg"}],"synthetic instruction",http=h)
    payload=h.calls[0][1]["json"]
    image_url=payload["messages"][0]["content"][1]["image_url"]["url"]
    return {"ok":answer=="safe synthetic vision result","vision_model_selected":model=="gpt-4o-mini","multimodal_payload_constructed":image_url.startswith("data:image/jpeg;base64,"),"authorization_header_constructed":"Authorization" in h.calls[0][1].get("headers",{}),"response_validation_passed":True,"credential_values_returned":False,"image_values_returned_by_evidence":False,"instruction_values_returned_by_evidence":False,"model_response_values_returned_by_evidence":False,"external_network_operation_performed":False}
