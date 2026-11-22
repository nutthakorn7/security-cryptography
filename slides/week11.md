---
marp: true
theme: default
paginate: true
header: "Cryptography and Network Security · Week 11"
---

<!-- Delivery: 100-minute lab session. 10 retrieval review + 10 brief + 70 practice + 10 evidence. Short talk, then the lab (bank.py). Everyone completes the common 60 plus the assigned Conventional 40 or AIR-Sec 20/10/10. The viva is formative, no extra points. -->

# Week 11
## Digital signatures — the "twin" signature that pays the bank twice
Cryptography and Network Security · Nutthakorn Chalaemwongwan

<!-- Hook: ask "if I give you a valid signature (r, s), can you make a second, different-looking valid signature for the same message, without the private key?" Let them guess. The lab shows you can, in one subtraction. Logic of the deck: a signature proves who sent a message; the twin shows the signature is not unique, so it is not the identity of a transaction; a bank that uses it as the id pays twice; low-S closes this one twin; the id must come from the signed message. Each slide answers one question and ends with the next. -->

---

## Today

- Signatures vs. MACs, and a **zero-knowledge** idea (Schnorr)
- ECDSA signature **malleability**: `(r, s)` has a valid twin `(r, n−s)`
- A bank that uses the **signature** as the transaction id pays twice
- The fix, **low-S**, and what it still does not solve
- 🔓 **Lab:** double-spend the vulnerable bank, then try the fixed one

<!-- Roadmap. Spine line to say out loud: "a valid signature does not mean the same transaction". Most of the class is the lab. Logic: the first two bullets say what a signature is, the next two show how it breaks and how a bank is hurt, the last two show the fix and its limit; the lab walks the same order. -->

---

## Recap — Week 10

- **Hybrid encryption:** RSA locks a key, AES-GCM locks the messages
- A **nonce** must never repeat, or Eve reads without a key
- Today: **signatures** prove who sent something, and one design choice around them can break a bank

![Week 10 was hybrid encryption: RSA locks a key and AES-GCM locks the messages, so the data stays secret. Week 11 is digital signatures, which prove who sent something, and one design choice around a signature can make a bank pay twice.](img/w11-recap.svg)

<!-- Bridge. Week 10 was confidentiality, this week is authenticity. Logic: encryption hides a message but does not say who wrote it; a stranger can still send you a perfectly encrypted lie. Next question: how can anyone check who sent a message, without sharing a secret? -->

---

## Signatures vs. MACs

| | **MAC** | **Digital signature** |
|---|---|---|
| Create with | shared secret key | **private** key |
| Verify with | the *same* shared key | **public** key |
| Who can verify? | only key-holders | **anyone** with the public key |

**Why PKI uses signatures:** a stranger can verify your claim with your public key. A MAC cannot do that, because checking it needs the secret that creates it.

![Left, a MAC: Alice and Bob hold the same secret key k, so both can create and check a tag, but a stranger without k cannot check it. Right, a digital signature: the owner signs with a private key and anyone with the public key can verify it, so a stranger can check it too.](img/w11-sig-vs-mac.svg)

```
tag = mac(k, m)         ok = (tag == mac(k, m))     # the same secret k on both sides
sig = sign(sk, m)       ok = verify(pk, m, sig)     # only the owner has sk, anyone has pk
```

<!-- Worksheet Q1. Ask: "why can't a MAC secure HTTPS certificates?" A CA cannot hand its signing key to every browser. Logic: a MAC (Week 3) needs both sides to share k, so whoever can check can also forge; a signature splits the key in two, one half to create (sk) and one half to check (pk), so checking no longer gives the power to create. Next question: how can someone prove they hold the secret without showing it? -->

---

## Proving you know a secret (Schnorr)

Peggy proves she knows a secret `x` **without sending it**:

1. Peggy sends a **commitment** (from a fresh random value)
2. Victor sends a random **challenge**
3. Peggy sends a **response** that only the holder of `x` can compute

- Victor becomes sure Peggy knows `x`, and learns nothing about `x`
- A recording is **useless**: next time the challenge is different

![Peggy sends a commitment made from a fresh random value. Victor answers with a random challenge. Peggy sends a response that only the holder of the secret x can compute. Victor becomes sure she knows x, and x itself is never sent.](img/w11-schnorr.svg)

```
R = commit(k)             # Peggy: k is a fresh random value, only R is sent
c = challenge()           # Victor: a random number, chosen after R
s = respond(k, c, x)      # Peggy: only the holder of x can compute this
ok = check(R, c, s, X)    # Victor: X is the public value that goes with x
```

<!-- Worksheet Q4 and the AIR-Sec EiPE. Three arrows on the board. Fiat-Shamir (replace the live challenge with a hash) is only a one-line mention here and an optional question. Do not generalise it to every signature scheme. Logic: the response mixes the secret x with the fresh random k, so it proves knowledge of x and the random k hides x; a new challenge each time is why a recording is useless. This part is read only, the lab does not run Schnorr. Next question: real signatures are numbers too, so what exactly do they look like, and can they be changed? -->

---

## The break: the signature has a twin

**Every valid ECDSA signature `(r, s)` has a valid twin `(r, n − s)`**

- Same message, same key, still **verifies True**, but **different numbers**
- Nobody needs the private key to make it: only the public number `n`
- A textbook-secure primitive (nobody can forge a **new** message) with a real-system failure: the signature is **not unique**

![The attacker holds a valid signature (r, s). Subtracting s from the public curve order n gives the twin (r, n minus s), with no private key. Both signatures verify as true for the same message and the same key, but the numbers are different.](img/w11-twin.svg)

```
verify(pk, m, (r, s))    == True      # the owner's signature
s2 = n - s                            # only the public number n is needed
verify(pk, m, (r, s2))   == True      # a different signature, the same m
```

<!-- CWE-347 and CWE-345. Worksheet steps 1 and 2: bank.py vuln sign prints the twin and the two different txids. ECDSA is not broken: the twin signs the SAME message. The mistake is treating the signature as the identity of the transaction. Logic (derivation in words): the check builds a curve point from z/s and r/s (z = the message hash), so with n minus s both numbers change sign, the point is mirrored, and its x coordinate, which is what is compared with r, stays the same; that is why the twin passes. You do not need to prove it in class, the lab shows it with bank.py. Next question: what goes wrong in a real system that treats the signature as the id? -->

---

## Where it bites

A bank allows **one** withdrawal. To avoid paying twice it remembers a **txid**:

```python
txid = sha256(str(r) + str(s))      # vulnerable_app.py
if txid in seen: reject()
seen.add(txid); pay()
```

- Same signature again ⇒ same txid ⇒ `409`, caught ✅
- The **twin** ⇒ a **new** txid ⇒ paid again ❌ (`total_withdrawn` 200)

![One authorized withdrawal produces two valid-looking transaction ids. The attacker holds a valid signature (r, s) and computes its twin (r, n minus s) with only the public curve order n. Both verify against the same message and key, but they hash to two different transaction ids, so the bank processes the same authorization twice.](img/signature-malleability.svg)

<!-- Worksheet steps 4 and 5. This is exactly the line the students see in vulnerable_app.py. Every check passes: the signature is valid both times. Logic: the bank wants "one authorization, one payment", so it needs an id; it picked the cheapest thing it had, the signature; the twin is a new signature, so it is a new id. Next question: how does a bank refuse the twin? -->

```sim
ecdsa-malleability
```

<!-- The sim computes n − s with real arithmetic and hashes both ids with real SHA-256. Use it for 3 to 4 minutes before the lab. Logic: the sim shows the same two ids the lab prints, so students see the lab result before they run it. -->

---

## The fix: low-S

```python
if not is_low_s(s):      # fixed_app.py
    return 403           # BIP-62 / BIP-146
```

- Of `(r, s)` and `(r, n−s)`, **exactly one** has a small `s` (low-S)
- The bank accepts only that one: the twin gets **`403`**
- Worksheet steps 7 to 9: `fixed pay twin` → `403`

![The range of s runs from 0 to n. The lower half, up to n over 2, is low-S and the upper half is high-S. A signature and its twin sit mirrored around the middle, so exactly one of them is low-S. The fixed bank accepts the low one with 200 and refuses the high one with 403.](img/w11-low-s.svg)

```
accept (r, s) only if s <= n/2      # is_low_s(s) in fixed_app.py, else 403
# s and n - s are mirrored around n/2, so exactly one of the pair passes
```

<!-- Worksheet steps 7, 8, 9. In the lab the fixed bank's /sign always returns the low-S form, so the first withdrawal works and the twin fails. Logic: the twin always lands in the other half, so a rule that allows only one half leaves exactly one valid form of each pair; the txid can then no longer be changed by this subtraction. Next question: does one allowed form per pair mean one signature per message? -->

---

## Low-S is not the whole fix

- Low-S stops **this** twin only
- Signing the same message again gives a **new** valid low-S signature, so a bank that still hashes the signature **pays again**
- A better transaction id: the **message + public key**, or a **unique number inside the signed message**

![Left: if the bank still hashes the signature, signing the same message again gives a new valid low-S signature with a different transaction id, so it pays twice. Right: a transaction id taken from the signed message, such as the public key and a unique number inside the message, is the same every time, so the second one is refused.](img/w11-not-whole-fix.svg)

```
sign(sk, m) = (r1, s1)    sign(sk, m) = (r2, s2)     # a fresh random k each time, both low-S
txid = hash(pk, m)        # m holds a unique number, so the id does not depend on (r, s)
```

<!-- Worksheet step 10 (the optional second fixed sign + pay original shows total 200 and a flag on the fixed bank). MtGox: the historical claim that malleability caused the collapse is disputed (Decker and Wattenhofer measured much less impact), so do not say it caused the collapse. Logic: ECDSA signing uses a fresh random number k, so signing again gives a different valid signature that low-S cannot catch; the real fix is to stop using the signature as the id and take the id from the signed message, which no one can change without the key. Next question: what do I actually do in the lab? -->

---

## 🔓 Lab today — what to do

![Three lab steps. A1: ask the vulnerable bank on port 8102 for a signature and see its twin. A2: pay with the original signature, which gets 200, send it again, which gets 409, then pay with the twin, which gets 200 and a total of 200 with a flag. A3: on the fixed bank on port 8103 the twin gets 403. Then hand in Wk11 student ID PDF at learn.zcr.ai/submit by Sunday 17 January 2027, 23:59.](img/w11-lab-flow.svg)

| Bank | Port | Twin signature |
|---|---|---|
| `vuln` | `:8102` | **accepted** (pays twice) |
| `fixed` | `:8103` | **rejected** (`403`) |

- **Everyone (common 60):** A1 get a signature and its twin · A2 pay with the original, replay it, pay with the twin · A3 the fixed bank says no, then find the `is_low_s` line
- **Your form (40):** student ID ends **odd** → AIR-Sec · **even** → Conventional
- **Answer sheet:** Classroom → Week 11 → file for your form → type in the grey boxes → File → Download → PDF
- Hand in `Wk11_<StudentID>.pdf` at `learn.zcr.ai/submit`

<!-- Exact commands are in the worksheet. Do the whole lab without restarting: a restart gives each bank a new key and a zero balance. Start Docker early and wait for "Running on" 8102 and 8103. Logic: A1 shows the twin and its different id, A2 shows the replay caught (409) and the twin paid (total 200), A3 shows low-S refusing the twin (403) and where the one differing line is (is_low_s). -->

---

## Takeaway

- Every valid ECDSA signature has a **twin**: valid, different, no key needed
- A signature is **not** the identity of a transaction: do not use it as the id
- **Low-S** closes this twin, but the id should come from the **signed message**
- Next week: **TLS** (certificates and signatures at work)

![The vulnerable bank uses a hash of the signature as the transaction id, so the twin has a new id and is paid twice. A transaction id taken from the signed message is the same for the twin, so it would be refused.](img/w11-takeaway.svg)

```
txid = sha256(str(r) + str(s))    # twin ⇒ new id ⇒ paid twice
txid = hash(pk, m)                # twin ⇒ refused (m holds a unique number)
```

<!-- Land the spine: "a valid signature does not mean the same transaction". Cold-call: "what did the vulnerable bank use as the transaction id, and why did the twin get through?" Remind them the CryptoVault milestone is reviewed in the feedback block. Logic: valid and unique are different properties; a signature gives the first, so an id must come from something that is unique by design. Next: TLS puts signatures to work in certificates. -->
