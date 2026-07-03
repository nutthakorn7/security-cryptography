# How to Do & Submit Work

**Platforms:** **Google Classroom** (worksheets, reports, grades) + **GitHub** (your code fixes).
This course has its **own** Google Classroom instance and its **own** GitHub repo — separate
from the companion `software-security` course's Classroom and repo, even though the two courses
share the same 19-week skeleton and pedagogy. Join *this* course's Classroom and fork *this*
course's repo; submissions to the wrong course's platform cannot be graded here.

All offensive work is on the provided sandbox targets only — see this course's own ethics &
authorized-use policy, [`ETHICS.md`](ETHICS.md).

---

## One-time setup (Week 1)
1. Create a GitHub account; **fork** this course's repo (`security-cryptography`) to your account.
2. `git clone` your fork; stand up the environment (Docker) per Week 1.
3. Join this course's Google Classroom (code given in class — a different code/instance than any
   other course you're taking).

---

## Weekly LAB — how to do & submit

**Do it:**
1. In your fork, create a branch `wk<NN>` (e.g. `wk04`).
2. Stand up the week's target: `docker compose up` (or the command in that lab's README).
3. Work through the **worksheet** (`labs/week<NN>…/worksheet.md`): for each task record the
   **payload/command**, a **screenshot** of the result, and a **2–3 sentence mitigation**.
4. For the **Defend / fix** task: edit the code, **commit to your `wk<NN>` branch**, and note the
   **commit hash** in the worksheet.

**Submit (two parts):**
| Part | Where | What |
|------|-------|------|
| Worksheet | **Google Classroom** | the completed worksheet exported to **PDF** (screenshots embedded) |
| Code fix | **GitHub** | push branch `wk<NN>`, open a PR (or paste the commit link in the worksheet + Classroom) |

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
enforced manually until the personalized-flag pipeline is live; you'll be told in class/Classroom
once `FLAG_*` values are personalized and this note will be removed.

---

## QUIZ — how it works
- **Online via Google Form** (link posted in this course's Classroom at quiz time).
- **Weekly quiz:** a short **~10-min quiz at the start of every teaching week** (6 Q: 5 MCQ + 1 short, **individual**). Low-stakes — the **lowest 1–2 are dropped**.
- **Cumulative review quizzes:** two bigger 25-pt quizzes in the **review weeks** (W7 pre-midterm, W17 pre-final).
- No separate file to submit — the Form **is** the submission.

---

## EXAMS
| Exam | Covers | How submitted |
|------|--------|---------------|
| W8 Midterm written | Wk1–6 (Intro → AEAD) | on paper / Google Form in class (120 min) |
| W9 Midterm practical CTF | Wk1–6 | submit **flags/evidence + payload + mitigation** via the CTF Form/Classroom (150 min) |
| W18 Final written | cumulative, emphasis Wk10–16 (Hybrid-Encryption → Capstone) | on paper / Google Form (150 min) |
| W19 Final CTF + capstone demo | cumulative, emphasis Wk10–16 | flags/evidence via Form; live CryptoVault project demo (graded by rubric) |

## TERM PROJECT — CryptoVault
- Report: a fill-in report template mirroring `software-security/project/REPORT-TEMPLATE.md`'s
  section-by-section rubric mapping is **not yet built** for this course (see `project/README.md`);
  until it exists, structure your write-up around that README's deliverables list (design doc →
  self-audit, one section per primitive → crypto-agility note → conclusion), export to PDF, and
  submit via **Google Classroom**.
- Code + design doc + self-audit: in the team's **GitHub** repo (link in the report).
- Milestones per [project/README.md](project/README.md) (design doc Wk4 → KDF+AEAD-at-rest Wk7 →
  sharing flow draft Wk11 → transport + self-audit Wk14 → capstone-studio WIP demo Wk16 → graded
  final demo Wk19).

---

## Rules for every submission
- **Name + Student ID** on every file; teamwork only where stated (labs/quizzes/exams are individual; CryptoVault is team-graded with peer-contribution scaling — see `project/README.md`).
- **AI-tool disclosure:** state how you used any AI tool (search, code, translate) — a section is built into the worksheet/report.
- **Late:** score deduction per the syllabus; submit what you have.

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
- **Your screenshots must show you.** Evidence must include your **terminal `whoami` / login
  email / student ID** and a **timestamp**. Generic or borrowed screenshots are not accepted.
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
