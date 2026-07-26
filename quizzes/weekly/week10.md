# Weekly Quiz — Week 10 (Asymmetric & Hybrid Encryption)

**~10 min · 6 questions · low-stakes** (lowest scores dropped). Individual.

**Name:** ____________  **Student ID:** ________

## MCQ (5 × 1)
1. Pure **RSA** is unsuitable for encrypting a video file because:
   a) RSA encrypts text but not binary data  b) it is far slower than AES, and one RSA-4096-OAEP operation caps out at a few hundred bytes  c) RSA's security falls as the plaintext grows longer  d) OAEP padding expands every ciphertext several times over
2. In the **hybrid** scheme Bob uses to message Alice, the value wrapped with RSA-OAEP is:
   a) each message, wrapped one at a time  b) the AES-GCM nonce, wrapped per message  c) a fresh AES-256 session key, wrapped once per session  d) the GCM authentication tag, wrapped with each ciphertext
3. In an **asymmetric key exchange**, an eavesdropper who records both public keys still cannot compute the shared secret because:
   a) discrete-log hardness means a public key does not reveal its private key  b) the public keys travel encrypted under a pre-shared password  c) each public key is derived from the other party's private key  d) the shared secret is sent, but only in the last message
4. In **ECIES**, the raw ECDH shared secret is:
   a) transmitted with the ciphertext so the recipient can decrypt  b) used directly as the AES key  c) signed with the sender's long-term key  d) passed through a KDF such as HKDF to derive the symmetric key
5. Two messages are sent under the **same AES-GCM key and the same nonce**. A passive eavesdropper who records both ciphertexts can:
   a) do nothing until the RSA-wrapped session key is recovered  b) XOR the two ciphertexts to obtain the XOR of the two plaintexts  c) do nothing, because GCM rejects the second ciphertext  d) act only by querying Alice repeatedly as an oracle

## Short answer (1 × 3)
6. A hybrid scheme wraps a session key with RSA-OAEP and encrypts each message with AES-GCM, reusing one nonce for every message in a session. (a) In your own words, state what an eavesdropper who records two such messages can compute from the ciphertexts alone, and what still stands between that value and the two plaintexts. (b) A teammate proposes moving from RSA-2048 to RSA-4096 as the fix. Explain **why** that changes nothing here.
