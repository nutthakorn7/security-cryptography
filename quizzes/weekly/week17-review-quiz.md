# Week 17 — Cumulative Review Quiz (Weeks 10–16)

**Course:** Security & Cryptography (KOSEN69) · **Time:** 30 min · **Total:** 25 pts
**Covers:** Asymmetric/hybrid encryption · Signatures & ZKP · Secure transport (TLS) · E2E
encryption · Authentication · PQC · Capstone (+ light callback to Wk2–6 fundamentals)

**Name:** ____________________  **Student ID:** ____________  **Date:** ________

---

## Part A — Multiple Choice (10 × 1 pt)

1. The main reason systems use **hybrid encryption** instead of pure asymmetric encryption for
   bulk data is:
   a) asymmetric crypto is insecure b) asymmetric crypto is too slow for large messages
   c) symmetric keys never need protecting d) asymmetric ciphertext is smaller

2. Reusing a **nonce** with AES-GCM lets an attacker:
   a) recover the private key directly b) XOR two ciphertexts to leak the XOR of the two
   plaintexts (and forge tags) c) speed up brute force only d) nothing — GCM tolerates nonce reuse

3. **ECDSA signature malleability** means:
   a) the private key can be recovered from one signature b) a valid `(r, s)` has a valid twin
   `(r, n−s)` for the same message c) any message can be signed without the key d) signatures
   expire after one use

4. What actually gives TLS its "encrypted to the right party" guarantee?
   a) the handshake being encrypted b) certificate validation against a trusted CA chain +
   hostname check c) using a long enough key d) HTTPS in the URL bar

5. **End-to-end encryption (E2EE)** differs from "just using TLS/HTTPS" because:
   a) E2EE is faster b) E2EE removes the server from the trust boundary — it never sees plaintext
   c) TLS already prevents the server from reading messages d) they are the same thing

6. Sending a password over TLS to authenticate still has which weakness?
   a) TLS doesn't encrypt passwords b) the plaintext password is handed to the server itself,
   which must be trusted not to log/leak it c) TLS certificates can't carry passwords d) it is
   slower than challenge-response

7. Why does a **quantum computer** threaten RSA/ECC but only dent AES/SHA?
   a) Shor's algorithm breaks the discrete-log/factoring problem RSA/ECC rely on; Grover's
   algorithm only halves AES/SHA's effective security (i.e. double the key/output size to
   compensate) b) quantum computers can't run classical algorithms at all c) AES and RSA use the
   same math d) quantum computers only affect network protocols, not math

8. A **Lamport one-time signature** becomes forgeable if:
   a) the message is too short b) the same key pair signs a second, different message
   c) the hash function is SHA-256 d) it is used over TLS

9. "**Harvest now, decrypt later**" describes:
   a) collecting today's ciphertext to decrypt once a quantum computer is available b) a phishing
   technique c) a supply-chain attack d) a padding-oracle attack

10. In this course's capstone framing, the core deliverable arc is:
    a) write code only b) threat-model → demonstrate the attack → apply and justify the fix
    c) pass a written exam only d) submit a slide deck with no working system

---

## Part B — Short Answer (3 × 3 pts)

11. Explain in 2–3 sentences why an **unauthenticated Diffie–Hellman exchange** (Week 5) is
    MITM-able, and name the one property that fixes it.

12. A teammate says: "Our chat app uses HTTPS, so the server can't read our messages." Explain
    why this is wrong and what would actually have to change to make it true.

13. Give one concrete reason a **challenge-response** (or PAKE-style) login is stronger than
    sending the password directly, even over TLS.

---

## Part C — Applied (2 × 3 pts)

14. You review a signed-transaction system and find it accepts `(r, n−s)` as a different,
    equally-valid transaction from `(r, s)` on the same message. Name the vulnerability class and
    describe the one-line server-side fix.

15. A colleague reuses a Lamport one-time key pair to sign two different admin messages "to save
    key-generation time." Explain what an attacker can now do, and state the one operational rule
    that must be enforced to prevent it.
