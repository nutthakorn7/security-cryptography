---
marp: true
theme: default
paginate: true
header: "Cryptography and Network Security · Week 19"
---

<!-- DRAFT. Deck for the midterm make-up sitting. Eligibility, the exact date, time, room and the split of the 100 minutes between the written and the practical part are NOT decided yet: the instructor announces them in Classroom, so none is printed here. Delivery: 100 minutes, individual. Show slides 2, 3, 6 and 7 while students sit down; slides 4 and 5 are a revision aid posted before the sitting. Logic of the deck: say what the sitting is, what it covers, what is different about the papers, the six ideas behind Weeks 1 to 6, what the practical evidence contains, and what to prepare. Each slide answers one question and ends with the next. -->

# Week 19
## Midterm make-up
Cryptography and Network Security · Nutthakorn Chalaemwongwan

<!-- Say: this is a second sitting of the midterm only. It is not a second final and it adds no new marks. Logic: the title fixes the purpose so that nobody expects new content or a team practical (the old Week 19 practical was cancelled and its 15 points moved to the Week 18 written exam). -->

---

## A second sitting of the midterm

![Week 19 is a second chance at the midterm only: the Week 8 written exam and the Week 9 practical. It is not a second final and adds no new marks.](img/w19-what.svg)

```
marks = W8 8 + W9 12 = 20       # the midterm; the make-up adds nothing on top
```

- The **Week 8** written exam (8 course points)
- The **Week 9** practical (12 course points)
- **Weeks 1 to 6 only**, no new marks

<!-- Source: SUBMISSION.md exam table and docs/lesson-plans/week19-final-practical.md. How the make-up result is used (replace, combine) is set by the instructor and announced in Classroom: do not state it. Logic: first what it is; the next slide says how the papers differ from the first time. -->

---

## Different papers, announced in Classroom

![New variants and keys held by the instructor, not the papers or per-student variants of the original sittings. The instructor announces eligibility, date, format and the split of the 100 minutes in Classroom.](img/w19-format.svg)

- New variants and keys, **held by the instructor**
- Not the papers or per-student variants of the first sittings
- Who may sit, the date, the format and the split of the 100 minutes: **announced in Classroom**
- Individual work

<!-- Source: the W19 lesson plan. Nothing here is guessed: until the announcement exists, answer "it will be in Classroom". Logic: after "what is it", students ask "is it the same paper"; the next slide shows the six ideas the papers draw on. -->

---

## What the papers draw on: Weeks 1 to 6

![Week 1 threat model. Week 2 salted slow hash. Week 3 HMAC. Week 4 tag check before trust. Week 5 a tag on the public value. Week 6 one failure answer.](img/w19-weeks.svg)

```
h   = KDF(salt, password)           # W2
tag = HMAC(k, m)                    # W3   not SHA256(k + m)
t' == tag(k, nonce, c') ?           # W4   check first, then decrypt
open(k, nonce, c, t, ad) = p or FAIL    # W6   one failure answer
```

<!-- The same six ideas as the callbacks on the final (Week 18 deck). Week 5: put a tag on the public value (tA = HMAC(AUTH_KEY, A)); it covers the sender's public value only. Logic: this is the revision map; the next slide covers what to hand in for the practical part. -->

---

## Practical part: what goes in the evidence

![The practical evidence PDF has three parts: what you observed, the payload you used, and the mitigation you propose. It is submitted through the course platform.](img/w19-evidence.svg)

```
evidence = (observation, payload, mitigation)
```

- **Evidence:** what you observed
- **Payload:** what you sent
- **Mitigation:** what stops it
- One PDF through the course platform

<!-- Source: SUBMISSION.md, W9 row ("evidence PDF (evidence, payload and mitigation) through the submission platform"). Whether the make-up has a practical part and how long it lasts is announced by the instructor: this slide is for students who sit it. Logic: the practical part is marked on evidence, not on a flag alone. -->

---

## Before you come

![Check the Classroom announcement for who may sit, the date, the time and the room. Bring your student ID. For the practical part prepare the same laptop, Docker Desktop and Python environment as for Week 9.](img/w19-before.svg)

- Read the **Classroom** announcement: who, date, time, room
- Bring your **student ID**
- Practical part: same **laptop, Docker Desktop and Python** set-up as Week 9
- Test the set-up the day before

<!-- If local infrastructure fails during the practical part the instructor provides an equivalent prepared trace or harness under the same criteria without reducing task time (W19 Classroom draft). Logic: the last thing students need is a checklist; the takeaway repeats the one line. -->

---

## Takeaway

![Weeks 1 to 6, the midterm again, new papers, no new marks.](img/w19-takeaway.svg)

- Week 19 is the **midterm make-up**, not a second final
- Weeks 1 to 6, **new papers**, no new marks
- Everything else is **announced in Classroom**

<!-- Cold-call: "what does Week 19 cover?" (the Week 8 written exam and the Week 9 practical, Weeks 1 to 6). "Does it add marks?" (no). Logic: three facts are all a student must leave with. -->
