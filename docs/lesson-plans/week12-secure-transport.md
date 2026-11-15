# Lesson Plan — Week 12: Secure transport: TLS and Noise

**02005104 · Cryptography and Network Security · Year 4 · Semester 2 AY2026 · Lecture**
**Contact time: 100 minutes.** Kind: Docker lab (guided, local containers).
Lab/analysis: [`labs/week12-secure-transport`](../../labs/week12-secure-transport/README.md) · slides: `slides/week12.md`.

## Objectives and preparation

Implement and test certificate-chain and hostname validation without silently disabling either check.

Code writing and tests belong to common practical 60 in both forms. The student edit is three lines in `alice_student.py`; the worksheet shows the correct lines from `alice.py` first (guided edit) and the student must explain them and test both the impostor and the real Bob. Prebuild images before class (`docker compose -f docker-compose.vulnerable.yml build`). The required GitHub fork and commit link has no marks of its own.

Images, dependencies and long readings are preparation; confirm the environment before class.
Students run the compose files with `run --rm alice` in worksheet steps 2, 5 and 9; no manual certificate work is asked. Only
authorized local targets/test data are used. An unavailable environment is handled with a
prepared trace/code example and documented follow-up, not a fabricated successful result.

## In-class run sheet

| Minutes | Activity |
|---|---|
| 0–10 | Retrieval quiz/review (Week 1: baseline diagnostic); recall previously taught material. |
| 10–20 | Brief the mechanism, safety scope and expected evidence. |
| 20–35 | A1: run the vulnerable Alice, record `TLS handshake succeeded WITHOUT verifying` and Eve's `MITM INTERCEPTED` line. |
| 35–50 | A2: run the fixed Alice (`CERT VERIFICATION FAILED`, `intercepted NOTHING`); A3 step 7: read the correct lines in `alice.py`. |
| 50–80 | A3: every student edits `build_client_context()` in `alice_student.py` (3 lines), runs the impostor test and the trusted-peer test with Bob, and explains why both are needed. |
| 80–95 | Compare results/control, explain the mechanism and limits, receive feedback; begin the assigned form. |
| 95–100 | Save evidence and submit the in-class checkpoint. |

**Core artifact:** the vulnerable and fixed logs, the student-built `build_client_context()`, a rejected impostor and an accepted Bob.

## Assessment and after-class work

Worksheet 12 is **100 raw points → 2.5 course points**, one of 12 equally weighted worksheets:

| Part | Conventional | AIR-Sec |
|---|---:|---:|
| A1 Alice does not check, Eve reads the secret (steps 2–3) | 20 | 20 |
| A2 Alice checks, Eve gets nothing (steps 5–6) | 20 | 20 |
| A3 student fix, two-way test and its limits (steps 7–10) | 20 | 20 |
| Conventional technical written questions | 40 | — |
| Audit-the-AI | — | 20 |
| Explain-in-Plain-English | — | 10 |
| Prompt Problem | — | 10 |
| **Total** | **100** | **100** |

Everyone completes shared 60; finish only the assigned form's 40. Week 12 code/testing belongs in
shared 60. Preserve and complete the full assigned question text outside class as needed:
Conventional Q1–Q4 are lab-tied; SSL history, 0-RTT/replay, Web PKI mitigations and Noise stay as optional extended work; the classroom MITM may fail at issuer trust even when its claimed hostname matches.

The quiz remains inside the course's 10% quiz/participation component. Reproduction checks and
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
