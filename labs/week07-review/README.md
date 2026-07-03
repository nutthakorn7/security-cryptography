# Week 7 — Reflection & Review (pre-Midterm)

No new content. Consolidate **Weeks 1–6** and prepare for the midterm (Weeks 8–9).

> **Note on Week 1:** Week 1 (intro + threat-modeling a crypto system) is Conceptual — no Docker
> target/flag by design (see `labs/week01-intro/`) — but Weeks 8–9 still examine its core lesson
> alongside Weeks 2–6, so this review covers it too (see the recap table below).

## ✅ This week — what to do
1. **Before class** — review Weeks 1–6: your worksheets (`labs/week02-hash/worksheet.md` …
   `labs/week06-aead/worksheet.md`), each week's README "Concepts"/"Analogous CWE" line, and any
   slides published so far.
2. **In class (300 min)** — cumulative review quiz
   (`../../quizzes/weekly/week07-review-quiz.md`) → **Crypto Jeopardy** (below) → **mock CTF /
   mock-written dry-run** in the midterm's format → debrief on weak spots.
3. **Prepare** — the **midterm is Weeks 8–9**: Week 8 is a written/concept exam, Week 9 is a
   hands-on practical. Both cover Weeks 1–6 only.

*Time breakdown follows the same 120 min lecture / 180 min lab split as every other week, with
the lecture slot replaced by the review game and the lab slot replaced by the mock CTF.*

---

## Recap — the one-line lesson from each week

| Wk | Topic | Core lesson (one line) |
|----|-------|------|
| 1 | Intro & threat-modeling a crypto system | Textbook-secure crypto still fails in real systems when the **threat model, key management, or protocol composition** is wrong — the algorithm is rarely the weak link. |
| 2 | Hash functions | A **fast** hash (MD5/SHA-256) is the wrong tool for passwords; only a **slow, salted KDF** (bcrypt/argon2id) resists offline dictionary/rainbow-table attacks at scale. |
| 3 | MACs | `H(key \|\| message)` is **not** a MAC — Merkle-Damgard hashes are vulnerable to **length-extension**, letting an attacker append data and compute a valid new digest without the key; HMAC's nested construction is not. |
| 4 | AES / block-cipher modes | **Unauthenticated encryption is malleable** — CBC's `P_i = D(C_i) XOR C_{i-1}` relation lets an attacker flip chosen plaintext bits by flipping ciphertext bits, with no integrity check to catch it. |
| 5 | Key exchanges | **Unauthenticated Diffie-Hellman gives secrecy against eavesdroppers but zero identity guarantee** — an active attacker in the middle completes two independent handshakes and relays/reads everything; authentication (signature/MAC-bound keys) is what DH itself doesn't provide. |
| 6 | Authenticated encryption (AEAD) | Combining a MAC and a cipher the *wrong* way (MAC-then-encrypt / encrypt-and-MAC done naively) opens a **padding oracle** that decrypts ciphertext byte-by-byte with no key; **encrypt-then-MAC** or a single AEAD primitive (AES-GCM) closes it — the capstone of Wk3 (MAC) + Wk4 (cipher) combined correctly. |

**The through-line:** Wk2 is about *storage* (one-way, no key). Wk3 shows a *keyed hash isn't
authentication*. Wk4 shows *encryption isn't integrity*. Wk5 shows *key agreement isn't identity*.
Wk6 shows what happens when you *bolt Wk3 + Wk4 together wrong* — and how to bolt them together
right. Every week is a variation on the same idea: **confidentiality, integrity, and
authenticity are three separate properties, and a primitive that gives you one does not give you
the others for free.**

---

## 🎯 Signature activity — "Crypto Jeopardy"

Team quiz-show across all six topics, with point values (100/200/300/400/500) and a **Final
Wager** round. Questions are drawn from each week's worksheet (Conventional-arm Part
1/2 questions and lab Task deliverables) — see the instructor board for the full 30-question set.

| Threat Modeling (Wk1) | Hashing (Wk2) | MACs (Wk3) | AES Modes (Wk4) | Key Exchange (Wk5) | AEAD (Wk6) |
|---|---|---|---|---|---|
| 100 | 100 | 100 | 100 | 100 | 100 |
| 200 | 200 | 200 | 200 | 200 | 200 |
| 300 | 300 | 300 | 300 | 300 | 300 |
| 400 | 400 | 400 | 400 | 400 | 400 |
| 500 | 500 | 500 | 500 | 500 | 500 |

**Sample clues (answer in question form, Jeopardy-style):**
- *Hashing – 100:* "This is the difference between a hash's *preimage resistance* and its
  *collision resistance*, in one sentence." *(What is: preimage = can't find any input for a
  given output; collision = can't find any two inputs with the same output.)*
- *MACs – 300:* "This is the specific Merkle-Damgard property that makes `SHA-256(key ||
  message)` forgeable without knowing the key." *(What is: the ability to resume hashing from a
  known internal state — length-extension.)*
- *AES Modes – 300:* "Flipping a bit here in CBC ciphertext flips the *same* bit position in the
  *next* plaintext block, unpredictably scrambling the *current* one." *(What is: the previous
  ciphertext block, `C_{i-1}`?)*
- *Key Exchange – 400:* "This is what an authenticated DH exchange checks that plain DH does
  not." *(What is: the peer's identity — that the public key came from who you think it did?)*
- *AEAD – 500 (Daily Double candidate):* "This is the one-sentence reason AES-GCM has no padding
  oracle, covering both *what mode it is* and *when the tag is checked*." *(What is: it's a
  stream-cipher-style mode with no padding to malform, and the tag is verified before any
  plaintext is released?)*

**Final Wager:** "This attacker model — the one shared by Week 5's relay and Week 6's
`encrypt-and-MAC` mistake — sees and can modify every message in transit, not just read it." Teams
wager any/all of their points. *(What is: an active (on-path) attacker, as opposed to a passive
eavesdropper?)*

Instructor note: build the full clue board from each week's `worksheet.md` — every Part
1/2 Conventional-arm question and every hands-on Task deliverable is fair game at some point
value. Keep clue phrasing close to worksheet phrasing so review reinforces, rather than
surprises with new vocabulary.

---

## 🧪 Mock midterm dry-run

A short, mixed practice session in the **exact format of Weeks 8–9** so there are no surprises.
Ungraded (participation only) — the goal is comfort with the format, not new content.

**Mock written half (mirrors Week 8):** four sections, same shape as the real midterm —
- **Section A — Concepts (MCQ/short answer):** hash properties, MAC vs. hash vs. signature,
  AEAD's three guarantees, DH vs. authenticated DH.
- **Section B — Spot the vulnerability:** short code/protocol snippets (e.g. `H(key ||
  message)` used as a cookie MAC, a GCM nonce reused across two calls, a naive MAC-then-encrypt
  padding check) — name the CWE-equivalent flaw and the one-line fix.
- **Section C — Attack walkthrough:** given a vulnerable construction (unauthenticated CBC token,
  or a length-extension setup), walk through the attack step by step.
- **Section D — Design:** design a secure cookie/session scheme, or justify an AEAD choice for a
  given deployment constraint (hardware, nonce-misuse risk, throughput).

**Mock practical half (mirrors Week 9):** re-run **any one** of the Week 2–6 labs cold, without
your notes from that week, and recapture the flag/evidence artifact solo:

| # | Challenge | Topic | Target |
|---|-----------|-------|--------|
| 1 | Crack the admin password from a leaked unsalted-MD5 store | Hashing (W2) | `labs/week02-hash` (`docker compose up`, ports 8094/8095) |
| 2 | Forge an admin cookie via HMAC length-extension | MACs (W3) | `labs/week03-macs` |
| 3 | Bit-flip a CBC session token from `role=guest` to `role=admin` | AES modes (W4) | `labs/week04-aes-modes` (ports 8096/8097) |
| 4 | MITM an unauthenticated DH handshake and recover the relayed secret | Key exchange (W5) | `labs/week05-key-exchanges` (`docker compose -f docker-compose.vulnerable.yml up`) |
| 5 | Run a padding-oracle attack to decrypt a ciphertext byte-by-byte | AEAD (W6) | `labs/week06-aead` (ports 8098/8099) |

**For each you attempt:** note your payload/technique and a one-line fix, then check yourself
against that week's `exploit.py` and `worksheet.md`. Instructors: hints and full solutions live
in each week's own directory — no separate spoiler-free copy is needed since this is a *repeat*
of a lab already completed, not a fresh challenge.

## Deliverable
Each student submits a one-page **cheat sheet** (allowed as an open-note aid in the exam, if the
instructor permits open-note). Suggested contents: the six one-line lessons above, the
CBC decryption relation, the length-extension idea, and the AEAD composition rule
(encrypt-then-MAC is safe; the other two orders are not).

## Covers
Weeks 1–6: [intro/threat-modeling](../week01-intro/) (Conceptual, no lab target — see note above),
[hash functions](../week02-hash/), [MACs](../week03-macs/), [AES modes](../week04-aes-modes/),
[key exchanges](../week05-key-exchanges/), [AEAD](../week06-aead/).

Next: the cumulative quiz — [`../../quizzes/weekly/week07-review-quiz.md`](../../quizzes/weekly/week07-review-quiz.md).
