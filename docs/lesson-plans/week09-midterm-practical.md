# Lesson Plan — Week 9: Midterm — Practical (CTF)

| | |
|---|---|
| **Course** | Security & Cryptography (`21025117`, syllabus.md §header) |
| **Week / date** | 9 · ⬚ |
| **Week kind** | Exam — practical (no lecture, no weekly quiz; single graded block) |
| **Contact time** | 150 min single block (AGENDA.md "Week 9 — Midterm CTF practical (150 min)" / per-week table Wk9 Exam = 150, Total = 150). The standard 300-min lecture+lab split does **not** apply to exam weeks. |
| **Lab folder** | `⬚ (instructor-held)` — course-spec §6, Wk9 row. There is **no** `labs/week09-midterm-practical/` directory in the repo; the exam re-uses the already-built Wk2/3/4/6 lab targets (see §1). |
| **Slides** | ⬚ (no `slides/week09.md`; exam week has no deck) |
| **Standards** | Analogous CWEs named in each station's public lab README — CWE-916 / CWE-327 / CWE-759 / CWE-760 (Wk2 hash), CWE-347 / CWE-290 (Wk3 MAC), CWE-353 / CWE-649 / CWE-347 (Wk4 AES-CBC), CWE-347 / CWE-757 / CWE-204 (Wk6 AEAD). This is a crypto-misuse course — the READMEs give no OWASP category mapping and none is invented here. |
| **CLOs addressed** | **CLO2** break · **CLO3** rebuild · **CLO6** ethics & evidence — from the course-spec §6 schedule row for Week 9 (not the §4 "W8 written + W9 practical" combined row, which spans 1–4, 6 because it also covers the Week 8 written half). |

> **What this plan may and may not contain.** The exam questions, flag values, payloads,
> per-station solutions and the required mitigation wording live in the git-ignored instructor
> key `instructor/exams/week09-midterm-practical-ctf-answers.md` and are **not reproduced here**.
> Station identity, ports, coverage, the flag-key vocabulary and the 100-pt scoring rules are
> already public (they appear in `labs/week07-review/README.md` and each lab's tracked
> `docker-compose.yml`), so this plan states them; the "how you solve it" column is deliberately
> omitted.

---

## 1. What is assessed

The Week 9 midterm is a **hands-on capture-the-flag practical** covering **Weeks 1–6** (syllabus
§3; SUBMISSION.md exam table; AGENDA.md special-week agenda). It is the practical half of the
20% midterm component (the other half is the Week 8 written exam) and is graded **individually**
(syllabus §3).

Per the instructor key, the practical selects **four flag-bearing stations** from the pre-midterm
LAB weeks. Wk1 (Intro/threat-modelling) is CONCEPTUAL with no target; Wk5 (Key Exchanges) is
excluded by the key because its attributable artifact is the `RELAY INTERCEPTED` evidence-log
line, not a flag (see the instructor note in §5).

| # | Source week | Station (public game name) | Targets (host ports) | Flag env-var | Pts |
|---|---|---|---|---|---|
| 1 | Wk2 Hash | "Crack the Leaked DB" — recover a password from an unsalted-MD5 store | `:8094` vuln / `:8095` bcrypt-fixed | `FLAG_HASH` | 20 |
| 2 | Wk3 MACs | "Forge the Admin Cookie" — SHA-256 length-extension on a secret-prefix cookie MAC | `:8092` vuln / `:8093` HMAC-fixed | `FLAG_MACS` | 30 |
| 3 | Wk4 AES-modes | "Flip Your Way to Admin" — CBC bit-flip an unauthenticated session token | `:8096` vuln / `:8097` GCM-fixed | `FLAG_AES` | 25 |
| 4 | Wk6 AEAD | "Read the Secret Without the Key" — CBC padding-oracle plaintext recovery | `:8098` vuln / `:8099` GCM-fixed | `FLAG_AEAD` | 25 |

Ports and flag env-vars above are quoted from the four tracked `docker-compose.yml` files;
station/point weights are from the instructor key (100 pts total). The key notes the weighting
reflects relative attack complexity — length-extension (station 2) is the heaviest single
hand-computation, hash-cracking (station 1) is the most mechanical, so 30 vs 20.

> **Instructor note — station selection and weights are the instructor's per-cohort choice.**
> They are held in `instructor/exams/week09-midterm-practical-ctf-answers.md` (git-ignored). The
> `instructor/exams/item-bank.md` CTF pool ships rotation variants **M1–M4** (one per station,
> a differently-seeded target for the same concept) so the exam can be rebuilt each cohort without
> re-using the same challenge the students already solved as a weekly lab.

## 2. What the exam is testing (the through-line)

The four stations are not four unrelated tricks — they walk the pre-midterm spine stated in
`labs/week07-review/README.md`: **confidentiality, integrity and authenticity are three separate
properties, and a primitive that gives you one does not give you the others for free.** Wk2 is
storage (a fast hash is the wrong tool for passwords); Wk3 shows a keyed hash is **not** a MAC
(length-extension); Wk4 shows encryption is **not** integrity (CBC malleability); Wk6 shows what
happens when you bolt a MAC and a cipher together the wrong way (padding oracle) and how to bolt
them together right (AEAD / encrypt-then-MAC). Every station requires the student to **break** the
misused construction (CLO2) and state the **one-line fix** that closes it (CLO3) — the fixed
container on the paired port (`:8095`/`:8093`/`:8097`/`:8099`) is the evidence that the fix
actually defeats the same attack.

## 3. Prior knowledge and readiness

- **Students, before the exam:** the Week 7 review has already run the "exact format of the
  upcoming exam" mock CTF (AGENDA.md special-week agenda; `labs/week07-review/README.md` mock
  practical half). Docker Desktop working; the same host-side Python prerequisites each weekly lab
  named (e.g. `requests` on the host to run an `exploit.py`, or run it inside the `vulnerable`
  container). Bring the one-page open-note cheat sheet from Week 7 **if** the instructor permits
  open-note (that permission is ⬚ — the repo does not fix it).
- **Instructor, before the exam:** complete the infrastructure readiness and flag-seeding steps in
  §4 the day before, not at the bell. Pre-pull `python:3.12-slim` and pre-build the four stacks so
  the runtime `pip install` is not happening live (see §4 and §8).

## 4. Infrastructure readiness and per-student flag seeding

**There is no live CTFd instance for this course** (README.md status note; course-plan-19weeks.md
open item #6; SUBMISSION.md status note). Delivery is therefore **students running the four local
Docker stations on their own machines**, submitting flags + payload + one-line mitigation via the
**CTF Form / Google Classroom** (SUBMISSION.md exam table, W9 row). The local-Docker path is the
*primary* delivery, not a fallback.

**Eight host ports are in play at once** — `8092`/`8093` (Wk3), `8094`/`8095` (Wk2),
`8096`/`8097` (Wk4), `8098`/`8099` (Wk6). Confirm none collide on the exam machines during the
0:00–0:10 target check (§5).

### Per-student flag seeding — the primary route

Each of the four labs reads its flag from an environment variable with an in-code default, and
every one of the four `docker-compose.yml` files carries the same seeding comment, quoted exactly:

```
# Per-student flag: python3 ../../instructor/seed_flags.py env <STUDENT_ID> > .env
```

`instructor/seed_flags.py` **exists and is verified** — it is a thin shim (2026-07-22) to the
curriculum monorepo's `tools/seed_flags.py`, keyed by this course's own `SC_FLAG_SALT` (never
share software-security's salt). Running `seed_flags.py env <STUDENT_ID>` emits a `.env` with a
per-student `FLAG_HASH` / `FLAG_MACS` / `FLAG_AES` / `FLAG_AEAD` (plus `FLAG_SIG` / `FLAG_PQC` for
later weeks). Because each value is an HMAC of student-ID + challenge under a secret salt, a
copied flag is traceable to the student it was issued to. The **instructor** runs this (the salt
stays private) and hands each student their pre-seeded `.env`, or seeds each exam machine before
the student sits down.

> **Instructor note — the exam key's flag-seeding premise is stale; do not follow it verbatim.**
> `instructor/exams/week09-midterm-practical-ctf-answers.md` states "this course does not yet have
> an `instructor/seed_flags.py` generator … Until it exists, rotate flags for the exam manually."
> That file **does now exist** and works end-to-end (course-plan-19weeks.md open item #5 records
> `env`/`gen`/`verify` as DONE and verified). Prefer the per-student `seed_flags.py env` route
> above; the manual per-cohort commands below are the documented fallback, not the only option.
> Reported in `escalated` — the fix is in lab/instructor content, not this plan.

### Per-cohort manual rotation — documented fallback

If per-student seeding is not used, rotate a fresh per-cohort flag (and, where the key says,
the underlying secret/key so a leaked prior-cohort forgery won't validate). Quoted verbatim from
the instructor key:

```bash
cd labs/week02-hash && echo "FLAG_HASH=FLAG{hash_$(openssl rand -hex 4)}" > .env
cd labs/week03-macs && { echo "FLAG_MACS=FLAG{macs_$(openssl rand -hex 4)}"; echo "MAC_SECRET=$(openssl rand -hex 16)"; } > .env
cd labs/week04-aes-modes && { echo "FLAG_AES=FLAG{aes_$(openssl rand -hex 4)}"; echo "AES_KEY=$(openssl rand -hex 32)"; } > .env
cd labs/week06-aead && echo "FLAG_AEAD=FLAG{aead_$(openssl rand -hex 4)}" > .env
```

> **Critical ordering — seed before you stand the stack up.** Every compose file interpolates the
> flag at `up` time (`FLAG_HASH=${FLAG_HASH:-FLAG{hash_crack_me}}`). Writing `.env` **after**
> `docker compose up` silently does nothing, and every candidate captures the public default
> (`FLAG{hash_crack_me}`, `FLAG{macs_demo}`, `FLAG{aes_cbc_is_malleable}`,
> `FLAG{padding_oracle_leaks_all}`) — non-attributable, un-gradable evidence. Seed `.env` first,
> then `docker compose up -d`.

**Readiness check** (run in `instructor/`, per platform-build/README.md):

```bash
python3 check_flag_keys.py     # confirms seed_flags.py <-> .env.example agree
```

## 5. Run-of-show (150 min)

The only timings the repo fixes for Week 9 are AGENDA.md's two lines — reproduced exactly. Note
that **per-station minute budgets are ⬚** (the repo does not allocate the 140-min solve block
across the four stations); students self-manage, using the point weights in §1 as the only steer.

| Time | Block | What happens |
|---|---|---|
| 0:00–0:10 | **Rules + target check** | Read the rules of engagement (ETHICS.md — sandbox targets only); each student confirms their four local targets answer on the eight ports; no questions on solutions |
| 0:10–2:30 | **Solve challenges** | Students work the four stations in any order; capture each flag; record payload/technique + the one-line mitigation; **submit** flags/evidence + payload + mitigation via the CTF Form / Classroom before 2:30 (submission is folded into this block, not a separate timed row) |

`0:10 + 140 = 150` — the block is full; there is no spare slot inside it (see §9 on the debrief).

> **Instructor note — AGENDA vs the exam key on Wk5.** AGENDA.md's Week 9 line says students
> "submit flags (Wk2–4, 6 style) **and evidence log lines (Wk5 style)**". The instructor key
> builds **four** flag stations and **excludes Wk5** (its artifact is a log line, and the four
> stations already total 100 pts). This plan follows the four-station instrument that actually
> exists in the key. If a Wk5 evidence-log task is added back, it would use
> `docker compose -f docker-compose.vulnerable.yml up --build` (the Wk5 invocation) and capture
> the `RELAY INTERCEPTED: …` line — but that is an instructor decision, not reconciled in the
> repo. Reported in `escalated`.

## 6. Scoring

Total **100 pts** (instructor key). Per-station rules, quoted in substance from the key:

| Rule | Award |
|---|---|
| Flag captured for a station | Full points for that station (§1 weights) |
| No flag, but correct payload/technique + clear method shown, execution error blocked cash-in | Up to **60%** of the station's points |
| Partial attempt (e.g. identifies the vulnerable line but does not complete the exploit) | Up to **20%** at instructor discretion |
| **Required for full credit on each station** | The correct **one-line mitigation** stated, *in addition to* the flag |

The accepted per-station mitigation wording is in the instructor key and is **not** reproduced
here; award the mitigation credit for a correct fix even if the student names encrypt-then-MAC
rather than AEAD on the CBC stations, provided they explain why it closes the specific hole.
Per-station point weights are the instructor's per-cohort choice (§1) and may be rotated with the
item-bank M1–M4 variants.

## 7. Anti-cheating controls actually used

Split honestly into what is enforced **now** and what is the **target state** — SUBMISSION.md is
explicit that "flags are still the same placeholder value for everyone, *not* personalized or
checked against a roster … enforced manually until the personalized-flag pipeline is live."

**In force now (manual enforcement, SUBMISSION.md "Academic Integrity & Anti-Cheating"):**
- **Identity-stamped screenshots** — evidence must show the student's terminal `whoami` / login
  email / student ID **and** a timestamp; generic or borrowed screenshots are not accepted.
- **Code-similarity checks** — submitted exploit code run through **MOSS / JPlag** against
  classmates and previous cohorts.
- **Random live checks / viva** — a student may be asked to reproduce a station or explain their
  fix live; an answer they cannot explain in their own words scores zero.
- **Individual, time-limited** — the practical is individual; the block is fixed at 150 min.
- **Per-cohort secret rotation** — rotating `MAC_SECRET` (Wk3) and `AES_KEY` (Wk4) per cohort (§4)
  means a forged cookie or bit-flipped token leaked from a prior cohort will not validate, even
  though the *attack mechanism* is unchanged.

**Target state (built, not yet live end-to-end):** per-student attributable flags via
`seed_flags.py` (§4) once a CTFd instance is stood up — at which point a submitted flag reverse-
looks-up to the student it was issued to (`seed_flags.py verify`), making sharing detectable
rather than merely banned. Until then, treat the "your flags are unique to you" rule as in force
for *behaviour* (do not share evidence) and rely on the manual controls above for *enforcement*.

## 8. Contingency (if the local platform fails)

Framed around the real failure modes of this tooling, since there is no CTFd to go down:

| Risk | Mitigation |
|---|---|
| Slow/failed image pull or the runtime `pip install --no-cache-dir -r requirements.txt` on four stacks at the bell — a local pip cache does **not** help (`--no-cache-dir`) | Pre-pull `python:3.12-slim` and pre-build/stand up all four stations the day before; keep a USB copy (`docker save`/`docker load`); if a build is mid-run at 0:10, extend the target-check window rather than the solve window |
| One of the eight host ports (`8092`–`8099`) already bound on an exam machine | Remap the **host** side of the port mapping in that lab's `docker-compose.yml` (the left of `"8096:8096"`, etc.); note the container apps hard-code their internal port, so change only the host side, and point any `exploit.py` at the new host port via the `*_PORT`/`*_HOST` env vars it reads |
| `.env` seeded after `docker compose up`, so every student captures the public default flag | Re-seed `.env` and `docker compose up -d --force-recreate` for the affected station; the identity-stamped screenshot + viva (§7) is the backstop for attribution that session |
| Runtime error prevents a student cashing in a flag they clearly derived | Scoring rule in §6 awards up to 60% for correct technique + method shown without cash-in; capture the payload/screenshot on paper/PDF and grade the mechanism |
| Whole-room Docker failure on institutional machines | Fall back to paper capture — students record payload + derived flag/technique + one-line mitigation for each station on the exam PDF; grade the mechanism per §6; do not extend the block beyond the fixed 150 min |

## 9. Debrief

> **The 150-min budget contains no debrief slot — debrief timing is ⬚.** AGENDA.md's Week 9 line
> is `0:00–0:10 rules + target check` + `0:10–2:30 solve` = the full 150 min. The scheduled
> "Debrief: common mistakes + exam logistics" is in **Week 7** (the pre-midterm review week,
> AGENDA.md special-week agenda), **before** this exam — not after it. No post-exam debrief is
> scheduled in the repo; run the debrief below in a later session or asynchronously (Classroom).

Debrief content to cover (not scheduled inside the exam block):
- **The through-line, restated** (§2): confidentiality ≠ integrity ≠ authenticity — which station
  taught which, and where students conflated them.
- **The fixed-container evidence** — for each station, the paired fixed port (`:8095`/`:8093`/
  `:8097`/`:8099`) defeats the same attack; students who captured a flag but could not state *why*
  the fix works lost the mitigation credit (§6) and should see it demonstrated.
- **Common execution stalls** — e.g. seeding `.env` after `up`; byte-indexing on the CBC flip;
  glue-padding length on the length-extension station. Keep these at the *symptom* level; solution
  detail stays in the instructor key.
- **Integrity outcomes** — how the identity-stamp / MOSS-JPlag / viva controls (§7) resolved, if
  any submission was flagged.
- **Feed-forward** — the same break-then-rebuild rhythm returns after the midterm (Wk10 onward);
  the Week 17 review + Week 19 final CTF are cumulative.

## 10. Post-exam reflection

*Complete after the session — this also feeds the course's engagement data.*

- Attendance / completion, and how many of the four stations the median student cashed in: ⬚
- Whether the 140-min solve block was enough / too much for four stations (no per-station budget
  is set in the repo — this run establishes the first data point): ⬚
- Infrastructure incidents (image pull, `pip install`, port collisions, `.env`-ordering mishaps): ⬚
- Whether flags were per-student-seeded, per-cohort-rotated, or left at default this offering: ⬚
- Any integrity flag raised by the identity-stamp / similarity / viva controls: ⬚
- Whether the Wk5 evidence-log task (AGENDA line) should be added for the next offering, or the
  four-station instrument kept: ⬚
- Anything to change before this exam runs again: ⬚
