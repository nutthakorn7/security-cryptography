---
marp: true
theme: default
paginate: true
header: "Security & Cryptography · Week 4"
---

# Week 4
## AES / Block-Cipher Modes (CBC bit-flipping, malleability)
Security & Cryptography · Nutthakorn Chalaemwongwan

<!-- Hook: ask "if AES is unbreakable, why do we keep having crypto CVEs?" Answer: AES the cipher is fine — what breaks is how it's *used*. This is the course spine every week: textbook-secure primitive, real-system failure. Today's failure: encryption without integrity lets you edit a message you can't even read. ~2 min. -->

---

## Today

- AES: the primitive (block cipher) vs. the **mode** wrapping it
- Why unauthenticated **CBC is malleable** — bit-flip an encrypted token
- The fix: **AES-GCM / AEAD** — encryption + integrity, together
- 🏁 Game: **Flip Your Way to Admin** — forge `role=admin` without the key

<!-- Roadmap, 1 min. Flag the lab up front: two live Flask targets, same endpoints, one CBC-only (breakable) and one GCM (not). Students will attack both. -->

---

## Recap — Week 3

- A **keyed hash is not automatically a MAC** — length-extension forges valid tags without the key
- HMAC fixed *that* gap: a construction designed to resist it
- Same theme, one level up: last week broke **integrity without a real MAC**; today we break **integrity without any authentication at all**

<!-- Bridge from W3. W3 = "keyed hash ≠ MAC." W4 = "encryption ≠ integrity" — an even more common real-world mistake, because encrypted data *looks* safe. Ask: "if I encrypt something, is it also protected from tampering?" (No — that's today.) ~2 min. -->

---

## AES: the primitive vs. the mode

- AES itself: a **textbook-secure** block cipher — 128-bit blocks, 128/192/256-bit keys, no known practical break
- A block cipher only encrypts **one 16-byte block**
- Real messages need a **mode of operation** to chain blocks together: ECB, CBC, GCM…
- The **mode** — not AES — decides whether the resulting scheme is actually secure

<!-- Set up the whole lecture's thesis in one slide. Emphasize: nobody breaks AES itself in this course, or in practice. Every attack today is a mode/protocol-usage attack. This is the "textbook-secure primitive" half of the spine. ~6 min. -->

---

## ECB leaks patterns (Q1)

- ECB encrypts each block **independently** with the same key
- Identical plaintext blocks → **identical ciphertext blocks**
- The "ECB penguin": encrypt a bitmap image in ECB — the outline is still visible in the ciphertext
- AES is unbroken here — the **mode** leaks structure, the cipher doesn't

<!-- Show the ECB penguin image if you have it handy (search "ECB penguin"). Ask: "the ciphertext looks random byte-by-byte — so why can you still see the outline?" Answer: repeated plaintext blocks (same-color regions) always encrypt the same way under ECB. This is Q1 on the worksheet. ~6 min. -->

---

## CBC: chaining fixes ECB's leak

- Each plaintext block is XOR-ed with the **previous ciphertext block** before encrypting
- `C_i = E(P_i XOR C_{i-1})` — block 0 uses a random **IV** instead of a previous block
- Decrypt: `P_i = D(C_i) XOR C_{i-1}`
- Fixes ECB's pattern leak... but the XOR-chaining opens a different door

<!-- Walk the formula on the board both directions (encrypt and decrypt). Stress the IV's job: without it, two messages with the same first block would still produce the same first ciphertext block (this is Q2 — reused IV leaks a shared prefix). Don't resolve the "different door" yet — that's the next slide's reveal. ~8 min. -->

---

## The gap: encryption ≠ integrity (Q3, Q9)

- CBC (and most classic modes) give **confidentiality only**
- Nothing stops an attacker from **editing ciphertext** — the receiver still decrypts to *something* and trusts it
- No MAC / no auth tag = no way to *detect* tampering
- **CWE-353** (Missing Support for Integrity Check) / **CWE-649** (Reliance on Encryption Without Integrity)
- Today's lab exploits exactly this gap to become `admin`

<!-- The core lesson of the week — say it plainly: "encrypted" and "tamper-proof" are NOT the same property, and CBC alone never claimed to give you the second one. Cold-call: "if you can't read the plaintext, can you still change it?" (Yes — that's the whole lab.) ~6 min. -->

---

## The target: an unauthenticated CBC token

`vulnerable_app.py :8096` issues `base64(IV ‖ C0 ‖ C1)` — AES-256-CBC, **no MAC**. Fixed 32-byte plaintext, two blocks:

| Block | Plaintext | Token bytes |
|---|---|---|
| 0 | `comment=FILLER!!` | `IV = token[0:16]` |
| 1 | `role=guest;xpad0` | `C0 = token[16:32]`, `C1 = token[32:48]` |

- `/login` issues the token, `/whoami` decrypts and reports the role, `/admin` checks it

<!-- Put this table on screen and keep it up for the next two slides — it's the anchor for the whole exploit. Point out: /login takes no user input, so the role offset is always the same deterministic byte range. That determinism is what makes the flip "clean." ~8 min. -->

---

## Why flipping C0 changes the role

- CBC decrypt: **`P1 = AES_decrypt(C1) XOR C0`**
- Flipping byte *k* of **C0** flips byte *k* of **P1** — deterministically, without the key
- `guest` sits at `P1[5..9]`; `admin` is also 5 bytes → same-length swap
- `C0[5+i] ^= guest[i] ^ admin[i]` for `i = 0..4` → edit token bytes `21..25`
- Side effect: block 0's plaintext (`comment=...`) turns to garbage — harmless, the app never reads it

<!-- The "aha" slide. Derive it live: P1 = D(C1) XOR C0, so if you XOR a delta d into C0, the new P1 becomes (old P1) XOR d. Pick d = guest XOR admin and the guest bytes become admin bytes. Ask: "what happens to block 0's plaintext when we edit C0?" (It becomes garbage — that's fine, only block 1 matters.) ~8 min. -->

---

## Cashing in the flip

```bash
docker compose up -d          # vulnerable_app.py :8096, fixed_app.py :8097
python exploit.py             # PASS :8096 (flag), PASS :8097 (rejected)
```

- No AES library needed for the attack itself — pure byte math (XOR)
- Replay the tampered token cookie against `/admin` → flag
- The attack **never touches the key** — swapping `AES_KEY` still works, proving it's pure ciphertext malleability, not a key leak

<!-- Live-run this if you can (or show a recorded terminal). The env-var swap point is important — it proves to skeptical students the exploit isn't secretly cheating by reading the key. Negative controls worth mentioning: /admin with no cookie → 403; /admin with the original untampered guest token → 403. ~8 min. -->

---

## The fix: authenticated encryption (Q4)

- `fixed_app.py :8097` issues `base64(nonce ‖ AES-256-GCM(plaintext) ‖ tag)`
- GCM = AES-CTR (confidentiality) **+ GHASH** authentication tag computed over the ciphertext
- Decrypt **checks the tag first** — any edited ciphertext byte → tag mismatch → reject
- Attacker can't recompute a valid tag without the key — no equivalent of the CBC trick exists

<!-- Contrast directly with the CBC slide: CBC has no step that ever asks "was this tampered with?" — it just decrypts and hands back bytes. GCM adds exactly that missing check. Explain GHASH only at the level "it's a keyed checksum over the ciphertext" — no need for the polynomial math here. ~8 min. -->

---

## Proving it empirically

- Apply the *same* "flip a ciphertext byte" idea to a `:8097` token
- Result: **`403`, no flag** — GCM rejects the tamper every time
- The concrete difference: CBC silently accepts a coherent forged plaintext; GCM raises on decrypt
- Q10's trap: GCM only helps if the app **actually checks the tag** and doesn't swallow the exception (an improper-verification bug, in the spirit of **CWE-347**)

<!-- This is the empirical proof step students run themselves in the lab — don't just assert it, show the exploit.py output for both ports side by side. Ask: "AES-GCM is deployed correctly here — could a developer still mess this up?" (Yes — catch and ignore the tag-verification exception, and you're back to square one.) ~5 min. -->

---

## The wider family of mode pitfalls

- **ECB** — pattern leakage (Q1)
- **CBC, reused IV** — reveals whether two messages share a prefix (Q2)
- **GCM, reused nonce** — catastrophic: keystream *and* auth key both reused → plaintext XOR leaks *and* tags become forgeable (Q5/Q6)
- **Disk encryption (LUKS/BitLocker)** uses **AES-XTS**, not GCM — no room for a per-sector nonce+tag, so it trades away authentication for a tweakable cipher (Q8)
- **Mobile/IoT**: AES-GCM where **hardware AES acceleration** exists (x86 AES-NI, ARMv8 crypto ext.); ChaCha20-Poly1305 otherwise — avoids timing side channels without hardware accel (Q7)

<!-- Zoom out from this week's one exploit to the whole family — the lab only shows malleability, but the worksheet's Q5–Q8 cover the rest. Nonce reuse in GCM is worse than people expect: it doesn't just leak, it can let an attacker forge future tags. Don't derive the math live — point them to the worksheet. ~8 min. -->

---

## 🏁 Game — Flip Your Way to Admin

| Service | Port | Scheme | Tamperable? |
|---|---|---|---|
| `vulnerable_app.py` | `:8096` | AES-256-CBC, no MAC | **Yes** |
| `fixed_app.py` | `:8097` | AES-256-GCM, AEAD | **No** |

1. `GET /login` on `:8096` → capture the `token` cookie
2. XOR the 5-byte delta into `token[21..25]` — no key needed
3. Replay against `/admin` → flag
4. Try the identical trick on `:8097` → rejected

<!-- Explain the game before lab: it's not guesswork, it's exact byte math they compute themselves on paper first (Task 2), then verify with exploit.py. "Why it's exciting" framing for students: flipping bytes you can't even read to seize admin is the closest thing to hacking in a movie this course gets. ~3 min. -->

---

## Lab today

> 📋 **Worksheet 4** — `labs/week04-aes-modes/worksheet.md` · kickoff: `docker compose up -d`

- **Part 1:** Q1–Q10 written questions (ECB/CBC/GCM/XTS/nonces)
- **Part 2A:** Tasks 0–5 — capture a token, locate the bytes, flip, cash in the flag, confirm GCM rejects, explain why
- **Part 2C — Audit the AI:** an AI claims CBC's random IV + secret key means "the client can't change the role" — find the flaw, rewrite with AEAD, verify against the lab
- **Part 2D:** EiPE + Prompt Problem · **Part 2E:** viva spot-check (3 questions, pass/fail gate)

<!-- The graded output. Point out Part 2C explicitly — the AI's answer is fluent, uses a real library, and is confidently wrong on exactly the one sentence that matters ("they'd have to break AES to produce a valid token"). That's this week's Audit-the-AI target. Remind them evidence needs a timestamp + identity per 2B. -->

---

## Key takeaways

- AES the cipher is textbook-secure — the **mode** is where real systems fail
- Encryption alone is not integrity: unauthenticated CBC is **malleable**
- AEAD (GCM / ChaCha20-Poly1305) binds confidentiality + integrity — but only if the tag is actually **checked**

<!-- Recap, 3 lines, tie explicitly back to the course spine: "textbook-secure primitive, real-system failure" — say it out loud one more time. Cold-call: "name one thing GCM checks that CBC never does." ~3 min. -->

---

# Questions?
Next week: Key Exchanges — MITM-ing an unauthenticated Diffie-Hellman handshake

<!-- Cliffhanger: "next week you become the silent eavesdropper in the middle of a key exchange — and then get shut out by a single authentication tag." Remind: docker targets for W5 will be new containers, same workflow. ~1 min. -->
