# Lesson Plan — Week 4: AES modes and CBC malleability

**02005104 · Cryptography and Network Security · Year 4 · Semester 2 AY2026 · Lecture**
**Contact time: 100 minutes.** Kind: LAB.
Lab/analysis: [`labs/week04-aes-modes`](../../labs/week04-aes-modes/README.md) · slides: `slides/week04.md`.

## Objectives and preparation

See that an encrypted CBC token can be changed without the key and the server does not notice, run the supplied script that turns a guest token into an admin one, and show that authenticated encryption (GCM) rejects a changed token.

Students pull the image before class; the script runs inside the container, so no host Python is needed (`docker compose exec -e FIXED_HOST=fixed vulnerable python exploit.py`; without the `-e` part it waits about a minute, then prints `FAIL: fixed app never came up`). The worksheet uses no byte offsets or hand XOR.

Project: the Week 4 milestone forms the CryptoVault team and submits the design plan (KDF + AEAD-at-rest). Teams review the plan in class before submitting it; do not assume a design was submitted earlier.

Images, dependencies and long readings are preparation; confirm the environment before class.
Students run the supplied helper (`exploit.py`) in worksheet step 8; no manual byte work is asked. Only
authorized local targets/test data are used. An unavailable environment is handled with a
prepared trace/code example and documented follow-up, not a fabricated successful result.

## In-class run sheet

| Minutes | Activity |
|---|---|
| 0–10 | Retrieval quiz on Week 3; recall previously taught material. |
| 10–20 | Brief the mechanism, safety scope and expected evidence. |
| 20–35 | A1: log in, read `/whoami`, change one letter of the CBC token and see that the server still answers `guest`. |
| 35–60 | A2: read the picture, run the supplied `exploit.py` inside the container, record `guest` becoming `admin` and the flag. |
| 60–80 | A3: make the same one-letter change to the GCM token, see `invalid or tampered token`, compare the CBC and GCM code lines and explain why the tag check refuses it. |
| 80–95 | Compare results/control and explain the confidentiality/integrity difference; teams confirm membership and review their CryptoVault design plan with instructor feedback before submitting it. |
| 95–100 | Save evidence (answer-sheet boxes for steps 1–17) and note what is left; the PDF is due Sunday 29 Nov 2026 23:59 ICT. |

**Core artifact:** A changed CBC token that the server accepts (`guest` → `admin`) and a changed GCM token that it refuses.

## Assessment and after-class work

Worksheet 4 is **100 raw points → 2.5 course points**, one of 12 equally weighted worksheets:

| Part | Conventional | AIR-Sec |
|---|---:|---:|
| A1 — encrypted is not tamper-proof (steps 1–6) | 20 | 20 |
| A2 — script changes the token to admin (steps 8–10) | 20 | 20 |
| A3 — GCM notices + reasoning (steps 12–17) | 20 | 20 |
| Conventional technical written questions | 40 | — |
| Audit-the-AI | — | 20 |
| Explain-in-Plain-English | — | 10 |
| Prompt Problem | — | 10 |
| **Total** | **100** | **100** |

Everyone completes shared 60; finish only the assigned form's 40. In Weeks 1/10 shared work is
analysis/diagram/proof, with no Docker or flag requirement. Week 12 code/testing belongs in
shared 60. Preserve and complete the full assigned question text outside class as needed:
Q2 and Q6–Q10 (IV reuse, nonce reuse, GCM vs ChaCha20-Poly1305, XTS, HTTPS, an unchecked tag) are optional reading with no marks. XTS reveals equality at the same sector/block position across rewrites, not arbitrary identical plaintext across different tweaks.

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
