---
marp: true
theme: default
paginate: true
header: "Security & Cryptography · Week 10"
---

# Week 10
## Asymmetric & Hybrid Encryption
Security & Cryptography · Nutthakorn Chalaemwongwan

<!-- Hook: ask "if RSA can encrypt anything, why does every real system — TLS, Signal, age, PGP — bolt AES onto it instead of just using RSA?" Let them guess before you answer. Today = why hybrid encryption exists, then an implementation that gets every primitive right and is still broken. ~2 min. -->

---

## Today

- Why asymmetric encryption alone can't encrypt bulk data
- Hybrid encryption: wrap a symmetric key once, encrypt many messages
- Asymmetric key exchange (ECDH) → ECIES as a concrete hybrid scheme
- 🔬 Game: **Nonce Detective** — audit an AI-generated hybrid implementation

<!-- Roadmap, 1 min. Flag up front: no Docker target this week — it's a conceptual week, hands-on core is the Audit-the-AI exercise (Worksheet 10, Part 3). Same category as Week 1. -->

---

## Recap — Week 6

- **AEAD** (AES-GCM) = confidentiality + integrity + authenticity in *one* primitive
- It closed the padding-oracle hole in unauthenticated CBC — no padding step, tag checked before any plaintext is released
- Today: AES-GCM shows up again — genuinely correct, and still breakable
- Same spine, new victim: even the primitive that *fixed* last week's failure has its own misuse mode

<!-- Bridge from W6. Cold-call: "what made GCM immune to the padding oracle?" (no padding step; tag verified first). Today we show that immunity doesn't mean "unbreakable" — it means "immune to that specific attack." ~3 min. -->

---

## Why not just use RSA for everything?

- RSA operations are orders of magnitude slower than AES for bulk data
- RSA-4096-OAEP: roughly a **470-byte plaintext ceiling** — can't fit a photo, let alone a video
- OAEP padding eats further into the usable message size
- **The fix isn't "use a bigger RSA key"** — it's "use RSA for something small"

<!-- Worksheet Q1. Ask: "what's the biggest thing you could RSA-encrypt directly?" Answer: nowhere near a file. Get them to the idea themselves before naming hybrid encryption. ~6 min. -->

---

## Hybrid encryption: wrap once, encrypt many

1. Bob generates a fresh AES-256 session key (CSPRNG)
2. Bob wraps it with Alice's RSA public key (OAEP) — sent **once**
3. Bob encrypts every message with AES-GCM under that session key
4. Alice unwraps the session key with her RSA private key — **once**
5. Alice decrypts every GCM ciphertext with the unwrapped key

> Pay RSA's cost once per session, not once per message.

<!-- Worksheet Q2. Draw this as a numbered diagram on the board — Bob's side, the wire, Alice's side. Point out it's exactly how TLS's handshake works: asymmetric once, symmetric for the bulk. ~8 min. -->

---

## Public-key encryption in one slide

- Alice publishes her **public** key; keeps the **private** key secret
- Bob encrypts to Alice's public key — anyone can do this, it's public
- Only the matching private key can invert the trapdoor function
- Alice never has to share a secret with Bob in advance — that's the whole point over symmetric crypto

<!-- Worksheet Q3. Keep this short — it's foundational review, not new. Ask: "why can Bob encrypt but not decrypt his own ciphertext?" (he doesn't have Alice's private key either). ~6 min. -->

---

## Asymmetric key exchange

- Alice and Bob each generate an ephemeral elliptic-curve key pair
- They exchange **public** keys over the open channel
- Each combines their own private key with the other's public key → the *same* shared secret on both sides
- An eavesdropper who sees both public keys cannot compute it (discrete-log hardness on the curve)

<!-- Worksheet Q4. This is Diffie-Hellman, elliptic-curve flavor (ECDH) — connect back to Week 5's key-exchange lab if it's still fresh for them. The magic: two public values combine into a secret neither public value reveals. ~8 min. -->

---

## ECIES: hybrid encryption on ECDH

- Sender generates an ephemeral EC key pair, runs ECDH against the recipient's public key
- Shared secret → **KDF** (e.g. HKDF) → symmetric key — never the raw ECDH output used directly
- Symmetric key encrypts the message with an AEAD cipher (AES-GCM / ChaCha20-Poly1305)
- Ephemeral public key + nonce travel with the ciphertext, in the clear
- No symmetric key is ever transmitted — Bob and Alice each *derive* it independently

<!-- Worksheet Q5. Point out this is the same shape as the RSA hybrid pattern, just with ECDH standing in for RSA-OAEP as the "key delivery" step. This slide doubles as their checklist for the Part 4B Prompt Problem later. ~8 min. -->

---

## A shallow review would stop here

A teammate's AI assistant wrote a Bob-to-Alice hybrid encryption module. A quick review checks:

- Real algorithm, not textbook RSA? Uses **RSA-OAEP**. ✅
- Symmetric key strong and CSPRNG-generated? **AES-256**, `os.urandom`-backed. ✅
- Authenticated, not plain CBC/ECB? **AES-GCM**. ✅
- Tag actually checked on decrypt, not ignored? ✅

It runs. The round trip succeeds. Alice decrypts everything Bob sends. **Approved — right?**

<!-- Set up the trap explicitly: every box a rushed reviewer checks is genuinely checked-off correct here. That's deliberate — the point of the exercise is that "right primitives" is necessary but not sufficient. Ask: "what would you check next, if anything?" ~5 min. -->

---

## The failure mode: nonce reuse under GCM

- AES-GCM needs a **nonce** — a value that must never repeat under the same key
- NIST SP 800-38D §8.2: the (key, nonce) pair must be **unique for every message**
- The failure shape to hunt for: a nonce that's a **fixed constant**, or derived from something that isn't actually unique per call, reused silently across an entire session

```python
# illustrative shape of the bug — not the exact lab code
nonce = FIXED_VALUE                       # same nonce, every call
ciphertext = aesgcm.encrypt(nonce, plaintext, aad)
```

- **CWE-323** — Reusing a Nonce, Key Pair in Encryption

<!-- This is genuinely new content, not the lab spoiler — teach the general shape of the bug (LLMs love a "clean," fixed nonce because it looks tidy), not the specific file's line. NIST's own wording is the authority here: "unique," not "random," is the requirement. ~6 min. -->

---

## The break: what a passive eavesdropper gets

- GCM's keystream depends only on **(key, nonce)** — same pair twice ⇒ same keystream
- `C1 = P1 ⊕ KS` and `C2 = P2 ⊕ KS` ⇒ **`C1 ⊕ C2 = P1 ⊕ P2`**
- No key needed, no interaction with Bob or Alice — just two intercepted ciphertexts, XORed
- Any crib — a known word, a predictable header, language redundancy — peels apart both plaintexts

<!-- Walk the algebra on the board slowly — this is the "aha" the lab is built around. Ask: "does the attacker need to break RSA to do this?" (no — RSA-OAEP is never touched; the break is entirely downstream of the key). ~8 min. -->

---

## Worse: it's not just confidentiality

- Week 6's padding oracle needed an **active** attacker — send a query, read 200 vs 403, repeat
- Nonce reuse needs only a **passive** eavesdropper — two recorded messages, zero interaction
- Reuse under GCM specifically also leaks the **authentication subkey** (Joux, 2006 — "the forbidden attack")
- Recover that subkey and you can **forge valid tags** on messages nobody sent — both of GCM's guarantees fail from one mistake

<!-- Contrast attacker models explicitly with Week 6: active oracle vs passive eavesdropper is a big jump in how easy the attack is to mount in the real world. The forbidden-attack citation is in this week's README references — mention it exists, don't derive GHASH algebra live unless the class is ready for it. ~6 min. -->

---

## The fix — general principle

- Never reuse a (key, nonce) pair — give **every message** its own nonce
- Two standard disciplines: a fresh CSPRNG-random 96-bit nonce per message, **or** a monotonic counter — pick one, don't mix
- The nonce isn't secret — it travels with the ciphertext, in the clear
- Untouched: RSA key size, OAEP padding, the AES-256 session key, per-session key wrapping
- The bug lives in nonce *discipline*, not in any primitive — the fix stays local to the encrypt call

<!-- Tie to the lab's own constraint: the fix must NOT re-wrap the key per message (that defeats hybrid encryption's whole point). Ask: "why doesn't this fix touch the RSA/OAEP code at all?" — get them to say it out loud before the lab. ~6 min. -->

---

## 🔬 Signature game — Nonce Detective

- You're handed a hybrid-encryption implementation that looks textbook-correct — proper RSA-OAEP, proper AES-GCM, nothing wrong at a skim
- Find the one planted bug — then **prove** it: recover leaked plaintext from two intercepted messages, not just point at a line
- It passes every "did they use the right primitives" checklist — the only way to catch it is to think like an attacker

<!-- Explain the game before lab, don't demo the answer. The whole exercise is designed so a checklist review passes it — emphasize that "it runs and round-trips" is not evidence of security. The payoff is real: a genuine "aha" when the recovered plaintext prints. ~4 min. -->

---

## Lab today

> 📋 **Worksheet 10** — `labs/week10-hybrid-encryption/worksheet.md` (Parts 1–5) · start at `audit_the_ai/README.md`

- Part 2 — 5 essay questions: bulk-data limits, hybrid encryption flow, public-key encryption, key exchange, ECIES
- Part 3 (required) — **Audit-the-AI**: find the planted bug in `broken_hybrid_encrypt.py`, write a proof script recovering real leaked plaintext, explain the attack, submit `fixed_hybrid_encrypt.py`
- Part 4 — EiPE (explain hybrid encryption, no jargon) + Prompt Problem (ask an AI to implement ECIES, critique its output against a checklist)
- Part 5 — live viva spot-check, no notes
- No Docker target, no flag — conceptual week, graded on your written reasoning and proof script

<!-- Point them straight at audit_the_ai/README.md — it has the full task + hints (checks the RSA/OAEP fundamentals are fine, then says "look at the nonce"). Python-only, standard library + cryptography package, no environment setup needed. ~4 min. -->

---

## Key takeaways

- **Textbook-secure primitive, real-system failure** — this week it's AEAD's turn
- RSA-OAEP correct + AES-256 correct + AES-GCM correct **does not** imply a secure system
- One reused nonce breaks *both* confidentiality and authenticity of GCM — and needs only a passive eavesdropper
- "Did they use the right primitives?" is necessary — it is never sufficient. AI-generated crypto code needs the same scrutiny as any other AI-generated code

<!-- Recap, cold-call: "name the one thing this week's broken code got wrong, given everything else was right." Land the course spine explicitly — this is the throughline for the whole term. ~3 min. -->

---

# Questions?
Next week: Digital Signatures & Zero-Knowledge Proofs

<!-- Cliffhanger: "next week you prove you know a secret — without ever revealing it." Remind: worksheet + audit_the_ai/ due per Classroom deadline; disclose any AI assistance on Part 1 of the worksheet. ~1 min. -->
