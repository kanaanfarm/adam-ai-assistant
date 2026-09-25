"""Buyer-safe encrypted meeting-memory evidence for Adam Acquisition v4.9."""
from .encrypted_meeting_memory import public_manifest, persist_encrypted_memory, recall_encrypted_memory

def build_encrypted_meeting_memory_manifest(version: str) -> dict:
    return {
        "schema":"adam-acquisition-encrypted-meeting-memory/v1",
        "product":"Adam Acquisition","version":version,
        "status":"buyer_controlled_encrypted_memory_foundation_tested",
        "encrypted_meeting_memory":{"boundary_module":"adam_core.encrypted_meeting_memory","capabilities":public_manifest()},
        "next_targets":["buyer KMS binding","real meeting adapter binding","production deployment security review"],
    }

def encrypted_meeting_memory_is_privacy_safe(payload: dict) -> bool:
    c=(((payload or {}).get("encrypted_meeting_memory") or {}).get("capabilities") or {})
    p=c.get("privacy") or {}
    return bool(c.get("buyer_controlled_encrypted_memory_persistence") and c.get("key_management_external_to_adam") and
                c.get("plaintext_persistence_allowed") is False and p.get("encryption_keys_stored") is False and
                p.get("plaintext_memory_exposed_in_buyer_evidence") is False and p.get("ciphertext_exposed_in_buyer_evidence") is False)

def encrypted_meeting_memory_self_test() -> dict:
    stored=[]
    # Synthetic reversible adapter proves the injected contract only; it is not a production cipher.
    def enc(text,handle): return "synthetic:" + text[::-1]
    def dec(cipher,handle): return cipher.removeprefix("synthetic:")[::-1]
    saved=persist_encrypted_memory("Synthetic private meeting outcome",key_handle="buyer-kms-key-001",encrypt=enc,store_ciphertext=lambda e: stored.append(e) or True)
    recall=recall_encrypted_memory("outcome",search_ciphertext=lambda q:stored,decrypt=dec)
    return {
        "ok":bool(saved.get("ok") and recall.get("ok") and recall.get("matches_verified")==1),
        "encrypted_persistence_contract_verified":saved.get("ciphertext_stored") is True,
        "plaintext_stored":saved.get("plaintext_stored"),
        "buyer_controlled_key_handle_verified":saved.get("buyer_controlled_key_handle_required") is True,
        "encryption_key_stored_by_adam":saved.get("encryption_key_stored_by_adam"),
        "encrypted_recall_contract_verified":recall.get("matches_verified")==1,
        "production_cipher_used":False,
        "credentials_used":False,
        "external_network_accessed":False,
        "private_values_returned":False,
    }
