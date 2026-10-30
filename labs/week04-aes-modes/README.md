# Week 4 — AES / Block-Cipher Modes: CBC Bit-Flipping and Malleability

**Topic (KOSEN68 source):** `Week4_AES Questions.docx` · **Kind:** LAB
**Concepts:** AES block cipher, ECB/CBC/GCM modes, IV vs. nonce, malleability, authenticated
encryption (AEAD) · **Analogous CWE:** CWE-353 (Missing Support for Integrity Check), CWE-649
(Reliance on Obfuscation/Encryption Without Integrity), CWE-347 (Improper Verification of a
Cryptographic Signature)

## This week — 100-minute class and assigned assessment

1. **Before class** — Prepare Docker and the host tools listed in SUBMISSION.md before class; complete first downloads before the contact block. Read the relevant recap.
2. **In class (100 minutes)** — 10 quiz/review + 10 brief + 60 shared practice/analysis +
   15 debrief + 5 evidence capture. Week 1 starts with orientation/review, not a quiz on
   material not yet taught. Slides: `slides/week04.md`. The full deck includes reference/deep-dive
   material; the instructor selects the core explanation for this block.
3. **Common work (60 points)** — Capture the token, calculate the target byte range and XOR delta, and demonstrate CBC bit-flipping. Compare with GCM rejection and explain the integrity guarantee, nonce assumptions and limits of the demonstration.
4. **Assigned format (40 points)** — complete **either** the Conventional written questions
   **or** AIR-Sec (Audit the AI 20 + EiPE 10 + Prompt Problem 10). Both versions total 100.
   Viva checks support feedback/authenticity within the criteria; they add no separate marks.
5. **After class** — finish detailed calculations, explanations and the assigned format;
   retain all original questions as assigned work or study extensions. Submit the worksheet
   PDF and required evidence according to [SUBMISSION.md](../../SUBMISSION.md). This week
   has no separate code-fix/GitHub submission.

## Objectives
- Explain why **AES itself being secure** does not make an AES-*based* scheme secure — the
  **mode** (ECB/CBC/GCM) and the **absence/presence of integrity** decide it.
- Execute a **CBC bit-flipping** attack: alter the decrypted plaintext of an unauthenticated
  AES-CBC token (`role=guest` → `role=admin`) **without the key**, by XOR-ing bytes into the
  previous ciphertext block.
- Explain why **authenticated encryption** (AES-GCM here) defeats the same tampering — the tag
  check rejects any altered ciphertext — and verify that empirically against a live target.
- Recognize the family of related mode pitfalls (ECB pattern leakage, IV/nonce reuse, "encrypt
  but don't authenticate") even where this week's exploit targets only malleability.

## 🔓 Token game — "Flip Your Way to Admin"
Two Flask targets, same endpoints, different token scheme:

| Service | Port | Token scheme | Malleable / tamperable? |
|---|---|---|---|
| `vulnerable_app.py` | `:8096` | `base64(IV ‖ AES-256-**CBC**(plaintext))` — **no MAC/tag** | **Yes** — CBC bit-flip |
| `fixed_app.py` | `:8097` | `base64(nonce ‖ AES-256-**GCM**(plaintext) ‖ tag)` — AEAD | **No** — tag check rejects |

**Why it's exciting:** flipping bytes you can't even read to seize admin is the closest thing to
"hacking in a movie" this course gets.

Both issue a session token at `GET /login` encoding a **fixed server-side plaintext** whose role
field is `guest`. `GET /whoami` decrypts and reports the parsed role. `GET /admin` returns the
flag **iff** the parsed role is `admin`.

1. **Capture:** `GET /login` on `:8096`; grab the `token` cookie (base64 of `IV ‖ C0 ‖ C1`).
2. **Flip:** without ever learning the AES key, XOR a small delta into the ciphertext block that
   sits **before** the role block, so the *next* block decrypts to `role=admin` instead of
   `role=guest` (`exploit.py` does this with pure byte math — no crypto library needed for the
   attack itself).
3. **Cash in:** replay the tampered token against `/admin` on `:8096` → flag.
4. **Confirm the fix:** apply the *same* tampering idea to a `:8097` (GCM) token → must be
   **rejected** (`403`, no flag). This is the empirical proof that *encryption ≠ integrity*, and
   that AEAD is what closes the gap.

### The block layout (why the flip is clean)
The server plaintext is a **fixed 32-byte constant** (two AES blocks); `/login` takes no input
that shifts the role offset, so the target byte range is deterministic:

```
            plaintext bytes            token bytes (after base64-decode)
Block 0     [ 0..15]  b"comment=FILLER!!"    IV = token[ 0:16]   (random per login)
Block 1     [16..31]  b"role=guest;xpad0"    C0 = token[16:32]   <- we edit THIS block
                                             C1 = token[32:48]
```
CBC decrypts block 1 as **`P1 = AES_decrypt(C1) XOR C0`**. So flipping byte `k` of **C0** flips
byte `k` of **P1** — and turns block 0's plaintext (`comment=FILLER!!`) into unpredictable
garbage, which is fine because the app never reads the comment. `guest` sits at `P1[5..9]` and
`admin` is the same length (5 bytes), so the flip is a clean, length-preserving XOR:
`C0[5+i] ^= guest[i] ^ admin[i]` for `i = 0..4`, i.e. edit `token[21..25]`.

## Run it
```bash
cd labs/week04-aes-modes
docker compose up -d          # vulnerable_app.py on :8096, fixed_app.py on :8097
python exploit.py             # PASS on :8096 (flag), PASS on :8097 (correctly rejected); exit 0
```
Flag configuration: use an instructor-supplied personalised `.env` if available. Otherwise
record the shared demo flag with your own evidence and explanation; no automatic roster
validation is assumed.

**Verified:** `docker compose up -d` followed by `python exploit.py` was run against live
containers on this machine; both PASS checks printed (`:8096` returned the flag to the
bit-flipped token; `:8097` returned `403` with no flag to the same tampering) and the script
exited `0`. `/whoami` confirmed the tampered vuln token parses as `role=admin` while the original
parses as `role=guest`. An `AES_KEY` **and** `FLAG_AES` env-var override was also confirmed: the
exploit still succeeds and returns the *new* flag — proving the attack never depends on the key
(it is pure ciphertext malleability). Negative controls confirmed: `/admin` with no cookie →
`403`; `/admin` with a legitimate (unflipped) `role=guest` token → `403`.

## Deliverable

Submit the common evidence and reasoning (60) plus only the assigned Conventional (40)
or AIR-Sec (40) format. The details below describe the common artifact; the worksheet
identifies the alternative sections.
The captured flag + your tampered token (base64) + a short note stating **exactly which token
byte range** you XOR-ed and **why editing that block** (not the role block itself) is what
changes `guest` → `admin`, plus one sentence on why AES-GCM rejects the identical edit. Full
tasks: `worksheet.md`.

## References
- Boneh & Shoup, *A Graduate Course in Applied Cryptography*, ch. 4–5 (block ciphers, modes, AE)
  — free online.
- NIST SP 800-38A (block-cipher modes: ECB/CBC/…) and SP 800-38D (GCM).
- RFC 5116 — *An Interface and Algorithms for Authenticated Encryption* (AEAD).
- https://en.wikipedia.org/wiki/Malleability_(cryptography) and
  https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation
