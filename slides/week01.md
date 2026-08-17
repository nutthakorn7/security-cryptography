---
marp: true
theme: default
paginate: true
header: "Security & Cryptography · Week 1"
---

# Week 1
## Security Mindset & Threat-Modeling a Cryptographic System
Security & Cryptography · Nutthakorn Chalaemwongwan

<!-- Hook: ask the room "if I told you a system uses AES-256 and RSA-4096 — the biggest algorithms available — is it safe?" Let a few say yes. Hold the answer. That tension is this entire course. ~2 min. -->

---

## Today

- The course's spine: **textbook-secure primitive, real-system failure**
- What "cryptographically secure" promises — and doesn't
- CIA triad, applied precisely to cryptography
- Trust boundaries + a lightweight threat-modeling process
- 🐍 Game: **Snake Oil Bingo**

<!-- Roadmap. No recap today — this is Week 1, so we're framing the whole 19-week course instead. Name the lab up front: Worksheet 1, no Docker, no flag — a reasoning exercise (Audit-the-AI) instead of a code exploit. ~2 min. -->

---

## The course's spine

Every remaining teaching week takes **one mathematically sound primitive**
and shows **one specific, real way it fails when misused**:

> **Textbook-secure primitive, real-system failure.**

- The primitive's proof holds
- The deployment breaks it anyway
- Implementation bugs, bad randomness, protocol misuse, side channels,
  key-management failure — never the math itself

<!-- Write the boxed line on the board — it is the lens for all 19 weeks. Emphasize: nobody in this course is going to break AES or factor an RSA modulus. Every "break" from here on is a decision made *around* a sound primitive. ~5 min. -->

---

## Preview: the pattern, week by week

| Wk | Primitive (textbook-secure) | Real-system failure |
|---|---|---|
| 2 | Hash functions | Unsalted/unstretched password storage — GPU cracks the DB |
| 4 | AES (block cipher) | CBC with no integrity check — ciphertext bits flip undetected |
| 5 | Diffie–Hellman | No authentication — MITM relays two key exchanges |
| 11 | ECDSA signatures | Nonce reuse algebraically recovers the private key |
| 12 | TLS / certificates | Sound crypto, client skips hostname validation — MITM anyway |

*(Full 11-row table is in this week's README — you'll hypothesize about two
unseen rows in the worksheet.)*

<!-- Don't over-explain each row yet — these are previews, not lessons. Point out the shape: primitive column never says "broken," failure column always names a missing check or a violated assumption. Ask: "what do all five failure descriptions have in common?" ~6 min. -->

---

## What "cryptographically secure" actually promises

- A primitive resists a **well-defined class of mathematical attack**
- Under **stated assumptions** (e.g. discrete log is hard in this group)
- At a **stated security level** (e.g. 128-bit, 256-bit)

That's it. It says **nothing** about:

- Whether the program calling it is secure
- Whether keys are generated, stored, or rotated safely
- Whether the protocol around it is composed correctly

<!-- The precise definition students need to be able to state on the viva (Part 5, Q1). Contrast with the vague "it's unbreakable" framing from marketing. This is also directly the Snake Oil Bingo answer key — "military-grade encryption" fails on exactly this distinction. ~5 min. -->

---

## CIA, specifically for cryptography

| Property | Mechanism | The limit |
|---|---|---|
| **Confidentiality** | Encryption (right primitive/mode/key mgmt) | Says nothing about tampering or availability |
| **Integrity/Authenticity** | MACs, signatures, AEAD — **not encryption alone** | Missing this is the #1 conflation this course fixes |
| **Availability** | Key management (generation, backup, rotation) | Usually a key-mgmt failure, not an algorithm failure |

<!-- Walk each row. Integrity row is the big one — write "encryption ≠ integrity" on the board, it recurs hard in Week 4 (CBC bit-flipping) and Week 6 (padding oracles). Ask: "if I encrypt a message with no MAC, can an attacker change it without me noticing?" (yes). ~6 min. -->

---

## "We encrypted it" is a confidentiality claim only

- Encryption alone answers: **can an adversary read this?**
- It does **not** answer: can an adversary **tamper** with it undetected?
- Encryption with no integrity mechanism → ciphertext can be modified in
  structured, exploitable ways

> Encrypt-then-MAC, or a proper AEAD mode, is what actually closes this gap
> (Week 6). Week 4 shows exactly how the gap gets exploited.

<!-- This is Worksheet Q5 — make sure they can articulate it precisely. Concrete hook: "if you flip one bit of an AES-CBC ciphertext block, what happens to the decrypted plaintext? Predictably — that's the Week 4 exploit." No need to solve it now, just plant the seed. ~5 min. -->

---

## Trust boundaries around key material

A trust boundary = any point where **control over, or visibility into, key
material changes hands**:

- Client vs. server
- Application vs. OS keystore / HSM
- One microservice vs. another
- A developer's laptop vs. production

Every crossing is where key-management failures concentrate: hardcoded
keys in source control, keys logged in plaintext, keys shared across
environments, no rotation or revocation path.

<!-- This is the practical skill for Worksheet Q3 (name 3 crossings in a web app + what goes wrong at each). Draw a simple box diagram: browser → app server → DB, mark the boundaries. Ask for volunteers to name a key-management failure at each. ~6 min. -->

---

## Real incident: sound primitive, broken deployment

**Debian OpenSSL predictable-RNG bug (CVE-2008-0166)**

- OpenSSL's PRNG itself: mathematically fine
- A Debian packaging patch cut the entropy-gathering code
- Result: only ~32,768 possible keys per key type, system-wide
- **CWE-330** — Use of Insufficiently Random Values

<!-- The primitive (OpenSSL's CSPRNG design) was never the problem. A single packaging change destroyed its entropy source, and every key generated on affected Debian systems for ~2 years was guessable. This is the "bad randomness" branch of the throughline table — foreshadow Week 15 (Lamport OTS: reuse breaks even a provably secure scheme). ~5 min. -->

---

## Real incident: the PS3's signing key

**fail0verflow, "Console Hacking 2010" (27C3)**

- Sony used ECDSA — mathematically sound — to sign PS3 firmware
- The implementation reused the **same nonce** for every signature
- Reused nonce + two signatures → private signing key algebraically
  recoverable
- Result: anyone could sign arbitrary "official" firmware

<!-- ECDSA itself is fine; nonce reuse is a protocol-misuse/key-management failure, not a math failure. This directly foreshadows Week 11 — flag it explicitly: "we will do this recovery by hand in Week 11." Ask: "was RSA or ECDSA broken here?" (no — the nonce discipline was). ~5 min. -->

---

## Watch the entropy collapse — live

- The Debian bug above isn't special-cased math — it's a **keyspace** failure
- Shrink the seed source to ~32,768 possible values and the strongest algorithm
  downstream can't save you
- Same shape as Snake Oil squares #4 and #9 — "seeded from the clock," "our session
  tokens are randomly generated, so they can't be guessed"
- This is what square **#23** ("we follow current NIST key-length guidance, so our use
  of cryptography is fine") leaves out — and it's the Exhibit's exact thesis in Part 3

![Two zones sharing one comparison point. Top: the intended design expands a seed assumed to be one of 2^128 possible values into a private key, then publishes a one-way commitment to it -- safe only if that assumption holds. Bottom: in the real deployment the seed actually comes from a narrow, guessable source such as a process ID, so an attacker who only ever sees the published commitment runs every one of the roughly 32,768 real candidates through the identical expand and commit functions, compares each result against that published commitment, and recovers the exact private key in under a second.](img/entropy-collapse.svg)

```sim
seed-crack
```

<!-- expand()/commit() in the sim are toy mixers, not real HKDF/SHA-256 — say so explicitly, same disclaimer as Week 3's toy hash. What's real: the brute-force loop actually runs in the browser, and Verifier B's "years needed" figure is computed live from the exact candidates/sec that loop just measured, not quoted from a table. To make the search-range slider fail, don't nudge it just below the real range — TRUE_SEED is uniform in that range, so near the boundary a "wrong" guess still succeeds most of the time (a genuine coin flip right at the edge, worth naming out loud). Drag it down to roughly a quarter of the real range instead, run it (misses), then push it back to the real range or above (recovers the exact key in well under a second) — that flip is this slide's version of "textbook-secure primitive, real-system failure": expand()/commit() are never the problem, the seed is. Close the loop explicitly to Part 3: the sim is a live refutation of square #23 in the one failure category (randomness/entropy) the Exhibit never names. ~5 min. -->

---

## This week's break: an AI that's never technically wrong

- No primitive has been taught yet — nothing to exploit in code
- Instead: a real, professionally-worded AI answer to *"why does
  textbook-secure crypto fail in real systems?"*
- Every individual factual claim in it is **true**
- It still has exactly **one systematic, load-bearing gap**

> Finding that gap *is* this week's exploit — a reasoning exploit instead
> of a code exploit.

<!-- Set up Part 3 of the worksheet before they read the Exhibit. This is the pattern that recurs every AIR-Sec week from here: distrust confident, correct-sounding AI output; verify against primary literature. Don't reveal the gap yet — let the worksheet do that work. ~4 min. -->

---

## The Exhibit's shape (don't solve it yet)

The AI's answer explains real-world crypto failure entirely in terms of:

- Insufficient **key length** (DES-56, RSA-1024)
- Outdated **algorithm choices** (SHA-1, MD5)
- "Stay current with NIST key-length guidance" as the fix

It's all correct. It is also **only one of several failure categories** —
compare it against everything on this slide deck so far.

<!-- Read the Exhibit aloud from the README/worksheet verbatim (or have a student read it) — this is the Snake Oil Bingo trigger moment. Do not tell them the gap categories; the worksheet task is to name them (key management, randomness/entropy, protocol/composition misuse, side channels) and give an example of each. ~6 min. -->

---

## The correct construction: threat model before you code

Lightweight process, applied to a system that handles cryptographic keys:

1. **Assets** — what needs protecting (keys, plaintext, session tokens)
2. **Adversaries** — who's attacking, what can they see/touch
3. **Attack surface** — every trust boundary the assets cross
4. **Ask, at each primitive:** what assumption does this rely on, and does
   this system actually uphold it?

<!-- This is the antidote to the Exhibit's gap and the antidote to "textbook-secure ≠ system-secure" in general. Walk a mini example on the board: a login form's password — asset, adversary (network sniffer, DB thief), boundary (browser→server, server→DB). This process is what Week 4's project design doc will require. ~7 min. -->

---

## 🐍 Signature game — Snake Oil Bingo

- Everyone gets a bingo card of common crypto myths: *"military-grade
  encryption," "unbreakable 256-bit security," "quantum-proof because the
  key is long enough"*
- As the Exhibit is read aloud and picked apart, mark a square the moment
  its myth surfaces
- A square only counts once your table gives the one-line **technical**
  reason it's wrong
- First verified BINGO wins

<!-- Hand the cards out at the START of the lecture, not at this slide. Verified against the shipped cards (instructor/week01-snake-oil-bingo-key.md §3): the Exhibit read-aloud plus the square you model yourself puts only 3 squares up on any card — one line short of the 4 non-FREE squares any BINGO line needs, so a win is impossible on all six cards if cards come out only now. The trust-boundary, Debian RNG and PS3 slides earlier in this same lecture put the count to ~11 by 1:35, which makes a line arithmetically reachable on 2 of 6 cards — still tight, so budget the prompt bank in the instructor key. If you forgot to hand cards out early, pre-announce a reduced win condition (e.g. any 4 verified squares, not necessarily in a line) before play starts — never after a table is one square away. Model one square yourself first: "military-grade encryption" → not a real technical term, no standard defines "military-grade." Circulate to verify squares — a table must give the real reason, not just "that sounds fake." ~8 min. -->

---

## Lab today — Worksheet 1

> 📋 **Worksheet 1** — `labs/week01-intro/worksheet.md` · Parts 1–5 · 180 min
> **No Docker, no flag** — conceptual week, rubric-graded

- Part 2 — 6 short-answer questions (CIA, trust boundaries, the throughline)
- Part 3 — **Audit-the-AI** (required): what the Exhibit gets right + the
  gap + an example per missing category + rewrite its summary paragraph
- Part 4 — Explain-in-Plain-English + a Prompt Problem
- Part 5 — Viva spot-check, live, no notes

<!-- Walk the deliverable structure before they start. Point out Part 3 is the heaviest (35/100 points) — it's graded on specificity of the gap, not agreement/disagreement. Remind: disclose any AI assistance used anywhere in the worksheet (Part 1). Submit as PDF to learn.zcr.ai/submit; the weekly quiz is at learn.zcr.ai/quiz (one-time code on their slip). -->

---

## Takeaway

- **"Cryptographically secure" is a claim about math, not about your system**
- Real failures cluster at the boundary: bad randomness, key management,
  protocol misuse, side channels — rarely the primitive itself
- **Textbook-secure primitive, real-system failure** — this is the lens for
  every remaining week

<!-- Cold-call: "if AES-256 and RSA-4096 are both unbroken and the system still gets compromised, where does security actually live?" (answer: in the decisions around the primitive — the theme of the whole course). ~3 min. -->

---

# Questions?
Next week: Cryptographic hash functions

<!-- Cliffhanger: "SHA-256 has never been cracked. Next week we crack an entire password database anyway — in minutes, with a GPU. The hash function isn't the problem." Remind: bring a laptop, Week 2 has a Docker lab. -->
