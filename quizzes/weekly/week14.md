# Weekly Quiz — Week 14 (User Authentication: Challenge-Response, PAKE & MFA)

**~10 min · 6 questions · low-stakes** (lowest scores dropped). Individual.

**Name:** ____________  **Student ID:** ________

## MCQ (5 × 1)
1. In the lab's vulnerable mode the server logs `SERVER SAW PASSWORD: correct-horse-battery`. Wrapping the whole exchange in TLS would **not** remove that line, because:
   a) TLS encrypts only the response, not the request body  b) an eavesdropper on the network path would still read the password in transit  c) the server terminates the TLS, decrypts the request, and holds the plaintext in its handler  d) the server writes its log line before the TLS handshake has finished
2. In the lab's fixed mode the client sends only a nonce and a proof. The server decides the login is valid by comparing that proof against:
   a) the plaintext password it stored for `alice` at signup  b) a bcrypt hash of the password carried in the request body  c) the nonce it issued, hashed once with SHA-256  d) a proof it recomputes itself from its stored verifier and the nonce it issued
3. The README is explicit that this fixed demo is **not** a full PAKE. The two properties a real PAKE (SRP, OPAQUE) adds and this demo lacks are:
   a) offline-dictionary resistance on the stored verifier, and mutual authentication  b) forward secrecy, and resistance to quantum attack  c) encryption of the nonce, and encryption of the proof  d) protection against replay, and rate limiting of failed logins
4. The Audit-the-AI login handler stores passwords correctly with `bcrypt.checkpw()`, but logs the full request body on every attempt and `login FAILED for <user> (pw=<password>)` on failure. Its security flaw is:
   a) bcrypt is the wrong algorithm here; only argon2id is acceptable  b) the two logging calls put the raw password into the application log  c) returning 401 on failure tells an attacker the username exists  d) the bcrypt work factor is left at its default, so the stored hashes can be cracked
5. A phishing page at a lookalike domain can relay a victim's **TOTP** code to the real site in real time, but the same trick fails against **FIDO2/WebAuthn**, because:
   a) a 6-digit TOTP code can be brute-forced within its 30-second window  b) FIDO2 private keys live in hardware, and hardware cannot be phished  c) the FIDO2 signature is bound to the origin, so one made for the fake domain will not verify for the real one  d) the TOTP secret is shared with the server, whereas the FIDO2 private key never is

## Short answer (1 × 3)
6. In fixed mode you logged in successfully, yet `grep -c "correct-horse-battery"` over the server's own logs returned **0**. In your own words: (a) why can an attacker who records that entire exchange — the nonce *and* the proof — not reuse it to log in tomorrow? (b) Name **one** thing that attacker could still do if, instead, they stole the server's stored verifier for `alice`.
