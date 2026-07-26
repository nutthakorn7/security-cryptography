# Lesson Plan — Week 1: Security Mindset & Threat-Modelling a Cryptographic System

| | |
|---|---|
| **Course** | Security & Cryptography · course code `21025117` (per [syllabus.md](../../syllabus.md); [course-specification.md](../course-specification.md) §1 leaves the field ⬚ — *"Confirm against the registrar before print if in doubt."*) |
| **Week / date** | 1 · ⬚ |
| **Contact time** | 300 min = 120 lecture + 180 studio (AGENDA per-week table; the ~10-min weekly quiz sits *inside* the 120-min lecture block, not on top of it) |
| **Kind** | **CONCEPTUAL** — no Docker target, no flag, rubric-graded ([course-specification.md](../course-specification.md) §6) |
| **Lab folder** | `labs/week01-intro` (README.md + worksheet.md only — no code, no `docker-compose.yml`) |
| **Slides** | `slides/week01.md` (17 slides, Marp) |
| **Standards** | NIST FIPS 140-3 · OWASP Cryptographic Storage Cheat Sheet · CWE-320 (Key Management Errors) · CWE-330 (Use of Insufficiently Random Values) · OWASP Threat Modeling Cheat Sheet |
| **CLOs addressed** | **CLO1** select & justify the primitive · **CLO5** evaluate & communicate (schedule row, [course-specification.md](../course-specification.md) §6) |
| **Signature game** | 🐍 "Snake Oil Bingo" |

---

## 1. Session objectives

Taken from `labs/week01-intro/README.md` "Objectives" and the worksheet's own tasks. By the end of
this week a student can:

**Knowledge (K)**
- K1 — Explain the CIA triad *specifically as it applies to cryptography*, and why "we encrypted
  it" is a confidentiality claim only, not an integrity or availability guarantee.
- K2 — State precisely what "cryptographically secure" promises (a primitive resists a
  well-defined class of mathematical attack, under stated assumptions, at a stated security level)
  and what it explicitly does **not** promise (that the *system* using it is secure).
- K3 — Distinguish a textbook-secure primitive from a real-system failure: the proof holds, the
  deployment breaks it anyway — implementation bugs, side channels, bad randomness, protocol/mode
  misuse, or human/key-management failure.
- K4 — Define a *trust boundary* and name, for a system handling key material, where key-management
  failures concentrate.

**Analysis skills (P)** — this week's "skills" are analytical, not exploitative; there is no target.
- P1 — Apply a lightweight threat-modelling process (assets, adversaries, attack surface) to a
  system that handles cryptographic keys.
- P2 — Audit a confident, professionally-worded AI answer in which **every individual factual claim
  is true**, and name the systematic category (or categories) it omits — not merely that it is
  incomplete.
- P3 — Supply a concrete real or realistic counter-example for each omitted category: a system that
  used current, correctly-sized, unbroken primitives and still failed.
- P4 — Rewrite a flawed summary so that it is correct *and complete*, without making it longer.
- P5 — Write and then critique a single AI prompt against a five-point checklist (key management,
  randomness/entropy, protocol/composition misuse, side channels, hand-waving), quoting the line
  being judged.
- P6 — Explain to a non-technical audience, with no jargon, why algorithm strength alone does not
  answer "are we safe?".

**Attitude (A)**
- A1 — Work only within [ETHICS.md](../../ETHICS.md); every student signs the acknowledgment of
  that policy this week.
- A2 — Disclose AI assistance (tool + what was asked) in Part 1, and submit work they can defend
  live with no notes (Part 5).
- A3 — Distrust confident AI output and verify it against the primary literature — the pattern the
  README says "recurs in every AIR-Sec week after this one".

## 2. Key ideas (the through-line)

A primitive being "secure" is a claim about a mathematical object under stated assumptions. It says
nothing about whether the program calling it is secure. Every remaining teaching week takes one
sound primitive and shows a specific way real systems break it anyway — the README's 11-row table
(Weeks 2–6, 10–15) is the map, and in every row the primitive itself is intact. What breaks is a
decision made *around* it: a missing check, a reused value, a skipped verification, an assumption
the real system quietly violates.

The corollary matters more than the slogan: real cryptographic failure clusters at trust
boundaries, where control over or visibility into key material changes hands. So the transferable
question, asked at every primitive from Week 2 onwards, is *"what assumption is this primitive
relying on, and does this system actually uphold it?"*

Because no primitive has been introduced yet, there is nothing to exploit. This week's exploit is a
**reasoning exploit**: the Audit-the-AI Exhibit is not wrong about anything it says, and finding
the load-bearing gap is the exercise.

## 3. Prior knowledge and preparation

**Students, before class**
- Per the lab README: *"no environment setup needed. This week is discussion- and writing-based;
  no Docker, no code."* Skim the course README and `course-plan-19weeks.md`.
- Starred pre-reading for W1 ([readings.md](../../readings.md)): Moxie Marlinspike, *The
  Cryptographic Doom Principle* — https://moxie.org/2011/12/13/the-cryptographic-doom-principle.html
- **Conflict to resolve before you send this instruction out** — AGENDA's Week 1 exception and
  [SUBMISSION.md](../../SUBMISSION.md) §"One-time setup (Week 1)" both put Docker on students this
  week ("`git clone` your fork; stand up the environment (Docker) per Week 1"). See §5 and
  *Escalations* below; decide which instruction the class receives, and do not let students arrive
  with neither a fork nor Docker Desktop because they read the README's line literally.

**Instructor, before class**
- **Produce the Snake Oil Bingo cards.** The README says *"Everyone gets a bingo card of common
  crypto myths"*; no card artefact exists anywhere in the repository. The only myth strings the
  repo states are "military-grade encryption," "unbreakable 256-bit security," and "quantum-proof
  because the key is long enough" — everything else on the card is your authorship. Cards: ⬚.
- **Decide the 0:00–0:10 quiz slot.** `quizzes/weekly/` contains only `week07-review-quiz.md` and
  `week17-review-quiz.md`; there is no Week 1 instrument, and the deck's own note says *"No recap
  today — this is Week 1."* Week 1 quiz item: ⬚.
- **Decide the studio timing question in §5** and write the decision into §9 afterwards.
- **Decide the per-student variant question in §6** *before* marking begins, not during.
- Have `instructor/week01-intro-answer-key.md` open for the Part 3 rubric bands and the viva
  expected-answer notes (instructor-only; git-ignored; never shown to students or pasted into
  slides).
- Bring the ETHICS acknowledgment forms — ETHICS.md: *"Every student signs an acknowledgment of
  this policy in Week 1."*

**Prerequisite concept:** none specific to cryptography. Syllabus prerequisites are programming
(Python/C), data structures, basic discrete maths/number theory.

## 4. Lecture — 120 min

Row boundaries are the AGENDA CONCEPTUAL-week lecture template; the content column maps
`slides/week01.md` onto it in deck order.

| Time | Block | Content (slides) | Method |
|---|---|---|---|
| 0:00–0:10 | Weekly quiz + recap | Quiz instrument: ⬚ (none exists for Week 1). No recap — Week 1 frames the 19-week course instead. Opening hook: *"if I told you a system uses AES-256 and RSA-4096 — the biggest algorithms available — is it safe?"* (~2 min), then "Today" roadmap (~2 min) | Hook question, hold the answer |
| 0:10–0:55 | Core concepts | "The course's spine" (~5) · "Preview: the pattern, week by week" (~6) · "What *cryptographically secure* actually promises" (~5) · "CIA, specifically for cryptography" (~6) · "We encrypted it is a confidentiality claim only" (~5) · "Trust boundaries around key material" (~6) | Lecture + board work (write the boxed spine line and "encryption ≠ integrity"; draw browser → app server → DB and mark the boundaries) |
| 0:55–1:05 | Break | | |
| 1:05–1:35 | Worked analysis (whiteboard, not Docker) | Debian OpenSSL predictable-RNG, CVE-2008-0166 (~5) · fail0verflow PS3 ECDSA nonce reuse (~5) · "This week's break: an AI that's never technically wrong" (~4) · "The Exhibit's shape (don't solve it yet)" (~6) · "Threat model before you code" — assets, adversaries, attack surface, then the assumption question (~7) | Case walk-through + a mini threat model on the board |
| 1:35–1:55 | Design trade-offs / where real systems get this wrong | 🐍 **Snake Oil Bingo** (~8). The deck places the trigger at the Exhibit read-aloud — read the Exhibit verbatim from the README/worksheet (or have a student read it), then run the game | Table game; instructor circulates to verify squares |
| 1:55–2:00 | Brief the studio | "Lab today — Worksheet 1" (Parts 1–5, no Docker, no flag) + "Takeaway" (~3) | Instruction |

**Capacity note.** The deck's own speaker-note budgets total ≈75 min across the slides that carry
one — that figure already includes the 0:00–0:10 block's hook (~2) and roadmap (~2). Adding the
10-min break (no speaker note) and the ≈6 min of the quiz slot not already inside the 75 (10 − 4)
accounts for ≈91 of the 120 min. The remaining ≈29 min is discussion and board work — expect the
CIA and trust-boundary slides to absorb most of it, since they are where Worksheet Q3–Q5 are
earned.

**Checks for understanding during lecture**
- After "What *cryptographically secure* actually promises": cold-call Part 5 Q1's actual wording —
  *"If a system uses AES-256 and RSA-4096 (both far beyond any known practical attack) and is
  still compromised, what does that tell you about where security actually lives in a
  cryptographic system?"* (this slide's own speaker note says students need to be able to state
  this definition "on the viva (Part 5, Q1)" — the Takeaway slide separately carries its own,
  differently-worded cold-call note on the same idea)
- On the CIA slide: *"if I encrypt a message with no MAC, can an attacker change it without me
  noticing?"* (Yes — and that is the Week 4 exploit.)
- During Bingo: a square is only claimed once the table gives the one-line **technical** reason.
  Model the first one yourself; do not accept "that sounds fake".
- **Do not reveal the Exhibit's missing categories.** Naming them is the graded worksheet task.

## 5. Studio / analysis — 180 min

No `docker compose up`, no target, no flag. Row boundaries are the AGENDA CONCEPTUAL-week lab
template; the "Student does" column is built from Worksheet 1's own parts.

| Time | Block | Student does (worksheet task) | Evidence produced |
|---|---|---|---|
| 0:00–0:15 | **Onboarding** — this week's design/audit brief (no `docker compose up`) | Part 1: name, student ID, date, group; disclose any AI assistance used anywhere in the worksheet (tool + what was asked). Sign the ETHICS acknowledgment | Completed Part 1 header; signed acknowledgment |
| — | **Week 1 exception — term-wide environment setup** | AGENDA: *"Budget ~30–40 min of the 180-min block for this before the threat-modeling task."* Content per SUBMISSION.md §"One-time setup (Week 1)": create a GitHub account and **fork** this course's repo (`security-cryptography`); `git clone` your fork; stand up the environment (Docker); join this course's Google Classroom. AGENDA adds "first `docker compose up` on a throwaway container" | A working Docker Desktop, a cloned fork, Classroom joined |
| 0:15–1:45 | **Design/analysis tasks** | AGENDA names the Week 1 task as *"threat-model a small crypto system end-to-end"*. The worksheet's corresponding written work is Part 2, Q1–Q6 (4–8 sentences each) — of which **Q3 is the only threat-boundary item**: define *trust boundary*, then name three concrete crossings in a typical web application's architecture and one thing that commonly goes wrong at each. Q2 requires a cited real incident; Q6 asks for two falsifiable hypotheses about weeks not yet studied | Written answers Q1–Q6, with a source citation on Q2 |
| 1:45–2:25 | **Structured peer critique of another team's design/analysis** | ⬚ — Worksheet 1 contains **no peer-critique task**, and the only repo-stated group activity for this week (Snake Oil Bingo) is placed in the lecture block by the slides. Either run a critique of Part 2 answers you define yourself (ungraded, since the rubric has no line for it) or fold this time into Part 2/Part 3 | ⬚ (nothing the rubric scores) |
| 2:25–2:45 | **AI-resilient tasks** (start in class, finish as homework) | Part 3 *Audit the AI*, items 1–4: what the Exhibit gets **right** and why a shallow reviewer would accept it; the **gap** — name the missing categories, *"not just 'it's incomplete'"*; one concrete example per missing category (Q2 may be reused for one, so at least two further distinct examples); rewrite the "In summary" paragraph only, in 3–5 sentences. Part 4A EiPE (3–5 sentences, no jargon — explicitly no "nonce", "side channel", "AEAD"). Part 4B Prompt Problem: write one prompt, run it, critique the result against the five checklist bullets | Part 3 answers 1–4 inline; Part 4A answer; Part 4B — the exact prompt, the AI's full response, and a bullet-by-bullet critique marking each item correct / incorrect / hand-waved with the specific line quoted |
| 2:45–2:55 | **Rotating micro-demo** | 2–3 students walk through their critique | Live walk-through |
| 2:55–3:00 | **Submit** | Worksheet PDF → this course's Google Classroom. No fix to push — no code this week | `Wk<NN>_<StudentID>.pdf` (Week 1 instance of SUBMISSION.md's stated pattern) |

**Part 5 (viva spot-check) is instructor-run and live**, and the AGENDA places viva spot-checks
alongside the micro-demo rather than in a slot of their own; it is worth 10 of the worksheet's 100
points. Three questions are published in the worksheet — students answer them with no notes.

**Timing — an unreconciled arithmetic, decide it before the session.** The AGENDA's CONCEPTUAL lab
template already fills 0:00–3:00 with no slack, and the Week 1 exception then adds ~30–40 min of
environment setup *inside* the same 180 min. The AGENDA does not say which blocks absorb it, and
this plan does not invent an answer: the shifted boundaries are ⬚. Choose in advance — the 1:45–2:25
peer-critique block is the only one with no rubric line attached to it, which makes it the least
costly candidate — and record what you actually did in §9. **Do not resolve this by editing the
worksheet, the AGENDA or the lab README**; those are graded/parity-gated material (see
*Escalations*).

**Formative checkpoints**
- By ~1:15, a student whose Q3 lists *technologies* rather than *crossings* has missed the
  definition — push them back to "where does control over, or visibility into, key material change
  hands?"
- The single most common Part 3 failure is a critique that says the Exhibit is "incomplete" without
  naming categories. The worksheet forbids exactly this; check it at ~2:35 while the block is still
  live, because the specificity is what carries the 35 points.
- A student arguing that the Exhibit is *wrong* has misread the task. Every claim in it is true;
  the finding is what it omits.
- Q6 is graded on making a specific, falsifiable guess, not on being right — tell a stuck student
  that explicitly rather than letting them research ahead.

## 6. Assessment for this week

| Instrument | Evidence | Outcome | Weight |
|---|---|---|---|
| Worksheet 1, Parts 1–5 | Written analysis, the Audit-the-AI critique, the prompt artefacts, live viva | K1–K4, P1–P6, A2 | Part of the 30% worksheet component ([course-specification.md](../course-specification.md) §4) |
| Weekly quiz (start of lecture) | Quiz score | ⬚ — no Week 1 instrument exists | Part of the 10% quiz/participation component |
| Micro-demo + viva spot-check | Live walk-through and defence with no notes | P2–P5, A2 | Scored inside the worksheet rubric (10 pts), not separately |
| Per-student planted-error variant | See the note below | A2 | ⬚ — not defined for Week 1 |

**How the analysis is graded.** Worksheet 1 publishes its own 100-point split, and it is weighted
towards the AI audit rather than the essay arm:

| Criterion | Points |
|---|---|
| Conventional arm — 6 short-answer questions (Part 2) | 30 |
| Audit-the-AI — what's right + the gap + examples + rewritten summary (Part 3) | 35 |
| EiPE (Part 4A) | 10 |
| Prompt Problem (Part 4B) | 15 |
| Viva spot-check (Part 5, instructor-run) | 10 |

The worksheet states the marking stance for each arm: Part 2 is graded *"on the accuracy and
completeness of your reasoning, not on matching a specific sentence"*; Part 3 on the **critique**,
*"not on agreeing or disagreeing wholesale with the AI"*; Q6 on making a specific, falsifiable
guess. Detailed full/partial/no-credit bands for Part 3, and the expected-answer notes for the
viva, live in `instructor/week01-intro-answer-key.md` — instructor-only, git-ignored, and not to be
reproduced in this plan, the slides, or anything a student sees. Practical consequence for marking
consistency: Part 3 item 3 has a countable floor (an example for *each* named category, of which at
least two must be distinct from the Q2 incident), and Part 4B has a countable floor (five checklist
bullets, each marked and each with a quoted line) — mark those before the prose.

**How the per-student variant is assigned.** ⬚ — **no mechanism is defined for Week 1 anywhere in
this repository, and this plan will not invent one.** The tension is worth stating plainly, because
it is real:

- [course-specification.md](../course-specification.md) §7 says CONCEPTUAL weeks *"use per-student
  planted-error variants instead"* of flags, and `course-plan-19weeks.md` says a CONCEPTUAL week's
  personalised artefact is *"typically a seeded flaw instance or a per-student prompt seed"*.
- Week 1's material does the opposite: one Exhibit, identical for the whole class. The worksheet
  states *"**No personalized flag this week** — this is a Conceptual week, graded entirely on your
  written reasoning and viva performance"*, and SUBMISSION.md's by-week table puts Wk1 under
  submission mechanism **"No lab/flag"**.
- `instructor/research/planted-error-bank.md` is the study's separate H2 instrument with its own
  A/B form assignment; it is not a Week 1 worksheet variant and should not be repurposed as one
  without amending the research protocol.

What Week 1 *does* produce per student, and what therefore carries the attribution load until a
variant scheme is decided: the Part 4B prompt is student-authored and its AI response is unique to
that run (require the tool name, the exact prompt and the date); Q2's incident and Q6's two chosen
weeks are student-selected; Part 1 carries the identity stamp and the AI-assistance disclosure; and
Part 5 is a live, no-notes defence. If a per-student seed is to be introduced (e.g. a prompt seed
per student), decide and document it before the session — retrofitting it after submissions are in
makes the marks incomparable across the cohort, which matters here because both course arms feed
one preregistered study.

## 7. Materials

- Lab: `labs/week01-intro/` — `README.md`, `worksheet.md`. **That is the whole folder** — no code,
  no `docker-compose.yml`, no flag (by design).
- Slides: `slides/week01.md`
- Snake Oil Bingo cards: ⬚ (not in the repository — see §3)
- Week 1 quiz: ⬚ (not in the repository — `quizzes/weekly/` holds the two review quizzes only)
- Reading ([readings.md](../../readings.md), W1): ⭐ Moxie Marlinspike, *The Cryptographic Doom
  Principle* · "Crypto Fails" writeups · NIST Cryptographic Standards and Guidelines overview ·
  CISA Secure by Design
- References cited by the lab README: NIST FIPS 140-3 · CWE-320, CWE-330 (https://cwe.mitre.org/) ·
  OWASP Cryptographic Storage and Threat Modeling cheat sheets · fail0verflow, *Console Hacking
  2010: PS3 Epic Fail* (27C3) · Debian OpenSSL predictable-RNG advisory (CVE-2008-0166)
- Answer key: `instructor/week01-intro-answer-key.md` (instructor-only, git-ignored)
- Submission channels: [SUBMISSION.md](../../SUBMISSION.md) · Rules of engagement:
  [ETHICS.md](../../ETHICS.md)

## 8. Risks and contingencies

| Risk | Mitigation |
|---|---|
| The Part 3 critique collapses into "the answer is incomplete" with no named categories — the single failure mode this week's 35-point task is designed around | The worksheet already forbids it in writing; check it live at ~2:35 rather than at marking. Do **not** pre-announce the four categories in the lecture — the deck's own note says to let the worksheet do that work |
| Students argue the Exhibit is factually wrong and spend the block fact-checking true claims | Frame it on the "an AI that's never technically wrong" slide before they read it, and re-frame at the start of the studio: every individual claim is true; the finding is the omission |
| Bingo squares claimed without the one-line technical reason — the game degrades into pattern-matching on scary phrases | Model the first square yourself ("military-grade encryption" is not a defined technical term); circulate and require the reason from the table before the square counts |
| The Part 4B prompt returns an answer that already covers all five checklist bullets, leaving nothing to critique | That is a gradable outcome, not a failed task — the fifth bullet asks whether it hand-waves or over-generalises, and every mark must quote the specific line. Require tool + exact prompt + date, since the same prompt will not reproduce the same response later |
| Part 3 is 35 % of the worksheet but the template gives the whole AI-resilient block ~20 min in class | It is explicitly "start in class, finish as homework" — say so out loud at 2:25, or students will submit the in-class draft as final |
| Environment setup collides with the analysis blocks (see §5), or students arrive with no fork and no Docker because the README told them none was needed | Resolve the instruction before the week runs; if setup must happen in-session, take the time from the block with no rubric line rather than from Part 3 |
| Q2 answers cite an "incident" that never happened, or an AI-supplied summary of one | Q2 requires a citation. Two verified incidents are already in the lab README and on the slides (CVE-2008-0166; the fail0verflow PS3 ECDSA talk) — accept those or an independently verifiable source |
| No Week 1 quiz instrument exists, so the 10 % quiz component silently starts a week late | Decide before class: run a diagnostic, run nothing, or start the count in Week 2 — and record the choice, since "drop lowest 1–2" changes meaning if the denominator changes |
| A student finishes Parts 2–4 early | Extension that stays inside the material: apply the Q3 trust-boundary analysis to their own term-project idea (README point 5 asks them to start naming "what data crosses what boundary, encrypted with what" for the Week 4 design doc) |

## 9. Post-teaching reflection

*Complete after the session — this also feeds the course's engagement data.*

- Attendance / completion: ⬚
- Where the environment setup was actually taken from (which block absorbed the ~30–40 min): ⬚
- Time actually taken per block (vs. plan): ⬚
- Did the class name the Exhibit's missing categories unprompted, and how many named all of them: ⬚
- Quality of the Part 4B critiques — did students quote lines, or summarise impressions: ⬚
- Misconception that showed up in the EiPE answers: ⬚
- Whether Snake Oil Bingo produced technical reasons or just recognition: ⬚
- Decision recorded on the per-student variant question (§6): ⬚
- Anything to change before this week runs again: ⬚

---

### Escalations — defects in lab/course content, recorded here rather than fixed

These are content issues found while writing this plan. They are **not** corrected in `labs/`,
AGENDA.md or the course specification, because that material is graded, parity-gated against the
curriculum monorepo, and mirrored by an instructor answer key.

1. `labs/week01-intro/README.md` line 15 says the slides are *"(not yet written — see
   `course-plan-19weeks.md`)"*, but `slides/week01.md` exists and is a complete 17-slide deck with
   speaker notes. Stale note.
2. `labs/week01-intro/README.md` tells students *"no environment setup needed … no Docker, no
   code"*, while AGENDA.md's Week 1 exception budgets ~30–40 min of Docker/repo setup inside the
   same lab block and SUBMISSION.md §"One-time setup (Week 1)" instructs students to fork, clone
   and "stand up the environment (Docker) per Week 1". Students following the README arrive
   unprepared for the setup the other two documents assume.
3. AGENDA.md's CONCEPTUAL lab template and its own Week 1 exception cannot both hold: the template
   allocates the full 180 min, the exception adds 30–40 min inside it, and no shifted boundary is
   given.
4. AGENDA.md states the Evidence & Integrity artefact for CONCEPTUAL weeks is *"a design
   artifact"*, and names the Week 1 studio task as "threat-model a small crypto system end-to-end";
   Worksheet 1's Evidence & Integrity section requires an identity stamp plus a 1–2 sentence
   restatement, and its only threat-modelling item is Part 2 Q3. No design artefact is collected,
   and the rubric has no line for one.
5. AGENDA.md's CONCEPTUAL template includes a 40-minute "structured peer critique of another team's
   design/analysis"; Worksheet 1 has no peer-critique task and the rubric has no line for it.
6. `labs/week01-intro/README.md` promises *"Everyone gets a bingo card of common crypto myths"*;
   no bingo-card artefact exists in the repository (not in `labs/`, `slides/` or `instructor/`).
   The game cannot run as written without the instructor authoring the card first.
7. course-specification.md §7 promises per-student planted-error variants for CONCEPTUAL weeks;
   Worksheet 1 and SUBMISSION.md both state Week 1 has no personalised artefact, and no assignment
   mechanism is defined. See §6.
8. No Week 1 weekly-quiz instrument exists (`quizzes/weekly/` holds only the Week 7 and Week 17
   review quizzes) although the specification, AGENDA and the lecture template all place a ~10-min
   quiz at the start of every teaching week.
9. Minor CLO inconsistency: the schedule row (§6) maps Week 1 to CLOs 1 and 5, while the
   worksheet-part table (§4) maps "Conceptual analysis (CONCEPTUAL weeks …)" to CLO1 and **CLO4**.
   This plan follows the schedule row.
