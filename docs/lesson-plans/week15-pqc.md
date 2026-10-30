# Lesson Plan — Week 15: PQC and Lamport one-time key reuse

**02005104 · Cryptography and Network Security · Year 4 · Semester 2 AY2026 · Lecture**
**Contact time: 100 minutes.** Kind: LAB.
Lab/analysis: [`labs/week15-pqc`](../../labs/week15-pqc/README.md) · slides: `slides/week15.md`.

## Objectives and preparation

Explain which Lamport secrets are revealed by each signature and why one-time key state is a security requirement.

Prebuild images and reset state before each independent run. Arbitrary two messages need not reveal every secret: the complementary pair is the bounded classroom example.

Images, dependencies and long readings are preparation; confirm the environment before class.
Students may consult the supplied helper after explaining the bounded manual checkpoint. Only
authorized local targets/test data are used. An unavailable environment is handled with a
prepared trace/code example and documented follow-up, not a fabricated successful result.

## In-class run sheet

| Minutes | Activity |
|---|---|
| 0–10 | Retrieval quiz/review (Week 1: baseline diagnostic); recall previously taught material. |
| 10–20 | Brief the mechanism, safety scope and expected evidence. |
| 20–35 | Start fresh state and request a signature on the supplied all-zero bit string; relate revealed preimages to public hashes. |
| 35–60 | Obtain the complementary all-one signature on the vulnerable key; assemble the admin-message signature and record verification. |
| 60–80 | Test the fixed key single-use policy from fresh state; show second signing rejected and explain why the attack cannot collect both halves. |
| 80–90 | Connect the toy state failure to real one-time-signature management and state the Shor/Grover migration distinction. |
| 90–100 | Save before/after evidence, give concise reasoning, obtain feedback and submit the checkpoint. |

**Core artifact:** A forged toy Lamport signature and rejected second use of a fixed key.

## Assessment and after-class work

Worksheet 15 is **100 raw points → 2.5 course points**, one of 12 equally weighted worksheets:

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
HNDL/ML-KEM is optional extension work, carries no additional required points, and is not a full quantum/Shor implementation. Complete full PQC-family questions outside class.

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
