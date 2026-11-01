---
marp: true
theme: default
paginate: true
header: "Cryptography and Network Security · Week 1"
---

# Week 1
## Cryptography basics & the security mindset
Cryptography and Network Security · Nutthakorn Chalaemwongwan

<!-- Warm-up week: no math, no Docker. Hook: "if a system uses AES-256 and RSA-4096 — the biggest algorithms available — is it safe?" Let a few say yes and hold the answer; the sim later in the deck answers it. Have every table draw its 5×5 Bingo grid now (see the Bingo slide) so squares can be marked during the whole lecture. -->

---

## Today

- The **words** we use every week
- **Symmetric** vs **asymmetric**
- Which **tool** for which goal
- Who the **attacker** is
- **Try it:** crack a key that was never really random
- 🐍 **Snake Oil Bingo** · Worksheet 1 (Part A + your form)

---

## The words we use every week

![Plaintext meet at 10 is encrypted with a key into scrambled ciphertext, then decrypted with the key back into the same plaintext. The algorithm is public; only the key is secret.](img/w1-encrypt-decrypt.svg)

| Word | Meaning |
|---|---|
| **Plaintext** | The readable data you want to protect |
| **Ciphertext** | The scrambled output — useless without the right key |
| **Key** | The secret value that controls encryption and decryption |
| **Kerckhoffs' principle** | The algorithm is public; **only the key is secret** |

<!-- Thai glosses if useful: plaintext = ข้อความต้นฉบับ, ciphertext = ข้อความที่เข้ารหัสแล้ว, key = กุญแจ. Kerckhoffs answers Bingo #16 ("our algorithm is proprietary, so attackers have nothing to analyse"). -->

---

## Symmetric vs asymmetric

![Left, symmetric: Alice and Bob hold the same shared key and send ciphertext between them. Right, asymmetric: Alice locks the message with Bob's public key, which anyone can use, and only Bob's private key can open it.](img/w1-sym-asym.svg)

- **Symmetric:** one shared key — fast (AES). Hard part: sharing the key safely.
- **Asymmetric:** public key locks, private key opens — slower (RSA, elliptic curves); used to agree on keys and to sign.

> Real systems use **both**: asymmetric to agree on a key, symmetric for the data (HTTPS/TLS).

<!-- Draw Alice and Bob on the board: one key between them (symmetric), then Bob's padlock that anyone can close but only Bob can open (asymmetric). No math today. -->

---

## Pick the tool for the goal

| Goal | Tool | Gives | Does **not** give |
|---|---|---|---|
| Keep data secret | Encryption (AES-GCM) | Only key holders read it | Plain encryption alone doesn't stop tampering — use **AEAD** |
| Notice a change | Hash (SHA-256) | A fingerprint of the data | No secret, so it proves nothing about *who* |
| Prove it came from a key holder | MAC (HMAC) | Detects tampering by outsiders | Both sides can create it |
| Prove who signed | Digital signature (Ed25519, RSA) | Anyone can verify | Doesn't keep data secret |
| Store passwords | Slow KDF (bcrypt, Argon2) | Makes guessing expensive | Weak passwords still fall |

<!-- Quick-fire questions: "store passwords?" (slow KDF, not SHA-256 — Bingo #12), "make sure a downloaded file wasn't changed?" (hash), "prove an update came from the vendor?" (signature). The AEAD row answers Bingo #2 ("it's encrypted, so nobody can change it"). Hash, MAC, AEAD and signatures each get their own lab in Weeks 2–11. -->

---

## Who is the attacker?

![Left, passive attacker: Eve listens to the line between Alice and Bob but changes nothing, so encryption is the defence. Right, active attacker: Mallory sits between Alice and Bob and can change, replay or impersonate, so integrity and authenticity tools are needed.](img/w1-passive-active.svg)

| The attacker has… | Example |
|---|---|
| Ciphertext only | Captured encrypted Wi-Fi traffic |
| Known plaintext | Knows messages start with a fixed header |
| Chosen plaintext | Can make your system encrypt what they pick |
| Chosen ciphertext | Can send changed ciphertext and watch the reaction (Week 6) |

> Brute force on a 128-bit key is not practical — real attacks go **around** the math.

---

## The course's lens: good crypto, broken system

Every week takes **one sound primitive** and shows **one real way a system breaks it**.

| How systems break | Real example |
|---|---|
| **Key management** — key hardcoded or stored next to the data | Keys committed to a repository |
| **Bad randomness** — predictable seeds | Debian OpenSSL (2008): only ~32,768 keys |
| **Protocol misuse** — reused nonce, encryption without integrity | PS3 signing key recovered (2010) |
| **Side channels** — timing, error messages | Padding oracle (Week 6) |
| **Implementation bugs** | Heartbleed (2014) leaked memory |

<!-- Write on the board: "Textbook-secure primitive, real-system failure." Nobody in this course breaks AES or factors RSA; every break is a decision made around a sound primitive. -->

---

## Try it: crack a key that was never really random

- Debian's OpenSSL bug cut the randomness: every key came from ~32,768 possible seeds
- The algorithm was fine — the **seed** was guessable
- Open the simulation, pick a target, press **Run the brute force**, and watch it recover the key

![Two zones sharing one comparison point. Top: the intended design expands a seed assumed to be one of 2^128 possible values into a private key, then publishes a one-way commitment to it -- safe only if that assumption holds. Bottom: in the real deployment the seed actually comes from a narrow, guessable source such as a process ID, so an attacker who only ever sees the published commitment runs every one of the roughly 32,768 real candidates through the identical expand and commit functions, compares each result against that published commitment, and recovers the exact private key in under a second.](img/entropy-collapse.svg)

```sim
seed-crack
```

<!-- This is worksheet Part A3: everyone screenshots KEY RECOVERED. expand()/commit() are toy mixers, not real HKDF/SHA-256 — say so. The brute-force loop really runs in the browser, and the "years needed" figure is computed from the speed it just measured. To show a miss, drag the search range down to about a quarter of the real range, run it, then push it back up. Bingo #4 and #9 surface here. -->

---

## Threat model in 4 steps — the notes app

![The notes app: the user's browser talks over HTTPS to the app server, which reads and writes the encrypted note database, uses the key store, and sends encrypted backups to an ops team that also has a key-recovery path. The worksheet asks who can see the plaintext and the key, and where the trust boundaries are.](img/w1-notes-app.svg)

**Assets → attackers → trust boundaries → each risk: control · assumption · still left**

| Risk | Control | Assumption | Still left |
|---|---|---|---|
| Backups *and* the key go to the same ops team | Keep the key in a separate key store | Key-store access is limited and logged | Lose the key = backups unrecoverable |

<!-- This is worksheet Part A1/A2. Ask: "the database is encrypted — can the app server still read the notes?" (yes, it holds the key; Bingo #13 is the key-next-to-data version). -->

---

## 🐍 Snake Oil Bingo + the AI Exhibit

![An example Snake Oil Bingo grid: five by five squares with the myth numbers 1 to 24 in any order and FREE in the centre; two squares are ticked as verified. Five verified squares in a row, column or diagonal wins.](img/w1-bingo-grid.svg)

- Mark a myth when it comes up today; it counts only with a **one-line technical reason**
- **The Exhibit** (worksheet Part 3): an AI answer where every sentence is true — but something big is missing

<!-- Project the myth list (instructor/print/week01-bingo-no-print-slides.pdf) while tables write their grids; the reasons are in instructor/week01-snake-oil-bingo-key.md. Read the Exhibit aloud from the worksheet. Don't reveal its gap — that is the AIR-Sec task. -->

---

## Worksheet 1 — warm-up week

- **Part A (everyone, 60):** who sees the notes and the key (A1) · two risk/control rows (A2) ·
  seed-crack screenshot + 3 short answers (A3)
- **Your form (40):** student ID ends in an **odd** digit → Conventional · **even** → AIR-Sec
- Thai or English answers are fine · no Docker, no flag
- **Answer sheet:** Classroom → Week 01 → open the file for your form, type in the grey boxes,
  then File → Download → PDF
- Hand in `Wk01_<StudentID>.pdf` at `learn.zcr.ai/submit` by **Sun 8 Nov 23:59**

---

## Takeaway

- **"Cryptographically secure" is a claim about the math, not about your system**
- Systems break at the edges: keys, randomness, protocol use, side channels, bugs
- **No quiz today.** Week 2 opens with a 10-minute quiz on today's basics at `learn.zcr.ai/quiz`
- Next week: **hash functions** — we crack a leaked password database in minutes,
  then fix it with salt + a slow KDF (Docker lab — bring a laptop)

<!-- Cold-call: "AES-256 and RSA-4096 are unbroken and the system was still compromised — where does security live?" (in the decisions around the primitive). Remind them to install Git, Docker and Python and fork the repo before Week 2. -->
