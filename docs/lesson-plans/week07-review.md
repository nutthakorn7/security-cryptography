# Lesson Plan — Week 7: Reflection & Review (pre-Midterm)

| | |
|---|---|
| **Course** | Security & Cryptography (course code `21025117`, per [syllabus.md](../../syllabus.md); the [course specification](../course-specification.md) §1 still records the code as ⬚ — confirm with the registrar before print) |
| **Week / date** | 7 · ⬚ |
| **Contact time** | 300 min (course specification §1: 2 lecture + 3 laboratory hours; [AGENDA.md](../../AGENDA.md) runs the review weeks as one continuous block) |
| **Lab folder** | `labs/week07-review` — **`README.md` only**. No worksheet, no code, no `mock-ctf.md` (Week 17's folder has one; Week 7's mock is carried inline in its README) |
| **Slides** | ⬚ — there is no `slides/week07.md` in the repository (decks exist for Weeks 01–06 and 10–15) |
| **Type** | Review — **no new content**. Consolidates Weeks 1–6 |
| **Standards consolidated** | The "Analogous CWE" lines of the six weeks under review: CWE-320, CWE-330 (Wk1) · CWE-916, CWE-327, CWE-759/760 (Wk2) · CWE-347, CWE-290 (Wk3) · CWE-353, CWE-649, CWE-347 (Wk4) · CWE-322, CWE-300 (Wk5) · CWE-347, CWE-757, CWE-204 (Wk6) |
| **CLOs addressed** | **CLO1–CLO4** (course specification §6, week 7 row) |

---

## 1. Session objectives

By the end of this week a student can:

**Knowledge (K)**
- K1 — Recall, without notes, the one-line core lesson of each of Weeks 1–6 as recorded in the lab README's recap table, and name the analogous CWE that goes with it.
- K2 — State the course's through-line in their own words: confidentiality, integrity and authenticity are three separate properties, and a primitive that gives one does not give the others for free.
- K3 — Describe the shape of both midterm papers — Week 8 is written (120 min), Week 9 is a hands-on practical (150 min), and **both cover Weeks 1–6 only** — well enough to plan revision time against them.

**Skills (P)**
- P1 — Re-run **any one** of the Week 2–6 labs cold, without their notes from that week, and recapture the flag or evidence artefact solo (the lab README's mock practical brief).
- P2 — For each challenge attempted, record the payload/technique **and** a one-line fix, then self-check against that week's `exploit.py` and `worksheet.md`.
- P3 — Produce a one-page cheat sheet that is their own compression of the half-term, not a transcription of a worksheet.
- P4 — Identify honestly which of the six topics they cannot yet do unaided, and say so in the debrief.

**Attitude (A)**
- A1 — Work only against the sandbox targets supplied by the course, under [ETHICS.md](../../ETHICS.md) — this holds in a practice run exactly as it does in a graded one.
- A2 — Treat the mock as calibration rather than performance: an unsolved challenge discovered today is worth more than a solved one copied from a neighbour.
- A3 — Keep treating confident cryptographic prose — from an AI or from a classmate — as something to verify (course specification §7).

## 2. Key ideas (the through-line)

The lab README states the arc the review has to make retrievable: Week 2 is about *storage* (one-way,
no key); Week 3 shows a keyed hash is not authentication; Week 4 shows encryption is not integrity;
Week 5 shows key agreement is not identity; Week 6 shows what happens when Weeks 3 and 4 are bolted
together wrongly, and how to bolt them together correctly. Week 1 sits underneath all five: the
primitive is almost never the weak link — the threat model, the key management or the composition is.

Every one of the six weeks is therefore the same question in a different costume: **which of
confidentiality, integrity and authenticity does this construction actually give me, and which am I
assuming it gives me?** The exam will ask that question in an unfamiliar wrapper, so today's job is
retrieval under time pressure rather than re-teaching. The second job is calibration: students
consistently over-rate what they can reproduce with the worksheet closed, and the mock is the
cheapest place to find that out.

## 3. Prior knowledge and preparation

- **Students, before class** (lab README, step 1): re-read the Week 1–6 worksheets
  (`labs/week01-intro/worksheet.md` … `labs/week06-aead/worksheet.md`), each week's README
  "Concepts"/"Analogous CWE" line, and the slide decks published so far (`slides/week01.md` …
  `slides/week06.md`). Bring the machine they intend to sit Week 9 on.
- **Instructor, before class — the four Flask targets.** Weeks 2, 3, 4 and 6 each run *two*
  containers off `python:3.12-slim` with the lab directory bind-mounted, and each container runs
  `pip install --no-cache-dir -r requirements.txt` **at container start**. That is eight installs per
  student if the whole set is brought up (`flask`, `requests`, plus `bcrypt` in Week 2 and
  `cryptography` in Weeks 4 and 6). Pre-pull the image and bring the stacks up once on the room
  network the day before.
- **Instructor, before class — Week 5 is different.** `labs/week05-key-exchanges` builds its own
  image (`build: .`, a `Dockerfile` that installs `cryptography` at *build* time) and publishes **no
  host ports** — its evidence is container log output, not a browser page. Build it ahead of the
  session.
- **Instructor, before class — the Jeopardy board does not exist.** The lab README points at "the
  instructor board for the full 30-question set"; no such file ships for Week 7 (the git-ignored
  `instructor/` directory holds `week17-jeopardy-bank.md` for the *other* review week, and
  `week07-review-quiz-answers.md` for today's quiz). Build the 6 × 5 board plus the Final Wager
  beforehand from each week's `worksheet.md` — the README asks that clue phrasing stay close to
  worksheet phrasing — and from `instructor/exams/item-bank.md`.
- **Instructor, before class — two decisions to announce today.** Whether the one-page cheat sheet is
  admitted to the Week 8 written exam (the README offers it "if the instructor permits open-note"):
  ⬚. Whether the cumulative quiz runs on paper or as a Google Form (SUBMISSION.md routes quizzes
  through a Form posted in Classroom): ⬚. Both change how students spend tonight.
- **Prerequisite state:** the Week 2–6 labs have been completed and submitted. A student who never
  stood up one of those targets will lose the mock block to environment setup.

## 4. Consolidation — the six weeks under review

| Wk | Topic (kind) | Signature game | Must be retrievable cold | Re-tested today by |
|---:|---|---|---|---|
| 1 | Intro & threat-modelling a crypto system (CONCEPTUAL) | 🐍 "Snake Oil Bingo" | Textbook-secure ≠ system-secure; trust boundaries around key material; CIA applied to crypto, and that availability failures are usually key-management failures | Jeopardy *Threat Modeling*; quiz Q1 and Q8 |
| 2 | Hash functions (LAB) | 🔓 "Crack the Leaked DB" | Preimage vs collision resistance; why a *fast* hash is the wrong tool for passwords; what a per-user salt defeats; what a work factor buys — and what it does not | Mock practical #1; Jeopardy *Hashing*; quiz Q2, Q3, Q10 |
| 3 | MACs (LAB) | 🍪 "Forge the Admin Cookie" | `H(key ‖ message)` is not a MAC; Merkle–Damgård length-extension; why HMAC's nested construction closes it; related pitfalls — non-constant-time tag comparison, replay | Mock practical #2; Jeopardy *MACs*; quiz Q4 |
| 4 | AES & block-cipher modes (LAB) | 🎯 "Flip Your Way to Admin" | `P_i = D(C_i) XOR C_{i-1}`; that you edit the ciphertext block **before** the one you want to change; ECB pattern leakage; IV/nonce reuse; AEAD as the modern default | Mock practical #3; Jeopardy *AES Modes*; quiz Q5, Q9 |
| 5 | Key exchanges (HYBRID) | 🕵️ "The Silent Third Wheel" | DH gives secrecy against an eavesdropper and no identity guarantee at all; the active attacker runs two independent handshakes; authenticating the public keys does **not** cost forward secrecy | Mock practical #4; Jeopardy *Key Exchange*; quiz Q6, Q8; the Final Wager |
| 6 | Authenticated encryption (LAB) | 🔮 "Read the Secret Without the Key" | Encrypt-then-MAC is the safe generic composition; a distinguishable padding response *is* an oracle; why AES-GCM has no padding to probe and checks the tag before releasing plaintext | Mock practical #5; Jeopardy *AEAD*; quiz Q7, Q9 |

**Coverage gap to name out loud.** Week 1 is CONCEPTUAL by design — no Docker target, no flag — so the
mock practical has no Week 1 challenge, and the lab README says so explicitly. Threat modelling is
carried today by the Jeopardy *Threat Modeling* category and by quiz questions 1 and 8, and it **is**
examined in Week 8. A student who revises only from the mock practical will walk into the written
paper having skipped a sixth of the syllabus.

## 5. Session run-sheet — 300 min

Timings are AGENDA.md's "Week 7 & 17 — Review (300 min)" block. The lab README maps the same shape
onto the usual 120/180 split: the lecture slot becomes the review game, the lab slot becomes the mock.

| Time | Block | What happens |
|---|---|---|
| 0:00–0:30 | **Cumulative review quiz** | `quizzes/weekly/week07-review-quiz.md` — individual, closed book |
| 0:30–1:45 | **Crypto Jeopardy** | Team quiz-show across the six topics |
| 1:45–2:00 | **Break** | Students bring their mock targets up during the break, not at 2:00 |
| 2:00–4:30 | **Mock midterm dry-run** | Written half (Sections A–D) + practical half, in the Weeks 8–9 format |
| 4:30–5:00 | **Debrief** | Common mistakes (§6) + midterm logistics (§7) |

### 5.1 Cumulative review quiz — 0:00–0:30

| Field | Value |
|---|---|
| Instrument | `quizzes/weekly/week07-review-quiz.md` — "Weekly Quiz — Week 7 (Cumulative Review, Weeks 1–6)" |
| Blueprint as written | MCQ 7 × 1 pt + short answer 3 × 3 pts = **16 pts**, 10 questions |
| Stated duration | "~20 min" in the file header; AGENDA.md allots the 30-minute slot above |
| Covers | Threat modelling · hashing · MACs · AES modes · key exchanges · AEAD, one or two questions per week |
| Conditions | Individual, closed book |
| Delivery | Google Form posted in this course's Classroom at quiz time (SUBMISSION.md); the markdown file prints as the paper fallback |
| Where it counts | The 10% weekly-quizzes / participation component (course specification §4) |

> **Instructor note — points drift, decide before you print.** AGENDA.md records the cumulative
> review quizzes as **25 pts** ("quiz1 / quiz2 — 25 pts", and footnote ‡); SUBMISSION.md
> independently tells students the same figure ("two bigger 25-pt quizzes in the review weeks
> (W7 pre-midterm, W17 pre-final)", line 88); the Week 7 file as it stands totals **16**. Week 17's
> file does total 25. Resolve this in the quiz file, its key (`instructor/week07-review-quiz-answers.md`),
> and SUBMISSION.md's quiz description *before* the session — do not rescale marks mid-class, and do
> not let a mismatch between the paper, the gradebook, and what students were told land on students.

Weeks 7 and 17 carry no six-question weekly quiz of their own; the cumulative quiz **is** this week's
retrieval practice (AGENDA.md).

**Cohort rotation.** The quiz file is static and reused each cohort, which is a leak risk. Swap two or
three MCQs and/or a short-answer item from `instructor/exams/item-bank.md` into a cohort copy, holding
the total constant at whatever §5.1's note settles on.

### 5.2 Crypto Jeopardy — 0:30–1:45

- **Name.** The lab README calls it **"Crypto Jeopardy"**; the course specification §6 abbreviates the
  same activity as "🏆 Jeopardy recap (Wk 1–6)" and AGENDA.md as "Crypto Jeopardy team review".
- **Categories** — exactly the six columns in the README's board, one per week under review:
  *Threat Modeling (Wk1) · Hashing (Wk2) · MACs (Wk3) · AES Modes (Wk4) · Key Exchange (Wk5) ·
  AEAD (Wk6)*.
- **Board** — 5 values per category, **100/200/300/400/500**, plus a **Final Wager** round in which
  teams wager any or all of their points. That is the 30-question set the README refers to; it must be
  built beforehand (§3).
- **Clue style** — Jeopardy-style, answered in question form. The README ships five worked sample
  clues (Hashing 100, MACs 300, AES Modes 300, Key Exchange 400, AEAD 500 flagged as a Daily Double
  candidate) plus the Final Wager clue on the active-versus-passive attacker model. Use them as the
  calibration for the other 25 and keep phrasing close to the worksheets.
- **Sources** — every Conventional-arm Part 1/2 question and every hands-on Task deliverable in Weeks
  1–6 is fair game at some point value (README instructor note).
- **Teams** — run by Houses; points feed the participation / Houses layer (syllabus.md §3). If this
  course's CTFd deployment is not yet live — AGENDA.md and SUBMISSION.md both hedge it as not yet
  running — tally on the whiteboard instead; nothing today is graded on those points.
- **Purpose** — this is the retrieval slot for Week 1, which the practical half cannot reach. Weight
  the board accordingly rather than filling it with padding-oracle questions.

### 5.3 Mock midterm dry-run — 2:00–4:30

Ungraded, participation only. The goal is comfort with the format, not new content.

**Written half (mirrors Week 8)** — four sections, in the shape the lab README publishes:

| Section | Focus |
|---|---|
| A — Concepts | Hash properties; MAC vs hash vs signature; AEAD's three guarantees; DH vs authenticated DH |
| B — Spot the vulnerability | Short code/protocol snippets — name the CWE-equivalent flaw and the one-line fix |
| C — Attack walkthrough | Given a vulnerable construction, walk the attack through step by step |
| D — Design | Design a secure cookie/session scheme, or justify an AEAD choice against a stated deployment constraint |

Section marks are carried by the instructor-held paper (`instructor/exams/`, git-ignored) and are not
published here: ⬚ in this document.

**Practical half (mirrors Week 9)** — re-run **any one** of the Week 2–6 labs cold, without that
week's notes, and recapture the flag or evidence artefact solo:

| # | Challenge | Topic | Target and start command |
|---|---|---|---|
| 1 | Crack the admin password from a leaked unsalted-MD5 store | Hashing (W2) | `labs/week02-hash` — `docker compose up`, ports 8094/8095 |
| 2 | Forge an admin cookie via length-extension | MACs (W3) | `labs/week03-macs` — the Week 7 README's row gives neither command nor ports; the lab's own README runs `docker compose up -d`, ports 8092/8093 |
| 3 | Bit-flip a CBC session token from `role=guest` to `role=admin` | AES modes (W4) | `labs/week04-aes-modes` — `docker compose up`, ports 8096/8097 |
| 4 | MITM an unauthenticated DH handshake and recover the relayed secret | Key exchange (W5) | `labs/week05-key-exchanges` — the Week 7 README gives `docker compose -f docker-compose.vulnerable.yml up`; the lab's own README and the compose file's header comment both run it as `docker compose -f docker-compose.vulnerable.yml up --build`. No published ports; read the container logs |
| 5 | Run a padding-oracle attack to decrypt a ciphertext byte-by-byte | AEAD (W6) | `labs/week06-aead` — `docker compose up`, ports 8098/8099 |

> **Instructor note — two corrections the lab README needs, which this plan must not make for it.**
> (a) Row 2 of that table describes the W3 attack as "**HMAC** length-extension". Length extension
> works against the *secret-prefix* construction `SHA256(MAC_SECRET + data)` on `:8092`; HMAC on
> `:8093` is precisely what defeats it, and the whole point of the week is that the two are not the
> same thing. Students who revise from that row will get the Week 8 Section B question backwards.
> (b) Row 2 is also the only row with no ports listed; they are 8092 (vulnerable) / 8093 (HMAC fixed).
> Fix both in `labs/week07-review/README.md` and in the curriculum monorepo copy together, per
> [CLAUDE.md](../../CLAUDE.md).

**For each challenge attempted** (README): record the payload/technique and a one-line fix, then
self-check against that week's `exploit.py` and `worksheet.md`. The README is explicit that hints and
full solutions live in each week's own directory and that no spoiler-free copy is needed, because this
is a *repeat* of a completed lab.

**Formative checkpoints.** By the midpoint of the 2:00–4:30 block every student should have at least
one challenge landed end-to-end;
a student with none is usually still fighting the environment, not the cryptography — put them on
Week 2 or Week 4, the two shortest paths, and mark the mechanism explanation rather than the
keystrokes. A student who finishes early should take a *second* week cold rather than polish the first,
and should prefer Week 3 or Week 6, the two that need real computation (glue-padding derivation;
oracle query logic) rather than a wordlist run.

### 5.4 Debrief — 4:30–5:00

Run §6's list against the room ("hands up who is still shaky on this one") and drill the two or three
that draw the most hands. Then give the Week 8/9 logistics from §7, and collect or sight the one-page
cheat sheet.

## 6. Misconceptions to re-test

Every row below is a correction that already exists somewhere in Weeks 1–6, because the naive version
was wrong when it met the running lab.

| # | Misconception | Where it comes from | How to re-test it today |
|---:|---|---|---|
| 1 | "Use current algorithms and long enough keys and your crypto is secure" | The Week 1 Audit-the-AI exhibit is exactly this argument, stated fluently and with every individual claim true; the week's lesson is that key management and composition, not key length, are where real systems fail | Jeopardy *Threat Modeling*; quiz Q1 — ask for the *root cause* wording, not the fix |
| 2 | "It's encrypted, so it's protected" | Week 1's CIA section names this as the conflation the course exists to correct; Week 4 demonstrates it — the token is encrypted and still edited to `role=admin` | Jeopardy *AES Modes*; ask which of C/I/A the CBC token actually had |
| 3 | "A salt makes a hash safe for passwords" | Week 2's exhibit pairs SHA-256 (praised for being fast) with one module-level constant salt; `slides/week02.md`'s presenter note calls this the week's "looks professional, is wrong" | Quiz Q2 and Q3; ask what a *per-user random* salt buys that a constant does not |
| 4 | "bcrypt means solved" | Week 2's README warns against exactly this overclaim, and `slides/week02.md` flags it as the trap in worksheet Task 5b: the fixed store resists *this fast technique*, not a patient per-hash dictionary against a weak password | Ask: "who still cracks that account, and what stops them?" — the answer is a password policy, not the hash |
| 5 | "Add a secret to a hash and you have a MAC" | Week 3's whole premise; `slides/week03.md` sets it up as the natural — and wrong — next question after Week 2 | Quiz Q4; Jeopardy *MACs 300* (the length-extension clue) |
| 6 | "Length extension needs the secret" | Week 3's README: `exploit.py` assumes the secret's *length* is known (16 ASCII bytes here) and never its *value* | Mock practical #2 — make them state which bytes are glue padding and why the value never appears |
| 7 | "HMAC in the code means the MAC is safe" | Week 3's objectives name the related pitfalls the exploit does *not* target: non-constant-time tag comparison and replay | Jeopardy *MACs*: "the tag is a correct HMAC and the design is still broken — how?" |
| 8 | "To change a plaintext block, tamper with that block" | Week 4's block-layout section: `P1 = AES_decrypt(C1) XOR C0`, so you edit **C0** and accept that block 0 becomes garbage the app never reads | Mock practical #3 — ask for the byte range edited, not the flag |
| 9 | "We switched to GCM, so tampering is handled" | `slides/week04.md` names Q10's trap: GCM helps only if the application actually checks the tag and does not swallow the exception (in the spirit of CWE-347) | Jeopardy *AES Modes 400/500*; Written-half Section B |
| 10 | "DH gives us a secure channel" | Week 5's README: plain DH gives secrecy against an eavesdropper and **no** way to check who the secret was agreed with | Quiz Q6; mock practical #4 — the relay completes two clean handshakes and nobody errors |
| 11 | "Authenticating the exchange costs forward secrecy" | Week 5's fix paragraph: the signed mode still runs a fresh DH every session; what changes is that the public keys carry a tag | Jeopardy *Key Exchange 400*; ask what is still safe if the pre-shared key leaks next year |
| 12 | "If the endpoint never returns plaintext, it leaks nothing" | `slides/week06.md`'s presenter note on the vulnerable `/decrypt` branch — a 200-versus-403 answer *is* the oracle | Mock practical #5; then "what did the 200 tell you?" |
| 13 | "More precise error codes are better engineering" | Week 6's exhibit returns distinct codes per failure case; `slides/week06.md` notes that split is a *three*-way oracle, worse than the two-way one it replaced | Jeopardy *AEAD 500*; Written-half Section D |
| 14 | "HMAC is a reasonable way to store passwords" | Quiz Q10 is built on this exact claim, and it is the cumulative Week 2 × Week 3 confusion | Quiz Q10 — require the *two different problems* to be named separately |
| 15 | "Passive and active attackers are a detail" | The Final Wager clue and quiz Q8 both turn on it; Weeks 5 and 6 are the two weeks where the attacker must be active | Final Wager; then ask which Week 1–6 attacks work passively |

## 7. Exam preparation

### 7.1 Week 8 — written

- **Format:** single 120-minute block, no lab (AGENDA.md, "Week 8 / 18 — Written exam"). Delivered on
  paper or by Google Form in class (SUBMISSION.md).
- **Covers:** Weeks 1–6 only — including Week 1, which has no lab (lab README).
- **Shape:** the four sections rehearsed in §5.3's written half. Marks and the item pool live in the
  instructor-held paper under `instructor/exams/` (git-ignored); published here as ⬚.
- **Tell students plainly** that Week 1 and the conceptual halves of Weeks 5 and 6 — the parts with no
  flag attached — are examinable, since those are precisely the parts a revision plan built around
  re-running labs will miss.

### 7.2 Week 9 — practical

- **Format:** 150 minutes. AGENDA.md's Week 9 agenda: `0:00–0:10 rules + target check · 0:10–2:30
  solve challenges`.
- **Covers:** Weeks 1–6 (SUBMISSION.md's exam table).
- **Submission:** flags/evidence **plus** payload **plus** mitigation, via the CTF Form / Classroom
  (SUBMISSION.md). AGENDA.md describes the artefact mix as flags in the Week 2–4, 6 style and evidence
  log lines in the Week 5 style. The one-line mitigation is the cheapest mark on the paper and the
  most often left blank — say so today.
- **Instructor note:** reconcile that public description against the instructor-held Week 9 key before
  you tell students what to revise. The mock's five-challenge list and the exam's own selection are
  not identical, and students calibrate their revision on whichever they hear first.
- **Attribution caveat.** SUBMISSION.md's status note is honest that flags are currently a shared
  placeholder rather than per-student values: `instructor/seed_flags.py` exists and is verified, but
  this course has no live CTFd deployment yet. Until it does, a submitted flag proves little on its
  own — the payload, the mitigation and the viva spot-check are what carry attribution.

### 7.3 What today's mock does *not* reproduce — say this explicitly

| | Mock (today) | Week 9 |
|---|---|---|
| Stakes | ungraded, participation | part of the 20% midterm (course specification §4) |
| Material | a *repeat* of labs already completed | the same labs, but sat cold |
| Aids | each week's `exploit.py` and `worksheet.md` sit in the student's own checkout, and the README tells them to self-check against those | none of that is available in the exam |
| Challenge set | five, chosen by the student | fixed by the instructor-held key |

The third row is the one that quietly ruins the calibration: "without your notes from that week" is a
request, not a technical control, because the solution script is one directory away. Ask students to
attempt each challenge with the lab folder closed and to open `exploit.py` only for the self-check.

### 7.4 Logistics to read out in the debrief

None of these are recorded in the repository:

- Week 8 (written) — date / time / room: ⬚
- Week 9 (practical) — date / time / room: ⬚
- Whether the one-page cheat sheet is admitted to Week 8: ⬚ (announce **today** — it changes how the
  sheet gets built)
- Machine readiness: anyone whose targets did not come up today must be fixed before Week 9, not on
  the day.

### 7.5 Deliverable — the one-page cheat sheet

Each student submits their own one-page sheet. The lab README's suggested contents: the six one-line
lessons from the recap table, the CBC decryption relation, the length-extension idea, and the AEAD
composition rule (encrypt-then-MAC is safe; the other two orders are not). Building it *is* the
studying, which is why it must not be a shared file.

## 8. Assessment for this week

| Instrument | Evidence | Outcome | Weight |
|---|---|---|---|
| Cumulative review quiz | Quiz score | K1, K2 | Part of the 10% weekly-quizzes / participation component |
| Crypto Jeopardy | Team points | K1, K2 | Non-graded engagement (Houses); no CTFd scoreboard for this course yet |
| Mock written half | Attempted Sections A–D | K1–K3 | **Ungraded** — participation |
| Mock practical half | Payload/technique + one-line fix per challenge attempted | P1, P2, A1 | **Ungraded** — participation |
| One-page cheat sheet | The sheet | P3 | ⬚ (the README states the deliverable, not a mark for it) |
| Debrief self-assessment | Named weak areas | P4, A2 | Formative — feeds the instructor's Week 8/9 support list |

There is **no worksheet for Week 7**: the 12 graded worksheets are Weeks 1–6 and 10–15 (course
specification §4). The graded midterm follows in Weeks 8–9 and is worth 20%.

## 9. Materials

- Lab: `labs/week07-review/README.md` (the only file in the folder)
- Quiz: `quizzes/weekly/week07-review-quiz.md`
- Slides: ⬚ — none for this week; the decks under review are `slides/week01.md` … `slides/week06.md`
- Mock targets: `labs/week02-hash`, `labs/week03-macs`, `labs/week04-aes-modes`,
  `labs/week05-key-exchanges`, `labs/week06-aead`
- Self-check files already in the student's checkout: each week's `exploit.py`, `fixed_app.py` and
  `worksheet.md`; Week 5's `docker-compose.fixed.yml` for the "after" evidence
- Course documents: [AGENDA.md](../../AGENDA.md) (review-week block) ·
  [course-plan-19weeks.md](../../course-plan-19weeks.md) · [syllabus.md](../../syllabus.md) ·
  [SUBMISSION.md](../../SUBMISSION.md) · [ETHICS.md](../../ETHICS.md) ·
  [course specification](../course-specification.md)
- Instructor-only, git-ignored: `instructor/week07-review-quiz-answers.md`,
  `instructor/exams/item-bank.md`, `instructor/exams/` (the Week 8 and Week 9 papers and keys),
  `instructor/week01-intro-answer-key.md` … `instructor/week06-aead-answer-key.md`,
  `instructor/seed_flags.py`
- What comes next: the Week 8 written exam and the Week 9 practical — both instructor-held, with no
  lab folder in the repository (course specification §6 records ⬚ for both)

## 10. Risks and contingencies

| Risk | Mitigation |
|---|---|
| **The Jeopardy board does not exist for Week 7.** The README defers to an "instructor board" that ships nowhere; only Week 17 has a bank file. Unprepared, the 75-minute middle block has no content | Build the 6 × 5 board plus the Final Wager beforehand from the Week 1–6 worksheets and `instructor/exams/item-bank.md`, seeded by the README's five sample clues. Fallback: run the README's recap table as a cold-call round and extend the mock |
| **The cumulative quiz totals 16 pts, AGENDA.md says 25 — and SUBMISSION.md tells students 25 too (line 88).** A paper that does not match the gradebook or what students were told, discovered at 0:05 | Settle it in the quiz file, its key, and SUBMISSION.md's quiz description before printing (§5.1). Never rescale mid-session |
| **Eight `pip install` runs on the room network.** Weeks 2, 3, 4 and 6 each install `flask` + `requests` (+ `bcrypt`, + `cryptography`) at *container start*, twice per lab. In a teaching week that is one round-trip; today it can be eight per student | Pre-pull `python:3.12-slim` and bring the four stacks up once the day before; have students start containers during the 1:45–2:00 break; keep an offline image copy (`docker save` / `docker load`). Students who did Weeks 2–6 on the same machine already have the layers cached |
| **Week 5 behaves unlike the other four.** It is the only lab that *builds* an image and the only one with no published host ports, so a student hunting for a page on `localhost` will conclude it is broken | Brief it as a log-reading exercise: `docker compose -f docker-compose.vulnerable.yml up --build`, read the `RELAY INTERCEPTED …` line, then `docker compose -f docker-compose.vulnerable.yml down` before starting the fixed file |
| **Week 5's run never "finishes".** `alice` exits once her message is sent, but `bob` and `relay` are long-running servers, so `up` sits there and looks hung; both compose files also pin the same container names (`week05-alice`, `week05-bob`, `week05-relay`), so the two modes cannot be up at once and a stale scrollback is easy to mistake for this run's evidence | Follow the README: `Ctrl-C`, then the matching `docker compose -f … down`, before switching modes. The fixed mode's evidence is the **absence** of the interception line plus `AUTH FAILED - ABORTING` from both ends — which is only meaningful in a clean log |
| **The repository lives under OneDrive.** The Week 6 README records that verification had to be run from a scratch copy because OneDrive placeholder files can break an in-place `docker build`; Week 5 is the build-dependent lab today | Copy the lab directory to a local scratch path before building, or ensure the files are pinned as "always keep on this device" before class |
| **`python exploit.py` fails on the host.** All four exploit scripts import `requests`, which the containers install but the host does not | Have students `pip install requests` on the host beforehand, or run the exploit from inside a container. A student without it should reason the attack through instead — that is what the practical's partial credit rewards |
| **Eight containers on a student laptop.** The ports (8092–8099) are all distinct, so there is no bind clash across the four Flask labs — the failure mode is memory, not ports | Run one lab at a time; the challenges are independent and the mock asks for "any one" of them |
| **The mock's "cold" condition is voluntary.** `exploit.py` solves each challenge end-to-end and sits in the student's own checkout | Ask for the lab folder to be closed until the self-check, and make the debrief question "which one could you not have done alone?" — put those names on the Week 8/9 support list |
| **Revision built only on the labs skips Week 1** — which has no target by design and is examined in Week 8 | Weight the Jeopardy *Threat Modeling* category deliberately and say the coverage gap out loud (§4) |
| **A student cannot sit the Form quiz** (Forms are posted in this course's Classroom, and only this course's) | Print `quizzes/weekly/week07-review-quiz.md` — it carries name/ID/date fields — and mark to the same total settled in §5.1 |

## 11. Post-teaching reflection

*Complete after the session — this also feeds the course's engagement data.*

- Attendance / completion: ⬚
- Time actually taken per block (vs. plan): ⬚
- Where the class got stuck, and what unblocked them: ⬚
- Mock challenges left unlanded by more than a third of the room: ⬚
- Misconceptions from §6 that actually surfaced in the debrief (and any new ones): ⬚
- Whether the Jeopardy board's clue phrasing tracked the worksheets closely enough to feel like revision rather than ambush: ⬚
- Anything to change before this week runs again: ⬚
