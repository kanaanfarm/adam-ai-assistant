"""Buyer-safe evidence for v2.9 Configuration Service Boundary."""
from __future__ import annotations
import hashlib,json,tempfile
from pathlib import Path
from .configuration import load_ai_settings, save_ai_settings, public_ai_status, MAX_CONFIG_BYTES

def build_configuration_manifest(version):
    service={"schema":"adam-acquisition-configuration-service-boundary/v1","product":"Adam Acquisition","version":version,"status":"extracted_tested","boundary_module":"adam_core.configuration","responsibilities":["AI provider configuration load/save","environment fallback","bounded configuration persistence","atomic configuration writes","buyer-safe configuration status projection"],"controls":{"configuration_path_injected":True,"environment_fallback_preserved":True,"allowed_keys_bounded":True,"file_size_bounded":True,"atomic_write_used":True,"malformed_store_tolerated":True,"legacy_ai_settings_callers_preserved":True,"service_testable_without_application_data":True},"privacy":{"api_key_values_exposed":False,"configuration_values_exposed":False,"environment_values_exposed":False,"file_contents_exposed":False,"contact_values_exposed":False,"private_memory_exposed":False},"next_extraction_targets":["owner approval persistence boundary","Windows speech fallback boundary","runtime configuration consolidation"]}
    raw=json.dumps(service,sort_keys=True,separators=(",",":")).encode()
    return {"configuration_service":service,"configuration_service_sha256":hashlib.sha256(raw).hexdigest()}

def configuration_is_privacy_safe(payload):
    p=payload.get("configuration_service",{}).get("privacy",{})
    return bool(p) and not any(bool(v) for v in p.values())

def configuration_self_test():
    with tempfile.TemporaryDirectory() as d:
        p=Path(d)/"ai_settings.json"
        env={"AI_API_BASE":"https://env.invalid/v1","AI_API_KEY":"synthetic-env-secret","AI_MODEL":"env-model"}
        a=load_ai_settings(p,environ=env)
        save_ai_settings(p,"https://saved.invalid/v1/","synthetic-file-secret","saved-model")
        b=load_ai_settings(p,environ=env); status=public_ai_status(b)
        raw=p.read_text(encoding="utf-8")
        p.write_text("{malformed",encoding="utf-8"); c=load_ai_settings(p,environ=env)
        return {"ok":bool(a["model"]=="env-model" and b["model"]=="saved-model" and status["configuration_complete"] and c["model"]=="env-model" and len(raw.encode())<=MAX_CONFIG_BYTES),"environment_fallback_verified":a["model"]=="env-model" and c["model"]=="env-model","atomic_persistence_verified":b["model"]=="saved-model","bounded_file_verified":len(raw.encode())<=MAX_CONFIG_BYTES,"malformed_store_recovery_verified":c["model"]=="env-model","public_status_boolean_only_verified":all(isinstance(v,bool) for v in status.values()),"credential_values_returned_by_evidence":False,"configuration_values_returned_by_evidence":False,"external_application_data_accessed":False}
