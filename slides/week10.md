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

<!-- Roadmap. Spine line to say out loud: "strong keys do not help if the nonce repeats". Most of the class is the lab, not these slides. -->

---

## Recap — Weeks 4 to 6

- **Week 4:** CBC has no check; GCM adds a **tag**. A nonce must not repeat (we mentioned it)
- **Week 5:** key exchange needs authentication, or someone sits in the middle
- **Week 6:** GCM checks its tag first and answers the same every time
- This week: the part of GCM we have not tried to break yet, the **nonce**

<!-- Bridge. Week 4's slide said "reuse a nonce and data leaks". Today they see it happen. -->

---

## Why not just RSA?

- RSA is **slow**, thousands of times slower than AES
- RSA can only lock **short** data (a few hundred bytes), not a video or a PDF
- So real systems use RSA for one small thing: **the key**
- AES-GCM then does the heavy work, fast

<!-- Worksheet Q1. Keep it short. The numbers are not needed: "slow and short" is the whole point. Our demo uses RSA 2048 (a 256-byte locked key). -->

---

## Hybrid encryption: who holds what

| Who | Holds | Does |
|---|---|---|
| **Alice** | public key (everyone) + private key (only her) | unlocks the session key, then opens the messages |
| **Bob** | a random AES key (the session key) | locks it with Alice's **public** key, sends it **once**, then encrypts each message |
| **Eve** | nothing | sees the locked key, the nonces and the ciphertexts |

- Anyone can lock with the public key; **only Alice** can unlock with the private key

<!-- Worksheet step 1, Q2, Q3. Draw Bob, the wire and Alice on the board. TLS 1.3 uses authenticated ephemeral Diffie-Hellman instead of RSA key transport, but the shape (set up a key, then AEAD) is the same. -->

---

## The nonce

- AES-GCM needs a **nonce** (a number used once) for **every message**
- It is **not secret**, it travels with the ciphertext
- The rule: the same key must **never** be used with the same nonce twice (NIST SP 800-38D §8.2)
- Two common ways: a fresh **random** 96-bit nonce per message, or a **counter**

<!-- Worksheet Q4 and step 10. A nonce is not a key. Hiding it is pointless. The rule is about uniqueness. CWE-323: Reusing a Nonce, Key Pair in Encryption. -->

---

## What happens if the nonce repeats

![Bob's session reuses one nonce, so both messages are covered by the same random stream. Eve, who only sees the two ciphertexts, combines them: the stream disappears, and what is left is the two messages mixed together. If she knows one message, she reads the other. She never needed a key.](img/gcm-nonce-reuse.svg)

- Same key + same nonce ⇒ the **same random stream** covers both messages
- Eve combines the two ciphertexts: the stream **cancels out**
- If she knows one message (a greeting Bob always sends), she **reads the other**

<!-- Worksheet steps 4 and 5. No formulas needed on the slide: the picture is enough, and the script does the work. The optional Extension in Part 2 has the ⊕ explanation for the curious. Real GCM also breaks authenticity when the nonce repeats (tags can be forged, Joux 2006), say it in one sentence. -->

```sim
nonce-reuse
```

<!-- The sim uses a toy cipher, not real AES-GCM, but the structural point is the same: the stream depends only on (key, nonce). The lab runs the real AESGCM from the cryptography package. -->

---

## The lab's code: one line of difference

```python
if mode == "reuse":
    nonces = [os.urandom(12)] * 2                    # SAME nonce twice
else:
    nonces = [os.urandom(12), os.urandom(12)]        # NEW nonce each time
```

- `reuse`: Alice still opens both messages, **nothing looks wrong**
- But Eve reads message 2: `RESULT: Eve read message 2 WITHOUT the key`
- `good`: Eve gets `nothing readable`

<!-- Worksheet steps 5, 7 and 9. Stress: RSA-OAEP, AES-256 and the GCM tag are all correct in this code. The only fault is how the nonce is chosen. This is also what a rushed reviewer misses in AI-generated code (the AIR-Sec audit file). -->

---

## Fix, and what is still missing

- **Fix:** a new nonce for **every** message; send it with the ciphertext
- Do **not** fix it by locking the key again for every message, that defeats hybrid encryption
- **Still not solved:** how does Bob know the public key is really Alice's? (Week 5: authentication)
- **Still not solved:** can Alice tell who sent the message? (A public key lets **anyone** send)

<!-- Worksheet Q2 and the "limitation" idea. Do not reopen the full theory: one sentence each. ECIES (Diffie-Hellman based hybrid encryption) is the optional Q6. -->

---

## 🔓 Lab today — what to do

| Mode | nonce | Eve |
|---|---|---|
| `good` | new each time | reads nothing |
| `reuse` | same twice | reads message 2 |

- **Everyone (common 60):** A1 watch Bob send two messages · A2 reuse the nonce, Eve reads the secret · A3 new nonce, Eve gets nothing
- **Your form (40):** student ID ends **odd** → Conventional · **even** → AIR-Sec
- **Answer sheet:** Classroom → Week 10 → open the file for your form, type in the grey boxes, then File → Download → PDF
- Hand in `Wk10_<StudentID>.pdf` at `learn.zcr.ai/submit`

<!-- Exact commands are in the worksheet: one known-good path, copy and run. Start Docker early; wait for "week 10 lab ready" in the logs. The nonces are random per run, so students' hex values differ; the YES / NO and RESULT lines must match. -->

---

## Takeaway

- RSA locks the **key** (slow, short), AES-GCM locks the **messages** (fast)
- A **nonce** is not secret, but it must **never repeat** under the same key
- One repeated nonce lets Eve read a message **without any key**, and Alice never notices
- Next week: **digital signatures** (prove who sent it)

<!-- Land the spine: "the strongest keys are no help if the nonce repeats". Cold-call: "name one thing that looked fine in the reuse run." (Alice opened both messages normally.) Remind them: worksheet due Sunday before next class. -->
