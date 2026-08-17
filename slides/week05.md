---
marp: true
theme: default
paginate: true
header: "Security & Cryptography · Week 5"
---

# Week 5
## Key Exchanges (Diffie-Hellman, MITM on unauthenticated DH)
Security & Cryptography · Nutthakorn Chalaemwongwan

<!-- Hook: ask "if Alice and Bob have never met and the network is public, how do they agree on a secret key without an eavesdropper learning it?" Let them sit with it for 30 sec — that's the whole lecture. This week's spine: DH is a textbook-secure primitive; run it *unauthenticated* over a network an active attacker controls and it fails completely, invisibly. ~2 min. -->

---

## Today

- Why a key *exchange*, not just "send a key"
- Diffie-Hellman: the math, and why it's hard to break passively
- The active-attacker gap: MITM on unauthenticated DH
- The fix: authenticate the DH public keys (HMAC), keep forward secrecy
- 🕵️ Signature game: **The Silent Third Wheel**

<!-- Roadmap, 1 min. Flag the lab up front: they'll run a real invisible MITM against two Python services, then watch one HMAC tag shut it down with no other code change. Same spine every week: sound primitive, real-system failure, correct construction. -->

---

## Recap — Week 4

- AES block-cipher modes: ECB leaks patterns, CBC needs a random IV, GCM gives you authentication too
- Week 4 assumed Alice and Bob **already share a key**
- Week 5's question: how do they *get* that shared key in the first place — over a network anyone can watch?

<!-- Bridge from W4. W4 = protect data once you have a key. W5 = how you agree on that key over an open channel without handing it to an eavesdropper. This is the missing precondition from last week. ~2 min. -->

---

## The problem: sharing a secret over a public channel

- Alice and Bob want a shared symmetric key for AES
- They've never met; the only channel is the open network
- **Naive idea:** just send the key. What goes wrong?
- Anyone watching the wire (an eavesdropper) now has it too

<!-- Ask: "why can't Alice just email Bob the AES key?" Let students find it: a passive eavesdropper reads it in transit, game over. This motivates *why* a key exchange protocol exists — Q1 on the worksheet asks exactly this. ~4 min. -->

---

## Diffie-Hellman — the idea

- Public, shared: a large prime `p` and generator `g`
- Alice picks secret `a`, sends `g^a mod p`
- Bob picks secret `b`, sends `g^b mod p`
- Both compute the same shared secret: `g^(ab) mod p`
- An eavesdropper sees `g^a`, `g^b`, `p`, `g` — but not `a`, `b`, or `g^(ab)`

<!-- Walk the algebra on the board. Emphasize: nobody ever transmits the secret itself, only public values derived from it. This is the "textbook-secure" half of the spine — against a purely passive eavesdropper, this genuinely works. ~6 min. -->

---

## Why an eavesdropper can't recover it

- Recovering `a` from `g^a mod p` = the **discrete logarithm problem**
- No efficient algorithm known for a well-chosen, large prime `p`
- This week's lab uses **RFC 3526 Group 14**: a standard 2048-bit MODP prime
- Small or non-prime `p`, or a bad `g`, can make the DLP tractable — never invent your own parameters

<!-- Discrete log hardness is *why* DH resists a passive eavesdropper. Tie to worksheet Q4/Q5 (why p must be large and prime) and Q7 (custom/non-standard groups are dangerous). Point out: this lab's common.py hardcodes RFC 3526 Group 14 — never roll your own. ~5 min. -->

---

## But DH answers the wrong question

- DH gives Alice and Bob a secret no **eavesdropper** can compute
- It gives **neither side a way to check who they just agreed it with**
- "Whoever answers when I dial Bob's address" ≠ "Bob"
- That gap is everything an **active** attacker needs

<!-- The pivot slide — this is the spine's "real-system failure" half arriving. Passive vs. active is the crux: DH secures the math, not the identity. Worksheet Q2/Q3 ask students to reason about exactly this gap. ~4 min. -->

---

## Meet the lab: Alice, Bob, and Relay

| Service | Role | What it does |
|---|---|---|
| `bob.py` | Server | Listens on `:5000`, DH handshake, decrypts one AES-GCM message |
| `alice.py` | Client | Connects to `PEER_HOST:PEER_PORT` — **`relay`, never `bob` directly** |
| `relay.py` | Attacker | Sits on the network path between them |

- The premise **is** the lesson: Alice's peer address is `relay`, not `bob`

<!-- Set up the lab topology before the attack. Stress the premise line — an active attacker who controls the network path can simply BE the address you dial. This is CWE-300 (Channel Accessible by Non-Endpoint) made concrete. ~4 min. -->

---

## The attack: two handshakes, one puppet-master

1. Relay runs a full DH handshake with Alice — **posing as Bob**
2. Relay runs a second, completely independent DH handshake with Bob — **posing as Alice**
3. Relay now holds two different shared secrets: one per side
4. It decrypts Alice's AES-GCM message with the Alice-side key, logs it, re-encrypts the same plaintext under the Bob-side key, forwards it

<!-- Walk relay.py's handle_mitm() step by step. Key insight for viva prep (worksheet Part 2d, viva Q1): why TWO handshakes, not one? Because relay must be a real, independent DH peer to *each* side — that's what makes both handshakes complete cleanly with no error. ~6 min. -->

![Two independent Diffie-Hellman handshakes run side by side at the top of the diagram: on the left, Alice exchanges public values with Relay posing as Bob and both sides honestly derive the identical shared secret K_A, while on the right, Relay posing as Alice exchanges public values with Bob and both sides honestly derive a different shared secret K_B, with nothing linking K_A to K_B and neither side ever comparing them; both secrets then feed straight down into Relay in the middle of the diagram, the only party holding both keys, which decrypts Alice's message with K_A to expose the plaintext, re-encrypts that same plaintext with K_B, and forwards it down to Bob, who decrypts it successfully and never suspects a substitution occurred.](img/dh-mitm.svg)

```sim
dh-mitm
```

<!-- The sim runs a REAL DH handshake — actual BigInt modular exponentiation over a small verified safe prime, not a scripted result — so Alice's and Relay's independently-computed shared secrets are genuinely equal, and Alice's key vs Bob's key are genuinely different, live on screen. What's illustrative: the session-key derivation, the message cipher, and the pubkey-authentication tag are toy mixing functions standing in for real SHA-256/AES-GCM/HMAC, same simplification Week 3's mac-extend sim made for its hash — say so explicitly. Run it live right after these bullets, before "Why neither side notices": the three presets are just different messages, same mechanic. The "has AUTH_KEY leaked to Relay?" checkbox previews next fix slide's Verifier B — leave it unchecked here (matches this slide's vulnerable-mode story); come back to it, checked, once you reach the HMAC fix to make the viva Q3 nuance ("the fix is only as strong as AUTH_KEY's secrecy") land visually instead of just verbally. ~5 min. -->

---

## Why neither side notices

- Alice's handshake completes successfully — she has *a* shared secret
- Bob's handshake completes successfully — he has *a* shared secret
- Neither is the *same* secret, and neither side ever checks that
- No MAC, no signature, nothing binds the public key to an identity
- **CWE-322** — Key Exchange without Entity Authentication

<!-- The punchline of the vulnerable run. Both handshakes are individually "textbook correct" DH — the failure is entirely that nobody authenticated *who* was on the other end. This is CWE-322, stated verbatim from the README/worksheet. ~4 min. -->

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

<!-- Read the log with them line by line — this is exactly what they'll capture as lab evidence. Ask: "which two lines have to appear before RELAY INTERCEPTED, and why does relay need both first?" (It needs the Alice-side key to decrypt AND to still be mid-handshake with Bob to forward on.) Verified by running the stack repeatedly: the first two lines (RELAY completed w/ Alice, ALICE sent) occasionally swap order — container log interleaving, not a bug. RELAY INTERCEPTED reliably follows both RELAY: completed lines because those three come from relay's own sequential stdout; RELAY INTERCEPTED → BOB RECEIVED is a cross-container pair that held in every run tested but isn't structurally guaranteed the way the same-container ordering is. Don't let a swapped top pair read as "something's wrong." ~4 min. -->

---

## The fix: authenticate the public key, not the channel

- Each side computes **HMAC-SHA256(AUTH_KEY, public_key_bytes)** and sends the tag alongside its DH public value
- The peer verifies the tag **before** deriving any session key
- `relay` doesn't have `AUTH_KEY` — it can still try the identical substitution, but it can only send a junk tag
- Verification fails → both sides print `AUTH FAILED - ABORTING` and exit

<!-- The correct construction. Emphasize: same code path in relay.py runs (handle_mitm_signed) — relay still generates DH keypairs and still tries to splice in. The ONLY thing that changes is one HMAC check. Cheap fix, total defeat of the attack. ~5 min. -->

---

## What the fix does *not* give up

- DH still runs fresh, every session — the session key is still **ephemeral**
- That means **forward secrecy**: if `AUTH_KEY` leaks next year, past captured traffic is still safe
- The fix authenticates the exchange — it does **not** replace it
- Real systems (TLS, SSH) authenticate DH with signatures/certificates, not a shared MAC — same principle: *authenticate the exchange, don't just run it*

<!-- Critical nuance students miss: why not just use AUTH_KEY as the encryption key and skip DH entirely (worksheet Part 2d, viva Q3)? Answer: you'd lose forward secrecy — a single leaked AUTH_KEY would retroactively break every past session. HMAC-signing the DH public key gets you authentication AND keeps ephemeral secrecy. ~5 min. -->

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

<!-- Contrast directly with the vulnerable log two slides ago. Same relay.py attempt, same structure, opposite outcome. Have them run `grep -c "RELAY INTERCEPTED"` on the fixed-mode logs and confirm it prints 0 — that's their required lab evidence. Verified by running the stack repeatedly: unlike vulnerable mode, BOTH pairs here (relay-attempted/alice-AUTH-FAILED, and relay-attempted/bob-AUTH-FAILED) flip order between runs with no dominant sequence — it's a genuine race, not just an occasional swap. Also expect CryptographyDeprecationWarning (FFDH) lines interleaved in. Don't grade or worry about line order here; only the two AUTH FAILED lines + zero RELAY INTERCEPTED matter. ~3 min. -->

---

## Not in today's demo — stays conceptual

- **Weak/non-standard groups** (small or non-prime `p`) — Q7
- **Missing public-key validation** — this lab's code does **not** validate `peer_y` against the group order — Q8
- **Small-subgroup confinement attack** — a malicious public key can collapse the "shared secret" to one of only a handful of possible values, letting an attacker leak bits of a private key — Q9 / EiPE Part 2b

<!-- Draw a hard line: today's running demo is ONLY the key-substitution MITM. These three are real, related DH pitfalls but this week's code doesn't exploit them — they're conceptual, covered by essay questions and the EiPE (Explain in Plain English) exercise. Don't let students conflate "no identity check" (what we ran) with "no input validation" (what we didn't). ~4 min. -->

---

## 🕵️ Signature game — The Silent Third Wheel

- Be the eavesdropper who becomes an **active puppet-master**
- Sit silently between Alice and Bob, run your own DH handshake with each
- Read their "secure" channel in the clear — they never notice
- Then watch **one HMAC tag** over the public key shut you out completely, no other code change

<!-- Sell the game before the lab. "You get to be the invisible third wheel in someone else's private conversation — then feel exactly how thin that privacy was." Both halves are the same relay.py, same attempt — only the outcome differs. ~3 min. -->

---

## Lab today

> 📋 **Worksheet 5** — `labs/week05-key-exchanges/worksheet.md` · Part 1 (10 essay Q's) + Part 2 (AIR-Sec: lab evidence, EiPE, Prompt Problem, viva)

- **Run, don't exploit-and-fix code** — this is a read/run/observe lab
- Vulnerable: `docker compose -f docker-compose.vulnerable.yml up --build` → capture `RELAY INTERCEPTED: the launch code is 4471`
- Fixed: `docker compose -f docker-compose.fixed.yml up --build` → capture both `AUTH FAILED - ABORTING` lines + confirm `grep -c "RELAY INTERCEPTED"` = 0
- **+ EiPE** (small-subgroup, plain English) **+ Prompt Problem** (critique an AI's MITM explanation) — see worksheet

<!-- The graded output. Unlike some weeks, code doesn't change here — the deliverable is captured evidence + identity proof (whoami/timestamp) + reasoning, not a patched repo. Remind them: which compose file they point -f at is the ONLY thing selecting vulnerable vs. fixed mode. ~4 min. -->

---

## Key takeaways

- **Textbook-secure primitive, real-system failure:** DH's math defeats a passive eavesdropper — it says nothing about *who* you just agreed a secret with
- An active attacker who controls the network path exploits exactly that silence — two independent handshakes, invisible to both sides (CWE-322, CWE-300)
- The fix authenticates the exchange without sacrificing what DH is for: forward secrecy

<!-- Recap, 3 lines. Cold-call: "why does the fixed mode still run a fresh DH exchange every session instead of just using AUTH_KEY as the key?" (forward secrecy). ~2 min. -->

---

# Questions?
Next week: Authenticated Encryption (AEAD)

<!-- Cliffhanger: "We just fixed authentication for a key exchange with a bolted-on HMAC. Next week we look at ciphers that build authentication in from the start." Remind them: worksheet + captured logs + identity proof due via Classroom/GitHub per SUBMISSION.md. ~1 min. -->
