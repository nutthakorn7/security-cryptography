---
marp: true
theme: default
paginate: true
header: "Cryptography and Network Security · Week 15"
---

<!-- Delivery: 100-minute lab session. 10 min Week 14 retrieval + 10 min brief + 60 min practice + 15 min feedback + 5 min evidence capture. Short talk, then the lab (lamport.py and exploit.py inside Docker). Everyone completes the common 60 plus the assigned Conventional 40 or AIR-Sec 20/10/10. The viva is formative, no extra points. -->

# Week 15
## Post-quantum cryptography — a one-time signature used twice
Cryptography and Network Security · Nutthakorn Chalaemwongwan

<!-- Hook: ask "if a large quantum computer existed today, is a TLS session you sent an hour ago already broken?" Answer: only if someone recorded it (harvest now, decrypt later). Bridge from Week 14: authentication proved who you talk to; a signature proves what was said and that it was not changed, and the maths behind today's signatures has a quantum shelf life. Today: why quantum breaks RSA/ECC but not AES/SHA, and a signature so simple that its whole private key falls out the moment you misuse it once. About 2 minutes. -->

---

## Today

- A **10-minute quiz** on Week 14 to start (one question at a time)
- The quantum threat: **Shor** vs **Grover**, and **harvest now, decrypt later**
- The four **PQC families**, and what ML-KEM and ML-DSA are for
- **Lamport** one-time signatures — and the one-time-only rule
- 🔓 **Lab:** sign twice, take the private key, forge the admin signature, then watch the fixed server refuse

<!-- Roadmap. Say the spine line out loud: "textbook-secure primitive, real-system failure". Two identical servers run the same Lamport scheme: one reuses its key, one does not. Most of the class is the lab, not these slides. The scored Week 15 quiz opens in Week 16. -->

---

## Why quantum breaks (some) crypto

- **Shor's algorithm** solves factoring and discrete log → breaks **RSA and elliptic curves** outright
- **Grover's algorithm** is a square-root speed-up for search → only **halves** symmetric and hash security
- Cheap fix for Grover: **double the key or output length** (AES-256 stays strong)

<!-- Worksheet Q1. The distinction students must get: Shor is a real break (no key length saves RSA/ECC), Grover is a dent. Ask: "if Grover roughly halves AES-256's strength, is AES-256 still safe after quantum?" (yes). About 5 minutes. -->

---

## Harvest now, decrypt later

- An attacker **records ciphertext today** and decrypts it once a quantum computer exists
- That makes migration urgent **now**, even though no large quantum computer exists yet
- Real today for data with a **long secrecy lifetime**: health records, state secrets, long-lived credentials

<!-- Worksheet Q2. The "why now" slide. Ask: "if your data must stay secret for 20 years and a quantum computer might exist in 15, when did you need to have migrated?" (already). The optional hndl/ companion lab makes this concrete for key exchange; this week's required lab is the signature half of PQC. About 4 minutes. -->

---

## The four PQC families

- **Lattice-based** — **ML-KEM** (Kyber, a KEM) and **ML-DSA** (Dilithium, a signature)
- **Hash-based** — Lamport, XMSS, SPHINCS+ ← **this week**
- **Code-based** — Classic McEliece
- **Multivariate** — UOV (a research candidate, not a NIST standard)
- NIST 2024: **FIPS 203** (ML-KEM) · **FIPS 204** (ML-DSA) · **FIPS 205** (SLH-DSA / SPHINCS+)

<!-- Worksheet Q4 and the optional Q5. Name the families; do not teach lattice maths. KEM vs signature: a KEM agrees a shared key (TLS handshake), a signature vouches for data or a certificate. Hash-based signatures rest only on a hash, which Grover only dents; Lamport (1979) is the ancestor of SPHINCS+. About 4 minutes. -->

---

## Lamport one-time signatures

- Private key: **two secret tokens per message bit**
- Public key: the **hash** of every token
- To sign bit *i*, reveal the token for that bit's value (0 or 1)
- Anyone can check: **hash the token, compare with the public key**
- The toy relies on hash preimage resistance **and** on using the key **once**

<!-- Worksheet Step 1 (read). Build a 4-bit example on the board. In the lab a message is 32 bits written as 8 hex digits, signed directly with no pre-hash so every bit is controllable. Say "token" in class; the code and the key call it a preimage. About 5 minutes. -->

---

## What one signature reveals

- One signature reveals **exactly one token per bit** — the one matching the message
- The **other** token for each bit stays secret
- Lab check (bit 0, message `00000000`): the hash matches `pk[0][0]` but not `pk[0][1]`
- One signature ⇒ **half** the key is known, which is not enough to forge a different message

<!-- Worksheet Steps 2 and 3, done live: docker compose exec vulnerable python lamport.py sign 00000000. Ask: "is this fine if the key only ever signs one message?" (yes, hence one-time). About 5 minutes. -->

---

## The break: sign twice and the key falls out

- Sign `00000000` **and** its exact opposite `ffffffff`
- They differ in **every** bit → together they reveal **both** tokens for **all 32** positions
- That is the **whole private key**: no brute force
- Then build a signature on the admin message `0xA5A5C3C3`, which the server refused to sign

![Two zones, top to bottom. Top: the server holds one Lamport keypair; for each of the thirty-two bit positions two secret tokens are hashed into a published pair. Middle: the same reused key answers two sign requests, message zero and its bitwise complement all-ones, revealing every zero token and every one token. Bottom: the attacker, holding the complete private key, picks the matching token for each bit of the admin message it was never allowed to sign, assembles a forged signature, and submits it to the admin endpoint, which accepts it because verification only checks the signature against the public key.](img/lamport-key-reuse.svg)

```sim
lamport-reuse
```

<!-- Worksheet Steps 4, 5 and 6. The aha slide. Run the sim live here (it computes real SHA-256 and the same sign, verify and one-time logic as the two servers); then do the steps with lamport.py: sign ffffffff, both 0, forge. Ask: "why the opposite message, not any second message?" (every bit differs, so nothing is wasted). The server refuses to sign the admin message directly on both apps; the forgery is assembled offline. About 8 minutes. -->

---

## The fix: refuse the second signature

- `fixed_app.py`: the key signs **once**; a second `/sign` → `403`
- **No new maths**: only a usage rule (`_signed_message` remembers the first message)
- `verify()` and `/admin` are unchanged; signature checking was never the flaw
- The server refuses even a repeat of the **same** message; a real signer returns the stored signature for a retry, or uses a fresh key

<!-- Worksheet Steps 7 to 10. Run exploit.py ONCE: it repeats the vulnerable attack and then runs the identical attack on the fixed server (second sign refused, forgery rejected). Step 8: grep -n "_signed_message" fixed_app.py shows the guard; the same grep on vulnerable_app.py prints nothing. Ask: "why refuse even a duplicate of the same message?" (a trivial rule is easy to enforce correctly; an identical deterministic repeat reveals no new token, but the toy keeps it simple). A second run of exploit.py prints FAIL on the fixed server because its one signature is spent: restart the lab. About 6 minutes. -->

---

## Beyond "one signature ever"

- **Stateful** (XMSS, LMS): a tree of one-time keys, and the signer **must track** which leaf was used
- **Stateless** (SPHINCS+ / SLH-DSA, FIPS 205): a huge tree with pseudorandom key choice, so reuse is negligible
- **Crypto-agility**: be able to swap algorithms without a rewrite (for example hybrid classical + ML-KEM)

<!-- Worksheet Step 10 and the optional Q6, Q7. Stateful schemes make state loss an operational risk: a VM snapshot rollback replays old state and reuses a key. Ask: "if ECC were broken tomorrow, how long would it take your system to switch algorithms?" That is your crypto-agility score. About 4 minutes. -->

---

## 🔓 Lab today — what to do

| Server | Port | Second signature? |
|---|---|---|
| `vulnerable` | `:8100` | **allowed** (the bug) |
| `fixed` | `:8101` | **refused** (`403`) |

- **Everyone (common 60):** A1 one signature, half the key · A2 sign the opposite, recover the key, forge the admin signature · A3 the fixed server refuses, and how far the fix goes
- **Your form (40):** student ID ends **odd** → AIR-Sec · **even** → Conventional
- **Answer sheet:** Classroom → Week 15 → open the file for your form, type in the grey boxes, then File → Download → PDF
- Hand in `Wk15_<StudentID>.pdf` at `learn.zcr.ai/submit` with the code from your KMITL email, by **Sun 14 Feb, 23:59**
- Do the lab with the lab started **once**, in order. Type the `exploit.py` step only once. No Python needed on your computer: everything runs in Docker

<!-- Exact commands are in the worksheet and the answer sheet: copy and run. Start Docker early and wait for "Running on" 8100 and 8101 in the logs (Prep step 6). The commands are docker compose exec vulnerable python lamport.py ... on both Windows and Mac. If port 8100 is busy on a student's computer, Docker says "port is already allocated": close the other program. The optional hndl/ companion lab adds no points. -->

---

## Takeaway

- **Shor** breaks RSA and elliptic curves; **Grover** only dents AES and SHA
- A signature **and its opposite** hand over the whole toy private key
- The fix is a **usage rule**, not a bigger algorithm: a secure scheme can still be used insecurely
- Next week: the **capstone studio**, putting the term's primitives together

<!-- Land the spine: "textbook-secure primitive, real-system failure". Cold-call: "name the key-state mistake and say why refusing the second signature fixes it." CWE-323 (reuse in encryption) is only an analogy here. Remind them: Docker and laptop ready for next week too. -->
