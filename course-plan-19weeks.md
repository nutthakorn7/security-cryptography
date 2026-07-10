# Security & Cryptography — 19-Week Course Plan (KOSEN69)

> **Status: DRAFT — checkpoint before going live.** All 12 teaching weeks (Wk1–6, 10–15) are built
> and verified below — Labs, Hybrids, and Conceptual weeks — plus the capstone (Wk16 — a studio
> day, not a lecture; see `project/README.md`, no vulnerable-target lab by design), both review
> weeks (7, 17), and both exam blocks (8–9, 18–19). This course's own `seed_flags.py` +
> `check_flag_keys.py` + flag-bridge wiring are built and verified (`instructor/platform-build/`).
> Remaining: the deployment catalog (`challenges-import.csv` / `ctfd/challenges.yml`) — labs are
> Docker-verified standalone but not yet live in a CTFd deployment. See
> [OPEN DECISIONS](#open-decisions) before treating this as final.

This course reuses the same 19-week skeleton as [`software-security`](../KOSEN69%20-%20software-security/course-plan-19weeks.md):
**12 teaching weeks (1–6, 10–15) · 1 capstone week (16) · 2 review weeks (7, 17) · 2 exam blocks (8–9, 18–19)**, and is a
second arm of the same preregistered multi-course study (`software-security/instructor/research/preregistration.md`
§3 — this course is named there as "Security & Cryptography").

## Why this course exists, and why it's a separate repo

Committed in the study's preregistration (3 KOSEN-KMITL courses × 2 sections, counterbalanced
AIR-Sec vs Conventional) before this repo existed. A prior offering of this course ran at KOSEN68
(reference material in `Lecture Archive/KOSEN68 - SecAndCrypto/`, **not copied into this public
repo** — see [Reuse & provenance](#reuse--provenance)). It's a separate repo, not a subfolder of
`software-security`, because it's a genuinely separate course (own students, own CTFd deployment,
own `seed_flags.py`) — bundling them would force artificial sharing of flag-key namespaces and
grading data that should stay independent.

## The dual-arm requirement — read this before writing any week

**Every teaching week needs BOTH an AIR-Sec assessment and a Conventional assessment**, not just
one with a label. This is the single most important design constraint carried over from the
advisor review that shaped this plan:

> The old KOSEN68 essay questions ARE essentially the Conventional arm, not just reference
> material — porting them *is* building the control condition. But porting them ≠ building the
> AIR-Sec arm. Every AIR-Sec-condition week — including CONCEPTUAL ones — still needs the anti-AI
> layer (Audit-the-AI, EiPE, Prompt Problem, a personalized artifact, viva) on top. The risk is the
> CONCEPTUAL bucket quietly degrading into "ported old essays with an AIR-Sec label," which is the
> control condition wearing a costume and confounds `course` as a clean replication factor in the
> preregistered crossover.

So for every week below, two things must exist:
- **Conventional arm** — the KOSEN68 essay/discussion question(s) for that topic, minimally
  adapted (same essay format, no AI-resilience layer, no personal artifact).
- **AIR-Sec arm** — the *same underlying concept*, delivered with the AIR-Sec taxonomy: a
  personalized/attributable artifact (flag, seeded bug instance, or per-student parameter),
  Audit-the-AI and/or EiPE and/or Prompt Problem as appropriate to the content, and viva
  spot-checks. A LAB week's flag *is* the personalized artifact; a CONCEPTUAL week's personalized
  artifact is typically a seeded flaw instance or a per-student prompt seed.

## Week classification

Each week is one of three kinds, decided by **whether the source material names a concretely
exploitable bug** (per advisor guidance: default to the plain reading, don't force a CTF wrapper
onto inherently theoretical content):

- **LAB** — a runnable vulnerable/fixed target exists or is directly buildable from the topic.
  Gets a Docker lab + flag, same as `software-security`'s pattern.
- **HYBRID** — a smaller, genuinely demonstrable exploit exists alongside content that stays
  theoretical. Small lab/demo + conceptual material for the rest.
- **CONCEPTUAL** — no natural exploit; content is protocol-design/math analysis. No lab, no flag —
  same precedent as `software-security`'s Week 1 (threat modeling) and Weeks 12–13 (supply-chain/
  cloud static-scan labs), which are honestly flag-less and rubric-graded (see that repo's
  `instructor/platform-build/images/README.md`).

## Course at a glance

Every content week gets a **signature game**, same as `software-security`'s own convention — see
that repo's `course-plan-19weeks.md` for the precedent this mirrors.

| Wk | Topic (KOSEN68 source) | Kind | 🎮 Signature game + AIR-Sec hands-on core | Conventional source |
|----|-------|------|---|---|
| 1  | Intro + threat-modeling a crypto system | **Conceptual** ✅ *built* | 🐍 **"Snake Oil Bingo."** Audit-the-AI: mark off a bingo card of common crypto myths ("military-grade encryption," "quantum-proof because long keys") as they surface in an AI answer to "why does textbook-secure crypto fail in real systems" — a square only counts with a correct one-line reason. *Why it's exciting: spotting a plausible-sounding lie is oddly addictive, and it's the one skill that transfers to every other week this term.* | *(new framing, no direct KOSEN68 week)* |
| 2  | Hash functions | **Lab** ✅ *built* | 🔓 **"Crack the Leaked DB."** Password-cracking a weakly-hashed user DB (unsalted MD5/SHA1) — deliberately distinct from `software-security` W3's ECB oracle. *Why it's exciting: instant feedback — the password either cracks or it doesn't — then watch the identical attack bounce off bcrypt.* | *(no Week2 Questions doc found — build fresh)* |
| 3  | MACs | **Lab** ✅ *built* | 🍪 **"Forge the Admin Cookie."** Hash-only auth-cookie forgery + HMAC length-extension. *Why it's exciting: forging your way into someone else's cookie with pure math, no password needed, feels like a magic trick — until HMAC slams the door.* | `Week3_MACs Questions.docx` (10 Q) |
| 4  | AES (block-cipher modes) | **Lab** ✅ *built* | 🎯 **"Flip Your Way to Admin."** CBC bit-flipping (malleability) tamper attack → why unauthenticated encryption fails; fixed with AES-GCM. Distinct from Wk6 (padding-oracle) and Wk10 (nonce-reuse audit) — together a why-authenticate → how → how-it-still-fails arc. (Pairs with source Q3/Q9 on unauthenticated encryption.) *Why it's exciting: flipping bytes you can't even read to seize admin is the closest thing to "hacking in a movie" this course gets.* | `Week4_AES Questions.docx` (10 Q) |
| 5  | Key Exchanges | **Hybrid** ✅ *built* | 🕵️ **"The Silent Third Wheel."** MITM an unauthenticated DH exchange; small-subgroup confinement stays conceptual (EiPE). *Why it's exciting: you get to be the silent eavesdropper who becomes an active puppet-master — then a single HMAC tag shuts you out completely.* | `Week5_Key Exchanges Questions.docx` (10 Q) |
| 6  | Authenticated Encryption (AEAD) | **Lab** ✅ *built* | 🔮 **"Read the Secret Without the Key."** Padding-oracle attack on MAC-then-encrypt / encrypt-and-MAC, then rebuild with encrypt-then-MAC or AES-GCM — capstone of the symmetric block (Wk3 MAC + Wk4 AES combined correctly). *Why it's exciting: a padding oracle turns a plain 403 error into a skeleton key, recovering a whole secret one byte at a time from nothing but yes/no answers.* | *(new topic, not in KOSEN68 — build fresh)* |
| **7** | **Reflection & Review (pre-midterm)** | — ✅ *built* | 🏆 **"Jeopardy" recap** covering Wk1–6, categories = the six games above. | — |
| **8–9** | **Midterm** (Wk8 written · Wk9 practical) | — ✅ *built* | covers Wk 1–6 | — |
| 10 | Asymmetric & Hybrid Encryption | **Conceptual** ✅ *built* | 🔬 **"Nonce Detective."** Audit-the-AI: find the planted bug in an AI-generated hybrid-encryption implementation. *Why it's exciting: the code looks textbook-correct at a glance — finding the one reused nonce that breaks everything is a genuine "aha," proven by actually recovering the leaked plaintext.* | `Week9 Questions — Asymmetric & Hybrid Encryption.docx` (5 Q) |
| 11 | Signatures & Zero-Knowledge Proofs | **Hybrid** ✅ *built* | 💰 **"Double-Spend the Bank."** Signature malleability demo (MtGox-style, txid mutation); Schnorr/ZKP stays conceptual (EiPE/Prompt Problem). *Why it's exciting: the same signature, mathematically mutated, buys a second withdrawal — real exchanges have lost real money to exactly this trick.* | `Week10 Questions — Signature and ZKP.docx` (5 Q) |
| 12 | Secure Transport (TLS & Noise) | **Hybrid** ✅ *built* | 🎭 **"The Impostor's Certificate."** Cert-validation-bypass MITM against a client that skips hostname checks; PKI trust-model comparison stays conceptual. **The one week in this course where you write the fix yourself** (`alice_student.py`, a stubbed `build_client_context()`) rather than confirm a pre-built one — see [SUBMISSION.md](SUBMISSION.md)'s coding-scope note. *Why it's exciting: your forged certificate sails through — until one line of validation code slams the door in your face.* | `Week11 Questions.docx` (6 Q) |
| 13 | E2E Encryption | **Hybrid** ✅ *built* | 👀 **"Who's Reading Your Mail?"** Vuln/fixed pair: TLS-only chat server that *can* read messages vs. an E2E version that *can't* (server-log evidence). *Why it's exciting: watching your own "private" message sit in plaintext in a server log is the moment end-to-end encryption stops being an abstract idea.* | `Week12 Questions.docx` (5 Q) |
| 14 | User Authentication | **Hybrid** ✅ *built* | 🗝️ **"Never Say the Password."** Small demo: plaintext-password-over-TLS vs. a PAKE-style guarantee; FIDO2/SSO/TOTP comparison stays conceptual. *Why it's exciting: proving you know a secret without ever saying it out loud feels like a magic trick the first time it clicks.* | *(no Questions doc found — build fresh)* |
| 15 | PQC | **Lab** ✅ *built* | 🔑 **"Forge the Admin Signature."** Lamport one-time-signature key-reuse: sign twice, recover private-key bits. *Why it's exciting: a keypair meant to sign exactly once, signed twice — and the private key just falls out of the math.* | 60-Q final exam bank (6 Q on PQC) |
| 16 | Capstone studio (project WIP) | — ✅ *built (`project/README.md`)* | 🏗️ **CryptoVault build.** Term project: teams compose KDF+AEAD+key-exchange+signatures+TLS correctly (see `project/README.md`; `EE2E Project.xlsx` was **not copied in**, rebuilt from scratch). | — |
| **17** | **Reflection & Review (pre-final)** | — ✅ *built* | 🏆 **"Jeopardy: Champions Edition"** covering Wk10–16, categories = the games above. | — |
| **18–19** | **Final** (Wk18 written · Wk19 practical) | — ✅ *built* | cumulative, emphasis Wk10–16 | — |

Cryptocurrency (old-course topic, 9 questions in the exam bank) is **not** given its own teaching
week — it's folded into the Wk18 written-exam item bank instead, since UTXO/BFT/Merkle-proof
content is exam-testable without needing a dedicated lecture slot, and the old course itself
treated it as exam-only supplementary material rather than a weekly lecture with its own Questions
doc.

## Decisions (resolved) & open items

**Resolved (this session):**

1. **Course code → `21025117`.** Tiebreaker from the KOSEN68 archive: `21025117` appears in two
   independent, agreeing course-specific artifacts (the final-exam doc header, and last year's
   Google Form delivery config: "Course: 21025117 Security and Cryptography | Year 4 | Sem
   2/2025"), whereas `02005104` appears only as the *filename* of the syllabus xlsx — which is a
   generic KOSEN whole-curriculum template, not course-specific. `21025117` is now the code in
   `syllabus.md`. (If the registrar's official code later proves to be `02005104`, that's a
   one-line header change.)
2. **Week 6 → Authenticated Encryption (AEAD), a LAB.** The pre-midterm block had 5 topics for 6
   slots. AEAD is the natural capstone of the symmetric block — Wk3 (MAC) + Wk4 (AES) "combined
   correctly." Its lab is a padding-oracle attack on a naive MAC-then-encrypt / encrypt-and-MAC
   construction, then a rebuild with encrypt-then-MAC or AES-GCM — deliberately distinct from
   Wk4's GCM nonce-reuse. (Note: an earlier draft floated "split TLS into two weeks" to fill this
   gap — that was wrong, TLS is post-midterm (Wk12) and its block is already full; the gap was
   always pre-midterm.)

3. **Term project → DONE.** `project/README.md` built: "CryptoVault," teams of 2-3 compose a slow
   KDF + AEAD-at-rest + key-exchange/wrapping + signatures + TLS correctly (not a vuln/fixed find-
   the-bug lab — a build-it-right synthesis project), 100-pt rubric, mirrors
   `software-security/project/`'s format. Timeline starts at **Week 4** (team + design doc), not
   Week 13 — an earlier draft of this table tagged Wk13 as "term project kickoff," which was wrong
   and has been removed; the real cadence is Wk4/7/11/14/16/19, mirroring the sibling course's own
   pacing. `EE2E Project.xlsx` (old course, implied a prior rubric) was **not copied in**
   (student-identifying grade data) — CryptoVault was designed fresh.

4. **`airsec_flag_bridge` de-inline → DONE.** The plugin (in the `software-security` repo) no
   longer hardcodes any course's `CHALLENGES` list — it reads the valid-key whitelist from an
   `AIRSEC_CHALLENGE_KEYS` environment variable, set per-course from that course's
   `seed_flags.py`. When this course gets its own CTFd deployment, it will set its own
   `AIRSEC_CHALLENGE_KEYS` without touching the plugin code. Verified: flag-format parity
   preserved (34 comparisons), the drift guard `check_flag_keys.py` reworked to check the
   deployment env value vs `seed_flags.py` (set-equal), and `docker compose config` hard-errors
   (naming the var) if the whitelist is unset rather than silently breaking attribution. The
   change touched the plugin, `.env.example`, `docker-compose.prod.yml`, `new-cohort.sh`,
   `demo.sh`, the drift guard, and the plugin README — all in the `software-security` repo.

**Resolved (this session), continued:**

5. **`seed_flags.py` + deployment wiring → DONE (CTFd instance itself → still open).**
   `instructor/seed_flags.py` built with this course's own `CHALLENGES = [hash, macs, aes, aead,
   sig, pqc]` — the 6 weeks that actually mint a `FLAG_*` (conceptual/log-line-evidence weeks and
   the capstone deliberately excluded, same precedent as `software-security`'s own flag-less
   weeks). Verified end-to-end: `env`/`gen`/`verify` all tested (correct flag format, no
   collisions across students, wrong-salt correctly rejected). `instructor/check_flag_keys.py`
   built and verified both ways (passes when in sync, correctly detects+reports a deliberately
   introduced drift). `instructor/platform-build/deploy/.env.example` wired with this course's own
   `AIRSEC_CHALLENGE_KEYS` and a **separate** `FLAG_SALT` placeholder (never share with
   software-security's). `instructor/platform-build/README.md` documents that this course
   deliberately **reuses** software-security's plugin/deployment scripts as-is rather than forking
   them — only `seed_flags.py` and this `.env.example` are course-specific.

**Still open:**

6. **An actual running CTFd instance** — the flag-generation mechanism and deployment `.env` are
   ready, but there is no live server, no `challenges-import.csv` image/point-value catalog, and
   no challenge host provisioned for this course yet (see `platform-build/README.md`'s "Not yet
   built" section — these need deployment-specific decisions, e.g. point values and image tags,
   made when a real cohort is being stood up, not guessed here). `SUBMISSION.md` states this
   honestly to students (flags are currently a shared placeholder, not yet personalized).

## Reuse & provenance

Source: `Lecture Archive/KOSEN68 - SecAndCrypto/` (a prior offering of this course, outside any
git repo). What was and wasn't brought in:

- ✅ **Ported as Conventional-arm content**: the six "Questions" docx files' essay questions
  (extracted as plain text, re-typed here — the original .docx files are not copied in).
  The 60-question final exam (`Final_Exam_Security_and_Cryptography.md`) is a directly reusable
  answer-keyed item bank for the Wk18 written exam.
- ✅ **Used as topic/scope reference only**: weekly slide decks (titles and structure informed
  the week list above; slide *content* is rewritten, not copied, since the old decks were built
  for a lecture-only format and this course needs the lab/game framing).
- ❌ **Not copied, deliberately**: `EE2E Project.xlsx` and any poster/report PDFs from the old
  term projects (real student names, project photos, grades — this repo is public); the syllabus
  xlsx (generic KOSEN whole-curriculum template, not course-specific, no useful content found).

## Verification status

All three worked examples are independently verified (not just self-reported by whichever agent
built them — a separate check re-ran each lab from a clean copy):

- **Wk3 (MACs, LAB)** — verified live: `exploit.py` forges an admin cookie via length-extension
  against the vulnerable app (`sha256(secret+data)`) and captures the flag; the identical forged
  cookie is correctly rejected (403) by the HMAC-based fixed app. Forged-padding bytes matched an
  independent hand computation exactly (26-byte glue for a 38-byte message).
- **Wk5 (Key Exchanges, HYBRID)** — verified live, twice (once during build, once independently
  afterward): vulnerable mode's `relay` completes two independent DH handshakes and logs
  `RELAY INTERCEPTED: the launch code is 4471`, with `bob` receiving the same plaintext; fixed
  mode (`SIGNED=1`, HMAC-tagged public keys) makes both `alice` and `bob` print
  `AUTH FAILED - ABORTING` and exit 1, with zero `RELAY INTERCEPTED` occurrences anywhere in the
  logs (`grep -c` confirmed 0). Worksheet's all 10 source questions and full AIR-Sec arm (lab
  evidence, EiPE, Prompt Problem, viva) confirmed present.
- **Wk10 (Asymmetric/Hybrid, CONCEPTUAL)** — no Docker lab by design; the planted bug (fixed
  AES-GCM nonce reused across messages) was confirmed *live*, not just by code review: two
  messages encrypted in one session, tags stripped, `XOR(C1,C2) == XOR(P1,P2)` verified `True`
  against the vulnerable version and `False` against the fixed reference. Answer key's GCM
  authentication-break explanation checked against NIST SP 800-38D.

**Wave 1 LAB weeks — all four independently Docker-verified (build agent + a separate verify
agent that re-ran each lab from a clean scratch copy):**

- **Wk2 (Hash, LAB)** — `exploit.py` cracks the leaked unsalted-MD5 admin hash against a shipped
  wordlist (`sunshine2021`), logs into the vulnerable app (:8094), captures the flag; the bcrypt
  fixed store (:8095) is not crackable by the fast-dictionary technique. Verify agent additionally
  live-attacked :8095 to confirm bcrypt *accepts* the correct password (raises cost, doesn't
  reject) — the pedagogically correct behavior. (Note: `exploit.py`'s own "fixed resists" step is
  an offline CSV check, not a live HTTP attack — fine, but don't misread it as the latter.)
- **Wk4 (AES modes, LAB)** — CBC bit-flip on an unauthenticated token flips `role=guest`→`admin`
  and captures the flag (:8096); the AES-GCM fixed app (:8097) rejects the tamper (403). Verify
  agent *independently reproduced* the bit-flip with pure stdlib (no app code) — same result.
- **Wk6 (AEAD, LAB)** — a from-scratch CBC padding-oracle attack fully recovers the `/secret`
  plaintext (containing the flag) byte-by-byte via the 200/403 padding side channel (:8098); the
  AES-GCM fixed app (:8099) returns a uniform 403, so the same attack recovers nothing.
- **Wk15 (PQC, LAB)** — Lamport OTS key reuse: `exploit.py` signs message `M` and its complement
  `~M`, recovers the full private key, forges a valid signature on the fixed admin message, and
  captures the flag (:8100); the one-time-enforcing fixed app (:8101) refuses the 2nd `/sign`
  (403), so the forgery fails. Both apps also refuse to directly sign the admin message (no
  trivial bypass).

These form the intended arc: **Wk4** (why unauthenticated encryption fails) → **Wk6** (how to fix
it: AEAD) → **Wk10** (how AEAD *still* fails if you reuse a nonce).

- Several build-agent runs across this session hit transient "connection closed / stalled
  mid-response" API errors (not a content/design problem) — recovered each time by retrying with
  smaller, more isolated agent calls or by verifying directly; no data was lost.

**Wave 2 HYBRID weeks — all four independently Docker-verified:**

- **Wk11 (Sig/ZKP, HYBRID, flag pattern)** — ECDSA malleability double-spend: submitting `(r,s)`
  then the malleated `(r, n-s)` (same message, different txid) processes the same withdrawal
  twice on the vulnerable bank (:8102) and captures the flag; the fixed bank (:8103) enforces
  low-S normalization (BIP-62 style) and rejects the malleated twin before it ever reaches
  signature verification. No private key committed (generated in-memory at startup). One
  cosmetic README fix applied: the exploit-run instructions now default to `localhost` (both
  ports are published) instead of a Docker network name that only worked if the checkout
  directory kept its exact name.
- **Wk12 (Transport/TLS, HYBRID)** — cert-validation-bypass MITM: with `VERIFY` unset, `alice`
  accepts the MITM's self-signed impostor cert (`CERT_NONE`) and the secret leaks
  (`MITM INTERCEPTED: the vault code is 7731`); with `VERIFY=1`, cert validation against the demo
  CA fails and `alice` aborts (`CERT VERIFICATION FAILED - ABORTING`) with zero interception.
  Demo CA + certs generated fresh at container startup; nothing committed (`git ls-files` confirms
  no `.pem`/`.key`/`.crt` tracked anywhere in the repo).
- **Wk13 (E2E Encryption, HYBRID)** — with `E2E` unset the messaging server logs the raw plaintext
  (`SERVER SAW: meet at pier 39 at midnight`); with `E2E=1`, alice encrypts client-side (RSA-OAEP
  wraps a fresh AES-256-GCM key) so the server logs only ciphertext, and bob still decrypts and
  recovers the plaintext client-side (`BOB DECRYPTED: ...`). Bob's keypair generated in-memory;
  no key committed.
- **Wk14 (Authentication, HYBRID)** — with `PAKE` unset the server logs the raw password
  (`SERVER SAW PASSWORD: correct-horse-battery`); with `PAKE=1`, a challenge-response protocol
  authenticates without ever transmitting the password (server logs only `nonce=...proof=...`).
  The honest "simplified challenge-response, not a full PAKE (missing offline-dictionary
  resistance + mutual auth)" caveat is present in the code comments, README, worksheet, and answer
  key — not overclaimed as SRP/OPAQUE-equivalent.

- **Built: Wk1, 2, 3, 4, 5, 6, 10, 11, 12, 13, 14, 15** (all 12 teaching weeks) plus Wk16's capstone (`project/README.md`), both review
  weeks (7, 17), and both exam blocks (8–9 midterm; 18–19 final — `instructor/exams/`). Also
  built: this course's own `seed_flags.py` + `check_flag_keys.py` + flag-bridge deployment wiring
  (open item #5's flag mechanism — done; the live CTFd instance itself is a separate, still-open
  deployment task), and the crypto-specific research instruments
  (`instructor/research/pre-post-test.md` + `planted-error-bank.md`, H3/H2 for this replication
  arm of the same study).
  Also built: the exam-rotation `instructor/exams/item-bank.md` (midterm/final pools across
  Concepts/Spot-the-flaw/Applied/Defense-design, plus a CTF pool reusing this course's own
  `hash/macs/aes/aead/sig/pqc` flag keys — mirrors `software-security`'s own item-bank.md).
  **Remaining: Wk16 (capstone)** — no separate lab dir by design, covered by
  `project/README.md` — plus the deployment catalog (`challenges-import.csv` /
  `ctfd/challenges.yml`) needed for an actual live CTFd instance.
  `ETHICS.md`, `SUBMISSION.md`, `AGENDA.md`, and `readings.md` have all been adapted into
  this repo (own policy/pattern, own repo/Docker sandbox, not shared with `software-security`).
