"""Buyer-safe architecture progress manifest for Adam Acquisition v2.6."""
from __future__ import annotations

from hashlib import sha256
import json


CORE_MODULES = [
    {"module": "adam_core.runtime_configuration", "responsibility": "centralized runtime environment configuration and presence-only projection", "status": "extracted_tested"},
    {"module": "adam_core.runtime_configuration_boundary", "responsibility": "privacy-safe runtime configuration consolidation evidence", "status": "extracted_tested"},
    {"module": "adam_core.runtime", "responsibility": "secure runtime secret and persistent root", "status": "extracted_tested"},
    {"module": "adam_core.diagnostics", "responsibility": "buyer-safe health diagnostics", "status": "extracted_tested"},
    {"module": "adam_core.orchestration", "responsibility": "workflow state and approval separation", "status": "extracted_tested"},
    {"module": "adam_core.workflow_persistence", "responsibility": "bounded atomic workflow persistence", "status": "extracted_tested"},
    {"module": "adam_core.approval_persistence", "responsibility": "bounded atomic owner-approval receipt persistence", "status": "extracted_tested"},
    {"module": "adam_core.approval_persistence_boundary", "responsibility": "privacy-safe owner-approval persistence evidence", "status": "extracted_tested"},
    {"module": "adam_core.governance", "responsibility": "policy, receipts and privacy-safe governance", "status": "extracted_tested"},
    {"module": "adam_core.acquisition", "responsibility": "readiness and demo scenario metadata", "status": "extracted_tested"},
    {"module": "adam_core.evidence", "responsibility": "buyer evidence pack and fingerprint", "status": "extracted_tested"},
    {"module": "adam_core.diligence", "responsibility": "technical diligence manifest and risk register", "status": "extracted_tested"},
    {"module": "adam_core.diligence_closeout", "responsibility": "privacy-safe technical diligence closeout evidence and remaining disclosures", "status": "extracted_tested"},
    {"module": "adam_core.acquisition_facade", "responsibility": "central buyer-output assembly separated from Flask routes", "status": "extracted_tested"},
    {"module": "adam_core.architecture", "responsibility": "architecture migration evidence", "status": "extracted_tested"},
    {"module": "adam_core.contacts", "responsibility": "contact persistence validation and safe upsert", "status": "extracted_tested"},
    {"module": "adam_core.followups", "responsibility": "follow-up persistence, due parsing and status projection", "status": "extracted_tested"},
    {"module": "adam_core.service_boundaries", "responsibility": "service-boundary migration evidence", "status": "extracted_tested"},
    {"module": "adam_core.connectors", "responsibility": "owner-controlled email/calendar/WhatsApp execution adapters", "status": "extracted_tested"},
    {"module": "adam_core.connector_boundaries", "responsibility": "connector-boundary migration evidence", "status": "extracted_tested"},
    {"module": "adam_core.microsoft_identity", "responsibility": "Microsoft config/cache persistence and device-flow state projection", "status": "extracted_tested"},
    {"module": "adam_core.identity_boundary", "responsibility": "privacy-safe Microsoft identity-boundary evidence", "status": "extracted_tested"},
    {"module": "adam_core.whatsapp_boundary", "responsibility": "WhatsApp configuration and webhook verification service", "status": "extracted_tested"},
    {"module": "adam_core.whatsapp_boundary_evidence", "responsibility": "privacy-safe WhatsApp boundary evidence", "status": "extracted_tested"},
    {"module": "adam_core.document_processing", "responsibility": "bounded local document/attachment extraction and DOCX rendering", "status": "extracted_tested"},
    {"module": "adam_core.document_boundary", "responsibility": "privacy-safe document-processing boundary evidence", "status": "extracted_tested"},
    {"module": "adam_core.microsoft_graph_transport", "responsibility": "Microsoft Graph HTTP transport with injected token and HTTP providers", "status": "extracted_tested"},
    {"module": "adam_core.graph_transport_boundary", "responsibility": "privacy-safe Microsoft Graph transport evidence", "status": "extracted_tested"},
    {"module": "adam_core.whatsapp_cloud_transport", "responsibility": "WhatsApp Cloud API HTTP transport with injected configuration and HTTP provider", "status": "extracted_tested"},
    {"module": "adam_core.whatsapp_transport_boundary", "responsibility": "privacy-safe WhatsApp Cloud transport evidence", "status": "extracted_tested"},
    {"module": "adam_core.vision_ai_transport", "responsibility": "vision AI multimodal HTTP transport with injected credentials and HTTP provider", "status": "extracted_tested"},
    {"module": "adam_core.vision_transport_boundary", "responsibility": "privacy-safe vision AI transport evidence", "status": "extracted_tested"},
    {"module": "adam_core.windows_speech_fallback", "responsibility": "bounded Windows System.Speech fallback synthesis", "status": "extracted_tested"},
    {"module": "adam_core.windows_speech_fallback_boundary", "responsibility": "privacy-safe Windows speech fallback evidence", "status": "extracted_tested"},
    {"module": "adam_core.ai_provider_transport", "responsibility": "general text AI request construction and HTTP transport", "status": "extracted_tested"},
    {"module": "adam_core.ai_provider_boundary", "responsibility": "privacy-safe text AI provider transport evidence", "status": "extracted_tested"},
    {"module": "adam_core.audit_events", "responsibility": "audit event construction and bounded JSONL persistence", "status": "extracted_tested"},
    {"module": "adam_core.configuration", "responsibility": "bounded atomic AI configuration persistence and environment fallback", "status": "extracted_tested"},
    {"module": "adam_core.configuration_boundary", "responsibility": "privacy-safe configuration service evidence", "status": "extracted_tested"},
    {"module": "adam_core.audit_boundary", "responsibility": "privacy-safe audit event service evidence", "status": "extracted_tested"},
]


def _hash(payload):
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return sha256(raw).hexdigest()


def build_architecture_manifest(*, version):
    core = {
        "schema": "adam-acquisition-architecture/v1",
        "product": "Adam Acquisition",
        "version": version,
        "strategy": "Incrementally extract stable, buyer-critical behavior from the legacy Flask application into small tested core modules without breaking approved owner workflows.",
        "core_modules": list(CORE_MODULES),
        "module_count": len(CORE_MODULES),
        "legacy_boundary": {
            "component": "app.py",
            "status": "migration_in_progress",
            "buyer_impact": "No buyer credentials or private content are required for architecture evidence.",
        },
        "migration_controls": {
            "approved_checkpoint_preserved": True,
            "thin_acquisition_routes": True,
            "pure_core_modules_testable_without_flask": True,
            "privacy_safe_architecture_evidence": True,
        },
        "next_extraction_targets": [
            "workflow persistence service boundary",
            "voice AI transport boundary",
            "configuration service boundary",
            "owner approval persistence boundary",
            "Windows speech fallback boundary",
            "runtime configuration consolidation",
            "final acquisition demo hardening",
            "technical diligence closeout",
        ],
        "privacy": {
            "credentials_exposed": False,
            "contact_details_exposed": False,
            "message_bodies_exposed": False,
            "attachment_contents_exposed": False,
            "private_memory_exposed": False,
        },
    }
    return {"architecture": core, "architecture_sha256": _hash(core)}


def architecture_is_privacy_safe(payload):
    text = json.dumps(payload or {}, sort_keys=True, default=str).lower()
    forbidden = (
        "api_key", "access_token", "refresh_token", "client_secret", "password",
        "contact_email", "phone_number", "message_body", "attachment_body",
        "private_memory_value", "prompt_text",
    )
    return not any(term in text for term in forbidden)
