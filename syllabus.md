# Security & Cryptography — Course Syllabus & Outline

**Level:** Undergraduate (3rd / 4th year)
**Credits:** 3 (2 lecture hours + 3 lab hours per week) — matches `software-security`'s format
**Prerequisites:** Programming (Python/C), Data Structures, basic Discrete Math/Number Theory
**Format:** Lecture + weekly hands-on lab
**Course code:** `21025117` — the code used in last year's exam and Google Form delivery (the
earlier `02005104` was only the generic-template xlsx's filename; see `course-plan-19weeks.md`
Decisions #1 for the tiebreaker). Confirm against the registrar before print if in doubt.
**Status:** DRAFT — see [course-plan-19weeks.md](course-plan-19weeks.md) for what's built vs. scoped.

---

## 1. Course Description

This course teaches how cryptographic primitives are supposed to work, how they fail when
misused in real systems, and how to use them correctly. It pairs each concept with a lab in which
students either exploit a deliberately misused primitive (forge a MAC, MITM an unauthenticated
key exchange, recover plaintext from a reused GCM nonce) or defend/build a correct implementation
— the same break/defend rhythm as `software-security`, applied to hashes, MACs, symmetric and
asymmetric encryption, signatures, transport security, and authentication.

Not every topic in cryptography has a natural "break it" lab — protocol-design and mathematical
content (zero-knowledge proofs, post-quantum lattice constructions, BFT consensus) stays
conceptual, assessed through AI-resilient analysis tasks (Audit-the-AI, Explain-in-Plain-English,
Prompt Problem) rather than a forced CTF wrapper. See `course-plan-19weeks.md`'s week
classification for which weeks are which.

## 2. Learning Outcomes

By the end of the course, students will be able to:

1. **Distinguish** hashing, MACs, symmetric encryption, and asymmetric encryption, and select the
   correct primitive for a given confidentiality/integrity/authenticity requirement.
2. **Identify and exploit** common cryptographic misuse (ECB/ CBC/ ECB pattern leakage, nonce
   reuse, unauthenticated key exchange, non-constant-time comparison, weak hashing) in a
   controlled environment.
3. **Implement primitives correctly**, using vetted libraries and modes (AEAD, salted KDFs,
   authenticated key exchange) rather than ad hoc constructions.
4. **Reason about protocol security** — TLS/Noise handshakes, PKI trust models, digital
   signatures, zero-knowledge proofs — at the level of "what breaks if this step is skipped,"
   even where no runnable exploit is assigned.
5. **Evaluate AI-generated cryptographic code and explanations** for subtle correctness bugs
   (nonce reuse, missing authentication, wrong mode) that a plausible-looking answer can hide.
6. **Communicate cryptographic risk** to both technical and non-technical audiences.

## 3. Assessment

Same weighting structure as `software-security` (both courses share one preregistered study
design, so component weights are kept aligned):

| Component | Weight | Graded |
|---|---|---|
| Weekly lab worksheets — 12 graded (Weeks 1–6, 10–15) | 30% | **Individual** |
| Midterm — Week 8 (written) + Week 9 (CTF practical) | 20% | **Individual** |
| Final — Week 18 written *(individual)* + Week 19 capstone CTF *(team)* | 25% | Mixed |
| Term project — CryptoVault (see `project/README.md`) | 15% | **Team of 2–3** |
| Weekly quizzes (drop lowest 1–2) + participation / **Houses** leaderboard | 10% | Individual + Houses |

> **Individual vs team.** Your grade is dominated by **individual mastery** (worksheets,
> quizzes, exams ≈ 75%). **Team** work is bounded (project 15% + the Week 19 capstone CTF).

### Assessment taxonomy (AIR-Sec)

Every teaching week carries **both** an AIR-Sec assessment and a Conventional (essay/discussion)
assessment, per the preregistered crossover design — see `course-plan-19weeks.md`'s "dual-arm
requirement" section for why this is non-negotiable rather than a nice-to-have. In brief, per
week:

- **Conventional arm** — essay/discussion questions (ported from the prior offering of this
  course where available, written fresh otherwise), no AI-resilience layer.
- **AIR-Sec arm** — the same concept delivered through a personalized/attributable artifact (a
  flag, a seeded bug instance, or a per-student parameter) plus Audit-the-AI / EiPE / Prompt
  Problem as fits the content, and viva spot-checks.

**Late submissions.** Same policy as `software-security`: −10% of that item's score per day late,
up to 3 days; not accepted after day 3 without an approved extension. Weekly/in-class quizzes have
no late window (an absence is covered by the drop-lowest-1–2 rule instead). Documented emergencies
get a case-by-case extension at the instructor's discretion.

## 4. Structure

Same skeleton as `software-security`: **13 teaching weeks (1–6, 10–16), 2 review weeks (7, 17),
2 exam blocks (8–9 midterm, 18–19 final)**. Full week-by-week table:
[course-plan-19weeks.md](course-plan-19weeks.md).

## 5. References

- Boneh & Shoup, *A Graduate Course in Applied Cryptography* (free online) — primary theory
  reference for MACs/signatures/ZKP weeks.
- OWASP Cryptographic Storage Cheat Sheet, OWASP Transport Layer Protection Cheat Sheet.
- NIST SP 800-38D (GCM), SP 800-56A (key establishment), FIPS 205 (SLH-DSA/PQC signatures).
