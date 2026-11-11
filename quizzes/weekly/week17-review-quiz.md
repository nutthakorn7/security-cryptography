# Week 17 — Cumulative Review Quiz (Weeks 10–16)

**Course:** Cryptography and Network Security (KOSEN69) · **Time:** 30 min · **Total:** 25 pts
**Covers:** Asymmetric/hybrid encryption · Signatures & ZKP · Secure transport (TLS) · E2E
encryption · Authentication · PQC · Capstone (+ light callback to Wk1–6 fundamentals)

**Name:** ____________________  **Student ID:** ____________  **Date:** ________

---

## Part A — Multiple Choice (10 × 1 pt)

1. The main reason systems use **hybrid encryption** instead of pure asymmetric encryption for
   bulk data is:
   a) asymmetric crypto is insecure b) asymmetric crypto is too slow for large messages
   c) symmetric keys never need protecting d) asymmetric ciphertext is smaller

2. Reusing a **nonce** with AES-GCM lets an attacker:
   a) recover the private key directly b) XOR aligned ciphertext bodies to leak the XOR of the
   two plaintexts, and potentially undermine authentication c) speed up brute force only d) nothing — GCM tolerates nonce reuse

3. **ECDSA signature malleability** means:
   a) the private key can be recovered from one signature b) a valid `(r, s)` has a valid twin
   `(r, n−s)` for the same message c) any message can be signed without the key d) signatures
   expire after one use

4. What actually gives TLS its "encrypted to the right party" guarantee?
   a) the handshake being encrypted b) certificate validation against a trusted CA chain +
   hostname check c) using a long enough key d) HTTPS in the URL bar

5. **End-to-end encryption (E2EE)** differs from "just using TLS/HTTPS" because:
   a) E2EE is faster b) clients encrypt to authenticated recipient keys so the relay does not see message plaintext
   c) TLS already prevents the server from reading messages d) they are the same thing

6. Sending a password over TLS to authenticate still has which weakness?
   a) TLS doesn't encrypt passwords b) the plaintext password is handed to the server itself,
   which must be trusted not to log/leak it c) TLS certificates can't carry passwords d) it is
   slower than challenge-response

7. Why does a **quantum computer** threaten RSA/ECC differently from AES and hash functions?
   a) Shor's algorithm attacks the factoring/discrete-log problems RSA/ECC rely on; Grover's
   algorithm gives a quadratic speedup for unstructured key/preimage search, so suitable symmetric
   and hash parameters can retain security b) quantum computers can't run classical algorithms at all c) AES and RSA use the
   same math d) quantum computers only affect network protocols, not math

8. In the Week 15 **Lamport one-time-signature lab**, what exposes both secret preimages at every
   bit position and permits an arbitrary-message forgery?
   a) a message that is too short b) signing a message and its bitwise complement with the same key pair
   c) using SHA-256 d) sending the signatures over TLS

9. "**Harvest now, decrypt later**" describes:
   a) collecting today's ciphertext to decrypt once a quantum computer is available b) a phishing
   technique c) a supply-chain attack d) a padding-oracle attack

10. In the CryptoVault capstone, the core deliverable arc is:
    a) write code only b) define trust boundaries → implement the five controls → test failures
    and justify the design c) pass a written exam only d) submit a slide deck with no working system

---

## Part B — Short Answer (3 × 3 pts)

11. Explain in 2–3 sentences why an **unauthenticated Diffie–Hellman exchange** (Week 5) is
    MITM-able, and name the one property that fixes it.

12. A teammate says: "Our chat app uses HTTPS, so the server can't read our messages." Explain
    why this is wrong and what would actually have to change to make it true.

13. In the course's **toy challenge-response** demo, what one property is better than sending the
    password directly, even over TLS? Name one security limit the toy still has.

---

## Part C — Applied (2 × 3 pts)

14. You review a signed-transaction system and find it accepts `(r, n−s)` as a different,
    equally-valid transaction from `(r, s)` on the same message. Name the vulnerability class,
    the check that rejects this twin, and the application control that prevents repeat processing
    of the same authorized transaction even if another valid signature is produced.

15. A colleague signs a message `M` and its bitwise complement `~M` using the **same** Lamport
    key pair "to save key-generation time." Explain what an attacker can now recover and forge,
    and state the operational rule that prevents it.
