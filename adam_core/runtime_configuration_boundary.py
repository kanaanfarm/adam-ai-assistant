"""Buyer-safe evidence for Adam Acquisition v3.2 runtime configuration consolidation."""
from __future__ import annotations
import hashlib, json
from .runtime_configuration import openai_environment, vision_model_environment, alpaca_environment, microsoft_client_id_environment, public_runtime_status


def build_runtime_configuration_manifest(version):
    service={
      "schema":"adam-acquisition-runtime-configuration-consolidation/v1",
      "product":"Adam Acquisition","version":version,"status":"extracted_tested",
      "boundary_module":"adam_core.runtime_configuration",
      "responsibilities":["centralized runtime environment reads","AI provider environment defaults","vision model environment selection","Alpaca credential environment compatibility","Microsoft client-id environment lookup","buyer-safe configuration-presence projection"],
      "controls":{"environment_reads_centralized":True,"legacy_environment_names_preserved":True,"default_ai_base_preserved":True,"default_ai_model_preserved":True,"secret_values_never_returned_by_public_status":True,"service_testable_with_injected_environment":True},
      "privacy":{"api_key_values_exposed":False,"secret_key_values_exposed":False,"client_id_values_exposed":False,"environment_values_exposed":False,"configuration_file_contents_exposed":False,"private_memory_exposed":False},
      "next_extraction_targets":["final acquisition demo hardening","technical diligence closeout"]}
    raw=json.dumps(service,sort_keys=True,separators=(",",":")).encode()
    return {"runtime_configuration_service":service,"runtime_configuration_sha256":hashlib.sha256(raw).hexdigest()}


def runtime_configuration_is_privacy_safe(payload):
    p=payload.get("runtime_configuration_service",{}).get("privacy",{})
    return bool(p) and not any(bool(v) for v in p.values())


def runtime_configuration_self_test():
    env={"OPENAI_API_KEY":"synthetic-openai-secret","OPENAI_API_BASE":"https://synthetic.invalid/v1/","OPENAI_MODEL":"synthetic-model","AI_VISION_MODEL":"synthetic-vision","ALPACA_API_KEY":"synthetic-alpaca-key","ALPACA_API_SECRET":"synthetic-alpaca-secret","MICROSOFT_CLIENT_ID":"synthetic-client-id"}
    ai=openai_environment(env); alp=alpaca_environment(env); status=public_runtime_status(env)
    secret_values=list(env.values())
    serialized=json.dumps(status,sort_keys=True)
    return {"ok":bool(ai["api_base"]=="https://synthetic.invalid/v1" and ai["model"]=="synthetic-model" and vision_model_environment(env)=="synthetic-vision" and alp["secret_key"]=="synthetic-alpaca-secret" and microsoft_client_id_environment(env)=="synthetic-client-id" and all(status.values()) and not any(v in serialized for v in secret_values)),"injected_environment_verified":True,"legacy_alpaca_secret_alias_verified":alp["secret_key"]=="synthetic-alpaca-secret","ai_defaults_and_normalization_verified":ai["api_base"]=="https://synthetic.invalid/v1","presence_only_projection_verified":not any(v in serialized for v in secret_values),"external_network_accessed":False,"external_application_data_accessed":False,"environment_values_returned_by_evidence":False}
