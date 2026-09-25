"""Privacy-safe technical diligence manifest for Adam Acquisition v1.7."""
from __future__ import annotations
from hashlib import sha256
import json


def _hash(payload):
    raw=json.dumps(payload,sort_keys=True,separators=(",",":"),default=str).encode("utf-8")
    return sha256(raw).hexdigest()


def build_diligence_manifest(*, version, acquisition, governance):
    acq=dict(acquisition or {})
    gov=dict(governance or {})
    integrations=dict(acq.get("integration_configuration") or {})
    capabilities=[
        {"id":"conversation","name":"Conversational Assistant","status":"available"},
        {"id":"memory","name":"Context + Memory","status":"available"},
        {"id":"documents","name":"Document Operator","status":"available"},
        {"id":"email","name":"Outlook Email Operator","status":"configured" if integrations.get("microsoft_client_configured") else "configuration_required"},
        {"id":"calendar","name":"Calendar Operator","status":"configured" if integrations.get("microsoft_client_configured") else "configuration_required"},
        {"id":"whatsapp","name":"WhatsApp Business Operator","status":"configured" if integrations.get("whatsapp_configured") else "configuration_required"},
        {"id":"market_data","name":"Paper Market Data / Trading","status":"configured" if integrations.get("alpaca_paper_configured") else "configuration_required"},
        {"id":"governance","name":"Owner Approval + Audit Governance","status":"available"},
    ]
    risks=[
        {"id":"credentials","severity":"controlled","control":"Credentials are excluded from buyer evidence and supplied only by deployment environment."},
        {"id":"consequential_actions","severity":"controlled","control":"Email, WhatsApp and calendar execution require owner approval and execution confirmation."},
        {"id":"live_trading","severity":"controlled","control":"Live trading is blocked in the acquisition build."},
        {"id":"privacy","severity":"controlled","control":"Buyer evidence excludes contact details, message bodies, attachment contents and private memory values."},
        {"id":"architecture","severity":"attention","control":"Architecture extraction is active: acquisition assembly plus Contacts and Follow-Up data services now run through tested adam_core modules; see /api/acquisition/architecture and /api/acquisition/service-boundaries for migration evidence."},
    ]
    manifest={
        "schema":"adam-acquisition-diligence/v1",
        "product":"Adam Acquisition",
        "version":version,
        "positioning":acq.get("positioning"),
        "core_checks_pass":bool(acq.get("all_core_checks_pass")),
        "capabilities":capabilities,
        "governance":{
            "workflow_count":int(gov.get("workflow_count") or 0),
            "approval_events":int(gov.get("approval_events") or 0),
            "completion_events":int(gov.get("completion_events") or 0),
            "owner_approval_required_for":list((gov.get("policy") or {}).get("owner_approval_required_for") or []),
        },
        "risks":risks,
        "evidence_endpoints":[
            "/api/health","/api/governance","/api/acquisition/readiness",
            "/api/acquisition/demo-scenarios","/api/acquisition/evidence-pack",
            "/api/acquisition/diligence","/api/acquisition/architecture","/api/acquisition/service-boundaries"
        ],
        "privacy":{
            "credentials_exposed":False,"contact_details_exposed":False,
            "message_bodies_exposed":False,"attachment_contents_exposed":False,
            "private_memory_exposed":False,
        },
    }
    return {"manifest":manifest,"manifest_sha256":_hash(manifest)}


def diligence_is_privacy_safe(payload):
    text=json.dumps(payload or {},sort_keys=True,default=str).lower()
    forbidden=("api_key","access_token","refresh_token","client_secret","password","contact_email","phone_number","message_body","attachment_body","private_memory_value")
    return not any(x in text for x in forbidden)
