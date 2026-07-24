---
marp: true
theme: default
paginate: true
header: "Security & Cryptography · Week 13"
---

# Week 13
## End-to-End Encryption (TLS is not enough; the server still reads your messages)
Security & Cryptography · Nutthakorn Chalaemwongwan

<!-- Hook: ask "if an app is HTTPS everywhere, can the company running the server still read your messages?" Most students say no. Reveal: by default, yes — that's exactly what "HTTPS everywhere" leaves open. Today closes that gap. ~2 min. -->

---

## Today

- **Transport encryption** (TLS/HTTPS) vs. **end-to-end encryption** (E2EE) — different guarantees
- The server as a trusted third party: TLS *terminates* there
- Hybrid encryption at the endpoints: AES-256-GCM wrapped in RSA-OAEP
- What E2EE still doesn't prove: the root-of-trust problem
- 👀 Game: **Who's Reading Your Mail?**

<!-- Roadmap, 1 min. Flag the lab: same server code in both modes, two client behaviors — students tail their own server's log and watch it flip from plaintext to unreadable gibberish while the recipient still decrypts fine. -->

---

## Recap — Week 12

- TLS asked: is this channel going to the **right endpoint**? (certificate-validation MITM)
- The fix was checking the chain to a trusted CA before sending anything
- This week: even when the channel IS the right endpoint, that endpoint is the **server** — and encryption *to* the server is not encryption *from* the server

<!-- Bridge from W12. W12 = "are you talking to who you think you're talking to." W13 = "even if yes, that party still reads everything you send it." Ask: does TLS ever hide plaintext from the server itself, even when certificate validation is perfect? (No — never did.) ~2 min. -->

---

## Two different guarantees

| | **Transport encryption (TLS/HTTPS)** | **End-to-end encryption (E2EE)** |
|---|---|---|
| Protects data | *in transit* | *from the server operator itself* |
| Hides plaintext from | a network eavesdropper | the provider running the service |
| Where plaintext can exist | at every hop, incl. the server | only on the two endpoints |

**The first does not imply the second.** That confusion is the whole lesson.

<!-- Put both definitions on the board side by side. Poll: "if a service is 'all HTTPS,' is your data safe from the company running it?" Most hands say yes — that's the misconception this week dismantles. ~4 min. -->

---

## Why: the server terminates TLS

Alice → **[TLS]** → Server → **[TLS]** → Bob

- The server **decrypts**, holds plaintext, then **re-encrypts** to forward it
- It is a trusted third party **by construction**, not by accident — app logic, routing, storage all need plaintext at that hop
- A TLS-only provider can read, log, subpoena-respond-to, scan, or leak every message that passes through

<!-- Draw two TLS tunnels meeting AT the server, not passing through it. This is normal, necessary infrastructure — not a bug in TLS. The point: plaintext genuinely exists at that hop, whether or not anyone misuses it. ~5 min. -->

---

## The break: a threat-model mismatch, not a broken primitive

- **CWE-311** — Missing Encryption of Sensitive Data
- **CWE-319** — Cleartext Transmission of Sensitive Information (here: cleartext *storage on the relay*, even though transit was encrypted)
- TLS is not defeated — it's answering a question nobody asked: *"is the wire safe?"* not *"is the operator safe?"*

**Textbook-secure primitive: TLS does exactly what it promises. Real-system failure: assuming that promise covers something it never claimed.**

<!-- Say the spine line out loud, the way W11 distinguished malleability from nonce reuse. This is NOT "TLS is broken" — TLS's confidentiality-in-transit guarantee holds perfectly. The mistake lives one layer up, in what people assume it implies about who can read the message once it arrives. ~5 min. -->

---

## The fix: move the boundary to the endpoints

- A **fresh AES-256-GCM key** is generated **per message** (fast, symmetric)
- That key is **wrapped to the recipient's public key with RSA-OAEP** (NIST SP 800-56B) — hybrid encryption
- Encryption happens on the sender's device; decryption happens on the recipient's device — the server never holds a key that opens either
- Same hybrid pattern as Week 10's KEM/DEM — deployed here into an actual messaging shape

<!-- Callback to Week 10's hybrid-encryption slide — recognize the pattern before applying it. Ask "why not just RSA-encrypt the whole message?" (RSA is slow and size-limited; that's exactly why you wrap a fast symmetric key instead). ~5 min. -->

---

## The demo: one server, two client roles

| Service | Role | What it does |
|---|---|---|
| `server.py` | The provider | `/pubkey`, `/send`, `/fetch`. Logs **verbatim**: `SERVER SAW: <payload>`. **Byte-for-byte identical code in both modes** — it has no idea whether E2EE is on. |
| `alice.py` | Sender | Vulnerable: sends raw plaintext. Fixed: fetches bob's public key, encrypts **client-side** before sending. |
| `bob.py` | Recipient | Vulnerable: reads plaintext. Fixed: generates an RSA keypair **in memory**, publishes only the public half, decrypts client-side → `BOB DECRYPTED: <secret>`. |

<!-- Point at server.py's log line first. The whole lesson in one sentence: nothing about the server changes between modes — only what Alice chooses to hand it changes. ~5 min. -->

---

## Vulnerable mode — watch your own log leak

```
week13-server  | SERVER: listening on 0.0.0.0:8080 (E2E=False)
week13-alice   | ALICE: sending the raw plaintext (no E2EE)
week13-server  | SERVER SAW: meet at pier 39 at midnight
week13-bob     | BOB RECEIVED: meet at pier 39 at midnight
```

The `SERVER SAW: ...` line is your **personalized evidence artifact** for this HYBRID week — pair it with your identity proof.

<!-- Run this live: `docker compose -f docker-compose.vulnerable.yml up --build`. Let students spot the `SERVER SAW` line themselves before you point at it — that's the punchline. Note: no literal TLS cert exists in this lab; vulnerable mode *models* "HTTPS in transit, plaintext stored at the server." ~6 min. -->

---

## Fixed mode — same server, unreadable log

```
week13-server  | SERVER: listening on 0.0.0.0:8080 (E2E=True)
week13-bob     | BOB: published my public key, waiting for a message
week13-alice   | ALICE: encrypted the secret to bob's public key (client-side)
week13-server  | SERVER SAW: eyJlbmNfa2V5IjogImdQY29aZVcrSUdOSVJt...
week13-bob     | BOB DECRYPTED: meet at pier 39 at midnight
```

`grep -c "meet at pier 39 at midnight"` on the **server** log → **0** (vs. **1** in vulnerable mode).

<!-- Run the grep live, side by side with the previous slide's evidence. Bob still recovers the secret — E2EE is about who CAN'T read it, not about breaking delivery. Same server binary both times. ~6 min. -->

---

## What this lab does NOT prove — root of trust

- Alice trusts whatever public key the server hands her
- A **malicious server could substitute its own key** — a public-key MITM, the messaging cousin of Week 5's Diffie–Hellman MITM
- This lab proves the **server cannot read** an E2EE message — it does **not** prove Alice is talking to the real Bob
- Stays conceptual this week: Worksheet Q2 and the Audit-the-AI exercise

<!-- Say this explicitly — don't let students walk away overclaiming what the demo showed. Tie back to the Week 5 DH MITM recap for continuity. Ask: "how would Alice know the key really came from Bob?" (out-of-band verification, safety numbers, a CA, a key-transparency log — Q2.) ~5 min. -->

---

## Why encrypted email (PGP) never took off

- **Key discovery**: how do you even get someone's public key in the first place?
- **Metadata leaks** even when the message body is encrypted (who, when, subject lines in S/MIME)
- **Usability**: "manage your own long-term keyring" defeated ordinary users — Whitten & Tygar, *Why Johnny Can't Encrypt*, USENIX Security 1999

<!-- Worksheet Q3. Ask the class why they've never personally used PGP despite it existing since 1991. Usability, not math, is what killed mass adoption — the crypto in PGP was never the weak link. ~4 min. -->

---

## How Signal improves on PGP

- **TOFU** (trust on first use) — key management happens automatically, mostly invisible to the user
- **X3DH** — an asynchronous handshake; works even if Bob is offline when Alice sends
- **Double Ratchet** — **forward secrecy** (a key compromise today doesn't expose past messages) + **post-compromise security** (the session heals after a compromise)

<!-- Worksheet Q4. Contrast with PGP's static long-term keyring: Signal rotates keys continuously and automates the trust decisions a PGP user had to make by hand. Concrete example: if your phone is seized tomorrow, can they read yesterday's messages? With Double Ratchet, no. ~5 min. -->

---

## 👀 Game — Who's Reading Your Mail?

- Play the messaging **provider**: `tail` your own server's log while a "private" message passes through
- Watch it sit there in **plaintext**, sender's name and all
- Flip the client to encrypt **client-side** — watch your own log turn into unreadable ciphertext, while the recipient still decrypts it perfectly

<!-- Frame this as a game before releasing them into the lab. The exciting moment: watching your own "private" message sit in cleartext in a log file YOU control is when E2EE stops being an abstract slide and becomes personal. They're playing the operator, not the attacker. ~3 min. -->

---

## Lab today — Worksheet 13

> 📋 **Worksheet 13** — `labs/week13-e2e-encryption/worksheet.md` · kickoff: `docker compose -f docker-compose.vulnerable.yml up --build`, then the `.fixed.yml` file

- **Part 1 (essays):** TLS vs. E2EE, the root-of-trust problem, why PGP failed, Signal vs. PGP, open problems in E2EE
- **Part 2a (lab):** capture both modes' logs — plaintext `SERVER SAW` vs. base64 `SERVER SAW`, `BOB DECRYPTED`, and the `grep -c` showing `0`
- **🤖 Audit the AI:** critique an AI-written "secure chat backend" that calls itself end-to-end encrypted because it uses HTTPS — same flaw as vulnerable mode, dressed up in reassuring language
- **🧠 EiPE + Prompt Problem:** explain WhatsApp's "lock icon" to a non-technical friend; probe an AI on TLS vs. E2EE and check it for hallucinated claims

<!-- Mirror W11's lab slide structure. Stress: no host port published, read the container logs, this isn't a browser demo. Audit-the-AI is 15 of 100 points and is NOT optional — it's this lecture's exact bug wearing confident prose. Remind: code is unchanged this week, it's a read/run/observe lab, not exploit-and-fix. ~3 min. -->

---

## Key takeaways

- HTTPS/TLS protects the **wire** — it does not protect you from the **operator**; that's a different guarantee entirely
- **Textbook-secure primitive, real-system failure:** TLS wasn't broken — it was trusted for something it never promised
- E2EE closes the gap with hybrid encryption (AES-256-GCM + RSA-OAEP) moved to the **endpoints** — but it still doesn't solve *whose key you're actually encrypting to* (root of trust)

<!-- Recap, 3 lines — say the spine phrase out loud, it threads every week. Cold-call: "name one concrete thing a provider can no longer do once messages are truly E2EE" (hand over readable messages on subpoena, scan them for ads, leak them in a breach). ~2 min. -->

---

# Questions?
Next week: (see course roadmap)

<!-- Close by previewing the root-of-trust / Key Transparency open problem (Q5c) as a hook for later PKI-at-scale material. Remind students the identity-proof + timestamp requirement applies to their captured log evidence, same as every other week. ~2 min. -->
