# Security & Cryptography

A hands-on undergraduate course on applied cryptography: how cryptographic primitives fail when
misused, and how to use them correctly. Companion course to
[`software-security`](../KOSEN69%20-%20software-security/) — same 19-week skeleton, same
AIR-Sec pedagogy, same preregistered study, different subject matter and a separate repo/CTFd
deployment.

> ⚠️ **Status: DRAFT.** All 12 teaching weeks are built (Weeks 1–6, 10–15 — Labs, Hybrids, and
> Conceptual weeks; see [course-plan-19weeks.md](course-plan-19weeks.md) for which is which),
> plus the capstone (Week 16 — a studio day, not a lecture; covered by `project/README.md`, no
> vulnerable-target lab by design), both review weeks (7, 17), and both exam blocks (8–9, 18–19).
> This course's own `seed_flags.py` + `check_flag_keys.py` + flag-bridge wiring are built and
> verified (`instructor/platform-build/`). Remaining: the deployment catalog
> (`challenges-import.csv` / `ctfd/challenges.yml`) — the labs are Docker-verified standalone but
> not yet live in a CTFd deployment. Do not use this for a live course yet.

> ⚠️ **Ethics first.** All offensive techniques are taught for **defensive and authorized testing
> only**. Attack only the provided sandbox targets. See [`ETHICS.md`](ETHICS.md) for this
> course's authorized-use policy.

---

## Quick start

```bash
git clone <this-repo-url>
cd security-cryptography
cd labs/week03-macs
cat README.md
docker compose up
```

**Base requirements:** Docker Desktop, Git, a browser proxy where relevant. Same Docker-first
approach as `software-security` — no full VM required.

## Course at a glance

| Wk | Topic | 🎮 Signature game |
|----|-------|------------|
| 1  | Intro & threat-modeling a crypto system | 🐍 "Snake Oil Bingo" |
| 2  | Hash functions | 🔓 "Crack the Leaked DB" |
| 3  | MACs | 🍪 "Forge the Admin Cookie" |
| 4  | AES / block-cipher modes | 🎯 "Flip Your Way to Admin" |
| 5  | Key Exchanges | 🕵️ "The Silent Third Wheel" |
| 6  | Authenticated Encryption (AEAD) | 🔮 "Read the Secret Without the Key" |
| **7**  | **🔁 Reflection & Review (pre-midterm)** | 🏆 "Jeopardy" recap |
| **8–9** | **📝 Midterm** (Wk8 written · Wk9 CTF practical) | — |
| 10 | Asymmetric & Hybrid Encryption | 🔬 "Nonce Detective" |
| 11 | Signatures & Zero-Knowledge Proofs | 💰 "Double-Spend the Bank" |
| 12 | Secure Transport (TLS) | 🎭 "The Impostor's Certificate" |
| 13 | End-to-End Encryption | 👀 "Who's Reading Your Mail?" |
| 14 | User Authentication | 🗝️ "Never Say the Password" |
| 15 | Post-Quantum Cryptography | 🔑 "Forge the Admin Signature" |
| 16 | Capstone studio (CryptoVault WIP) | 🏗️ Build & peer review |
| **17** | **🔁 Reflection & Review (pre-final)** | 🏆 "Jeopardy: Champions Edition" |
| **18–19** | **📝 Final** (Wk18 written · Wk19 CTF practical) | — |

Full details, technical rationale, and each game's "why it's exciting" hook:
[course-plan-19weeks.md](course-plan-19weeks.md). Build/verification status per week is tracked
there too.

## Repository layout

```
security-cryptography/
├── README.md                  ← you are here
├── course-plan-19weeks.md     ← full week-by-week plan, classification, open decisions
├── syllabus.md                ← outcomes, assessment, references
├── labs/
│   ├── week01-intro/              ← CONCEPTUAL — threat-modeling a crypto system, Audit-the-AI (no Docker target)
│   ├── week02-hash/               ← LAB — unsalted-hash password cracking
│   ├── week03-macs/               ← LAB — hash-only cookie forgery / length-extension
│   ├── week04-aes-modes/          ← LAB — CBC bit-flipping (malleability)
│   ├── week05-key-exchanges/      ← HYBRID — unauthenticated DH MITM
│   ├── week06-aead/               ← LAB — CBC padding-oracle attack
│   ├── week07-review/             ← pre-midterm review (no lab, no flag)
│   ├── week10-hybrid-encryption/  ← CONCEPTUAL — Audit-the-AI (no Docker target)
│   ├── week11-signatures-zkp/     ← HYBRID — ECDSA signature-malleability double-spend
│   ├── week12-secure-transport/   ← HYBRID — cert-validation-bypass MITM
│   ├── week13-e2e-encryption/     ← HYBRID — TLS-only vs. E2E chat server (server-log evidence)
│   ├── week14-authentication/     ← HYBRID — plaintext-password vs. challenge-response demo
│   ├── week15-pqc/                ← LAB — Lamport OTS key-reuse private-key recovery
│   └── week17-review/             ← pre-final review (no lab, no flag)
├── quizzes/weekly/
├── slides/
├── project/
└── instructor/                 ← git-ignored, private repo — answer keys, flags, research data
```

## Relationship to `software-security`

- Same 19-week skeleton (12 teaching + 1 capstone + 2 review + 2×2 exam), same AIR-Sec assessment taxonomy
  (Audit-the-AI, EiPE, Prompt Problem, viva, per-student attributable artifacts).
- **Separate** `seed_flags.py` / CHALLENGES namespace, separate CTFd deployment, separate
  `RESEARCH_SALT` and pseudonymization run — no shared identifiers between the two courses'
  research data.
- Has its own [`ETHICS.md`](ETHICS.md) (adapted from `software-security`'s policy, not a shared
  file — this course has its own repo, Docker sandbox, and Classroom instance).
- Has its own [`SUBMISSION.md`](SUBMISSION.md), adapted from `software-security`'s pattern for
  this course's own Classroom/GitHub instances. Reuses `software-security`'s pseudonymization
  tooling (`instructor/pseudonymize.py`) by reference/copy rather than reinventing it — not yet
  copied over (tracked in `course-plan-19weeks.md`'s open decisions).
- Content source: a prior (pre-AIR-Sec) offering of this course at KOSEN68. See
  course-plan-19weeks.md's "Reuse & provenance" section for exactly what was and wasn't ported.
