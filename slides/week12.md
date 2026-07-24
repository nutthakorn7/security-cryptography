---
marp: true
theme: default
paginate: true
header: "Security & Cryptography · Week 12"
---

# Week 12
## Secure Transport / TLS (certificate-validation-bypass MITM)
Security & Cryptography · Nutthakorn Chalaemwongwan

<!-- Hook: ask "if the padlock icon is green and the URL says https, is the connection safe?" Most students say yes. Today's answer: it means encrypted — not necessarily encrypted to the party you think you're talking to. That gap is the whole lecture. ~2 min. -->

---

## Today

- The TLS handshake: what it authenticates — and what it doesn't
- X.509 certificates & the CA chain of trust
- Hostname verification (SAN, RFC 6125)
- Live MITM: a client that skips certificate validation
- 🎭 Game: **The Impostor's Certificate**

<!-- Roadmap, 1 min. Flag the lab up front: run the demo in vulnerable + fixed mode, then — the one week in this course where you write the fix yourself — implement `build_client_context()` in `alice_student.py`. ~1 min. -->

---

## Recap — Week 11

- A digital signature lets **anyone with the public key** verify a claim — no shared secret needed
- A signature is also a non-interactive **zero-knowledge proof**: it convinces you the signer knows the private key, without revealing it
- This week: a certificate **is** a CA's signature over "this key belongs to this name" — watch what happens when nobody checks it

<!-- Bridge from W11. W11 = signatures/ZKP as primitives (unforgeable, but ECDSA's encoding wasn't unique). W12 = signatures as the load-bearing piece of Web PKI — the CA's signature is the ONLY thing that turns a certificate's claim into something checkable. Ask: "why can't a certificate just use a MAC instead of a signature?" (a CA can't hand its verification key to every browser — that's the shared-secret problem signatures solve). ~2 min. -->

---

## The TLS handshake — three jobs

- **Key exchange** — negotiate a shared session key → confidentiality
- **Server authentication** — the server presents a certificate claiming an identity
- **`CertificateVerify`** — server proves it holds the *private key* matching that cert
- Skip any one of the three and a machine-in-the-middle is back on the table

<!-- Core mental model for the whole lecture — write it on the board. This week's bug lives entirely in job #2: the client never actually checks whether to believe the presented certificate. Preview: today's demo keeps key exchange and CertificateVerify intact — the ONLY thing missing is validating who signed the cert. ~5 min. -->

---

## X.509 certificates & the chain of trust

- A certificate is a **claim**: "this public key belongs to `bob`"
- Anyone can generate a certificate that claims to be `bob` — self-signing costs nothing and needs no permission
- A **Certificate Authority's signature** is what makes the claim checkable — your OS/browser already trusts the CA, so a CA-signed cert inherits that trust
- No signature from a trusted CA → no chain → nothing backs the claim

<!-- RFC 5280 territory. Draw the chain on the board: root CA -> (intermediate) -> leaf cert. Analogy: a notary's stamp doesn't change what a document says, it changes who's willing to back it. Preview: the lab's impostor certificate claims CN=bob but has zero chain to the demo CA — it's the self-signing half of this slide, live. ~5 min. -->

---

## Hostname verification

- A valid chain of trust still isn't enough — the *name* in the cert must match the name you meant to connect to
- Check the **SAN** (Subject Alternative Name) — RFC 6125 — not just the legacy CN field
- In this week's lab, **both** the real and impostor certs carry `CN=bob`, `SAN=DNS:bob` — hostname matching alone cannot tell them apart
- You need **both**: chain of trust *and* hostname match

<!-- Important nuance to set up the punchline. Ask: "if the impostor's name is correct, what's left to catch it?" (only the signature/issuer). Foreshadow: the fixed client's failure reason will be a TRUST failure, not a NAME failure — that distinction is the entire point of this lab (see Part 2c/2e). ~4 min. -->

---

## The lab: 4 services, one Docker network

| Service | Role | What it does |
|---|---|---|
| `gen_certs.py` | init | generates a demo CA, Bob's CA-signed cert, and a **self-signed impostor** (also `CN=bob`) |
| `bob.py` | legit server | mostly idle — Alice never dials it directly |
| `mitm.py` | attacker | presents the impostor cert; logs `MITM INTERCEPTED: <secret>` on success |
| `alice.py` | client | dials `mitm`, believing it's `bob`; behavior set by env var `VERIFY` |

<!-- Draw the topology. The key line to say out loud: "Alice's PEER_HOST is literally mitm, not bob" — that's the premise of an attacker who controls the network path (DNS spoofing, ARP poisoning, rogue AP — the how doesn't matter, the demo starts from "attacker already has the path"). Point out mitm.py's code is IDENTICAL in vulnerable and fixed runs — only Alice's validation changes. ~5 min. -->

---

## The break: `CERT_NONE`, `check_hostname=False`

```
ALICE: TLS handshake succeeded WITHOUT verifying the server cert
ALICE: sent encrypted message ('the vault code is 7731')
MITM INTERCEPTED: the vault code is 7731
```

- **CWE-295** — Improper Certificate Validation
- **CWE-300** — Channel Accessible by Non-Endpoint
- The handshake genuinely succeeds — real crypto, real session key — just negotiated with the wrong party

<!-- The core lesson slide — say it like the course spine: "textbook-secure primitive (TLS's crypto), real-system failure (nobody checked who signed the cert)." Ask: "the log says handshake SUCCEEDED — was the traffic encrypted?" (yes, genuinely). "So why did the attacker read it in cleartext?" (because the attacker IS the other endpoint of that encrypted channel — CWE-300). ~6 min. -->

---

## "Encrypted" ≠ "encrypted to the right party"

- Encryption protects a channel; only **certificate validation** ties that channel to a specific identity
- `CertificateVerify` even passes — the MITM genuinely holds the impostor cert's private key
- `check_hostname=False` + `CERT_NONE` = Alice never asks "is this actually bob?"
- Whoever answers when Alice dials `mitm:8443` gets treated as `bob` — no questions asked

<!-- Reconciles the counterintuitive fact from the last slide — this is the exact viva question (Part 2e Q1). Have a student explain it back in their own words before moving on: key exchange ran correctly, CertificateVerify ran correctly — the ONLY missing check was "should I trust who signed this cert." ~4 min. -->

---

## The fix: `VERIFY=1` — load the CA, keep hostname checking

```
ALICE: connecting to mitm:8443 as if it were 'bob' -- FIXED (VERIFY=1)
CERT VERIFICATION FAILED - ABORTING
ALICE: (reason: self-signed certificate)
```

- `mitm.py` is **byte-for-byte unchanged** — same impostor cert, same attempt
- Alice now trusts *only* the demo CA; the impostor has no chain to it
- Fails **during the handshake, before the secret is sent**
- Reason given: a **trust/issuer** error — not a hostname mismatch (the name was correct all along)

<!-- Emphasize what changed and what didn't — nothing about the attacker changed, only Alice's validation (this is Part 2e Q2). Tie back to the hostname slide: since the impostor's SAN is correct, only a real chain-of-trust check catches it — this is CWE-295, fixed by turning validation back on. ~6 min. -->

---

## The real-world version of this bug

- `verify=False` (Python `requests`) · `CERT_NONE` (Python `ssl`) · `InsecureSkipVerify` (Go)
- Almost always copy-pasted to silence an SSL error — "just make it work"
- **"It's HTTPS, so it's encrypted"** is true — and irrelevant if nobody checked *who* is on the other end
- This is the single most common real-world TLS mistake — not a CA compromise, not a crypto break

<!-- Direct preview of Part 2b (Audit the AI): an AI assistant "fixes" SSL errors for a teammate by adding verify=False and then claims the connection is secure because it's HTTPS. Flag it now so students recognize the trap immediately in the worksheet — same bug, dressed up as confident AI-generated code. ~5 min. -->

---

## Beyond the demo — this week's essay arm

- Why SSL was retired, what TLS 1.3 changed
- **Forward secrecy** — each session gets an ephemeral key, so a leaked long-term key can't decrypt *past* traffic (contrast: legacy static-RSA key exchange, removed in TLS 1.3 — see **Heartbleed** as the case for why that mattered)
- **0-RTT** — the performance-vs-replay trade-off
- Mitigations for a **compromised CA**: pinning, revocation (CRL/OCSP), Certificate Transparency
- TLS vs. the **Noise Protocol Framework**

<!-- These are Part 1's six essay questions — written up individually (150-250 words each), not fully lectured today. Flag them so students know what to read/think about before writing. Worth saying explicitly: a compromised CA would produce a VALIDLY-chained cert and defeat today's exact check — that gap is real and is exactly what Q5 asks about. ~4 min. -->

---

## 🎭 Game — "The Impostor's Certificate"

- You play the attacker: stand in for the server with nothing but a self-signed cert you generated yourself
- Watch a careless client hand you its secret — "encrypted" the whole time
- Flip on real certificate validation — the *same* impostor cert gets rejected before a single byte ships

<!-- Run the vulnerable-mode demo live (or have pairs run it themselves first, then watch fixed mode together). The thrill: your forgery clears the padlock/lock-icon check in vulnerable mode; one line of validation code kills it in fixed mode. Same forged cert both times — only the client changed. ~3 min. -->

---

## Lab today — Worksheet 12

> 📋 **Worksheet 12** — `labs/week12-secure-transport/worksheet.md` · kickoff: `docker compose -f docker-compose.vulnerable.yml up --build`

- **Part 1 (essays):** SSL→TLS, handshake security roles, forward secrecy, 0-RTT, Web PKI, TLS vs Noise
- **Part 2a:** capture vulnerable + fixed logs, then **write the fix yourself** in `alice_student.py`
- **🤖 Audit the AI:** critique a `verify=False` "fix" that an AI assistant swears is secure
- **EiPE + Prompt Problem + viva prep**

<!-- The graded output — mirror the structure from earlier weeks. Stress Part 2a step 5: this is the ONE lab in the course where they write the validation code themselves, not just confirm a pre-built fix — one stdlib call (SSLContext + check_hostname) does chain + hostname correctly, no hand-rolling needed. Remind: identity-proof screenshot required alongside every captured log. ~3 min. -->

---

## Key takeaways

- TLS's crypto is textbook-sound — key exchange and signatures both work exactly as designed
- **Textbook-secure primitive, real-system failure:** the bug was skipping *validation*, not broken math
- "Encrypted" and "encrypted to the right endpoint" are different claims — only certificate validation bridges them

<!-- Recap, 3 lines — say the spine phrase out loud, same thread as every week. Cold-call: "name the exact line that turned this from secure to broken" (CERT_NONE / check_hostname=False — or in the real world, verify=False). ~2 min. -->

---

# Questions?
Next week: End-to-end encryption

<!-- Close with a viva-style question as a preview of live spot-checks: "the impostor cert has the correct name — so why does the fixed client reject it, and at what point in the exchange, before or after the secret is sent?" Remind students the MITM INTERCEPTED line is their personalized evidence artifact — pair it with an identity-proof screenshot. ~2 min. -->
