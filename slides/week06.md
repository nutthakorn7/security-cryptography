---
marp: true
theme: default
paginate: true
header: "Security & Cryptography · Week 6"
---

# Week 6
## Authenticated Encryption / AEAD (the CBC padding oracle)
Security & Cryptography · Nutthakorn Chalaemwongwan

<!-- Hook: ask "if I encrypt something with AES, is it safe?" Let them say yes. Then: "I'm going to decrypt this ciphertext in front of you — without the key — using nothing but a web server that answers yes/no." Today's spine: a mathematically sound cipher (AES-CBC), combined wrong with a MAC (or with no MAC at all), fails in a very specific, very real way. ~2 min. -->

---

## Today

- What **AEAD** guarantees, in one primitive (RFC 5116)
- Encrypt-then-MAC vs the two fragile alternatives
- Why unauthenticated CBC + a padding check = a **padding oracle**
- Why **AES-GCM** has no equivalent hole
- 🔓 Game: **Read the Secret Without the Key**

<!-- Roadmap, 1 min. Flag the lab up front: two live Flask targets, same secret, different cipher — one falls to a byte-by-byte decryption attack, one doesn't. This is the capstone of the symmetric block: Week 3 (MAC) + Week 4 (AES-CBC) combined. -->

---

## Recap — Week 5

- Diffie–Hellman gives Alice & Bob a shared secret no *eavesdropper* can compute
- But raw DH authenticates **nobody** — an *active* attacker (`relay`) ran two independent handshakes and sat invisibly in the middle
- Fix: authenticate the exchange (HMAC over the public keys) — one added check closed it, no crypto swapped

<!-- Bridge from W5. W5 = a sound primitive (DH) with a missing guarantee (identity). W6 = the same shape of failure: a sound primitive (AES) combined with a missing guarantee (integrity/authenticity). Ask: "what guarantee did DH not give you?" (authentication) then pivot: "what guarantee does plain CBC not give you?" (the answer today: integrity). ~3 min. -->

---

## What is AEAD?

**A**uthenticated **E**ncryption with **A**ssociated **D**ata — three guarantees, one primitive:

| Guarantee | Stops |
|---|---|
| **Confidentiality** | eavesdropping — ciphertext reveals nothing about plaintext |
| **Integrity** | undetected tampering — any bit-flip is caught |
| **Authenticity** | forgery — only a key-holder could have produced this ciphertext |

<!-- Anchor to RFC 5116, the AEAD interface spec. Stress "one primitive, one call" — you don't assemble it yourself from a cipher + a MAC by hand, because (as today shows) that's exactly where it goes wrong. AES-GCM and ChaCha20-Poly1305 are AEAD ciphers; plain AES-CBC is NOT — it only gives you the first row. ~8 min. -->

---

## Safe composition: how NOT to build it yourself

- **Encrypt-then-MAC (EtM)** — MAC over the *ciphertext*, verified **before** decryption is even attempted. The *provably safe* generic composition.
- **MAC-then-Encrypt (MtE)** — MAC over plaintext, then encrypt the (plaintext‖MAC). Verifier must **decrypt first** — old TLS CBC cipher suites did this.
- **Encrypt-and-MAC (E&M)** — MAC over plaintext, sent alongside ciphertext (legacy SSH). MAC itself can leak plaintext info.

> If the verifier has to touch the plaintext *before* the MAC check passes, you have a problem.

<!-- Q2 on the worksheet is exactly this. The rule to land: verify BEFORE you decrypt. MtE is the trap — "decrypt, then check padding, then check the MAC" means an attacker's malformed ciphertext gets processed (and can error out differently) before authentication ever happens. That processing gap is where today's whole attack lives. ~10 min. -->

---

## Bridge: CBC is malleable (Week 4, recap)

CBC decryption: **P_i = D(C_i) ⊕ C_{i-1}**

- Flip a bit in ciphertext block **C_{i-1}** → the *same bit* flips in plaintext block **P_i**
- No MAC, no signature — nothing stops the attacker from tampering
- Week 4: bit-flipping. **Today: malleability weaponized into full decryption.**

<!-- Make them re-derive the XOR relation on the board. This is not new material — it's the Week 4 fact that makes today possible. The one-sentence bridge: "malleability means an attacker can change ciphertext and predictably change plaintext; a padding oracle means the attacker can also SEE (indirectly) what plaintext they produced." ~8 min. -->

---

## The vulnerability: a padding oracle

`vulnerable_app.py` — unauthenticated AES-256-CBC, `POST /decrypt`:

```python
if pkcs7_valid(plaintext):
    return jsonify({"status": "ok"}), 200
return jsonify({"error": "bad padding"}), 403
```

- The endpoint **never returns the plaintext**
- But `200` vs `403` is a **distinguishable signal** — that's the oracle
- "We don't leak the plaintext" is not the same as "we leak nothing"

<!-- This is the exact code from vulnerable_app.py — point at the two return lines. Task 0 on the worksheet asks students to find this exact branch. The trap they must unlearn: developers think "as long as I don't print the plaintext, I'm safe." Ask: "what does a 200 actually tell an attacker?" ~10 min. -->

---

## The attack: byte-by-byte, without the key

Attacker submits a **forged previous block** + the real last block as a fake `IV‖ct`:

- Server computes `P = D(C_t) ⊕ forged_prev`, checks only: is `P`'s padding valid?
- Try every `forged_prev[15]` until the server says `200` → last byte of `P` is (almost always) `0x01`
- **`D(C_t)[15] = winning_guess ⊕ 0x01`** — one byte of the *intermediate value*, per query
- Repeat forcing `…0x02 0x02`, `…0x03 0x03 0x03`, … → recover the whole block
- False-positive case (`P` ends `…0x02 0x02` by accident) → re-query a neighbour byte to disambiguate

<!-- The core mechanic — Worksheet Task 2 walks this exact derivation. Write the formula on the board: D(C_t)[15] = winning_guess XOR 0x01. Stress: the attacker NEVER learns the AES key or D(C_t) directly for other purposes — only enough per-block algebra to peel off one plaintext byte per ~256 queries, with zero crypto library needed on the attacker side (exploit.py only uses `requests`). ~12 min. -->

---

## The fix: AES-GCM has no padding to probe

`fixed_app.py` — AES-256-GCM, `POST /decrypt`:

```python
try:
    _aesgcm.decrypt(nonce, ct_and_tag, None)   # raises on ANY tamper
except Exception:
    return jsonify({"error": "decryption failed"}), 403   # uniform, always
return jsonify({"status": "ok"}), 200
```

- **No padding** — GCM is a *stream* mode (CTR-based); there's no "valid vs invalid padding" question to ask
- The **128-bit tag is checked first** — no plaintext is released until it passes
- Every failure — bad base64, wrong length, bad nonce, forged tag — returns the **identical** `403`

<!-- Two independent reasons, and Q4 asks for both separately: (1) what mode it is — no padding step at all; (2) ordering — tag verified before plaintext ever touches application logic. The uniform-403 line IS the teaching point: one error code for every failure kills the signal, full stop. ~10 min. -->

---

## Associated data — the "AD" in AEAD

- Data you want **authenticated but NOT encrypted** — stays readable, but tamper-evident
- Example: a protocol header, sequence number, or recipient/context field a router needs to read
- If that data is left **unauthenticated**, an attacker can splice a valid ciphertext onto a *different* header — a context-confusion forgery, even though the ciphertext itself is untouched

<!-- Worksheet Q5. Keep it concrete: "why would you ever want something NOT encrypted but still tamper-proof?" — routing info, a TLS record type, a database row's key. AEAD APIs (AES-GCM included) take an explicit AD parameter for exactly this. ~6 min. -->

---

## This is not a toy bug

- **CWE-347** — Improper Verification of Cryptographic Signature *(the tag/MAC isn't checked first)*
- **CWE-757** — Selection of Less-Secure Algorithm *(unauthenticated CBC where AEAD belongs)*
- **CWE-208** — Observable Timing/Response Discrepancy *(the 200-vs-403 side channel itself)*
- Real CVEs, not hypothetical: **POODLE** (2014, SSLv3 CBC padding oracle), **Lucky-13** (TLS CBC timing variant) — deployed in production TLS for over a decade

<!-- Ground it — this isn't a contrived classroom bug, it broke real HTTPS. Vaudenay's 2002 paper started it; POODLE forced SSLv3's retirement industry-wide. Ask: "why did it take over a decade to fully stamp out CBC-mode padding oracles in TLS?" (answer: MtE was baked into cipher suite design; the real fix was migrating to AEAD suites.) ~6 min. -->

---

## 🔓 Game — "Read the Secret Without the Key"

- Two live targets, same secret (contains your flag): `:8098` = AES-CBC (vulnerable), `:8099` = AES-GCM (fixed)
- Attacker only ever sees `200`/`403` from `/decrypt` — never the plaintext, never the key
- Run the padding-oracle attack on `:8098` → recover `msg:FLAG{...}` byte by byte
- Run the **identical** attack on `:8099` → zero usable signal, nothing recovered — AEAD holds

<!-- This is the signature game AND the exploit — this is a LAB week. Sell it before lab: "you will decrypt a secret you were never given, without ever knowing the key, using only yes/no answers." Then immediately deflate: run it again against the fixed app and watch it get nothing. Same code, same attacker, opposite outcome — that contrast IS the lesson. ~5 min. -->

---

## Lab today

> 📋 **Worksheet 6** — `labs/week06-aead/worksheet.md` · **kickoff:** `docker compose up -d` (`:8098` CBC, `:8099` GCM) → `python exploit.py`

- Tasks 0–5: read the oracle branch, capture ciphertext, derive `D(C_t)[15] = guess ⊕ 0x01`, recover the flag, confirm GCM gets no signal
- **Deliverable:** recovered flag + which byte you forced to `0x01`/`0x02 0x02` and why
- **+ Audit the AI** (a "safe" decrypt endpoint that reintroduces the oracle via `400`/`422`/`200`), **EiPE**, **Prompt Problem**
- Part 2: 8 conventional written questions (Q1–Q8), no AI-resilience layer — answer yourself

<!-- Point at worksheet.md directly, walk the task list once. Flag the Audit-the-AI trap specifically: the AI's answer LOOKS careful (validates padding, validates format) but the 400-vs-422-vs-200 split is a THREE-way oracle, worse than the original two-way one. Remind: per-student flag via seed_flags.py env override. ~5 min. -->

---

## Key takeaways

- **Textbook-secure primitive, real-system failure:** AES-CBC is a fine cipher — "AES-CBC + tell me if the padding failed" is not
- The fix isn't hiding the error message — it's **composing correctly** (encrypt-then-MAC) or reaching for a real **AEAD** cipher (AES-GCM)
- Any distinguishable response to an attacker-controlled input is a potential oracle — ask what your error codes reveal

<!-- Recap, 3 lines, cold-call: "if EtM is provably safe, why does anyone still get this wrong?" (answer: it's easy to bolt a MAC on AFTER decrypting, because that's the order the data naturally flows through your code — you have to deliberately verify first.) ~3 min. -->

---

# Questions?
Next week: Review — consolidating Weeks 1–6 before the midterm

<!-- Cliffhanger/logistics: Week 7 is the review week for the pre-midterm block (hashing → MACs → AES modes → key exchange → AEAD). Tell them to bring their padding-oracle formula and the EtM/MtE/E&M comparison — both are fair game. -->
