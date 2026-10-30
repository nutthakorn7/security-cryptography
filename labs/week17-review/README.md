# Week 17 — Reflection & Review (pre-Final)

No new content. Consolidate **Weeks 10–16** (with a quick callback to first-half core concepts —
hashing, MACs, AES modes, key exchange, AEAD) and prepare for the final (Weeks 18–19).

**Kind:** Review (no lab, no flag) · **Format:** same skeleton as [Week 7](../week07-review/) —
this repo mirrors `software-security`'s review-week structure.

## ✅ This week — what to do
1. **Before class** — review **Weeks 10–16** (+ first-half callbacks: Wk2 hash, Wk3 MACs, Wk4 AES
   modes, Wk5 key exchange, Wk6 AEAD).
2. **In class (100 min)** — cumulative review quiz (`../../quizzes/weekly/week17-review-quiz.md`)
   → **Security Jeopardy: Champions Edition** → **mock final CTF/practical** → debrief.
3. **Prepare** — the **final is Weeks 18–19**: Wk18 written (cumulative, emphasis Wk10–16),
   Wk19 team practical; submit the project video (at most 5 minutes), report and code before W19. Project clarification is in W16/W20.

**100-minute plan:** cumulative quiz 20 + selected Jeopardy clues 15 + two bounded mock
stations 45 + explanation/correction 15 + capture/revision actions 5. The complete bank below
is retained for preparation/extension; it is not an eleven-challenge in-class requirement.

## Recap — Weeks 10–16 core lesson

| Wk | Topic | Kind | Core lesson (one line) |
|----|-------|------|-------------------------|
| 10 | Asymmetric & Hybrid Encryption | Conceptual | Asymmetric crypto is too slow for bulk data — real systems wrap a fast symmetric session key with RSA-OAEP or derive key material through ECDH+KDF; reusing a GCM nonce under the same key leaks relationships between plaintexts. Reusing a GCM key is not itself the failure if nonce requirements are met. |
| 11 | Digital Signatures & Zero-Knowledge Proofs | Hybrid | A signature proves *authenticity*, not *uniqueness* — ECDSA's `(r, s)` has a valid twin `(r, n−s)`, so malleability lets an attacker mutate a signed message's identity (e.g. txid) without invalidating it; low-S rejects that particular twin, while application transaction identity/replay state is still necessary because other valid low-S signatures can exist. |
| 12 | Secure Transport (TLS & Noise) | Hybrid | "The traffic is encrypted" ≠ "encrypted to the right party" — TLS's security guarantee comes from **certificate validation against a trusted CA chain**, not from the handshake alone; skip verification and MITM is trivial. |
| 13 | End-to-End Encryption | Hybrid | Transport encryption (TLS) protects data *in transit* but the **server is still a trusted third party** that can read plaintext at rest/in processing; client encryption keeps message plaintext from the relay under the demo's authenticated-key and honest-client assumptions; key distribution, endpoints and metadata still require trust analysis. |
| 14 | User Authentication | Hybrid | Sending a password over TLS still **hands the plaintext to the server** — the toy challenge-response does not send that string, but permits offline guessing and is not a full PAKE. Distinguish transcript security from complete server compromise in OPAQUE. |
| 15 | Post-Quantum Cryptography | Lab | Quantum computers (Shor) break RSA/ECC outright but only dent AES/SHA (Grover) — hash-based one-time signatures (Lamport) are quantum-resistant *only if the key is used exactly once*; reuse leaks enough private-key bits to forge a second signature. |
| 16 | Capstone Studio | — | Putting the whole term together: threat-model your own build, show the attack, show the fix, and defend the design choices live — the same "attack → root cause → fix" arc as every weekly lab, now end-to-end on your own project. |

**First-half callback (Wk2–6):** unsalted hashing is crackable (Wk2) → a MAC must be
purpose-built, not `hash(secret+data)` (Wk3, length-extension) → encryption without integrity is
malleable (Wk4, CBC bit-flip) → an unauthenticated key exchange is MITM-able (Wk5) → CBC without a MAC can expose a padding oracle; the supplied GCM control rejects tampering (Wk6).
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
- Instructor-run: choose a small set of clues from the existing worksheets/private review materials. Game points are formative; they do not add a new course-weight category.

## 🧪 Mock final prep

- **Format:** teams practise two bounded stations within the 45-minute review block. The W19 exam has three bounded signature/TLS/Lamport stations within 80 task minutes plus 20 minutes for briefing/submission. The broader topic pool below remains optional preparation, **ungraded** (participation).
- **Targets:** reuse this term's built labs — `labs/week10-hybrid-encryption` (audit-the-AI
  nonce-reuse), `labs/week11-signatures-zkp` (ECDSA malleability), `labs/week12-secure-transport`
  (cert-bypass MITM), `labs/week13-e2e-encryption` (TLS-vs-E2EE server-log evidence),
  `labs/week14-authentication` (password-over-the-wire vs. challenge-response),
  `labs/week15-pqc` (Lamport key-reuse forgery) — plus a callback item from Wk2–6.
- **Walkthrough:** a dedicated [`mock-ctf.md`](mock-ctf.md) (with hints + self-check pointers,
  no flags) mirrors `software-security/labs/week17-review-final-prep/mock-ctf.md`'s table format
  (challenge / topic / hint / self-check): six post-midterm challenges (Wk10–15) plus a first-half
  callback round (Wk2–6).

## Exam-prep note

The final is **cumulative** (Wk1–16) but **emphasizes Weeks 10–16**, matching the sibling
`software-security` course's Wk17/Wk18 pattern (`course-plan-19weeks.md`: *"Week 18 — Written
exam: cumulative, with emphasis on Weeks 10–16"*). Concretely:
- Wk18 written exam item bank should weight roughly 60–70% Wk10–16 content, 30–40%
  Wk1–6 + review-week callbacks.
- Wk19 practical uses bounded signature/TLS/Lamport stations. Earlier topics support reasoning and are assessed in the written paper; there is no extra first-half practical station beyond the 80-minute task plan.

## Covers

Weeks 10–16: [hybrid encryption](../week10-hybrid-encryption/), [signatures & ZKP](../week11-signatures-zkp/),
[secure transport](../week12-secure-transport/), [E2E encryption](../week13-e2e-encryption/),
[authentication](../week14-authentication/), [PQC](../week15-pqc/), capstone studio (Wk16 — no
separate lab dir by design, see `project/README.md`).
