# Security & Cryptography

**02005104 Cryptography and Network Security** — Year 4, 1 credit, Semester 2 AY2026.
Lecture format with practical work in class: **20 weeks × 100 minutes**. The 12 teaching
worksheets are W1–6 and W10–15; ten have runnable labs and W1/W10 use case/code analysis.
W16 is the CryptoVault studio, W7/W17 are review, W8/W9/W18/W19 are exams, and W20 is feedback.

Both worksheet formats share **practical work 60/100**. The remaining **40/100** is either
Conventional written questions or AIR-Sec (Audit-the-AI 20, Explain-in-Plain-English 10,
Prompt Problem 10). Each worksheet contributes **2.5 course points**, for 30 in total.
See [syllabus.md](syllabus.md) and [SUBMISSION.md](SUBMISSION.md) for the current assessment policy.
These local materials do not establish the deployment or personalized-flag status of a live cohort.

> ⚠️ **Ethics first.** All offensive techniques are taught for **defensive and authorized testing
> only**. Attack only the provided sandbox targets. See [`ETHICS.md`](ETHICS.md) for this
> course's authorized-use policy.

---

## Quick start

[คู่มือ Lab Cryptography ทั้ง 10 สัปดาห์และการส่งงาน](SUBMISSION.md) — คำสั่งรัน ผลที่ต้องตรวจ และรายการหลักฐานส่งงานสำหรับนักศึกษา

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
| **18–19** | **📝 Final** (Wk18 written · Wk19 team practical; 100 minutes each) | — |
| **20** | **Feedback, reflection and project clarification** | Return results and discuss controls |

Full details and the current 20-week schedule: [course-plan-19weeks.md](course-plan-19weeks.md).
The filename is retained for existing links; the plan inside covers 20 weeks.

## Repository layout

```
security-cryptography/
├── README.md                  ← you are here
├── course-plan-19weeks.md     ← current 20-week plan (legacy filename retained)
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
│   ├── week17-review/             ← pre-final review (no lab, no flag)
│   └── week20-feedback/           ← feedback/reflection (no additional graded lab)
├── quizzes/weekly/
├── slides/
├── project/
└── instructor/                 ← git-ignored, private repo — answer keys, flags, research data
```

## Relationship to `software-security`

The courses share the Conventional/AIR-Sec teaching approach, while keeping their own topics,
repositories and grades. Both Cryptography worksheet formats include the same practical core;
viva checks verify understanding within the existing rubric and add no separate marks or pass gate.
Cryptography uses its own [ETHICS.md](ETHICS.md), sandbox targets and [SUBMISSION.md](SUBMISSION.md).
Current course delivery uses the course platform and the student's GitHub fork for the W12 fix.
Any separate research protocol, consent or external registration must be verified independently;
this teaching plan does not claim a registered study or a live CTFd deployment.

Some conceptual questions were adapted from a prior KOSEN68 offering. The current course code,
credits, 20-week timetable and grading are those confirmed for AY2026 in the current syllabus.
