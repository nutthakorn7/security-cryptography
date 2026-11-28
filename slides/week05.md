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

<!-- Roadmap. Say the spine line out loud: "the math is fine; the missing check is the problem". Most of the class is the lab, not these slides. The Week 5 quiz itself is taken at the start of Week 6. Logic of the deck: we need a shared key (W4 assumed one); DH gives one in the open; but DH cannot tell who is on the other end; the lab shows an attacker in the middle; a tag with a pre-shared key stops it. Each slide answers one question and ends with the next. -->

---

## Recap — Week 4

![Week 5 asks how Alice and Bob agree on a key over a public network. Week 4 then used that key to protect data with AES modes.](img/w5-recap.svg)

- AES modes: **ECB** shows patterns, **CBC** can be changed, **GCM** adds a tag
- Week 4 started with "Alice and Bob **already share a key**"
- Week 5 asks the step before that: how do they **get** the key — over a network anyone can watch?

<!-- Bridge from W4. W4 = protect data once you have a key. W5 = how to agree on that key in the open. This is the missing first step. Logic: W4 used a key; where did it come from? Next question: why can't Alice just send it? -->

---

## The problem: a secret over a public wire

- Alice wants to send Bob a secret message with AES
- They need the **same key**, and they have never met
- **Naive idea:** send the key over the network
- Anyone watching the wire now has the key too

![Alice sends an AES key to Bob over a public network. Eve, who is listening, copies the key too, so the key is no longer secret.](img/w5-key-problem.svg)

```
key = random()                  # Alice makes an AES key
send(Bob, key)                  # on a public wire
Eve sees key   ⇒   enc(key, m) is no longer secret
```

<!-- Ask: "why can't Alice just email Bob the AES key?" Let students find it: anyone who reads the message in transit has the key, game over. Worksheet Q1. Logic: the key travels on the same wire as the data, so whoever can read one can read the other. Next question: can two people end up with the same secret without ever sending it? -->

---

## Diffie-Hellman — the idea in function calls

- Each side keeps a **private number** and never sends it
- Each side sends a **public value** made from it
- Mixing **my private number** with **your public value** gives both of us the **same secret**
- A person who only **listens** sees the two public values — and cannot rebuild the secret
- Why: going backwards is a famous hard problem, the **discrete logarithm** (you only need the name)

![Alice keeps a private number a and sends a public value A. Bob keeps a private number b and sends a public value B. Each side mixes its own private number with the other public value and gets the same secret K. An eavesdropper sees only A and B and cannot work out K.](img/w5-dh-idea.svg)

```
A = pub(a)           B = pub(b)            # only A and B cross the wire
K_alice = shared(a, B)
K_bob   = shared(b, A)
K_alice = K_bob                            # the same secret; Eve knows only A and B
```

<!-- Use the paint-mixing picture if it helps: mixing is easy, un-mixing is not. No algebra and no group theory this week: the lab uses a standard 2048-bit group (RFC 3526 Group 14) and students never calculate anything. The "hard to undo" part is the discrete-log problem; name it once, do not derive it. Logic: shared(a, B) and shared(b, A) are equal by the rule of the group (in the lab B^a = A^b mod p), but recovering a from A is the hard problem. So a listener fails. Next question: does that mean the problem is solved? -->

---

## But DH answers the wrong question

- DH gives a secret that a **listener** cannot work out
- It does **not** tell you **who** you agreed the secret with
- "Whoever answers when I dial Bob" is not the same as "Bob"
- An attacker who is **in the middle** can answer for Bob

![Alice dials Bob. Someone answers. Diffie-Hellman gives a shared secret with whoever answered, but it does not say whether that is Bob or an attacker called relay.](img/w5-who-answers.svg)

```
secret = shared(a, X)            # X = whoever answered
X = Bob    or    X = relay       # nothing in DH checks which
```

<!-- The pivot slide. Passive versus active is the crux: DH protects against listening, not against someone who can answer in your place. This is CWE-322 (key exchange without entity authentication). Worksheet Q2 and Q3. Logic: shared(a, X) works for any X, so the handshake always finishes; it never asks who X is. Next question: what does an attacker do with that? -->

---

## Meet the lab: Alice, Bob and relay

| Service | Role | What it does |
|---|---|---|
| `alice` | Client | Sends one secret message — through `relay`, **not** straight to Bob |
| `bob` | Server | Does the handshake and reads one message |
| `relay` | The attacker | Sits on the path between them |

- The premise **is** the lesson: Alice dials `relay`, because the attacker controls the network path

![Alice dials relay instead of Bob because the attacker controls the network path. relay does a handshake with Alice and a second one with Bob and forwards the message in between.](img/w5-lab-topology.svg)

<!-- Set up the topology before the attack. Stress the premise line. Three containers on one private Docker network; nothing is opened to the outside, so it is safe to run on a laptop. Logic: set the stage before the attack so the next slide is easy to read. -->

---

## The attack: two handshakes

![Two independent Diffie-Hellman handshakes side by side: Alice does one with relay (relay posing as Bob), and relay does a second one with Bob (relay posing as Alice). Relay holds both secrets, decrypts Alice's message, reads it, re-encrypts it and forwards it to Bob. Alice and Bob never share a secret with each other.](img/w5-two-handshakes.svg)

```sim
dh-mitm
```

```
Alice <-> relay:   K1 = shared(a, R1)  = shared(r1, A)
relay <-> Bob:     K2 = shared(r2, B)  = shared(b, R2)
c  = enc(K1, m)                    # Alice sends her message
m  = dec(K1, c)                    # relay reads it
c' = enc(K2, m)                    # relay sends it on to Bob
```

<!-- Walk the picture: handshake one is Alice with relay, handshake two is relay with Bob. Relay needs BOTH because it must be a real DH partner to each side, otherwise it could not read and then re-send the message. The sim runs a real small DH handshake, not a script; the cipher, key mixing and tag in it are toy stand-ins (same simplification as the Week 3 sim). Run it live after this slide with the "has AUTH_KEY leaked to relay?" box UNCHECKED. One run shows both results: Verifier A (plain DH, accepted) is the first lab run, and Verifier B (HMAC, rejected) is the second, so point back to Verifier B at the fix slide. Tick the box only to show what happens if AUTH_KEY leaks: Verifier B then accepts (worksheet step 12). Logic (equation): relay is a real DH partner twice, so it holds K1 and K2 and can decrypt, read and re-encrypt. Next question: why does nobody notice? -->

---

## Why neither side notices

- Alice's handshake **finishes fine** — she has *a* secret
- Bob's handshake **finishes fine** — he has *a* secret
- They do **not** share the same secret, and neither side can tell
- Nothing ties a public value to a **person**

![relay shares key K1 with Alice and a different key K2 with Bob. K1 is not equal to K2, so Alice and Bob never share a secret with each other, and neither can tell.](img/w5-keys-not-equal.svg)

```
K1 = shared(a, R1)       K2 = shared(b, R2)       K1 ≠ K2
```

```
RELAY: completed independent DH handshake with Alice (posing as Bob)
RELAY: completed independent DH handshake with Bob (posing as Alice)
RELAY INTERCEPTED: the launch code is 4471
BOB RECEIVED: the launch code is 4471
```

<!-- The punchline of the first run. Both handshakes are correct DH; the failure is that nobody checked who was on the other end. The log lines can swap order a little between runs; RELAY INTERCEPTED always comes after both "completed" lines. Real terminal output also has CryptographyDeprecationWarning lines (the library warns that this old kind of DH is on its way out). The worksheet filters them out. Logic: each handshake is correct on its own, so each side sees success; the only problem is that K1 and K2 differ and nothing checks who sent R1 and R2. Next question: what check would catch it? -->

---

## The fix: put a tag on the public value

- Alice and Bob already share a secret key, `AUTH_KEY`, from **before**
- Each side adds a **tag** (HMAC, from Week 3) to its public value
- The other side checks the tag **before** using the value
- `relay` does not know `AUTH_KEY`, so it cannot make a good tag — both sides stop

![Alice sends her public value A with a tag made from AUTH_KEY. The relay replaces A with its own value R but has no AUTH_KEY so it cannot make a matching tag. Bob recomputes the tag and compares: on a match he continues, on no match he stops with AUTH FAILED.](img/w5-tag-check.svg)

```
tA = HMAC(AUTH_KEY, A)                 # Alice sends (A, tA)
check:  t' == HMAC(AUTH_KEY, A') ?     # A' = the value that actually arrived
relay sends (R, t') without AUTH_KEY   ⇒   no match   ⇒   AUTH FAILED
```

```
RELAY: (fixed mode) attempted DH substitution with Alice (posing as Bob)
RELAY: (fixed mode) attempted DH substitution with Bob (posing as Alice)
AUTH FAILED - ABORTING          (alice)
AUTH FAILED - ABORTING          (bob)
```

<!-- Same relay code runs: it still tries to swap its own values in. The ONLY change is one tag check. Zero RELAY INTERCEPTED lines is the evidence. Say what the fix needs: Alice and Bob must share AUTH_KEY in advance, by a safe route. That is the "trust bootstrap" problem. If someone asks why not use AUTH_KEY to encrypt directly: a later leak of AUTH_KEY would open every recorded conversation; with a fresh DH each time (and the private numbers erased) it would not. Plain-words name: forward secrecy. Logic: the tag is a function of AUTH_KEY, so a changed public value cannot come with a matching tag unless the sender knows AUTH_KEY. The check does not say which of the two sent it; both hold AUTH_KEY. Next question: what do you do in the lab? -->

---

## 🔓 Lab today — what to do

![Three lab steps. A1: run the vulnerable pair; relay reads the message (RELAY INTERCEPTED). A2: run the fixed pair with the tag check; both sides print AUTH FAILED. A3: explain why it works and what it needs. Then hand in Wk05 student ID PDF at learn.zcr.ai/submit by Sunday 6 December 23:59.](img/w5-lab-flow.svg)

| Run | Command mode | What relay can do |
|---|---|---|
| vulnerable | no tag check | **read** the message |
| fixed | tag check | **nothing** — both sides stop |

- **Everyone (common 60):** A1 watch `relay` read the message · A2 run the tag check, see `AUTH FAILED` · A3 explain why it works and what it needs
- **Your form (40):** student ID ends **odd** → AIR-Sec · **even** → Conventional
- **Answer sheet:** Classroom → Week 05 → open the file for your form, type in the grey boxes, then File → Download → PDF
- Hand in `Wk05_<StudentID>.pdf` at `learn.zcr.ai/submit`

<!-- Exact commands are in the worksheet: one known-good path, copy and run. Build the image at home (needs internet) so class time goes to the lab. On Windows the worksheet gives findstr and PowerShell versions. The line "the launch code is 4471" is a fixed demo message, the same for everyone. Logic: the three steps check the equations. A1: K1 and K2 let relay read the message. A2: the tag check fails, so no key is derived and nothing is read. A3: say why, and what the fix needs (AUTH_KEY shared first). -->

---

## Takeaway

- DH lets two people agree on a secret **in the open**
- It stops people who **listen**, not a person **in the middle**
- A **tag** on each public value stops the middle person — if the key was shared **safely first**
- Next week: **AEAD** — encryption that checks for changes, and what an error message can give away

![A listener cannot break plain Diffie-Hellman. A person in the middle can. Adding a tag on each public value, with AUTH_KEY shared safely first, stops the person in the middle too.](img/w5-takeaway.svg)

```
DH:         listener fails,   man in the middle succeeds
DH + tag:   listener fails,   man in the middle fails    (if AUTH_KEY was shared first)
```

<!-- Land the spine. Cold-call: "name the one thing relay did not have in the second run." (AUTH_KEY.) Remind: Docker and laptop ready for next week too. Logic: DH removes the listener, the tag removes the middle person, and the price is a key shared in advance. -->
