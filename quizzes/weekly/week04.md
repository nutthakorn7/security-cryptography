# Weekly Quiz — Week 4 (AES & Block-Cipher Modes)

**Course:** Security & Cryptography (KOSEN69) · **~10 min · 6 questions · low-stakes**
(lowest scores dropped). Individual.

**Name:** ____________  **Student ID:** ________

## MCQ (5 × 1)
1. The "ECB penguin" — an image encrypted with **AES-ECB** still shows its outline — because:
   a) AES-128's key is too short for image data  b) the same IV was reused for every block  c) identical plaintext blocks encrypt to identical ciphertext blocks  d) the image was not padded to a block boundary
2. Two messages are encrypted with **AES-CBC** under the same key **and the same IV**. An observer learns:
   a) whether the two messages begin with the same bytes  b) the AES key, recovered from the repeated blocks  c) the full plaintext of the shorter message  d) nothing — the IV is public anyway, so reusing it is harmless
3. A developer says: *"the token is AES-encrypted with a key only the server knows, so the client cannot change the role."* The flaw in that claim is:
   a) AES-256 is now brute-forceable on modern GPUs  b) shipping the IV to the client leaks the key schedule  c) base64 is an encoding, so the role is readable anyway  d) confidentiality is not integrity — unauthenticated ciphertext is malleable
4. **AES-GCM** rejects the same byte-flipping edit that unauthenticated AES-CBC accepts, because it:
   a) is a stream-cipher mode, so editing a ciphertext byte cannot affect the plaintext at all  b) verifies an authentication tag over the ciphertext before returning any plaintext  c) uses a 256-bit key, making the ciphertext too hard to alter usefully  d) issues a fresh nonce per request, so the replayed token is stale
5. Reusing a **GCM nonce** under the same key is called catastrophic because:
   a) the ciphertext grows longer than the plaintext, leaking the message length  b) confidentiality suffers, but the authentication guarantee still holds  c) the keystream repeats and the authentication key leaks, so tags become forgeable  d) GCM detects the repeat and refuses to decrypt, taking the service down

## Short answer (1 × 3)
6. The lab's `:8096` token is `IV ‖ C0 ‖ C1` over the fixed plaintext `comment=FILLER!!` ‖ `role=guest;xpad0`. In your own words, explain **why** XOR-ing a few bytes into `C0` changes the role that block 1 decrypts to, even though the attacker never learns the AES key — and say what happens to block 0's plaintext as a side effect, and why that side effect does not stop the attack.
