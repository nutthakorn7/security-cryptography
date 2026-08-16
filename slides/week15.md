---
marp: true
theme: default
paginate: true
header: "Security & Cryptography · Week 15"
---

# Week 15
## Post-Quantum Cryptography (Lamport one-time signatures, key reuse)
Security & Cryptography · Nutthakorn Chalaemwongwan

<!-- Hook: ask "if a large-scale quantum computer existed today, is a TLS session you sent an hour ago already broken?" Answer: only if someone recorded it — "harvest now, decrypt later." Today: why quantum breaks RSA/ECC but not AES/SHA, and a signature scheme so simple that its ENTIRE private key falls out of the math the moment you misuse it once. ~2 min. -->

---

## Today

- The quantum threat: **Shor vs. Grover**
- **Harvest now, decrypt later**
- The four **PQC families** + NIST's **ML-KEM / ML-DSA**
- Hash-based signatures: **Lamport OTS** — and its one-time-only rule
- 🔓 Signature game: **Forge the Admin Signature** (key reuse → private-key recovery)

<!-- Roadmap, 1-2 min. Flag the lab: two identical Flask servers running the SAME Lamport signature scheme — one reuses its keypair, one doesn't. Students recover a full private key from two signatures against the vulnerable one, forge an admin signature, then prove the fix actually holds against the other. -->

---

## Recap — Week 14

- Authentication proved **who** you're talking to (passwords, MFA, sessions)
- A **signature** proves **what was said** and that it wasn't tampered with — integrity + non-repudiation
- This week: the primitive *behind* signatures is itself under threat — from quantum computers

<!-- Bridge from W14. Ask: "week 14 verified identity at login — what verifies a message wasn't altered afterward?" -> digital signatures. Pivot: even signature schemes we trust today (RSA, ECDSA) have a quantum shelf life. That's the whole week. ~2 min. -->

---

## Why quantum breaks (some) crypto

- **Shor's algorithm** — solves factoring / discrete log efficiently → breaks **RSA and ECC outright**
- **Grover's algorithm** — quadratic speedup on search → only **halves** symmetric/hash security
- Grover's mitigation: **double the key/output length** (AES-256 stays ~AES-128-strength — still fine)

<!-- The distinction students must nail. Ask: "if Grover roughly halves AES-256's effective security, is AES-256 still safe post-quantum?" (yes). Contrast RSA/ECC: no length increase saves them — Shor is a real break, not a dent. ~6 min. -->

---

## Harvest now, decrypt later

- Adversary **records ciphertext today**, decrypts it once a quantum computer exists
- Makes PQC migration urgent **now** — even though no large quantum computer exists yet
- Real today for anything with a **long confidentiality lifetime**: health records, state secrets, long-lived credentials

<!-- The "why now" slide. Ask: "if your data must stay secret for 20+ years, and a quantum computer might exist in 15, when did you need to have already migrated?" (now). Companion hndl/ lab makes this concrete for key exchange; this week is the signature half of PQC. ~5 min. -->

---

## The four PQC families

- **Lattice-based** — NIST's **ML-KEM** (Kyber, a KEM) and **ML-DSA** (Dilithium, a signature)
- **Hash-based** — Lamport, SPHINCS+, XMSS ← **this week**
- **Code-based**
- **Multivariate**
- NIST standards (2024): **FIPS 203** (ML-KEM) · **FIPS 204** (ML-DSA) · **FIPS 205** (SLH-DSA / SPHINCS+)

<!-- Name the four families; don't over-teach lattice math here. Distinguish KEM vs signature: ML-KEM secures key exchange (companion hndl/ lab), ML-DSA/SLH-DSA sign. Today builds intuition for hash-based signing via the simplest possible construction: Lamport. ~5 min. -->

---

## Lamport one-time signatures — the construction

- Private key: **two random preimages per message bit** — `sk[i] = (a_i, b_i)`
- Public key: **hashes of both** — `pk[i] = (H(a_i), H(b_i))`
- To sign bit *i*: reveal `a_i` if that bit is 0, `b_i` if it's 1
- Security rests on **one assumption** — hash preimage resistance. No exotic math, quantum-resistant

<!-- Build this on the board for a tiny 4-bit example. Stress: textbook-secure, resting purely on a hash function, which Grover only dents. This is exactly why hash-based signatures are a PQC family. Lamport (1979) is the ancestor of SPHINCS+. ~7 min. -->

---

## What one signature reveals

- Signing message `M` reveals **exactly one preimage per bit** — the one matching `M`'s bit value
- The *other* preimage for each bit position stays secret
- Lab check (bit 0, message `0x00000000`): `SHA256(sig[0]) == pk[0][0]`, but `SHA256(sig[0]) != pk[0][1]`
- One signature ⇒ attacker learns **half** the private key — never enough to forge a *different* message

<!-- This is Worksheet Task 1 — do it live: POST /sign {"message_hex":"00000000"}, show sig[0] hashes to pk[0][0], not pk[0][1]. Ask: "is this scheme fine if you only EVER sign one message with this key?" (yes — hence "one-time"). ~6 min. -->

---

## The break: sign twice and the key falls out

- Sign `M = 0x00000000` **and** its bitwise complement `~M = 0xFFFFFFFF`
- They differ in **every bit** → together the two signatures reveal **both preimages, every position**
- That *is* the complete private key — no brute force, just algebra
- **CWE-323** — Reusing a Nonce/Key Pair in Encryption (the vulnerable app's exact flaw)

<!-- The "aha" slide — the whole week's lesson in one line. Ask: "why the complement specifically, not any second message?" (guarantees every bit differs, so nothing is wasted — one signature per bit-value learned). This is exactly Worksheet Task 2. ~6 min. -->

---

## Worked example: forging the admin signature

```python
# vulnerable_app.py — ONE Lamport keypair reused on every /sign call
sig0 = sign(0x00000000)   # reveals the "bit=0" preimage for every position
sig1 = sign(0xFFFFFFFF)   # reveals the "bit=1" preimage for every position
# assemble ANY message OFFLINE now -- including 0xA5A5C3C3, the admin message
forged = [sig0[i] if bit(admin_msg, i) == 0 else sig1[i] for i in range(32)]
# POST /admin {forged}  ->  {"flag": FLAG_PQC}
```

<!-- Walk exploit.py's recover_and_forge logic line by line. Point out /sign refuses the admin message directly (403) on BOTH apps -- that shared baseline is what makes this a genuine forgery and not a one-line curl shortcut. The forged signature is built entirely offline from the two collected signatures. ~6 min. -->

---

## The fix — operational, not mathematical

- `fixed_app.py`: the key signs **at most once**; any 2nd `/sign` call → `403`
- No new math, no bigger keys — just **refuse reuse**
- Rule is **"one signature, period"** — not "one distinct message" (a 2nd request for the *same* message is refused too)
- A client retrying a dropped response must **cache the first signature**, never re-sign
- Still **CWE-323**, not a new class — `verify()`/`/admin` are byte-identical to the vulnerable app; only `sign_endpoint`'s one-time guard changed

<!-- The punchline of the week. Ask: "why refuse even a duplicate of the exact same message, not just a different one?" (the rule must be trivial to enforce correctly -- no edge cases). Ties to Worksheet Q6 / Task 5b: "scheme being secure" vs. "scheme being used securely." ~6 min. -->

---

## Scaling past "one signature ever"

- **Stateful** (XMSS, LMS) — a tree of one-time keys; must **track which leaf was used** — lose the state, reuse a key, break everything
- **Stateless** (SPHINCS+ / SLH-DSA, FIPS 205) — huge tree + **pseudorandom key selection**; reuse becomes cryptographically negligible, no state to lose
- Real deployed hash-based schemes are Lamport's exact discipline, engineered around

<!-- Answers Worksheet Task 5c -- how can SPHINCS+ be stateless yet dodge the reuse trap? Emphasize: statefulness is itself an operational risk (e.g. a VM snapshot rollback replaying old state = catastrophic key reuse). ~5 min. -->

---

## 🔓 Signature game — Forge the Admin Signature

- Two identical Flask targets, same Lamport scheme: `:8100` reuses its key, `:8101` allows only one signature
- `POST /sign` two messages → recover the private key → forge `0xA5A5C3C3` → `POST /admin` → flag
- Win condition: flag captured on `:8100` **and** the identical attack correctly *defeated* on `:8101`

```bash
docker compose up -d
python exploit.py   # needs Python 3 + `requests` on the host
                    # PASS on :8100 (flag captured), PASS on :8101 (attack defeated)
```

<!-- Explain before lab -- this isn't just "get the flag." The win condition requires proving the fix actually holds, mirroring a real bug-bounty proof-of-fix submission. ~3 min. -->

---

## Crypto-agility — the real engineering lesson

- Algorithms keep changing (MD5→SHA-2, RSA→PQC) — systems must **swap primitives without a rewrite**
- Practical pattern: **hybrid classical + ML-KEM** channels (see companion `hndl/` lab) — safe even if one side is later broken
- The Lamport lesson generalizes: **correct usage discipline** matters as much as the underlying math

<!-- Zoom out from the exploit to the industry takeaway. Ask: "if ECC were broken tomorrow, how long would it take your system to switch algorithms?" That answer IS your crypto-agility score. ~4 min. -->

---

## Lab today

> 📋 **Worksheet 15** — `labs/week15-pqc/worksheet.md` (Part 2 written + Part 3 hands-on) · kickoff: `docker compose up -d`

- Recover the Lamport private key from two signatures, forge the admin signature, capture the flag
- Confirm one-time enforcement defeats the identical attack on `:8101`
- **+ Audit the AI** (a hashing-first Lamport signer that *still* reuses its key) **+ EiPE / Prompt Problem**

<!-- The graded output. Point specifically at the Audit-the-AI snippet -- remind them hashing the message first does NOT fix key reuse, it only changes which bits leak, not whether reuse leaks. Point to exploit.py as the reference implementation. ~2 min. -->

---

## Key takeaways

- Shor breaks RSA/ECC outright; Grover only dents AES/SHA — mitigated by longer keys
- Hash-based signatures are **textbook-secure** on one assumption — *if* used strictly one-time
- Real-system failure: reuse the key **once** and the entire private key falls out — no math needed
- The fix is a **usage rule**, not a bigger algorithm — "textbook-secure primitive, real-system failure"

<!-- Recap, 4 lines, tie explicitly back to the course spine. Cold-call: "name the CWE for the vulnerable app's flaw." (CWE-323). ~2 min. -->

---

# Questions?
Next week: Capstone studio — composing the term into CryptoVault

<!-- Cliffhanger: Week 16 is the capstone studio where every primitive learned this term (KDF, AEAD, key exchange, signatures, TLS) gets composed into one system (CryptoVault) they design and build themselves -- the project itself kicked off back in Week 4. Remind them: crypto-agility from today's slide is exactly what the capstone will test. ~2 min. -->
