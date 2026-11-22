# Week 7 — Reflection & Review (pre-Midterm)

No new content. Review **Weeks 1–6** and get ready for the midterm (Weeks 8–9). Nothing is submitted this week
except a one-page cheat sheet; the teams' CryptoVault KDF + AEAD-at-rest demo is feedback only.

> **Note on Week 1:** Week 1 (intro + threat modelling) has no Docker target by design. The midterm still
> asks about its main idea, so it is in the recap table below.

## ✅ This week — what to do
1. **Before class** — read your own answers from Weeks 2–6 and the recap table below. You do **not** need to
   redo any lab at home.
2. **In class (100 min)** — short quiz → a few **Crypto Jeopardy** clues → **two mock checkpoints** with the
   supplied scripts → explain one mistake and how to fix it.
3. **Prepare** — Week 8 is a written exam and Week 9 is a hands-on practical. Both cover Weeks 1–6 only.

**100-minute plan:** quiz 20 + selected Jeopardy clues 10 + two mock checkpoints 40 + explain a fix, CryptoVault
team, design doc and demo 25 + save the cheat sheet and read the exam rules 5. The full board below is extra
practice: do not try every clue in class.

---

## Recap — the one-line lesson from each week

| Wk | Topic | Core lesson (one line) |
|----|-------|------|
| 1 | Threat modelling | Good crypto still fails when the **threat model, the key handling or the way the pieces are combined** is wrong. The algorithm is rarely the weak link. |
| 2 | Hash functions | A **fast** hash (MD5, SHA-256) is the wrong tool for passwords. Use a **slow, salted** password hash (bcrypt, argon2id); the salt stops one pre-computed table from working on every user. |
| 3 | MACs | `SHA256(key ‖ message)` is not a safe MAC: an attacker who has one valid cookie can **extend** it without the key. HMAC is built to avoid this. |
| 4 | AES modes | **Encryption alone does not stop changes.** In CBC the server accepted a changed token (guest became admin) because nothing checks that the data was not changed. |
| 5 | Key exchange | **Plain Diffie-Hellman keeps the key from someone who only listens, but not from someone in the middle.** The middle one makes two separate handshakes. Authentication is what is missing. |
| 6 | AEAD | The CBC server's `200` / `403` answers leak enough for the script to read the secret **without the key**. AES-GCM checks its **tag first** and answers the same every time, so it leaks nothing. |

**The through-line:** secrecy, "not changed" and "really from them" are three different properties. A tool
that gives you one does not give you the other two for free.

---

## 🎯 Signature activity — "Crypto Jeopardy"

Team quiz show across all six topics with values 100–500 and a final wager. In class the instructor picks
**about 8 clues** that match the mistakes seen so far. Clue wording stays close to the worksheets.

| Threat modelling (Wk1) | Hashing (Wk2) | MACs (Wk3) | AES modes (Wk4) | Key exchange (Wk5) | AEAD (Wk6) |
|---|---|---|---|---|---|
| 100 | 100 | 100 | 100 | 100 | 100 |
| 200 | 200 | 200 | 200 | 200 | 200 |
| 300 | 300 | 300 | 300 | 300 | 300 |
| 400 | 400 | 400 | 400 | 400 | 400 |
| 500 | 500 | 500 | 500 | 500 | 500 |

**Sample clues (answer in question form):**
- *Hashing – 100:* "Same password, same hash for every user: this random value added per user stops it." *(What is a salt?)*
- *MACs – 300:* "This is the property of `SHA-256(key ‖ message)` that lets an attacker add data and still get a valid digest without the key." *(What is length extension?)*
- *AES modes – 300:* "In the Week 4 lab, this missing check let a changed CBC token be accepted as admin." *(What is a check that the data was not changed, a tag or MAC?)*
- *Key exchange – 400:* "This is what an authenticated Diffie-Hellman exchange checks that plain Diffie-Hellman does not." *(What is who the other side really is?)*
- *AEAD – 500:* "This is why the script could read the CBC secret but got nothing from AES-GCM." *(What is: GCM checks the tag first and answers the same for every change, so there is no yes/no to ask?)*

**Final wager:** "This kind of attacker, in the Week 5 relay and the Week 6 CBC server, can change messages, not only read them." *(What is an active attacker, one in the middle?)*

---

## 🧪 Mock midterm practice (two checkpoints in class)

Ungraded. The aim is to be comfortable with the format of Weeks 8–9. The instructor picks **one checkpoint from
group A (Weeks 2–4) and one from group B (Weeks 5–6)**. Re-do it without your notes from that week, using the
scripts and commands that come with that lab.

| # | Checkpoint | Group | From |
|---|-----------|-------|------|
| 1 | Find the admin password in a leaked store of unsalted MD5 hashes | A | `labs/week02-hash` |
| 2 | Run the supplied forgery script on a signed cookie and show HMAC refuses it | A | `labs/week03-macs` |
| 3 | Run the supplied script that turns a `guest` CBC token into `admin`, then show GCM rejects the same change | A | `labs/week04-aes-modes` (ports 8096/8097) |
| 4 | Show a man in the middle reading a plain Diffie-Hellman handshake | B | `labs/week05-key-exchanges` |
| 5 | Ask the CBC and GCM servers about a changed message and run `exploit.py` | B | `labs/week06-aead` (ports 8098/8099) |

**For each one:** write the result in one line and **one fix**, then compare with that week's `worksheet.md`.
Written half of the midterm: four kinds of question (short concept, spot the weak design and its fix,
walk through an attack that you did in a lab, design a safer scheme). Practice by explaining your own lab results in 2–3 sentences.

## Deliverable
A one-page **cheat sheet** (open note only if the instructor allows it in the exam). Suggested contents: the six
one-line lessons above, the idea of length extension in plain words, what "authenticated" adds (a tag that is
checked first), and the AES-GCM rules (never reuse a nonce, always obey the tag result).

## Covers
Weeks 1–6: [intro/threat modelling](../week01-intro/), [hash functions](../week02-hash/), [MACs](../week03-macs/),
[AES modes](../week04-aes-modes/), [key exchanges](../week05-key-exchanges/), [AEAD](../week06-aead/).

Next: the cumulative quiz, [`../../quizzes/weekly/week07-review-quiz.md`](../../quizzes/weekly/week07-review-quiz.md).
