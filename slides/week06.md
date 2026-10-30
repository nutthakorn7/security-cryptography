---
marp: true
theme: default
paginate: true
header: "Security & Cryptography · Week 6"
---

# Week 6
## Authenticated Encryption / AEAD (the CBC padding oracle)
Security & Cryptography · Nutthakorn Chalaemwongwan

<!-- Hook: ask "if I encrypt something with AES, is it safe?" Let them say yes. Then: "I'm going to decrypt this ciphertext in front of you — without the key — using nothing but a web server that answers yes/no." Today's spine: a mathematically sound cipher (AES-CBC), combined wrong with a MAC (or with no MAC at all), fails in a very specific, very real way.  -->

---

## Today

**100-minute class:** 10 quiz/review · 10 brief · 60 shared practice · 15 debrief · 5 capture.
**Assessment:** common 60 + assigned Conventional written 40 **or** AIR-Sec 20/10/10.
Preparation and detailed write-up are outside the contact block. Week 1 opens with orientation/review.

<!-- The full deck is a teaching/reference bank, not an additional lecture block.
Use the core explanation for the 10-minute brief and just-in-time guidance during practice;
assign the remaining deep dives as preparation or follow-up. Viva is formative, with no
separate points or automatic-zero rule. -->

- What **AEAD** guarantees, in one primitive (RFC 5116)
- Encrypt-then-MAC vs the two fragile alternatives
- Why unauthenticated CBC + a padding check = a **padding oracle**
- Why **AES-GCM** has no equivalent hole
- 🔓 Game: **Read the Secret Without the Key**

<!-- Roadmap,  Flag the lab up front: two live Flask targets, same secret, different cipher — one falls to a byte-by-byte decryption attack, one doesn't. This is the capstone of the symmetric block: Week 3 (MAC) + Week 4 (AES-CBC) combined. -->

---

## Recap — Week 5

- Diffie–Hellman gives Alice & Bob a shared secret no *eavesdropper* can compute
- But raw DH authenticates **nobody** — an *active* attacker (`relay`) ran two independent handshakes and sat invisibly in the middle
- Fix: authenticate the exchange (HMAC over the public keys) — one added check closed it, no crypto swapped

<!-- Bridge from W5. W5 = a sound primitive (DH) with a missing guarantee (identity). W6 = the same shape of failure: a sound primitive (AES) combined with a missing guarantee (integrity/authenticity). Ask: "what guarantee did DH not give you?" (authentication) then pivot: "what guarantee does plain CBC not give you?" (the answer today: integrity).  -->

---

## What is AEAD?

**A**uthenticated **E**ncryption with **A**ssociated **D**ata — three guarantees, one primitive:

| Guarantee | Stops |
|---|---|
| **Confidentiality** | eavesdropping — ciphertext reveals nothing about plaintext |
| **Integrity** | undetected tampering — any bit-flip is caught |
| **Authenticity** | forgery — only a key-holder could have produced this ciphertext |

<!-- Anchor to RFC 5116, the AEAD interface spec. Stress "one primitive, one call" — you don't assemble it yourself from a cipher + a MAC by hand, because (as today shows) that's exactly where it goes wrong. AES-GCM and ChaCha20-Poly1305 are AEAD ciphers; plain AES-CBC is NOT — it only gives you the first row.  -->

---

## Safe composition: how NOT to build it yourself

- **Encrypt-then-MAC (EtM)** — authenticate the ciphertext and relevant IV/metadata with an independent MAC key before decryption, under the construction's standard assumptions.
- **MAC-then-Encrypt (MtE)** — MAC over plaintext, then encrypt the (plaintext‖MAC). Verifier must **decrypt first** — old TLS CBC cipher suites did this.
- **Encrypt-and-MAC (E&M)** — MAC over plaintext, sent alongside ciphertext (legacy SSH). MAC itself can leak plaintext info.

> Never release or act on unauthenticated plaintext. The supplied lab compares CBC with **no MAC** against GCM.

<!-- Q2 on the worksheet is exactly this. The rule to land: do not release or use unauthenticated plaintext; EtM can verify before decryption. MtE is the trap — "decrypt, then check padding, then check the MAC" means an attacker's malformed ciphertext gets processed (and can error out differently) before authentication ever happens. Today's running target is simpler: unauthenticated CBC with no MAC. MtE/E&M are related composition examples, not what this code implements.  -->

---

## Bridge: CBC is malleable (Week 4, recap)

CBC decryption: **P_i = D(C_i) ⊕ C_{i-1}**

- Flip a bit in ciphertext block **C_{i-1}** → the *same bit* flips in plaintext block **P_i**
- No MAC, no signature — nothing stops the attacker from tampering
- Week 4: bit-flipping. **Today: malleability weaponized into full decryption.**

<!-- Make them re-derive the XOR relation on the board. This is not new material — it's the Week 4 fact that makes today possible. The one-sentence bridge: "malleability means an attacker can change ciphertext and predictably change plaintext; a padding oracle means the attacker can also SEE (indirectly) what plaintext they produced."  -->

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

<!-- This is the exact code from vulnerable_app.py — point at the two return lines. Task 0 on the worksheet asks students to find this exact branch. The trap they must unlearn: developers think "as long as I don't print the plaintext, I'm safe." Ask: "what does a 200 actually tell an attacker?"  -->

---

## The attack: byte-by-byte, without the key

Attacker submits a **forged previous block** + the real last block as a fake `IV‖ct`:

- Server computes `P = D(C_t) ⊕ forged_prev`, checks only: is `P`'s padding valid?
- Try every `forged_prev[15]` until the server says `200` → last byte of `P` is (almost always) `0x01`
- **`D(C_t)[15] = winning_guess ⊕ 0x01`** — one byte of the *intermediate value*, after scanning candidate guesses
- A byte usually takes multiple oracle queries; confirm padding to rule out false positives
- Repeat forcing `…0x02 0x02`, `…0x03 0x03 0x03`, … → recover the whole block
- False-positive case (`P` ends `…0x02 0x02` by accident) → re-query a neighbour byte to disambiguate

![Two zones, top to bottom, left to right. Top: the server decrypts an attacker-forged blob by computing D of the ciphertext block XORed with the attacker's forged previous block to get a candidate plaintext, then checks only whether its PKCS-7 padding is valid, returning 200 for valid or 403 for invalid. Bottom: the attacker, who never sees the key or the decrypted plaintext, tries all 256 values for one byte of the forged previous block, finds the single value the server accepts as 200, and from that single accepted guess derives one real byte of the intermediate decrypted value and hence one real byte of the actual plaintext, repeating this to recover the entire secret without ever learning the encryption key.](img/padding-oracle.svg)

<!-- The core mechanic — Worksheet Task 2 walks this exact derivation. Write the formula on the board: D(C_t)[15] = winning_guess XOR 0x01. Stress: the attacker NEVER learns the AES key or D(C_t) directly for other purposes — only enough per-block algebra to peel off one plaintext byte per ~256 queries, with zero crypto library needed on the attacker side (exploit.py only uses `requests`).  -->

```sim
padding-oracle
```

<!-- The sim uses a toy block cipher, not real AES — two rounds of substitute/reverse/substitute, not 14 rounds of SubBytes/ShiftRows/MixColumns — but the SAME CBC relation (P_i = D(C_i) XOR C_{i-1}) and the SAME PKCS#7 check `vulnerable_app.py` runs, so the byte-by-byte recovery is the real algorithm, not a scripted result. Point that out explicitly so nobody walks away thinking real AES is "toy". Oracle B previews today's fix (tag checked before any padding logic exists) — run both live: drag the slider once to land the first byte, then click "Run the full byte-by-byte recovery" and watch Oracle A produce the whole secret while Oracle B stalls at zero bytes recovered.  -->

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

<!-- Two independent reasons, and Q4 asks for both separately: (1) what mode it is — no padding step at all; (2) ordering — tag verified before plaintext ever touches application logic. The uniform-403 line IS the teaching point: one error code for every failure kills the signal, full stop.  -->

---

## Associated data — the "AD" in AEAD

- Data you want **authenticated but NOT encrypted** — stays readable, but tamper-evident
- Example: a protocol header, sequence number, or recipient/context field a router needs to read
- If that data is left **unauthenticated**, an attacker can splice a valid ciphertext onto a *different* header — a context-confusion forgery, even though the ciphertext itself is untouched

<!-- Worksheet Q5. Keep it concrete: "why would you ever want something NOT encrypted but still tamper-proof?" — routing info, a TLS record type, a database row's key. AEAD APIs (AES-GCM included) take an explicit AD parameter for exactly this.  -->

---

## This is not a toy bug

- **CWE-347** — Improper Verification of Cryptographic Signature *(the tag/MAC isn't checked first)*
- **CWE-757** — Selection of Less-Secure Algorithm *(unauthenticated CBC where AEAD belongs)*
- **CWE-208** — Observable Timing/Response Discrepancy *(the 200-vs-403 side channel itself)*
- Real CVEs, not hypothetical: **POODLE** (2014, SSLv3 CBC padding oracle), **Lucky-13** (TLS CBC timing variant) — deployed in production TLS for over a decade

<!-- Ground it — this isn't a contrived classroom bug, it broke real HTTPS. Vaudenay's 2002 paper started it; POODLE forced SSLv3's retirement industry-wide. Ask: "why did it take over a decade to fully stamp out CBC-mode padding oracles in TLS?" (answer: MtE was baked into cipher suite design; the real fix was migrating to AEAD suites.)  -->

---

## 🔓 Game — "Read the Secret Without the Key"

- Two live targets, same secret (contains your flag): `:8098` = AES-CBC (vulnerable), `:8099` = AES-GCM (fixed)
- Attacker only ever sees `200`/`403` from `/decrypt` — never the plaintext, never the key
- Run the padding-oracle attack on `:8098` → recover `msg:FLAG{...}` byte by byte
- Run the **identical** attack on `:8099` → zero usable signal, nothing recovered — AEAD holds

<!-- This is the signature game AND the exploit — this is a LAB week. Sell it before lab: "you will decrypt a secret you were never given, without ever knowing the key, using only yes/no answers." Then immediately deflate: run it again against the fixed app and watch it get nothing. Same code, same attacker, opposite outcome — that contrast IS the lesson.  -->

---

## Lab today

- **Common 60:** Capture the ciphertext, explain one manual oracle query and run the CBC padding-oracle recovery.
- Compare the control/fixed case, explain its limits, and capture your own evidence.
- **Conventional 40:** the original written questions, if assigned.
- **AIR-Sec 40:** Audit the AI 20 + EiPE 10 + Prompt Problem 10, if assigned.
- Finish the detailed write-up after class; submit the PDF per SUBMISSION.md.
- Viva is formative/authenticity feedback within the rubric, with no separate points.

<!-- Preserve every worksheet question; students submit the common work and only their
assigned format. Shared demo flags are acceptable if no personal configuration is supplied. -->

---

## Key takeaways

- **Textbook-secure primitive, real-system failure:** AES-CBC is a fine cipher — "AES-CBC + tell me if the padding failed" is not
- The fix isn't hiding the error message — it's **composing correctly** (encrypt-then-MAC) or reaching for a real **AEAD** cipher (AES-GCM)
- Any distinguishable response to an attacker-controlled input is a potential oracle — ask what your error codes reveal

<!-- Recap, 3 lines, cold-call: "if EtM is provably safe, why does anyone still get this wrong?" (answer: it's easy to bolt a MAC on AFTER decrypting, because that's the order the data naturally flows through your code — you have to deliberately verify first.)  -->

---

# Questions?
Next week: Review — consolidating Weeks 1–6 before the midterm

<!-- Cliffhanger/logistics: Week 7 is the review week for the pre-midterm block (hashing → MACs → AES modes → key exchange → AEAD). Tell them to bring their padding-oracle formula and the EtM/MtE/E&M comparison — both are fair game. -->
