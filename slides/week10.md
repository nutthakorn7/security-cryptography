---
marp: true
theme: default
paginate: true
header: "Cryptography and Network Security · Week 10"
---

<!-- Delivery: 100-minute lab session. 10 retrieval review + 10 brief + 60 practice + 15 debrief + 5 evidence. Short talk, then the lab (demo.py). The scored Week 10 quiz opens Week 11. Everyone completes the common 60 plus the assigned Conventional 40 or AIR-Sec 20/10/10. The viva is formative, no extra points. -->

# Week 10
## Hybrid encryption — lock the key with RSA, lock the messages with AES
Cryptography and Network Security · Nutthakorn Chalaemwongwan

<!-- Hook: ask "if RSA can encrypt anything, why does every real system (TLS, Signal, PGP) add AES on top?" Let them guess. Then: "and what happens if the AES part is used wrongly even though every key is strong?" -->

---

## Today

- Why RSA alone is not used for bulk data
- **Hybrid encryption:** lock one AES key with RSA, encrypt every message with AES-GCM
- The **nonce**: what it is, and what happens if it repeats
- 🔓 **Lab:** watch Eve read a secret **without any key** when Bob reuses a nonce

<!-- Roadmap. Spine line to say out loud: "strong keys do not help if the nonce repeats". Most of the class is the lab, not these slides. Logic of the deck: RSA is slow and short, so it locks only a key; AES-GCM locks the messages; GCM needs a nonce per message; a repeated nonce reuses the random stream, and Eve cancels it out; the fix is one new nonce per message. Each slide answers one question and ends with the next. -->

---

## Recap — Weeks 4 to 6

![Week 4: CBC has no check, GCM adds a tag, and the nonce must not repeat. Week 5: key exchange needs authentication. Week 6: GCM checks its tag first and answers the same every time. Week 10 today: the nonce, the part of GCM we have not tried to break yet.](img/w10-recap.svg)

- **Week 4:** CBC has no check; GCM adds a **tag**. A nonce must not repeat (we mentioned it)
- **Week 5:** key exchange needs authentication, or someone sits in the middle
- **Week 6:** GCM checks its tag first and answers the same every time
- This week: the part of GCM we have not tried to break yet, the **nonce**

<!-- Bridge. Week 4's slide said "reuse a nonce and data leaks". Today they see it happen. Logic: W4 to W6 gave us a cipher with a tag and a way to agree on a key; today asks what still goes wrong with a good cipher and good keys, and the answer is the nonce. Next question: why not use RSA for everything? -->

---

## Why not just RSA?

- RSA is **slow**, thousands of times slower than AES
- RSA can only lock **short** data (under 200 bytes with RSA 2048), not a video or a PDF
- So real systems use RSA for one small thing: **the key**
- AES-GCM then does the heavy work, fast

![RSA is slow and can only lock short data, under 200 bytes with a 2048-bit key. AES-GCM is fast and takes data of any size, such as a video or a PDF. So RSA locks one small thing, the AES key, and AES-GCM locks the messages.](img/w10-why-rsa.svg)

```
locked = rsa_enc(pubA, k)          # k is 32 bytes: it fits in RSA, once
c = seal(k, nonce, message)        # any size: AES-GCM does the heavy work
```

<!-- Worksheet Q1. Keep it short. The numbers are not needed: "slow and short" is the whole point. Our demo uses RSA 2048 (a 256-byte locked key; with OAEP-SHA256 at most 190 bytes fit, the 32-byte AES key is well inside). Logic: two tools, two limits: RSA cannot take a big message, AES needs both sides to share a key; so lock the small key with RSA and the big data with AES. Next question: who holds which key? -->

---

## Hybrid encryption: who holds what

| Who | Holds | Does |
|---|---|---|
| **Alice** | public key (everyone) + private key (only her) | unlocks the session key, then opens the messages |
| **Bob** | a random AES key (the session key) | locks it with Alice's **public** key, sends it **once**, then encrypts each message |
| **Eve** | nothing | sees the locked key, the nonces and the ciphertexts |

- Anyone can lock with the public key; **only Alice** can unlock with the private key

![Alice publishes her public key and keeps her private key. Bob makes one random AES session key, locks it with Alice's public key and sends it once, then sends every message encrypted with AES-GCM with a new nonce. Alice unlocks the session key with her private key and opens the messages. Eve sees the locked key, the nonces and the ciphertexts, but holds no key.](img/w10-hybrid-flow.svg)

```
locked = rsa_enc(pubA, k)         # Bob, once (RSA-OAEP)
k = rsa_dec(privA, locked)        # Alice only
(c_i, t_i) = seal(k, n_i, m_i)    # every message, new nonce n_i
```

<!-- Worksheet step 1, Q2, Q3. Draw Bob, the wire and Alice on the board. TLS 1.3 uses authenticated ephemeral Diffie-Hellman instead of RSA key transport, but the shape (set up a key, then AEAD) is the same. Logic: the public key can only lock, so only the holder of the private key gets k back; after that Alice and Bob share k, and Eve, who never gets k, cannot read. Next question: what is the nonce that appears in every seal() call? -->

---

## The nonce

- AES-GCM needs a **nonce** (a number used once) for **every message**
- It is **not secret**, it travels with the ciphertext
- The rule: the same key must **never** be used with the same nonce twice (NIST SP 800-38D §8.2)
- Two common ways: a fresh **random** 96-bit nonce per message, or a **counter**

![A message sent with AES-GCM has three parts: a 12-byte nonce that is not secret and travels with the message, the ciphertext, and a 16-byte tag. The rule is that the same key must never meet the same nonce twice. Two common ways are a fresh random 96-bit nonce per message, or a counter.](img/w10-nonce.svg)

```
n_i = random(12 bytes)            # new for every message, sent in the clear
n_i != n_j   for all i != j       # under the same key k
```

<!-- Worksheet Q4 and step 10. A nonce is not a key. Hiding it is pointless. The rule is about uniqueness. CWE-323: Reusing a Nonce, Key Pair in Encryption. Logic: the nonce makes the random stream different for every message, so uniqueness is the only job it has; it is public, so hiding it adds nothing. Next question: what exactly goes wrong if it repeats? -->

---

## What happens if the nonce repeats

![Bob's session reuses one nonce, so both messages are covered by the same random stream. Eve, who only sees the two ciphertexts, combines them: the stream disappears, and what is left is the two messages mixed together. If she knows one message, she reads the other. She never needed a key.](img/gcm-nonce-reuse.svg)

- Same key + same nonce ⇒ the **same random stream** covers both messages
- Eve combines the two ciphertexts: the stream **cancels out**
- If she knows one message (a greeting Bob always sends), she **reads the other**

```
c1 xor c2 = m1 xor m2             # same key + same nonce: the stream cancels
m2 = c1 xor c2 xor m1             # Eve knows m1 (the greeting)
```

<!-- Worksheet steps 4 and 5. No formulas needed on the slide: the picture is enough, and the script does the work. The optional Extension in Part 2 has the ⊕ explanation for the curious. Real GCM also breaks authenticity when the nonce repeats (tags can be forged, Joux 2006), say it in one sentence. Logic (equation): GCM encrypts as c = m xor s with a stream s that depends only on (k, nonce); two messages with one nonce share s, so c1 xor c2 = (m1 xor s) xor (m2 xor s) = m1 xor m2, and xor with a known m1 leaves m2. Next question: how small is the mistake in the lab code? -->

```sim
nonce-reuse
```

<!-- The sim uses a toy cipher, not real AES-GCM, but the structural point is the same: the stream depends only on (key, nonce). The lab runs the real AESGCM from the cryptography package. -->

---

## The lab's code: one line of difference

![In reuse mode Bob uses the same nonce for both messages. Alice still opens both messages and nothing looks wrong, but Eve prints RESULT: Eve read message 2 WITHOUT the key. In good mode Bob uses a new nonce for each message and Eve gets nothing readable.](img/w10-code-diff.svg)

```python
if mode == "reuse":
    nonces = [os.urandom(12)] * 2                    # SAME nonce twice
else:
    nonces = [os.urandom(12), os.urandom(12)]        # NEW nonce each time
```

- `reuse`: Alice still opens both messages, **nothing looks wrong**
- But Eve reads message 2: `RESULT: Eve read message 2 WITHOUT the key`
- `good`: Eve gets `nothing readable`

```
reuse:  n1 == n2   ⇒   c1 xor c2 xor m1 = m2    # Eve reads it
good:   n1 != n2   ⇒   the result is noise       # nothing readable
```

<!-- Worksheet steps 5, 7 and 9. Stress: RSA-OAEP, AES-256 and the GCM tag are all correct in this code. The only fault is how the nonce is chosen. This is also what a rushed reviewer misses in AI-generated code (the AIR-Sec audit file). Logic: the lab turns the equation into one line of code; the only difference between a safe run and a broken run is the nonce list, and nothing on Alice's side shows it. Next question: how do we fix it? -->

---

## Fix, and what is still missing

![Fix: a new nonce for every message, sent with the ciphertext. Do not lock the key again for every message, that defeats hybrid encryption. Still not solved: whether the public key really belongs to Alice, which Week 5 covered with authentication, and who sent the message, because a public key lets anyone send.](img/w10-fix.svg)

- **Fix:** a new nonce for **every** message; send it with the ciphertext
- Do **not** fix it by locking the key again for every message, that defeats hybrid encryption
- **Still not solved:** how does Bob know the public key is really Alice's? (Week 5: authentication)
- **Still not solved:** can Alice tell who sent the message? (A public key lets **anyone** send)

```
n_i = random(12 bytes)            # a new nonce for every message
c_i = seal(k, n_i, m_i)           # send (n_i, c_i) together
```

<!-- Worksheet Q2 and the "limitation" idea. Do not reopen the full theory: one sentence each. ECIES (Diffie-Hellman based hybrid encryption) is the optional Q6. Logic: the bug was a repeated nonce, so the fix is a new nonce per message; but the scheme only gives secrecy, so two questions stay open, which key is Alice's (W5) and who is the sender (W11). Next question: what do we do in the lab? -->

---

## 🔓 Lab today — what to do

![Three lab steps with demo.py inside the container. A1: run demo.py good and watch Bob send two messages with a new nonce each time. A2: run demo.py reuse then demo.py attack reuse and Eve reads message 2 without the key. A3: run demo.py attack good and Eve gets nothing readable. Then hand in Wk10 student ID PDF at learn.zcr.ai/submit by the Sunday 23:59 in the Classroom post.](img/w10-lab-flow.svg)

| Mode | nonce | Eve |
|---|---|---|
| `good` | new each time | reads nothing |
| `reuse` | same twice | reads message 2 |

- **Everyone (common 60):** A1 watch Bob send two messages · A2 reuse the nonce, Eve reads the secret · A3 new nonce, Eve gets nothing
- **Your form (40):** student ID ends **odd** → Conventional · **even** → AIR-Sec
- **Answer sheet:** Classroom → Week 10 → open the file for your form, type in the grey boxes, then File → Download → PDF
- Hand in `Wk10_<StudentID>.pdf` at `learn.zcr.ai/submit`

<!-- Exact commands are in the worksheet: one known-good path, copy and run. Start Docker early; wait for "week 10 lab ready" in the logs. The nonces are random per run, so students' hex values differ; the YES / NO and RESULT lines must match. Logic: the three steps check the equations. A1: new nonces, so n1 != n2. A2: the same nonce, so c1 xor c2 xor m1 = m2. A3: new nonces again, so nothing readable. -->

---

## Takeaway

- RSA locks the **key** (slow, short), AES-GCM locks the **messages** (fast)
- A **nonce** is not secret, but it must **never repeat** under the same key
- One repeated nonce lets Eve read a message **without any key**, and Alice never notices
- Next week: **digital signatures** (prove who sent it)

![RSA locks the key, which is slow and short. AES-GCM locks the messages, which is fast. A nonce is not secret but must never repeat under the same key. One repeated nonce lets Eve read a message without any key, and Alice never notices.](img/w10-takeaway.svg)

```
k locks the messages, RSA locks k       # hybrid encryption
same (k, nonce) twice   ⇒   m2 = c1 xor c2 xor m1
```

<!-- Land the spine: "the strongest keys are no help if the nonce repeats". Cold-call: "name one thing that looked fine in the reuse run." (Alice opened both messages normally.) Remind them: worksheet due Sunday before next class. Logic: lock the key once, lock each message with a new nonce; secrecy alone does not say who sent it, which is next week. -->
