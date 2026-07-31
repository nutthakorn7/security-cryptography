# How to Do & Submit Work

**Platforms:** the **course platform** (material, quizzes, hand-in) + **GitHub** (your code fixes).

| What | Where |
|---|---|
| Course material — worksheets, lab guides | **`learn.zcr.ai/learn/cryptography`** — no sign-in needed |
| Weekly quiz | **`learn.zcr.ai/quiz`** — the one-time code on your slip |
| Worksheet PDFs, project report | **`learn.zcr.ai/submit`** — the submission code on your slip |
| Code fixes (Wk12) | **GitHub** — your own fork of this course's repo |

> **No Google.** Material, quizzes and worksheet hand-in all run on the course
> platform. There is no Google Classroom and no Google Form for this course.

This course has its **own** GitHub repo, separate from the companion
`software-security` course's, even though the two share the same 19-week skeleton and pedagogy.
Fork *this* course's repo; work submitted against the wrong course cannot be graded here. The
platform files every quiz and every hand-in under the course it belongs to, so the code on your
slip is what puts your work in *this* class.

All offensive work is on the provided sandbox targets only — see this course's own ethics &
authorized-use policy, [`ETHICS.md`](ETHICS.md).

---

## One-time setup (Week 1)
**Every lab starts with `cd labs/weekNN-…`, so you need the repository on your own
machine before Week 1. Nothing on the website will work without this step.**

1. Create a GitHub account, then **fork** this course's repo:
   <https://github.com/nutthakorn7/security-cryptography>
2. Clone your fork and check it out:
   ```bash
   git clone https://github.com/<your-github-username>/security-cryptography.git
   cd security-cryptography
   ```
   Then stand up the environment (Docker) per Week 1.
3. Read the material at **`learn.zcr.ai/learn/cryptography/`** — no sign-in needed.
4. Keep the **slip you are given in class**. It carries your quiz code and your submission code;
   those two codes are the only credential you need, and they are what files your work under
   *this* course. There is no account to create and no password to remember.

---

## Weekly LAB — how to do & submit

**Read this before assuming "edit the code, commit a fix" — most weeks in this course don't work
that way.** Unlike `software-security` (which ships a `solution_skeleton.py` per week for you to
complete), this course's `fixed_app.py`/reference-fixed mode is **already fully built** for every
week except one. Most weeks you *confirm* the fix works and *explain why* — you don't write it.

**Do it (most weeks):**
1. Stand up the week's target: `docker compose up` (or the command in that lab's README).
2. Work through the **worksheet** (`labs/week<NN>…/worksheet.md`): for each task record the
   **payload/command**, a **screenshot** of the result, and the requested explanation. The
   "Audit the AI" section does require you to **rewrite a flawed snippet** — but that rewrite goes
   *in the worksheet itself*, not as a code commit.

**Do it (Week 12 only — the one week with a real code-writing task):** in addition to the above,
`alice_student.py` ships with its one fix function stubbed as `raise NotImplementedError`. Write
the real implementation yourself (see that lab's worksheet Part 2a step 5 and the file's own
docstring), verify it against `docker-compose.student-task.yml`, then:
1. In your fork, create a branch `wk12`.
2. Commit your completed `alice_student.py` to that branch and note the **commit hash** in the
   worksheet, alongside your explanation of what each line does.

**Submit:**
| Part | Where | What | Weeks |
|------|-------|------|------|
| Worksheet | **`learn.zcr.ai/submit`** | the completed worksheet exported to **PDF** (screenshots embedded). You can replace it any time before the deadline. | all |
| Code fix | **GitHub** | push branch `wk12`, open a PR (or paste the commit link in the worksheet) | Wk12 only |

**File name:** `Wk<NN>_<StudentID>.pdf`  (e.g. `Wk04_65123456.pdf`)
**Deadline:** before the next class session (unless told otherwise).
**Grading:** the 100-pt rubric in each worksheet.

### Flags and evidence, by week type

`course-plan-19weeks.md` classifies each week as LAB / HYBRID / CONCEPTUAL, but that classification
is about how much of the week is a runnable exploit vs. theory — it does **not** by itself tell you
what to submit. **Wk11 (Sig/ZKP) is classified HYBRID but its runnable half uses the same
flag-gated mechanism as a LAB week**, not the log-line mechanism the other HYBRID weeks use — so
what you actually capture is determined by the **submission mechanism** column below, not the
course-plan `Kind` column:

| Weeks | Course-plan `Kind` | Submission mechanism | What you capture |
|---|---|---|---|
| Wk2 Hash, Wk3 MACs, Wk4 AES-modes, Wk6 AEAD, Wk11 Sig/ZKP, Wk15 PQC | LAB (all but Wk11); Wk11 is HYBRID | **Flag-gated** | a **personalized flag**, printed by the vulnerable target once you complete the attack — `FLAG_HASH`, `FLAG_MACS`, `FLAG_AES`, `FLAG_AEAD`, `FLAG_SIG`, `FLAG_PQC` respectively |
| Wk5 Key-Exchanges, Wk12 Secure-Transport, Wk13 E2E-Encryption, Wk14 Authentication | HYBRID | **Evidence-log-gated** | the required **evidence-log line(s)** from Part 2a of the worksheet (e.g. captured server-side log output showing the vulnerable vs. fixed behavior) — these weeks don't gate on a single flag string, they gate on you producing and explaining the specific log artifact the worksheet names |
| Wk1 Intro, Wk10 Hybrid-Encryption | CONCEPTUAL | **No lab/flag** | no Docker target, no flag — Audit-the-AI / discussion deliverable per that week's worksheet |

**Status note (be aware before you rely on this):** the personalized, per-student attribution of
flags (deriving each `FLAG_*` value from your student ID) is **built but not yet live**. This
course's own `instructor/seed_flags.py` exists and is verified end-to-end (generates a per-student
`FLAG_HASH`/`FLAG_MACS`/`FLAG_AES`/`FLAG_AEAD`/`FLAG_SIG`/`FLAG_PQC` for the 6 flag-gated weeks, and
can reverse-look-up who a submitted flag was issued to) — but there is **no running CTFd instance
yet** for this course (the deployment `.env` wiring and drift guard are ready; the actual server,
image catalog, and challenge host are not stood up). Until a cohort's CTFd goes live, flags are
still the same placeholder value for everyone, *not* personalized or checked against a roster.
Submit your worksheet evidence (command + screenshot + flag/log line) as instructed regardless —
the anti-cheating controls in the section below (screenshot identity-stamping, code-similarity
checks, viva spot-checks) apply and are
enforced manually until the personalized-flag pipeline is live; you'll be told in class once
`FLAG_*` values are personalized and this note will be removed.

**Where the flag goes:** into your worksheet PDF, alongside the command and the screenshot, and
that PDF goes to `learn.zcr.ai/submit`. This course has no scoreboard of its own to paste a flag
into — that is what the status note above is about.

---

## QUIZ — how it works
- **On the course platform:** go to **`learn.zcr.ai/quiz`** and enter the **one-time code** on
  your slip. The code is yours alone and works once.
- **Weekly quiz:** a short **~10-min quiz at the start of every teaching week** (6 Q: 5 MCQ + 1 short, **individual**). Low-stakes — the **lowest 1–2 are dropped**.
- **Cumulative review quizzes:** two bigger 25-pt quizzes in the **review weeks** (W7 pre-midterm, W17 pre-final).
- No separate file to submit — the quiz **is** the submission. Questions come one at a time and
  the quiz only moves forward, so answer each one before you continue.

---

## EXAMS
| Exam | Covers | How submitted |
|------|--------|---------------|
| W8 Midterm written | Wk1–6 (Intro → AEAD) | on paper in class, or **`learn.zcr.ai/quiz`** with the code on your slip (120 min) |
| W9 Midterm practical CTF | Wk1–6 | **flags/evidence + payload + mitigation** in one PDF via **`learn.zcr.ai/submit`** (150 min) |
| W18 Final written | cumulative, emphasis Wk10–16 (Hybrid-Encryption → Capstone) | on paper in class, or **`learn.zcr.ai/quiz`** (90 min) |
| W19 Final CTF + capstone demo | cumulative, emphasis Wk10–16 | flags/evidence via **`learn.zcr.ai/submit`**; live CryptoVault project demo (graded by rubric) |

## TERM PROJECT — CryptoVault
- Report: a fill-in report template mirroring `software-security/project/REPORT-TEMPLATE.md`'s
  section-by-section rubric mapping is **not yet built** for this course (see `project/README.md`);
  until it exists, structure your write-up around that README's deliverables list (design doc →
  self-audit, one section per primitive → crypto-agility note → conclusion), export to PDF, and
  submit via **`learn.zcr.ai/submit`**.
- Code + design doc + self-audit: in the team's **GitHub** repo (link in the report).
- Milestones per [project/README.md](project/README.md) (design doc Wk4 → KDF+AEAD-at-rest Wk7 →
  sharing flow draft Wk11 → transport + self-audit Wk14 → capstone-studio WIP demo Wk16 → graded
  final demo Wk19).

---

## Rules for every submission
- **Name + Student ID** on every file; teamwork only where stated (labs/quizzes/exams are individual; CryptoVault is team-graded with peer-contribution scaling — see `project/README.md`).
- **AI-tool disclosure:** state how you used any AI tool (search, code, translate) — a section is built into the worksheet/report.
- **Late:** −10%/day, up to 3 days (see `syllabus.md` §3); submit what you have.

---

## Academic Integrity & Anti-Cheating

This is a security course — we practice the same rigor on your own work. The following controls
are in place; assume your submission is checked.

- **Your flags are unique to you.** Each student receives **personalized CTF/lab flags** derived
  from your student ID. A flag is traceable to the person it was issued to — submitting someone
  else's flag is detected automatically and counts as a violation for **both** parties.
  *(As noted above: this course's personalized-flag pipeline is still being built, so this control
  is not yet technically enforced end-to-end — it is the target state and will be announced when
  live. Treat it as already in force for behavior: do not share or reuse another student's
  evidence in the meantime.)*
- **Your screenshots must show you.** Evidence must include a terminal running `printf '%s | %s | ' "$(whoami)" '<YOUR-STUDENT-ID>'; date '+%F %T %Z'` **in
  the same image as the evidence**. When the evidence is a browser page, a DevTools panel or a
  rendered response, put that terminal **beside the browser and capture the whole screen** — a
  cropped window carries nothing that identifies you, and the lab's own output is
  byte-identical for the whole cohort *by design*, so the stamp is the only thing that makes
  the shot yours. Generic or borrowed screenshots are not accepted.
- **Your code is attributable.** Work in **your own GitHub fork** with your own commits.
  Submissions are run through **code-similarity tools (MOSS/JPlag)** against classmates and
  previous cohorts. A single "paste-everything" commit with no history is a red flag.
- **Quizzes** are individual, time-limited, one attempt, locked to your school account, with
  shuffled questions/options.
- **Random live checks.** You may be asked to **reproduce a task or explain your fix live**.
  Answers you can't explain in your own words score zero.
- **Explain, don't copy.** Reflection questions are graded on *your* reasoning about *your*
  results.

**Allowed:** discussing concepts, helping a classmate debug their *own* setup, using AI tools **if disclosed**.
**Not allowed:** sharing flags/answers/code, submitting another's screenshots, copying a report.

Violations follow this course's ethics & academic-integrity policy ([`ETHICS.md`](ETHICS.md)) and
KOSEN's conduct process.
