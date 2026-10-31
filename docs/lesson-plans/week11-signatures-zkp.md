# Lesson Plan — Week 11: Signatures, ZKP and ECDSA malleability

**02005104 · Cryptography and Network Security · Year 4 · Semester 2 AY2026 · Lecture**
**Contact time: 100 minutes.** Kind: HYBRID.
Lab/analysis: [`labs/week11-signatures-zkp`](../../labs/week11-signatures-zkp/README.md) · slides: `slides/week11.md`.

## Objectives and preparation

Construct (r,n−s) for the same signed message and distinguish signature-byte identity from transaction identity.

Prebuild images, but acquire the signature after the current server starts: restarting changes the key/state. Run the manual original/twin pair before any automated exploit, then reset before a rerun.

Project: teams submit the CryptoVault sharing-flow draft (Week 11 milestone) before class; the instructor reviews it in the final feedback block.

Images, dependencies and long readings are preparation; confirm the environment before class.
Students may consult the supplied helper after explaining the bounded manual checkpoint. Only
authorized local targets/test data are used. An unavailable environment is handled with a
prepared trace/code example and documented follow-up, not a fabricated successful result.

## In-class run sheet

| Minutes | Activity |
|---|---|
| 0–10 | Retrieval quiz/review (Week 1: baseline diagnostic); recall previously taught material. |
| 10–20 | Brief the mechanism, safety scope and expected evidence. |
| 20–30 | Start fresh state and obtain a live signature; read the txid derivation. |
| 30–45 | Create the malleated twin `(r, n−s)` for the same message; record both signature encodings and their transaction identifiers. |
| 45–60 | Submit the original and the twin to the vulnerable service; record the duplicate authorization effect. |
| 60–75 | Run the fixed service's positive/negative controls from fresh state; show which low-S form is accepted and why the twin is rejected. |
| 75–90 | Explain the results: a protocol-level deduplication alternative and the boundary between malleability and nonce-reuse key recovery. |
| 90–100 | Save before/after evidence, give concise reasoning and submit the checkpoint; instructor feedback on the CryptoVault sharing-flow draft (Week 11 milestone). |

**Core artifact:** A signature twin, repeated authorization and canonicalization control.

## Assessment and after-class work

Worksheet 11 is **100 raw points → 2.5 course points**, one of 12 equally weighted worksheets:

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
Keep full Schnorr/Fiat–Shamir, EUF-CMA/SUF-CMA and nonce-reuse discussion outside the bounded core. This lab demonstrates malleability, not private-key recovery. Low-S canonicalizes only the twin pair; fresh signing randomness can produce other valid low-S signatures. Application replay/idempotency still needs an authenticated transaction ID or nonce and suitable spent-state.

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
