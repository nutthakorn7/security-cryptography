# Lesson Plan — Week 10: Asymmetric and hybrid encryption

**02005104 · Cryptography and Network Security · Year 4 · Semester 2 AY2026 · Lecture**
**Contact time: 100 minutes.** Kind: CONCEPTUAL.
Lab/analysis: [`labs/week10-hybrid-encryption`](../../labs/week10-hybrid-encryption/README.md) · slides: `slides/week10.md`.

## Objectives and preparation

Trace a hybrid-encryption design, identify a reused-nonce failure and justify authenticated key distribution.

This is shared practical analysis. No Docker flag or fabricated exploitation service is required; a diagram, calculation or executable proof can supply evidence.

Images, dependencies and long readings are preparation; confirm the environment before class.
Students may consult the supplied helper after explaining the bounded manual checkpoint. Only
authorized local targets/test data are used. An unavailable environment is handled with a
prepared trace/code example and documented follow-up, not a fabricated successful result.

## In-class run sheet

| Minutes | Activity |
|---|---|
| 0–10 | Retrieval quiz/review (Week 1: baseline diagnostic); recall previously taught material. |
| 10–20 | Brief the mechanism, safety scope and expected evidence. |
| 20–40 | Draw sender/recipient key roles and the KEM or key-wrap plus AEAD data flow. |
| 40–60 | Work through the supplied reused-GCM-nonce example or reproducible small calculation; show what equality/XOR relation leaks. |
| 60–80 | Correct the nonce/identity assumptions and test the design with an adversary counterexample. |
| 80–95 | Compare results/control, explain the mechanism and limits, receive feedback; begin the assigned form. |
| 95–100 | Save evidence and submit the in-class checkpoint. |

**Core artifact:** A KEM/DEM design, nonce analysis and counterexample.

## Assessment and after-class work

Worksheet 10 is **100 raw points → 2.5 course points**, one of 12 equally weighted worksheets:

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
Full RSA/OAEP size calculations, ECIES and protocol-tradeoff questions remain in the assigned written form and extension material.

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
