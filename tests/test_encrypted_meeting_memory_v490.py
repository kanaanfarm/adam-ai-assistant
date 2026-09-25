from adam_core.encrypted_meeting_memory import persist_encrypted_memory, recall_encrypted_memory, EncryptedMeetingMemoryError
from adam_core.encrypted_meeting_memory_boundary import build_encrypted_meeting_memory_manifest, encrypted_meeting_memory_is_privacy_safe, encrypted_meeting_memory_self_test

def test_boundary_privacy_and_external_key_management():
    p=build_encrypted_meeting_memory_manifest("v4.9.0")
    assert encrypted_meeting_memory_is_privacy_safe(p)
    c=p["encrypted_meeting_memory"]["capabilities"]
    assert c["key_management_external_to_adam"] is True
    assert c["plaintext_persistence_allowed"] is False
    assert c["production_cipher_not_bundled"] is True

def test_injected_encryption_contract_and_recall():
    rows=[]
    enc=lambda t,h:"x:"+t[::-1]
    dec=lambda c,h:c[2:][::-1]
    r=persist_encrypted_memory("private outcome",key_handle="buyer-key",encrypt=enc,store_ciphertext=lambda e:rows.append(e) or True)
    assert r["ok"] and r["plaintext_stored"] is False and r["encryption_key_stored_by_adam"] is False
    q=recall_encrypted_memory("outcome",search_ciphertext=lambda q:rows,decrypt=dec)
    assert q["matches_verified"]==1 and q["private_values_returned"] is False

def test_self_test_is_synthetic_and_network_free():
    r=encrypted_meeting_memory_self_test()
    assert r["ok"] and r["production_cipher_used"] is False and r["external_network_accessed"] is False
