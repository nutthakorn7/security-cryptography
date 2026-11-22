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

<!-- Roadmap. Say the spine line out loud: "the math is fine; the way it was used is not". Most of the class is the lab, not these slides. Logic of the deck: AES is strong, so the question is the mode. ECB leaks patterns, CBC hides them but cannot notice changes, the lab shows the change, GCM adds a tag that notices. Each slide answers one question and ends with the question the next slide answers. -->

---

## Recap — Week 3

- A plain hash has **no secret**, so it cannot prove who made a message
- A **MAC (HMAC)** adds a secret key and checks that a message was **not changed**
- This week: what about **encryption**? Does it also stop changes?

<!-- Bridge from W3. W3 = checking that a message was not changed (MAC). W4 asks the natural next question: if I encrypt it, is it also protected from changes? (No — that is today.) Logic: W3 gave us a check for changes (a MAC); W4 asks whether encryption alone gives the same check. It does not, and the next slides show why. -->

---

## AES is strong — the mode decides

![A message is cut into blocks of 16 bytes. AES locks each block with the secret key and gives one locked block. AES itself is strong; the open question is how the blocks are connected, and that choice is the mode: ECB, CBC or GCM.](img/w4-blocks-mode.svg)

```
c = E(k, p)     # lock ONE block (16 bytes) with the key k
p = D(k, c)     # unlock it again with k
```

- **AES** locks one **block** (16 bytes) at a time; no practical attack on AES itself is known
- A real message has many blocks, so a **mode** connects them (ECB, CBC, GCM …). The **mode** — not AES — decides whether the result is safe

<!-- The thesis in one slide: nobody breaks AES in this course, or in practice. Every attack today is about how AES is used. Logic: E is a one-to-one lock for a single block, so a longer message needs a rule for connecting the blocks; that rule is the mode. Next question: what is the simplest mode, and is it safe? -->

---

## ECB: same block → same ciphertext

![The same two blocks HELLO and HELLO are encrypted. In ECB they give two equal ciphertext blocks, so the pattern leaks. In CBC they give two different ciphertext blocks.](img/w4-ecb-same-blocks.svg)

```
c1 = E(k, p1)
c2 = E(k, p2)
p1 = p2   ⇒   c1 = c2        # same block in, same block out
```

- ECB locks every block **on its own**, so **patterns leak** (the "ECB penguin"). Never use it for real data

<!-- Worksheet Q1. NIST SP 800-38A §6.1: ECB assigns a fixed ciphertext block to each plaintext block under a given key. Ask: "the ciphertext looks random byte by byte, so why can you still see an outline in an encrypted picture?" (equal blocks stay equal). Do not show the original Tux image; the picture on this slide is enough. Logic: E is a function, so equal inputs give equal outputs; an eavesdropper sees which blocks are equal without the key. Next question: how do we make equal blocks look different? -->

---

## CBC: mix each block with the one before

![In CBC the first block is mixed with a random start value called the IV, then locked with AES. The locked result of each block is mixed into the next block before that block is locked, so the blocks form a chain.](img/w4-cbc-chain.svg)

```
c1 = E(k, p1 xor iv)
c2 = E(k, p2 xor c1)
c3 = E(k, p3 xor c2)
```

- Each block is **mixed** with the block before (the first with a fresh start value, the **IV**), so equal blocks now give **different** ciphertext
- But CBC has **no way to notice** that someone changed the data

<!-- Keep to this level: lock = encrypt, mix = XOR. No formulas needed. NIST SP 800-38A: the CBC IV need not be secret but must be unpredictable (that is Q2 in the optional list). Do not reveal the "different door" yet: the next slide does. Logic: each block is mixed with the block before, so equal blocks now give different results and the pattern is gone. Secrecy is fixed. Next question: is secrecy enough? -->

---

## Encrypted ≠ tamper-proof

- CBC gives **secrecy** (nobody can read it)
- It does **not** give **integrity** (nobody can change it unseen)
- The server just decrypts whatever arrives, and trusts the result

```
dec(k, c') → p'       # CBC always answers, for any c'
                      # nothing here checks that c' was not changed
```
- **CWE-353** (missing integrity check) / **CWE-649** (encryption without integrity)

> A token nobody can read can still be **changed**.

<!-- The core idea of the week. Cold-call: "if you cannot read a message, can you still change it?" Yes — that is the lab. In the lab, changing one letter of a CBC token changes nothing the server can see: it still answers guest. Logic: secrecy and integrity are two different properties. CBC decryption answers for every ciphertext, so it never refuses a changed one. Next question: how exactly can someone change it without the key? (Lab first, then the picture.) -->

---

## Why changing the block before works

![In CBC a block is read back in two steps: unlock it with the secret key, then mix the result with the block before it. If someone changes the block before, the same spot in the result changes, so role guest can become role admin without the key. The changed block itself turns into garbage, but in this lab nobody reads it.](img/w4-cbc-mix.svg)

```
p2  = D(k, c2) xor c1                       # what the server computes
c1' = c1 xor delta                          # the attacker changes the block before
p2' = D(k, c2) xor c1' = p2 xor delta       # no key used
delta = "guest" xor "admin"   ⇒   p2' = "admin"
```

- The block before is **in the token**: change it and the result changes in the **same spot** — **no key needed**

```sim
cbc-bitflip
```

<!-- The aha slide, in pictures. The lab script does this for the students; they never compute it. The sim uses a toy cipher, not real AES, with the same chaining shape; say so explicitly so nobody thinks AES itself is toy. Verifier B in the sim previews the fix on the next slide; do not over-explain it. Logic (equation): the server reads p2 = D(k, c2) xor c1, and c1 sits in the token. Adding delta to c1 adds delta to p2, using only xor and never the key. "guest" and "admin" are both 5 letters, so delta fits. The cost is that p1 becomes garbage; in this lab nobody reads it. Student analogy from the worksheet: result = secret + block before, so +1 on the block before gives +1 on the result. Next question: how do we stop this? -->

---

## The fix: GCM = encrypt + tag

![A GCM token has a nonce, the encrypted data and a tag. The server re-makes the tag from what arrived using its secret key and compares it with the tag that came in. If they match it accepts; if anything was changed they do not match and it answers invalid or tampered token.](img/w4-gcm-tag-check.svg)

```
(c, t) = GCM_enc(k, nonce, p)       # t = tag(k, nonce, c)
server checks:  t' == tag(k, nonce, c') ?
changed c'  ⇒  t' ≠ tag(k, nonce, c')  ⇒  403
```

- A changed token → tags differ → **rejected** (`403`). A matching tag means **not changed**; an old valid token sent again still passes (needs a different defence)

<!-- Say "tag" = seal. Do not go into GHASH. The tag also covers any extra authenticated data (none in this lab) and depends on the nonce; a matching tag shows the data was not changed, it does not stop replay. TLS 1.3 removed CBC and keeps only authenticated (AEAD) algorithms such as AES-GCM: RFC 8446 §1.2. It only helps if the program really obeys the check (worksheet Step 11 and optional Q10). Logic: the tag is a function of the key, so changing c without the key cannot give a matching tag (the chance of guessing one is negligible); CBC accepts every changed c', GCM rejects almost every changed c'. A resent valid (c, t) still passes: a tag shows "not changed", not "new". Next question: what else must we get right? -->

---

## How a tag is made (a toy version)

![Toy example with the secret s equal to 2. The sender works through the data 3, 1, 4: (0 plus 3) times 2 is 6, (6 plus 1) times 2 is 14, (14 plus 4) times 2 is 36, so the tag is 36. Eve changes the 3 into a 5. The receiver works through 5, 1, 4 the same way and gets 10, 22 and 52. The result 52 is not the tag 36 that came with the data, so the message is rejected. Eve does not know s, so she cannot tell which tag would match her changed data.](img/w4-tag-toy.svg)

```
tag = 0
for d in data:  tag = (tag + d) * s      # s = the secret number
(3, 1, 4)  with s = 2  ⇒  6 → 14 → 36   # tag = 36
(5, 1, 4)  with s = 2  ⇒  10 → 22 → 52  # 52 ≠ 36 ⇒ reject
```

- Sender and receiver share a **secret number**; the tag **mixes every piece** of the data with it
- The receiver **works it out again** from what arrived and compares
- Change any piece → a different tag. Eve does not know the secret, so she cannot fix the tag
- Toy only: real GCM makes its secret numbers **from the key**, uses 128-bit numbers and mixes in the nonce

<!-- Student version: only the toy. Walk the numbers aloud: 3 → 6, 14, 36; then Eve changes the 3 into a 5 → 10, 22, 52. Ask: "Eve knows the rule but not s; can she say which tag fits 5, 1, 4?" (No: with s = 3 the original data would give 102, not 36, so the tag depends on the secret.) Logic: slide 9 said the server re-makes the tag and compares; this slide shows what "re-make" means, with numbers small enough to follow by hand; the next slide asks what must never repeat. INSTRUCTOR ONLY, not for the slide: the real recipe (NIST SP 800-38D §6.4, verified in code against AESGCM): H = E(k, 0); counter-mode encryption with E(k, nonce||2), E(k, nonce||3), ...; GHASH over the extra data, the ciphertext and a length block, Y = (Y xor X) * H in GF(2^128), the same "mix, then multiply by the secret" loop as the toy; tag = Y xor E(k, nonce||1). The last term is a one-time mask made from the nonce. If a nonce repeats, the mask repeats, and xor of two tags leaks an equation in H; that is the "tags can be forged" on the next slide. -->

---

## One more rule: a nonce is used once

```
s  = stream(k, nonce)
c1 = p1 xor s
c2 = p2 xor s                 # same nonce ⇒ same s
c1 xor c2 = p1 xor p2         # the data leaks
```

- GCM needs a number called a **nonce** for every message
- It is **not secret** — but it must **never repeat** with the same key
- Repeat it, and the data **leaks** and tags can be **forged**
- In code **you** hand the library the nonce: use a new one for every message

<!-- Worksheet Q5 (Q6 optional). NIST SP 800-38D §8: a repeated IV under the same key breaks GCM; the recommended length is 96 bits. Real case, only if time allows: in 2016 researchers found 184 HTTPS servers repeating GCM nonces (Böck et al., IACR ePrint 2016/475). Logic: GCM encrypts by xor with a stream made from (key, nonce); if the nonce repeats the stream repeats, and the same xor trick as slide 8 leaks the data. The tag also depends on the nonce, so a repeat lets tags be forged (stated, not derived here). Optional: skip if time is short. -->

---

## 🔓 Lab today — what to do

![Three lab steps. A1: on the CBC server at port 8096, log in and change one letter of the token; the server still says guest. A2: run exploit.py inside the container; guest becomes admin and the flag appears. A3: on the GCM server at port 8097, change one letter of the token; the server answers 403 invalid or tampered token. Then hand in Wk04 student ID PDF at learn.zcr.ai/submit by Sunday 29 November 23:59.](img/w4-lab-flow.svg)

- **Everyone (common 60):** A1 change a letter of a CBC token · A2 run the script, get `admin` · A3 see GCM refuse
- **Your form (40):** student ID ends **odd** → Conventional · **even** → AIR-Sec
- **Answer sheet:** Classroom → Week 04 → open the file for your form, type in the grey boxes, then File → Download → PDF, and hand in `Wk04_<StudentID>.pdf` at `learn.zcr.ai/submit`

<!-- Exact commands are in the worksheet: one known-good path, copy and run. The shared demo flag is fine. Start Docker early; wait for Running on ...:8096 and :8097 in the logs. On Windows, use curl.exe. Logic: the three steps check the equations. A1: the token is iv, c1, c2 and the first letter belongs to iv, which only changes p1; the role is in p2, so the server still says guest (it did not notice). A2: the script changes c1 by delta, so p2 becomes admin. A3: the same kind of change on GCM breaks the tag, so 403. -->

---

## Takeaway

- AES is strong — the **mode** is where real systems fail
- Encryption alone is **not** integrity: unauthenticated CBC can be changed
- **GCM** adds a tag — but only helps if the program **checks it**

```
CBC:  secret ✓   check for changes ✗
GCM:  secret ✓   check for changes ✓   (the tag, if the program obeys it)
```
- Next week: **key exchange** — a secret handshake in the open, and the man in the middle

<!-- Land the spine: "textbook-secure primitive, real-system failure". Cold-call: "name one thing GCM checks that CBC never does." Remind: Docker + laptop ready for next week too. -->
