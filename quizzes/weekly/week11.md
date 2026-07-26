# Weekly Quiz — Week 11 (Signatures & Zero-Knowledge Proofs)

**~10 min · 6 questions · low-stakes** (lowest scores dropped). Individual.

**Name:** ____________  **Student ID:** ________

## MCQ (5 × 1)
1. Unlike a **MAC**, a digital signature can be verified by:
   a) only the parties holding the shared secret  b) only the signer, using the private key  c) anyone holding the signer's public key  d) only a certificate authority
2. The **Fiat–Shamir transform** turns the interactive Schnorr protocol into a signature by:
   a) replacing the verifier's live random challenge with a hash of the commitment and the message  b) encrypting the response with the signer's private key  c) sending the secret to the verifier once, at registration  d) repeating the three-move exchange until the verifier is convinced
3. Given a valid ECDSA signature `(r, s)`, an attacker who does **not** know the private key can produce a second, different, still-valid signature on the *same* message by computing (`n` = the curve's group order):
   a) `(n − r, s)`  b) `(r, n − s)`  c) `(r, s⁻¹ mod n)`  d) `(r + n, s)`
4. A payment system that treats "one valid signature" as "one unique transaction" is assuming a security property ECDSA does **not** satisfy. That property is called:
   a) EUF-CMA (existential unforgeability)  b) collision resistance of the message hash  c) determinism of the signing nonce `k`  d) SUF-CMA (strong existential unforgeability)
5. The lab's fixed bank rejects any signature with `s > n//2` (**low-S / BIP-62**). This closes the double-spend because:
   a) it makes ECDSA signatures unforgeable, which they were not before  b) of the two twin values of `s`, exactly one satisfies `s ≤ n/2`, leaving one canonical signature per `(message, public key)`  c) it rejects both twins, so no withdrawal is processed at all  d) it forces the bank to verify the signature a second time before deduplicating

## Short answer (1 × 3)
6. A bank de-duplicates withdrawals by the hash of the signature, `sha256(r‖s)`, so an exact resubmission is rejected as a replay. Every valid ECDSA signature `(r, s)` also has a mathematically valid twin `(r, n − s)` for the same message and key. In your own words: why does one authorisation become two paid transactions under that rule — what is the bank treating as the transaction's identity? Then give **one** change to that identity rule (not a low-S check) that would stop it.
