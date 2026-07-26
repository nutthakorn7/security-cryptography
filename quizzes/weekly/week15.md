# Weekly Quiz — Week 15 (Post-Quantum Cryptography & Lamport One-Time Signatures)

**~10 min · 6 questions · low-stakes** (lowest scores dropped). Individual.

**Name:** ____________  **Student ID:** ________

## MCQ (5 × 1)
1. **Grover's algorithm** applied to AES-256:
   a) breaks it outright, as Shor's algorithm breaks RSA  b) halves it to about 128-bit strength — mitigated by longer keys  c) leaves symmetric ciphers alone; it threatens only hash functions  d) forces AES key lengths to be quadrupled to stay secure
2. "**Harvest now, decrypt later**" describes an adversary who:
   a) waits for a quantum computer, so today's traffic is unaffected  b) breaks AES today and stores the plaintext for later analysis  c) buys quantum hardware now to decrypt traffic in real time  d) records encrypted traffic today and decrypts it once quantum computers exist
3. A Lamport private key holds **two** secret preimages per message bit. After the key signs one 32-bit message, an attacker holding that signature knows:
   a) one preimage per bit — the one matching that message's bits  b) both preimages for half the bit positions, which is enough to forge  c) nothing secret, because a signature only ever reveals hashes  d) the whole private key, since the public key publishes both hashes
4. The attack on `:8100` signs `M = 0x00000000` and then `~M = 0xFFFFFFFF` because:
   a) any two distinct messages together reveal a Lamport private key  b) the two messages share a SHA-256 digest, so one signature covers both  c) `0xFFFFFFFF` is the only other message the reused key will sign  d) they differ in every bit, revealing both preimages at every position
5. NIST standardised **ML-KEM** (FIPS 203) and **ML-DSA** (FIPS 204). They differ in that:
   a) ML-KEM signs messages, while ML-DSA establishes a session key  b) ML-KEM is the hash-based scheme, ML-DSA the lattice-based one  c) ML-KEM establishes a session key, while ML-DSA produces signatures  d) ML-KEM protects symmetric traffic, while ML-DSA replaces hashing

## Short answer (1 × 3)
6. The fixed app on `:8101` refuses **every** second `/sign` — even a repeat request for the *same* message it has already signed. In your own words: why is "one signature, period" the right rule rather than "one distinct message"? Then say what must happen when that signature request is retried, and why the answer cannot be "sign it again".
