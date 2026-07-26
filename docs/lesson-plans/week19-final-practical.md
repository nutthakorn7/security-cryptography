# Lesson Plan — Week 19: Final — Practical (Capstone CTF + CryptoVault demos)

| | |
|---|---|
| **Course** | Security & Cryptography (`21025117`, syllabus.md §header) |
| **Week / date** | 19 · ⬚ |
| **Week kind** | Exam — practical. No lecture, no lab, no weekly quiz. **Two graded instruments run back-to-back in one block**: the capstone CTF (final component) and the graded CryptoVault project demos (project component). |
| **Contact time** | 240 min single block (AGENDA.md per-week table, Wk19: Exam = 240, Total = 240; special-week agenda "Week 19 — Final CTF + project demos (240 min)"). The standard 300-min lecture+lab split does **not** apply to exam weeks. |
| **Lab folder** | `⬚ (instructor-held)` — course-spec §6, Wk19 row. There is **no** `labs/week19-final-practical/` directory in the repo; the CTF re-uses the already-built Wk11–Wk15 lab targets (see §1), and the demo half is graded from `project/`. |
| **Slides** | ⬚ (no `slides/week19.md`; exam week has no deck) |
| **Standards** | Analogous CWEs named on each station lab's public README: CWE-347 / CWE-345 (Wk11 signatures), CWE-295 / CWE-300 (Wk12 transport), CWE-311 / CWE-319 (Wk13 E2EE), CWE-522 / CWE-319 / CWE-532 (Wk14 authentication), CWE-323 / CWE-347 (Wk15 PQC). This is a crypto-misuse course — the READMEs give no OWASP category mapping and none is invented here. |
| **CLOs addressed** | **CLO2** break · **CLO3** rebuild · **CLO5** evaluate & communicate · **CLO6** ethics & evidence — from the course-spec §6 schedule row for Week 19 (not the §4 "W18 written + W19 practical" combined row, which marks all six CLOs because it also covers the Week 18 written half). |

> **What this plan may and may not contain.** Station solutions, payloads, flag values, the exact
> capture strings and the accepted mitigation wording live in the git-ignored instructor key
> `instructor/exams/week19-final-ctf-capstone-answers.md` and are **not reproduced here**. Station
> identity, ports, run commands and station coverage are already public (they
> appear in each lab's tracked `README.md` / `docker-compose*.yml`, in `AGENDA.md` and in
> `labs/week17-review/mock-ctf.md`), so this plan states them; the "how you solve it" column is
> deliberately omitted. The repository is public — treat every line below as student-readable.

---

## 1. What is assessed

Week 19 is the **practical half of the 25% Final** component (syllabus §3: "Final — Week 18
written *(individual)* + Week 19 capstone CTF *(team)*"; course-spec §4). It is **team-graded**,
and it is the one exam item in the course that is not individual — the syllabus bounds team weight
deliberately ("Team work is bounded (project 15% + the Week 19 capstone CTF)").

Two distinct instruments run in the same 240-min block and are **graded on separate scales**:

**(a) Capstone CTF — 150 pts.** Per the instructor key, five timed stations drawn from the
post-midterm lab arc. Week 10 is CONCEPTUAL with no target and is **not** run as a timed station —
the key is explicit that including it would mean inventing a flag the course has refused to fake
(`labs/week10-hybrid-encryption/README.md`, "Why no lab target this week"); its Audit-the-AI
artefact is credited as an optional, pre-submitted Station 0 instead.

| # | Source week | Station (public signature game) | Capture type | Target(s) | Key/artefact | Pts | Key's budget |
|---|---|---|---|---|---|---|---|
| 0 *(optional)* | Wk10 Hybrid Encryption | 🔬 "Nonce Detective" — Audit-the-AI | Audit proof, **submitted pre-exam, not timed** | none | Worksheet 10 rubric | — | — |
| 1 | Wk11 Signatures & ZKP | 💰 "Double-Spend the Bank" | **Flag capture** | `:8102` vuln / `:8103` fixed (published) | `FLAG_SIG` | 30 | 20 min |
| 2 | Wk12 Secure Transport | 🎭 "The Impostor's Certificate" | **Evidence artefact** (log line) | `:8443` compose-internal | `MITM INTERCEPTED:` line | 30 | 20 min |
| 3 | Wk13 End-to-End Encryption | 👀 "Who's Reading Your Mail?" | **Evidence artefact** (log line) | `:8080` compose-internal | `SERVER SAW:` line | 30 | 20 min |
| 4 | Wk14 Authentication | 🗝️ "Never Say the Password" | **Evidence artefact** (log line) | `:8080` compose-internal | `SERVER SAW PASSWORD:` line | 30 | 20 min |
| 5 | Wk15 PQC | 🔑 "Forge the Admin Signature" | **Flag capture** | `:8100` vuln / `:8101` fixed (published) | `FLAG_PQC` | 30 | 20 min |

Ports and flag env-vars are quoted from the tracked compose files
(`labs/week11-signatures-zkp/docker-compose.yml`, `labs/week15-pqc/docker-compose.yml`,
`labs/week12-secure-transport/docker-compose.vulnerable.yml`,
`labs/week13-e2e-encryption/docker-compose.vulnerable.yml`,
`labs/week14-authentication/docker-compose.vulnerable.yml`); station points, the 20-min budgets and
the station selection are from the instructor key. **Only stations 1 and 5 publish host ports** —
stations 2–4 publish none, so their capture comes out of `docker compose … logs`, not a browser.
Only two of this course's six `seed_flags.py` challenge keys (`sig`, `pqc`) are in play this week
(`instructor/exams/item-bank.md`, Wk19 pool note).

**(b) Graded CryptoVault final demo.** Each team gives a **10-min demo + 5-min Q&A**
(AGENDA.md Week 19 block). It is graded against the **100-pt rubric in `project/README.md`** —
the term project's 15% component, with marks scaled per member by the peer-contribution
evaluation (typically ×0.8–1.1). The Week 19 deliverables due here are the final demo, the
self-audit and the crypto-agility note (`project/README.md` timeline). The demo mark is **not**
folded into the 150-pt CTF total; the instructor key says so explicitly.

> **Instructor note — three repo sources disagree on what the Week 19 CTF covers; this plan
> follows the instrument that actually exists.** AGENDA.md's Week 19 line says the tournament runs
> "LAB + Wk11 flags, plus Wk5/12/13/14 evidence lines, cumulative" (i.e. it implies Wk2/3/4/6
> flags and a Wk5 station); `labs/week17-review/README.md` promises the final draws from Wk10–16
> "plus one first-half callback challenge"; and `labs/week17-review/mock-ctf.md` — billed as "the
> same format as the Week 19 final practical" — runs **eleven** challenges (six post-midterm plus a
> five-item Wk2–6 callback round). The instructor key builds **five** stations (Wk11–15), with no
> Wk5 and no first-half callback. Follow the key: it is the exam instrument, and 5 × 30 = the
> stated 150-pt total. Students who prepared on the mock will expect a callback round — say in
> Week 17's debrief which shape the real exam takes. Reported in `escalated`; the reconciliation
> belongs in lab/AGENDA content, not in this plan.

## 2. What the exam is testing (the through-line)

The five stations walk the post-midterm spine stated in `labs/week17-review/README.md`, and the
sentence students should be able to say out loud is the one `mock-ctf.md` puts at the end of its
warm-up: **confidentiality, integrity and authenticity are three separate properties — nearly
every challenge here is a system that bought one and assumed it got the others for free.**

- **Wk11** — a signature proves *authenticity*, not *uniqueness*; ECDSA's `(r, s)` has a valid twin,
  so an identity derived from the signature is malleable. Fix: low-S / BIP-62 normalisation.
- **Wk12** — "the traffic is encrypted" ≠ "encrypted to the right party"; the guarantee comes from
  certificate validation against a trusted chain, not from the handshake.
- **Wk13** — transport encryption still leaves the **server inside the trust boundary**; only
  client-side encryption removes it.
- **Wk14** — sending a password over TLS still hands the plaintext to the server; challenge-response
  proves knowledge without transmitting the secret.
- **Wk15** — a one-time key is only quantum-resistant if it is used exactly once; reuse leaks enough
  private-key bits to forge.

Every station requires the team to **break** the misused construction (CLO2) *and* state the
one-line mitigation (CLO3) — the paired fixed mode (`:8103`, `:8101`, or `docker-compose.fixed.yml`)
is the evidence that the fix actually defeats the same attack. The demo half carries CLO3 and CLO5:
the team must explain, live and under questioning, why each primitive in their own build is the
right one (`project/README.md`, self-audit and "End-to-end composition" criteria).

## 3. Prior knowledge and readiness

- **Students have had two dry runs.** The Week 16 capstone studio block includes a "Practice CTF
  tournament (previews Week 19)" (2:15–4:45), and Week 17 runs the mock final —
  `labs/week17-review/mock-ctf.md`, "**Format:** same as the Week 19 final practical · **Ungraded**
  (participation) · **Time:** ~165 min · teams · **sandbox targets only**", with hints and
  self-check pointers and no flags printed.
- **Students, before the exam:** Docker Desktop working; teams (2–3, the CryptoVault teams) fixed;
  host-side Python able to run `python exploit.py` for the two flag stations, or run it inside the
  `vulnerable` container. Whether the exam is open-note is ⬚ — the repo does not fix it.
- **Students, before the exam (demo half):** demo, self-audit and crypto-agility note ready per
  `project/README.md`; the write-up uses `project/REPORT-TEMPLATE.md`.
- **Instructor, before the exam:** run the whole of §4 the day before, not at the bell. Three of the
  five stations (`week12`, `week13`, `week14`) are `build: .` images, not pulls — they build a
  `python:3.12-slim` layer and `pip install --no-cache-dir -r requirements.txt`
  (`cryptography>=48.0.1`, Flask, requests) at first `up --build`.
- **Rules of engagement:** [ETHICS.md](../../ETHICS.md) — the provided sandbox targets only. The
  mock CTF states the same constraint, and Week 1 has the signed acknowledgement on file.

> **Instructor note — SUBMISSION.md misdirects students on the report due this week.** Its term-
> project section still says the fill-in report template "is **not yet built** for this course …
> until it exists, structure your write-up around that README's deliverables list".
> `project/REPORT-TEMPLATE.md` **does** exist and `project/README.md` §Report points to it as the
> thing to use. Tell students in Week 17 to use the template; do not let the stale instruction
> stand into the graded submission. Reported in `escalated`.

## 4. Infrastructure readiness and per-student flag seeding

**There is no live CTFd instance for this course** (README.md status note; SUBMISSION.md status
note; course-plan-19weeks.md open item #6 — "no live server, no `challenges-import.csv`
image/point-value catalog, and no challenge host provisioned"). Delivery is therefore **teams
running the station stacks locally in Docker**, submitting flags/evidence via the **Form /
Classroom** (SUBMISSION.md exam table, W19 row: "flags/evidence via Form; live CryptoVault project
demo (graded by rubric)"). The local-Docker path is the *primary* delivery, not a fallback.

**Only four host ports are in play** — `8100`/`8101` (Wk15) and `8102`/`8103` (Wk11). The Wk12,
Wk13 and Wk14 stacks publish no host ports at all (their `:8443` / `:8080` are compose-internal),
so they cannot collide, but they also cannot be checked with a browser — check them with
`docker compose … logs`.

### Per-student flag seeding — the primary route

Both flag-bearing labs read their flag from an environment variable with an in-code default, and
both `docker-compose.yml` files carry the same seeding comment, quoted exactly:

```
# Per-student flag: python3 ../../instructor/seed_flags.py env <STUDENT_ID> > .env
```

`instructor/seed_flags.py` **exists and is verified end-to-end** — `env`/`gen`/`verify` all tested,
correct flag format, no collisions across students, wrong salt correctly rejected
(course-plan-19weeks.md, resolved item #5). Because each value is an HMAC of student-ID +
challenge under this course's own private salt, a copied flag is traceable to the student it was
issued to (`seed_flags.py verify`). The **instructor** runs this and hands each team member their
pre-seeded `.env`, or seeds each exam machine before the students sit down.

> **Instructor note — three station documents are stale on this point; do not follow them
> verbatim.** `labs/week15-pqc/docker-compose.yml` continues the seeding comment with "(once this
> course's seed_flags.py exists; until then FLAG_PQC defaults below)"; both flag-bearing labs'
> READMEs repeat the same "once this course's `instructor/seed_flags.py` exists" caveat (Wk15's
> even directs the reader to add a `"pqc"` entry to the *sibling* course's `CHALLENGES` list); and
> the Week 19 key says "Without it, every station falls back to its documented default flag".
> `seed_flags.py` **does** now exist, carries `pqc` and `sig` in its own `CHALLENGES` list, and is
> verified. Prefer the per-student route; hand-rotation below is the documented fallback, not the
> only option. Reported in `escalated` — the fix is in lab/instructor content, not this plan.

> **Critical ordering — seed before you stand the stack up.** Both compose files interpolate the
> flag at `up` time (`FLAG_SIG=${FLAG_SIG:-…}`, `FLAG_PQC=${FLAG_PQC:-…}`). Writing `.env` **after**
> `docker compose up` silently does nothing and every team captures the in-repo default value,
> which is printed in the tracked compose file and therefore known to anyone with the repo —
> non-attributable, un-gradable evidence. Seed `.env` first, then `docker compose up -d`.

### Per-cohort rotation — the fallback, and the only control on stations 2–4

Stations 2, 3 and 4 have **no `FLAG_*` at all**. Their capture strings are plain environment values
set in the tracked compose files (`SECRET_MESSAGE` in `week12`/`week13`, `PASSWORD` in `week14`) —
identical for every team, and published in the repo. The key's repeat-cohort note is the control:
rotate those three secret strings, and the two `FLAG_*` defaults, **by hand between cohorts**, so
answers cannot be passed down verbatim term to term. See §7 for what this does and does not buy.

### Readiness checks (run the day before)

Drift guard, run in `instructor/` (per `instructor/platform-build/README.md`):

```bash
python3 check_flag_keys.py     # confirms seed_flags.py <-> .env.example agree
```

Then stand each station up once, exactly as the student will, and tear it down again. Commands
quoted verbatim from each lab's README:

| Station | Stand up (vulnerable) | Fixed mode | Tear down |
|---|---|---|---|
| 1 · Wk11 | `docker compose up -d`, then `pip install ecdsa requests` (once, on the host), then `python exploit.py` | same stack — `fixed_app.py` is already on `:8103` | ⬚ (that README states no teardown command) |
| 2 · Wk12 | `docker compose -f docker-compose.vulnerable.yml up --build` | `docker compose -f docker-compose.fixed.yml up --build` | `docker compose -f docker-compose.vulnerable.yml down -v` |
| 3 · Wk13 | `docker compose -f docker-compose.vulnerable.yml up --build` | `docker compose -f docker-compose.fixed.yml up --build` | `docker compose -f docker-compose.vulnerable.yml down` |
| 4 · Wk14 | `docker compose -f docker-compose.vulnerable.yml up --build --abort-on-container-exit` | `docker compose -f docker-compose.fixed.yml up --build --abort-on-container-exit` | `docker compose -f docker-compose.vulnerable.yml down` |
| 5 · Wk15 | `docker compose up -d`, then `python exploit.py` | same stack — `fixed_app.py` is already on `:8101` | ⬚ (that README states no teardown command) |

A green pre-flight looks like: `exploit.py` exits `0` with two `PASS` lines on stations 1 and 5
(README "Verified" sections); station 2's fixed run gives
`docker compose -f docker-compose.fixed.yml logs | grep -c "MITM INTERCEPTED"` → `0`; station 4's
fixed run gives `docker compose -f docker-compose.fixed.yml logs | grep -c "SERVER SAW PASSWORD"`
→ `0` while `LOGIN OK` is still present; station 3's fixed run gives `0` for the plaintext string on
the **server** log while Bob still decrypts it. Tear every stack down (`-v` on Wk12) before the exam
so no stale `certs` volume or in-container history survives into the graded run.

## 5. Run-of-show (240 min)

The repo fixes two blocks for Week 19 — AGENDA.md's special-week agenda, reproduced exactly — plus
the instructor key's per-station budget. Both are shown; where they do not reconcile, it is said so
rather than smoothed over.

| Time | Block | What happens |
|---|---|---|
| 0:00–2:30 | **Capstone CTF tournament** | Teams work the five stations; capture the flag or the evidence line, record payload/technique **and** the one-line mitigation for each; submit flags/evidence via the Form/Classroom before 2:30 |
| 2:30–4:00 | **Graded final CryptoVault project demos** | 10-min demo + 5-min Q&A per team, graded on the `project/README.md` rubric |

**Inside the CTF block.** The key allocates **20 min per station**: "5 timed stations × 20 min +
transitions ≈ 120 min CTF block", and adds "Adjust timing to your section's actual headcount — same
instructor discretion as the sibling key." AGENDA gives the block **150 min**. The ~30-min
difference is **⬚ — the repo does not allocate it**. Nothing in the repo defines a rules /
target-check row for Week 19 either (Week 9's agenda line has an explicit `0:00–0:10 rules + target
check`; Week 19's does not). Both are instructor decisions on the day; do not present either as a
published rule to students.

> **Instructor note — the demo half does not fit a normal cohort, and the arithmetic is the
> repo's, not this plan's.** 90 min ÷ (10-min demo + 5-min Q&A) = **6 team slots**. Teams are 2–3
> students (`project/README.md`; syllabus §3) and AGENDA.md states this course's scale as N≈80–120,
> i.e. roughly 27–60 teams. Six slots cannot absorb that. The key's own escape hatch is "adjust
> timing to your section's actual headcount"; realistic options are parallel demo rooms with a
> second assessor, or scheduling demos outside this block against the same rubric. **Do not solve
> it by shortening the CTF block or by trimming the published 10+5 demo format** — both are graded
> instruments. Reported in `escalated`; the fix belongs in AGENDA/project content.

## 6. Scoring

**CTF — the point scheme lives in the instructor key, not here.** This repository is public, so
this plan does not reproduce per-station point values, the partial-credit threshold, or any bonus
amounts. Open the key alongside this plan and fill in ⬚ below before the sitting.

| Rule | Award |
|---|---|
| Flag captured, or correct evidence line **plus identity proof**, for a station | ⬚ (key) |
| Correct method demonstrated without a valid capture (right exploit reasoning, mistimed run) | ⬚ partial credit (key) |
| **Required for full credit on each station** | The correct **one-line mitigation**, *in addition to* the capture |
| Optional first-blood bonus | ⬚ (key) |
| Station 0 (Wk10 audit proof, if run as a pre-submitted station) | Graded on the existing Worksheet 10 rubric — **not** scored again here; do not double-count |

The accepted per-station mitigation wording is in the instructor key and is **not** reproduced here.
`AGENDA.md` does publish the sibling midterm CTF's 150-point total, so students already know the
order of magnitude; the per-station split is what stays private.

**Demo — graded separately** on `project/README.md`'s own **100-pt** rubric (KDF 13 · AEAD-at-rest
15 · key exchange/wrapping 15 · signatures 15 · transport 12 · end-to-end composition 20 · demo &
report clarity 10) — that rubric is already published to students — with the crypto-agility note as
a **+5 bonus capped so the total cannot exceed 100**, and each member's mark scaled by the
peer-contribution evaluation. Do not fold it into the CTF total.

The two instruments feed **different course components**: the CTF into the 25% Final (with the
Week 18 written half), the demo into the 15% CryptoVault project (syllabus §3; course-spec §4).

> **Instructor note — the item bank assumes a CTFd that does not exist.** The bank's scoring
> assumptions (dynamic decay for early solves, a first-blood bonus) and its rotation-variant
> pricing are instructor-side and are deliberately not restated in this public file. Operationally:
> with no live CTFd there is no decay, so run the key's flat scheme with any bonus awarded by hand,
> and if you substitute a rotation variant for a station, re-price it to the station it replaces
> rather than mixing two scales.

## 7. Anti-cheating controls actually used

Split honestly into what is enforced **now** and what is the **target state** — SUBMISSION.md is
explicit that "flags are still the same placeholder value for everyone, *not* personalized or
checked against a roster … enforced manually until the personalized-flag pipeline is live"
(quoted verbatim; the repo's own spelling).

**In force now (manual enforcement, SUBMISSION.md "Academic Integrity & Anti-Cheating"):**

- **Identity-stamped evidence** — the submission must show the student's terminal `whoami` / login
  email / student ID **and** a timestamp. The key requires the exact log line **plus** identity
  proof for stations 2–4.
- **Code-similarity checks** — submitted exploit code through **MOSS / JPlag** against classmates
  and previous cohorts.
- **Random live checks / viva** — a team may be asked to reproduce a station or explain a fix live;
  an answer they cannot explain in their own words scores zero. On the demo half the 5-min Q&A
  *is* the live check, and commit history corroborates who did what (`project/README.md`,
  peer-contribution section).
- **Per-cohort rotation** — rotate the two `FLAG_*` defaults and the three station-2/3/4 secret
  strings by hand between cohorts (key, "Notes for repeat cohorts"), so a prior cohort's captures
  do not validate.
- **Separate stacks per team where sections are large** — the key: duplicate the compose stacks on
  alternate host ports rather than running several teams against one shared container, because the
  Wk11 and Wk15 stations are **stateful** (withdrawal / signature history persists in-container
  until torn down), so one team's run can both corrupt and reveal another's.

**Two limits specific to this exam — plan around them, do not overstate them:**

1. **Stations 2–4 produce a constant.** Their "personalized/attributable evidence artifact" (the
   labs' own words) is a
   log line whose content is fixed in the tracked compose file — the same string for every team in
   the cohort. Attribution rests entirely on the identity proof and the viva, not on the artefact's
   value. Per-cohort rotation makes it non-transferable *between terms*, not *between teams*.
2. **The exploit scripts for stations 1 and 5 ship publicly in the lab directories.**
   `labs/week11-signatures-zkp/exploit.py` and `labs/week15-pqc/exploit.py` are tracked, and each
   prints `PASS` and the captured flag. A team can cash both flag stations with one command. The
   counters that actually bite are the **mandatory one-line mitigation** (§6), the **viva**, and
   substituting an item-bank rotation variant (F1/F2 — "a differently-seeded target for the same
   concept") so the shipped script does not solve the graded target.

**Target state (built, not yet live end-to-end):** per-student attributable flags via
`seed_flags.py` (§4) once a CTFd instance is stood up, at which point a submitted flag
reverse-looks-up to the student it was issued to. Until then, treat "your flags are unique to you"
as in force for *behaviour* and rely on the manual controls above for *enforcement*.

## 8. Contingency (if the platform fails)

Framed around the real failure modes of this tooling, since there is no CTFd to go down.

| Risk | Mitigation |
|---|---|
| Three of the five stations build images rather than pulling (`week12`/`week13`/`week14` Dockerfiles, `pip install --no-cache-dir -r requirements.txt` incl. `cryptography>=48.0.1`) — building at the bell costs the CTF block; a local pip cache does **not** help (`--no-cache-dir`) | Pre-build all five stacks the day before (§4) and keep the images on the exam machines; keep a USB copy (`docker save`/`docker load`); if a build is mid-run when the block opens, extend the target-check window, not the solve window |
| Host port `8100`–`8103` already bound on an exam machine (only stations 1 and 5 publish ports) | Remap the **host** side of the mapping in that lab's `docker-compose.yml`; the container apps hard-code their internal port, so change only the host side, and point `exploit.py` at the new host/port via the env vars it reads — `VULN_HOST`/`FIXED_HOST` are shown in the Wk11 README's throwaway-container invocation, `FIXED_PORT` in the Wk15 README's verification note |
| `.env` seeded after `docker compose up`, so every team captures the in-repo default flag | Re-seed `.env` and `docker compose up -d --force-recreate` for that station; identity-stamped evidence + viva (§7) is the attribution backstop for that session |
| Stale `certs` volume from the term's Wk12 run, or leftover in-container state on the stateful Wk11/Wk15 stations, contaminating the graded run | Tear the Wk12 stack down with `docker compose -f docker-compose.vulnerable.yml down -v` before the exam (`gen_certs` must then complete — `service_completed_successfully` — before `bob`/`mitm`/`alice` start); for Wk11/Wk15 the READMEs state no teardown command (⬚), so recreate them with `docker compose up -d --force-recreate` between cohorts and between teams sharing a machine |
| A well-meant dependency bump before the exam — `labs/week11-signatures-zkp/requirements.txt` pins the unfixable `ecdsa` advisory (CVE-2024-23342, side channels declared out of scope upstream) as a **documented accepted risk** | Do **not** "fix" it during exam prep. The pure-Python `ecdsa` implementation is what makes station 1's malleability demonstration legible; replacing or pinning it away breaks the station (course-spec §10; that lab's `requirements.txt` and README) |
| A team clearly derived a capture but a runtime error blocked the cash-in | The §6 rule awards up to 60% for correct technique with method shown; capture the payload/screenshot to PDF and grade the mechanism |
| The Form/Classroom submission path fails (it is the single submission channel — there is no CTFd scoreboard to fall back to) | Fall back to paper/PDF capture — flag or log line + payload/technique + one-line mitigation per station, collected at the end of the block; grade the mechanism per §6 |
| Whole-room Docker failure on institutional machines | Paper capture as above; do not extend the block beyond the fixed 240 min, and protect the 2:30–4:00 demo half — it is a different graded component |
| A team's CryptoVault build will not run at demo time | Grade against the rubric from the self-audit + design doc + report (`project/REPORT-TEMPLATE.md`), which carry the composition and clarity criteria; a non-running build loses demo credit, not the whole rubric |

## 9. Debrief

> **The 240-min budget contains no debrief slot — post-exam debrief timing is ⬚.** AGENDA.md's
> Week 19 agenda is `0:00–2:30` CTF + `2:30–4:00` demos = the full 240 min. The scheduled "Debrief:
> common mistakes + exam logistics" sits in **Week 17** (the pre-final review week), **before** this
> exam. No post-exam debrief is scheduled in the repo; run the content below asynchronously
> (Classroom) or in a later session, and note it is the last teaching contact of the term.

Debrief content to cover (not scheduled inside the exam block):

- **The through-line, restated** (§2) — which station taught which of confidentiality / integrity /
  authenticity, and where teams conflated them.
- **The fixed-mode evidence** — for each station, the paired fixed mode defeats the same attack;
  teams that captured but could not say *why* the fix works lost the mitigation credit (§6) and
  should see it demonstrated.
- **Common execution stalls, at symptom level only** — e.g. seeding `.env` after `up`; checking a
  compose-internal station in a browser instead of the logs; tearing down without `-v` on Wk12.
  Solution detail stays in the instructor key.
- **Integrity outcomes** — how the identity-stamp / MOSS-JPlag / viva controls (§7) resolved, if any
  submission was flagged, and whether the constant-artefact limitation on stations 2–4 caused a
  dispute.
- **Project feedback** — rubric results, the peer-contribution scaling outcome, and whether the
  crypto-agility stretch note was attempted (+5, capped at 100).
- **Feed-forward** — this is where the break-then-rebuild rhythm lands: the same failure modes the
  labs planted are the ones the teams had to design out of their own build.

## 10. Post-exam reflection

*Complete after the session — this also feeds the course's engagement data.*

- Attendance / completion, and how many of the five stations the median team cashed in: ⬚
- Whether 20 min per station held, and what the unallocated ~30 min in the 150-min block was
  actually used for: ⬚
- How the demo half was actually run given the 6-slot arithmetic (parallel rooms? scheduled
  outside the block?), and whether every team was assessed: ⬚
- Infrastructure incidents (image builds, port collisions, `.env`-ordering, stale `certs` volume,
  stateful-container interference between teams): ⬚
- Whether flags were per-student-seeded, per-cohort-rotated, or left at the in-repo default this
  offering, and whether the three station-2/3/4 secret strings were rotated: ⬚
- Whether any team simply ran the shipped `exploit.py` on stations 1 and 5, and whether the
  mitigation requirement / viva caught it: ⬚
- Whether the AGENDA-vs-key coverage divergence (§1) confused students who prepared on the
  11-challenge mock: ⬚
- Whether to substitute the item-bank rotation variants (F1/F2) for the shipped stations next
  offering: ⬚
- Anything to change before this exam runs again: ⬚
