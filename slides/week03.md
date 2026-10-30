---
marp: true
theme: default
paginate: true
header: "Security & Cryptography · Week 3"
---

# Week 3
## MACs (hash-only auth, length-extension)
Security & Cryptography · Nutthakorn Chalaemwongwan

<!-- Hook: ask "if I hash a secret and a message together, is that a MAC?" Let them say yes. Today you prove them wrong — live — by forging an admin cookie with pure math, no password.  -->

---

## Today

**100-minute class:** 10 quiz/review · 10 brief · 60 shared practice · 15 debrief · 5 capture.
**Assessment:** common 60 + assigned Conventional written 40 **or** AIR-Sec 20/10/10.
Preparation and detailed write-up are outside the contact block. Week 1 opens with orientation/review.

<!-- The full deck is a teaching/reference bank, not an additional lecture block.
Use the core explanation for the 10-minute brief and just-in-time guidance during practice;
assign the remaining deep dives as preparation or follow-up. Viva is formative, with no
separate points or automatic-zero rule. -->

- Hashes vs. MACs vs. signatures — what "authenticity" actually requires
- Why `H(secret ‖ data)` is *not* a MAC — SHA-256 length-extension
- HMAC's nested construction — why it closes the gap
- 🔓 Game: **Forge the Admin Cookie**

<!-- Roadmap,  Flag the lab: two Flask apps, same endpoints, one uses a secret-prefix hash and one uses real HMAC — students forge a cookie against the first and watch the same trick bounce off the second. -->

---

## Recap — Week 2

- A hash proves **integrity** only if the attacker can't recompute it
- Bare `H(password)` broke because attackers *could* recompute — at scale, with rainbow tables
- Fix was salting + slow KDFs (bcrypt/Argon2) — but hashing still had **no secret**

<!-- Bridge from W2. W2 = hashing without a secret, broken by brute-force/precomputation. Natural next question: "what if I just add a secret to the hash?" That's exactly today's trap.  -->

---

## The spine of this course

**Textbook-secure primitive → real-system failure → correct construction.**

- SHA-256 is a mathematically sound, collision-resistant hash function. Full stop.
- Stick a secret in front of it to build authentication, and the *system* breaks anyway
- Today's failure: **length-extension** — misuse, not a flaw in SHA-256 itself

<!-- State the spine explicitly — this is the sentence that should echo through every week. SHA-256 isn't broken; the way people bolt a secret onto it is.  -->

---

## What a MAC needs to guarantee

- **Integrity** — data wasn't modified in transit
- **Authenticity** — data came from someone who knows a secret key
- A hash alone gives you neither if the attacker can compute the same hash function

> `cookie = username || SHA-3(username)` — no secret at all. Anyone can recompute it for `username=admin`.

<!-- This is source Q1: the hash-only cookie has zero secret, so tampering is undetectable — the server has nothing to check against that the attacker can't also produce. Ask: "what's missing?" → a key.  -->

---

## The tempting-but-wrong fix: secret-prefix hash

```
sig = SHA256(MAC_SECRET + data)
```

- Looks reasonable: now there IS a secret in the computation
- **This is exactly the vulnerable construction in `vulnerable_app.py`**
- CWE-347 — Improper Verification of Cryptographic Signature

<!-- This is source Q5's construction, generalized. Point out: this "feels" secure to most developers — that's why the bug is so common in the wild (old API signing schemes shipped exactly this).  -->

---

## Why: Merkle-Damgard hashes process in chunks

- SHA-256 absorbs input in 64-byte blocks, updating internal state block by block
- The **final internal state IS the digest** — nothing more, nothing less
- If you know a valid `SHA256(secret ‖ data)`, you know the *exact* internal state after processing `secret ‖ data`

<!-- The mechanical core. Draw the block chain on the board: block1 -> state1 -> block2 -> state2 -> ... -> stateN = digest. The digest isn't a "summary" — it's literally where the computation stopped.  -->

---

## Length-extension: resume, don't restart

- Attacker doesn't need `secret` — only `sig`, `len(secret)`, and `len(data)`
- Attacker resumes SHA-256 compression **from that known state**
- Appends **glue padding** (the `0x80` + zero bytes + 8-byte bit-length SHA-256 always adds) then their own extra bytes (`&admin=true`)
- Result: a valid `SHA256(secret ‖ data ‖ glue ‖ extra)` — computed with **zero knowledge of `secret`**

![Two block chains sharing one starting point. Top: the server's real MAC computation feeds a locked secret block and a data block through the hash's compression function to produce a digest. Bottom: the attacker never sees the secret, but takes that same digest as their own starting state and feeds it, left to right, through glue-padding then extension blocks through the identical compression function, producing a forged digest the server accepts as valid.](img/length-extension.svg)

<!-- The attack itself. Emphasize: the secret's LENGTH must be known/guessable (16 bytes here, a realistic assumption per the README), but its VALUE never is. Worksheet Task 2 has them hand-compute the glue length: len(secret)+len(data) = 16+22 = 38 bytes, using SHA-256's own padding rule. Run the sim below live before Task 2 — sliding the length guess to a wrong value and watching Verifier A reject it is a faster way to land "length must be right, not just guessed" than the board math alone.  -->

```sim
mac-extend
```

<!-- The sim uses a toy hash, not real SHA-256 — same Merkle-Damgard shape (padding leaks length, digest IS the resumable state), small enough to read the whole compression step on screen. Point that out explicitly so nobody walks away thinking SHA-256 itself is "toy". Verifier B in the sim previews next week's fix (nested hash / HMAC) — don't over-explain it here, just let them see it hold.  -->

---

## CWE-290: this IS authentication bypass by spoofing

- The server's `/admin` check: does `sig` match AND does `data` contain `admin=true`?
- Forged cookie satisfies **both** — without ever learning `MAC_SECRET`
- The server can't tell "legitimately signed" from "resumed from a leaked digest"

<!-- Land the CWE mapping explicitly (README's "Analogous CWE" line): CWE-347 is the broken verification design, CWE-290 is what it enables — spoofed authentication. Same bug, two angles graders may ask about.  -->

---

## The fix: HMAC's nested construction

```
HMAC(key, msg) = H( (key⊕opad) ‖ H( (key⊕ipad) ‖ msg ) )
```

- **Inner hash** processes `key⊕ipad ‖ msg` → produces an intermediate digest
- **Outer hash** re-hashes that digest *with a fresh key-derived prefix* — a brand-new Merkle-Damgard chain
- The final outer SHA-256 digest **can** be extended, but the result is not a valid HMAC
- A valid outer input is the key-derived prefix plus **one fixed-size inner digest**
- Extending the outer input adds bytes after that digest; it does not authenticate a new message

<!-- The construction that closes the door. Key point: HMAC isn't "hash the key and the message harder" — it's TWO hashes composed so the inner message-hash state is hidden and extending the outer digest produces the wrong input format. RFC 2104.  -->

---

## Fixed vs. vulnerable — one line differs

```python
# vulnerable_app.py
sig = hashlib.sha256(MAC_SECRET.encode() + data).hexdigest()

# fixed_app.py
sig = hmac.new(MAC_SECRET.encode(), data, hashlib.sha256).hexdigest()
```

- Same secret, same data, same SHA-256 — only the construction changed
- Length-extension against `:8093` (HMAC) → **rejected, 403, no flag**

<!-- Make it concrete: this is the literal diff in the two lab apps. Ask students to spot it before you highlight it. This empirically proves HMAC ≠ "hash with a key stuck on" — same exploit script, different outcome.  -->

---

## One fix doesn't fix everything

```python
if sig != expected:      # plain string comparison — in BOTH apps
    return jsonify({"error": "bad signature"}), 403
```

- HMAC defeats length-extension — it does **not** make `!=` constant-time
- Byte-by-byte early-exit comparison leaks timing information → an attacker can recover the tag one byte at a time
- Real fix: `hmac.compare_digest()` (constant-time by design)

<!-- Source Q4. Important: both vulnerable_app.py and fixed_app.py leave this in on purpose, so students learn "the HMAC fix and the constant-time fix are two SEPARATE problems." Don't let them conflate the two.  -->

---

## MACs alone don't stop everything else

- A valid `(data, sig)` pair can be **replayed** later — MAC says nothing about *when*
- Separate **tag collisions** (about `2^32` samples for 64 bits) from **new-message forgery**
- For an ideal 64-bit tag, `q` guessing attempts succeed with probability about `q / 2^64`;
  a collision among already-tagged messages is not automatically a forgery
- Today's fix is length-extension only — a secure cookie design needs more (nonces/timestamps, tag length, comparison)

<!-- Quick, don't over-invest — this previews worksheet Q3/Q6 material without turning into a full lecture. The point: "HMAC fixed" is not the same as "cookie secure."  -->

---

## 🔓 Game — Forge the Admin Cookie

| Service | Port | Scheme | Length-extension? |
|---|---|---|---|
| `vulnerable_app.py` | `:8092` | `SHA256(MAC_SECRET + data)` | **Yes** |
| `fixed_app.py` | `:8093` | `HMAC-SHA256(MAC_SECRET, data)` | **No** |

1. Log in as `guest` on `:8092`, capture `(data, sig)`
2. Forge `&admin=true` appended, via length-extension — no `MAC_SECRET` needed
3. Cash in at `/admin` → flag
4. Replay the same trick against `:8093` → must be rejected

<!-- Explain the game before lab. This is the payoff of the whole lecture — forging your way in with pure math feels like a magic trick until HMAC slams the door. Walk through the flow once on the board before they touch a terminal.  -->

---

## Lab today

- **Common 60:** Capture a guest cookie, calculate glue padding and demonstrate the intended SHA-256 length-extension forgery.
- Compare the control/fixed case, explain its limits, and capture your own evidence.
- **Conventional 40:** the original written questions, if assigned.
- **AIR-Sec 40:** Audit the AI 20 + EiPE 10 + Prompt Problem 10, if assigned.
- Finish the detailed write-up after class; submit the PDF per SUBMISSION.md.
- Viva is formative/authenticity feedback within the rubric, with no separate points.

<!-- Preserve every worksheet question; students submit the common work and only their
assigned format. Shared demo flags are acceptable if no personal configuration is supplied. -->

---

## Key takeaways

- SHA-256 is textbook-sound — the *misuse* (`H(secret ‖ data)`) is what breaks
- Length-extension resumes hash state the attacker was never supposed to see
- HMAC's nested construction fixes this — but doesn't fix comparison timing or replay

<!-- Recap, 3 lines. Cold-call: "why does resuming SHA-256's internal state let you forge a MAC, and why does extending HMAC's outer hash fail to produce a valid tag for a new message?"  -->

---

# Questions?
Next week: AES — CBC bit-flipping and why unauthenticated encryption fails

<!-- Cliffhanger: "Next week you flip bytes in ciphertext you can't even read — and walk in as admin." Remind: same Docker-first setup, new pair of targets. -->
