---
marp: true
theme: default
paginate: true
header: "Cryptography and Network Security · Week 2"
---

# Week 2
## Hash functions — and how a password database falls
Cryptography and Network Security · Nutthakorn Chalaemwongwan

<!-- Lab week: short talk, then everyone cracks a real (sandbox) leaked password file. Hook: show a leaked CSV of `username,md5hash` on screen and ask "how long to find the admin's password?" — answer: milliseconds, live, in a moment. Bring a laptop with Docker; one guided path, no math. -->

---

## Today

- A **10-minute quiz** on Week 1 to start (one question at a time)
- What a **hash** is, and the three things it promises
- Why a stolen password file can fall in **milliseconds**
- The fix: **salt** + a **slow** password hash (bcrypt / Argon2)
- 🔓 **Lab:** crack a leaked database, then watch the fix stop the same attack

<!-- Roadmap. Say the spine line out loud: "the math is fine; the way it was used is not" — the same shape as Week 1. Most of the class is the lab, not these slides. -->

---

## Recap — Week 1

- Last week: think like an attacker; a system can use **sound** crypto and still break
- Systems break at the edges — keys, randomness, how a tool is used
- This week is the **first real case**: a good hash function, used the wrong way

<!-- Bridge from W1. W1 was the mindset; W2 makes it concrete for the first time. Ask: "what's the difference between a tool being broken and a tool being misused?" — that's the whole lesson. -->

---

## What is a hash function?

![A hash function takes any input and produces a short fixed-size digest. Two different inputs that look almost the same produce completely different digests, and you cannot go from a digest back to the input.](img/w2-hash-what.svg)

- Any input → a short **fixed-size** fingerprint (the *digest*)
- **One-way:** easy to go forward, not meant to be reversed
- Change one character → a **completely different** digest
- Same input → **same** digest, every time

<!-- Live demo: `echo -n password | sha256sum`, then change one letter and run again — the digest looks nothing alike. Thai: hash = แฮช / ลายนิ้วมือข้อมูล, digest = ค่าแฮช. Keep it to these four facts; no formal proofs. -->

---

## What do we use hashes for?

| Job | Example |
|---|---|
| Check a file wasn't changed | Compare the download's hash to the published one |
| Part of a digital signature | Week 11 |
| **Store passwords** | Keep the hash, not the password — *if done right* |

> Today is about that last one — and the very common way it goes wrong.

<!-- Keep this light — one line each. The point is only to reach "store passwords", which is the rest of the lecture. Ask: "why keep the hash instead of the password?" (so a leak doesn't hand over the password directly — in theory). -->

---

## The real failure: you don't *reverse* a hash

![An attacker who steals a password file does not reverse the hash. They take a wordlist of common passwords, hash each guess, and compare it to the stolen hashes until one matches.](img/w2-guess-and-hash.svg)

- An attacker who steals the file does **not** un-hash it
- They **guess and hash**: hash a common word, compare, repeat — billions per second
- A **fast** hash (MD5, even SHA-256) makes guessing cheap
- Speed is good for file checks — it's a **problem** for passwords

<!-- The pivot. Ask: "SHA-256 has never been broken — so why is it wrong for passwords?" Answer: the attacker never needed to break it; they only need to guess fast, and SHA-256 lets them. This is the heart of the week. -->

---

## No salt = the whole file falls at once

```
username,md5hash
admin,f364b087df0401706d6b1c8f68a50bf7
alice,5f4dcc3b5aa765d61d8327deb882cf99   <- "password"
```

- No **salt**: the same password gives the **same** hash for everyone
- So **one** list of hashed guesses cracks **every** row at the same time
- This is exactly the file you'll crack in the lab

<!-- This is users_vulnerable.csv from the lab. Point at the two identical-looking rows idea: if two users pick the same password, their stored hashes are identical — the attacker sees that for free. "No salt" is why one table covers the whole file, not just one victim. -->

---

## 🔓 Lab — crack the leaked database

Two copies of the same login service, same users, **different** storage:

| Service | Port | Stores passwords as | Falls to a fast wordlist? |
|---|---|---|---|
| vulnerable | `:8094` | MD5, no salt | **Yes — milliseconds** |
| fixed | `:8095` | bcrypt (salt + slow) | **No** |

1. Run `crack.py` → recover every password from the leaked MD5 file
2. Log in as `admin`, get the **flag**
3. Run the *same* crack on the bcrypt file → it finds **nothing**

![The same wordlist aimed at two stores. Against the unsalted MD5 store it cracks the target instantly and every other matching row for free. Against the salted, slow store the identical fast attack matches nothing, and only a far slower per-user attack could make progress.](img/hash-crack.svg)

```sim
hash-crack
```

<!-- The sim runs a real MD5 over a real 101-word list in the browser — md5("sunshine2021") really is this week's admin hash. Crack store A instantly, watch the same technique score 0 on store B, drag the cost slider up and re-run. Everyone does this on their own laptop in the lab; the deck is just the picture of it. -->

---

## Fix 1 — add a salt

![With a per-user salt, two people who choose the same password get different stored hashes, so one precomputed list no longer cracks the whole file.](img/w2-salt.svg)

- A **salt** = a random value, one per user, stored **next to** the hash (not secret)
- Store `hash(salt + password)` → same password now gives **different** hashes
- One precomputed list no longer works — the attacker needs a **fresh** one per user

<!-- Worksheet material. Stress: the salt is not a secret — it sits in the open right beside the hash. Its job is uniqueness, not secrecy. Ask: "why doesn't the salt need to be secret?" (the attacker who stole the hashes stole the salts too; it still kills the one-list-cracks-all shortcut). -->

---

## Fix 2 — use a *slow* password hash

- **bcrypt / Argon2 / scrypt** are built to be **deliberately slow**, with a tunable *cost*
- Measured in this lab: one MD5 guess ≈ **0.4 millionths of a second**; one bcrypt guess ≈ **0.2 seconds**
- The real user logs in once — the delay is nothing
- The attacker pays that cost on **every guess**, for **every** user — it piles up

> bcrypt buys **time**, not magic — a weak password can still be guessed, just far slower

<!-- Worksheet Q "who does raising the cost hurt more?" The honesty clause matters: this raises the attacker's cost by ~500,000×, it does NOT make a weak password unbreakable. That's why you also need a strong-password policy. Don't let anyone leave thinking "bcrypt = solved". -->

---

## Lab today — what to do

- **Everyone (common 60):** crack the leaked MD5 file, log in as `admin`, capture the flag, then show the bcrypt file resists the same attack
- **Your form (40):** student ID ends **odd** → Conventional · **even** → AIR-Sec
- Exact commands are in the worksheet — one known-good path, copy and run
- **Answer sheet:** Classroom → Week 02 → open the file for your form, type in the grey boxes, then File → Download → PDF
- Hand in `Wk02_<StudentID>.pdf` at `learn.zcr.ai/submit`

<!-- Point at the worksheet's Task 0–4; they are the class. The shared demo flag is fine — no personal flag is needed. Start Docker early (it installs on first run); if the page 403s at first, wait for "Running on" in the logs. -->

---

## Takeaway

- A hash function can be **sound** and the system still falls — because of *how* it stores passwords
- The attacker doesn't reverse the hash — they **guess and hash**, fast
- Fix = **salt** (kills the one-list shortcut) + a **slow** hash (raises the cost) + strong passwords
- Next week: **MACs** — proving a message wasn't changed, and forging an admin cookie

<!-- Land the spine: "textbook-secure primitive, real-system failure" — the pattern for the whole course. Cold-call: "I hand you an unsalted SHA-256 password store — is SHA-256 broken? Then what's wrong?" (nothing's broken; it's fast and unsalted). Remind: Docker + laptop ready for next week too. -->
