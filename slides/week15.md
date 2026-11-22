---
marp: true
theme: default
paginate: true
header: "Cryptography and Network Security · Week 15"
---

<!-- Delivery: 100-minute lab session. 10 min Week 14 retrieval + 10 min brief + 60 min practice + 15 min feedback + 5 min evidence capture. Short talk, then the lab (lamport.py and exploit.py inside Docker). Everyone completes the common 60 plus the assigned Conventional 40 or AIR-Sec 20/10/10. The viva is formative, no extra points. Logic of the deck: signatures need maths that is hard to undo; a large quantum computer undoes some of it (Shor) and only dents the rest (Grover); recorded traffic makes that urgent now; the hash-based family is the simplest to see in a lab; the simplest hash-based signature (Lamport) is secure only if each key signs once; the lab breaks that rule and then enforces it. Each slide answers one question and ends with the next. -->

# Week 15
## Post-quantum cryptography — a one-time signature used twice
Cryptography and Network Security · Nutthakorn Chalaemwongwan

<!-- Hook: ask "if a large quantum computer existed today, is a TLS session you sent an hour ago already broken?" Answer: only if someone recorded it (harvest now, decrypt later). Bridge from Week 14: authentication proved who you talk to; a signature proves what was said and that it was not changed, and the maths behind today's signatures has a quantum shelf life. Today: why quantum breaks RSA/ECC but not AES/SHA, and a signature so simple that its whole private key falls out the moment you misuse it once. About 2 minutes. Logic: Week 14 showed who we talk to; the signature is the tool that proves what was said, so the next question is how long that proof stays safe. -->

---

## Today

![Five boxes in a row show today: the quantum threat of Shor and Grover, harvest now decrypt later, the four post-quantum families, the Lamport one-time signature, and the lab where you sign twice, forge the admin signature and watch the fixed server refuse.](img/w15-roadmap.svg)

- A **10-minute quiz** on Week 14 to start (one question at a time)
- The quantum threat: **Shor** vs **Grover**, and **harvest now, decrypt later**
- The four **PQC families**, and what ML-KEM and ML-DSA are for
- **Lamport** one-time signatures — and the one-time-only rule
- 🔓 **Lab:** sign twice, take the private key, forge the admin signature, then watch the fixed server refuse

<!-- Roadmap. Say the spine line out loud: "textbook-secure primitive, real-system failure". Two identical servers run the same Lamport scheme: one reuses its key, one does not. Most of the class is the lab, not these slides. The scored Week 15 quiz opens in Week 16. Logic: five steps, each one answers the question the one before leaves open: what does quantum break, why now, what replaces it, what is the simplest replacement, what happens if you misuse it. -->

---

## Why quantum breaks (some) crypto

![Shor algorithm makes factoring and discrete logarithms fast, so RSA and elliptic curves are broken and no key length saves them. Grover algorithm is only a square-root speed-up for search, so AES and SHA lose half their strength bits and doubling the length fixes it; AES-256 stays about 128-bit strong.](img/w15-shor-grover.svg)

- **Shor's algorithm** solves factoring and discrete log → breaks **RSA and elliptic curves** outright
- **Grover's algorithm** is a square-root speed-up for search → only **halves** symmetric and hash security
- Cheap fix for Grover: **double the key or output length** (AES-256 stays strong)

```
Shor:    factor(N), dlog(A)  ⇒  fast        # RSA, ECC: no key length saves them
Grover:  search 2^n          ⇒  2^(n/2)    # AES-256: about 128-bit strength
```

<!-- Worksheet Q1. The distinction students must get: Shor is a real break (no key length saves RSA/ECC), Grover is a dent. Ask: "if Grover roughly halves AES-256's strength, is AES-256 still safe after quantum?" (yes). About 5 minutes. Logic: Shor and Grover are two different algorithms with two different costs: Shor turns factoring and discrete log from impossible to fast, so the whole RSA/ECC idea fails; Grover only turns a search over 2^n keys into about 2^(n/2) steps, so a longer key repairs it. Next question: is any of this a problem before the machine exists? -->

---

## Harvest now, decrypt later

![Three steps on a timeline. Today an attacker records your encrypted traffic and keeps a copy. Years pass while the data still has to stay secret. On the day a large quantum computer exists the attacker decrypts the old copy. The lesson is to migrate before the recording, not after the quantum computer.](img/w15-hndl.svg)

- An attacker **records ciphertext today** and decrypts it once a quantum computer exists
- That makes migration urgent **now**, even though no large quantum computer exists yet
- Real today for data with a **long secrecy lifetime**: health records, state secrets, long-lived credentials

```
secrecy_years + migration_years > years_to_quantum   ⇒   already late   # rule of thumb
```

<!-- Worksheet Q2. The "why now" slide. Ask: "if your data must stay secret for 20 years and a quantum computer might exist in 15, when did you need to have migrated?" (already). The optional hndl/ companion lab makes this concrete for key exchange; this week's required lab is the signature half of PQC. About 4 minutes. Logic: if the data must stay secret for X years and the move to new crypto takes Y years, the move must start when X + Y is longer than the years until the quantum computer (Mosca's rule of thumb); a recording made today is already in the attacker's hands. Next question: what do we move to? -->

---

## The four PQC families

![Four post-quantum families as cards. Lattice-based gives ML-KEM, a key agreement, and ML-DSA, a signature. Hash-based gives Lamport, XMSS and SPHINCS+ and is the focus this week. Code-based gives Classic McEliece. Multivariate gives UOV, a research candidate and not a NIST standard. A KEM agrees a shared key and a signature vouches for data or a certificate.](img/w15-families.svg)

- **Lattice-based** — **ML-KEM** (Kyber, a KEM) and **ML-DSA** (Dilithium, a signature)
- **Hash-based** — Lamport, XMSS, SPHINCS+ ← **this week**
- **Code-based** — Classic McEliece
- **Multivariate** — UOV (a research candidate, not a NIST standard)
- NIST 2024: **FIPS 203** (ML-KEM) · **FIPS 204** (ML-DSA) · **FIPS 205** (SLH-DSA / SPHINCS+)

```
(ct, K) = encaps(pk)     K = decaps(sk, ct)        # KEM: agree a shared key
sig = sign(sk, m)        ok = verify(pk, m, sig)   # signature: vouch for data
```

<!-- Worksheet Q4 and the optional Q5. Name the families; do not teach lattice maths. KEM vs signature: a KEM agrees a shared key (TLS handshake), a signature vouches for data or a certificate. Hash-based signatures rest only on a hash, which Grover only dents; Lamport (1979) is the ancestor of SPHINCS+. About 4 minutes. Logic: the two equations are the two jobs: encaps/decaps agree a key for confidentiality, sign/verify vouch for data; today we take the hash-based family because its security rests on a hash only, so we can build it by hand. Next question: how does a signature built from a hash alone work? -->

---

## Lamport one-time signatures

![A four-bit example with message bits one, zero, one, one. For each bit position the secret key holds two tokens and the public key holds the hash of each. To sign, the signer reveals the token that matches the bit value. The verifier hashes the revealed token and compares it with the public key hash for that bit.](img/w15-lamport-idea.svg)

- Private key: **two secret tokens per message bit**
- Public key: the **hash** of every token
- To sign bit *i*, reveal the token for that bit's value (0 or 1)
- Anyone can check: **hash the token, compare with the public key**
- The toy relies on hash preimage resistance **and** on using the key **once**

```
pk[i][b] = H(sk[i][b])            # public key: hash of every token
sig[i]   = sk[i][bit_i(m)]        # reveal the token that matches bit i
H(sig[i]) == pk[i][bit_i(m)] ?    # verify, for every bit i
```

<!-- Worksheet Step 1 (read). Build a 4-bit example on the board. In the lab a message is 32 bits written as 8 hex digits, signed directly with no pre-hash so every bit is controllable. Say "token" in class; the code and the key call it a preimage. About 5 minutes. Logic: the public key is just the hashes of the secret tokens; revealing the token for a bit proves you hold the secret because nobody can invent a token that hashes to the published value (preimage resistance). Verification is one hash and one compare per bit. Next question: what does the verifier, or an attacker, now know about the key? -->

---

## What one signature reveals

![One signature on message all zeros reveals the zero token at each of the thirty-two bit positions. The one tokens stay secret. So the attacker knows 32 of the 64 tokens, which is half the key and not enough to sign a different message.](img/w15-one-signature.svg)

- One signature reveals **exactly one token per bit** — the one matching the message
- The **other** token for each bit stays secret
- Lab check (bit 0, message `00000000`): the hash matches `pk[0][0]` but not `pk[0][1]`
- One signature ⇒ **half** the key is known, which is not enough to forge a different message

```
sign(sk, "00000000")  ⇒  reveals sk[i][0] for all i     # known: 32 of 64 tokens
```

<!-- Worksheet Steps 2 and 3, done live: docker compose exec vulnerable python lamport.py sign 00000000. Ask: "is this fine if the key only ever signs one message?" (yes, hence one-time). About 5 minutes. Logic: each position has two tokens and a signature shows only the one that matches the bit, so a single signature uncovers 32 of the 64 tokens; the other half is exactly what a different message would need. Next question: what if the same key signs a second message? -->

---

## The break: sign twice and the key falls out

- Sign `00000000` **and** its exact opposite `ffffffff`
- They differ in **every** bit → together they reveal **both** tokens for **all 32** positions
- That is the **whole private key**: no brute force
- Then build a signature on the admin message `0xA5A5C3C3`, which the server refused to sign

```
bits(00000000) xor bits(ffffffff) = all ones      # every bit differs
sk[i][0] from sig(00000000), sk[i][1] from sig(ffffffff)   # 64 of 64 tokens
forged[i] = sk[i][bit_i(0xA5A5C3C3)]              # the admin signature
```

![Two zones, top to bottom. Top: the server holds one Lamport keypair; for each of the thirty-two bit positions two secret tokens are hashed into a published pair. Middle: the same reused key answers two sign requests, message zero and its bitwise complement all-ones, revealing every zero token and every one token. Bottom: the attacker, holding the complete private key, picks the matching token for each bit of the admin message it was never allowed to sign, assembles a forged signature, and submits it to the admin endpoint, which accepts it because verification only checks the signature against the public key.](img/lamport-key-reuse.svg)

```sim
lamport-reuse
```

<!-- Worksheet Steps 4, 5 and 6. The aha slide. Run the sim live here (it computes real SHA-256 and the same sign, verify and one-time logic as the two servers); then do the steps with lamport.py: sign ffffffff, both 0, forge. Ask: "why the opposite message, not any second message?" (every bit differs, so nothing is wasted). The server refuses to sign the admin message directly on both apps; the forgery is assembled offline. About 8 minutes. Logic: a second message that differs in every bit (the bitwise opposite) uncovers the token the first one hid, so 32 + 32 = 64 tokens, the whole key; with the whole key the attacker can reveal the right token for any bit pattern, including 0xA5A5C3C3. Next question: what is the smallest change that stops this? -->

---

## The fix: refuse the second signature

![Two servers compared. On the vulnerable server on port 8100 both signing requests return 200, so the key is recovered and the forgery is accepted. On the fixed server on port 8101 the first signing request returns 200 and the second returns 403 because the key was already used, so there is no second signature and the forgery is rejected. The fix is only a usage rule that remembers the first message.](img/w15-fix.svg)

- `fixed_app.py`: the key signs **once**; a second `/sign` → `403`
- **No new maths**: only a usage rule (`_signed_message` remembers the first message)
- `verify()` and `/admin` are unchanged; signature checking was never the flaw
- The server refuses even a repeat of the **same** message; a real signer returns the stored signature for a retry, or uses a fresh key

```
if _signed_message is not None:   # this key was already used
    return 403                    # refuse the second /sign
_signed_message = m              # remember the first message
```

<!-- Worksheet Steps 7 to 10. Run exploit.py ONCE: it repeats the vulnerable attack and then runs the identical attack on the fixed server (second sign refused, forgery rejected). Step 8: grep -n "_signed_message" fixed_app.py shows the guard; the same grep on vulnerable_app.py prints nothing. Ask: "why refuse even a duplicate of the same message?" (a trivial rule is easy to enforce correctly; an identical deterministic repeat reveals no new token, but the toy keeps it simple). A second run of exploit.py prints FAIL on the fixed server because its one signature is spent: restart the lab. About 6 minutes. Logic: the break needs a second signature, so the fix refuses it; the maths (sign, verify, /admin) is untouched, which shows the flaw was how the key was used. Next question: how do real systems sign many messages? -->

---

## Beyond "one signature ever"

![Two trees of one-time keys. Stateful schemes such as XMSS and LMS use leaves in order, so the signer must save which leaf was used and a lost state can reuse a key. Stateless SPHINCS+, standardised as SLH-DSA in FIPS 205, uses a huge tree and picks a leaf pseudorandomly so reuse is negligible. Crypto-agility means swapping algorithms without a rewrite.](img/w15-beyond.svg)

- **Stateful** (XMSS, LMS): a tree of one-time keys, and the signer **must track** which leaf was used
- **Stateless** (SPHINCS+ / SLH-DSA, FIPS 205): a huge tree with pseudorandom key choice, so reuse is negligible
- **Crypto-agility**: be able to swap algorithms without a rewrite (for example hybrid classical + ML-KEM)

```
sig = sign(sk[leaf], m);  leaf = leaf + 1      # stateful: never reuse a leaf
leaf = PRF(seed, m)                            # stateless: reuse is negligible
```

<!-- Worksheet Step 10 and the optional Q6, Q7. Stateful schemes make state loss an operational risk: a VM snapshot rollback replays old state and reuses a key. Ask: "if ECC were broken tomorrow, how long would it take your system to switch algorithms?" That is your crypto-agility score. About 4 minutes. Logic: one key per message would work but is not practical, so real schemes hang many one-time keys under one public key; either the signer counts the leaves (stateful, and a lost count means reuse) or it picks them pseudorandomly from a huge tree (stateless). Next question: what do you do in the lab? -->

---

## 🔓 Lab today — what to do

![Today the lab uses two servers: vulnerable on port 8100 where a second signature is allowed, and fixed on port 8101 where it is refused with 403. Step A1 signs one message and checks that half the key is known. Step A2 signs the opposite message, recovers the key and forges the admin signature. Step A3 shows the fixed server refusing and how far the fix goes. Then do your form worth 40 marks: an odd last digit does AIR-Sec and an even one does Conventional. Hand in Wk15 student ID PDF at learn.zcr.ai/submit by Sunday 14 February 23:59.](img/w15-lab-flow.svg)

- **Everyone (common 60):** A1 one signature, half the key · A2 sign the opposite, recover the key, forge the admin signature · A3 the fixed server refuses, and how far the fix goes
- **Your form (40):** student ID ends **odd** → AIR-Sec · **even** → Conventional
- **Answer sheet:** Classroom → Week 15 → open the file for your form, type in the grey boxes, then File → Download → PDF
- Hand in `Wk15_<StudentID>.pdf` at `learn.zcr.ai/submit` with the code from your KMITL email, by **Sun 14 Feb, 23:59**
- Do the lab with the lab started **once**, in order. Type the `exploit.py` step only once. No Python needed on your computer: everything runs in Docker

<!-- Exact commands are in the worksheet and the answer sheet: copy and run. Start Docker early and wait for "Running on" 8100 and 8101 in the logs (Prep step 6). The commands are docker compose exec vulnerable python lamport.py ... on both Windows and Mac. If port 8100 is busy on a student's computer, Docker says "port is already allocated": close the other program. The optional hndl/ companion lab adds no points. Logic: the lab replays the lecture in order: A1 one signature (half the key), A2 the opposite message (whole key, forgery), A3 the fixed server (the rule); the common 60 come first, then your own form. -->

---

## Takeaway

![Three takeaways. Shor breaks RSA and elliptic curves while Grover only dents AES and SHA. A signature and its opposite give away the whole toy private key. The fix is a usage rule and not a bigger algorithm, because a secure scheme can still be used insecurely.](img/w15-takeaway.svg)

- **Shor** breaks RSA and elliptic curves; **Grover** only dents AES and SHA
- A signature **and its opposite** hand over the whole toy private key
- The fix is a **usage rule**, not a bigger algorithm: a secure scheme can still be used insecurely
- Next week: the **capstone studio**, putting the term's primitives together

<!-- Land the spine: "textbook-secure primitive, real-system failure". Cold-call: "name the key-state mistake and say why refusing the second signature fixes it." CWE-323 (reuse in encryption) is only an analogy here. Remind them: Docker and laptop ready for next week too. Logic: three lines, three slides back: the algorithm that breaks (Shor), the key-state mistake (reuse), the repair (a usage rule). Next question: how do we put the term's primitives together? That is the capstone. -->
