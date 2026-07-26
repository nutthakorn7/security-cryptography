# Lesson Plan — Week 18: Final, Written Exam

| | |
|---|---|
| **Course** | Security & Cryptography · course code `21025117` ([syllabus.md](../../syllabus.md), tiebreaker recorded in [course-plan-19weeks.md](../../course-plan-19weeks.md) *Decisions #1*; the [course specification](../course-specification.md) §1 still records the code as ⬚ — reconcile the two before print) |
| **Week / date** | 18 · ⬚ |
| **Contact time** | 90 min — a single written-exam block. No lecture, no lab, no weekly quiz ([AGENDA.md](../../AGENDA.md), *Week 8 / 18 — Written exam*: "120 min (midterm) / 90 min (final)", and the per-week time table row 18) |
| **Lab folder** | ⬚ (instructor-held paper) — course specification §6, row 18. There is no `labs/week18-*` directory in this repository, by design |
| **Slides** | ⬚ — no `slides/week18.md` exists. `slides/` carries decks for the twelve teaching weeks only (`week01.md`–`week06.md`, `week10.md`–`week15.md`), so there is no proctor deck for this sitting |
| **Covers** | Cumulative, emphasis **Weeks 10–16** (course specification §6 row 18; both papers' own headers) — read §2 before repeating that phrase to students |
| **Standards** | ⬚ — the course specification's schedule attaches no OWASP/CWE ids to the exam weeks, and this paper asks the student to supply none (it is single-best-answer multiple choice throughout) |
| **CLOs addressed** | **CLO1** select & justify · **CLO2** break · **CLO3** rebuild · **CLO4** protocol reasoning · **CLO5** evaluate & communicate (course specification §6, row 18 — this row assigns CLO**5**, not CLO6, unlike the Week 8 row). §2 reads that claim against what a multiple-choice paper can actually evidence |

> **This plan quotes no exam question, no option text, no answer letter and no flag.** Both forms
> and both keys are instructor-held and git-ignored (`.gitignore:41`); they are referenced here by
> path only, and the blueprint below stays at section granularity so this file can remain public.
> Where a defect in the papers is only describable by quoting the key, it is named but not
> quantified here and is reported to the instructor out of band instead.

---

## 1. What this paper evidences

This is an assessment week, so the objectives are stated as *what a script demonstrates about its
author*, not as what is taught. A student whose script scores well has shown that they can:

**Knowledge (K)**
- K1 — Recall, unaided and under time pressure, the Week 10–15 primitive- and protocol-level
  concepts at the granularity of picking the one correct statement out of five candidates
  (Sections 1–5 and 7 of the paper).
- K2 — Hold the cryptocurrency material the course examines but never teaches in a lecture week —
  Section 6. The course specification §6 closing note and `course-plan-19weeks.md` both record this
  as a deliberate decision ("Cryptocurrency … is **not** given its own teaching week — it's folded
  into the Wk18 written-exam item bank instead"). §2 explains why this is the paper's weakest
  claim.
- K3 — State what a primitive does *not* provide — the through-line
  `labs/week17-review/README.md` sets out in its *Recap — Weeks 10–16 core lesson* table (a
  signature proves authenticity, not uniqueness; "the traffic is encrypted" ≠ "encrypted to the
  right party"; TLS leaves the server inside the trust boundary; Grover dents where Shor breaks).

**Skills (P)**
- P1 — Discriminate a correct security claim from four plausible-sounding distractors. This is the
  same discrimination the term's *Audit the AI* tasks train (course specification §7: "plausible-
  sounding cryptographic nonsense is exactly what students must learn to detect"), here applied
  cold, with no machine and no reference.
- P2 — Recognise each Week 10–15 lab's failure mode from a written description alone, with no
  target running, no `exploit.py` and no worksheet to consult.
- P3 — Sustain that discrimination across seven topic areas inside 90 minutes — roughly 3 minutes
  per item, including reading five options.

**Attitude (A)**
- A1 — Sit an individual assessment ([SUBMISSION.md](../../SUBMISSION.md), *Rules for every
  submission*: labs, quizzes and exams are individual) and stand behind the script as their own
  work.
- A2 — **Note:** unlike the Week 8 paper, this paper carries **no ethics instruction line and no
  "answer in your own words" line** — a multiple-choice paper has no own-words dimension, and
  neither form restates [ETHICS.md](../../ETHICS.md). Integrity here is entirely procedural (§6),
  not a marked or even a printed item. Say the rules aloud; the script will not say them.
- A3 — Accept that guessing is structurally rewarded on this paper (both forms state "No negative
  marking; unanswered questions receive zero points") and answer every item — an instruction worth
  stating before the clock, because a student who leaves blanks is penalised by their own caution.

## 2. Exam blueprint — what is assessed

Taken from the two papers' own headers: **90 min · 100 pts · closed book · 30 single-best-answer
multiple-choice items, five options each (A–E), no negative marking, unanswered items score zero ·
100/30 ≈ 3.33 pts per item.** Kept at section granularity deliberately — nothing below narrows
down an individual item.

Both forms carry the same seven sections and differ only in how many items each section holds:

| Section | Topic | Form A | Form B | Teaching week | CLO reading |
|---|---|:--:|:--:|---|---|
| **1** | Asymmetric & Hybrid Encryption | 5 | 4 | Wk 10 | CLO1 |
| **2** | Digital Signatures & Zero-Knowledge Proofs | 4 | 5 | Wk 11 | CLO1, CLO2 |
| **3** | Secure Transport: TLS & Noise | 5 | 4 | Wk 12 | CLO4 |
| **4** | End-to-End Encryption | 4 | 5 | Wk 13 | CLO4 |
| **5** | User Authentication | 5 | 4 | Wk 14 | CLO1, CLO4 |
| **6** | Cryptocurrency | 4 | 5 | **none — exam-only** | ⬚ |
| **7** | Post-Quantum Cryptography | 3 | 3 | Wk 15 | CLO2, CLO4 |

The **per-section CLO attribution above is this plan's reading**, not the repository's: the course
specification assigns CLOs at *week* granularity (§6 row 18 → CLO1–CLO5) and nowhere maps them to
sections.

**Read the coverage honestly before claiming it in a programme review.**

- **Weeks 1–6 are 0 % of both forms.** Every section maps to Weeks 10–15 or to the untaught
  cryptocurrency block. Meanwhile `labs/week17-review/README.md` (*Exam-prep note*) tells students
  the Week 18 item bank "should weight roughly 60–70 % Wk10–16 content, 30–40 % Wk1–6 +
  review-week callbacks", the Week 17 Jeopardy carries a *First-Half Callback* category at
  **higher point values**, and `quizzes/weekly/week17-review-quiz.md` carries a Week 5 callback
  item. A student who revises in the proportion the repository promises spends roughly a third of
  their revision on material that is not on the paper. **Correct this verbally at the Week 17
  debrief** — see the instructor note in §3.
- **Week 16 is not examined at all.** "Emphasis Weeks 10–16" sends students to revise the capstone
  studio, and `quizzes/weekly/week17-review-quiz.md` item 10 asks about the capstone framing — but
  no section of either form draws on Week 16. The examinable band is effectively **Weeks 10–15
  plus cryptocurrency**.
- **Section 6 is examined but never taught, and the two forms do not carry it equally.** There is
  no Week 16-style capstone coverage to fall back on: no teaching week, no `slides/` deck, no lab
  folder, no entry in [readings.md](../../readings.md), no Jeopardy category in
  `labs/week17-review/README.md`, none in the instructor-held `instructor/week17-jeopardy-bank.md`
  either, and no item in `quizzes/weekly/week17-review-quiz.md`. Checked exhaustively: the
  repository records **no revision source for this material, student-facing or instructor-held**.
  On top of that, Form A
  carries 4 such items (≈ 13.3 pts) and Form B carries 5 (≈ 16.7 pts) — so two candidates on
  different forms face materially different amounts of untaught content. That is a **parallel-forms
  defect**, not merely a coverage gap. Decide before the sitting: supply a named revision source
  and announce it in Week 17, or drop the section and rescale. Do not run it silently.
- **CLO3 cannot be evidenced here, and CLO5 cannot either.** The specification's CLO3 is "rebuild
  the construction correctly … and demonstrate *empirically* that the original attack now fails";
  CLO5 is "explain a finding to both a technical and a non-technical audience". This paper produces
  **no prose whatsoever** — a candidate writes nothing but a chosen letter per item. Both outcomes
  are carried elsewhere: CLO3 by the Week 19 practical, CLO5 by the worksheets' *Audit the AI* /
  EiPE / *Prompt Problem* parts and the Week 19 graded demos. Course specification §6 row 18 claims
  CLO1–CLO5 for this week; claim **CLO1, CLO2 and CLO4 at recognition level** and attribute the
  rest honestly.
- **CLO2 is recognition, not cryptanalysis.** There is no running target and no interpreter; a
  candidate can identify a break but cannot perform one. The performing half is Week 19.
- **Marking is fully objective.** Both keys state "no partial credit — single best answer". Unlike
  Week 8, there are no method marks and no borderline-answer rulings to settle — but also no
  partial credit for a candidate who reasons correctly and mis-selects (§7).
- **Known drift in the item bank — say it, then fix the bank, not the paper.**
  `instructor/exams/item-bank.md` heads its FINAL POOL "Weeks 10–15, cumulative" and its preamble
  says "Final (Wk18) is cumulative, emphasis **Wk10–15**", while the course specification,
  `AGENDA.md`, [SUBMISSION.md](../../SUBMISSION.md) and both papers say **Wk10–16**. Given the
  bullet above, the bank's narrower wording is the more accurate one — reconcile in the bank (§8).

## 3. Preparation before the day

- **Students, before the exam:** revise via Week 17's consolidation — `labs/week17-review/README.md`,
  the cumulative review quiz `quizzes/weekly/week17-review-quiz.md` (30 min, 25 pts), *Security
  Jeopardy: Champions Edition*, and the mock final `labs/week17-review/mock-ctf.md`.
- **The format-practice gap — check this first.** `labs/week17-review/mock-ctf.md` is a dry-run of
  the **Week 19 practical** ("Format: same as the Week 19 final practical … teams … sandbox targets
  only"). There is **no mock written paper** for Week 18, unlike Week 7, whose block includes a
  mock in the Weeks 8–9 format. Worse, the multiple-choice format students have practised is not
  this paper's: `quizzes/weekly/week07-review-quiz.md` and `quizzes/weekly/week17-review-quiz.md`
  both use **four options (a–d)**, and [SUBMISSION.md](../../SUBMISSION.md) describes the weekly
  quiz as "6 Q: 5 MCQ + 1 short". This paper is **30 items × five options (A–E)**, 100 % of the
  written final. Nothing in the term trains it. At minimum, walk the cohort through the paper's
  instruction rubric — five options, single best answer, no negative marking, answer everything —
  at the Week 17 debrief.
- **Instructor, at the Week 17 debrief** ([AGENDA.md](../../AGENDA.md), Week 7 & 17 block,
  `4:30–5:00` *Debrief: common mistakes + exam logistics*): announce which form is being sat (§5);
  announce the delivery route (§4); confirm the closed-book rule, which unlike the sibling course's
  final **is** printed on both papers; resolve the "cumulative" wording and the Weeks 1–6 weighting
  (§2); state the Section 6 decision and its revision source (§2); and walk the answer-rubric above.
- **Instructor, before the day:** confirm the form; settle the option-order/re-lettering decision
  (§6) *before* printing, because it changes both the paper and the key; produce the printed paper
  from the chosen form and proof-read the printed copy (§11); have the matching key to hand and
  only that key. Because `instructor/` is git-ignored, both papers and both keys must be moved out
  of band — a clone of the public repository contains none of them.
- **Instructor note — do not fix any of this by editing graded material.** Two mismatches are
  recorded above and **this plan changes neither file**:
  1. `labs/week17-review/README.md` promises the Week 18 bank will carry 30–40 % Weeks 1–6 content;
     both built forms carry none.
  2. `instructor/exams/item-bank.md` scopes the final to Wk10–15 while every student-facing document
     says Wk10–16.

  Either the papers move or the summaries do. That is an instructor decision about graded material,
  not a documentation tidy-up; it is reported upward rather than applied here. (A third, smaller
  drift in the same file: `labs/week17-review/README.md` still tells students the Jeopardy question
  bank is "not yet built", but `instructor/week17-jeopardy-bank.md` exists and is built. Harmless
  for this exam; worth correcting before Week 17 runs.)
- **⬚** Room, seating plan, number of sections/sittings, invigilator roster, script paper and
  printing arrangements are not recorded in this repository.

## 4. The 90-minute block — logistics

`AGENDA.md` budgets **90 min** for the written final and nothing else; it budgets no briefing or
settling time, so the pre-clock allowance is **⬚** and must come from the faculty's own exam
regulations. There is **no proctor deck** for this week (`slides/week18.md` does not exist), so the
order of business below is assembled from the papers' own headers and
[SUBMISSION.md](../../SUBMISSION.md) — brief from this table, or write the deck first (§11).

| Step | Action | Source |
|---|---|---|
| Before the clock | State the delivery route actually in use — `SUBMISSION.md` lists W18 as "on paper / Google Form (90 min)". Decide beforehand; do not announce it as an option | `SUBMISSION.md`, *EXAMS* |
| Before the clock | State the duration (90 min), the total (100 pts), that there are 30 items across seven topic sections, and that the paper is **closed book** — both forms print this in their header | Paper headers |
| Before the clock | State the answer rubric: choose the **one best** answer of five (A–E); no negative marking; unanswered items score zero — therefore answer every item | Paper instruction line |
| Before the clock | State the no-phones / no-AI rule (**⬚** — institutional) and that the paper is individual work. Neither form prints an ethics or an own-words line, so this must be said, not assumed | This plan; `SUBMISSION.md`; [ETHICS.md](../../ETHICS.md) |
| Before the clock | State the early-finish rule — 30 items in 90 min is ~3 min per item, so expect finishers well before time (§6) | This plan |
| Clock starts | 90 min. Keep talking minimal once the clock runs | `AGENDA.md` |
| On the paper | Name, Student ID and Date fields are printed on both forms — check they are filled before collecting | Paper header |
| At collection | Collect the scripts; remind the cohort that Week 19 is a 240-min block — a capstone CTF tournament (`0:00–2:30`) **plus graded CryptoVault demos** (`2:30–4:00`, 10-min demo + 5-min Q&A per team), so their Docker targets and their project must both be working | `AGENDA.md`, *Week 19*; `project/README.md` |

**Materials allowed.** **Closed book**, stated in both papers' own headers — this is sourced, not a
decision to be made. Note the difference from Week 8, whose header reads "Closed book unless stated
otherwise": there is no conditional here, and the repository asks for no Week 17 cheat-sheet
deliverable (unlike Week 7, whose README makes a one-page sheet a deliverable). If an open-note
concession is granted anyway, it contradicts the printed paper — amend the paper first.

## 5. Forms A and B, and make-up sittings

Course specification §9 states the intended arrangement: *written exams exist in parallel Form A/B
drawn from a maintained item bank.* **For Week 18 both forms exist** — unlike Week 8, which has
Form A only (see `week08-midterm-written.md` §5). The exposure here is different, and worse.

| Form | Where it lives | Status | Use |
|---|---|---|---|
| **A** | `instructor/exams/week18-final-written-formA.md` | Built. Instructor-held and git-ignored (`.gitignore:41`) | The sitting this cohort takes |
| **B** | `instructor/exams/week18-final-written-formB.md` | Built. The **disjoint complement** of Form A, same 90 min / 100 pts / 30 items | Make-up sitting; second section; next cohort |

- The two forms are **halves of one source**. Both headers record that they are ported from the
  same 60-question answer-keyed bank in the KOSEN68 archive, split disjointly, "together … cover
  all 60 source questions exactly once". Sit both in one term — a cohort split across two sections
  — and **the entire source bank is burned in a single term**, with no Form C and no rotation
  source that can supply the shape (§8).
- **The forms are proportional but not equivalent on Section 6.** Sections 1–5 trade items
  symmetrically (5/4 against 4/5), which is defensible for taught material. Section 6 does not:
  4 items on Form A against 5 on Form B, on content with no teaching week (§2). Equalise, drop, or
  rescale before running both in the same term.
- **The most likely leak is upstream of this repository.** Both headers state that question text,
  answer choices **and answer letters** were ported *unchanged* from the prior offering's exam
  document, and `course-plan-19weeks.md` *Decisions #1* records that last year's delivery ran
  through a Google Form. A repeating student, a shared drive, or a photograph from the previous
  cohort therefore plausibly holds both of this year's papers **already answered**. Treat prior-year
  circulation, not this sitting, as the primary threat (§11).
- Once a form is deployed it is burned. Record **which form each sitting used**, on the day, so the
  make-up runs the other one.
- **⬚** Make-up sitting date, eligibility rules and any cap on the make-up mark are institutional
  and not recorded in this repository.

## 6. Invigilation and academic integrity

This repository has **no `instructor/anti-cheating.md`**, so the written-exam invigilation protocol
has to be assembled from what is recorded and marked ⬚ where it is not.

**Sourced and in force:**

- The paper is **individual work** ([SUBMISSION.md](../../SUBMISSION.md), *Rules for every
  submission*: "labs/quizzes/exams are individual").
- **Name + Student ID** are required on every submission; both forms carry Name, Student ID and
  Date fields.
- [ETHICS.md](../../ETHICS.md) applies and was acknowledged by every student in Week 1 — though,
  unlike the Week 8 paper, **neither form restates it** (§1, A2).
- **AI-tool disclosure** is a standing course rule (`SUBMISSION.md`).
- **Random live checks** ("You may be asked to reproduce a task or explain your fix live") are a
  course-wide control, so a viva probing a candidate's grasp of a topic they scored on is available
  where authorship is in doubt — though on a letter-only script there is no handwriting or working
  to interrogate, which makes the seating record below the primary evidence.

**Deliberately not imported.** `SUBMISSION.md`'s anti-cheating section is scoped to worksheets,
flags and the online weekly quizzes — per-student flags derived from the student ID,
identity-stamped screenshots showing `whoami`/timestamp, MOSS/JPlag similarity checking of pushed
code. None of those is a written-paper control, and the personalised-flag pipeline is in any case
not yet live (README.md status note; `SUBMISSION.md`'s own caveat). Do not cite them as if they
invigilated this paper.

**The Google Form route is materially stronger here than it was at Week 8.** `SUBMISSION.md`'s
quiz controls — individual, time-limited, one attempt, locked to the school account, shuffled
questions **and options** — apply directly to a 30-item multiple-choice paper, and the Week 8
argument against the route (Section C's byte/hex working records badly in a text box, and method
marks become hard to award) does not exist here: there is no working to capture and no partial
credit to award. A Form also marks itself. Decide once, before the Week 17 debrief.

**Option order is the one integrity control this paper actually needs.** Checked against both keys:
the distribution of correct-answer letters across the two forms is **materially unbalanced**, in a
way that rewards a candidate who applies a fixed guessing heuristic and that effectively narrows
each item's option set. The specifics are deliberately **not recorded in this public file**; they
are held outside it and must be given to the instructor out of band, and they belong in
`instructor/exams/item-bank.md` alongside the affected items. The defect is **inherited** — both
headers state that answer letters were ported unchanged from the source bank — so the fix belongs
at deployment or in the source bank, not in the porting. Two workable fixes:
- **Google Form route:** enable *shuffle option order* per item. The Form stores the correct
  *option*, not a letter, so it marks itself correctly regardless of display order and the letter
  key becomes irrelevant. This is the cheapest fix and the strongest argument for the route.
- **Paper route:** permute the options and **re-key** before printing. The letter key in
  `…-formA-answers.md` / `…-formB-answers.md` no longer applies to a re-lettered paper — mark
  against the re-keyed working copy, and say so on the copy.

**Early finishers.** 30 items in 90 min is roughly 3 min per item, so a substantial part of the
cohort will finish early — a pressure the 120-min prose midterm did not create. Decide, and state
before the clock, whether a candidate may leave early, whether re-entry is permitted, and how
scripts are collected from early leavers without disturbing the room. **⬚** — institutional.

**If copying is found:** keep the evidence and follow the course's own route — ETHICS.md plus
KOSEN's conduct process (`SUBMISSION.md`, closing line) and **⬚** (the institutional policy itself,
which the course specification §11 also leaves as ⬚).

**⬚** Invigilator roster, bag/phone handling and seating plan. **Keep a seating record anyway.** On
a letter-only script, identical wrong answers on adjacent scripts is the *only* similarity signal
available, and without a seating record the adjacency cannot be checked after collection.

## 7. Marking

- **Who marks: ⬚.** The course specification §1 names one instructor and records no TA, second
  marker or moderation arrangement. Marking is objective here, so a section split is unnecessary —
  but if a Form route is used, one person should own the Form's answer-key configuration.
- **The keys:** `instructor/exams/week18-final-written-formA-answers.md` and
  `instructor/exams/week18-final-written-formB-answers.md`. Both are git-ignored; transfer them out
  of band before marking day and never "fix" the gap by committing them.
- **Match the key to the deployed form before the first script.** The two papers share their title
  stem, duration, total, item count, item numbering (1–30) and all seven section titles. The only
  distinguishing mark is the form letter. A form/key mismatch here would not look obviously wrong
  until the marks did — write the form letter on the board and on the script header, and open only
  the deployed form's key.
- **No partial credit.** Both keys state "no partial credit — single best answer", and both papers
  state "no negative marking". So none of Week 8's borderline-answer rulings arise: a candidate who
  reasons correctly and selects the wrong letter scores zero on that item, and there is nothing on
  the script to award method marks against.
- **Settle the 3.33 arithmetic before marking, not after.** The papers and keys record
  100/30 ≈ 3.33 pts per item. Taken literally, 30 × 3.33 = **99.9**, not 100. Mark each script out
  of **30 raw** and scale by 100/30 to get the percentage — that is what the papers' own "100 pts
  total" claims, and it avoids a rounding drift that would otherwise cost every candidate 0.1.
- **If options were re-lettered for deployment (§6), mark against the re-keyed copy**, not the
  stored key.
- **Score entry.** Final is **25 %** of the course and covers **both** this paper and the Week 19
  practical (course specification §4; `syllabus.md` §3). **⬚ — how the two combine into that 25 %
  is not recorded anywhere in this repository**; there is no gradebook file here, unlike the
  sibling course. Note also that the Week 19 half is **team-graded** (`syllabus.md` §3: "Week 18
  written *(individual)* + Week 19 capstone CTF *(team)*"), so the combination rule decides how much
  of a nominally mixed component is individual. Fix the rule before marking, not after seeing the
  marks.
- **⬚** Grading scale and letter-grade boundaries (institutional).

## 8. After the exam — item analysis and the item bank

The repository defines the *loop* but not the *statistics*. Everything below that is not sourced is
marked ⬚ rather than guessed. A multiple-choice paper supports a sharper analysis than Week 8's
prose paper did — use it.

1. **Mark, then look at the paper rather than the students.** For each item note where the cohort
   clustered: near-universal correct (the item discriminated nothing), near-universal wrong (the
   item was mis-set or mis-worded, or the teaching week did not land), and
   split-with-strong-students-wrong (the item is probably ambiguous).
2. **Count the distractors, not just the key — this is what an MCQ paper gives you for free.** An
   option nobody selected is a dead distractor: a five-option item with two dead options behaves
   like a three-option item and its guessing floor rises accordingly. An item where one wrong option
   out-drew the key is either mis-keyed or teaching a misconception that landed harder than the
   correct answer. Record both classes against the item.
3. **Separate a bad item from a real gap.** This is the last written instrument of the term, so a
   cohort-wide failure cannot be retaught to this cohort. Route it to the emphasised teaching week
   (10–15) and to Week 17's consolidation, not to the bin.
4. **The one same-term use of the analysis.** If marking finishes before Week 19, a topic the cohort
   failed cohort-wide is fair ground for the **5-min Q&A** in the Week 19 graded CryptoVault demos
   (`AGENDA.md`, Week 19, `2:30–4:00`). It probes rather than re-teaches, and it is optional.
5. **Replace, don't patch — and be honest that this paper currently has nowhere to draw from.**
   `instructor/exams/item-bank.md`'s stated purpose is exactly this rotation, but its FINAL POOL is
   built as **A Concepts (short answer) · B Spot the flaw · C Applied · D Defense & design** *(the
   bank's own spelling)* — prose items, mirroring the **midterm's** shape. This paper is 30
   single-best-answer multiple-choice items across seven topic sections. **The pool cannot supply a
   single replacement item in the deployed format.** Rotating an item here means *writing* a new
   five-option item with four working distractors, or changing the paper's shape and stating that it
   is no longer a parallel form. Budget for writing before promising rotation.
6. **Write the corrections back into the bank.** While you are in there, fix three things:
   its FINAL POOL scope ("emphasis Wk10–15" against Wk10–16 everywhere else, §2); the option-letter
   imbalance and its per-item notes (§6); and the bank's own premise — it justifies rotation by
   saying the *public* `weekNN-*.md` exam files are static and leak between cohorts, which is not
   true in this repository, where `instructor/` is git-ignored. `week08-midterm-written.md` §8
   flagged the same inherited wording; the real leak vector here is the **prior-year source
   document** (§5), and that changes the mitigation from "rotate after use" to "assume this cohort
   may already hold both papers".
7. **Close the loop on the forms.** Record which form this cohort sat, and whether Section 6 ran,
   was dropped or was rescaled — the next cohort's default must not be the paper this one
   photographed.
8. **Where a first-half gap goes: nowhere, currently.** Week 8's plan (§8.6) routes cohort-wide
   Weeks 1–6 weaknesses into "the Week 18 paper's 30–40 % first-half share". Both built forms carry
   **no** Weeks 1–6 items (§2), so that route is presently closed. Either write first-half items
   into the bank, or correct the promise in `labs/week17-review/README.md` and in the Week 8 plan —
   an instructor decision, recorded here rather than made here.

**⬚ Not defined anywhere in this repository, and deliberately not invented here:** which item
statistic is used (facility index, discrimination index, point-biserial, or none), the threshold at
which an item counts as discriminating poorly, who reviews the analysis, when it is done, and where
it is recorded. Fix these once and record them in `instructor/exams/item-bank.md`, not in this
public file.

## 9. Assessment for this week

| Instrument | Evidence | Outcome | Weight |
|---|---|---|---|
| Final written paper, Sections 1–7 | The script, 30 items, 100 pts | K1–K3, P1–P3 | Part of the 25 % final component, shared with the Week 19 practical (combination rule ⬚ — §7) |
| Sitting record: form sat, whether Section 6 ran, seating, incidents | Conditions under which the script was produced | A1, A3 | Integrity control, not a mark |
| Item analysis (§8) | Per-item and per-distractor performance across the cohort | Course-level, not student-level | Feeds `instructor/exams/item-bank.md` and next cohort's Week 17 |

**No worksheet, no weekly quiz and no flag this week** — nothing is submitted to Classroom or
GitHub, and no Docker target is stood up.

## 10. Materials

- Paper, **Form A** — instructor-held, git-ignored, **never published**:
  `instructor/exams/week18-final-written-formA.md`
- Paper, **Form B** — instructor-held, git-ignored, **never published**:
  `instructor/exams/week18-final-written-formB.md`
- Keys — instructor-held, git-ignored, **never published**:
  `instructor/exams/week18-final-written-formA-answers.md`,
  `instructor/exams/week18-final-written-formB-answers.md`
- Rotation source — instructor-held: `instructor/exams/item-bank.md` (FINAL POOL) — but see §8.5:
  it cannot supply this paper's format
- Proctor deck — ⬚, does not exist for Week 18 (§4, §11)
- What students revised from: `labs/week17-review/README.md` (Jeopardy: Champions Edition,
  cheat-sheet-free), `labs/week17-review/mock-ctf.md` (practical dry-run only — §3),
  `quizzes/weekly/week17-review-quiz.md`, the Week 10–15 lab folders
  `labs/week10-hybrid-encryption` … `labs/week15-pqc`, and [readings.md](../../readings.md)
- Revision source for Section 6 (cryptocurrency): **⬚ — none exists in this repository** (§2)
- What comes next: `project/README.md` (Week 19 graded final demo, self-audit, crypto-agility note)
- Course frame: [course specification](../course-specification.md) §4, §6, §9 ·
  [AGENDA.md](../../AGENDA.md) · [syllabus.md](../../syllabus.md) §3 ·
  [SUBMISSION.md](../../SUBMISSION.md) · [ETHICS.md](../../ETHICS.md)
- **⬚** Printed papers, answer sheets, room booking, invigilator roster

## 11. Risks and contingencies

| Risk | Mitigation |
|---|---|
| **The prior cohort plausibly holds both papers, answered.** Both forms' headers record that question text, options *and* answer letters were ported unchanged from the KOSEN68 source exam, and `course-plan-19weeks.md` *Decisions #1* records that last year's delivery ran through a Google Form | Assume prior-year circulation before assuming this sitting is the leak. If a repeating student is in the cohort or the archive document is known to have circulated, neither form is safe as-is — re-order and reword items, or write fresh ones, before the sitting |
| **Section 6 (cryptocurrency) is examined but never taught** — no week, no deck, no lab, no `readings.md` entry, no Jeopardy category, no review-quiz item — and Form A carries 4 such items against Form B's 5 | Decide before Week 17: supply and announce a named revision source, or drop the section and rescale the paper. If it runs, equalise the count across the two forms first — otherwise two candidates sit materially different papers |
| **Both forms carry 0 % Weeks 1–6**, while `labs/week17-review/README.md` promises the Week 18 bank will weight 30–40 % first-half content and the Week 17 Jeopardy gives first-half callbacks *higher* point values | Correct it verbally at the Week 17 debrief so revision time matches the paper. The durable fix — first-half items in the bank, or an amended promise — is a decision about graded material and is reported upward, not applied here (§3) |
| **The correct-answer letters are unevenly distributed across both forms**, rewarding a fixed guessing heuristic and effectively narrowing each item's option set | Shuffle option order per item (Google Form does this natively and marks against the option, not the letter), or permute and **re-key** before printing. Decide before printing — it changes both paper and key (§6) |
| **The rotation source cannot refill this paper.** `instructor/exams/item-bank.md`'s FINAL POOL is short-answer / spot-the-flaw / applied / design; the paper is seven sections of five-option MCQ. After both forms are burned there is no Form C | Budget for *writing* five-option items with working distractors, not selecting them; or accept a shape change and stop calling the result a parallel form (§8.5) |
| **Both forms in one term burns the whole 60-item source** — they are disjoint halves of a single document | Sequence sittings so only one form is needed, or accept that next cohort's paper must be written from scratch. Record which form each section sat |
| A Form B sitting marked against the Form A key — the two share title stem, duration, total, item numbering and all seven section titles | Write the form letter on the board and the script header; open only the deployed form's key (§7) |
| `instructor/` is git-ignored, so a colleague marking from a clone of the public repository has **neither paper nor key** | Transfer both out of band before marking day; never resolve this by committing them — the repository is public |
| **No mock written paper and the wrong MCQ format practised** — Week 17's mock is the Week 19 *practical*, and both review quizzes use four options (a–d) against this paper's five (A–E) | Walk the answer rubric at the Week 17 debrief (five options, single best, no negative marking, answer everything) and repeat it before the clock; consider adding a short written dry-run to Week 17 for the next cohort |
| **No proctor deck** (`slides/week18.md` does not exist) — the pre-clock briefing has no artefact and depends on the invigilator remembering it | Brief from §4 of this plan, or write the deck before the day; either way hand the invigilator a written running order |
| **The paper prints no ethics line and no own-words line**, unlike the Week 8 paper, so a cohort that sat Week 8 may read the omission as a relaxation | State the individual-work, no-AI and no-phones rules aloud before the clock (§4); they are procedural here, not printed |
| **Printing a Markdown paper.** Each item carries five prose options; a page break between an item's stem and its later options changes what the candidate is choosing between. A handful of items on each form also carry non-ASCII mathematical characters — a middle dot, a multiplication sign, an arrow and a radical — that a substituting font can render wrongly or drop, and one of them sits inside an option rather than a stem | Export to PDF once, read the printed proof item by item, confirm no item's stem is separated from any of its five options and that every mathematical character survived, and only then duplicate |
| **90 min for 30 items (~3 min each) means early finishers**, a pressure the 120-min midterm did not create | Decide the leave/re-entry and collection stance before the day and state it before the clock (§6) |
| **The 3.33-per-item arithmetic sums to 99.9**, not 100 | Mark out of 30 raw and scale ×100/30 (§7); state the total as 100 pts, as both papers do |
| **No lab block this week**, so nothing is checked on a machine — Week 19 is a 240-min block combining a CTF tournament with graded project demos | Use the collection slot to state the Week 19 running order and tell teams to dry-run their CryptoVault build before they leave the room |
| A student misses the sitting | Run the form the main cohort did not sit (§5). Eligibility, date and any mark cap are **⬚** |

## 12. Post-teaching reflection

*Complete after the session — this also feeds the course's engagement data.*

- Attendance / completion: ⬚
- Form sat (A / B), by which section, and whether a make-up is now owed: ⬚
- Delivery route used (paper / Google Form), and whether option shuffling was enabled: ⬚
- Whether Section 6 (cryptocurrency) ran, was dropped or was rescaled, and what revision source was
  given for it: ⬚
- Whether the Weeks 1–6 weighting was corrected verbally at the Week 17 debrief: ⬚
- Time actually used by the cohort (how many finished before 90 min?): ⬚
- Section-by-section mark distribution, and which section was weakest: ⬚
- Items that discriminated poorly, and dead distractors found in the per-option counts (§8.2): ⬚
- Whether any item's wrong option out-drew the key, and what that says about the teaching week: ⬚
- Evidence that the prior-year source document had circulated (§5, §11): ⬚
- Integrity incidents, and how they were handled: ⬚
- Anything to change before this exam runs again: ⬚
