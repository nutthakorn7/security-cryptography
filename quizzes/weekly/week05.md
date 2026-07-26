# Weekly Quiz — Week 5 (Key Exchanges)

**~10 min · 6 questions · low-stakes** (lowest scores dropped). Individual.

**Name:** ____________  **Student ID:** ________

## MCQ (5 × 1)
1. An eavesdropper who records the **whole** Diffie-Hellman handshake between Alice and Bob learns:
   a) the shared secret `g^(ab) mod p`, because both sides transmit it  b) `p`, `g`, `g^a mod p` and `g^b mod p`, but not `a`, `b` or `g^(ab) mod p`  c) Alice's private exponent `a`, because it is sent in the clear  d) nothing at all, because every value on the wire is already encrypted
2. Recovering Alice's private exponent `a` from the `g^a mod p` she sends is believed to be hard because it means solving:
   a) the integer factorisation problem  b) a collision on SHA-256  c) an exhaustive search of the AES-GCM key space  d) the discrete logarithm problem
3. In the vulnerable run, `relay` completes **two** independent DH handshakes rather than one because it must:
   a) be a genuine DH peer to each side, so it ends up holding a different shared secret with Alice and with Bob  b) compare the two exchanges in order to recover Alice's private exponent `a`  c) forward Alice's own public value unchanged so that Bob's handshake still completes  d) generate its own prime `p` and generator `g` for each connection
4. In the fixed run, the tag each side sends **alongside** its DH public value is:
   a) an AES-GCM encryption of the public value under the session key  b) a plain SHA-256 hash of the public value  c) HMAC-SHA256 over the public-key bytes under a pre-shared `AUTH_KEY` that `relay` does not hold  d) a digital signature made with that side's private DH exponent
5. Alice and Bob already share `AUTH_KEY`. The fixed version still runs a **fresh** DH exchange every session rather than just using `AUTH_KEY` as the encryption key, because:
   a) `AUTH_KEY` is consumed by the HMAC and cannot be reused  b) the session key stays ephemeral, so traffic recorded today is still safe if `AUTH_KEY` leaks next year  c) an HMAC key and an AES key may never be the same length  d) modular exponentiation is faster than AES-GCM on long messages

## Short answer (1 × 3)
6. `relay` runs almost the same code in both modes — it generates its own DH keypairs and attempts the same substitution either way — yet the fixed run ends in `AUTH FAILED - ABORTING` instead of `RELAY INTERCEPTED`. In your own words (2–3 sentences), say what `relay` is unable to produce, and why the check that catches it has to happen *before* either side derives a session key.
