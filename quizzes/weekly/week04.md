# Weekly Quiz — Week 4 (AES & Block-Cipher Modes)

**Course:** Cryptography and Network Security (KOSEN69) · **~10 min · 6 questions · low-stakes**
(lowest scores dropped). Individual.
Taken at the start of Week 5 as a recap of Week 4.

**Name:** ____________  **Student ID:** ________

## MCQ (5 × 1)
1. The "ECB penguin" — an image encrypted with **AES-ECB** still shows its outline — because:
   a) AES-128's key is too short for image data  b) the same IV was reused for every block  c) identical plaintext blocks encrypt to identical ciphertext blocks  d) the image was not padded to a block boundary
2. In the lab you changed one letter of a **CBC** token and `/whoami` still said `guest`. This happened because:
   a) AES was broken by the change  b) CBC has no tag or MAC, so nothing checks whether the token was changed  c) the token was too short to be checked  d) base64 hides every change
3. A developer says: *"the token is AES-encrypted with a key only the server knows, so the client cannot change the role."* The flaw in that claim is:
   a) AES-256 is now brute-forceable on modern GPUs  b) shipping the IV to the client leaks the key  c) base64 is an encoding, so the role is readable anyway  d) confidentiality is not integrity — unauthenticated ciphertext can be changed
4. **AES-GCM** refuses the kind of change that unauthenticated AES-CBC accepts, because it:
   a) is a stream-cipher mode, so editing a ciphertext byte cannot affect the plaintext at all  b) checks a tag over the ciphertext before it returns any plaintext  c) uses a 256-bit key, making the ciphertext too hard to alter usefully  d) issues a fresh nonce per request, so the replayed token is stale
5. A **GCM nonce** must be:
   a) secret and random  b) the same for every message, so the server can check it  c) unique: never repeated with the same key  d) equal to the key

## Short answer (1 × 3)
6. In your own words, with no formulas: why did the CBC server accept your changed token while the GCM server refused it? Say what GCM adds that CBC does not.
