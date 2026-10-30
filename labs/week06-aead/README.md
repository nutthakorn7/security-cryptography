# Week 6 — Authenticated Encryption (AEAD): the CBC Padding Oracle

**Topic:** *(new topic — not in KOSEN68; built fresh)* · **Kind:** LAB
**Concepts:** authenticated encryption (AEAD), unauthenticated-CBC malleability, PKCS#7 padding
oracle, AES-GCM, encrypt-then-MAC · **Analogous CWE:** CWE-347 (Improper Verification of
Cryptographic Signature), CWE-757 (Selection of Less-Secure Algorithm), CWE-204
(Observable Response Discrepancy — the side channel)

This is the **capstone of the symmetric block**: Week 3 gave you a MAC (integrity), Week 4 gave
you AES-CBC (confidentiality) and showed CBC ciphertext is *malleable*. The running
target here is **CBC with no MAC at all**, plus a padding-validity response: it demonstrates
a **padding oracle**, not an implementation of MAC-then-encrypt or encrypt-and-MAC. The
comparison target uses AES-GCM. Correct encrypt-then-MAC composition is discussed in the
written questions; it is not the supplied fixed target.

## This week — 100-minute class and assigned assessment

1. **Before class** — Prepare Docker and the host tools listed in SUBMISSION.md before class; complete first downloads before the contact block. Read the relevant recap.
2. **In class (100 minutes)** — 10 quiz/review + 10 brief + 60 shared practice/analysis +
   15 debrief + 5 evidence capture. Week 1 starts with orientation/review, not a quiz on
   material not yet taught. Slides: `slides/week06.md`. The full deck includes reference/deep-dive
   material; the instructor selects the core explanation for this block.
3. **Common work (60 points)** — Capture the ciphertext, explain one manual oracle query and run the CBC padding-oracle recovery. Compare with the GCM target, distinguish no usable padding signal from a failed setup, and state tag/nonce assumptions.
4. **Assigned format (40 points)** — complete **either** the Conventional written questions
   **or** AIR-Sec (Audit the AI 20 + EiPE 10 + Prompt Problem 10). Both versions total 100.
   Viva checks support feedback/authenticity within the criteria; they add no separate marks.
5. **After class** — finish detailed calculations, explanations and the assigned format;
   retain all original questions as assigned work or study extensions. Submit the worksheet
   PDF and required evidence according to [SUBMISSION.md](../../SUBMISSION.md). This week
   has no separate code-fix/GitHub submission.

## Objectives
- State what **AEAD** stands for and the three guarantees it delivers in one primitive.
- Explain a **padding oracle**: how a single distinguishable "bad padding" response turns
  unauthenticated CBC into a byte-by-byte decryption of arbitrary ciphertext — *without the key*.
- Run the standard CBC padding-oracle attack to recover a secret plaintext (containing your flag)
  from ciphertext alone, using only a 200-vs-403 side channel.
- Explain why **AES-GCM** (an AEAD cipher) has no padding oracle — stream mode means no padding to
  probe, and the authentication tag is verified *before* any plaintext is released — and verify
  that empirically against a fixed target that returns a uniform error for every failure.
- Compare encrypt-then-MAC under its standard assumptions with compositions that require
  extra care; authenticate all relevant ciphertext/IV data and withhold unauthenticated plaintext.

## 🔓 Decryption game — "Read the Secret Without the Key"
Two Flask targets, same endpoints, different cipher:

| Service | Port | Cipher | Vulnerable to a padding oracle? |
|---|---|---|---|
| `vulnerable_app.py` | `:8098` | AES-256-**CBC**, unauthenticated, `/decrypt` leaks padding validity | **Yes** |
| `fixed_app.py` | `:8099` | AES-256-**GCM** (AEAD), `/decrypt` returns a **uniform** error | **No** |

**Why it's exciting:** a padding oracle turns a plain 403 error into a skeleton key, recovering a
whole secret one byte at a time from nothing but yes/no answers.

Both serve the *same* secret message (which **contains the flag**) at `GET /secret` as
base64. Both expose `POST /decrypt {"ciphertext": "<base64>"}`. The difference is the *decrypt
response*:

- **Vulnerable (`:8098`, CBC):** `200` if the decrypted plaintext has **valid PKCS#7 padding**,
  `403 "bad padding"` if not. Those two distinguishable answers are the **oracle** — the endpoint
  *never returns the plaintext*, yet the attacker recovers it purely from the 200/403 signal.
- **Fixed (`:8099`, GCM):** `200` only if the 128-bit tag verifies; **`403` (uniform)** for *any*
  failure — bad base64, wrong length, bad nonce, tag mismatch — all indistinguishable. No signal.

1. **Grab the ciphertext:** `GET /secret` on `:8098` → `base64(IV || ct)`.
2. **Recover it:** using only the `/decrypt` oracle, run the CBC padding-oracle attack to recover
   the full plaintext **byte-by-byte, without the AES key** (`exploit.py` implements it from
   scratch — no crypto library needed on the attacker side, only `requests`).
3. **Read the flag:** the recovered plaintext is `msg:FLAG{...}` → that's your flag.
4. **Confirm the fix:** run the same padding-oracle routine against `:8099` (AES-GCM). It gets **zero**
   usable signal (every query is `403`), recovers nothing → this target provides no usable padding signal. This is evidence against
   this attack, not proof that every aspect of the application is secure.

**The key is never known to the attacker.** The whole point is that unauthenticated CBC + a
padding side channel gives *decryption without the key*; AEAD removes both the side channel and
the malleability.

## Run it
```bash
cd labs/week06-aead
docker compose up -d          # vulnerable_app.py on :8098, fixed_app.py on :8099
python exploit.py             # PASS on :8098 (recovers plaintext + flag), PASS on :8099
                              #   (attack gets no signal); exit 0
docker compose down
```
Flag configuration: use an instructor-supplied personalised `.env` if available. Otherwise
record the shared demo flag with your own evidence and explanation; no automatic roster
validation is assumed.

**Verified:** `docker compose up -d --build` (from a scratch copy — OneDrive placeholders can
break in-place `docker build`) followed by `python exploit.py` was run against live containers on
this machine. Both PASS checks printed and the script exited `0`: the padding oracle recovered
the full plaintext `msg:FLAG{...}` from `:8098` **without the key**, and the
identical attack recovered **nothing** from the AES-GCM app on `:8099` (uniform `403`). The
`FLAG_AEAD` env-override was confirmed with a different-length flag (`FLAG{aead_student_42_xyz}` →
a 2-block ciphertext instead of 3) — the exploit derived the new block count from `/secret` and
recovered it correctly, PKCS#7 padding stripped. Negative controls confirmed: garbage/empty
ciphertext → `403` on both apps; a tampered GCM tag → `403` on `:8099`; the original secret →
`200` on both.

## Deliverable

Submit the common evidence and reasoning (60) plus only the assigned Conventional (40)
or AIR-Sec (40) format. The details below describe the common artifact; the worksheet
identifies the alternative sections.
The recovered flag + a short note on **how changing the forged previous block forces
`0x01`, `0x02 0x02`, … in the decrypted plaintext**. Explain how several trial queries identify
a byte of the intermediate value `D(C_t)`, including the false-positive check, and why
AES-GCM provides no equivalent padding-validity probe. Full tasks: `worksheet.md`.

## References
- Boneh & Shoup, *A Graduate Course in Applied Cryptography*, ch. 9 (Authenticated Encryption) —
  free online.
- Vaudenay (2002), *Security Flaws Induced by CBC Padding* — the original padding-oracle paper.
- NIST SP 800-38D — *Galois/Counter Mode (GCM) and GMAC*.
- RFC 5116 — *An Interface and Algorithms for Authenticated Encryption* (defines the AEAD API).
- https://en.wikipedia.org/wiki/Padding_oracle_attack
