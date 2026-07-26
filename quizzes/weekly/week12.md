# Weekly Quiz — Week 12 (Secure Transport — TLS)

**~10 min · 6 questions · low-stakes** (lowest scores dropped). Individual.

**Name:** ____________  **Student ID:** ________

## MCQ (5 × 1)
1. The TLS handshake does three jobs — key exchange, server authentication and `CertificateVerify`. This week's vulnerable client skipped:
   a) key exchange, so no real session key was ever negotiated  b) `CertificateVerify`, so the server never proved it held the matching private key  c) server authentication, so the client never decided whether to believe the certificate  d) encrypting the secret before sending it, so it travelled in cleartext
2. Bob's real certificate and the impostor's certificate both carry `CN=bob` and `SAN=DNS:bob`. In fixed mode the client therefore rejects the impostor with:
   a) a hostname mismatch, since SAN checking is what catches an impostor  b) no error at all, since the names match and validation passes  c) a revocation error, since the impostor's serial is on the demo CA's CRL  d) a trust/issuer error, since the impostor has no chain to the demo CA
3. In vulnerable mode Alice logs that the handshake **succeeded** and the bytes on the wire really are ciphertext — yet `mitm.py` prints the secret in cleartext. This is because:
   a) the MITM is itself the other endpoint, so it holds the session key  b) the MITM broke the key exchange and recovered the session key from the traffic  c) Alice sent the secret before the handshake had finished negotiating  d) the negotiated session key was too short to resist an on-path attacker
4. A teammate's internal API presents a certificate issued by their own private CA, which is not in the public trust store, so their client throws SSL errors. The correct fix is to:
   a) pass `verify=False`, since TLS still encrypts everything on the wire  b) give the client that internal CA certificate as its trust anchor  c) call `urllib3.disable_warnings()` so the SSL warnings stop appearing  d) keep `CERT_REQUIRED` but set `check_hostname=False` to clear the error
5. **Forward secrecy** means that an attacker who records today's traffic and later steals the server's long-term private key:
   a) can decrypt the recording, since that key is what protected the session  b) can decrypt it only if the session used 0-RTT early data  c) still cannot decrypt it, since each session's keys were ephemeral and discarded  d) can decrypt it only once the server's certificate has expired

## Short answer (1 × 3)
6. In fixed mode `mitm.py` ran byte-for-byte the same code and presented the same impostor certificate, yet your run ended with `CERT VERIFICATION FAILED - ABORTING` and no `MITM INTERCEPTED` line anywhere. In your own words: what changed on **Alice's** side, and at what point did the connection fail relative to the secret being sent — why does that timing matter? Then name **one** attacker capability that would still defeat that check even in fixed mode.
