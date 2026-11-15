# Lesson Plan — Week 13: End-to-end encryption

**02005104 · Cryptography and Network Security · Year 4 · Semester 2 AY2026 · Lecture**
**Contact time: 100 minutes.** Kind: Docker lab (guided, local containers).
Lab/analysis: [`labs/week13-e2e-encryption`](../../labs/week13-e2e-encryption/README.md) · slides: `slides/week13.md`.

## Objectives and preparation

Demonstrate the boundary between transport encryption and endpoint encryption and state the remaining trust assumptions.

Students run the compose stacks with `up -d --build` and `logs server` / `logs bob` (worksheet steps 2 and 5) and one `grep` over `alice.py` (step 7); no code is written. Switching between the two stacks without a `down` works. Logs are evidence; there is no required flag.

Images, dependencies and long readings are preparation; confirm the environment before class.
Only
authorized local targets/test data are used. An unavailable environment is handled with a
prepared trace/code example and documented follow-up, not a fabricated successful result.

## In-class run sheet

| Minutes | Activity |
|---|---|
| 0–10 | Week 12 retrieval quiz/review; recall previously taught TLS certificate validation. |
| 10–20 | Brief the mechanism, safety scope and expected evidence. |
| 20–40 | A1: run the TLS-only mode, record `SERVER SAW: meet at pier 39 at midnight` and `BOB RECEIVED`. |
| 40–60 | A2: run the client-side encryption mode; record the unreadable `SERVER SAW:` line (first 60 characters) and `BOB DECRYPTED`. |
| 60–80 | A3: find the two `payload = ` lines in `alice.py`, explain why the lab does not prove the relayed key is Bob's, and how safety numbers help. |
| 80–95 | Compare results/control, explain the mechanism and limits, receive feedback; begin the assigned form. |
| 95–100 | Save evidence and submit the in-class checkpoint. |

**Core artifact:** the readable and the unreadable `SERVER SAW:` lines, Bob's decrypted line, the two differing code lines and the named limit.

## Assessment and after-class work

Worksheet 13 is **100 raw points → 2.5 course points**, one of 12 equally weighted worksheets:

| Part | Conventional | AIR-Sec |
|---|---:|---:|
| A1 the server reads, HTTPS only (steps 2–3) | 20 | 20 |
| A2 E2EE, the server cannot read (steps 5–6) | 20 | 20 |
| A3 the differing lines and the limit (steps 7–10) | 20 | 20 |
| Conventional technical written questions | 40 | — |
| Audit-the-AI | — | 20 |
| Explain-in-Plain-English | — | 10 |
| Prompt Problem | — | 10 |
| **Total** | **100** | **100** |

Everyone completes shared 60; finish only the assigned form's 40. Conventional Q1–Q4 are lab-tied; PGP failure, open E2EE problems and Double Ratchet stay optional. Signal's historical X3DH, later PQXDH, ratchets and PGP key-management questions stay as extended analysis. Do not claim this small demo implements Signal, verified key distribution or forward secrecy.

Administer the scored Week 13 quiz at the start of Week 14, after this topic is taught; the Week 13 opening checks Week 12. The quiz remains inside the course's 10% quiz/participation component. Reproduction checks and
short explanations are feedback/authenticity checks within work, with no extra viva score or
automatic AIR-only gate. Use name/ID and cite tools/sources equally in both forms. Flags are
accepted only where the target provides them; a personal flag is required only if configured
and issued, never assumed from a shared default.

## Instructor checks and reflection

- Check that the vulnerable/control experiment produces distinct, interpretable results before class.
- Check evidence, code and explanations together; an output string alone is not full understanding.
- Keep all further-reading questions available; do not turn extension work into an unannounced requirement.
- Record attendance, time actually taken, environment failures, misconceptions and corrections after teaching.
- This 100 minute allocation is a plan; do not claim a human timing pilot has been completed.

See [agenda](../../AGENDA.md), [assessment policy](../../syllabus.md) and [submission rules](../../SUBMISSION.md).
