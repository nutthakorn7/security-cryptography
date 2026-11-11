---
marp: true
theme: default
paginate: true
header: "Cryptography and Network Security · Week 5"
---

# Week 5
## Key Exchanges (Diffie-Hellman, MITM on unauthenticated DH)
Cryptography and Network Security · Nutthakorn Chalaemwongwan

<!-- Hook: ask "if Alice and Bob have never met and the network is public, how do they agree on a secret key without an eavesdropper learning it?" Let them sit with it for 30 sec — that's the whole lecture. This week's spine: DH is a textbook-secure primitive; run it *unauthenticated* over a network an active attacker controls and it fails completely, invisibly.  -->

---

## Today

**100-minute class:** 10 Week 4 recap quiz · 10 brief · 60 shared practice · 15 debrief · 5 capture.
**Assessment:** common 60 + assigned Conventional written 40 **or** AIR-Sec 20/10/10.
Preparation and detailed write-up are outside the contact block. The opening quiz reviews
Week 4; the Week 5 quiz is taken at the start of Week 6.

<!-- The full deck is a teaching/reference bank, not an additional lecture block.
Use the core explanation for the 10-minute brief and just-in-time guidance during practice;
assign the remaining deep dives as preparation or follow-up. Viva is formative, with no
separate points or automatic-zero rule. -->

- Why a key *exchange*, not just "send a key"
- Diffie-Hellman: the math, and why it's hard to break passively
- The active-attacker gap: MITM on unauthenticated DH
- The fix: authenticate the DH public keys (HMAC), keep forward secrecy
- 🕵️ Signature game: **The Silent Third Wheel**

<!-- Roadmap,  Flag the lab up front: they'll run a real invisible MITM against two Python services, then watch one HMAC tag shut it down with no other code change. Same spine every week: sound primitive, real-system failure, correct construction. -->

---

## Recap — Week 4

- AES block-cipher modes: ECB leaks patterns, CBC needs a random IV, GCM gives you authentication too
- Week 4 assumed Alice and Bob **already share a key**
- Week 5's question: how do they *get* that shared key in the first place — over a network anyone can watch?

<!-- Bridge from W4. W4 = protect data once you have a key. W5 = how you agree on that key over an open channel without handing it to an eavesdropper. This is the missing precondition from last week.  -->

---

## The problem: sharing a secret over a public channel

- Alice and Bob want a shared symmetric key for AES
- They've never met; the only channel is the open network
- **Naive idea:** just send the key. What goes wrong?
- Anyone watching the wire (an eavesdropper) now has it too

<!-- Ask: "why can't Alice just email Bob the AES key?" Let students find it: a passive eavesdropper reads it in transit, game over. This motivates *why* a key exchange protocol exists — Q1 on the worksheet asks exactly this.  -->

---

## Diffie-Hellman — the idea

- Public, shared: a large prime `p` and generator `g`
- Alice picks secret `a`, sends `g^a mod p`
- Bob picks secret `b`, sends `g^b mod p`
- Both compute the same shared secret: `g^(ab) mod p`
- An eavesdropper sees `g^a`, `g^b`, `p`, `g` — but not `a`, `b`, or `g^(ab)`

<!-- Walk the algebra on the board. Emphasize: nobody ever transmits the secret itself, only public values derived from it. This is the "textbook-secure" half of the spine — against a purely passive eavesdropper, this genuinely works.  -->

---

## Why an eavesdropper can't recover it

- Recovering `a` from `g^a mod p` = the **discrete logarithm problem**
- No efficient algorithm known for a well-chosen, large prime `p`
- This week's lab uses **RFC 3526 Group 14**: a standard 2048-bit MODP prime
- Use a vetted group; its size and structure matter. Do not invent your own parameters.

<!-- Discrete-log hardness is why DH resists a passive eavesdropper in a vetted group. Detailed parameter and subgroup questions are optional this week. -->

---

## But DH answers the wrong question

- Plain DH lets each pair of participants establish a secret that a **passive eavesdropper** cannot feasibly compute
- It gives **neither side a way to check who they just agreed it with**
- "Whoever answers when I dial Bob's address" ≠ "Bob"
- That gap is everything an **active** attacker needs

<!-- The pivot slide — this is the spine's "real-system failure" half arriving. Passive vs. active is the crux: DH secures the math, not the identity. Worksheet Q2/Q3 ask students to reason about exactly this gap.  -->

---

## Meet the lab: Alice, Bob, and Relay

| Service | Role | What it does |
|---|---|---|
| `bob.py` | Server | Listens on `:5000`, DH handshake, decrypts one AES-GCM message |
| `alice.py` | Client | Connects to `PEER_HOST:PEER_PORT` — **`relay`, never `bob` directly** |
| `relay.py` | Attacker | Sits on the network path between them |

- The premise **is** the lesson: Alice's peer address is `relay`, not `bob`

<!-- Set up the lab topology before the attack. Stress the premise line — an active attacker who controls the network path can simply BE the address you dial. This is CWE-300 (Channel Accessible by Non-Endpoint) made concrete.  -->

---

## The attack: two handshakes, one puppet-master

1. Relay runs a full DH handshake with Alice — **posing as Bob**
2. Relay runs a second, completely independent DH handshake with Bob — **posing as Alice**
3. Alice and Relay share one secret; Bob and Relay share another. Relay alone holds **both**
4. It decrypts Alice's AES-GCM message with the Alice-side key, logs it, re-encrypts the same plaintext under the Bob-side key, forwards it

<!-- Walk relay.py's handle_mitm() step by step. Key insight for viva prep (worksheet Part 2d, viva Q1): why TWO handshakes, not one? Because relay must be a real, independent DH peer to *each* side — that's what makes both handshakes complete cleanly with no error.  -->

![Two independent Diffie-Hellman handshakes run side by side at the top of the diagram: on the left, Alice exchanges public values with Relay posing as Bob and both sides honestly derive the identical shared secret K_A, while on the right, Relay posing as Alice exchanges public values with Bob and both sides honestly derive a different shared secret K_B, with nothing linking K_A to K_B and neither side ever comparing them; both secrets then feed straight down into Relay in the middle of the diagram, the only party holding both keys, which decrypts Alice's message with K_A to expose the plaintext, re-encrypts that same plaintext with K_B, and forwards it down to Bob, who decrypts it successfully and never suspects a substitution occurred.](img/dh-mitm.svg)

```sim
dh-mitm
```

<!-- The sim runs a REAL DH handshake — actual BigInt modular exponentiation over a small verified safe prime, not a scripted result — so Alice's and Relay's independently-computed shared secrets are genuinely equal, and Alice's key vs Bob's key are genuinely different, live on screen. What's illustrative: the session-key derivation, the message cipher, and the pubkey-authentication tag are toy mixing functions standing in for real SHA-256/AES-GCM/HMAC, same simplification Week 3's mac-extend sim made for its hash — say so explicitly. Run it live right after these bullets, before "Why neither side notices": the three presets are just different messages, same mechanic. The "has AUTH_KEY leaked to Relay?" checkbox previews next fix slide's Verifier B — leave it unchecked here (matches this slide's vulnerable-mode story); come back to it, checked, once you reach the HMAC fix to make the viva Q3 nuance ("the fix is only as strong as AUTH_KEY's secrecy") land visually instead of just verbally.  -->

---

## Why neither side notices

- Alice's handshake completes successfully — she has *a* shared secret
- Bob's handshake completes successfully — he has *a* shared secret
- Alice and Bob do not share the *same* secret, and neither side knows that
- No independently trusted tag or signature binds the public key to an identity
- **CWE-322** — Key Exchange without Entity Authentication

<!-- The punchline of the vulnerable run. Both handshakes are individually "textbook correct" DH — the failure is entirely that nobody authenticated *who* was on the other end. This is CWE-322, stated verbatim from the README/worksheet.  -->

---

## Watch it happen (vulnerable mode)

```
week05-relay | RELAY: completed independent DH handshake with Alice (posing as Bob)
week05-alice | ALICE: sent encrypted message ('the launch code is 4471')
week05-relay | RELAY: completed independent DH handshake with Bob (posing as Alice)
week05-relay | RELAY INTERCEPTED: the launch code is 4471
week05-bob   | BOB RECEIVED: the launch code is 4471
```

- Container log interleaving varies run to run — the first two lines can swap; `RELAY INTERCEPTED` always follows both `RELAY: completed...` lines (same-container stdout order, can't invert) and held before `BOB RECEIVED` in every run observed, though that pair spans two containers
- Real terminal output also interleaves `CryptographyDeprecationWarning` (FFDH) lines from the `cryptography` library — expected noise, not a sign anything broke

<!-- Read the log with them line by line — this is exactly what they'll capture as lab evidence. Ask: "which two lines have to appear before RELAY INTERCEPTED, and why does relay need both first?" (It needs the Alice-side key to decrypt AND to still be mid-handshake with Bob to forward on.) Verified by running the stack repeatedly: the first two lines (RELAY completed w/ Alice, ALICE sent) occasionally swap order — container log interleaving, not a bug. RELAY INTERCEPTED reliably follows both RELAY: completed lines because those three come from relay's own sequential stdout; RELAY INTERCEPTED → BOB RECEIVED is a cross-container pair that held in every run tested but isn't structurally guaranteed the way the same-container ordering is. Don't let a swapped top pair read as "something's wrong."  -->

---

## The fix: authenticate the public key, not the channel

- Each side computes an **HMAC-SHA256 tag** over its DH public value using the pre-shared `AUTH_KEY`
- The peer verifies the tag **before** deriving any session key
- `relay` doesn't have `AUTH_KEY` — it can still try the identical substitution, but it can only send a junk tag
- Verification fails → both sides print `AUTH FAILED - ABORTING` and exit

<!-- The correct construction. Emphasize: same code path in relay.py runs (handle_mitm_signed) — relay still generates DH keypairs and still tries to splice in. The ONLY thing that changes is one HMAC check. Cheap fix, total defeat of the attack.  -->

---

## What the fix does *not* give up

- DH still runs fresh for each session
- If the ephemeral DH secrets are erased, a later leak of `AUTH_KEY` alone does not reveal past captured sessions
- The fix authenticates the exchange — it does **not** replace it
- Real protocols have their own authenticated handshake design; this lab isolates the identity check with a pre-shared MAC key

<!-- Ask why the fixed run still needs fresh DH. Using AUTH_KEY directly as the long-lived encryption key would expose past recorded traffic if it later leaked. With ephemeral DH secrets erased, a later AUTH_KEY leak alone does not reveal old DH session keys. This lab uses an HMAC tag over each public value, not a digital signature. -->

---

## Watch it fail (fixed mode)

```
week05-relay | RELAY: (fixed mode) attempted DH substitution with Alice (posing as Bob)
week05-alice | AUTH FAILED - ABORTING
week05-relay | RELAY: (fixed mode) attempted DH substitution with Bob (posing as Alice)
week05-bob   | AUTH FAILED - ABORTING
```

- Container log interleaving varies run to run — either line in each relay/AUTH-FAILED pair can print first
- Zero occurrences of `RELAY INTERCEPTED` — that absence *is* the evidence, regardless of ordering

<!-- Contrast directly with the vulnerable log. The worksheet gives a grep command for Mac/Linux and Select-String for PowerShell; both should count 0. Container log order can vary. Grade the two AUTH FAILED lines and zero interception count, not their order. -->

---

## Optional study — not assessed today

- **Weak/non-standard groups** and **public-key validation** are separate implementation concerns
- A small-subgroup attack is **not** the key-substitution MITM you ran
- No group-theory explanation or small-subgroup answer is required for Worksheet 5

<!-- Today's running demo is only the key-substitution MITM. Group validation is a separate topic for optional study; it is absent from the marked questions and EiPE. -->

---

## 🕵️ Signature game — The Silent Third Wheel

- Be the eavesdropper who becomes an **active puppet-master**
- Sit silently between Alice and Bob, run your own DH handshake with each
- Read their "secure" channel in the clear — they never notice
- Then watch **one HMAC tag** over the public key shut you out completely, no other code change

<!-- Sell the game before the lab. "You get to be the invisible third wheel in someone else's private conversation — then feel exactly how thin that privacy was." Both halves are the same relay.py, same attempt — only the outcome differs.  -->

---

## Lab today

- **Common 60:** Run both DH topologies and trace the relay's two independent handshakes and interception.
- Compare the control/fixed case, explain its limits, and capture your own evidence.
- **Conventional 40:** four short questions on the observed lab and its control, if assigned.
- **AIR-Sec 40:** Audit the AI 20 + plain-language two-secret explanation 10 + Prompt Problem 10, if assigned.
- Finish the detailed write-up after class; submit the PDF per SUBMISSION.md.
- Viva is formative/authenticity feedback within the rubric, with no separate points.

<!-- Preserve every worksheet question; students submit the common work and only their
assigned format. Shared demo flags are acceptable if no personal configuration is supplied. -->

---

## Key takeaways

- **Textbook-secure primitive, real-system failure:** DH's math defeats a passive eavesdropper — it says nothing about *who* you just agreed a secret with
- An active attacker who controls the network path exploits exactly that silence — two independent handshakes, invisible to both sides (CWE-322, CWE-300)
- The fix authenticates the exchange without sacrificing what DH is for: forward secrecy

<!-- Recap, 3 lines. Cold-call: "why does the fixed mode still run a fresh DH exchange every session instead of just using AUTH_KEY as the key?" (forward secrecy).  -->

---

# Questions?
Next week: Authenticated Encryption (AEAD)

<!-- Cliffhanger: "We just fixed authentication for a key exchange with a bolted-on HMAC. Next week we look at ciphers that build authentication in from the start." Remind them: worksheet PDF and their own captured logs are due at learn.zcr.ai/submit per SUBMISSION.md. -->
