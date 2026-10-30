# Week 3 — MACs: Hash-Only Cookies and Length-Extension

**Topic (KOSEN68 source):** `Week3_MACs Questions.docx` · **Kind:** LAB
**Concepts:** message authentication codes, secret-prefix hashing, Merkle-Damgard
length-extension, HMAC · **Analogous CWE:** CWE-347 (Improper Verification of Cryptographic
Signature), CWE-290 (Authentication Bypass by Spoofing)

## This week — 100-minute class and assigned assessment

1. **Before class** — Prepare Docker and the host tools listed in SUBMISSION.md before class; complete first downloads before the contact block. Read the relevant recap.
2. **In class (100 minutes)** — 10 quiz/review + 10 brief + 60 shared practice/analysis +
   15 debrief + 5 evidence capture. Week 1 starts with orientation/review, not a quiz on
   material not yet taught. Slides: `slides/week03.md`. The full deck includes reference/deep-dive
   material; the instructor selects the core explanation for this block.
3. **Common work (60 points)** — Capture a guest cookie, calculate glue padding and demonstrate the intended SHA-256 length-extension forgery. Run the same technique against HMAC; distinguish a failed forgery from unrelated timing/replay limitations.
4. **Assigned format (40 points)** — complete **either** the Conventional written questions
   **or** AIR-Sec (Audit the AI 20 + EiPE 10 + Prompt Problem 10). Both versions total 100.
   Viva checks support feedback/authenticity within the criteria; they add no separate marks.
5. **After class** — finish detailed calculations, explanations and the assigned format;
   retain all original questions as assigned work or study extensions. Submit the worksheet
   PDF and required evidence according to [SUBMISSION.md](../../SUBMISSION.md). This week
   has no separate code-fix/GitHub submission.

## Objectives
- Explain why a bare hash of `key || message` (or `message || key`) is **not** a secure MAC.
- Execute a SHA-256 length-extension attack to forge a cookie without knowing the secret.
- Explain why HMAC's nested `H(key⊕opad || H(key⊕ipad || message))` construction defeats
  length-extension, and verify that empirically against a fixed target.
- Recognize related MAC-verification pitfalls (non-constant-time comparison, replay) even
  where this week's exploit doesn't target them directly.

## 🔓 Signature game — "Forge the Admin Cookie"
Two Flask targets, same endpoints, different signature scheme:

| Service | Port | Signature scheme | Vulnerable to length-extension? |
|---|---|---|---|
| `vulnerable_app.py` | `:8092` | `sig = SHA256(MAC_SECRET + data)` (secret-prefix hash) | **Yes** |
| `fixed_app.py` | `:8093` | `sig = HMAC-SHA256(MAC_SECRET, data)` | **No** |

**Why it's exciting:** forging your way into someone else's cookie with pure math, no password
needed, feels like a magic trick — until HMAC slams the door shut.

Both accept usernames of 1–64 ASCII letters, digits, `_`, `.` or `-`; malformed names
return `400` before any cookie is issued. This closes an unrelated field-injection shortcut
while preserving the intended length-extension exercise. Both issue a cookie at
`GET /login?user=<name>` encoding `data="user=<name>&admin=false"` plus a
signature. `GET /admin` recomputes the signature and, if it matches **and** `data` contains
`admin=true`, returns the flag.

1. **Capture:** log in as `guest` against `:8092` and grab the `data`/`sig` cookie pair.
2. **Forge:** without ever learning `MAC_SECRET`, compute a new `(data, sig)` pair that appends
   `&admin=true` to the message and still validates — using the length-extension property of
   SHA-256's Merkle-Damgard construction (`exploit.py` does this from scratch, no crypto library
   beyond the standard `hashlib`/`hmac`/`struct`).
3. **Cash in:** replay the forged cookie against `/admin` on `:8092` → flag.
4. **Confirm the fix:** replay the *same* forgery technique against `:8093` (HMAC) → must be
   rejected (`403`, no flag). This is the empirical proof that HMAC ≠ "hash with a key stuck on."

**MAC_SECRET length:** both apps use a demo secret that is **exactly 16 ASCII bytes**
(`0123456789abcdef` by default — override via the `MAC_SECRET` env var, keeping it 16 bytes so
`exploit.py`'s `SECRET_LEN` constant still matches). `exploit.py` assumes the secret's *length*
is known (a realistic assumption in practice — e.g. a fixed-width key field, or brute-forceable
over a small range of plausible lengths) but never its *value*.

## Run it
```bash
cd labs/week03-macs
docker compose up -d          # vulnerable_app.py on :8092, fixed_app.py on :8093
python exploit.py             # PASS on :8092 (flag), PASS on :8093 (correctly rejected); exit 0
```
Flag configuration: use an instructor-supplied personalised `.env` if available. Otherwise
record the shared demo flag with your own evidence and explanation; no automatic roster
validation is assumed.

**Verified:** `docker compose up -d` followed by `python exploit.py` was run against live
containers on this machine; both PASS checks printed and the script exited `0`. `MAC_SECRET`
env-var override was also confirmed to change both the captured signature and the forged
signature consistently, and negative controls (`/admin` with no cookie, `/admin` with a
legitimate non-admin cookie) both correctly returned `403`.

## Deliverable

Submit the common evidence and reasoning (60) plus only the assigned Conventional (40)
or AIR-Sec (40) format. The details below describe the common artifact; the worksheet
identifies the alternative sections.
The captured flag + your forged `(data, sig)` pair + a short note on exactly which byte range in
`data` is the SHA-256 glue padding your forgery relied on, and why HMAC closes the gap. Full
tasks: `worksheet.md`.

## References
- Boneh & Shoup, *A Graduate Course in Applied Cryptography*, ch. 6 (MACs) — free online.
- RFC 2104 — *HMAC: Keyed-Hashing for Message Authentication*.
- https://en.wikipedia.org/wiki/Length_extension_attack
- NIST FIPS 198-1 — *The Keyed-Hash Message Authentication Code (HMAC)*.
