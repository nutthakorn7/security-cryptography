# Cryptography and Network Security — 20-Week Course Plan (KOSEN69)

**02005104 · Year 4 · 1 credit · Semester 2 AY2026 · Lecture · 100 minutes per week.**
Approved teaching and assessment policy, updated 2026-10-30. The legacy filename
`course-plan-19weeks.md` is retained to preserve existing links. See [syllabus.md](syllabus.md),
[SUBMISSION.md](SUBMISSION.md), and each week's full worksheet for the tasks and submission details.

## Practical teaching and the two worksheet formats

Every teaching week (W1–6, W10–15) includes a shared practical core. LAB and HYBRID weeks
use the runnable demonstrations; CONCEPTUAL W1/W10 use cases, diagrams, experiments and code
analysis without requiring a Docker target or flag. Classification describes the activity,
not a different entitlement to practical marks.

| Component | Conventional | AIR-Sec |
|---|---:|---:|
| Main task and observations | 20 | 20 |
| Controls, tests and limitations | 20 | 20 |
| Reproducible evidence and reasoning | 20 | 20 |
| Ordinary written questions | 40 | — |
| Audit-the-AI | — | 20 |
| Explain-in-Plain-English | — | 10 |
| Prompt Problem | — | 10 |
| Total | 100 | 100 |

Students complete the common 60 plus the assigned format's 40, not both 40-point sections.
All original questions remain in the worksheets; preparation and extension questions are labelled
so the core practical task fits the class. Viva is formative/verification within the relevant
rubric, with no extra score or automatic fail gate. A shared placeholder flag is not proof of
personal attribution; commands/results and the student's explanation are required in both formats.

Normal 100-minute class: quiz/review 10 + brief 10 + practical 60 + debrief 15 + capture/exit 5.
Prepare dependencies/images before class where directed, and finish the selected written section
before the next class. W11 and W15 reserve 70 minutes for their larger practical cores:
quiz 10 + brief 10 + practical 70 + capture/exit 10. W11 obtains a fresh signature during class;
key-dependent captures made before a container restart cannot be reused.

## Week-by-week plan

| Week | Topic and practical core | Kind / class use |
|---|---|---|
| 1 | Intro and crypto threat modelling: in-class environment check; assets, trust boundaries, misuse cases and controls; quoted AI exhibit as the AIR-Sec audit; whole-class Snake Oil Bingo, whose claims AIR-Sec groups analyse | Conceptual; 100 minutes |
| 2 | Hashes: crack the unsalted MD5 demo data, contrast bcrypt cost and verify legitimate login | Lab; 100 minutes |
| 3 | MACs: forge `SHA256(secret || message)` by length extension, then test rejection by HMAC-SHA256 | Lab; 100 minutes |
| 4 | AES modes: CBC bit-flip from guest to admin; GCM detects tampering; project team formed, design plan reviewed in class and submitted | Lab; 100 minutes |
| 5 | Key exchange: MITM unauthenticated DH versus a pre-shared-key HMAC-authenticated exchange; subgroup analysis | Hybrid; 100 minutes |
| 6 | AEAD: recover CBC-without-MAC plaintext via padding oracle; compare the uniform GCM rejection control | Lab; 100 minutes |
| 7 | Review W1–6 and cumulative quiz; project KDF/AEAD checkpoint | Review; 100 minutes |
| 8 | Midterm written, W1–6 | 90-minute paper + 10-minute administration; 8 course points |
| 9 | Individual midterm practical, W1–6 | 80-minute practical + 20-minute brief/submission; 12 course points |
| 10 | Hybrid encryption: reproduce GCM nonce-reuse leakage in a supplied code case, correct and explain the design | Conceptual; 100 minutes |
| 11 | ECDSA signature malleability: fresh signature 10, twin 15, vulnerable POST 15, fixed positive/negative tests 15, reasoning 15 minutes; ZKP theory prepared/extended outside core; feedback on the project sharing-flow draft | Hybrid; 70-minute practical within 100 |
| 12 | TLS: intercept the unverified client; every student implements and tests `build_client_context()` with trusted CA and hostname validation | Hybrid; 100 minutes; W12 code link required for both formats |
| 13 | E2E: server-visible plaintext versus client encryption, successful recipient decryption, trust/key-distribution caveats | Hybrid; 100 minutes |
| 14 | Authentication: password transmission versus a toy challenge-response; distinguish the toy from PAKE/OPAQUE guarantees; project transport-security and self-audit review | Hybrid; 100 minutes |
| 15 | PQC/Lamport OTS: collect 15, recover/forge 25, control 20, reasoning 10 minutes; HNDL optional | Lab; 70-minute practical within 100 |
| 16 | CryptoVault studio: integration and testing; every team demonstrates its sharing flow at peer review; existing practice practical challenges check understanding; project clarification | Project; 100 minutes |
| 17 | Review W10–16 and cumulative quiz; prepare for final | Review; 100 minutes |
| 18 | Final written: cumulative with emphasis W10–16 | 90-minute paper + 10-minute administration; 10 course points |
| 19 | Team final practical; project video at most 5 minutes submitted beforehand | 80-minute practical + 20-minute brief/submission; 15 course points; no live project Q&A in this exam |
| 20 | Return exams, explain controls, course reflection and remaining project clarification | Feedback; 100 minutes; no extra graded worksheet |

W12 is the only standalone code-fix commit submission. Code corrections/proofs for the W10
analysis are retained in the worksheet PDF/attachments. Full references and question sets remain
available; cryptocurrency items from an older course are unscored reference material, since
there is no dedicated teaching coverage in this schedule.

## Assessment and teams

| Assessment | Course points |
|---|---:|
| Twelve worksheets, 2.5 each | 30 |
| Midterm written / practical | 8 / 12 |
| Final written / practical | 10 / 15 |
| CryptoVault project | 15 |
| Quiz / participation | 10 |
| Total | 100 |

The syllabus ability matrix remains Basic 20 / Technical 70 / Interdisciplinary 10. Midterm's
Basic 10 / Technical 10 are distributed written 4/4 and practical 6/6 (each paper uses raw Basic/Technical 50/50). Final's Basic 5 /
Technical 20 are distributed written 5/5 and practical 0/15. This keeps exam component totals
and the approved ability totals consistent.

Use teams of 3, with teams of 2 where needed to fit the class; the actual enrolment is not
assumed. CryptoVault milestones: W4 design/team, W7 KDF+AEAD, W11 sharing, W14 transport/self-audit,
W16 studio, video/report/code before W19, clarification in W16/W20. Final practical is team work;
midterm practical and written exams are individual. See the project rubric for contribution
scaling. The existing optional crypto-agility +5 bonus is capped at raw 100; HNDL adds no new
mandatory work or additional course-weight category.

## Technical boundaries to explain accurately

- HMAC is not broken by the secret-prefix MAC length-extension attack. Resuming an outer hash
  from its digest does not produce a valid HMAC for the fixed-format keyed construction.
- A 64-bit tag's random forgery probability and birthday collision bound describe different events.
- CBC without a MAC is the runnable padding-oracle target; MtE/E&M are comparison concepts,
  not separate implemented constructions in W6.
- DH needs peer authentication and group validation; primality of p alone does not eliminate
  small subgroups, and an HMAC key derived only from unauthenticated DH does not authenticate peers.
- XTS uses a position-dependent tweak; equal plaintext in different sectors is not the same
  equality case as repeated writes to the same location with the same key/tweak.
- W11 demonstrates ECDSA malleability, not recovery of a private key by nonce reuse. Low-S
  selects one representative of the `(r,s)` / `(r,n-s)` pair, not a unique signature for every
  message/key; replay protection still needs application-level transaction identity/state.
- The W14 toy does not transmit the password directly, but permits offline guessing from a
  transcript and is not a full PAKE. OPAQUE cannot prevent guessing after complete compromise
  of the server's credential data and keys; key stretching raises cost, and precomputation
  resistance is a different property.
- W15 Lamport key reuse is distinct from breaking a standardized post-quantum scheme. HNDL's
  tiny-RSA companion illustrates a later classical-KEM break; it does not run Shor's algorithm.

## Reuse and delivery status

Questions/concepts from the prior KOSEN68 offering are retained/adapted where relevant. Current
course identity and policy supersede old codes, essay-only control arms and longer exam timings.
The previous planning narrative is retained privately as historical reference, not current
instructions or evidence of external research registration. Any live deployment, cohort flag
issuance or research consent must be checked separately; local source changes alone do not publish
them. Authorized-use policy: [ETHICS.md](ETHICS.md).
