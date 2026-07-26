# Course Specification — Security & Cryptography

Outcome-based (OBE) course specification: what students are expected to be able to do (CLOs), how
they are taught, and how each outcome is evidenced and graded. Written to satisfy the usual
programme-review asks (AUN-QA criteria 1–5; the fields a TQF/มคอ.3-style form expects) without
being tied to one institutional template — sections can be lifted into whichever form the faculty
issues.

> **Fill before submission.** Fields marked ⬚ are institution-specific and are not recorded
> anywhere in this repository: course code, semester/academic year, section, room, grading scale,
> and the programme's own PLO list.

---

## 1. Course identification

| Field | Value |
|---|---|
| Course title | Security & Cryptography |
| Course code | ⬚ |
| Credits | 3 (2 lecture hours + 3 laboratory hours per week, 19 weeks) |
| Level | Undergraduate |
| Delivery | On-site lecture + hands-on laboratory; all targets run locally in Docker |
| Instructor | Nutthakorn Chalaemwongwan |
| Semester / Year | ⬚ |
| Programme | ⬚ |

## 2. Course description

Cryptography as it fails in practice. Rather than deriving primitives and stopping there, each
week pairs the mathematics with the specific way real systems misuse it: unsalted password hashes,
authentication built on a bare hash instead of a MAC, encryption without authentication, an
unauthenticated key exchange, a padding oracle, a reused nonce, a malleable signature, a
certificate nobody validates, a one-time signature key used twice.

Weeks are classified by what the topic honestly supports:

| Kind | Meaning |
|---|---|
| **LAB** | a runnable vulnerable/fixed pair exists — Docker target + attributable flag |
| **HYBRID** | a smaller demonstrable exploit alongside material that stays theoretical |
| **CONCEPTUAL** | protocol-design or mathematical analysis with no natural exploit — no lab, no flag, rubric-graded |

The classification is deliberate: a CONCEPTUAL week is not a week with a missing lab, and it is
graded as analysis rather than being forced into a capture-the-flag wrapper.

Every teaching week additionally carries **both** an AIR-Sec assessment and a Conventional
(essay/discussion) assessment, per the preregistered crossover design — see
[course-plan-19weeks.md](../course-plan-19weeks.md) for the dual-arm requirement.

## 3. Course learning outcomes (CLOs)

| # | Outcome | Bloom |
|---|---|---|
| **CLO1** | **Select and justify** the primitive that matches a stated security goal — confidentiality, integrity, authenticity, freshness — and state precisely what that primitive does *not* provide. | Analyse / Evaluate |
| **CLO2** | **Break** a misused construction in a controlled lab — unsalted hashes, hash-only authentication tokens, unauthenticated block-cipher modes, an unauthenticated key exchange, a padding oracle, a reused nonce, a malleable signature, a reused one-time key — and explain the mathematics that makes the break work. | Apply / Analyse |
| **CLO3** | **Rebuild** the construction correctly (KDF, HMAC / encrypt-then-MAC, AEAD, authenticated key exchange, validated certificates) and demonstrate empirically that the original attack now fails. | Create / Evaluate |
| **CLO4** | **Reason about protocol-level designs** — TLS and Noise, end-to-end messaging, PAKE/FIDO2 authentication, post-quantum migration — in terms of trust model, forward secrecy, downgrade resistance and the cost of a compromise. | Analyse / Evaluate |
| **CLO5** | **Evaluate** cryptographic claims and code produced by others, including AI-generated implementations and marketing "snake oil", and explain a finding to both a technical and a non-technical audience. | Evaluate |
| **CLO6** | **Practise** cryptanalytic work within legal and ethical limits, and produce evidence of their own work that withstands scrutiny. | Apply / Value |

## 4. CLO → assessment alignment

Weights follow [syllabus.md](../syllabus.md) §3 and are kept aligned with the *Software Security*
course, since both share one preregistered study design.

| Assessment | Weight | Mode | CLO1 | CLO2 | CLO3 | CLO4 | CLO5 | CLO6 |
|---|---|---|:--:|:--:|:--:|:--:|:--:|:--:|
| Weekly lab worksheets — 12 graded (Wk 1–6, 10–15) | 30% | Individual | ● | ● | ● | ● | ● | ● |
| Midterm — W8 written + W9 practical | 20% | Individual | ● | ● | ● | ● | | ● |
| Final — W18 written (individual) + W19 practical (team) | 25% | Mixed | ● | ● | ● | ● | ● | ● |
| Term project — CryptoVault (compose KDF + AEAD + key exchange + signatures + TLS correctly) | 15% | Team of 2–3 | ● | | ● | ● | ● | ● |
| Weekly quizzes (drop lowest 1–2) + participation | 10% | Individual | ● | ● | | ● | | |

Recurring worksheet parts and the outcome each carries:

| Worksheet part | Assesses |
|---|---|
| Exploit / demonstration task (LAB, HYBRID) | CLO2 |
| Rebuild-it-correctly task | CLO3 |
| Conceptual analysis (CONCEPTUAL weeks, and the theoretical half of HYBRID weeks) | CLO1, CLO4 |
| **Audit the AI** — find the planted flaw in an AI-generated implementation or claim | CLO5 |
| **Explain-in-Plain-English + Prompt Problem** | CLO5 |
| **Evidence & Integrity** — identity-stamped proof, per-student flags where the week has one | CLO6 |

## 5. CLO → PLO mapping

⬚ Replace `PLO1…PLOn` with the programme's own outcome statements. **I** = Introduced,
**R** = Reinforced, **M** = Mastered.

| CLO | ⬚ PLO1 | ⬚ PLO2 | ⬚ PLO3 | ⬚ PLO4 | ⬚ PLO5 |
|---|:--:|:--:|:--:|:--:|:--:|
| CLO1 Primitive selection | M | R | | | |
| CLO2 Cryptanalysis in the lab | M | R | | | |
| CLO3 Correct reconstruction | M | M | | R | |
| CLO4 Protocol reasoning | R | M | I | | |
| CLO5 Evaluation & communication | | | M | | R |
| CLO6 Ethics & evidence | | | R | | M |

## 6. Weekly schedule

5 contact hours per week (2 lecture + 3 lab). Signature games are the week's headline exercise.

| Wk | Topic | Kind | Lab folder | Signature game | CLOs |
|---:|---|---|---|---|---|
| 1 | Intro + threat-modelling a crypto system | CONCEPTUAL | `labs/week01-intro` | 🐍 "Snake Oil Bingo" | 1, 5 |
| 2 | Hash functions | LAB | `labs/week02-hash` | 🔓 "Crack the Leaked DB" | 1, 2, 3 |
| 3 | MACs | LAB | `labs/week03-macs` | 🍪 "Forge the Admin Cookie" | 1, 2, 3 |
| 4 | AES and block-cipher modes | LAB | `labs/week04-aes-modes` | 🎯 "Flip Your Way to Admin" | 1, 2, 3 |
| 5 | Key exchanges | HYBRID | `labs/week05-key-exchanges` | 🕵️ "The Silent Third Wheel" | 2, 3, 4 |
| 6 | Authenticated encryption (AEAD) | LAB | `labs/week06-aead` | 🔮 "Read the Secret Without the Key" | 1, 2, 3 |
| 7 | **Reflection & review** (pre-midterm) | — | `labs/week07-review` | 🏆 Jeopardy recap (Wk 1–6) | 1–4 |
| 8 | **Midterm — written** | — | ⬚ (instructor-held paper) | — | 1–4, 6 |
| 9 | **Midterm — practical** | — | ⬚ (instructor-held) | — | 2, 3, 6 |
| 10 | Asymmetric & hybrid encryption | CONCEPTUAL | `labs/week10-hybrid-encryption` | 🔬 "Nonce Detective" | 1, 4, 5 |
| 11 | Signatures & zero-knowledge proofs | HYBRID | `labs/week11-signatures-zkp` | 💰 "Double-Spend the Bank" | 2, 3, 4 |
| 12 | Secure transport (TLS & Noise) | HYBRID | `labs/week12-secure-transport` | 🎭 "The Impostor's Certificate" | 2, 3, 4 |
| 13 | End-to-end encryption | HYBRID | `labs/week13-e2e-encryption` | 👀 "Who's Reading Your Mail?" | 3, 4 |
| 14 | User authentication | HYBRID | `labs/week14-authentication` | 🗝️ "Never Say the Password" | 1, 4 |
| 15 | Post-quantum cryptography | LAB | `labs/week15-pqc` | 🔑 "Forge the Admin Signature" | 2, 3, 4 |
| 16 | Capstone studio — CryptoVault | — | `project/` | 🏗️ CryptoVault build | 1, 3, 4, 5 |
| 17 | **Reflection & review** (pre-final) | — | `labs/week17-review` | 🏆 Jeopardy: Champions Edition (Wk 10–16) | 1–5 |
| 18 | **Final — written** (cumulative, emphasis Wk 10–16) | — | ⬚ (instructor-held paper) | — | 1–5 |
| 19 | **Final — practical** (team) | — | ⬚ (instructor-held) | — | 2, 3, 5, 6 |

Week 12 is the one week in which students **write the fix themselves** (a stubbed
`build_client_context()` in `alice_student.py`) rather than confirm a supplied one — see
[SUBMISSION.md](../SUBMISSION.md)'s coding-scope note.

Cryptocurrency content (UTXO, BFT, Merkle proofs) has no teaching week; it is examined from the
Week 18 written item bank, matching how the source course treated it.

## 7. Teaching and learning methods

- **Break-then-rebuild laboratories** on LAB and HYBRID weeks; rubric-graded analysis on
  CONCEPTUAL weeks, where forcing a lab would misrepresent the topic.
- **Retrieval practice** — a ~10-minute quiz opens each teaching week (lowest 1–2 dropped); two
  cumulative review quizzes run in Weeks 7 and 17.
- **AI-resilient tasks** — *Audit the AI*, *Explain-in-Plain-English*, *Prompt Problem*. In this
  course the AI critique is often the headline exercise (Weeks 1 and 10), because plausible-sounding
  cryptographic nonsense is exactly what students must learn to detect.
- **Live accountability** — rotating micro-demos and viva spot-checks on submitted work.
- **Per-student evidence** — flags are minted per student on LAB/HYBRID weeks; CONCEPTUAL weeks
  use per-student planted-error variants instead.

## 8. Assessment criteria and grading

Individual work is ~75% of the final mark. Team-graded work is bounded: the CryptoVault project
(15%) and the Week 19 practical, with project marks scaled by peer-contribution evaluation.
Worksheets are graded against the rubric published in each worksheet. Grading scale: ⬚.

## 9. Verification of student achievement

- Each graded worksheet has an instructor-held answer key, reviewed against the published worksheet
  whenever lab content changes.
- Written exams exist in parallel Form A/B drawn from a maintained item bank.
- Viva spot-checks and micro-demos sample submitted work each week.
- Where a week issues flags, values are per-student, so duplicate submissions are detectable.
- End-of-term attainment is reviewed by mapping assessment scores back to §4.

## 10. Resources

- Course repository: labs, worksheets, slides and runnable targets.
- Docker Desktop on the student's own machine; no cloud account required.
- Reading list: [readings.md](../readings.md) · Submission channels: [SUBMISSION.md](../SUBMISSION.md)
- Rules of engagement: [ETHICS.md](../ETHICS.md)
- Note: `labs/week11-signatures-zkp` depends on the `ecdsa` package, which carries an unfixable
  advisory (CVE-2024-23342, side channels declared out of scope upstream). It is used deliberately
  — its pure-Python implementation is what makes the nonce/malleability demonstrations legible —
  and is documented as an accepted risk in that lab's `requirements.txt`.

## 11. Academic integrity and AI policy

AI assistants are permitted and are addressed head-on by the *Audit the AI*, *EiPE* and *Prompt
Problem* tasks. What is assessed is the student's own understanding; per-student flags and
variants, identity-stamped evidence, viva spot-checks and micro-demos exist to keep that
assessable. Submitting an implementation or a proof a student cannot explain or reproduce is an
academic-integrity matter under ⬚ (institutional policy).

---

*Weekly lesson plans that instantiate this specification: [`docs/lesson-plans/`](lesson-plans/).*
