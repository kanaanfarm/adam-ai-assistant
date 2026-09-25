from pathlib import Path
from adam_core.configuration import load_ai_settings,save_ai_settings,public_ai_status
from adam_core.configuration_boundary import build_configuration_manifest,configuration_is_privacy_safe,configuration_self_test

def test_roundtrip(tmp_path):
 p=tmp_path/"x.json"; save_ai_settings(p,"https://x/v1/","secret","model"); s=load_ai_settings(p,environ={}); assert s["api_base"]=="https://x/v1" and s["model"]=="model"
 assert public_ai_status(s)["configuration_complete"] is True
def test_manifest_safe():
 p=build_configuration_manifest("v2.9.0"); assert configuration_is_privacy_safe(p); assert len(p["configuration_service_sha256"])==64
def test_self_test():
 r=configuration_self_test(); assert r["ok"] and not r["credential_values_returned_by_evidence"] and not r["external_application_data_accessed"]
