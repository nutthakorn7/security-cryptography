# Lesson Plan — Week 4: AES modes and CBC malleability

**02005104 · Cryptography and Network Security · Year 4 · Semester 2 AY2026 · Lecture**
**Contact time: 100 minutes.** Kind: LAB.
Lab/analysis: [`labs/week04-aes-modes`](../../labs/week04-aes-modes/README.md) · slides: `slides/week04.md`.

## Objectives and preparation

Derive a CBC XOR delta, observe the collateral block effect, and verify that authenticated encryption rejects modification.

Use the documented exact byte layout. Do not guess offsets from a displayed Unicode string.

Project: the Week 4 milestone forms the CryptoVault team and submits the design plan (KDF + AEAD-at-rest). Teams review the plan in class before submitting it; do not assume a design was submitted earlier.

Images, dependencies and long readings are preparation; confirm the environment before class.
Students may consult the supplied helper after explaining the bounded manual checkpoint. Only
authorized local targets/test data are used. An unavailable environment is handled with a
prepared trace/code example and documented follow-up, not a fabricated successful result.

## In-class run sheet

| Minutes | Activity |
|---|---|
| 0–10 | Retrieval quiz/review (Week 1: baseline diagnostic); recall previously taught material. |
| 10–20 | Brief the mechanism, safety scope and expected evidence. |
| 20–35 | Decode the token and locate IV, ciphertext blocks and the known plaintext field. |
| 35–60 | Compute and apply guest-to-admin XOR bytes; submit once and record the vulnerable result. |
| 60–80 | Repeat against the authenticated control and explain its rejection, including which block the original edit corrupts. |
| 80–95 | Compare results/control and explain the confidentiality/integrity difference; teams confirm membership and review their CryptoVault design plan with instructor feedback before submitting it. |
| 95–100 | Save evidence and submit the in-class checkpoint. |

**Core artifact:** A same-length CBC field modification and authenticated rejection.

## Assessment and after-class work

Worksheet 4 is **100 raw points → 2.5 course points**, one of 12 equally weighted worksheets:

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
ECB/XTS comparisons and longer mode-selection questions are further reading/written work. XTS reveals equality at the same sector/block position across rewrites, not arbitrary identical plaintext across different tweaks.

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
