# Week 10 — Asymmetric & Hybrid Encryption

**Kind:** Conceptual (no Docker target, no flag — same precedent as this course's Week 1 and
`software-security`'s Weeks 1, 12–13: honestly flag-less, rubric-graded content).
**References:** NIST SP 800-56A (key establishment), SP 800-38D (GCM) · OWASP Cryptographic
Storage Cheat Sheet

## 100-minute class and assigned worksheet version

**In class:** 10 min retrieval quiz + 10 min brief explanation + 60 min practice/analysis + 15 min debrief + 5 min evidence capture = 100 min.

**Shared core — every student:** Trace the hybrid-encryption protocol and key roles; compare correct nonce discipline with a repeated-nonce case. Provide a repeatable diagram, state table or two-message XOR derivation. No Docker target, flag or standalone code submission is required for the shared core.

**Preparation and extensions:** Prepare the public-key/AEAD reading and Python environment if using the AIR-Sec task. Complete the assigned version's full essays or code audit, proof and corrected code outside the core block as needed.

**Assessment:** everyone completes the shared core (60 points) plus **one assigned version** (40 points): Conventional written analysis, or AIR-Sec Audit-the-AI 20 + EiPE 10 + Prompt Problem 10. Both versions total 100. All questions remain available; complete the assigned version's full questions, using out-of-class time for extended responses. The other version is ungraded reference practice, not an additional requirement. Viva/micro-demo questions are formative checks of the submitted explanation, with no separate points or automatic pass/fail score gate.

**Evidence:** record reproducible observations or reasoning and your name/student ID. Where the local target prints a shared placeholder flag, record it as observed; a personalized flag or live CTFd account is not a prerequisite. Follow SUBMISSION.md for the announced hand-in channel.

## This week — what to do
1. **Before class** — skim the Week 6 recap (AEAD — the previous teaching week; Weeks 7–9 are review and the midterm sittings). No environment setup needed —
   this week is Python-only, standard library + `cryptography` (already used in earlier weeks).
2. **Concept preparation and brief explanation (within the 100-minute plan)** — weekly quiz first (~10 min), then the lecture. Slides:
   `slides/week10.md`.
3. **Practice and assigned-version work (core in class; extensions outside class)** — complete **Worksheet 10**: the shared analysis core plus only your assigned Conventional or AIR-Sec version; the AIR-Sec task in `audit_the_ai/` retains its proof script and corrected-code deliverables.
4. **Submit** — shared-core evidence/reasoning plus your assigned 40-point version in the worksheet PDF via [SUBMISSION.md](../../SUBMISSION.md). For AIR-Sec, attach the proof script, its output and the complete `fixed_hybrid_encrypt.py` code in the PDF/worksheet; no separate GitHub code-fix submission is required.

5. **Project** — if your term project sends data between two parties that don't already share a
   secret, this week's pattern (RSA-OAEP wraps an AES session key) is directly applicable.

## Objectives
- Explain why asymmetric encryption alone is unsuitable for bulk data (performance + message
  size limits), and why hybrid encryption exists to solve that.
- Trace the complete hybrid-encryption flow end to end: key generation, key wrapping, symmetric
  encryption, transmission, unwrapping, decryption.
- Explain how a public key lets anyone encrypt to a recipient, while only the holder of the
  matching private key can decrypt.
- Explain asymmetric key exchange (how two parties derive a shared secret an eavesdropper
  cannot compute) and connect it to ECIES as a concrete hybrid scheme built on ECDH.
- Audit an AI-generated cryptographic implementation for a subtle-but-catastrophic correctness
  bug that a surface-level review would miss.

## 🔬 Signature game — "Nonce Detective"
You're handed a hybrid-encryption implementation that looks textbook-correct — proper RSA-OAEP,
proper AES-GCM, nothing obviously wrong at a skim. Find the one planted bug, then prove it's real
by actually recovering leaked plaintext from two intercepted messages, not just pointing at a
line of code.

**Why it's exciting:** the code passes every "did they use the right primitives" checklist — the
only way to catch it is to actually think like an attacker, and the payoff is a genuine "aha"
the moment the recovered plaintext prints.

## Why no lab target this week

Nothing here is a "break into a running service" exploit — it's protocol design and
correctness analysis, same category as `software-security`'s threat-modeling and supply-chain
weeks. Rather than force an artificial CTF wrapper onto that, this week's hands-on core is an
**Audit-the-AI** exercise: a plausible, AI-generated-looking hybrid-encryption implementation
that passes a shallow review and fails a careful one. See `audit_the_ai/README.md`.

## Deliverable
Complete the shared core (60 points) and only the assigned version (40 points), as listed in the worksheet rubric. Include reproducible evidence/reasoning in your worksheet PDF. All unassigned-version questions remain available for ungraded practice.
AIR-Sec retains every original audit deliverable: quoted buggy lines, proof script and output, explanation, and full corrected code attached in the PDF/worksheet. No Docker target or flag is required.

## References
- NIST SP 800-56A Rev. 3, *Recommendation for Pair-Wise Key-Establishment Schemes Using
  Discrete Logarithm Cryptography*.
- NIST SP 800-38D, *Recommendation for Block Cipher Modes of Operation: GCM and GMAC*.
- https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html
- SEC 1: Elliptic Curve Cryptography, §5.1 (ECIES) — Standards for Efficient Cryptography Group.
- Joux, *Authentication Failures in NIST version of GCM* (2006).
