---
marp: true
theme: default
paginate: true
header: "Cryptography and Network Security · Week 5"
---

# Week 5
## Key exchange — the man in the middle
Cryptography and Network Security · Nutthakorn Chalaemwongwan

<!-- Lab week: short talk, then the lab. Hook: ask "Alice and Bob have never met and the network is public. How can they agree on a secret key without anyone else learning it?" Let them sit with it for a moment. Then promise: they will watch a real attacker sit in the middle and read the "secret" channel, and then watch one small check stop it. Bring a laptop with Docker; one image build is needed before class. -->

---

## Today

- A **10-minute quiz** on Week 4 to start (one question at a time)
- How do two people get a shared key **over a public network**?
- **Diffie-Hellman (DH):** a handshake in the open
- DH stops people who **listen** — but not a person **in the middle**
- 🔓 **Lab:** watch `relay` read a message, then watch a tag check stop it

<!-- Roadmap. Say the spine line out loud: "the math is fine; the missing check is the problem". Most of the class is the lab, not these slides. The Week 5 quiz itself is taken at the start of Week 6. -->

---

## Recap — Week 4

- AES modes: **ECB** shows patterns, **CBC** can be changed, **GCM** adds a tag
- Week 4 started with "Alice and Bob **already share a key**"
- Week 5 asks the step before that: how do they **get** the key — over a network anyone can watch?

<!-- Bridge from W4. W4 = protect data once you have a key. W5 = how to agree on that key in the open. This is the missing first step. -->

---

## The problem: a secret over a public wire

- Alice wants to send Bob a secret message with AES
- They need the **same key**, and they have never met
- **Naive idea:** send the key over the network
- Anyone watching the wire now has the key too

<!-- Ask: "why can't Alice just email Bob the AES key?" Let students find it: anyone who reads the message in transit has the key, game over. Worksheet Q1. -->

---

## Diffie-Hellman — the idea, no formulas

- Each side keeps a **private number** and never sends it
- Each side sends a **public value** made from it
- Mixing **my private number** with **your public value** gives both of us the **same secret**
- A person who only **listens** sees the two public values — and cannot rebuild the secret
- Why: going backwards is a famous hard problem, the **discrete logarithm** (you only need the name)

<!-- Use the paint-mixing picture if it helps: mixing is easy, un-mixing is not. No algebra and no group theory this week: the lab uses a standard 2048-bit group (RFC 3526 Group 14) and students never calculate anything. The "hard to undo" part is the discrete-log problem; name it once, do not derive it. -->

---

## But DH answers the wrong question

- DH gives a secret that a **listener** cannot work out
- It does **not** tell you **who** you agreed the secret with
- "Whoever answers when I dial Bob" is not the same as "Bob"
- An attacker who is **in the middle** can answer for Bob

<!-- The pivot slide. Passive versus active is the crux: DH protects against listening, not against someone who can answer in your place. This is CWE-322 (key exchange without entity authentication). Worksheet Q2 and Q3. -->

---

## Meet the lab: Alice, Bob and relay

| Service | Role | What it does |
|---|---|---|
| `alice` | Client | Sends one secret message — through `relay`, **not** straight to Bob |
| `bob` | Server | Does the handshake and reads one message |
| `relay` | The attacker | Sits on the path between them |

- The premise **is** the lesson: Alice dials `relay`, because the attacker controls the network path

<!-- Set up the topology before the attack. Stress the premise line. Three containers on one private Docker network; nothing is opened to the outside, so it is safe to run on a laptop. -->

---

## The attack: two handshakes

![Two independent Diffie-Hellman handshakes side by side: Alice does one with relay (relay posing as Bob), and relay does a second one with Bob (relay posing as Alice). Relay holds both secrets, decrypts Alice's message, reads it, re-encrypts it and forwards it to Bob. Alice and Bob never share a secret with each other.](img/w5-two-handshakes.svg)

```sim
dh-mitm
```

<!-- Walk the picture: handshake one is Alice with relay, handshake two is relay with Bob. Relay needs BOTH because it must be a real DH partner to each side, otherwise it could not read and then re-send the message. The sim runs a real small DH handshake, not a script; the cipher, key mixing and tag in it are toy stand-ins (same simplification as the Week 3 sim). Run it live after this slide with the "has AUTH_KEY leaked to relay?" box UNCHECKED (this is the vulnerable story); tick it later, at the fix slide, to preview the second run. -->

---

## Why neither side notices

- Alice's handshake **finishes fine** — she has *a* secret
- Bob's handshake **finishes fine** — he has *a* secret
- They do **not** share the same secret, and neither side can tell
- Nothing ties a public value to a **person**

```
RELAY: completed independent DH handshake with Alice (posing as Bob)
RELAY: completed independent DH handshake with Bob (posing as Alice)
RELAY INTERCEPTED: the launch code is 4471
BOB RECEIVED: the launch code is 4471
```

<!-- The punchline of the first run. Both handshakes are correct DH; the failure is that nobody checked who was on the other end. The log lines can swap order a little between runs; RELAY INTERCEPTED always comes after both "completed" lines. Real terminal output also has CryptographyDeprecationWarning lines (the library warns that this old kind of DH is on its way out). The worksheet filters them out. -->

---

## The fix: put a tag on the public value

- Alice and Bob already share a secret key, `AUTH_KEY`, from **before**
- Each side adds a **tag** (HMAC, from Week 3) to its public value
- The other side checks the tag **before** using the value
- `relay` does not know `AUTH_KEY`, so it cannot make a good tag — both sides stop

```
RELAY: (fixed mode) attempted DH substitution with Alice (posing as Bob)
AUTH FAILED - ABORTING          (alice)
AUTH FAILED - ABORTING          (bob)
```

<!-- Same relay code runs: it still tries to swap its own values in. The ONLY change is one tag check. Zero RELAY INTERCEPTED lines is the evidence. Say what the fix needs: Alice and Bob must share AUTH_KEY in advance, by a safe route. That is the "trust bootstrap" problem. If someone asks why not use AUTH_KEY to encrypt directly: a later leak of AUTH_KEY would open every recorded conversation; with a fresh DH each time (and the private numbers erased) it would not. Plain-words name: forward secrecy. -->

---

## 🔓 Lab today — what to do

| Run | Command mode | What relay can do |
|---|---|---|
| vulnerable | no tag check | **read** the message |
| fixed | tag check | **nothing** — both sides stop |

- **Everyone (common 60):** A1 watch `relay` read the message · A2 run the tag check, see `AUTH FAILED` · A3 explain why it works and what it needs
- **Your form (40):** student ID ends **odd** → AIR-Sec · **even** → Conventional
- **Answer sheet:** Classroom → Week 05 → open the file for your form, type in the grey boxes, then File → Download → PDF
- Hand in `Wk05_<StudentID>.pdf` at `learn.zcr.ai/submit`

<!-- Exact commands are in the worksheet: one known-good path, copy and run. Build the image at home (needs internet) so class time goes to the lab. On Windows the worksheet gives findstr and PowerShell versions. The line "the launch code is 4471" is a fixed demo message, the same for everyone. -->

---

## Takeaway

- DH lets two people agree on a secret **in the open**
- It stops people who **listen**, not a person **in the middle**
- A **tag** on each public value stops the middle person — if the key was shared **safely first**
- Next week: **AEAD** — encryption that checks for changes, and what an error message can give away

<!-- Land the spine. Cold-call: "name the one thing relay did not have in the second run." (AUTH_KEY.) Remind: Docker and laptop ready for next week too. -->
