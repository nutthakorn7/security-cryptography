# Term Project Report — CryptoVault (Secure Build)

> Fill in every section. Keep the headings. Total **100 pts** + up to **5 bonus** (see rubric at the end).
> This is **team work** (2–3, nested in your House). Do not share your report or code with other teams.
> This is a **"build it right"** project: you are graded on **correct composition of primitives**, not
> features or polish. Each section below maps to a rubric line — for every primitive, show *where in the
> code* it lives and *why* your choice avoids the exact failure mode its weekly lab demonstrated.

## Cover

| Field | Value |
|---|---|
| Team name (House) | |
| Members (name + ID) | |
| App name & one-line description | |
| Tech stack (language / framework) | |
| Repository URL | |
| Date | |

## AI-tool usage disclosure
*Academic integrity: state how you used any AI tools (ChatGPT, Copilot, etc.) — e.g. searching, coding, translating, drafting. "None" is a valid answer.*

| Tool | How it was used |
|---|---|
| | |

---

## 1. Design Doc — System & Trust Boundary  *(part of §Demo & report clarity, 10 pts)*
*(one diagram + ~1 page)*

- **What the app does:** the vault/note-sharing flow in one paragraph.
- **Diagram (insert image):** client(s), server, data store; where each key lives and for how long;
  the **trust boundary** — mark exactly where plaintext (and the symmetric key protecting an entry)
  is *never* allowed to appear (server memory? network? disk?).
- **Key inventory:** for every key/secret (password-derived key, per-entry data key, sharing
  keypair, signing key, TLS material) state: how it's derived/generated, where it's stored, and who
  can see it.

---

## 2. Password KDF  *(13 pts — Wk2)*

| Field | Value |
|---|---|
| KDF chosen | Argon2id / bcrypt / scrypt / PBKDF2 |
| Parameters | e.g. Argon2id m=…, t=…, p=… / bcrypt cost=… |
| Where in code | `file:line` |
| Salt handling | per-user, random, length |

- **Why this is correct:** why these parameters resist offline GPU cracking.
- **Failure mode avoided (Wk2):** why you did **not** use a raw/fast hash (MD5/SHA-256/HMAC-as-KDF) —
  the exact thing that made the Wk2 leaked-DB crack fast.

---

## 3. AEAD at Rest  *(15 pts — Wk4 / Wk6)*

| Field | Value |
|---|---|
| AEAD construction | AES-GCM / ChaCha20-Poly1305 |
| Nonce strategy | how uniqueness-per-encryption is guaranteed |
| Where in code | encrypt `file:line`, decrypt `file:line` |
| What is authenticated (AAD) | |

- **Why this is correct:** how a fresh, unique nonce is guaranteed for **every** encryption, and how
  tampering is detected on decrypt (tag verification).
- **Failure modes avoided (Wk4/Wk6):** why not raw CBC (bit-flip malleability), and why not a
  fixed/counter-reused nonce (the catastrophic GCM nonce-reuse from the Wk6 material).

---

## 4. Key Exchange / Key Wrapping for Sharing  *(15 pts — Wk5 / Wk10)*

| Field | Value |
|---|---|
| Method | ECDH/X25519 agreement / RSA-OAEP wrap / hybrid |
| Where in code | `file:line` |
| How B's public key is authenticated | (guards against the Wk5 MITM) |

- **Why this is correct:** trace the shared entry's data key from A to B and show it is **never**
  transmitted or stored in the clear — only wrapped/agreed.
- **Failure modes avoided (Wk5/Wk10):** how a MITM can't silently substitute keys (Wk5), and correct
  RSA-OAEP / hybrid use — no reused ephemeral, no textbook RSA (Wk10).

---

## 5. Digital Signatures on Shared Entries  *(15 pts — Wk3 / Wk11)*

| Field | Value |
|---|---|
| Signature scheme | Ed25519 / ECDSA(+low-S) / RSA-PSS |
| What is signed | the entry, or a manifest of it |
| Verify on receipt | `file:line` |

- **Why this is correct:** the recipient verifies authenticity + integrity, and the sender can't
  repudiate. If ECDSA, state how malleability (low-S normalization) and **nonce** handling are managed.
- **Failure modes avoided (Wk3/Wk11):** why not `hash(secret + message)` (length-extension forgery,
  Wk3), and how you avoid ECDSA nonce-reuse key recovery (Wk11).

---

## 6. Transport Security  *(12 pts — Wk12)*

| Field | Value |
|---|---|
| Transport | TLS version / equivalent authenticated channel |
| Cert validation | how the client verifies the server cert & hostname |
| Where in code | `file:line` |

- **Why this is correct:** every client–server link is authenticated and encrypted; no plaintext-HTTP
  fallback.
- **Failure mode avoided (Wk12):** why your client does **not** skip certificate/hostname validation
  (the exact cert-bypass MITM from Wk12).

---

## 7. End-to-End Composition  *(20 pts — the heaviest criterion)*
*Show the WHOLE share-an-entry flow is secure as a system, not just primitive-by-primitive.*

- **Trace one full "share entry" operation** step by step: `KDF → AEAD(at rest) → key exchange/wrap
  → signature → TLS`, naming which primitive does what at each hop and which key is in play.
- **Composition argument:** why no plaintext and no bare symmetric key ever crosses the trust
  boundary you drew in §1 — end to end, including the server's view.
- **Where the seams are:** the one or two points where two primitives meet (e.g. the data key handed
  from AEAD to the key-wrap step) and why that hand-off is safe.

---

## 8. Crypto-Agility Note  *(stretch — +5 bonus, capped at 100)*
*(½–1 page — Wk15)*

- Which primitive(s) above are **broken by Shor's** (asymmetric: your key exchange + signatures) vs.
  merely **weakened by Grover's** (symmetric/hash: double the parameter).
- What you'd swap in to be PQC-ready (e.g. ML-KEM for the key-exchange step, a hash-based/lattice
  signature for §5) and what stays.

---

## 9. Conclusion & Reflection
- Residual risks and what you'd harden next.
- Lessons learned composing primitives you'd previously only *broken*.

---

## Peer-contribution ratings (required — see project/README.md)
*Each member privately rates every teammate (incl. self): Full / Most / Some / Little + a one-line
justification. Attach separately or here; the team mark is scaled per member by the averaged rating.*

---

## Grading rubric (100 + 5 bonus)

| Criterion | Pts | Section |
|---|---|---|
| Password KDF — slow KDF, correctly parameterized, no raw/fast hash (Wk2) | 13 | §2 |
| AEAD at rest — AES-GCM/ChaCha20-Poly1305, unique nonce, no raw CBC (Wk4/Wk6) | 15 | §3 |
| Key exchange / wrapping — symmetric key never in the clear (Wk5/Wk10) | 15 | §4 |
| Digital signatures — real scheme, verified, malleability-safe (Wk3/Wk11) | 15 | §5 |
| Transport security — TLS, no validation-skipping fallback (Wk12) | 12 | §6 |
| **End-to-end composition** — whole flow secure as a system; self-audit explains each choice | 20 | §7 |
| Demo & report clarity — design doc + self-audit write-up | 10 | §1, §9 |
| *Crypto-agility note (stretch)* | *+5* | §8 |

**Total: 100** (+5 bonus, capped so the total cannot exceed 100).

*All work stays within the [ethics policy](../ETHICS.md) — your own team's app and test accounts only.*
