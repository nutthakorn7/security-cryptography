# Weekly Quiz — Week 6 (Authenticated Encryption / AEAD)

**Course:** Security & Cryptography (KOSEN69) · **~10 min · 6 questions · low-stakes**
(lowest scores dropped). Individual.

**Name:** ____________  **Student ID:** ________

## MCQ (5 × 1)
1. The three guarantees an **AEAD** cipher delivers in a single primitive are:
   a) confidentiality, integrity, availability  b) confidentiality, integrity, authenticity  c) integrity, authenticity, non-repudiation  d) confidentiality, forward secrecy, integrity
2. Under **Encrypt-then-MAC**, the receiver's *first* action on an incoming message is to:
   a) decrypt the ciphertext, then check the MAC  b) strip the PKCS#7 padding and check the message format  c) verify the MAC over the ciphertext and refuse to decrypt if it fails  d) confirm the IV has not been used before
3. In an unauthenticated AES-CBC service whose `/decrypt` never returns the plaintext, the **padding oracle** is:
   a) the ciphertext being served as base64  b) the AES key being reused across messages  c) the IV travelling in the clear ahead of the ciphertext  d) the `200`-versus-`403` difference in the reply to a submitted ciphertext
4. An attacker varies the last byte of a forged previous block until the server accepts the padding, forcing the last plaintext byte to `0x01` with winning guess `g`. The last byte of the intermediate value `D(C_t)` is then:
   a) `g XOR 0x01`  b) `g` itself  c) `g XOR real_prev[15]`  d) `0x01 XOR real_prev[15]`
5. The **associated data** (the "AD" in AEAD) is data that is:
   a) encrypted with a second key, then sent alongside the ciphertext  b) encrypted but not authenticated, so it stays hidden without a tag  c) authenticated but not encrypted, so it stays readable yet tamper-evident  d) neither encrypted nor authenticated, since headers carry no secrets

## Short answer (1 × 3)
6. A developer says: *"Our decrypt endpoint never returns the plaintext — it only answers `200` or `403` — so an attacker learns nothing."* In your own words, explain why that reasoning is wrong and what an attacker can do with those two answers alone, then say why the same attack gains nothing against an AES-GCM endpoint.
