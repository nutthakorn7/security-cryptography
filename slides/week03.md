---
marp: true
theme: default
paginate: true
header: "Cryptography and Network Security · Week 3"
---

# Week 3
## MACs — signing a cookie the right way
Cryptography and Network Security · Nutthakorn Chalaemwongwan

<!-- Lab week: short talk, then the lab. Hook: ask "if I hash a secret and a message together, is that a MAC?" Let them say yes. The lab shows why not. Bring a laptop with Docker; one guided path, no math. -->

---

## Today

- A **10-minute quiz** on Week 2 to start (one question at a time)
- What a **MAC** is, and why a plain hash is not one
- The tempting mistake: `SHA256(secret + data)`
- The fix: **HMAC**
- 🔓 **Lab:** try to change a signed cookie, see a forgery work, then watch HMAC stop it

<!-- Roadmap. Say the spine line out loud: "the math is fine; the way it was used is not" — the same shape as Week 2. Most of the class is the lab, not these slides. -->

---

## Recap — Week 2

- A hash has **no secret**: anyone can compute it
- Password storage went wrong because the hash was **fast** and **unsalted**
- This week's question: *what if we add a secret to the hash?*

<!-- Bridge from W2. W2 was hashing without a secret. The natural next idea is to add a secret — and that is exactly today's trap. -->

---

## The cookie lives with the user

![The server sends a cookie with data and a signature. If the data comes back unchanged, the server's own check matches and it accepts. If someone changes admin=false to admin=true and keeps the old signature, the check does not match and the server refuses.](img/w3-signed-cookie.svg)

- The cookie sits in **your** browser, so you could change it
- The server adds a **signature** to notice that
- The signature is made with a **secret** only the server knows

<!-- This is lab task A1: students change the cookie by hand and get "bad signature". Ask: "why can't you just make a new signature?" (you don't know the secret — or so it seems). -->

---

## A hash alone is not enough

> `cookie = username || SHA-3(username)` — no secret at all. Anyone can recompute it for `username=admin`.

A **MAC** is a short tag made with a **secret key**. It gives you:

- **Integrity** — the data wasn't changed
- **Authenticity** — it came from someone who knows the key

<!-- This is worksheet Q1: the hash-only cookie has no secret, so tampering is undetectable. Ask: "what's missing?" → a key. Thai: MAC = รหัสยืนยันความถูกต้องของข้อความ. -->

---

## The tempting mistake

```
sig = SHA256(MAC_SECRET + data)
```

- Looks reasonable: now there **is** a secret
- This is exactly what `vulnerable_app.py` does
- SHA-256 is **not** broken here — it is being **misused**

<!-- Worksheet Q5. This feels secure to most developers, which is why the bug has shipped in real systems. CWE-347. -->

---

## Why it fails

![Two block chains sharing one starting point. Top: the server's real MAC computation feeds a locked secret block and a data block through the hash's compression function to produce a digest. Bottom: the attacker never sees the secret, but takes that same digest as their own starting state and feeds it through further blocks through the identical compression function, producing a forged digest the server accepts as valid.](img/length-extension.svg)

- SHA-256 processes data in **chunks** and remembers where it left off
- Its output **is** that stopping point
- So `sig` lets someone **carry on** and sign a longer message — without the secret
- This is called **length-extension**

```sim
mac-extend
```

<!-- Keep this to the picture and the one idea. Run the sim live: press Compute and show Verifier A accept. The sim uses a toy hash, not real SHA-256 — say so. No padding arithmetic in class. -->

---

## The fix: HMAC

![HMAC hashes twice. First the key and message go through an inner hash. Then the key and that inner result go through an outer hash, which gives the tag. The attacker only sees the final tag, and cannot carry on from it to sign a longer message.](img/w3-hmac-twice.svg)

- HMAC hashes **twice**, with the key mixed in each time
- You only ever see the final tag
- You cannot carry on from that tag to sign a longer message

<!-- HMAC isn't "hash the key harder": it is two hashes composed. RFC 2104. No ipad/opad needed at this level. -->

---

## One line differs

```python
# vulnerable_app.py
sig = hashlib.sha256(MAC_SECRET.encode() + data).hexdigest()

# fixed_app.py
sig = hmac_module.new(MAC_SECRET.encode(), data, hashlib.sha256).hexdigest()
```

- Same secret, same data, same SHA-256 — only the way it is used changed
- Same forgery against `:8093` → **rejected, 403, no flag**

<!-- This is the literal diff in the two lab apps, and worksheet A3. Ask students to spot it before you highlight it. -->

---

## HMAC does not fix everything

```python
if sig != expected:      # plain comparison — in BOTH apps
```

- **Comparison:** `!=` can stop at the first wrong character → use `hmac.compare_digest()`
- **Replay:** a valid cookie can be sent again later → add an expiry or a nonce

<!-- Worksheet A3(c) and Q3. Both apps keep the plain comparison on purpose, so students learn these are separate problems. "HMAC fixed" is not the same as "cookie secure". -->

---

## 🔓 Lab today — what to do

| Service | Port | How `sig` is made | Forgery works? |
|---|---|---|---|
| vulnerable | `:8092` | `SHA256(secret + data)` | **Yes** |
| fixed | `:8093` | `HMAC-SHA256(secret, data)` | **No** |

- **Everyone (common 60):** A1 change a cookie by hand · A2 run the forgery, get the flag · A3 show HMAC stops it
- **Your form (40):** student ID ends **odd** → Conventional · **even** → AIR-Sec
- **Answer sheet:** Classroom → Week 03 → open the file for your form, type in the grey boxes, then File → Download → PDF
- Hand in `Wk03_<StudentID>.pdf` at `learn.zcr.ai/submit`

<!-- Exact commands are in the worksheet — one known-good path, copy and run. The shared demo flag is fine. Start Docker early; wait for "Running on http://127.0.0.1" with :8092 and :8093 in the logs. On Windows, use curl.exe. -->

---

## Takeaway

- SHA-256 is sound — the **misuse** `SHA256(secret + data)` is what breaks
- A MAC needs the right construction: use **HMAC**, not a home-made mix
- HMAC does not fix comparison timing or replay — those are separate jobs
- Next week: **AES** — why encryption without authentication fails

<!-- Land the spine: "textbook-secure primitive, real-system failure". Cold-call: "SHA-256 isn't broken, so what went wrong in :8092?" Remind: Docker + laptop ready for next week too. -->
