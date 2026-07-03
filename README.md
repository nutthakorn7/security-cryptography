# Security & Cryptography

A hands-on undergraduate course on applied cryptography: how cryptographic primitives fail when
misused, and how to use them correctly. Companion course to
[`software-security`](../KOSEN69%20-%20software-security/) — same 19-week skeleton, same
AIR-Sec pedagogy, same preregistered study, different subject matter and a separate repo/CTFd
deployment.

> ⚠️ **Status: DRAFT.** 12 of 13 teaching weeks are built (Weeks 1–6, 10–15 — Labs, Hybrids, and
> Conceptual weeks; see [course-plan-19weeks.md](course-plan-19weeks.md) for which is which),
> plus both review weeks (7, 17) and both exam blocks (8–9, 18–19). Remaining: Week 16 (capstone
> studio — covered by `project/README.md`, no separate lab dir by design) and this course's own
> `seed_flags.py` + CTFd wiring — the labs are Docker-verified standalone but not yet live in a
> CTFd deployment. Do not use this for a live course yet.

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

See [course-plan-19weeks.md](course-plan-19weeks.md) for the full 13-topic mapping, including
which weeks are runnable labs vs. conceptual-only, and current build/verification status for
each.

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

- Same 19-week skeleton (13 teaching + 2 review + 2×2 exam), same AIR-Sec assessment taxonomy
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
