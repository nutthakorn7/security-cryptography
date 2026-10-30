# Lesson Plan — Week 2: Hash functions and password storage

**02005104 · Cryptography and Network Security · Year 4 · Semester 2 AY2026 · Lecture**
**Contact time: 100 minutes.** Kind: LAB.
Lab/analysis: [`labs/week02-hash`](../../labs/week02-hash/README.md) · slides: `slides/week02.md`.

## Objectives and preparation

Recover a deliberately weak password, carry the session cookie, and explain the cost/salt controls of a password KDF.

Pre-pull images and install host requests before class. A full automated rerun is a cross-check, not a substitute for the observed session experiment.

Images, dependencies and long readings are preparation; confirm the environment before class.
Students may consult the supplied helper after explaining the bounded manual checkpoint. Only
authorized local targets/test data are used. An unavailable environment is handled with a
prepared trace/code example and documented follow-up, not a fabricated successful result.

## In-class run sheet

| Minutes | Activity |
|---|---|
| 0–10 | Retrieval quiz/review (Week 1: baseline diagnostic); recall previously taught material. |
| 10–20 | Brief the mechanism, safety scope and expected evidence. |
| 20–40 | Inspect the stored MD5 and recover the admin password with the supplied wordlist; record method and result. |
| 40–55 | Log in using a persistent session/cookie jar; compare /admin with and without the cookie. |
| 55–80 | Test the supplied bcrypt control, compare verification code and explain why a weak password is still guessable at higher cost. |
| 80–95 | Compare results/control, explain the mechanism and limits, receive feedback; begin the assigned form. |
| 95–100 | Save evidence and submit the in-class checkpoint. |

**Core artifact:** Weak-hash recovery, authenticated session and KDF comparison.

## Assessment and after-class work

Worksheet 2 is **100 raw points → 2.5 course points**, one of 12 equally weighted worksheets:

| Part | Conventional | AIR-Sec |
|---|---:|---:|
| Core work / observation | 20 | 20 |
| Control verification / limitations | 20 | 20 |
| Reproducible evidence / reasoning | 20 | 20 |
| Conventional technical written questions | 40 | — |
| Audit-the-AI | — | 20 |
| Explain-in-Plain-English | — | 10 |
| Prompt Problem | — | 10 |
| **Total** | **100** | **100** |

Everyone completes shared 60; finish only the assigned form's 40. In Weeks 1/10 shared work is
analysis/diagram/proof, with no Docker or flag requirement. Week 12 code/testing belongs in
shared 60. Preserve and complete the full assigned question text outside class as needed:
Complete the extended KDF design, pepper/salt discussion and assigned written questions after class.

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
