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

<!-- Hook: ask "if I give you a valid signature (r, s), can you make a second, different-looking valid signature for the same message, without the private key?" Let them guess. The lab shows you can, in one subtraction. -->

---

## Today

- Signatures vs. MACs, and a **zero-knowledge** idea (Schnorr)
- ECDSA signature **malleability**: `(r, s)` has a valid twin `(r, n−s)`
- A bank that uses the **signature** as the transaction id pays twice
- The fix, **low-S**, and what it still does not solve
- 🔓 **Lab:** double-spend the vulnerable bank, then try the fixed one

<!-- Roadmap. Spine line to say out loud: "a valid signature does not mean the same transaction". Most of the class is the lab. -->

---

## Recap — Week 10

- **Hybrid encryption:** RSA locks a key, AES-GCM locks the messages
- A **nonce** must never repeat, or Eve reads without a key
- Today: **signatures** prove who sent something, and one design choice around them can break a bank

<!-- Bridge. Week 10 was confidentiality, this week is authenticity. -->

---

## Signatures vs. MACs

| | **MAC** | **Digital signature** |
|---|---|---|
| Create with | shared secret key | **private** key |
| Verify with | the *same* shared key | **public** key |
| Who can verify? | only key-holders | **anyone** with the public key |

**Why PKI uses signatures:** a stranger can verify your claim with your public key. A MAC cannot do that, because checking it needs the secret that creates it.

<!-- Worksheet Q1. Ask: "why can't a MAC secure HTTPS certificates?" A CA cannot hand its signing key to every browser. -->

---

## Proving you know a secret (Schnorr)

Peggy proves she knows a secret `x` **without sending it**:

1. Peggy sends a **commitment** (from a fresh random value)
2. Victor sends a random **challenge**
3. Peggy sends a **response** that only the holder of `x` can compute

- Victor becomes sure Peggy knows `x`, and learns nothing about `x`
- A recording is **useless**: next time the challenge is different

<!-- Worksheet Q4 and the AIR-Sec EiPE. Three arrows on the board. Fiat-Shamir (replace the live challenge with a hash) is only a one-line mention here and an optional question. Do not generalise it to every signature scheme. -->

---

## The break: the signature has a twin

**Every valid ECDSA signature `(r, s)` has a valid twin `(r, n − s)`**

- Same message, same key, still **verifies True**, but **different numbers**
- Nobody needs the private key to make it: only the public number `n`
- A textbook-secure primitive (nobody can forge a **new** message) with a real-system failure: the signature is **not unique**

<!-- CWE-347 and CWE-345. Worksheet steps 1 and 2: bank.py vuln sign prints the twin and the two different txids. ECDSA is not broken: the twin signs the SAME message. The mistake is treating the signature as the identity of the transaction. -->

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

<!-- Worksheet steps 4 and 5. This is exactly the line the students see in vulnerable_app.py. Every check passes: the signature is valid both times. -->

```sim
ecdsa-malleability
```

<!-- The sim computes n − s with real arithmetic and hashes both ids with real SHA-256. Use it for 3 to 4 minutes before the lab. -->

---

## The fix: low-S

```python
if not is_low_s(s):      # fixed_app.py
    return 403           # BIP-62 / BIP-146
```

- Of `(r, s)` and `(r, n−s)`, **exactly one** has a small `s` (low-S)
- The bank accepts only that one: the twin gets **`403`**
- Worksheet steps 7 to 9: `fixed pay twin` → `403`

<!-- Worksheet steps 7, 8, 9. In the lab the fixed bank's /sign always returns the low-S form, so the first withdrawal works and the twin fails. -->

---

## Low-S is not the whole fix

- Low-S stops **this** twin only
- Signing the same message again gives a **new** valid low-S signature, so a bank that still hashes the signature **pays again**
- A better transaction id: the **message + public key**, or a **unique number inside the signed message**

<!-- Worksheet step 10 (the optional second fixed sign + pay original shows total 200 and a flag on the fixed bank). MtGox: the historical claim that malleability caused the collapse is disputed (Decker and Wattenhofer measured much less impact), so do not say it caused the collapse. -->

---

## 🔓 Lab today — what to do

| Bank | Port | Twin signature |
|---|---|---|
| `vuln` | `:8102` | **accepted** (pays twice) |
| `fixed` | `:8103` | **rejected** (`403`) |

- **Everyone (common 60):** A1 get a signature and its twin · A2 pay with the original, replay it, pay with the twin · A3 the fixed bank says no, then find the `is_low_s` line
- **Your form (40):** student ID ends **odd** → Conventional · **even** → AIR-Sec
- **Answer sheet:** Classroom → Week 11 → file for your form → type in the grey boxes → File → Download → PDF
- Hand in `Wk11_<StudentID>.pdf` at `learn.zcr.ai/submit`

<!-- Exact commands are in the worksheet. Do the whole lab without restarting: a restart gives each bank a new key and a zero balance. Start Docker early and wait for "Running on" 8102 and 8103. -->

---

## Takeaway

- Every valid ECDSA signature has a **twin**: valid, different, no key needed
- A signature is **not** the identity of a transaction: do not use it as the id
- **Low-S** closes this twin, but the id should come from the **signed message**
- Next week: **TLS** (certificates and signatures at work)

<!-- Land the spine: "a valid signature does not mean the same transaction". Cold-call: "what did the vulnerable bank use as the transaction id, and why did the twin get through?" Remind them the CryptoVault milestone is reviewed in the feedback block. -->
