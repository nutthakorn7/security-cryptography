# Lesson Plan — Week 16: Capstone Studio (CryptoVault)

| | |
|---|---|
| **Course** | Security & Cryptography (course code `21025117`, per [syllabus.md](../../syllabus.md); the [course specification](../course-specification.md) §1 still records the code as ⬚ — confirm with the registrar before print) |
| **Week / date** | 16 · ⬚ |
| **Contact time** | 300 min, run as one continuous studio block ([AGENDA.md](../../AGENDA.md) per-week table, row 16: Lecture **—**, Lab **300**, Quiz **—**, Exam **—**, Total **300**; course specification §1 records the underlying 2 lecture + 3 laboratory hours) |
| **Lab folder** | ⬚ — there is **no `labs/week16-capstone/`** directory in this repository. course-specification.md §6 records Week 16's lab folder as `project/`; course-plan-19weeks.md states "no separate lab dir by design, covered by `project/README.md`" |
| **Worksheet** | ⬚ — Week 16 has no worksheet. The 12 graded worksheets are Weeks 1–6 and 10–15 (course specification §4) |
| **Slides** | ⬚ — there is no `slides/week16.md`; decks exist for Weeks 01–06 and 10–15 |
| **Practice-CTF board** | ⬚ — AGENDA.md schedules a 150-min "Practice CTF tournament (previews Week 19)" but this repository contains **no Week 16 board file**. The only built boards are `labs/week17-review/mock-ctf.md` (Week 17) and Week 7's mock, carried inline in `labs/week07-review/README.md`. See §6 |
| **Type** | **Capstone studio — no new content.** Term-project work-in-progress + a practice CTF |
| **Targets** | The teams' **own CryptoVault builds** (`project/README.md`) for the morning block; this term's own lab containers for the practice CTF (§6.1) |
| **Standards** | ⬚ — Week 16 introduces no CWE ids of its own. Practice-CTF targets carry the "Analogous CWE" line of their own week's README |
| **CLOs addressed** | **CLO1** select & justify · **CLO3** rebuild correctly · **CLO4** protocol reasoning · **CLO5** evaluate & communicate (course specification §6, row 16). §4's *Term project* row additionally marks **CLO6** — that row covers the project across the whole term, of which today is one checkpoint |

> **Instructor-only material is not reproduced here.** This repository is public. This plan states
> what happens in the session and how it is run; it contains no flag values, no exam questions and
> no answer-key content. The Week 19 instrument this studio warms up for lives in
> `instructor/exams/week19-final-ctf-capstone-answers.md` (git-ignored) — read it before the
> session if you intend to preview the final's format accurately.

---

## 1. Session objectives

This is a studio, not a lecture. Nothing new is taught. What the session is designed to produce:

**Knowledge (K)**
- K1 — Name the **five core primitives** CryptoVault must use *together*, and what each one is
  there for: a slow password KDF, AEAD at rest, a key-exchange/wrapping step for sharing,
  signatures on shared entries, and TLS (or an equivalent authenticated transport)
  (`project/README.md`, *The brief*, items 1–5).
- K2 — For each of the five, state the **weekly failure mode the rubric grades it against**: a
  raw/fast hash (Wk2), raw CBC or a reused nonce (Wk4/Wk6), a symmetric key transmitted or stored
  in the clear (Wk5/Wk10), `hash(secret + message)` or a malleable signature (Wk3/Wk11), and a
  client that skips certificate validation (Wk12).
- K3 — State where the team's **trust boundary** runs and, specifically, where plaintext *and the
  symmetric key protecting an entry* are never allowed to appear — server memory, network, disk
  (`project/REPORT-TEMPLATE.md` §1).
- K4 — Give the **key inventory**: for every key and secret (password-derived key, per-entry data
  key, sharing keypair, signing key, TLS material), how it is derived or generated, where it is
  stored, and who can see it (REPORT-TEMPLATE §1).
- K5 *(stretch)* — Say which primitives are **broken by Shor's** and which merely **weakened by
  Grover's**, and what would be swapped in for PQC-readiness (`project/README.md` item 6;
  REPORT-TEMPLATE §8).

**Skills (P)**
- P1 — Deliver the WIP demo in the shape AGENDA.md names for this block: **design decision →
  failure mode → fix**, over the walkthrough `project/README.md` deliverable 5 specifies —
  *create a vault entry → share it with another user → recipient verifies and decrypts* — narrating
  which primitive is doing what at each step.
- P2 — Trace **one full share-an-entry operation** out loud in the required order,
  `KDF → AEAD(at rest) → key exchange/wrap → signature → TLS`, naming which key is in play at each
  hop (REPORT-TEMPLATE §7). This is the 20-point rubric line, the heaviest one.
- P3 — Cite **where in the code** each primitive lives, as `file:line`, on demand — the field
  REPORT-TEMPLATE asks for in §§2–6.
- P4 — Peer-review another team against the **seven rubric criteria** of `project/README.md` and
  convert that review into a written punch-list with an owner per item (§5.2).
- P5 — State, out of the deliverables in `project/README.md`, exactly which are **done**, which are
  **partial**, and who owns the remainder before the graded demo in Week 19.
- P6 — Re-run this term's labs unaided in the practice CTF and produce the evidence artefact each
  week actually gates on — a flag for Wk2/3/4/6/11/15, a log line for Wk5/12/13/14 (SUBMISSION.md,
  *Flags and evidence, by week type*).

**Attitude (A)**
- A1 — Demo and test **only** the team's own app and the team's own test accounts, "never another
  team's deployment without permission" (`project/README.md`, closing ethics note), under
  [ETHICS.md](../../ETHICS.md).
- A2 — Show identity-stamped evidence — SUBMISSION.md's anti-cheating section requires the
  terminal `whoami` / login in screenshots, and the same standard applies to a live demo: the app
  on screen is the team's own build, running from the team's own repository.
- A3 — Take peer criticism as a punch-list to work, not a verdict to argue with, and give it the
  same way.
- A4 — Disclose AI-tool use honestly — the report carries a mandatory disclosure table, and "None"
  is a valid answer (REPORT-TEMPLATE, *AI-tool usage disclosure*).

## 2. Key ideas (the through-line)

CryptoVault inverts the whole term. `project/README.md` is explicit about it: this is a
**"build it right," not "find the bug"** project, where every week from Wk2 to Wk15 handed the
student a broken construction, and the project asks them to compose the same primitives so that
none of those failure modes reappears in their own code. Grading "rewards **correct composition** —
using each primitive for what it's actually for, and wiring them together so the whole pipeline
holds — over feature count or polish."

That is why the rubric's heaviest line is not a primitive at all. Five criteria worth 12–15 points
each grade the primitives (13 KDF, 15 AEAD, 15 key exchange, 15 signatures, 12 transport);
**20 points** grade the end-to-end composition — the share-an-entry flow
being secure *as a system*, not primitive-by-primitive — and REPORT-TEMPLATE §7 asks specifically
about **the seams**: "the one or two points where two primitives meet (e.g. the data key handed
from AEAD to the key-wrap step) and why that hand-off is safe." A team that can demo five correct
primitives and cannot narrate the hand-off between two of them is carrying a 20-point hole into
Week 19. Today is the cheapest place to find that out.

The second job is calibration. AGENDA.md gives the afternoon to a practice CTF that "previews
Week 19", where the same tournament is graded and the project demo is scored beside it. A team that
discovers on the day of the final that nobody remembers how to bring up the Week 15 target has lost
points to logistics, not to difficulty.

## 3. What teams bring in, and what they leave with

### 3.1 Coming in

By `project/README.md`'s own *Suggested timeline*, **every milestone before today is already
past due** — so this is a check, not a start:

| Milestone (verbatim from `project/README.md`) | Due |
|---|---|
| Team formed + design doc (KDF + AEAD-at-rest plan) | Week 4 |
| KDF + AEAD-at-rest working (local vault, no sharing yet) | Week 7 |
| Sharing flow — key exchange/wrapping + signatures — draft | Week 11 |
| TLS/transport wired in + self-audit drafted | Week 14 |
| **Capstone studio — WIP demo & peer review** | **Week 16 — today** |
| Final demo, self-audit, and crypto-agility note (graded) | Week 19 |

The five deliverables those milestones roll up into (`project/README.md`, *Deliverables*):

| # | Deliverable | What counts as evidence today |
|---|---|---|
| 1 | **Design doc** — one diagram + one page | The diagram on screen with the **trust boundary** drawn, plus the key inventory (REPORT-TEMPLATE §1) |
| 2 | **Working build** — all five core primitives together, "in a repo with commits that let the team's contributions be traced" | The app runs; `git log` shows more than one contributor |
| 3 | **Self-audit** — a short note per primitive citing *where in the code* and *why the choice is correct* | The `file:line` fields of REPORT-TEMPLATE §§2–6, answerable live |
| 4 | **Crypto-agility note** *(stretch)* — the ½–1 page PQC note | Draft or explicit "not started"; it is `+5` bonus, capped so the total cannot exceed 100 |
| 5 | **Demo** — the live walkthrough | Runs today as the **WIP demo**; the graded one is Week 19 |

### 3.2 Leaving with

Derived — the repository does not enumerate Week 16 outputs beyond AGENDA.md's "peer review" and
"finalize checklist before the final". Four things, all produced in the room:

| Artefact | Produced in | Basis |
|---|---|---|
| A written **punch-list** of gaps, three items, each with a named owner and a date | WIP review block | Derived from AGENDA.md's "+ peer review" and `project/README.md`'s milestone-to-Week-19 gap; the sheet is in §5.2 |
| **Peer marks against the seven rubric criteria** | WIP review block | `project/README.md`, *Rubric (100 pts)* |
| A **deliverable checklist** showing which of the five are real, not claimed | WIP review block | `project/README.md`, *Deliverables* |
| A **tournament retro**: what slowed us down, who owns what in Week 19 | End of the CTF block | Derived; AGENDA.md's 4:45–5:00 "Feedback + finalize checklist before the final" |

### 3.3 Instructor, before class

- **Decide the pod split and the rotation order** (§4.1–4.2) from the actual team count. This
  cannot be done in the room; see the arithmetic in §4.1.
- **Decide what the afternoon tournament actually is** — the repository ships no Week 16 board
  (§6). Make this decision before the session, not at 2:15.
- **Bring the practice targets up once** on a representative machine the day before. Every lab
  container in this course runs `pip install --no-cache-dir -r requirements.txt` *at container
  start* off `python:3.12-slim`, so the network cost lands in the room, not in a build cache.
  Pre-pull `python:3.12-slim`.
- **Know that there is no starter application.** `project/` contains `README.md` and
  `REPORT-TEMPLATE.md` only, and the brief says "You may pick any tech stack." You cannot pre-pull
  a team's images or predict their stack; a team whose environment is broken has no course-supplied
  fallback app. Plan §7 accordingly.
- **Confirm the scoreboard question.** README.md records that the labs are "not yet live in a CTFd
  deployment"; SUBMISSION.md is more specific — it records **no running CTFd instance yet** and
  that `FLAG_*` values are currently the same placeholder for everyone rather than per-student. If
  you want a leaderboard this afternoon, it is a whiteboard.

## 4. Studio timetable — 300 min

The four block boundaries below are AGENDA.md's (*Week 16 — Capstone Studio (300 min)*) and are
fixed. Everything finer is derived, and each derivation names its arithmetic.

| Time | Block | What happens | Source |
|---|---|---|---|
| 0:00–0:10 | **Studio stand-up** | Every team, standing, one minute or less: what is demo-ready, what is broken, what you want from the room today. Record the "broken" column — it is the §7 triage list | Derived: taken *out of* AGENDA.md's 0:00–2:00 block, leaving 110 min |
| 0:10–1:55 | **WIP review slots** | 7 × 15 min, run in parallel pods (§4.1 Variant B; a single strand under Variant A). The presenting team demos; the non-presenting teams score the rubric and write the punch-list | Derived: 110 min ÷ 15 min per team = 7 slots + 5 min slack. **15 min is Week 19's format** — "10-min demo + 5-min Q&A per team" (AGENDA.md, Week 19) — reused here because AGENDA.md states **no per-team budget for Week 16** (⬚) |
| 1:55–2:00 | **Punch-list handover** | Reviewing teams hand the presenting team the written sheet; collect the deliverable checklists | Derived from the same block |
| 2:00–2:15 | **Break** | | AGENDA.md |
| 2:15–2:25 | **Tournament rules + target check** | Read out the submit format; every team proves at least one target is up before the clock starts | Derived, mirroring AGENDA.md's Week 9 line ("0:00–0:10 rules + target check") |
| 2:25–4:30 | **Practice CTF tournament** | §6 — and read §6 before the session, because the board is ⬚ | Derived: the remainder of AGENDA.md's 2:15–4:45 tournament block |
| 4:30–4:45 | **Tournament retro** | What slowed you down; who owns what in Week 19 | Derived from the same block |
| 4:45–5:00 | **Feedback + finalise the checklist before the final** | Each team names one deliverable it will close before Week 19 and who owns it; confirm the Week 17/18/19 sequence | AGENDA.md |

> **Do not sub-divide the 10-minute demo into timed segments.** The sibling course's Week 16
> worksheet publishes a per-segment clock; this course has no Week 16 worksheet, and nothing in
> this repository budgets the inside of the demo. Give teams the **order** from AGENDA.md and
> `project/README.md` deliverable 5 — design decision → failure mode → fix, over
> create → share → verify-and-decrypt — and let the pod's timer enforce only the 10/5 split.

### 4.1 Why the demos must run in parallel

Straight arithmetic, all of it repo-sourced:

- AGENDA.md gives the demo block **120 min**. Week 19's stated per-team format is **15 min**
  (10 demo + 5 Q&A) → **8 slots**, and 7 once the stand-up is taken out.
- The only cohort figure the repository states is AGENDA.md's **N≈80–120**, and it appears in a
  sentence about weekly presentations being impossible — it does **not** say whether that is the
  whole cohort or one section. `project/README.md` and `syllabus.md` §3 put project teams at
  **2–3**, so N≈80–120 implies **27–60 teams** across however many sections that figure covers;
  split across two sections it is still **14–30 teams per session**.
- Actual cohort size, section split and team count for this cohort: ⬚.

Unless the team count is ≤ 7, a single plenary strand cannot seat everyone — and on the repo's own
figures it is not ≤ 7 under either reading. Two variants:

- **Variant A — plenary.** Use when the team count is ≤ 7. One strand, the table in §4 as written,
  every team seen by the instructor.
- **Variant B — parallel pods (the default at N≈80–120).** Pods = ⌈teams ÷ 7⌉, so the 27–60 teams
  above imply **4–9 pods**; the exact pod count and teams-per-pod for this cohort are ⬚. Each pod
  runs its own 15-minute slots. Within a pod, the non-presenting teams are the peer reviewers, and
  the instructor rotates (§4.2).

Draw pods **within a House** where possible — project teams are "nested in your House"
(`project/README.md`), so the reviewers already know each other and cross-House copying is not
being invited.

### 4.2 Instructor rotation

Under Variant B the instructor cannot sit every slot. Rotate on the 15-minute clock, one whole
slot per pod, and make the rotation **visible** — teams should know which slot you will be in,
because that is the slot in which they ask their hardest question.

| Rotation | Time | Pod visited | The instructor's job in that slot |
|---|---|---|---|
| R1 | 0:10–0:25 | Pod 1 | Sit the full slot. Ask for the §7 trace — *"walk me from the password to the recipient's plaintext, naming the key at each hop"* — and one unscripted follow-up on the seam between two primitives |
| R2 | 0:25–0:40 | Pod 2 | As R1 |
| R3 | 0:40–0:55 | Pod ⬚ | As R1 |
| R4 | 0:55–1:10 | ⬚ | As R1 |
| R5 | 1:10–1:25 | ⬚ | As R1 |
| R6 | 1:25–1:40 | ⬚ | As R1 |
| R7 | 1:40–1:55 | Triage sweep | Do not sit a slot. Walk the §7 triage list from the stand-up — the teams that said "broken" |

Fill the pod column from the actual pod count. With more pods than rotations, prioritise the teams
that reported a broken deliverable at stand-up and cover the rest from their written punch-lists.

**Rotation discipline.** Pods keep running while you are elsewhere — peer review is the primary
mechanism here, not filler, because there is no instructor-graded instrument in this session at all
(§8). Leave each pod a printed rubric (§5.1) and a timer instruction: slots start on the
quarter-hour whether or not the previous team finished.

**One question worth asking in every pod you visit.** Ask each member to name the primitive *they*
implemented and where it lives. `project/README.md` states each member's mark is scaled by an
averaged private peer rating (typically ×0.8–1.1) and that "each member's own commit history
corroborates who did what. A 'single paste-everything' contribution is a red flag." Surfacing a
one-person team in Week 16 gives them three weeks to fix the split; surfacing it at the Week 19
submission does not.

## 5. The work-in-progress review

### 5.1 What is checked

The review instrument is the project's own rubric — there is no separate Week 16 rubric in this
repository, and inventing one would grade teams against a standard the graded event does not use.
Each line names the weekly failure mode it is graded against, which is exactly the question to ask
in the slot:

| Criterion (`project/README.md`) | Pts | Ask in the slot |
|---|---:|---|
| Password KDF — slow KDF (Argon2id/bcrypt), correctly parameterized, no raw/fast hash (Wk2) | 13 | Which KDF, which parameters, and where is the per-user salt? |
| AEAD at rest — AES-GCM/ChaCha20-Poly1305, verified-unique nonce per encryption, no raw CBC (Wk4/Wk6) | 15 | *How is uniqueness guaranteed for **every** encryption?* — see the trap in §7 |
| Key exchange / key wrapping for sharing — symmetric key never transmitted or stored in the clear (Wk5/Wk10) | 15 | How is the recipient's public key authenticated? (that is the Wk5 MITM question) |
| Digital signatures — real signature scheme, verified on receipt, malleability-safe (Wk3/Wk11) | 15 | What exactly is signed, and where is verification on the receive path? |
| Transport security — TLS or equivalent, no validation-skipping fallback (Wk12) | 12 | Show the client context. Is there a debug branch that disables verification? |
| **End-to-end composition** — the whole flow secure as a system; self-audit explains each choice | 20 | The §7 trace, plus *"where do two primitives meet, and why is that hand-off safe?"* |
| Demo & report clarity (design doc + self-audit write-up) | 10 | Is the trust boundary drawn, or described? |
| *Crypto-agility note (stretch)* | *+5* | Shor vs Grover — which of your primitives, and what replaces them? |

Check against **evidence, not the claim**. "We use Argon2id" is not a tick; the `file:line` field
REPORT-TEMPLATE §2 asks for, shown on screen, is. Likewise the transport line is not ticked on the
word "HTTPS" — it is ticked when the client's certificate-validation code is on screen and there is
no fallback branch that turns it off.

**Scoring scale for the peer review: ⬚.** The repository defines none for Week 16. Two workable
choices — mark each line ✓ / partial / ✗ (fast, and enough to drive a punch-list), or score each
line against its own point value (slower, but rehearses the Week 19 mark). Announce one at the
stand-up and use it in every pod, or the sheets will not be comparable.

### 5.2 The feedback format teams receive

Derived — **the repository defines no Week 16 feedback sheet**; AGENDA.md says only "peer review".
The format below is a proposal you may replace, built only out of the rubric's own criterion names
so nothing on it is graded against a standard the project does not use. One sheet per presenting
team, filled by the reviewing team during the slot, handed over at 1:55.

```
CRYPTOVAULT WIP REVIEW — team: ______________  reviewed by: ______________  date: ______

Rubric lines (✓ / partial / ✗):
  KDF __   AEAD-at-rest __   key exchange/wrap __   signatures __
  transport __   end-to-end composition __   demo & report clarity __
  crypto-agility note (stretch) __

Deliverables seen, not claimed:
  1 design doc + trust boundary ☐   2 working build (all 5, together) ☐
  3 self-audit with file:line ☐     4 crypto-agility note ☐   5 demo ran ☐

Share-an-entry trace — did they name the key at every hop?
  KDF ☐ → AEAD ☐ → key exchange/wrap ☐ → signature ☐ → TLS ☐

| # | Gap observed (one line)             | Fix before Week 19 | Owner | Done ☐ |
|---|-------------------------------------|--------------------|-------|--------|
| 1 |                                     |                    |       |        |
| 2 |                                     |                    |       |        |
| 3 |                                     |                    |       |        |

One thing this team does better than us: ______________________________________
```

Three rules that make the format work:

1. **Every gap gets a named owner and a date.** The owner column is the same question the retro
   asks at 4:30; ask it while the gap is fresh.
2. **Gaps are phrased against a rubric line, not as taste.** "The nonce comes from a counter stored
   in the same row as the ciphertext" is actionable; "crypto felt shaky" is not.
3. **Cap it at three.** A punch-list of twelve items is a punch-list of none.

## 6. The afternoon tournament — read this before the session

AGENDA.md budgets **150 min** (2:15–4:45) to a "Practice CTF tournament (previews Week 19)".
**No Week 16 board exists in this repository** (⬚). The only built boards are
`labs/week17-review/mock-ctf.md` — Week 17's ~165-min mock, "Covers: the whole term, **emphasis
Weeks 10–16** · Format: same as the Week 19 final practical · Ungraded (participation)" — and Week
7's, carried inline in `labs/week07-review/README.md` and covering Weeks 1–6 only. Three honest
options; pick one **before** the day:

- **(b) — recommended. Run an open re-run block against the targets in §6.1.** Teams pick the weeks
  they are least confident in; the "tournament" is a whiteboard leaderboard. This is the option
  that actually satisfies AGENDA.md's stated purpose without spending Week 17's material: teams
  self-select the Week 10–15 targets the final emphasises, and the retro question at 4:30 ("which
  week will you drill?") is answered by what they chose to run.
- **(a) Fallback — run a subset of the Week 17 mock today.** Closest to the letter of AGENDA.md,
  but Week 17's lesson *is* the dry run for the final, and reusing its board a week early spends
  that material twice. If you must, take the *callback round* (challenges 7–11, Weeks 2–6) and
  leave the main round for Week 17 — accepting that the callback round previews the half of the
  final that is de-emphasised, which is precisely why this is the fallback and not the default.
- **(c) Give the time to the projects.** Defensible in a cohort where most teams are Amber or Red
  at stand-up (§7), and honest — but announce it rather than letting the block drift.

Whichever you choose: nothing this afternoon is graded (§8), the ethics policy applies to the
practice targets exactly as it does in a graded run ([ETHICS.md](../../ETHICS.md)), and for each
challenge attempted teams should record **the payload/command and a one-line mitigation** — the
habit `labs/week17-review/mock-ctf.md` asks for and the Week 19 practical marks.

### 6.1 This term's targets — how each one actually starts

Verified against the compose files and lab READMEs in this repository. Note that **the six
flag-gated labs publish six disjoint port pairs** (8092–8103), so unlike a single-port course they
can all be up at once — the cost is not a port clash but twelve containers each running
`pip install --no-cache-dir -r requirements.txt` at start.

| Week | Start command (run in that lab directory) | Ports | Artefact |
|---|---|---|---|
| Wk2 Hash | `docker compose up -d` | :8094 vulnerable / :8095 fixed | flag `FLAG_HASH` |
| Wk3 MACs | `docker compose up -d` | :8092 / :8093 | flag `FLAG_MACS` |
| Wk4 AES modes | `docker compose up -d` | :8096 / :8097 | flag `FLAG_AES` |
| Wk6 AEAD | `docker compose up -d` | :8098 / :8099 | flag `FLAG_AEAD` |
| Wk11 Signatures/ZKP | `docker compose up -d` | :8102 / :8103 | flag `FLAG_SIG` |
| Wk15 PQC | `docker compose up -d` | :8100 / :8101 | flag `FLAG_PQC` |
| Wk5 Key exchanges | `docker compose -f docker-compose.vulnerable.yml up --build` then `docker compose -f docker-compose.fixed.yml up --build` | none published | log line |
| Wk12 Secure transport | `docker compose -f docker-compose.vulnerable.yml up --build` / `docker compose -f docker-compose.fixed.yml up --build`; the student task is `docker compose -f docker-compose.student-task.yml up --build` | none published | log line |
| Wk13 E2E encryption | `docker compose -f docker-compose.vulnerable.yml up --build` / `docker compose -f docker-compose.fixed.yml up --build` | none published | log line |
| Wk14 Authentication | `docker compose -f docker-compose.vulnerable.yml up --build --abort-on-container-exit` then `docker compose -f docker-compose.fixed.yml up --build --abort-on-container-exit` | none published | log line |
| Wk10 Hybrid encryption | No Docker target by design — audit `audit_the_ai/` | — | written analysis |

Tear-down for the log-line weeks is `docker compose -f <file> down` (Wk12 and Wk13's READMEs use
`down -v` and `down` respectively — follow the lab's own line).

### 6.2 The retro (4:30–4:45) — three questions

1. **What slowed you down?** Force a concrete answer — a target that would not start, a technique
   nobody had practised, duplicated effort.
2. **Who owns what in Week 19?** Write the names down; same column as the punch-list owner.
3. **Which week will you drill before the final?** Map the answer onto Week 17's mock so the drill
   has a scheduled slot.

Close by naming what changes in Week 19: AGENDA.md gives it 0:00–2:30 for the cumulative tournament
and 2:30–4:00 for **graded** CryptoVault demos at 10 min + 5 min Q&A per team, and SUBMISSION.md
records the final written paper (Week 18) as cumulative with emphasis on Weeks 10–16.

## 7. Support for teams that are behind

"Behind" has a repo definition today — `project/README.md`'s milestone table (§3.1). Triage at the
stand-up and assign a tier; the tier decides what the team spends the 120-minute block on.

| Tier | Definition (`project/README.md` milestones) | What they do today |
|---|---|---|
| **Green** | All five deliverables present; the share-an-entry demo runs end to end | Normal slot. Push them: the §7 trace, the seam question, and the crypto-agility note — it is `+5` and it is the fastest five points on the board for a team with nothing left to build |
| **Amber** | Design doc (W4) and local vault with KDF + AEAD (W7) exist; the sharing flow (W11) or TLS + self-audit (W14) is partial | Demo the part that works, then **spend the rest of their own slot building**, in the room, with the peer team watching. The self-audit is the most recoverable item in a session — REPORT-TEMPLATE §§2–6 are fill-in tables, so a team that can answer the questions out loud can write the section on the spot (no repo-stated budget for this; instructor's judgement) |
| **Red** | The five primitives are not composed at all, or the app will not run | Drop the demo for today. There is **no course-supplied starter app** to reset onto (`project/` ships `README.md` and `REPORT-TEMPLATE.md` only), so the recovery path is the labs' own fixed implementations as reference (below). Target: one primitive working end to end, in their own repo, by 1:55 |

**Reference implementations in this repository** — every one of the five primitives has a working,
already-verified counterpart in a lab the team has run:

| Primitive | Reference in this repo |
|---|---|
| Slow password KDF | `labs/week02-hash/fixed_app.py` — bcrypt store; "each hash embeds a per-user random SALT and a tunable work factor (cost)" |
| AEAD at rest | **Use `labs/week04-aes-modes/fixed_app.py`** — AES-256-GCM with `nonce = os.urandom(12)` and the comment "96-bit GCM nonce -- fresh every token". That is the pattern the rubric wants. **Not** `labs/week06-aead/fixed_app.py`, which is AES-256-GCM with a *fixed* nonce — see the warning below |
| Key wrapping for sharing | `labs/week13-e2e-encryption/common.py` — "Hybrid encryption: AES-256-GCM for the message body, RSA-OAEP to wrap the" key |
| Signatures, malleability-safe | `labs/week11-signatures-zkp/fixed_app.py` — low-S normalisation, "BIP-62 canonical check: a signature is only accepted if s is in the LOWER half" |
| Transport | `labs/week12-secure-transport/alice_student.py` — the one function students write themselves, `build_client_context()`. The working implementation is in `alice.py`, which carries **both** branches gated on `VERIFY`: `create_default_context()` + `load_verify_locations(ca.crt)` (trust only the demo CA, `check_hostname=True`, `CERT_REQUIRED`) against the bypass path (`check_hostname = False` set *before* `verify_mode = ssl.CERT_NONE`). Only the first branch belongs in a CryptoVault build |
| Keyed integrity, not `hash(secret+message)` | `labs/week03-macs/fixed_app.py` — "a proper HMAC (hmac.new(key, msg, sha256)) instead of a secret-prefix hash" |

> **Warn every team about the AEAD nonce before they copy anything — the course ships two AES-GCM
> references and only one of them is safe to lift.** `labs/week04-aes-modes/fixed_app.py` derives a
> fresh nonce per token (`nonce = os.urandom(12)`, "fresh every token") and is the correct pattern.
> `labs/week06-aead/fixed_app.py` uses a **fixed** nonce and says so in its own comment (lines
> 33–35): it is "Fixed so /secret is stable within a process. (In real systems a GCM nonce must be
> UNIQUE per message under a key … a fixed nonce is acceptable here only because we encrypt exactly
> one message per process.)" A vault encrypts many entries under one key. A team that lifts the
> Week 6 file — the one from the week actually titled *AEAD* — loses the 15-point line to the exact
> failure the rubric names, "verified-unique nonce per encryption", and Week 10 spends its whole
> session proving why. Say this at the stand-up; it is the single most likely way a diligent team
> fails a criterion.

Three further supports, all cheap:

- **The self-audit is worth more than another feature.** The rubric gives 20 points to end-to-end
  composition and 10 to demo/report clarity, and both are written work. An Amber team with four
  hours left should write, not build.
- **Milestone dates are not the mark.** `project/README.md`'s rubric scores the artefacts, not
  their punctuality; Week 19 is the graded event. Tell Amber and Red teams that, then hold them to
  the punch-list.
- **Peer-contribution fairness cuts both ways.** The ×0.8–1.1 scaling protects the members who did
  the work, and `project/README.md` states "an unjustified low score is discussed before it's
  applied". Say both halves of that today, in front of the team.

## 8. Assessment for this week

**Nothing in this session is graded.** That is a derivation from the assessment table, and it is
worth stating to students so nobody spends the day optimising for a mark that is not there:

- course-specification.md §4 lists five graded components; the only one this session touches is the
  **term project (15%)**, which is graded at the **Week 19** demo against `project/README.md`'s
  100-point rubric, with each member's mark scaled by peer contribution.
- There is **no Week 16 worksheet** — the 30% worksheet component covers Weeks 1–6 and 10–15.
- There is **no weekly quiz** — AGENDA.md's per-week table gives Week 16 a quiz column of "—", and
  the retrieval quizzes belong to the teaching weeks.
- SUBMISSION.md lists no Week 16 submission. The project's own submission channels are Google
  Classroom for the report (PDF) and GitHub for code and design doc.

| Instrument | Evidence | Outcome | Weight |
|---|---|---|---|
| Today's WIP demo | The live create → share → verify walkthrough, plus the rubric trace | P1–P3, A1, A2 | **Ungraded** — formative. `project/README.md` places the graded demo in Week 19 |
| Peer review + punch-list | The sheet in §5.2 | P4, P5, A3 | **Ungraded** — the punch-list is the deliverable, not a mark |
| Practice tournament | Flags / evidence log lines + payload + one-line mitigation | P6 | **Ungraded**; points feed the non-graded Houses layer (syllabus.md §3) |
| Term project (graded Week 19) | The five deliverables + the graded demo | CLO1, CLO3, CLO4, CLO5, CLO6 | 15% of the final mark |

## 9. Materials

- Project (the source of truth for this week): [`project/README.md`](../../project/README.md) ·
  [`project/REPORT-TEMPLATE.md`](../../project/REPORT-TEMPLATE.md)
- Week agenda: [AGENDA.md](../../AGENDA.md) *Week 16 — Capstone Studio (300 min)* · course
  specification [§6](../course-specification.md) row 16
- Practice targets: `labs/week02-hash` · `labs/week03-macs` · `labs/week04-aes-modes` ·
  `labs/week05-key-exchanges` · `labs/week06-aead` · `labs/week10-hybrid-encryption` ·
  `labs/week11-signatures-zkp` · `labs/week12-secure-transport` · `labs/week13-e2e-encryption` ·
  `labs/week14-authentication` · `labs/week15-pqc`
- Nearest built board, if you choose option (a) in §6:
  [`labs/week17-review/mock-ctf.md`](../../labs/week17-review/mock-ctf.md)
- Reference implementations for behind teams: the table in §7
- Instructor-side: `instructor/exams/week19-final-ctf-capstone-answers.md` (git-ignored — the
  format this studio previews) · `instructor/seed_flags.py` · `instructor/check_flag_keys.py`
- Printing list: the §5.2 review sheet × one per presenting team; the §5.1 rubric × one per pod
- Submission channels: [SUBMISSION.md](../../SUBMISSION.md) · Rules of engagement:
  [ETHICS.md](../../ETHICS.md)

## 10. Risks and contingencies

| Risk | Mitigation |
|---|---|
| **More teams than slots.** 120 min ÷ 15 min = 8 slots (7 after the stand-up), against 27–60 teams at N≈80–120 in teams of 2–3 (§4.1) | Run Variant B pods (§4.1) and publish the pod list before the session. If even pods overflow, drop the Q&A to the pod the instructor is sitting in and keep the 10-minute demo everywhere else |
| **No board exists for the 150-minute tournament block** — AGENDA.md schedules it, the repository does not contain it (§6) | Decide *before* the day. §6 recommends option (b) — an open re-run against the §6.1 targets, teams choosing their weakest weeks — because it serves the "previews Week 19" purpose without spending Week 17's mock a week early |
| **`docker build` fails on `COPY` because the repository lives in OneDrive.** The Wk12, Wk13 and Wk14 READMEs all record that these labs were verified from a **local scratch copy** because "OneDrive placeholder files can break `docker build` COPY". Those four log-line labs are exactly the ones that build an image rather than bind-mounting | Copy the lab directory to a local scratch path before `--build`, as the labs' own verification notes did. Teams hitting this in the room should not debug Docker — hand them the scratch-copy workaround and move on |
| **Twelve containers, each running `pip install --no-cache-dir -r requirements.txt` at start.** Every flag-gated lab in this course installs at container start off `python:3.12-slim` | Pre-pull `python:3.12-slim` before the session and warm one machine. Do not have the whole room bring up all six pairs at once; §6.1's ports are disjoint, which makes it tempting |
| **No CTFd, and flags are not personalised.** README.md records the labs as "not yet live in a CTFd deployment"; SUBMISSION.md is more specific — no CTFd instance exists for this course and `FLAG_*` values are "still the same placeholder value for everyone, *not* personalized or checked against a roster" | Tally on the whiteboard. Treat duplicate flags this afternoon as a non-event: nothing is graded, teams play together, and the values are shared by construction. Keep `instructor/seed_flags.py` (`python3 ../../instructor/seed_flags.py env <STUDENT_ID> > .env`) for the graded Weeks 9 and 19 |
| **A team's TLS "works" because verification is off.** The 12-point transport line explicitly excludes a "validation-skipping fallback", and Wk12 is the week that demonstrates exactly that bypass | Ask to see the client context, not the URL bar. `labs/week12-secure-transport` generates a demo CA at container start and gates the fix on `VERIFY=1`; a team demoing over self-signed TLS should show the same shape — a trust anchor plus hostname checking — not `verify=False` with a comment |
| **A team ships `ecdsa` in their own build because the signatures lab does.** course-specification.md §10 records that `labs/week11-signatures-zkp` depends on `ecdsa`, which "carries an unfixable advisory (CVE-2024-23342, side channels declared out of scope upstream)" and is used deliberately because its pure-Python implementation makes the demonstrations legible | That acceptance is scoped to the lab, not to a build graded on correct composition. Flag it in the slot: the 15-point signature line wants a real, verified, malleability-safe scheme — point them at a vetted library and, if they keep ECDSA, at low-S normalisation and the nonce question |
| **The AEAD nonce trap** — the fixed reference the course supplies uses a fixed nonce by design (§7) | Announce it at the stand-up, before any team copies the pattern into a multi-entry vault |
| **Peer review degenerates into praise.** Ungraded feedback between friendly teams scores everything green | Require a mark on all seven rubric lines and *three* punch-list gaps with owners; a sheet handed in with fewer than three goes back to the reviewing team. The "one thing this team does better than us" line is where the praise goes |
| **A team's own app will not run at all in the room** | They present the design doc and the trace from the diagram, then spend the slot on the environment rather than the slides — and they are Red on the §7 triage list. There is no starter app to fall back on in this course; say so early rather than hunting for one |
| **A team demos against something that is not theirs.** `project/README.md`'s ethics note limits work to "your own team's app and your own test accounts, never another team's deployment without permission" | State the boundary at the stand-up. A demo against anything else stops there and is handled under [ETHICS.md](../../ETHICS.md) |

## 11. Post-teaching reflection

*Complete after the session — this also feeds the course's engagement data.*

- Attendance / completion: ⬚
- Actual team count, pod count and slots run (vs. the ⬚ in §4.1): ⬚
- Time actually taken per block (vs. plan): ⬚
- Teams triaged Amber/Red at the stand-up, and whether they closed the gap by 1:55: ⬚
- How many teams could trace `KDF → AEAD → key exchange/wrap → signature → TLS` unprompted: ⬚
- How many teams had copied a fixed nonce out of the Week 6 reference: ⬚
- Which rubric line the punch-lists most often flagged: ⬚
- Which option was used for the afternoon block (§6 a/b/c), and whether it was worth 150 min: ⬚
- Peer-contribution imbalances surfaced today, and what was said to the team: ⬚
- Anything to change before this week runs again: ⬚

---

### Escalations — defects in lab/course content, recorded here rather than fixed

These are content issues found while writing this plan. They are **not** corrected in `project/`,
`labs/`, `AGENDA.md`, `SUBMISSION.md` or the course specification, because that material is graded,
parity-gated against the curriculum monorepo, and mirrored by instructor answer keys.

1. **SUBMISSION.md contradicts `project/README.md` about the report template.** SUBMISSION.md's
   *TERM PROJECT — CryptoVault* section states that a fill-in report template "is **not yet built**
   for this course" and tells students to "structure your write-up around that README's
   deliverables list" instead. `project/REPORT-TEMPLATE.md` exists, is complete, and
   `project/README.md`'s *Report* section instructs students to use it. Students following
   SUBMISSION.md will hand in a differently structured report from the one the rubric's section
   mapping expects.
2. **The Week 19 graded-demo block cannot seat the cohort.** AGENDA.md gives Week 19's demos
   2:30–4:00 (**90 min**) at "10-min demo + 5-min Q&A per team" — **6 teams**. The same file puts
   the cohort at N≈80–120 (without stating whether that is the whole cohort or one section), and
   `project/README.md`/`syllabus.md` put project teams at 2–3 — i.e. roughly 27–60 teams, or 14–30
   per session if that figure spans two sections. Either reading overruns 6 slots by a factor of
   two or more. Week 16's 120-minute WIP block has the same shape and, unlike Week 19,
   states **no per-team budget at all**. Whatever the fix (parallel panels, staged demo days,
   recorded submissions), it is a scheduling decision for the graded event, not something a lesson
   plan should silently absorb.
3. **Week 16's tournament block has no board.** AGENDA.md schedules 150 minutes of "Practice CTF
   tournament (previews Week 19)" for Week 16, but the repository contains no Week 16 board file —
   the built boards are Week 7's (inline in `labs/week07-review/README.md`, Weeks 1–6) and Week
   17's `mock-ctf.md` (~165 min, whole term, emphasis Weeks 10–16, "same as the Week 19 final
   practical"). Weeks 16 and 17 therefore schedule two near-identical practice tournaments in
   consecutive weeks with material for only one. §6 gives three ways to run the block and
   recommends one; none of them is what the AGENDA literally promises.
4. **The AEAD reference students are most likely to reach for collides with the project's AEAD
   rubric line.** `project/README.md` awards 15 points for "AEAD at rest … with a **fresh, unique
   nonce per encryption** — never raw CBC, never a fixed or counter-reused nonce". The course ships
   two AES-256-GCM reference implementations: `labs/week04-aes-modes/fixed_app.py` uses
   `os.urandom(12)` per token and satisfies the line, while `labs/week06-aead/fixed_app.py` — the
   file from the week actually named *AEAD*, and therefore the one a team searching for "the AEAD
   reference" finds first — uses a **fixed** nonce. Neither lab is wrong, and Week 6 documents the
   choice honestly in its own comment (lines 33–35), but the two pieces of course material meet on
   the student's desk and the safer of the two is the less discoverable one. The cheapest fix is a
   cross-reference: one clause in Week 6's comment, or in the project brief's AEAD item, pointing
   at Week 4 as the pattern to copy for multi-message storage.
5. **course-plan-19weeks.md contradicts itself on Week 16's build status** within a single
   paragraph: the same *Verification status* block lists Wk16's capstone under "**Built:**" and
   then under "**Remaining: Wk16 (capstone)**". The course-at-a-glance table marks it
   "✅ *built (`project/README.md`)*". Cosmetic, but it is the file a reader checks to know what is
   finished.
