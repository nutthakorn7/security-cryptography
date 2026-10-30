# Lesson Plan — Week 3: MACs and length extension

**02005104 · Cryptography and Network Security · Year 4 · Semester 2 AY2026 · Lecture**
**Contact time: 100 minutes.** Kind: LAB.
Lab/analysis: [`labs/week03-macs`](../../labs/week03-macs/README.md) · slides: `slides/week03.md`.

## Objectives and preparation

Explain and demonstrate a secret-prefix SHA-256 MAC extension and show why the same construction attack does not forge HMAC.

Prepare the helper and images before class. Authenticate the original bytes and parse them consistently; arbitrary injected usernames are not the intended route.

Images, dependencies and long readings are preparation; confirm the environment before class.
Students may consult the supplied helper after explaining the bounded manual checkpoint. Only
authorized local targets/test data are used. An unavailable environment is handled with a
prepared trace/code example and documented follow-up, not a fabricated successful result.

## In-class run sheet

| Minutes | Activity |
|---|---|
| 0–10 | Retrieval quiz/review (Week 1: baseline diagnostic); recall previously taught material. |
| 10–20 | Brief the mechanism, safety scope and expected evidence. |
| 20–35 | Obtain an ordinary cookie and inspect exactly which bytes are authenticated. |
| 35–60 | Use the supplied SHA-256 state-resumption helper; derive the glue length and forge the allowed appended admin field. |
| 60–80 | Submit the forged cookie to both variants, capture accept/reject evidence and explain the construction change. |
| 80–95 | Compare results/control, explain the mechanism and limits, receive feedback; begin the assigned form. |
| 95–100 | Save evidence and submit the in-class checkpoint. |

**Core artifact:** A forged secret-prefix MAC and rejected HMAC control.

## Assessment and after-class work

Worksheet 3 is **100 raw points → 2.5 course points**, one of 12 equally weighted worksheets:

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
Retain full glue-padding derivations and tag-length questions for outside-class completion. An extendable HMAC outer hash is not a valid HMAC for an extended message.

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
