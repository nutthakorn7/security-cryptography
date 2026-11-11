---
marp: true
theme: default
paginate: true
header: "Cryptography and Network Security · Week 13"
---

<!-- Delivery: 100-minute lab-focused session. 10 Week 12 retrieval/review + 10 brief + 60 practice + 15 debrief + 5 evidence. The scored Week 13 quiz opens Week 14, after this lesson. Full slides and questions are retained as preparation/extension material; individual slide minute estimates are pacing aids, not an additional lecture block. Everyone completes shared60 + assigned Conventional40 or AIR20/10/10. Viva is formative, no extra points. See the worksheet core/extension plan. -->

# Week 13
## End-to-End Encryption (TLS is not enough; the server still reads your messages)
Cryptography and Network Security · Nutthakorn Chalaemwongwan

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
| Hides message plaintext from | a network eavesdropper | a provider without endpoint keys, assuming recipient keys are authentic |
| Where message plaintext can exist | at the TLS-terminating server | at the endpoints; retained chat history is a separate risk |

**The first does not imply the second.** That confusion is the whole lesson.

<!-- Put both definitions on the board side by side. Poll: "if a service is 'all HTTPS,' is your data safe from the company running it?" Most hands say yes — that's the misconception this week dismantles. ~4 min. -->

---

## Why: the server terminates TLS

Alice → **[TLS]** → Server → **[TLS]** → Bob

- The server **decrypts**, holds plaintext, then **re-encrypts** to forward it
- In a TLS-only design it is trusted with plaintext; routing can instead handle ciphertext when clients encrypt first
- A TLS-only provider can read, log, subpoena-respond-to, scan, or leak every message that passes through

<!-- Draw two TLS tunnels meeting AT the server, not passing through it. This is normal, necessary infrastructure — not a bug in TLS. The point: plaintext genuinely exists at that hop, whether or not anyone misuses it. ~5 min. -->

---

## The break: a threat-model mismatch, not a broken primitive

- **CWE-311** — Missing Encryption of Sensitive Data
- **CWE-532** — Insertion of Sensitive Information into Log File (`SERVER SAW:` in vulnerable mode)
- **CWE-312** — Cleartext Storage of Sensitive Information (the database in the Audit-the-AI example)
- TLS is not defeated — it's answering a question nobody asked: *"is the wire safe?"* not *"is the operator safe?"*

**Textbook-secure primitive: TLS does exactly what it promises. Real-system failure: assuming that promise covers something it never claimed.**

<!-- Say the spine line out loud, the way W11 distinguished malleability from nonce reuse. This is NOT "TLS is broken" — TLS's confidentiality-in-transit guarantee holds perfectly. The mistake lives one layer up, in what people assume it implies about who can read the message once it arrives. ~5 min. -->

---

## The fix: move the boundary to the endpoints

- A **fresh AES-256-GCM key** is generated **per message** (fast, symmetric)
- That key is **wrapped to the recipient's public key with RSA-OAEP** (NIST SP 800-56B) — hybrid encryption
- Encryption happens on the sender's device; decryption happens on the recipient's device — this honest relay has no key that opens the payload
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

The `SERVER SAW: ...` line is your **observed evidence artifact** for this HYBRID week — attribute the capture/transcript to your own run.

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

Inspect `docker compose -f docker-compose.fixed.yml logs server`: the `SERVER SAW:` payload has no readable secret. `logs bob` still shows successful decryption. This check also works in PowerShell.

<!-- Compare the server-only and Bob logs live. Bob still recovers the secret while this honest relay sees only ciphertext. Same server binary both times. ~6 min. -->

---

## See it yourself — compare your own server logs

- Run the vulnerable and fixed Compose stacks **on your own machine**, one at a time
- In both runs, `server.py` logs exactly what Alice sends as `SERVER SAW:`
- Compare the server-only logs, then check Bob's output to confirm delivery
- Ask what changes if a malicious server substitutes its own key for Bob's; the lab does not run that attack

<!-- The Docker exercise is the live demonstration. Keep the key-substitution attack conceptual and use the next diagram to explain it. ~5 min. -->

---

## Where the encryption boundary sits

![width:800px Two lanes show Alice sending toward Bob through a server. In the top lane, a TLS-only design terminates encryption at the server, which logs readable plaintext. In the bottom lane, Alice encrypts client-side to the public key the server relays, so this honest relay logs only ciphertext while Bob decrypts. A warning shows the remaining key-trust gap: a malicious server could substitute its own public key, read the message, then re-encrypt it to Bob. The Docker lab does not test that attack.](../labs/week13-e2e-encryption/img/encryption-boundary.svg)

---

## What this lab does NOT prove — root of trust

- Alice trusts whatever public key the server hands her
- A **malicious server could substitute its own key** — a public-key MITM, the messaging cousin of Week 5's Diffie–Hellman MITM
- This lab shows an **honest key relay without Bob's private key** cannot read this payload; it does **not** prove Alice is talking to the real Bob or protect against a malicious key substitution
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

- **First-use trust + safety numbers** — automated key setup, with an option to check identity out of band
- **X3DH historically; PQXDH later** — asynchronous key agreement while Bob is offline
- **Double Ratchet** — limits exposure of old deleted message keys and can recover after fresh, uncompromised ratchet input; retained plaintext or ongoing device control defeats these protections

<!-- Worksheet Q4. Contrast automated session-key rotation with PGP's user-managed keyring. Do not claim a seized phone cannot reveal old plaintext: chat history or recoverable keys may still be present. Current Signal documentation includes PQXDH; X3DH remains useful historical context. ~5 min. -->

---

## 👀 Game — Who's Reading Your Mail?

- Play the messaging **provider**: inspect your own server log while a "private" message passes through
- Watch it sit there in **plaintext**, sender's name and all
- Flip the client to encrypt **client-side** — watch your own log turn into unreadable ciphertext, while the recipient still decrypts it perfectly

<!-- Frame this as a game before releasing them into the lab. The exciting moment: watching your own "private" message sit in cleartext in a log file YOU control is when E2EE stops being an abstract slide and becomes personal. They're playing the operator, not the attacker. ~3 min. -->

---

## Lab today — Worksheet 13

**Shared practical/analysis core: 60 points for everyone.** Complete only your assigned **Conventional written 40** or **AIR-Sec Audit 20 + EiPE 10 + Prompt 10**. Each version totals 100; viva is formative. Full questions remain in the worksheet, with extensions outside the 100-minute class.


> 📋 **Worksheet 13** — `labs/week13-e2e-encryption/worksheet.md` · kickoff: `docker compose -f docker-compose.vulnerable.yml up --build`, then the `.fixed.yml` file

- **Part 1 (essays):** TLS vs. E2EE, the root-of-trust problem, why PGP failed, Signal vs. PGP, open problems in E2EE
- **Part 2a (lab):** capture both modes' logs — plaintext `SERVER SAW` vs. base64 `SERVER SAW`, `BOB DECRYPTED`, and the server-only log check

---

## Assigned written work

- **Assigned AIR-Sec Audit the AI:** critique an AI-written "secure chat backend" that calls itself end-to-end encrypted because it uses HTTPS — same flaw as vulnerable mode, dressed up in reassuring language
- **Assigned AIR-Sec EiPE + Prompt Problem:** explain the browser HTTPS padlock to a non-technical friend; probe an AI on TLS vs. E2EE and check it for false claims

<!-- Mirror W11's lab slide structure. Stress: no host port published, read the container logs, this isn't a browser demo. Audit-the-AI is 20 points for the assigned AIR-Sec version; Conventional students complete their written 40 instead — it's this lecture's exact bug wearing confident prose. Remind: code is unchanged this week, it's a read/run/observe lab, not exploit-and-fix. ~3 min. -->

---

## Key takeaways

- HTTPS/TLS protects the **wire** — it does not protect you from the **operator**; that's a different guarantee entirely
- **Textbook-secure primitive, real-system failure:** TLS wasn't broken — it was trusted for something it never promised
- E2EE closes the gap with hybrid encryption (AES-256-GCM + RSA-OAEP) moved to the **endpoints** — but it still doesn't solve *whose key you're actually encrypting to* (root of trust)

<!-- Recap, 3 lines. Ask what an honest provider without endpoint keys cannot do with the message body, and what metadata or compromised endpoints can still reveal. ~2 min. -->

---

# Questions?
Next week: (see course roadmap)

<!-- Close by previewing the root-of-trust / Key Transparency open problem (Q5c) as a hook for later PKI-at-scale material. Remind students their name/student ID and reproducible attribution apply to the submitted evidence; terminal stamping is optional, same as every other week. ~2 min. -->
