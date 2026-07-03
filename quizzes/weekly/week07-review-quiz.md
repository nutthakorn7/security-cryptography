# Weekly Quiz — Week 7 (Cumulative Review, Weeks 1–6)

**Course:** Security & Cryptography (KOSEN69) · **~20 min · 10 questions · low-stakes**
(lowest weekly-quiz scores dropped, per course grading policy). Individual, closed book.
**Covers:** threat modeling · hash functions · MACs · AES/block-cipher modes · key exchanges ·
AEAD — one or two questions per week, at the same difficulty as that week's own weekly quiz.

**Name:** ____________________  **Student ID:** ____________  **Date:** ________

---

## MCQ (7 × 1 pt)

1. *(Wk1 — threat modeling)* A crypto system uses AES-256 (textbook-secure) but hardcodes the key
   in a public GitHub repo. The **root cause** of the resulting breach is best described as:
   a) AES-256 being cryptographically weak
   b) a key-management failure, not an algorithm failure
   c) the ciphertext being too short
   d) using symmetric instead of asymmetric encryption

2. *(Wk2 — hashing)* The correct way to store user passwords is:
   a) MD5 b) SHA-256 c) Base64 d) a salted, slow KDF (argon2id/bcrypt)

3. *(Wk2 — hashing)* A per-user random **salt** primarily defeats:
   a) brute-force of a single password b) precomputed rainbow-table attacks across many users
   c) length-extension attacks d) timing attacks on comparison

4. *(Wk3 — MACs)* `cookie = username || SHA-256(secret || username)` is forgeable by an attacker
   who doesn't know `secret` because:
   a) SHA-256 is reversible b) Merkle-Damgard hashes allow length-extension from a known digest
   c) the cookie isn't Base64-encoded d) SHA-256 collides too easily

5. *(Wk4 — AES modes)* In unauthenticated AES-**CBC**, flipping one bit of ciphertext block
   `C_{i-1}` will:
   a) corrupt block `i-1`'s plaintext only b) flip the same bit position in plaintext block `i`
   in a predictable, attacker-controlled way c) cause decryption to fail with an error
   d) have no effect on decryption

6. *(Wk5 — key exchanges)* Plain (unauthenticated) Diffie-Hellman protects against a **passive**
   eavesdropper but not against:
   a) a slow network b) an active machine-in-the-middle who can intercept and substitute keys
   c) a weak password d) a padding oracle

7. *(Wk6 — AEAD)* Of the three ways to combine a cipher and a MAC, the one that is **provably
   safe** for any secure cipher + any secure MAC is:
   a) MAC-then-Encrypt b) Encrypt-and-MAC c) Encrypt-then-MAC d) Hash-then-Encrypt

## Short answer (3 × 3 pts)

8. *(Wk1/Wk5 — threat modeling)* Name the **attacker model** (passive vs. active) each of these
   assumes, and say why the distinction matters: (a) recovering a password from a leaked hash
   dump, (b) intercepting and relaying a Diffie-Hellman handshake.

9. *(Wk4/Wk6)* In one or two sentences, explain why a **padding oracle** is "malleability
   weaponized into full decryption" — connect it back to the CBC bit-flip relation
   `P_i = D(C_i) XOR C_{i-1}` from Week 4.

10. *(Wk2/Wk3 — cumulative)* A developer says: *"I don't store plaintext — I store `HMAC(key,
    password)`, and HMAC is a real MAC, not a hash-only construction. So this is a safe way to
    store passwords."* Is a keyed MAC the *right tool* for password storage? In 2–3 sentences,
    explain what property HMAC gives you here (integrity/authenticity of *known* data) versus
    what a password store actually needs (resistance to *fast offline guessing* once the data
    leaks) — and why the fix from Week 2 (a slow, salted KDF) is not the same problem HMAC solves.
