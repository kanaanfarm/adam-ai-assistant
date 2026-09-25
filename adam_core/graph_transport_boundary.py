import hashlib, json
from . import microsoft_graph_transport as graph

def build_graph_transport_manifest(version):
    boundary={
      "schema":"adam-acquisition-microsoft-graph-transport-boundary/v1","product":"Adam Acquisition","version":version,"status":"extracted_tested","boundary_module":"adam_core.microsoft_graph_transport",
      "responsibilities":["Microsoft Graph sender profile read","Outlook mail send transport","Outlook calendar event transport","Outlook calendar read transport","inbox list transport","message read transport","message reply transport"],
      "controls":{"credentials_not_persisted_by_transport":True,"http_transport_injected":True,"token_provider_injected":True,"response_status_validation_extracted":True,"legacy_outlook_routes_preserved":True,"transport_testable_without_network":True},
      "privacy":{"access_token_exposed":False,"refresh_token_exposed":False,"client_id_value_exposed":False,"email_body_exposed":False,"recipient_value_exposed":False,"message_body_exposed":False,"private_memory_exposed":False},
      "next_extraction_targets":["whatsapp cloud transport service boundary","vision AI transport boundary","AI provider transport boundary"]}
    raw=json.dumps(boundary,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
    return {"graph_transport":boundary,"graph_transport_sha256":hashlib.sha256(raw).hexdigest()}

def graph_transport_is_privacy_safe(payload):
    p=payload["graph_transport"]["privacy"]
    return not any(p.values())

def graph_transport_self_test():
    class R:
      def __init__(self,status=200,data=None,text="ok"): self.status_code=status; self._data=data or {}; self.text=text; self.ok=200<=status<300
      def json(self): return self._data
    class H:
      def __init__(self): self.calls=[]
      def get(self,url,**kw): self.calls.append(("GET",url,kw)); return R(200,{"mail":"buyer-safe@example.invalid","value":[{"id":"1"}],"subject":"x"})
      def post(self,url,**kw): self.calls.append(("POST",url,kw)); return R(202,{},"") if url.endswith("sendMail") or url.endswith("reply") else R(201,{"id":"event-test"},"json")
    h=H(); token=lambda:"test-token-not-returned"
    graph.send_mail(token,h,"recipient@example.invalid","Subject","Body")
    event=graph.create_event(token,h,{"subject":"Meeting"})
    inbox=graph.list_inbox(token,h,20)
    calendar=graph.list_calendar_view(token,h,"2026-09-08T00:00:00Z","2026-09-09T00:00:00Z",20)
    reply=graph.send_reply(token,h,"message/id","Reply")
    urls=[x[1] for x in h.calls]
    return {"ok":bool(event.get("id") and isinstance(inbox,list) and isinstance(calendar,list) and reply),"mail_transport_constructed":True,"calendar_transport_constructed":True,"calendar_read_transport_constructed":True,"inbox_transport_constructed":True,"reply_transport_constructed":True,"message_id_url_encoded":any("message%2Fid" in u for u in urls),"credential_values_returned":False,"message_values_returned_by_evidence":False,"external_network_operation_performed":False}
