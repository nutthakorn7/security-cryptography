# Week 17 — Reflection & Review (pre-Final)

No new content. Consolidate **Weeks 10–16** (with a quick callback to first-half core concepts —
hashing, MACs, AES modes, key exchange, AEAD) and prepare for the final (Weeks 18–19).

**Kind:** Review (no lab, no flag) · **Format:** same skeleton as [Week 7](../week07-review/) —
this repo mirrors `software-security`'s review-week structure.

## ✅ This week — what to do
1. **Before class** — review **Weeks 10–16** (+ first-half callbacks: Wk2 hash, Wk3 MACs, Wk4 AES
   modes, Wk5 key exchange, Wk6 AEAD).
2. **In class (300 min)** — cumulative review quiz (`../../quizzes/weekly/week17-review-quiz.md`)
   → **Security Jeopardy: Champions Edition** → **mock final CTF/practical** → debrief.
3. **Prepare** — the **final is Weeks 18–19**: Wk18 written (cumulative, emphasis Wk10–16),
   Wk19 capstone practical + project demos.

*Time breakdown follows the shared `AGENDA.md` Week 7/17 review-week block (quiz → Jeopardy →
mock exam → debrief), same as `software-security`.*

## Recap — Weeks 10–16 core lesson

| Wk | Topic | Kind | Core lesson (one line) |
|----|-------|------|-------------------------|
| 10 | Asymmetric & Hybrid Encryption | Conceptual | Asymmetric crypto is too slow for bulk data — real systems wrap a fast symmetric session key (RSA-OAEP/ECDH) with public-key crypto; a *fixed* nonce or reused key still breaks the symmetric layer underneath (GCM two-time-pad). |
| 11 | Digital Signatures & Zero-Knowledge Proofs | Hybrid | A signature proves *authenticity*, not *uniqueness* — ECDSA's `(r, s)` has a valid twin `(r, n−s)`, so malleability lets an attacker mutate a signed message's identity (e.g. txid) without invalidating it; low-S normalization closes the gap. |
| 12 | Secure Transport (TLS & Noise) | Hybrid | "The traffic is encrypted" ≠ "encrypted to the right party" — TLS's security guarantee comes from **certificate validation against a trusted CA chain**, not from the handshake alone; skip verification and MITM is trivial. |
| 13 | End-to-End Encryption | Hybrid | Transport encryption (TLS) protects data *in transit* but the **server is still a trusted third party** that can read plaintext at rest/in processing; true E2EE (client-side hybrid encryption) removes the server from the trust boundary entirely. |
| 14 | User Authentication | Hybrid | Sending a password over TLS still **hands the plaintext to the server** — a challenge-response/PAKE-style protocol proves knowledge of a secret without ever transmitting it, closing a gap TLS alone does not. |
| 15 | Post-Quantum Cryptography | Lab | Quantum computers (Shor) break RSA/ECC outright but only dent AES/SHA (Grover) — hash-based one-time signatures (Lamport) are quantum-resistant *only if the key is used exactly once*; reuse leaks enough private-key bits to forge a second signature. |
| 16 | Capstone Studio | — | Putting the whole term together: threat-model your own build, show the attack, show the fix, and defend the design choices live — the same "attack → root cause → fix" arc as every weekly lab, now end-to-end on your own project. |

**First-half callback (Wk2–6):** unsalted hashing is crackable (Wk2) → a MAC must be
purpose-built, not `hash(secret+data)` (Wk3, length-extension) → encryption without integrity is
malleable (Wk4, CBC bit-flip) → an unauthenticated key exchange is MITM-able (Wk5) → combining
confidentiality + integrity correctly is AEAD, and doing it naively leaks a padding oracle (Wk6).
The Wk10–15 arc is the **asymmetric/protocol-layer sequel** to that symmetric-primitives arc.

## 🎯 Signature activity — "Security Jeopardy: Champions Edition"

Whole-course quiz-show format (mirrors `software-security` Week 17), categories built from the
table above:

| Category | Spans |
|---|---|
| Asymmetric & Hybrid | Wk10 |
| Signatures & ZKP | Wk11 |
| Transport & TLS | Wk12 |
| E2EE | Wk13 |
| Authentication | Wk14 |
| PQC | Wk15 |
| First-Half Callback | Wk2–6 (wildcard row, higher point values) |

- Teams answer in Jeopardy point tiers (100/200/300/400/500 — higher value = harder/more
  applied question, e.g. "explain why" vs. "define").
- Instructor-run; question bank **not yet built** — add it as
  `../../instructor/week17-jeopardy-bank.md` (git-ignored, mirroring the answer-key convention)
  when this week is staffed.
- Scores feed the same season-long Houses/XP leaderboard as every other week.

## 🧪 Mock final prep

- **Format:** dry-run of the exact Week 19 practical format — mixed asymmetric/signature/
  transport/E2EE/auth/PQC challenges, teams, sandbox targets only, **ungraded** (participation).
- **Targets:** reuse this term's built labs — `labs/week10-hybrid-encryption` (audit-the-AI
  nonce-reuse), `labs/week11-signatures-zkp` (ECDSA malleability), `labs/week12-secure-transport`
  (cert-bypass MITM), `labs/week13-e2e-encryption` (TLS-vs-E2EE server-log evidence),
  `labs/week14-authentication` (password-over-the-wire vs. challenge-response),
  `labs/week15-pqc` (Lamport key-reuse forgery) — plus a callback item from Wk2–6.
- **Not built yet:** a dedicated `mock-ctf.md` walkthrough (with hints, self-check scripts) —
  build it alongside the Wk18/19 exam materials, mirroring `software-security/labs/
  week17-review-final-prep/mock-ctf.md`'s table format (challenge / topic / hint / self-check).

## Exam-prep note

The final is **cumulative** (Wk1–16) but **emphasizes Weeks 10–16**, matching the sibling
`software-security` course's Wk17/Wk18 pattern (`course-plan-19weeks.md`: *"Week 18 — Written
exam: cumulative, with emphasis on Weeks 10–16"*). Concretely:
- Wk18 written exam item bank should weight roughly 60–70% Wk10–16 content, 30–40%
  Wk1–6 + review-week callbacks.
- Wk19 capstone practical draws its challenges primarily from Wk10–16's lab arc (see targets
  above), plus one first-half callback challenge, same ratio as the mock above.

## Covers

Weeks 10–16: [hybrid encryption](../week10-hybrid-encryption/), [signatures & ZKP](../week11-signatures-zkp/),
[secure transport](../week12-secure-transport/), [E2E encryption](../week13-e2e-encryption/),
[authentication](../week14-authentication/), [PQC](../week15-pqc/), capstone studio (Wk16 — no
separate lab dir by design, see `project/README.md`).
