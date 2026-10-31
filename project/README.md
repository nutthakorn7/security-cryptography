# Term Project — CryptoVault

**Teams of 3 normally, 2 where needed for an uneven class (nested in your House). 15% of the final grade.**

This is a **"build it right," not "find the bug"** project — the inverse of the weekly labs. Every
week from Wk2–Wk15 hands you a *broken* construction and asks you to break it, then fix it.
CryptoVault instead asks you to **design and build a correct system from scratch**, composing the
primitives you fixed all term so that none of the classic failure modes (fast-hash passwords, raw
CBC, reused nonces, a symmetric key sent in the clear, an unauthenticated channel) reappear in your
own code. Grading rewards **correct composition** — using each primitive for what it's actually
for, and wiring them together so the whole pipeline holds — over feature count or polish.

## The brief

Teams design and build a small **encrypted vault / note-sharing app**: a user stores secrets
(notes, credentials, small files) protected by a password, and can share an individual vault entry
with another registered user without ever exposing it to the server or to the network in plaintext
— or exposing the symmetric key that protects it.

The build must correctly use, **together**:

1. **Password-derived key via a slow KDF** — Argon2id or bcrypt (scrypt/PBKDF2 with a modern work
   factor is acceptable with justification). A raw or fast hash (MD5/SHA-256/HMAC-as-KDF) is an
   automatic finding here — that's the exact failure Wk2 (hash-cracking) demonstrated.
2. **AEAD for data at rest** — AES-GCM (or ChaCha20-Poly1305) encrypting every stored vault entry,
   with a **fresh, unique nonce per encryption** — never raw CBC, never a fixed or counter-reused
   nonce. This is Wk4 (CBC bit-flip) and Wk6 (CBC padding-oracle / GCM control) applied constructively instead
   of destructively.
3. **A key-exchange or asymmetric step for sharing** — when User A shares a vault entry with User
   B, the symmetric key that protects that entry must reach B via ECDH/X25519 key agreement or
   public-key wrapping (RSA-OAEP or hybrid encryption), never transmitted or stored in the clear.
   This is the constructive counterpart to Wk5 (DH MITM) and Wk10 (hybrid encryption).
4. **Digital signatures on shared entries** — when an entry is shared, the sender signs it (or a
   manifest of it) so the recipient can verify authenticity and integrity, and the recipient can attribute it to the verified signing key, subject to key custody and the trust model. This is Wk3 (MAC/length-extension) and Wk11 (ECDSA
   malleability) applied to a real integrity guarantee — use a proper signature scheme, not `hash(secret + message)`. For ECDSA, low-S
   canonicalizes only the `(r,s)`/`(r,n−s)` twin pair; fresh signatures can have other low-S
   values. Bind replay/idempotency checks to an authenticated application transaction ID or
   nonce and spent-state, rather than relying on signature-byte hashes.
5. **TLS (or an equivalent authenticated transport)** for every client–server link — no
   plaintext-HTTP fallback, no client that skips certificate validation. This is Wk12 (cert-bypass
   MITM) applied correctly.
6. **Stretch goal — crypto-agility note.** A short written note (½–1 page) on what would have to
   change in your design to be PQC-ready: which primitive(s) above are broken by Shor's algorithm
   vs. merely weakened by Grover's, and what you'd swap in (e.g. ML-KEM for the key-exchange step,
   a hash-based or lattice signature for step 4). Ties back to Wk15 (PQC/Lamport). Not required for
   full marks on the core rubric, but required for the crypto-agility bonus (see rubric).

You may pick any tech stack. A CLI tool, a local web app, or a client-server pair are all fine —
the constraint is on the cryptographic composition, not the framework.

## Deliverables

1. **Design doc** — one diagram + one page: what each primitive protects, where keys live and
   how long, and the trust boundary between client and server (who can see plaintext, and when).
2. **Working build** — the vault app implementing all five core primitives (1–5 above) together,
   in a repo with commits that let the team's contributions be traced.
3. **Self-audit** — for each of the five core primitives, a short note (a few sentences each)
   citing *where in the code* it's implemented and *why* the specific choice (KDF, AEAD mode,
   key-exchange method, signature scheme, transport) is correct — i.e., show you know what could
   have gone wrong (the corresponding weekly lab's failure mode) and why your build avoids it.
4. **Crypto-agility note** *(stretch)* — the PQC note described in item 6 above.
5. **Demo** — a walkthrough of create entry → share → verify/decrypt, narrating the primitive
   at each step. Use the **Week 16** studio for work-in-progress feedback and clarification.
   Submit the final **video no longer than 5 minutes before Week 19**, with the build and report
   (put the video link, unlisted YouTube or Google Drive viewable by anyone with the link, in the report PDF);
   it is graded asynchronously using the existing project rubric. Any remaining clarification
   uses **Week 20**. The **Week 19 100 minute session is reserved for the final practical** and
   contains no project Q&A. No particular class headcount is assumed.

## Suggested timeline

| Milestone | Due |
|---|---|
| Team formed + design doc (KDF + AEAD-at-rest plan) | Week 4 |
| KDF + AEAD-at-rest working (local vault, no sharing yet) | Week 7 |
| Sharing flow — key exchange/wrapping + signatures — draft | Week 11 |
| TLS/transport wired in + self-audit drafted | Week 14 |
| Capstone studio — WIP demo & peer review | Week 16 |
| Final build, report/self-audit and ≤5 minute demo video; optional crypto-agility note | Before Week 19 |
| Remaining project clarification and feedback | Week 20 |

The design doc is due early (Wk4) because every later milestone depends on the KDF/AEAD choices
made then; the sharing flow (key exchange + signatures) is scheduled for Wk11, right after
signatures/ZKP (Wk11) and building on key exchange (Wk5) and hybrid encryption (Wk10); the
optional crypto-agility note is scheduled after PQC (Wk15), landing before the final submission.

## Rubric (100 pts)

This project weights **correct composition of primitives** heavily — a build that implements all
five correctly but has a plain UI scores far better than a polished app that gets one primitive
wrong (e.g. a fast hash, a reused nonce, or a symmetric key sent unencrypted). Each primitive is
graded against the specific failure mode its weekly lab exists to teach.

| Criterion | Pts |
|---|---|
| Password KDF — slow KDF (Argon2id/bcrypt), correctly parameterized, no raw/fast hash (Wk2) | 13 |
| AEAD at rest — AES-GCM/ChaCha20-Poly1305, verified-unique nonce per encryption, no raw CBC (Wk4/Wk6) | 15 |
| Key exchange / key wrapping for sharing — symmetric key never transmitted or stored in the clear (Wk5/Wk10) | 15 |
| Digital signatures — real signature scheme, verified on receipt, malleability-safe (Wk3/Wk11) | 15 |
| Transport security — TLS or equivalent securing the sharing link between users, no validation-skipping fallback (Wk12) | 12 |
| **End-to-end composition** — the full share-an-entry flow (KDF → AEAD → key exchange → signature → TLS) is secure as a whole, not just primitive-by-primitive; self-audit correctly explains each choice | 20 |
| Demo & report clarity (design doc + self-audit write-up) | 10 |

**Total: 100.** Crypto-agility note *(stretch)*: **+5 bonus**, added on top and capped so the
total cannot exceed 100 — it lets a team recover points lost elsewhere, but a team that nails the
100-point rubric does not need it for full marks.

**Deadline and late work:** the final build, report and video are due by 23:59 Thai time (ICT) on
the Sunday before the Week 19 class. Late work loses 10% of the project score for each day late (a part day counts as a
day), down to 0.

## Peer-contribution evaluation (individual fairness)

The project is graded team work, so each member's mark is adjusted for actual contribution:
- At submission, **each member privately rates every teammate** (including themselves) on a
  simple scale — e.g. *Full / Most / Some / Little* — with a one-line justification.
- The team mark is **scaled per member** by the averaged rating (typically ×0.8–1.1; an
  unjustified low score is discussed before it's applied).
- Each member's own commit history corroborates who did what. A "single paste-everything"
  contribution is a red flag.

This protects diligent students and removes the "carry a free-rider" problem — the reason team
weight is kept bounded while individual mastery (weekly labs, quizzes, exams) is graded
separately.

## Report

Write up the self-audit and design doc using the fill-in report template
[`REPORT-TEMPLATE.md`](REPORT-TEMPLATE.md) — it mirrors `software-security/project/REPORT-TEMPLATE.md`'s
section-by-section rubric mapping, adapted for CryptoVault: one section per core primitive (design doc
→ KDF → AEAD → key exchange → signatures → transport → end-to-end composition → crypto-agility note →
conclusion), each mapped to its rubric points and the weekly failure mode it must avoid, plus an
AI-tool usage disclosure and the peer-contribution ratings.

All work stays within this course's ethics policy — see [`../ETHICS.md`](../ETHICS.md) (authorized
targets only; here, that means your own team's app and your own test accounts, never another
team's deployment without permission).
