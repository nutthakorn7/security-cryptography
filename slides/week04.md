---
marp: true
theme: default
paginate: true
header: "Cryptography and Network Security · Week 4"
---

# Week 4
## AES modes — encrypted is not tamper-proof
Cryptography and Network Security · Nutthakorn Chalaemwongwan

<!-- Lab week: short talk, then the lab. Hook: ask "if AES is unbreakable, can someone still change a message they cannot read?" Let them say no. The lab shows they can. Bring a laptop with Docker; one guided path, no math. -->

---

## Today

- A **10-minute quiz** on Week 3 to start (one question at a time)
- AES is strong — the **mode** is where things go wrong
- **ECB** shows patterns; **CBC** can be changed without the key
- The fix: **GCM** — encryption **plus a tag** that checks for changes
- 🔓 **Lab:** change an encrypted token, then watch GCM refuse the same kind of change

<!-- Roadmap. Say the spine line out loud: "the math is fine; the way it was used is not". Most of the class is the lab, not these slides. At the end of the class the teams confirm membership and review the CryptoVault design plan (a project item, not part of the worksheet). -->

---

## Recap — Week 3

- A plain hash has **no secret**, so it cannot prove who made a message
- A **MAC (HMAC)** adds a secret key and checks that a message was **not changed**
- This week: what about **encryption**? Does it also stop changes?

<!-- Bridge from W3. W3 = checking that a message was not changed (MAC). W4 asks the natural next question: if I encrypt it, is it also protected from changes? (No — that is today.) -->

---

## AES is strong — the mode decides

- **AES** locks one **block** (16 bytes) at a time
- No practical attack on AES itself is known
- A real message has many blocks, so we need a **mode** to connect them: ECB, CBC, GCM …
- The **mode** — not AES — decides whether the result is safe

<!-- The thesis in one slide: nobody breaks AES in this course, or in practice. Every attack today is about how AES is used. -->

---

## ECB: same block → same ciphertext

![The same two blocks HELLO and HELLO are encrypted. In ECB they give two equal ciphertext blocks, so the pattern leaks. In CBC they give two different ciphertext blocks.](img/w4-ecb-same-blocks.svg)

- ECB locks every block **on its own**, with the same key
- Repeated blocks stay repeated, so **patterns leak** (the famous "ECB penguin")
- Never use ECB for real data

<!-- Worksheet Q1. NIST SP 800-38A §6.1: ECB assigns a fixed ciphertext block to each plaintext block under a given key. Ask: "the ciphertext looks random byte by byte, so why can you still see an outline in an encrypted picture?" (equal blocks stay equal). Do not show the original Tux image; the picture on this slide is enough. -->

---

## CBC: mix each block with the one before

- Before locking a block, CBC **mixes** it with the **block before**
- The first block is mixed with a fresh, unpredictable starting value, the **IV**
- Equal blocks now normally give **different** ciphertext, so the ECB pattern is gone
- But: CBC has **no way to notice** that someone changed the data

<!-- Keep to this level: lock = encrypt, mix = XOR. No formulas needed. NIST SP 800-38A: the CBC IV need not be secret but must be unpredictable (that is Q2 in the optional list). Do not reveal the "different door" yet: the next slide does. -->

---

## Encrypted ≠ tamper-proof

- CBC gives **secrecy** (nobody can read it)
- It does **not** give **integrity** (nobody can change it unseen)
- The server just decrypts whatever arrives, and trusts the result
- **CWE-353** (missing integrity check) / **CWE-649** (encryption without integrity)

> A token nobody can read can still be **changed**.

<!-- The core idea of the week. Cold-call: "if you cannot read a message, can you still change it?" Yes — that is the lab. In the lab, changing one letter of a CBC token changes nothing the server can see: it still answers guest. -->

---

## Why changing the block before works

![In CBC a block is read back in two steps: unlock it with the secret key, then mix the result with the block before it. If someone changes the block before, the same spot in the result changes, so role guest can become role admin without the key. The changed block itself turns into garbage, but in this lab nobody reads it.](img/w4-cbc-mix.svg)

- Reading a block = **unlock**, then **mix with the block before**
- The block before is **in the token**, so anyone holding the token can change it
- The result changes in the **same spot** — no key needed

```sim
cbc-bitflip
```

<!-- The aha slide, in pictures. The lab script does this for the students; they never compute it. The sim uses a toy cipher, not real AES, with the same chaining shape; say so explicitly so nobody thinks AES itself is toy. Verifier B in the sim previews the fix on the next slide; do not over-explain it. -->

---

## The fix: GCM = encrypt + tag

![A GCM token has a nonce, the encrypted data and a tag. The server re-makes the tag from what arrived using its secret key and compares it with the tag that came in. If they match it accepts; if anything was changed they do not match and it answers invalid or tampered token.](img/w4-gcm-tag-check.svg)

- GCM adds a **tag** (a seal) to every message
- On arrival the server **re-makes the tag** and compares
- Changed token → tags differ → **rejected** (`403`)
- A matching tag means **not changed**; an old valid token sent again still passes (needs a different defence)

<!-- Say "tag" = seal. Do not go into GHASH. The tag also covers any extra authenticated data (none in this lab) and depends on the nonce; a matching tag shows the data was not changed, it does not stop replay. TLS 1.3 removed CBC and keeps only authenticated (AEAD) algorithms such as AES-GCM: RFC 8446 §1.2. It only helps if the program really obeys the check (worksheet step 17 and optional Q10). -->

---

## One more rule: a nonce is used once

- GCM needs a number called a **nonce** for every message
- It is **not secret** — but it must **never repeat** with the same key
- Repeat it, and the data **leaks** and tags can be **forged**
- In code **you** hand the library the nonce: use a new one for every message

<!-- Worksheet Q5 (Q6 optional). NIST SP 800-38D §8: a repeated IV under the same key breaks GCM; the recommended length is 96 bits. Real case, only if time allows: in 2016 researchers found 184 HTTPS servers repeating GCM nonces (Böck et al., IACR ePrint 2016/475). -->

---

## 🔓 Lab today — what to do

| Service | Port | Mode | Changed token noticed? |
|---|---|---|---|
| vulnerable | `:8096` | AES-256-CBC | **No** |
| fixed | `:8097` | AES-256-GCM | **Yes** |

- **Everyone (common 60):** A1 change a letter of a CBC token · A2 run the script, get `admin` · A3 see GCM refuse
- **Your form (40):** student ID ends **odd** → Conventional · **even** → AIR-Sec
- **Answer sheet:** Classroom → Week 04 → open the file for your form, type in the grey boxes, then File → Download → PDF
- Hand in `Wk04_<StudentID>.pdf` at `learn.zcr.ai/submit`
- At the end of class: teams confirm membership and review the **CryptoVault** design plan (KDF + AEAD), then submit it as the project brief says

<!-- Exact commands are in the worksheet: one known-good path, copy and run. The shared demo flag is fine. Start Docker early; wait for Running on ...:8096 and :8097 in the logs. On Windows, use curl.exe. -->

---

## Takeaway

- AES is strong — the **mode** is where real systems fail
- Encryption alone is **not** integrity: unauthenticated CBC can be changed
- **GCM** adds a tag — but only helps if the program **checks it**
- Next week: **key exchange** — a secret handshake in the open, and the man in the middle

<!-- Land the spine: "textbook-secure primitive, real-system failure". Cold-call: "name one thing GCM checks that CBC never does." Remind: Docker + laptop ready for next week too. -->
