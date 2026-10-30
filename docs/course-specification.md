# Course Specification — Cryptography and Network Security

## Course identification

| Field | Confirmed value |
|---|---|
| Code / title | 02005104 — Cryptography and Network Security |
| Level / credits | Year 4 / 1 credit |
| Semester | Semester 2, Academic Year 2026 (2569) |
| Programme / type | Computer / Compulsory |
| Instructor | Nutthakorn Chalaemwongwan |
| Class format | Lecture, emphasizing in-class laboratory/practical analysis |
| Contact time | 100 minutes weekly over 20 weeks; scheduled total 2,000 minutes |

The approved institutional XLSX retains its original format and full text. Room, section,
calendar dates and any institutional grading-scale rules must come from the official timetable
or policy; none is invented here.

## Description and outcomes

Cryptographic systems are studied through primitive selection, controlled misuse demonstrations,
correct composition and explicit limits. Weeks 1/10 use practical analysis; runnable weeks use
local vulnerable/control pairs. Docker and flags are not universal assessment requirements.

| CLO | Student can |
|---|---|
| 1 | Select a primitive for confidentiality, integrity, authenticity and freshness and justify its limits. |
| 2 | Analyse a misuse and demonstrate a bounded attack with reproducible evidence. |
| 3 | Correctly use a vetted construction and verify rejection of the original attack. |
| 4 | Explain protocol trust, key authentication, compromise limits and PQC migration. |
| 5 | Evaluate technical and AI-generated claims and communicate their reasoning. |
| 6 | Work ethically, document sources/tools and produce their own explainable evidence. |

The owner-approved programme alignment is **C(4), G(1), G(5)**; MCC links follow the actual
weekly topics in the institutional syllabus. No placeholder PLO number is presented as an
institutionally confirmed mapping.

## Teaching and assessment alignment

| Assessment | Weight | Mode | Outcomes |
|---|---:|---|---|
| 12 worksheets, Weeks 1–6/10–15 | 30% | Individual; 2.5 course points each | CLO1–6 |
| Midterm W8 written / W9 practical | 8% / 12% | Individual | CLO1–4,6 |
| Final W18 written / W19 practical | 10% / 15% | Individual / team | CLO1–6 |
| CryptoVault | 15% | Teams 3 normally,2 where needed | CLO1,3–6 |
| Quizzes / participation | 10% | Individual and class participation | CLO1,2,4–6 |
| **Total** | **100%** | | |

Ability matrix remains **Basic 20 / Technical 70 / Interdisciplinary 10**:
Basic = midterm 10 + final 5 + quiz 5; Technical = midterm 10 + final 20 + quiz 5 + lab 25 + project 10;
Interdisciplinary = lab 5 + project 5. Written/practical splits and ability rows refer to the same
marks, not separate totals. Instructor item blueprints allocate the ability points explicitly.

All students complete the same common practical 60: core/observation 20, control or limitations 20,
reproducible evidence/reasoning 20. The assigned form contributes 40: Conventional technical
written questions 40, or AIR-Sec Audit 20 + Explain-in-Plain-English 10 + Prompt Problem 10.
Weeks 1/10 use diagrams, calculations and counterexamples for common 60. Week 12 student-written
`build_client_context()` and its tests are graded in common 60 for both forms. Each worksheet
raw 100 converts to `score/100×2.5`; the other form is not an extra requirement or grade.

Live explanations, feedback and reproduction checks happen within existing work. No extra
viva 10, automatic AIR-only gate or blanket personal-flag prerequisite applies. Personal flags
are used only when actually configured; ordinary name/ID, tool disclosure and integrity rules
apply equally. This current approved teaching policy changes older essay-only Conventional
descriptions; it does not assert that an external study registration has been updated or verified.

## Weekly schedule and learning methods

Ordinary 100 minute classes = quiz/review 10 + brief 10 + practice 60 + feedback/reasoning 15 +
checkpoint 5. Weeks 11/15 instead practice 70 and evidence/feedback 10 after quiz 10 + brief 10.
Week 1 orientation is ungraded; the Week 1 retrieval quiz opens Week 2.
Pre-class preparation covers images, installation and reading; full-form answers and all
extension questions remain available for after-class work. Instructor plans name a bounded core.

| Wk | Topic / activity | Principal evidence |
|---:|---|---|
| 1 | Security mindset / threat modelling | Threat model and primitive-selection diagram |
| 2 | Hashes / password KDFs | Weak-hash recovery, authenticated session and KDF comparison |
| 3 | MACs / length extension | A forged secret-prefix MAC and rejected HMAC control |
| 4 | AES modes / CBC malleability | A same-length CBC field modification and authenticated rejection |
| 5 | Authenticated key exchange | Unauthenticated DH interception and authenticated abort |
| 6 | AEAD / padding oracle | Oracle-dependent plaintext recovery and GCM rejection |
| 7 | Pre-midterm review | Quiz, selected mock and repair notes |
| 8 | Midterm written | 90 minute written script |
| 9 | Midterm individual practical | 80 minute individual checkpoints |
| 10 | Asymmetric / hybrid encryption | A KEM/DEM design, nonce analysis and counterexample |
| 11 | Signatures / ZKP / malleability | A signature twin, repeated authorization and canonicalization control |
| 12 | TLS / Noise / client-context coding | A student-built TLS context with a successful trusted connection and MITM rejection |
| 13 | End-to-end encryption | Server-visible plaintext versus ciphertext, with successful recipient decryption |
| 14 | Authentication / PAKE limits | Password logging versus a fresh challenge/proof exchange |
| 15 | PQC / one-time signatures | A forged toy Lamport signature and rejected second use of a fixed key |
| 16 | CryptoVault studio | Build/self-audit feedback and action list |
| 17 | Pre-final review | Quiz, selected mock and repair notes |
| 18 | Final written | 20 MCQs in 90 writing minutes |
| 19 | Final team practical | 80 minute team station evidence |
| 20 | Feedback / clarification / closure | Returned-work feedback and reflection |


All 20 contact slots are 100 minutes. Written exams use 90 task +10 admin minutes; practicals 80 task
+20 admin. Week 20 uses return 15 + mechanisms/control review 30 + project clarification 30 + reflection 20 + closure 5 minutes. Week 19 contains no project Q&A. Team videos are≤5 minutes and submitted before Week 19;
project clarification uses Weeks 16/20 and the existing rubric. Cryptocurrency/UTXO/BFT legacy
items are retained as a private bank, excluded from the current scored exam. HNDL is optional.

## Criteria and verification

The six approved rubric dimensions are: mechanism selection; attack analysis with evidence;
safe implementation/composition; protocol/PQC reasoning; evaluation of technical claims; and
communication, integrity and teamwork. VeryGood = correct, complete and evidenced; Good =
essential reasoning correct with omissions; Fail = central reasoning incorrect or evidence
insufficient. Apply these within the published component weights and worksheet subcriteria.

Private keys and current exam blueprints are held under `instructor/exams/`; student-facing
guides contain scope/timing without solution payloads. Preflight target freshness, variant
correctness and marking consistency before use. The time budgets are plans, not a completed
human timing trial. Record actual completion times and attainment after teaching. Grade scale
and misconduct handling follow institutional policy; do not invent thresholds here.

## Resources and integrity

Local repositories provide labs, all question text, readings, slides and submission guidance.
Use only authorized targets and course test accounts. Weeks 11/15 require fresh state; Week 11
demonstrates signature malleability, not nonce-reuse key recovery. Week 6 attacks unauthenticated
CBC and compares supplied GCM. Week 14's toy challenge-response is not full PAKE: OPAQUE does
not eliminate offline guessing after server plus credential compromise; see
[RFC 9807 § 10.11](https://www.rfc-editor.org/rfc/rfc9807.html#section-10.11).

AI use requires disclosure and verification. Students are graded on their own explainable work,
not the plausibility of a generated answer. The `ecdsa` side-channel advisory CVE-2024-23342
remains an explicitly accepted teaching-lab dependency risk; do not use the toy bank as a real
financial or authentication service.

See [syllabus](../syllabus.md), [agenda](../AGENDA.md), [lesson plans](lesson-plans/),
[project](../project/README.md), [submission](../SUBMISSION.md) and [ethics](../ETHICS.md).
