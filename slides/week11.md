---
marp: true
theme: default
paginate: true
header: "Security & Cryptography · Week 11"
---

# Week 11
## Digital Signatures & Zero-Knowledge Proofs (ECDSA Signature Malleability)
Security & Cryptography · Nutthakorn Chalaemwongwan

<!-- Hook: ask "if I hand you a signature `(r, s)` that verifies True, can you produce a SECOND, DIFFERENT-looking valid signature for the exact same message and key, with no idea what the private key is?" Answer: yes, for ECDSA, in one line of arithmetic. That's today. Title note: the objective/README call this "signature malleability," not nonce reuse (nonce reuse is a different, key-recovery bug) — say that distinction out loud up front so students don't conflate the two ECDSA pitfalls. ~2 min. -->

---

## Today

- Signatures vs. MACs; a signature as a **non-interactive ZKP**
- RSA vs. ECDSA vs. EdDSA — sound math, fragile implementations
- **ECDSA signature malleability**: `(r, s)` has a valid twin `(r, n−s)`
- The fix: **low-S / BIP-62** normalization
- 🔓 Game: **Double-Spend the Bank**

<!-- Roadmap, 1 min. Flag the lab up front: two Flask banks (:8102 vulnerable, :8103 fixed), same math bug, different acceptance rule. Students will double-spend a fake withdrawal, then prove the fix closes it. -->

---

## Recap — Week 10

- Asymmetric crypto (RSA/ECC) solves key-distribution — but is slow
- **Hybrid encryption**: use asymmetric to wrap a fast symmetric key (KEM/DEM)
- Same spine as always: textbook-sound primitive, real systems still misuse it

<!-- Bridge from W10. W10 = encryption (confidentiality) using asymmetric keys. W11 = the OTHER thing asymmetric keys do — prove authenticity via signatures — and its own way of getting misused. Ask: "encryption answers 'can only you read this'; what question does a signature answer?" (answer: "did you write this, and can anyone check?"). ~2 min. -->

---

## Signatures vs. MACs

| | **MAC** | **Digital signature** |
|---|---|---|
| Create with | shared secret key | **private** key |
| Verify with | *same* shared key | **public** key |
| Who can verify? | only key-holders | **anyone** with the public key |

**Why this matters for PKI:** a signature lets a stranger who never met you verify your claim — a MAC can't, because verifying it requires the same secret that created it.

<!-- Ties to worksheet Q1. Ask: "why can't a MAC secure HTTPS certificates?" (a CA can't share its signing key with every browser — that key would leak instantly). Signatures = asymmetric trust at scale; MACs = symmetric trust between two parties who already share a secret. ~5 min. -->

---

## A signature is a zero-knowledge proof

**Schnorr identification protocol** — Peggy proves she knows secret `x` (her private key) without revealing it:

1. Peggy sends a **commitment** (a random value derived from a fresh secret)
2. Victor sends a random **challenge**
3. Peggy answers with a **response** that only the holder of `x` could compute correctly

Victor is convinced Peggy knows `x` — but learns nothing about `x` itself, and a recorded transcript is useless to replay (next time the challenge is different).

<!-- Worksheet Q2 / EiPE task. Draw it as three arrows on the board: commit → challenge → response. Stress *why* it's zero-knowledge: a fresh random challenge each run means Peggy must genuinely know the secret to answer correctly every time — but Victor never sees the secret, and can't reuse the transcript to impersonate Peggy later. ~6 min. -->

---

## Fiat–Shamir: turning the proof into a signature

- Problem: Schnorr needs Victor **live**, sending a fresh challenge
- Fiat–Shamir trick: replace Victor's random challenge with `hash(commitment, message)`
- Now Peggy can compute the whole proof **alone**, offline, and attach it to a message

**Result: a digital signature *is* a non-interactive zero-knowledge proof of knowledge of the private key.** EdDSA (Ed25519) is literally this — a Fiat–Shamir transform of Schnorr. ECDSA (DSA family) is *also* a NIZK proof of knowledge of the private key, but **not** a literal Fiat–Shamir/Schnorr construction (its hash covers only the message, not the commitment).

<!-- Worksheet Q2(b)(c). The "aha": hashing removes the live verifier because a hash is unpredictable *and* bound to the message — nobody can pre-compute a fake response before knowing what they're "committing" to. This is the conceptual bridge from ZKP theory to the ECDSA math on the next two slides. ~5 min. -->

---

## RSA vs. ECDSA vs. EdDSA

| | **RSA** | **ECDSA** | **EdDSA (Ed25519)** |
|---|---|---|---|
| Hardness | integer factoring | elliptic-curve discrete log | elliptic-curve discrete log |
| Easy to implement correctly? | padding choices are a minefield (CWE-347-adjacent) | **fragile** — needs a unique, unpredictable nonce `k` every time | deterministic nonce — no `k` to get wrong |
| Known pitfall | e.g. PKCS#1 v1.5 padding oracles | reused/predictable `k` **leaks the private key** | signature malleability closed by construction |

**Why EdDSA is recommended today:** it removes the human/implementation decision points (`k` generation, encoding) that make RSA and ECDSA go wrong in practice.

<!-- Worksheet Q3. Name-drop the Sony PS3 disaster (reused ECDSA `k` → recovered the signing key) as the nonce-reuse pitfall — then say clearly: "that is NOT today's bug." Today's ECDSA problem lives one level up: even with a perfectly random, never-reused `k`, the *signature encoding itself* isn't unique. That's malleability, coming up next. ~5 min. -->

---

## Inside an ECDSA signature

- Signer picks a fresh random nonce `k`, computes point `R = k·G`, and lets `r = R.x mod n`
- Computes `s = k⁻¹ (hash(msg) + r·privkey) mod n`
- Signature = the pair **`(r, s)`**; `n` = the curve's group order (SECP256k1 here)
- Verification checks an equation built from `r`, `s`, the message hash, and the public key

This math is textbook-sound: nobody can forge `(r, s)` without the private key. **But nothing here says `(r, s)` is the *only* valid pair for this message.**

<!-- Set up the punchline deliberately — don't give away the twin yet. Ask: "the verification equation uses `s` — does it use `s` directly, or `s` squared, or `s` combined some other way?" (It only ever appears via `s⁻¹` inside the equation, and `s⁻¹` and `(n−s)⁻¹` turn out to satisfy the SAME check with a sign flip.) Draw the equation if the class is math-comfortable; otherwise just flag "watch what happens to `s`." ~5 min. -->

---

## The break: signature malleability

**Every valid ECDSA signature `(r, s)` has a valid twin `(r, n − s)`** — same message, same key, verifies True, but *different bytes*.

- **CWE-347** — Improper Verification of Cryptographic Signature
- **CWE-345** — Insufficient Verification of Data Authenticity
- Textbook-secure primitive: unforgeable. Real-system failure: **not unique**.

```python
n = ecdsa.SECP256k1.order
s_twin = n - s      # a second, different, still-valid signature
```

<!-- The core lesson slide — say the spine line explicitly: "textbook-secure primitive, real-system failure." ECDSA is not broken as a signature scheme (EUF-CMA holds — nobody can forge a signature on a NEW message). The failure is a system-design assumption: someone assumed "a valid signature" implies "a unique identifier." ~6 min. -->

---

## Where it bites: dedup by signature hash

A bank authorizes **one** withdrawal, signed with ECDSA. To stop double-processing, it computes a transaction id from the signature:

```python
txid = sha256(str(r) + str(s))          # vulnerable_app.py
if txid in seen: reject()
seen.add(txid); process(withdrawal)
```

`(r, s)` and `(r, n−s)` are the *same authorization* mathematically — but hash to **two different txids**. Submit both → the bank processes it **twice**.

<!-- This is exactly `vulnerable_app.py`'s `txid_of`/`withdraw` — the line students must quote in Lab Task 0. Point out: it isn't that the signature verification is broken — every check passes. It's that `sha256(r,s)` was the WRONG thing to treat as a unique transaction identity. Ask: "what should the txid have been derived from instead?" (message + pubkey, or an app-level nonce). ~6 min. -->

---

## Case study: MtGox

- 2014: the largest Bitcoin exchange at the time collapsed, citing ~850,000 BTC "missing"
- Part of the claimed mechanism: attackers **mutated transaction signatures** so a transaction's id changed, making it *look* like a withdrawal hadn't gone through
- Exchange software that tracked transactions by a **malleable id** reissued/duplicated payouts
- Bitcoin's own response: **BIP-62 / BIP-146** — standardize a single canonical (low-S) signature per transaction

<!-- Worksheet Q5(b). Keep it honest: malleability was one contributing factor among several claimed for MtGox (accounting bugs, alleged theft) — don't overstate it as "the sole cause," but it IS a real, historically significant instance of exactly this bug class. This is why the lab's dedup-by-signature-hash bank is not a contrived toy — it's a simplified, runnable replay of a real incident's root cause. ~4 min. -->

---

## SUF-CMA vs. EUF-CMA

- **EUF-CMA** (existential unforgeability): attacker cannot produce a valid signature on any **new message**. ECDSA satisfies this.
- **SUF-CMA** (*strong* unforgeability): attacker cannot produce **any new valid signature** either — not even a different encoding of an *already-signed* message.
- Malleability is exactly an EUF-CMA-safe, **SUF-CMA-violating** scheme: same message, new valid signature bytes.

**Lesson: if your system's security depends on signatures being unique, you need SUF-CMA — EUF-CMA alone is not enough.**

<!-- Worksheet Q5(c). This is the precise theoretical name for the bug — write both acronyms on the board and have students say back which one the vulnerable bank silently assumed (SUF-CMA) versus which one ECDSA actually promises (EUF-CMA only). This is also why EdDSA/Ed25519, which IS SUF-CMA-secure by construction (unique canonical `S`), sidesteps this entire class. ~5 min. -->

---

## The fix: low-S / BIP-62

`fixed_app.py` adds one check **before** dedup:

```python
def is_low_s(s, n):
    return s <= n // 2

if not is_low_s(sig_s, n):
    return 403  # "non-canonical signature: s must be <= n/2"
# ...only now compute txid and dedup
```

Exactly one of `{s, n−s}` is ≤ `n/2` — reject the other. Now there is **one** canonical signature per `(message, key)`, so the twin has nowhere to hide.

<!-- Worksheet Task 4. Say plainly: canonicalization, not "better verification," is the fix — the vulnerable app's *signature verification* was never wrong; the *identity* assumption was. Preview the fixed-app subtlety for the next slide: "PASS" ≠ "both rejected." ~5 min. -->

---

## 🔓 Game — Double-Spend the Bank

Two identical Flask banks, one rule apart:

| Bank | Port | Rule | Vulnerable? |
|---|---|---|---|
| `vulnerable_app.py` | `:8102` | dedups by `sha256(r,s)` | **Yes** |
| `fixed_app.py` | `:8103` | rejects high-S first, *then* dedups | No |

1. `GET /sign` → a valid `(r, s)` for `"withdraw 100 to attacker"`
2. `POST /withdraw` with `(r, s)` → processed, `total=100`
3. Compute the twin `(r, n−s)` → `POST` again → processed **again**, `total=200` → **flag** on `:8102`
4. Same sequence on `:8103` → first accepted, twin **403** → no flag (PASS = *not* both-rejected)

<!-- Explain the game before lab, and flag the tricky pass condition explicitly — the fixed bank must still accept the FIRST, legitimate withdrawal; only the malleated twin should be rejected. Students who see "both rejected" and call it a pass have misread the spec. `exploit.py` automates it; Task 2 has them hand-compute `s' = n − s` first so the math isn't a black box. ~3 min. -->

---

## Lab today — Worksheet 11

> 📋 **Worksheet 11** — `labs/week11-signatures-zkp/worksheet.md` · kickoff: `docker compose up -d`

- **Part 1 (essays):** signatures vs. MACs, Schnorr/Fiat–Shamir as ZKP, RSA/ECDSA/EdDSA, substitution attacks, malleability + MtGox + SUF-CMA
- **Part 2 (lab):** capture the flag on `:8102`, confirm the `403` rejection on `:8103`
- **🤖 Audit the AI:** critique a plausible-looking `process()` that dedups by signature hash — same bug, live in front of you
- **🧠 EiPE + Prompt Problem:** explain ZKP in plain English; probe an AI on *why* ECDSA is malleable and EdDSA isn't

<!-- The graded output — mirror the structure students already know from earlier weeks (essays + lab + Audit-the-AI + EiPE/Prompt). Call out that Audit-the-AI is NOT optional here — it's the same flaw as the lab, presented as confident-sounding AI code, and it's worth 20 of 100 points. Point to `docker compose up -d` and remind them both ports publish to localhost, no network-name juggling needed. ~3 min. -->

---

## Key takeaways

- ECDSA's math is sound — unforgeable (**EUF-CMA**) — but not unique (**not SUF-CMA**)
- **Textbook-secure primitive, real-system failure:** the bug was trusting `sha256(r,s)` as an identity, not the signature check itself
- The fix is a **canonicalization rule** (low-S/BIP-62), not "verify harder"

<!-- Recap, 3 lines — say the spine phrase out loud one more time, it's the thread across all 19 weeks. Cold-call: "if I dedup by `(message, pubkey)` instead of `sha256(r,s)`, does the malleability bug still let me double-spend?" (No — that's the other valid defense from Q5(d).) ~2 min. -->

---

# Questions?
Next week: (see course roadmap)

<!-- Close with the viva-style question bank from the worksheet as a preview of what instructors may spot-check live: "point to the one line that decides transaction identity," "which of s or n−s does the fixed bank accept, and why." Remind students the flag is per-student via `FLAG_SIG` — submitting someone else's is a violation. -->
