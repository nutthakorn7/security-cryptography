# Lesson Plan — Week 12: Secure transport: TLS and Noise

**02005104 · Cryptography and Network Security · Year 4 · Semester 2 AY2026 · Lecture**
**Contact time: 100 minutes.** Kind: HYBRID.
Lab/analysis: [`labs/week12-secure-transport`](../../labs/week12-secure-transport/README.md) · slides: `slides/week12.md`.

## Objectives and preparation

Implement and test certificate-chain and hostname validation without silently disabling either check.

Code writing and tests belong to common practical 60 in both forms. Prebuild images and certificates before class; do not distribute a completed student function as the assessed submission.

Images, dependencies and long readings are preparation; confirm the environment before class.
Students may consult the supplied helper after explaining the bounded manual checkpoint. Only
authorized local targets/test data are used. An unavailable environment is handled with a
prepared trace/code example and documented follow-up, not a fabricated successful result.

## In-class run sheet

| Minutes | Activity |
|---|---|
| 0–10 | Retrieval quiz/review (Week 1: baseline diagnostic); recall previously taught material. |
| 10–20 | Brief the mechanism, safety scope and expected evidence. |
| 20–35 | Observe the disabled-verification run and identify the intercepted plaintext. |
| 35–60 | Every student implements build_client_context() in alice_student.py using the provided CA trust material and hostname verification. |
| 60–80 | Run trusted-peer and impostor tests, save the outcomes and explain the actual chain or hostname failure. |
| 80–95 | Compare results/control, explain the mechanism and limits, receive feedback; begin the assigned form. |
| 95–100 | Save evidence and submit the in-class checkpoint. |

**Core artifact:** A student-built TLS context with a successful trusted connection and MITM rejection.

## Assessment and after-class work

Worksheet 12 is **100 raw points → 2.5 course points**, one of 12 equally weighted worksheets:

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
Retain Noise patterns, 0-RTT/replay and PKI design questions as extended work; the classroom MITM may fail at issuer trust even when its claimed hostname matches.

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
