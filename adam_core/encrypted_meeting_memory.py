"""Buyer-controlled encrypted meeting-memory persistence contract for Adam Acquisition v4.9.

The core never owns or stores encryption keys. A buyer/deployer injects encryption,
decryption and persistence adapters. Buyer-safe evidence contains metadata only.
"""
from __future__ import annotations
from typing import Any, Callable

MAX_CIPHERTEXT_CHARS = 12000
MAX_KEY_HANDLE_CHARS = 160

class EncryptedMeetingMemoryError(RuntimeError):
    pass

def _clean(value: Any, limit: int) -> str:
    return " ".join(str(value or "").split())[:limit]

def persist_encrypted_memory(
    plaintext_payload: str,
    *,
    key_handle: str,
    encrypt: Callable[[str, str], str],
    store_ciphertext: Callable[[dict], Any],
) -> dict:
    payload=str(plaintext_payload or "")
    handle=_clean(key_handle, MAX_KEY_HANDLE_CHARS)
    if not payload:
        raise EncryptedMeetingMemoryError("A private meeting-memory payload is required.")
    if not handle:
        raise EncryptedMeetingMemoryError("A buyer-controlled key handle is required.")
    ciphertext=str(encrypt(payload, handle) or "")
    if not ciphertext or ciphertext == payload:
        raise EncryptedMeetingMemoryError("Encryption adapter did not return protected ciphertext.")
    if len(ciphertext) > MAX_CIPHERTEXT_CHARS:
        raise EncryptedMeetingMemoryError("Encrypted payload exceeds the bounded storage contract.")
    envelope={"ciphertext":ciphertext,"key_handle":handle,"schema":"adam-private-meeting-memory/v1"}
    ok=store_ciphertext(envelope) is not False
    return {
        "ok":bool(ok),
        "status":"encrypted_memory_persisted",
        "ciphertext_stored":bool(ok),
        "plaintext_stored":False,
        "encryption_key_stored_by_adam":False,
        "buyer_controlled_key_handle_required":True,
        "private_values_returned":False,
    }

def recall_encrypted_memory(
    query: str,
    *,
    search_ciphertext: Callable[[str], list[dict] | None],
    decrypt: Callable[[str, str], str],
) -> dict:
    q=_clean(query, 500)
    if not q:
        raise EncryptedMeetingMemoryError("A recall query is required.")
    rows=search_ciphertext(q) or []
    verified=0
    for row in rows[:20]:
        if not isinstance(row,dict): continue
        c=str(row.get("ciphertext") or "")
        h=_clean(row.get("key_handle"),MAX_KEY_HANDLE_CHARS)
        if c and h and decrypt(c,h): verified += 1
    return {
        "ok":True,
        "status":"encrypted_memory_recall_verified",
        "matches_verified":verified,
        "plaintext_returned_in_buyer_evidence":False,
        "ciphertext_returned_in_buyer_evidence":False,
        "key_material_returned":False,
        "private_values_returned":False,
    }

def public_manifest() -> dict:
    return {
        "buyer_controlled_encrypted_memory_persistence":True,
        "encryption_adapter_injected":True,
        "decryption_adapter_injected":True,
        "ciphertext_store_injected":True,
        "key_management_external_to_adam":True,
        "key_handle_required":True,
        "plaintext_persistence_allowed":False,
        "production_cipher_not_bundled":True,
        "privacy":{
            "encryption_keys_stored":False,
            "plaintext_memory_exposed_in_buyer_evidence":False,
            "ciphertext_exposed_in_buyer_evidence":False,
            "meeting_links_exposed":False,
            "participant_identity_exposed":False,
        },
    }
