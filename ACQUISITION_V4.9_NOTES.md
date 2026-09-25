# Adam Acquisition v4.9.0 — Buyer-Controlled Encrypted Meeting Memory

- Adds injected encryption/decryption/persistence contract for structured meeting memory.
- Adam stores no encryption key material.
- Plaintext persistence is prohibited by the core contract.
- Buyer evidence exposes neither plaintext nor ciphertext.
- Acceptance uses a clearly labelled synthetic reversible adapter; no production cipher or KMS is bundled.
- Production deployment requires buyer-controlled KMS/cipher binding and security review.
- New acceptance tests only: 174–175.
