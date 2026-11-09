# Lesson Plan — Week 6: AEAD and the CBC padding oracle

**02005104 · Cryptography and Network Security · Year 4 · Semester 2 AY2026 · Lecture**
**Contact time: 100 minutes.** Kind: LAB.
Lab/analysis: [`labs/week06-aead`](../../labs/week06-aead/README.md) · slides: `slides/week06.md`.

## Objectives and preparation

See that an unauthenticated CBC server that never shows the plaintext still leaks it through two different answers (`200` vs `403`), run the supplied script that reads the secret from those answers without the key, and show that the GCM server gives the same answer for every change.

Students pull the image before class; the scripts run inside the container, so no host Python is needed (`docker compose exec vulnerable python ask.py vuln end`; `docker compose exec -e FIXED_HOST=fixed vulnerable python exploit.py`; without the `-e` part `exploit.py` waits about a minute, then prints `FAIL: fixed app never came up`). `ask.py` is a small helper added for this lab so students never type JSON. The worksheet uses no byte offsets or hand XOR.

Project: no CryptoVault milestone this week; the KDF + AEAD-at-rest vault is due in Week 7.

Images, dependencies and long readings are preparation; confirm the environment before class.
Students run the supplied helpers (`ask.py`, `exploit.py`) in worksheet steps 3–5, 8 and 11–14; no manual byte work is asked. Only
authorized local targets/test data are used. An unavailable environment is handled with a
prepared trace/code example and documented follow-up, not a fabricated successful result. Without Docker, steps 8 and 14 can use the simulator at `learn.zcr.ai/sim/padding-oracle` (a toy cipher, not real AES).

## In-class run sheet

| Minutes | Activity |
|---|---|
| 0–10 | Retrieval quiz on Week 5; recall previously taught material. |
| 10–20 | Brief: padding, the `200` / `403` yes/no, why it is a leak; safety scope and expected evidence. |
| 20–35 | A1: fetch the secret, ask the CBC server about the original, a letter changed at the start and a letter changed near the end; record `200`, `200`, `403`. |
| 35–60 | A2: read the picture, run the supplied `exploit.py` inside the container, record the three blocks, the recovered secret and the flag. |
| 60–80 | A3: ask the GCM server the same three questions (`200`, `403`, `403`), see the script find no signal, compare the CBC and GCM code lines and explain why the tag check gives nothing away. |
| 80–95 | Compare results/control and explain the confidentiality/integrity difference and the limits of GCM (ignored tag error, repeated nonce, other leaking messages); receive feedback; begin the assigned form. |
| 95–100 | Save evidence (answer-sheet boxes for steps 1–17) and note what is left; the PDF is due Sunday 13 Dec 2026 23:59 ICT. |

**Core artifact:** Three CBC answers (`200`, `200`, `403`), the secret recovered from them, and three GCM answers (`200`, `403`, `403`) with no recovery.

## Assessment and after-class work

Worksheet 6 is **100 raw points → 2.5 course points**, one of 12 equally weighted worksheets:

| Part | Conventional | AIR-Sec |
|---|---:|---:|
| A1 — what the CBC server gives away (steps 1–6) | 20 | 20 |
| A2 — script reads the secret without the key (steps 8–10) | 20 | 20 |
| A3 — GCM gives nothing away + reasoning (steps 11–17) | 20 | 20 |
| Conventional technical written questions | 40 | — |
| Audit-the-AI | — | 20 |
| Explain-in-Plain-English | — | 10 |
| Prompt Problem | — | 10 |
| **Total** | **100** | **100** |

Everyone completes shared 60; finish only the assigned form's 40. In Weeks 1/10 shared work is
analysis/diagram/proof, with no Docker or flag requirement. Week 12 code/testing belongs in
shared 60. Preserve and complete the full assigned question text outside class as needed:
Q2 (safe composition: Encrypt-then-MAC needs a MAC over IV and ciphertext, separate keys, and verification before decrypting), Q5 (associated data), Q6 (CBC malleability and the oracle), Q8 (choosing an AEAD) and the Extension (`D(C_t)[15] = guess XOR 0x01`) are optional reading with no marks.

The quiz remains inside the course's 10% quiz/participation component. Reproduction checks and
short explanations are feedback/authenticity checks within work, with no extra viva score or
automatic AIR-only gate. Use name/ID and cite tools/sources equally in both forms. Flags are
accepted only where the target provides them; a personal flag is required only if configured
and issued, never assumed from a shared default. The lab uses a fixed key and nonce for this demo only because it encrypts exactly one message; say so in class, since real systems must never repeat a nonce under a key.

## Instructor checks and reflection

- Check that the vulnerable/control experiment produces distinct, interpretable results before class.
- Check evidence, code and explanations together; an output string alone is not full understanding.
- Keep all further-reading questions available; do not turn extension work into an unannounced requirement.
- Record attendance, time actually taken, environment failures, misconceptions and corrections after teaching.
- This 100 minute allocation is a plan; do not claim a human timing pilot has been completed.

See [agenda](../../AGENDA.md), [assessment policy](../../syllabus.md) and [submission rules](../../SUBMISSION.md).
