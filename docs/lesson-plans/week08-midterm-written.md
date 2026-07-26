# Lesson Plan — Week 8: Midterm, Written Exam

| | |
|---|---|
| **Course** | Security & Cryptography · course code `21025117` ([syllabus.md](../../syllabus.md), tiebreaker recorded in [course-plan-19weeks.md](../../course-plan-19weeks.md) *Decisions #1*; the [course specification](../course-specification.md) §1 still records the code as ⬚ — reconcile the two before print) |
| **Week / date** | 8 · ⬚ |
| **Contact time** | 120 min — a single written-exam block. No lecture, no lab, no weekly quiz ([AGENDA.md](../../AGENDA.md), *Week 8 / 18 — Written exam*, and the per-week time table row 8) |
| **Lab folder** | ⬚ (instructor-held paper) — course specification §6, row 8. There is no `labs/week08-*` directory in this repository, by design |
| **Slides** | ⬚ — no `slides/week08.md` exists; this repository carries decks for the teaching weeks only |
| **Covers** | Weeks 1–6 |
| **Standards** | ⬚ — the course specification's schedule attaches no OWASP/CWE ids to the exam weeks. Section B's instruction asks the student to supply a CWE where applicable; no id is named in this plan |
| **CLOs addressed** | **CLO1** select & justify · **CLO2** break · **CLO3** rebuild · **CLO4** protocol reasoning · **CLO6** ethics & evidence (course specification §4, midterm row, and §6, row 8) |

> **This plan quotes no exam question, no answer and no flag.** The paper and its key are
> instructor-held and git-ignored (`.gitignore:41`); they are referenced here by path only, and
> the blueprint below stays at section granularity so this file can remain public.

---

## 1. What this paper evidences

This is an assessment week, so the objectives are stated as *what a script demonstrates about its
author*, not as what is taught. A student whose script scores well has shown that they can:

**Knowledge (K)**
- K1 — Recall and restate, unaided, the primitive-level concepts of Weeks 2–6 (Section A, 30 pts).
- K2 — Classify a flaw shown as a short code snippet against the CWE taxonomy rather than
  describing it loosely (Section B's instruction asks for the vulnerability, the CWE where
  applicable, and the fix).
- K3 — State what a primitive does *not* provide — the course's own through-line, that
  "confidentiality, integrity, and authenticity are three separate properties, and a primitive
  that gives you one does not give you the others for free"
  (`labs/week07-review/README.md`, *The through-line*).

**Skills (P)**
- P1 — Read a short code snippet cold and give the flaw, its CWE where applicable, and the fix
  (Section B, 20 pts).
- P2 — Carry an applied attack argument through on paper, with no running target and no
  interpreter to check against, showing the byte/hex working the paper's instruction line requires
  for computational answers (Section C, 30 pts).
- P3 — Produce a threat model and a defence argument as prose an engineer could act on, not as a
  list of keywords (Section D, 20 pts).

**Attitude (A)**
- A1 — Answer in their own words, as the paper's own instruction line requires.
- A2 — Carry the rules of engagement into a written scenario: the paper states that sandbox and
  ethics rules apply to every scenario on it ([ETHICS.md](../../ETHICS.md), acknowledged by every
  student in Week 1).
- A3 — Sit an individual assessment ([SUBMISSION.md](../../SUBMISSION.md), *Rules for every
  submission* — labs, quizzes and exams are individual) and stand behind the script as their own
  work.

## 2. Exam blueprint — what is assessed

Taken from the paper's own header: **120 min · 100 pts · closed book unless stated otherwise**,
covering Weeks 1–6. Kept at section granularity deliberately — the paper is held back until the
day it deploys, so nothing below narrows down an individual item.

| Section | Marks | Shape | Weeks drawn on | CLOs |
|---|---|---|---|---|
| **A — Concepts** | 30 (6 × 5) | Short answer | 2, 3, 4, 5, 6 | CLO1, CLO4 |
| **B — Spot the Vulnerability** | 20 (4 × 5) | Name the flaw (+ CWE where applicable) and give the fix, from a code snippet | 2, 3, 4, 6 | CLO2, CLO3 |
| **C — Applied** | 30 (5 × 6) | One multi-part scenario worked on paper, byte/hex working shown | 4, 6 | CLO2, CLO3 |
| **D — Defense & Design** *(the paper's own spelling)* | 20 (2 × 10) | Extended written answer | 1, 5, 6 | CLO1, CLO4 |

**Read the coverage honestly before claiming it in a programme review.**

- **CLO4** (protocol-level reasoning) rests on one of the two Section D items plus a single
  Section A item. This paper is not where CLO4 is chiefly evidenced — Weeks 12–15 are.
- **Week 1** (threat-modelling a crypto system) is examined inside one half of a single 10-pt
  item — realistically about 5 of 100 pts — even though `labs/week07-review/README.md` tells
  students that Weeks 8–9 examine Week 1 alongside Weeks 2–6. Say what the real weighting is at the
  Week 7 debrief so nobody spends revision time in proportion to the promise rather than the paper.
- **CLO3** is evidenced here **on paper only**. The specification's wording is "rebuild the
  construction correctly … and demonstrate *empirically* that the original attack now fails"; a
  written script can carry the rebuild argument but structurally cannot carry the demonstration.
  The empirical half is Week 9's practical. Do not double-count the two.
- **CLO6** is carried by the paper's ethics instruction line and by the sitting conditions in §6,
  not by a marked item.
- **CLO5** (evaluation and communication) is deliberately absent — course specification §4 assigns
  no CLO5 to the midterm row. It is carried by the worksheets' *Audit the AI* / EiPE / Prompt
  Problem parts instead.
- The paper is **Week 4/6-heavy**: Section C in full, plus items in A, B and D.

> **Known drift — say this aloud at the Week 7 debrief.** `labs/week07-review/README.md` describes
> the mock written half's Section A as "MCQ/short answer". The paper's Section A is six
> short-answer items and contains no MCQ. A student who practised MCQ technique for the mock has
> prepared the wrong skill for 30 % of the paper. Correct it verbally in Week 7; do not let it
> surface first in the exam hall.

## 3. Preparation before the day

- **Students, before the exam:** revise Weeks 1–6 through Week 7's consolidation
  (`labs/week07-review/README.md`) — the cumulative review quiz
  (`quizzes/weekly/week07-review-quiz.md`), Crypto Jeopardy, and the mock midterm dry-run in the
  Weeks 8–9 format. Week 7's deliverable is a one-page **cheat sheet**, which that README describes
  as an open-note aid *if the instructor permits open-note*.
- **Instructor, at the Week 7 debrief** ([AGENDA.md](../../AGENDA.md), Week 7 block, *Debrief:
  common mistakes + exam logistics*): announce the open-note decision **before** students write the
  cheat sheet; announce the calculator rule at the same time (§4); state which form is being sat
  (§5); and correct the Section A shape (§2).
- **Instructor, before the day:** confirm the form; produce the printed paper from that form and
  proof-read the printed copy (§11); have the matching key to hand and only that key. Because
  `instructor/` is git-ignored, both the paper and the key must be moved out of band — a clone of
  the public repository contains neither.
- **Instructor note — do not fix this by editing graded material.**
  `quizzes/weekly/week07-review-quiz.md` totals **16 pts** (7 × 1 pt MCQ + 3 × 3 pt short answer)
  and states "~20 min", while `AGENDA.md` budgets Week 7's `0:00–0:30` for it and calls it 25 pts,
  and `SUBMISSION.md` (line 88, *QUIZ*) calls the two cumulative quizzes "bigger 25-pt quizzes".
  Either the quiz or the two summaries has to move. This plan changes neither; the mismatch is
  reported upward.
- **⬚** Room, seating plan, number of sections/sittings, invigilator roster, script paper and
  printing arrangements are not recorded in this repository.

## 4. The 120-minute block — logistics

`AGENDA.md` budgets **120 min** for the written midterm and nothing else; it budgets no briefing or
settling time, so the pre-clock allowance is **⬚** and must come from the faculty's own exam
regulations. Unlike the sibling course there is **no proctor deck** for this week, so the order of
business below is assembled from the paper's own header and [SUBMISSION.md](../../SUBMISSION.md) —
brief from this table, or write the deck first (§11).

| Step | Action | Source |
|---|---|---|
| Before the clock | State the delivery route actually in use — `SUBMISSION.md` lists W8 as "on paper / Google Form in class (120 min)". This must be decided beforehand, not announced as an option | `SUBMISSION.md`, *EXAMS* |
| Before the clock | State the duration (120 min), the total (100 pts), the four sections A–D, and the closed/open-note rule | Paper header |
| Before the clock | State that computational answers must show the byte/hex working, not just a final value — this is the paper's own instruction and it is what makes Section C markable in parts | Paper instruction line |
| Before the clock | State the calculator rule (**⬚** — decide it; Section C is hand-computed) and the no-phones rule (**⬚** — institutional) | This plan |
| Before the clock | State that the paper is individual work, answered in the student's own words, and that the AI-disclosure and ethics rules apply | `SUBMISSION.md`; [ETHICS.md](../../ETHICS.md) |
| Clock starts | 120 min writing; keep talking minimal once the clock runs | `AGENDA.md` |
| On the paper | Name, Student ID and Date fields are printed on the paper — check they are filled before collecting | Paper header |
| At collection | Collect the scripts; remind the cohort that Week 9 is a 150-min hands-on CTF practical and their Docker targets must already work | `AGENDA.md`, *Week 9* |

**Materials allowed.** The default is **closed book** — the paper's own header says "Closed book
unless stated otherwise". The only documented candidate aid is the Week 7 one-page cheat sheet,
which `labs/week07-review/README.md` makes conditional on the instructor permitting open note. The
decision itself is **⬚**: record it here once made, because it changes what Week 7 asks students to
produce, and announce it before they produce it.

## 5. Forms A and B, and make-up sittings

Course specification §9 states the intended arrangement: *written exams exist in parallel Form A/B
drawn from a maintained item bank.* **For Week 8 that is not yet true, and the gap has an
operational consequence — plan around it rather than discovering it on the day.**

| Form | Where it lives | Status | Use |
|---|---|---|---|
| **A** | `instructor/exams/week08-midterm-written.md` | Built. Instructor-held and git-ignored (`.gitignore:41`) until the day it deploys | The sitting this cohort takes |
| **B** | ⬚ — **does not exist for Week 8** | To be built from the MIDTERM POOL of `instructor/exams/item-bank.md` | Make-up sitting; repeat cohort |

- Week 18 has both forms built (`instructor/exams/week18-final-written-formA.md` and
  `…-formB.md`). Week 8 has Form A and its key only. **A make-up sitting therefore has no second
  paper to run**, and a repeat cohort has nothing to rotate to.
- Form A's own instructor note states that the paper is static and leaks after use, and prescribes
  rebuilding/rotating a Form B from fresh questions for a repeat cohort — the same convention the
  sibling course follows.
- **Building Form B is not an assembly job — count unseen items, not slots.** The MIDTERM POOL
  holds 8 Concepts items, 5 Spot-the-flaw items, 3 Applied items and 3 Defence & design items,
  against a paper needing 6 / 4 / one 30-pt scenario / 2. The slot arithmetic looks comfortable and
  is misleading, because several pool entries restate Form A's own items in different words. Read
  the pool against the deployed paper before drawing from it; on the current contents the count of
  genuinely *unseen* items is roughly **five of eight in Section A, two of five in Section B, and
  one of three in Section D** — so B and D both need new items written, not just selected.
- **Section C is the hard blocker.** The pool's Applied entries are three separate ~6-pt items,
  whereas Form A's Section C is a single 30-pt scenario in five escalating parts. A Form B drawn
  purely from the pool either changes Section C's shape — and stops being a parallel form — or
  needs a fresh scenario written for it. Budget for writing that scenario, plus the Section B and D
  items above, before promising parity.
- Once a form is deployed it is burned. Record **which form each sitting used**, on the day, so the
  make-up runs the other one and next cohort's default is not the paper this cohort photographed.
- **⬚** Make-up sitting date, eligibility rules and any cap on the make-up mark are institutional
  and not recorded in this repository.

## 6. Invigilation and academic integrity

This repository has **no `instructor/anti-cheating.md`**, so the written-exam invigilation protocol
has to be assembled from what is recorded and marked ⬚ where it is not.

**Sourced and in force:**

- The paper is **individual work** ([SUBMISSION.md](../../SUBMISSION.md), *Rules for every
  submission*: "labs/quizzes/exams are individual").
- **Name + Student ID** are required on every submission; the paper carries Name, Student ID and
  Date fields to collect them.
- [ETHICS.md](../../ETHICS.md) applies, and every student signed its acknowledgment in Week 1. The
  paper restates that its scenarios target the labs already run, not real systems.
- **AI-tool disclosure** is a standing course rule (`SUBMISSION.md`).
- **Random live checks** ("You may be asked to reproduce a task or explain your fix live";
  "Answers you can't explain in your own words score zero") are a course-wide control, so a viva
  that samples a script's Section C or D reasoning is available where authorship is in doubt.

**Deliberately not imported.** `SUBMISSION.md`'s anti-cheating section is scoped to worksheets,
flags and the online weekly quizzes — per-student flags derived from the student ID,
identity-stamped screenshots showing `whoami`/timestamp, MOSS/JPlag similarity checking of pushed
code, and the shuffled/one-attempt/locked-account quiz settings. None of those is a written-paper
control, and the personalised-flag pipeline is in any case not yet live in this repository
(README.md status note; `SUBMISSION.md`'s own caveat). Do not cite them as if they invigilated
this paper.

**One conditional link.** If the **Google Form** route in `SUBMISSION.md`'s EXAMS table is chosen
over paper, the controls that section already describes for quizzes — individual, time-limited,
one attempt, locked to the school account, shuffled questions and options — do become available
for this paper. That is an argument for the Form route; §11 gives the argument against it. Decide
once, before Week 7's debrief.

**If copying is found:** keep the evidence and follow the course's own route — ETHICS.md plus
KOSEN's conduct process (`SUBMISSION.md`, closing line) and **⬚** (the institutional policy itself,
which the course specification §11 also leaves as ⬚).

**⬚** Invigilator roster, bag/phone handling, seating plan and whether a seating record is kept.
Keep one anyway: identical wrong answers on adjacent scripts is the written-exam form of a
similarity flag, and without a seating record the adjacency cannot be checked after collection.

## 7. Marking

- **Who marks: ⬚.** The course specification §1 names one instructor and records no TA, second
  marker or moderation arrangement. If more than one person marks, split by section — one marker
  takes Section C across every script — so that a judgement call is at least applied consistently.
- **The key:** `instructor/exams/week08-midterm-written-answers.md`. It is git-ignored; transfer it
  out of band before marking day and never "fix" the gap by committing it.
- **Method marks.** The paper requires byte/hex working for computational answers, which is exactly
  what lets Section C be marked in parts rather than right/wrong. **This repository records no
  course-wide partial-credit rule** — course specification §8 covers component weights and says
  worksheets are graded against the rubric published in each worksheet, and the grading scale is ⬚.
  So decide the classes of borderline answer once — whether a correct Section C method with an
  arithmetic slip keeps its method marks; whether a Section B answer that names the mechanism and
  the fix but omits the CWE loses the full item — write each ruling on your working copy of the
  key, apply it to every script, and carry it into §8 as a candidate item-bank note.
- **Score entry.** Midterm is **20 %** of the course and covers **both** this paper and the Week 9
  practical (course specification §4; `syllabus.md` §3). **⬚ — how the two combine into that 20 %
  is not recorded anywhere in this repository**; there is no gradebook file here, unlike the
  sibling course. Fix the rule before marking, not after seeing the marks.
- **⬚** Grading scale and letter-grade boundaries (institutional).

## 8. After the exam — item analysis and the item bank

The repository defines the *loop* but not the *statistics*. Everything below that is not sourced is
marked ⬚ rather than guessed.

1. **Mark, then look at the paper rather than the students.** For each item note where the cohort
   clustered: near-universal correct (the item discriminated nothing), near-universal wrong (the
   item was mis-set or mis-worded, or the teaching week did not land), and
   split-with-strong-students-wrong (the item is probably ambiguous).
2. **Separate a bad item from a real gap.** A cohort-wide failure on a Week 3 item is a teaching
   signal about Week 3, not a defective item — route it to §8.6, not to the bin.
3. **Replace, don't patch.** Rotate items from the MIDTERM POOL of
   `instructor/exams/item-bank.md`, whose stated purpose is exactly this — but mind §5: the pool
   cannot supply Section C's shape at all, and part of its Section B and D stock duplicates what
   this cohort has just sat. Replacing a burned item may mean writing one.
4. **Write the ruling back.** Every borderline-answer ruling made in §7 is evidence that an item is
   ambiguous. Add it to that item's marking note in the bank, or reword the item, before it is used
   again.
5. **Close the loop on the forms.** Record which form this cohort sat, so it is not the default next
   time.
6. **Where a first-half gap goes.** Week 17's review is scoped Weeks 10–16, so it does not revisit
   this material — but `labs/week17-review/README.md` states that the Week 18 written item bank
   should carry roughly **30–40 % Weeks 1–6 content**. A cohort-wide Weeks 1–6 weakness found here
   belongs in that 30–40 %, chosen deliberately rather than left to the next cohort.

> **Correct the bank's own premise while you are in there.** `instructor/exams/item-bank.md`
> justifies rotation by saying the *public* `weekNN-*.md` exam files are static and leak between
> cohorts. In this repository they are not public — `instructor/` is git-ignored and Form A's note
> says it stays there until the day it deploys. The leak vector here is the **sitting itself**:
> the paper is sat, photographed and shared afterwards. The mitigation is unchanged — rotate every
> cohort — but the wording is inherited from the sibling course and is wrong here.

**⬚ Not defined anywhere in this repository, and deliberately not invented here:** which item
statistic is used (facility index, discrimination index, point-biserial, or none), the threshold at
which an item counts as discriminating poorly, who reviews the analysis, when it is done, and where
it is recorded. Fix these once and record them in `instructor/exams/item-bank.md`, not in this
public file.

## 9. Assessment for this week

| Instrument | Evidence | Outcome | Weight |
|---|---|---|---|
| Midterm written paper, Sections A–D | The script, 100 pts | K1–K3, P1–P3, A1–A2 | Part of the 20 % midterm component, shared with the Week 9 practical (combination rule ⬚ — §7) |
| Sitting record: form sat, seating, incidents | Conditions under which the script was produced | A3 | Integrity control, not a mark |
| Item analysis (§8) | Per-item performance across the cohort | Course-level, not student-level | Feeds `instructor/exams/item-bank.md` and the Week 18 paper's first-half share |

**No worksheet, no weekly quiz and no flag this week** — nothing is submitted to Classroom or
GitHub, and no Docker target is stood up.

## 10. Materials

- Paper, **Form A** — instructor-held, git-ignored, **never published**:
  `instructor/exams/week08-midterm-written.md`
- Key — instructor-held, git-ignored, **never published**:
  `instructor/exams/week08-midterm-written-answers.md`
- Rotation source — instructor-held: `instructor/exams/item-bank.md` (MIDTERM POOL)
- **Form B** — ⬚, does not exist for Week 8 (§5)
- Proctor deck — ⬚, does not exist for Week 8 (§4, §11)
- What students revised from: `labs/week07-review/README.md` (Crypto Jeopardy, mock midterm
  dry-run, cheat-sheet deliverable), `quizzes/weekly/week07-review-quiz.md`, and the Week 1–6 lab
  folders `labs/week01-intro` … `labs/week06-aead`
- Course frame: [course specification](../course-specification.md) §4, §6, §9 ·
  [AGENDA.md](../../AGENDA.md) · [syllabus.md](../../syllabus.md) §3 ·
  [SUBMISSION.md](../../SUBMISSION.md) · [ETHICS.md](../../ETHICS.md)
- **⬚** Printed papers, script booklets, room booking, invigilator roster

## 11. Risks and contingencies

| Risk | Mitigation |
|---|---|
| **No Form B exists for Week 8** (§5), so a make-up sitting or a second section has no paper to run, and the course specification §9 currently over-claims parity | Build Form B before the sitting — and budget for *writing*, not selecting: the MIDTERM POOL cannot supply Section C's shape at all, and several of its Section B and D entries restate items Form A already uses |
| `instructor/` is git-ignored, so a colleague marking from a clone of the public repository has **neither the paper nor the key** | Transfer both out of band before marking day; never resolve this by committing them — the repository is public |
| **Delivery route undecided.** `SUBMISSION.md` offers "on paper / Google Form". Section C requires byte/hex working, which a Form short-answer box records badly and which makes method marks (§7) hard to award | Decide before the Week 7 debrief. If the Form route is used, either add a photo/upload field for the working or run Section C on paper and the rest on the Form |
| **Printing a Markdown paper.** Sections B and C are fenced code blocks, and Section C's scenario carries non-ASCII typographic characters inside monospace text. A substituting font, or a page break inside a snippet, silently changes what the item shows | Export to PDF once, read the printed proof line by line, confirm every snippet is intact, unwrapped and unbroken, and only then duplicate |
| **Calculator policy is ⬚** while Section C asks for hex computed by hand — students will ask, and an inconsistent answer between invigilators is an appeal waiting to happen | Decide it with the open-note rule, announce both at the Week 7 debrief, and repeat both before the clock |
| **No proctor deck** (`slides/week08.md` does not exist) — the pre-clock briefing has no artefact and depends on the invigilator remembering it | Brief from §4 of this plan, or write the deck before the day; either way hand the invigilator a written running order |
| Students revised Section A as MCQ, because `labs/week07-review/README.md`'s mock describes it as "MCQ/short answer" while the paper's Section A is six short-answer items (§2) | Correct it verbally at the Week 7 debrief and again before the clock |
| The **open-note decision** is taken after Week 7 — but the cheat sheet is a Week 7 deliverable, so a late rule either wastes that work or rewards the students who guessed right | Announce it in the Week 7 *exam logistics* debrief slot, before students write the sheet |
| **No lab block this week**, so nothing is checked on a machine — Week 9 is a 150-min CTF practical against Docker targets, and a broken Docker install would first surface at its start | Use the collection slot to tell students to re-check their Week 2–6 targets, and post the Week 9 target check before they leave the room |
| **Multiple sections or sittings of the same cohort** — the later sitting must not sit the paper the earlier one has already seen, which with no Form B is currently impossible | Sequence sittings so no gap exists between them, or build Form B first (§5); record which form each section sat |
| Identical wrong answers across adjacent scripts, with **no seating record required** by anything in this repository | Keep a seating record on the day regardless; without it the adjacency claim cannot be checked once the scripts are collected |
| A student misses the sitting | §5 — and note that this currently means re-running Form A, with the leak that implies. Eligibility and date are **⬚** |

## 12. Post-teaching reflection

*Complete after the session — this also feeds the course's engagement data.*

- Attendance / completion: ⬚
- Form sat (A / B), by which section, and whether a make-up is now owed: ⬚
- Delivery route used (paper / Google Form), and whether Section C's working came through legibly: ⬚
- Open-note and calculator rules as actually announced: ⬚
- Time actually used by the cohort (did anyone need the full 120 min?): ⬚
- Section-by-section mark distribution, and which section was weakest: ⬚
- Items that discriminated poorly, and what replaced them in the bank: ⬚
- Borderline-answer rulings made during marking, and the item wording they imply: ⬚
- Weeks 1–6 gaps to carry into the Week 18 paper's first-half share (§8.6): ⬚
- Integrity incidents, and how they were handled: ⬚
- Anything to change before this exam runs again: ⬚
