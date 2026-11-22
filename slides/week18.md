---
marp: true
theme: default
paginate: true
header: "Cryptography and Network Security · Week 18"
---

<!-- DRAFT. Exam-day deck for the final written exam. Date, time and room are NOT known yet (the academic office announces them): none is printed here. Delivery: 100 minutes. 5 minutes identity, seating and rules, 90 minutes independent writing, 5 minutes collect scripts. Show slides 2 to 4 and 8 while students sit down; the rest is a revision aid before the exam (posted a week earlier, not shown during the sitting). Logic of the deck: say what the exam is, what is on it, the one pattern behind every week, one line per week to recall it, how to answer, the rules, and what comes after. Each slide answers one question and ends with the next. -->

# Week 18
## Final written exam
Cryptography and Network Security · Nutthakorn Chalaemwongwan

<!-- Say: this is the whole final, 25 course points; Week 19 is not a second final. Bridge from Week 17 (review). Logic: the title slide fixes what the exam is so that nobody expects a practical. -->

---

## One sitting, 100 minutes

![Timeline of the final written exam: minutes 0 to 5 identity check, seating and rules; minutes 5 to 95 ninety minutes of independent writing; minutes 95 to 100 collect the scripts. The raw score out of 100 is scaled to 25 course points.](img/w18-run.svg)

```
points = raw / 100 * 25        # the whole final: 25 course points
```

- 5 minutes: identity, seat, rules
- **90 minutes:** independent writing
- 5 minutes: collect the scripts

<!-- Source: SUBMISSION.md exam table (90-minute paper + 10-minute administration, 25 course points, paper or instructor-assigned quiz) and the W18 lesson plan run sheet. Logic: the first question a student has is how long and how much it counts; the next slide says what is on the paper. -->

---

## What is on the paper

![The paper has 20 questions: 14 from Weeks 10 to 16, the emphasis of the final, and 6 callbacks, one each from Weeks 1 to 6.](img/w18-blueprint.svg)

```
questions = 14 + 6       # Weeks 10 to 16, plus one callback from each of Weeks 1 to 6
```

- **14** questions from Weeks 10 to 16 (the emphasis)
- **6** callbacks, one each from Weeks 1 to 6
- Individual work; cumulative paper

<!-- Source: labs/week17-review/README.md (14 of 20 from Wk10-16 and six from Wk1-6, one callback per week; Wk16 integration appears in applied questions). Per-topic counts are instructor-held and not printed. Logic: after how long, students ask what to revise; the next slide gives the one pattern that links the 14 questions. -->

---

## One pattern, nine weeks

![Each week broke a sound primitive by leaving out one check. Week 4: CBC has no tag. Week 5: Diffie-Hellman does not say who answers. Week 6: a check that answers differently leaks. Week 10: a repeated nonce. Week 11: a signature has a twin. Week 12: the certificate was not checked. Week 13: the server can read. Week 14: the password lands in the log. Week 15: a one-time key used twice.](img/w18-spine.svg)

```
failure = primitive_ok and check_missing
```

- The cipher or signature was fine; **one check was missing**
- Find the missing check and most questions answer themselves

<!-- The spine of the course: "textbook-secure primitive, real-system failure". Cold-call a week and ask for the missing check. Logic: the same shape fits W4 to W15, so a student who knows the shape can reason about a case never seen. The next slides give one line per week so the shape can be filled in. -->

---

## Callbacks: Weeks 1 to 6

![One idea from each early week. Week 1 threat model: assets, attacker, boundary. Week 2: salted slow hash. Week 3: a MAC is HMAC of key and message, not a hash of key plus message. Week 4: check the tag before trusting. Week 5: put a tag on the public value. Week 6: one failure answer.](img/w18-callbacks.svg)

```
h   = KDF(salt, password)           # W2
tag = HMAC(k, m)                    # W3   not SHA256(k + m)
t' == tag(k, nonce, c') ?           # W4   check first, then decrypt
open(k, nonce, c, t, ad) = p or FAIL    # W6   one failure answer
```

<!-- Equations are the ones used on the W2 to W6 slides. W5: tA = HMAC(AUTH_KEY, A) and check t' == HMAC(AUTH_KEY, A') (the lab tag covers the sender's public value only). Logic: each callback asks for the idea, so one memorable line per week is enough; the next slide does the same for Weeks 10 to 15. -->

---

## The big six: Weeks 10 to 15

![Week 10: lock the key with RSA, lock the messages with AES-GCM, never repeat a nonce. Week 11: a valid signature has a twin, so the id comes from the message. Week 12: check the certificate chain and the name. Week 13: end-to-end means the server sees only ciphertext. Week 14: send a proof, not the password. Week 15: a one-time key signs once.](img/w18-big-six.svg)

```
c1 xor c2 = m1 xor m2               # W10  same key + same nonce
txid = hash(pk, m)                  # W11  not sha256(r + s): the twin
ok = chain(cert, ca) and name(cert) == "bob"    # W12
server_sees = E(pk_B, m)            # W13  end-to-end
request = (nonce, proof)            # W14  not the password
one key, one signature              # W15  Lamport
```

<!-- Equations are the ones from the W10 to W15 slides. W16 is the integration week: the same ideas combined in one design, assessed through the applied questions. Logic: the six lines are the ideas the 14 questions come from; the next slide says how to write an answer. -->

---

## How to answer an applied question

![Four steps: name the primitive, find the missing check, say what the attacker can do, say the fix and one test.](img/w18-answer.svg)

```
answer = (primitive, missing_check, attack, fix)
```

1. **Primitive:** what is used?
2. **Missing check:** what is not verified?
3. **Attacker:** what can they do?
4. **Fix + test:** what stops it, and how would you check?

<!-- Model answer shape for a short question: "AES-CBC is used (primitive); nothing checks that the token was not changed (missing check); the attacker flips bits in the block before and turns guest into admin (attack); use GCM and check the tag first, then test that an edited token gets 403 (fix + test)." Short and specific beats long and general. Logic: the pattern slide says what to look for; this slide says how to write it so marks are not lost for vague answers. -->

---

## Before you sit down

![Individual work, 90 minutes of writing plus 10 minutes of administration, paper or an instructor-assigned quiz, permitted materials announced in Classroom.](img/w18-rules.svg)

- **Individual** work
- 90 + 10 minutes; paper or an instructor-assigned quiz
- Permitted materials: **announced in Classroom**
- Week 19 is only the **midterm make-up**, not a second final

<!-- Date, time, room and permitted materials are not known when this draft is written: fill them in when the academic office and the instructor announce them, do not guess. Logic: the last practical questions (what may I bring, is there a second chance) before the takeaway. -->

---

## Takeaway

![Know the pattern, name the missing check, state the fix.](img/w18-takeaway.svg)

- A sound primitive fails when **one check is missing**
- Name the missing check in one sentence
- Say the fix and how you would test it

<!-- Land the spine. Cold-call: "name the missing check in Week 12" (the certificate was not checked). Then: "what does Week 19 cover?" (only the midterm, W8 and W9). Logic: the exam asks the same three things in every question, so the takeaway is the three things. -->
