# Lesson Plan — Week 14: User authentication and password exposure

**02005104 · Cryptography and Network Security · Year 4 · Semester 2 AY2026 · Lecture**
**Contact time: 100 minutes.** Kind: HYBRID.
Lab/analysis: [`labs/week14-authentication`](../../labs/week14-authentication/README.md) · slides: `slides/week14.md`.

## Objectives and preparation

Show the toy challenge-response distinction and compare its limits with a real PAKE and phishing-resistant authentication.

The environment switch labelled PAKE enables a toy demonstration, not a full PAKE. The server still has password-derived verification material.

Project: the Week 14 milestone (transport wired in + self-audit drafted) is reviewed in class after the lab analysis.

Images, dependencies and long readings are preparation; confirm the environment before class.
Students may consult the supplied helper after explaining the bounded manual checkpoint. Only
authorized local targets/test data are used. An unavailable environment is handled with a
prepared trace/code example and documented follow-up, not a fabricated successful result.

## In-class run sheet

| Minutes | Activity |
|---|---|
| 0–10 | Retrieval quiz/review (Week 1: baseline diagnostic); recall previously taught material. |
| 10–20 | Brief the mechanism, safety scope and expected evidence. |
| 20–40 | Run the ordinary password mode; capture where the raw password reaches the server. |
| 40–60 | Run the toy challenge-response mode; capture a fresh nonce/proof and successful authentication without raw-password transmission. |
| 60–80 | Test/explain freshness and compare stolen-verifier/offline-guessing risk with OPAQUE, TOTP and FIDO2. |
| 80–95 | Compare results/control and distinguish replay protection, offline-guessing resistance and phishing resistance; then the CryptoVault transport-security and self-audit review (Week 14 milestone). |
| 95–100 | Save evidence and submit the in-class checkpoint. |

**Core artifact:** Password logging versus a fresh challenge/proof exchange.

## Assessment and after-class work

Worksheet 14 is **100 raw points → 2.5 course points**, one of 12 equally weighted worksheets:

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
Retain SSO/mTLS and full authentication comparison questions. Real OPAQUE protects against precomputation and permits client-side hardening; server plus credential compromise can still permit offline dictionary attacks (RFC 9807 § 10.11).

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
