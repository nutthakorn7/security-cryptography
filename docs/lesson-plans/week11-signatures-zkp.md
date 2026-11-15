# Lesson Plan — Week 11: Signatures, ZKP and ECDSA malleability

**02005104 · Cryptography and Network Security · Year 4 · Semester 2 AY2026 · Lecture**
**Contact time: 100 minutes.** Kind: Docker lab (guided, two containers).
Lab/analysis: [`labs/week11-signatures-zkp`](../../labs/week11-signatures-zkp/README.md) · slides: `slides/week11.md`.

## Objectives and preparation

See that (r, n−s) is a second valid signature for the same message and distinguish signature-byte identity from transaction identity.

Prebuild images, but acquire the signature after the current server starts: restarting changes the key/state. Run the manual original/twin pair before any automated exploit, then reset before a rerun.

Project: teams submit the CryptoVault sharing-flow draft (Week 11 milestone) before class; the instructor reviews it in the final feedback block.

Images, dependencies and long readings are preparation; confirm the environment before class.
Students run the supplied helper (`bank.py`) in worksheet steps 2, 5, 7 and 9; the twin is calculated by the helper, no manual arithmetic or `curl` is asked. Only
authorized local targets/test data are used. An unavailable environment is handled with a
prepared trace/code example and documented follow-up, not a fabricated successful result.

## In-class run sheet

| Minutes | Activity |
|---|---|
| 0–10 | Week 10 retrieval quiz/review; recall hybrid encryption before the Week 11 lab. |
| 10–20 | Brief the mechanism, safety scope and expected evidence. |
| 20–30 | A1: start fresh state, run `bank.py vuln sign`, record the signature, its twin and the two different txids. |
| 30–45 | A1 fill-in, then read how the bank deduplicates (txid from the signature hash). |
| 45–60 | A2: `vuln pay original`, the same again (`409`), then `vuln pay twin` (`200`, total 200, flag). |
| 60–75 | A3: `fixed sign`, `fixed pay original` (`200`) and `fixed pay twin` (`403`); find the `is_low_s` line. |
| 75–90 | Explain the results: a protocol-level deduplication alternative and the boundary between malleability and nonce-reuse key recovery. |
| 90–100 | Save before/after evidence, give concise reasoning and submit the checkpoint; instructor feedback on the CryptoVault sharing-flow draft (Week 11 milestone). |

**Core artifact:** the signature and its twin, the `409` replay, the repeated authorization (total 200 + flag) and the fixed bank's `403`.

## Assessment and after-class work

Worksheet 11 is **100 raw points → 2.5 course points**, one of 12 equally weighted worksheets:

| Part | Conventional | AIR-Sec |
|---|---:|---:|
| A1 signature and its twin (steps 2–3) | 20 | 20 |
| A2 double processing at the vulnerable bank (steps 5–6) | 20 | 20 |
| A3 fixed bank, low-S and its limits (steps 7–10) | 20 | 20 |
| Conventional technical written questions | 40 | — |
| Audit-the-AI | — | 20 |
| Explain-in-Plain-English | — | 10 |
| Prompt Problem | — | 10 |
| **Total** | **100** | **100** |

Everyone completes shared 60; finish only the assigned form's 40. Shared work is
a guided Docker lab with no personal flag (Weeks 1 and 10 were analysis / guided demo). Week 12 code/testing belongs in
shared 60. Preserve and complete the full assigned question text outside class as needed:
Schnorr is marked in Conventional Q4 (plain words); RSA/ECDSA/EdDSA, substitution attacks, SUF-CMA and Fiat–Shamir stay as optional questions outside the bounded core. This lab demonstrates malleability, not private-key recovery. Low-S canonicalizes only the twin pair; fresh signing randomness can produce other valid low-S signatures. Application replay/idempotency still needs an authenticated transaction ID or nonce and suitable spent-state.

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
