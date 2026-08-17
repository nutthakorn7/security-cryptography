---
marp: true
theme: default
paginate: true
header: "Security & Cryptography · Week 2"
---

# Week 2
## Hash Functions (password storage / cracking)
Security & Cryptography · Nutthakorn Chalaemwongwan

<!-- Hook: put a leaked CSV of "username,md5hash" on screen and ask "how long would it take you to find the admin's password?" Answer: milliseconds, live, in front of them — that's what's coming. Today = a mathematically sound primitive (hash functions) breaking in one very specific, very common way. ~2 min. -->

---

## Today

- What a cryptographic hash actually guarantees (and doesn't)
- Why MD5/SHA-1 are "broken" — and why that barely matters *here*
- The real failure: **fast hash + no salt = passwords fall in ms**
- The fix: **salting + slow KDFs** (bcrypt/argon2/scrypt)
- 🔓 Game: **Crack the Leaked DB**

<!-- Roadmap, 1 min. Flag the lab: two leaked password stores, same usernames/passwords, different hashing — one falls instantly, one doesn't. Say the spine line out loud now: "textbook-secure primitive, real-system failure" — it threads every week this semester. -->

---

## Recap — Week 1

- Week 1: adopt an attacker's mindset; threat-model a crypto system *before* trusting it
- A system can use a perfectly sound primitive and still fail — because of *how* it's used
- This week: the first concrete case study — a hash function, misused

<!-- Bridge from W1. W1 = design-level thinking about where trust breaks down. W2 = the pattern made concrete for the first time: sound math ≠ safe system. Ask: "what's the difference between a primitive being broken and a primitive being misused?" — that's the whole lecture in one question. ~2 min. -->

---

## What a cryptographic hash guarantees

- Any input, any size → fixed-size digest (deterministic)
- One-way: cheap to compute forward, expensive to invert
- Small input change → unrecognizably different output (avalanche effect)
- Used for: integrity checks, digital signatures, password storage *(if done right)*

<!-- Ground the primitive before breaking it. Live demo: `echo -n "password" | sha256sum`, then flip one character and rerun — show the digest looks nothing alike. Ask: "if I hand you only this digest, can you find the input?" — sets up preimage resistance next. ~5 min. -->

---

## Three security properties

| Property | An attacker can't... | Prevents |
|---|---|---|
| **Preimage resistance** | find *any* m with H(m) = h, given h | reversing a leaked hash |
| **2nd-preimage resistance** | find m₂ ≠ m₁ with H(m₂) = H(m₁), given m₁ | swapping *your* file for a same-hash fake |
| **Collision resistance** | find *any* m₁ ≠ m₂ with H(m₁) = H(m₂) | forging two same-hash documents from scratch |

<!-- Worksheet Q1 material. Walk each row with a concrete attack: preimage = "attacker has the hash, wants the password"; 2nd-preimage = "attacker has your signed contract, wants a different contract with the identical hash"; collision = attacker doesn't even need YOUR file — any two colliding files will do (e.g. a rogue CA certificate). ~6 min. -->

---

## MD5 / SHA-1: broken — but where does it matter?

- MD5 (2004) and SHA-1 ("SHAttered," Google/CWI, 2017) — practical **collision** attacks exist
- Collision resistance is what **digital signatures** rely on → broken badly (attacker forges a second document with the same signature)
- Password storage relies on something else entirely: the attacker not being able to **guess fast enough**

<!-- Key nuance students miss: "broken" isn't one thing. MD5's collision break is catastrophic for signing — ask "why would a forged same-hash contract be dangerous?" — but it is NOT why MD5 is bad for passwords; that's next. This is Worksheet Q2's hinge. ~4 min. -->

---

## The real failure: passwords aren't "reversed"

- An attacker with a leaked hash file does **not** invert the hash
- They **guess and hash** — try a candidate, compare, repeat, at billions/sec
- A **fast** hash (MD5, even plain SHA-256) is a gift to that attacker
- Speed is a *feature* for integrity checks — it's a **bug** for password storage

> CWE-916 — Use of Password Hash With Insufficient Computational Effort

<!-- The pivot slide — this is the "real-system failure" for this week. Ask: "SHA-256 has no known collisions — so why is it still wrong for passwords?" Answer: the attacker never needed a collision, they need speed, and SHA-256 hands them speed. Directly answers Worksheet Q3/Q6. ~5 min. -->

---

## Worked example: the vulnerable store

```python
# vulnerable_app.py — /login
stored = lookup(username)          # md5 hex, no salt (users_vulnerable.csv)
ok = hashlib.md5(password.encode()).hexdigest() == stored
```

- Same password → same hash, for **every** user, **every** time
- One precomputed wordlist × MD5 table cracks the **whole file** at once
- CWE-916 (fast primitive) + CWE-759 (no salt at all)

<!-- This is the exact code students find in Lab Task 0. Point at the line. Ask: "why does 'no salt' matter more here than 'MD5 is old'?" — because unsalted means one attack amortizes across every row in the leak, not just one victim. ~5 min. -->

---

## The attack: dictionary & rainbow tables

- **Dictionary attack:** hash each candidate word, compare against the leaked hash
- Unsalted + fast → **one precomputed table** cracks every matching row in the leak
- **Rainbow table:** precomputed hash chains — trade storage for time, invert fast unsalted hashes at internet scale
- Verified in this lab: `admin`'s password cracked from a **101-word** list in **~0.1 ms**

<!-- Make it visceral with the actual measured number. Ask: "if the wordlist were the top 10 million leaked passwords instead of 101, does the *approach* change?" (No — still milliseconds per row, just a bigger table.) This is the empirical proof behind Worksheet Q5/Q6. ~5 min. -->

---

## Fix 1 — salting

- **Salt:** a random value per user, stored *alongside* the hash — not secret
- Store `H(salt ‖ password)` — identical passwords → **different** hashes
- Defeats: precomputed rainbow tables (attacker needs a fresh table *per salt*) and cross-user correlation ("did two users pick the same password?")
- A **reused or constant** salt gives none of this protection — it's just a longer password

> CWE-759 / CWE-760 — one-way hash without a salt / with a predictable salt

<!-- Worksheet Q4/Q5 material. Stress: the salt sits right next to the hash in the open — its job isn't secrecy, it's uniqueness. Ask: "why doesn't the salt need to be secret?" (the attacker who has the hash file has the salt too — it kills precomputation and cross-row shortcuts, not per-row brute force.) ~5 min. -->

---

## Fix 2 — slow KDFs & work factor

- **bcrypt / argon2 / scrypt** — deliberately, tunably **slow**
- The **cost / work factor** controls how long *one* hash takes to compute
- Raising cost: the defender pays once per real login (negligible); the attacker pays **per guess, per row** — the cost compounds against them
- bcrypt buys **work factor**, not invincibility

<!-- Worksheet Q3 material — "who does raising cost hurt more?" is the crux. One login/sec is free for a real user; a billion-guesses/sec attacker now manages thousands/sec. Flag the honesty clause up front: this raises COST, it does not make a weak password unbreakable — that's the punch line of the next slide. ~5 min. -->

---

## The corrected construction

```python
# fixed_app.py — /login
stored = lookup(username)      # $2b$<cost>$<salt><hash>  (users_fixed.csv)
ok = bcrypt.checkpw(password.encode(), stored)
```

- One-line diff from the vulnerable version: `bcrypt.checkpw(...)` vs. `md5(...) ==`
- Same md5-precompute-over-wordlist technique → **0 / 8 rows match** (verified)
- **But:** `admin`'s real password (`sunshine2021`) *is* in the wordlist — a patient, *slow*, per-hash bcrypt dictionary attack would still find it, just at orders-of-magnitude higher cost

<!-- Don't let anyone leave thinking "bcrypt = solved." This is the overclaim trap the worksheet explicitly warns against (Task 5b). Ask: "so what actually stops that patient, per-hash attacker?" → answer is next slide: a strong-password policy, not the hash function alone. ~5 min. -->

![Two horizontal bands sharing the same wordlist. Top: an unsalted MD5 password store — a leaked file feeds a candidate wordlist through a single real MD5 pass, compared directly against the stored hash, cracking the target instantly and, for free, any other row that happens to share the same password. Bottom: the same wordlist aimed at a per-user salted, iterated KDF store — the identical fast technique matches nothing because the stored format differs entirely, and only an attacker who adapts to redo the real salted iterations per guess still finds the password, at a cost that multiplies with the iteration count.](img/hash-crack.svg)

```sim
hash-crack
```

<!-- The sim runs a REAL MD5 (RFC 1321, byte-identical to hashlib.md5 — md5("sunshine2021") really does come out f364b087df0401706d6b1c8f68a50bf7, this week's own admin hash) against a REAL 101-word dictionary, live in the browser. The salted store is NOT bcrypt — it's a small toy KDF (a real per-user salt, real repeated hashing, a real tunable cost) that's honest about not being the Blowfish-keyed real thing, while still making salting and work-factor genuinely measurable rather than asserted. Run it live here: crack Store A instantly, watch the identical technique score 0/101 against Store B, then drag the cost slider up and re-run the adapted attack — the operation-count multiplier it reports is computed, not decorative, and it should land as "orders of magnitude more expensive," never as "bcrypt is broken." Good beat right before the game: same trap as the slide above, now literally clickable. ~5 min. -->

---

## 🔓 Game — Crack the Leaked DB

Two identical services, same users/passwords, different hashing:

| Service | Port | Store | Crackable by fast offline dictionary? |
|---|---|---|---|
| `vulnerable_app.py` | `:8094` | unsalted MD5 | **Yes** — milliseconds |
| `fixed_app.py` | `:8095` | bcrypt, per-user salt + cost | **No** (to this technique) |

1. Exfil the leaked `users_vulnerable.csv`, crack `admin`'s MD5 with `wordlist.txt`
2. `POST /login` the recovered password, then `GET /admin` **on the same session** → flag
3. Run the *same* technique against `users_fixed.csv` → prove it matches nothing

```bash
docker compose up -d      # vulnerable_app.py :8094, fixed_app.py :8095
python exploit.py         # needs Python 3 + `requests` on the host
                           # PASS :8094 (flag) · PASS :8095 (0 bcrypt matches)
```

<!-- Explain before lab: instant feedback both directions — it cracks in ms, or it visibly doesn't. exploit.py needs only `requests` on the host — no bcrypt required to *run* the attack, only inside the fixed container. Point out the session-cookie step: login and /admin must share one `requests.Session()`, and a fresh request without the cookie jar gets 403. ~4 min. -->

---

## Lab today

> 📋 **Worksheet 2** — `labs/week02-hash/worksheet.md` · **kickoff:** `docker compose up -d`

- Part 2 (Q1–Q8): properties, broken hashes, fast-vs-slow, salts, rainbow tables, pepper
- Part 3 (Tasks 0–5): crack the MD5 store, capture the flag, confirm bcrypt resists it
- **🤖 Audit the AI:** critique an AI's "secure" `store_password` — bare SHA-256 + a hardcoded constant `"salt"`, framed as a benefit
- **🧠 EiPE + Prompt Problem:** explain the mechanism in plain English; stress-test an AI's password-storage advice

<!-- The graded output. Flag the Audit-the-AI trap specifically: the AI's code hashes AND claims "a salt" and still fails — same fast-hash mistake (SHA-256, called a benefit because it's "efficient") plus a shared constant instead of a per-user random salt. That's this week's "looks professional, is wrong." Worth 20/100 points — not optional. ~3 min. -->

---

## Key takeaways

- Hash functions are **textbook-secure** — the math (preimage/collision resistance) holds
- The **real-system failure**: using a fast, general-purpose hash where a slow, purpose-built KDF belongs
- The attacker doesn't break the math — they **guess and hash**, fast, at scale
- Fix = **salt** (kills precomputation) + **slow KDF** (raises cost) — still pair with a strong-password policy

<!-- Land the spine explicitly: "textbook-secure primitive, real-system failure" — this is the pattern for the whole course. Cold-call: "I hand you an unsalted SHA-256 password store — is SHA-256 broken? What's actually wrong?" ~3 min. -->

---

# Questions?
Next week: MACs — hash-only auth, and forging an admin cookie via length-extension

<!-- Cliffhanger: "we just watched a textbook-sound hash fail because of how it was used — every week from here on, we do this again for a different primitive." Remind students: Docker containers + wordlist.txt ready before lab starts; per-student flag via FLAG_HASH — submitting another student's flag is a violation. -->
