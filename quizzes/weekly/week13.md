# Weekly Quiz — Week 13 (End-to-End Encryption)

**~10 min · 6 questions · low-stakes** (lowest scores dropped). Individual.

**Name:** ____________  **Student ID:** ________

## MCQ (5 × 1)
1. A messaging provider serves every request over HTTPS with a valid certificate, yet it can still read every message it relays. The reason is that:
   a) HTTPS encrypts only the request headers, never the message body  b) the server terminates the TLS connection — it decrypts, holds the plaintext, then re-encrypts to forward it  c) the certificate authority that issued the certificate keeps a copy of the session key  d) TLS also keeps the message encrypted once it has been stored on the server
2. In fixed mode alice generates a **fresh AES-256-GCM key per message** and wraps that key to bob's public key with **RSA-OAEP**, instead of RSA-encrypting the message itself. The main reason is:
   a) AES-256-GCM on its own provides integrity but no confidentiality  b) RSA-OAEP can only encrypt data that is itself an RSA key  c) the server needs the AES key in order to route the message to bob  d) RSA is slow and size-limited, so the fast symmetric cipher carries the message and only the short key is wrapped
3. In fixed mode bob generates his RSA keypair inside his own container and publishes only the **public** half. The server relays that public key and stores the resulting ciphertext, yet still cannot read the message because:
   a) the private half never leaves bob's endpoint, and only it can unwrap the per-message AES key  b) the AES-GCM authentication tag stops any party other than the sender from decrypting the body  c) base64 cannot be reversed without the key that produced it  d) the server discards its copy of the payload as soon as bob fetches it
4. Fixed mode proves that the server cannot read the message. What it does **not** prove is that:
   a) bob can still recover the secret after alice encrypts it  b) the payload the server stored was already encrypted before it left alice  c) the public key alice fetched really belongs to bob, rather than one a malicious server substituted  d) the server's own log holds no copy of the plaintext
5. The **Double Ratchet** gives a Signal session **forward secrecy**, which specifically means that:
   a) a message is delivered even when the recipient's device is offline at the moment it is sent  b) an attacker who compromises a key today still cannot read the messages sent before that compromise  c) the session recovers its security after a compromise, so later messages are protected again  d) the recipient's key is accepted the first time it is seen and pinned for later comparison

## Short answer (1 × 3)
6. In the lab, `grep -c "meet at pier 39 at midnight"` against the **server** log printed `1` in vulnerable mode and `0` in fixed mode — even though `server.py` is byte-for-byte the same code in both runs and still prints `SERVER SAW:` on whatever it receives. In your own words: where did that difference actually come from? Then say why "but the connection was HTTPS" would not have changed your vulnerable-mode answer.
