# Lesson Plan — Week 10: Asymmetric and hybrid encryption

**02005104 · Cryptography and Network Security · Year 4 · Semester 2 AY2026 · Lecture**
**Contact time: 100 minutes.** Kind: Docker lab (guided, one container).
Lab/analysis: [`labs/week10-hybrid-encryption`](../../labs/week10-hybrid-encryption/README.md) · slides: `slides/week10.md`.

## Objectives and preparation

Trace a hybrid-encryption design, identify a reused-nonce failure and justify authenticated key distribution.

This is a guided lab with a small supplied helper (`demo.py`). There is no personal flag; the evidence is the commands and results from the student's own machine, with the `YES` / `NO` and `RESULT` lines the same for everyone.

Images, dependencies and long readings are preparation; confirm the environment before class.
Students run the supplied helper (`demo.py`) in worksheet steps 2, 5, 7 and 9; no manual XOR is asked. Only
authorized local targets/test data are used. An unavailable environment is handled with a
prepared trace/code example and documented follow-up, not a fabricated successful result.

## In-class run sheet

| Minutes | Activity |
|---|---|
| 0–10 | Retrieval review of Week 5 key exchange and Week 6 AEAD. The Week 10 scored quiz is given at the start of Week 11. |
| 10–20 | Brief the mechanism, safety scope and expected evidence. |
| 20–40 | A1: read who holds which key, run `demo.py good`, record the nonces and `nonces equal? NO`. |
| 40–60 | A2: run `demo.py reuse` and `demo.py attack reuse`; Eve reads message 2 without the key. |
| 60–80 | A3: run `demo.py attack good`, compare the two nonce lines in the code, explain why a repeated nonce is dangerous. |
| 80–95 | Compare results/control, explain the mechanism and limits, receive feedback; begin the assigned form. |
| 95–100 | Save evidence and submit the in-class checkpoint. |

**Core artifact:** the `good` and `reuse` outputs, Eve's reading in both cases, and the two nonce lines of code.

## Assessment and after-class work

Worksheet 10 is **100 raw points → 2.5 course points**, one of 12 equally weighted worksheets:

| Part | Conventional | AIR-Sec |
|---|---:|---:|
| A1 hybrid flow, new nonce each time (steps 2–3) | 20 | 20 |
| A2 nonce reused, Eve reads the secret (steps 5–6) | 20 | 20 |
| A3 new nonce, Eve reads nothing + reasoning (steps 7–10) | 20 | 20 |
| Conventional technical written questions | 40 | — |
| Audit-the-AI | — | 20 |
| Explain-in-Plain-English | — | 10 |
| Prompt Problem | — | 10 |
| **Total** | **100** | **100** |

Everyone completes shared 60; finish only the assigned form's 40. In Weeks 1/10 shared work is
a guided Docker lab with no personal flag (Week 1 stays an analysis sheet). Week 12 code/testing belongs in
shared 60. Preserve and complete the full assigned question text outside class as needed:
Key exchange (Q5), ECIES (Q6) and the XOR explanation stay as optional extension questions; the Conventional form marks Q1–Q4.

The quiz remains inside the course's 10% quiz/participation component. Reproduction checks and
short explanations are feedback/authenticity checks within work, with no extra viva score or
automatic AIR-only gate. Use name/ID and cite tools/sources equally in both forms. Flags are
accepted only where the target provides them; a personal flag is required only if configured
and issued, never assumed from a shared default.

## Instructor checks and reflection

- Run `demo.py good`, `reuse`, `attack reuse` and `attack good` before class: `RESULT: Eve read message 2 WITHOUT the key` only for `reuse`.
- Check evidence, code and explanations together; an output string alone is not full understanding.
- Keep all further-reading questions available; do not turn extension work into an unannounced requirement.
- Record attendance, time actually taken, environment failures, misconceptions and corrections after teaching.
- This 100 minute allocation is a plan; do not claim a human timing pilot has been completed.

See [agenda](../../AGENDA.md), [assessment policy](../../syllabus.md) and [submission rules](../../SUBMISSION.md).
