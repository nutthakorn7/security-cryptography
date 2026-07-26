# Lesson Plan — Week 14: User Authentication (The Server Sees Your Password — Unless It Can't)

| | |
|---|---|
| **Course** | Security & Cryptography (⬚ course code in [course-specification.md](../course-specification.md) §1; [syllabus.md](../../syllabus.md) records `21025117` — reconcile the two before print) |
| **Week / date** | 14 · ⬚ |
| **Week kind** | **HYBRID** — a runnable password-sent-vs-never-sent demo plus material that stays theoretical (authentication factors, TOTP vs FIDO2, credential stuffing, SSO/OAuth, and the two properties a real PAKE adds) |
| **Contact time** | 300 min = 120 lecture + 180 laboratory |
| **Lab folder** | `labs/week14-authentication` |
| **Slides** | `slides/week14.md` (Marp deck, complete — 18 slides with speaker notes). **The lab README says this deck is "*not yet written*" — that line is stale; see the instructor note in §5.** |
| **Signature game** | 🗝️ "Never Say the Password" |
| **Standards** | Analogous CWE (per lab README): CWE-522 (Insufficiently Protected Credentials) · CWE-319 (Cleartext Transmission of Sensitive Information — *to the endpoint*, even when the wire itself is TLS) · CWE-532 (Insertion of Sensitive Information into Log File). References named by the lab: NIST SP 800-63B · OWASP Authentication and Credential Stuffing Prevention Cheat Sheets · RFC 2945 (SRP) and `draft-irtf-cfrg-opaque` · W3C WebAuthn Level 2 · RFC 6238 (TOTP) |
| **CLOs addressed** | **CLO1** select & justify · **CLO4** protocol reasoning — the schedule row in [`course-specification.md`](../course-specification.md) §6. Worksheet 14 additionally carries the demonstration task (CLO2), the *Audit the AI* / EiPE / *Prompt Problem* parts (CLO5) and *Evidence & Integrity* (CLO6) that §4 of the same document maps to those outcomes — see §6 below. |

---

## 1. Session objectives

By the end of this week a student can:

**Knowledge (K)**
- K1 — Explain why sending a password to the server is a risk **even over TLS**: TLS protects the network path, but the server *terminates* the TLS and therefore holds the plaintext in a request handler — free to log it, store it, forward it, or lose it in a breach.
- K2 — Trace a challenge-response login (fresh nonce → proof computed locally → server recomputes from a stored verifier and compares) and state exactly what travels on the wire in each of the two modes.
- K3 — State the honest limits of this week's fixed demo: it proves **one** property, "the password is never transmitted." A real PAKE (SRP, OPAQUE) adds two more — offline-dictionary resistance on the stored verifier, and mutual authentication.
- K4 — Distinguish the three authentication factors (know / have / are), explain why a TOTP code is phishable while a FIDO2/WebAuthn credential is not, what credential stuffing is and why MFA blunts it, and what delegated authentication (SSO/OAuth) buys and concentrates. **None of this half has a runnable counterpart this week** — it is examined in Worksheet Part 1 and Part 2c.

**Skills (P)** — P1–P3 are produced by running the demo; P4–P6 are written analysis with no runnable counterpart.
- P1 — Execute the vulnerable topology and capture the evidence line `SERVER SAW PASSWORD: correct-horse-battery`, together with `LOGIN OK` from the client.
- P2 — Execute the fixed topology and capture *all* of: a `SERVER SAW: nonce=... proof=...` line, `LOGIN OK`, and the **absence** of any `SERVER SAW PASSWORD` line — confirmed by two `grep -c` commands that both print `0`, run **before** the stack is torn down.
- P3 — State in one line which service printed the password and why, and what the client sent *instead* of the password in fixed mode — including why a recorded nonce+proof cannot be replayed tomorrow (Worksheet Part 2a).
- P4 — Name the flaw in the AI-written Flask login handler, point at lines `(A)` and `(B)`, say what leaks to whom, and rewrite the two logging lines so the handler stays debuggable (Worksheet Part 2b — written **in the worksheet**, not as a code commit).
- P5 — Explain "proving you know a secret without revealing it" in plain English to someone who has never taken a crypto course, and name one thing a real PAKE protects against that this demo does not (Worksheet Part 2c).
- P6 — Critique an AI answer on password-free login against the four checks in Worksheet Part 2d, quoting the sentences that are correct, hand-waved or wrong.

**Attitude (A)**
- A1 — Run only the Docker targets supplied in `labs/`, under [ETHICS.md](../../ETHICS.md).
- A2 — Submit evidence stamped with their own identity (`whoami` / login email / student ID + timestamp) and be able to reproduce the captured lines live at a viva spot-check.
- A3 — Treat a confident AI login handler — or a confident AI explanation of PAKE — as something to check against a mechanism, not to trust.

## 2. Key ideas (the through-line)

Week 13 asked whether the server has to be able to read your *messages*; this week asks whether it
has to learn your *credential*. The answer is the same shape: shrink what the "trusted" server
structurally holds. Almost every login form on earth hands the server the plaintext password and
calls it secure because the page is HTTPS — but TLS solved the eavesdropper-on-the-wire problem,
and says nothing about what the endpoint does with the plaintext once it has decrypted it. A
challenge-response protocol removes that trust: the server issues a fresh random nonce, the client
combines it with the password **locally** into a proof, and the server checks the proof against a
verifier `v = KDF(salt, password)` it can store without ever holding the plaintext. Same successful
login; nothing to harvest. The discipline this week is as much epistemic as cryptographic — the
fixed side's evidence is an *absence*, and an absence is exactly the kind of evidence a student can
produce accidentally (see §5).

Two forward links worth naming in class:
- [AGENDA.md](../../AGENDA.md) puts "Wk5/12/13/14 evidence-log-line tasks" in **both** the Week 17
  mock CTF and the Week 19 capstone CTF. The evidence discipline practised today is examined twice
  more.
- Week 14 is a **CryptoVault milestone week**: the project timeline in
  [`project/README.md`](../../project/README.md) lists *"TLS/transport wired in + self-audit
  drafted"* as due in Week 14. Today's honest-scope discussion — naming precisely which property a
  construction does and does not give you — is the self-audit habit that milestone wants.

## 3. Prior knowledge and preparation

- **Students, before class:** Docker Desktop working; skim the Week 2 password-hashing recap — the
  lab README asks for this explicitly, because you reuse "store a verifier, never the password."
- **Prerequisite concepts:** from **Week 2**, salted slow KDFs (bcrypt/argon2) — Worksheet Q7 ties
  straight back to it; from **Week 3**, HMAC — the proof this week is `HMAC(verifier, nonce)`.
- **Instructor, before class:** get both images built on the room's machines ahead of the session
  by running each mode once and tearing it down
  (`docker compose -f docker-compose.vulnerable.yml up --build --abort-on-container-exit`, then
  `docker compose -f docker-compose.vulnerable.yml down`, and the same for `.fixed.yml`). Both
  services build the same image from `python:3.12-slim` plus `flask>=3.1.3`; a room doing that
  simultaneously is the usual way to lose the onboarding block.
- **Build from a local path, not a synced folder.** The lab README's own *Verified* section records
  that the verification run was done "from a scratchpad copy (OneDrive placeholders can break
  `docker build` COPY in place)". Tell students to work from a local clone, not from inside a cloud-
  synced directory.
- **Non-issue, so nobody chases it:** neither compose file publishes a port to the host — `8080` is
  reachable only on the internal `labnet` bridge. No port-conflict troubleshooting is needed, and
  nothing will be visible in a browser at `localhost:8080`; the evidence is entirely in the
  container logs.
- **Instructor note (deck timing).** 16 of the deck's 18 slides carry `~N min` speaker-note
  estimates totalling **~63 min**, against the **100 min** of non-quiz, non-break lecture time in
  the [AGENDA.md](../../AGENDA.md) HYBRID template. The gap is deliberate board work: the
  three-step-exchange slide says "Draw the three-step exchange on the board", and the cold-calls in
  §4 absorb the rest. The two unestimated slides are *"Lab today"* and *"Questions?"*. The tight
  block is the opposite case — see the timing caveat under the 1:35–1:55 row in §4.

## 4. Lecture — 120 min

Block boundaries are the HYBRID lecture template in [AGENDA.md](../../AGENDA.md); the content
column maps `slides/week14.md` onto it.

| Time | Block | Content | Method |
|---|---|---|---|
| 0:00–0:10 | Weekly quiz + recap | ~10-min retrieval quiz on Week 13 (end-to-end encryption); the bridge the deck's recap slide draws — W13 protected message *content* from the server operator, today it is a *credential* from the same operator (slides 1–3) | Individual quiz, lowest 1–2 dropped |
| 0:10–0:55 | Core concepts | TLS protects the wire, not the endpoint — draw client →[TLS]→ server →[decrypts]→ plaintext in a Python dict; the vulnerable worked example and where CWE-522/CWE-319 land; challenge-response in three steps (fresh nonce, proof computed *locally*, compare against a stored verifier); how verification works without the plaintext — `v = KDF(salt, password)`, `proof = HMAC(v, nonce)` (slides 4–7) | Lecture; the three-step exchange worked on the board |
| 0:55–1:05 | Break | | |
| 1:05–1:35 | The demonstrable half | The two-service topology — `server.py` (Flask, listens on `:8080`, behaviour set by the `PAKE` env var) and `client.py` (runs the matching flow, prints `LOGIN OK`); the fixed worked example and the `grep -c` that returns `0`; read both modes' log lines against each other (slide 8) | Lecture + walk `server.py`'s `login()` and `client.py`'s `run_fixed()` on the projector |
| 1:35–1:55 | Correct construction, out-of-scope, and the conceptual half | Honest scope — this is **not** a full PAKE; the two missing properties, with property 1 tied back to Week 2's slow KDFs; *Audit the AI* preview on the planted logging handler; then the half with no demo: know/have/are and why two "know" factors are not MFA, TOTP vs FIDO2 origin binding, credential stuffing, SSO/OAuth and the identity provider as a single point of failure (slides 9–14) | Lecture; ask for one example + one weakness per factor **before** revealing the table |
| 1:55–2:00 | Brief the game | 🗝️ "Never Say the Password" — not a flag hunt: the win is a successful `LOGIN OK` whose `grep -c` returns `0`, on the student's own terminal. Which compose file `-f` points at is the *only* thing that selects the mode (slides 15–16) | Instruction |

**Timing caveat for the 1:35–1:55 block.** Slides 9–14 carry ~26 min of speaker notes against a
20-minute block — this is the one place the deck is over-budget. Two honest ways to absorb it:
compress the factors table by eliciting the examples instead of reading it out, or move the
*Audit the AI* slide (~5 min) into the lab briefing, where it is Worksheet Part 2b anyway. Do not
skip the honest-scope slide to make room — it is the source for Q4, Part 2c and viva Q3.
Similarly, the closing slides (game brief ~3 min, *Lab today* and *Questions?* unestimated, *Key
takeaways* ~3 min) exceed the 5-minute briefing block; start the briefing before 1:55 or let the
takeaways run into the lab's onboarding.

**Checks for understanding during lecture**
- After the premise slide: *"TLS was doing its job here — so why did the password still leak?"*
  (Answer: it leaked *after* TLS did its job, at the endpoint.) This is viva question 1, so
  answering it now is rehearsal.
- After the verification slide: *"if an attacker steals the server's database and gets `v`, can they
  log in as alice directly?"* — read the instructor note in §5 before you take answers on this one.
- After the *Audit the AI* slide: *"who can read production logs?"* (log-aggregation services,
  on-call engineers, anyone who breaches the log store).
- Before the briefing: *"your friend says their login is secure because the login page uses HTTPS —
  what's missing from that claim?"*

## 5. Laboratory — 180 min

Target: the two-service stack in `labs/week14-authentication` (`server.py`, `client.py` on an
internal `labnet` bridge; demo account `alice`). This is a **read/run/observe** lab — the README
states it plainly: "code unchanged (this is a read/run/observe lab, not an exploit-and-fix-the-code
lab)". Nothing is pushed to GitHub this week; [SUBMISSION.md](../../SUBMISSION.md) is explicit that
Week 12 is the only code-push week in this course.

Block boundaries are the HYBRID lab template in [AGENDA.md](../../AGENDA.md). The **Kind** column
says which tasks are the runnable demo and which are written analysis.

| Time | Task | Kind | Student does | Evidence produced |
|---|---|---|---|---|
| 0:00–0:15 | **Onboarding** | Runnable | `cd labs/week14-authentication`; read the README's two-service table and its **honest-scope box** before touching anything; confirm Docker is up | Image builds; `SERVER: listening on 0.0.0.0:8080 (PAKE=False)` visible |
| 0:15–1:20 | **Vulnerable run — capture the "before" evidence** (Worksheet Part 2a, steps 1–2) | Runnable | `docker compose -f docker-compose.vulnerable.yml up --build --abort-on-container-exit`; capture the full log with identity proof visible; write the one-line note on **which service printed the password and why** TLS did not prevent it; tear down with `docker compose -f docker-compose.vulnerable.yml down` | `SERVER SAW PASSWORD: correct-horse-battery` + `LOGIN OK` in one capture showing `whoami`/login/student ID and a timestamp; the one-line note |
| 1:20–1:45 | **Fixed run — capture the "after" evidence** (Worksheet Part 2a, steps 3–4) | Runnable | `docker compose -f docker-compose.fixed.yml up --build --abort-on-container-exit`; capture the full log; **while the containers still exist**, run `docker compose -f docker-compose.fixed.yml logs \| grep -c "correct-horse-battery"` and `docker compose -f docker-compose.fixed.yml logs \| grep -c "SERVER SAW PASSWORD"`; then `docker compose -f docker-compose.fixed.yml down` | `SERVER SAW: nonce=... proof=...` + `LOGIN OK` + **both** `grep -c` outputs `0`, in the same capture; the one-line reflection on what the client sent instead and why it cannot be replayed |
| 1:45–2:25 | **Conceptual extension** | Written analysis | Worksheet Part 1 (8 essay questions, ~120–200 words each) — start here, finish as homework; Part 2c EiPE: proving you know a secret without revealing it, in plain English, plus one property a real PAKE adds that this demo lacks | Draft essay answers; the 4–6 sentence EiPE |
| 2:25–2:45 | **AI-resilient tasks** | Written analysis | Part 2b *Audit the AI* on the planted login handler — name the flaw, point at `(A)` and `(B)`, rewrite the two logging lines **in the worksheet**; Part 2d *Prompt Problem* against the four checks | The finding + the rewritten logging lines; exact prompt + full AI response + bullet-by-bullet critique (start in class, finish as homework) |
| 2:45–2:55 | **Rotating micro-demo** | Runnable | 2–3 students show their before/after captures and explain them in 2–3 min | Live reproduction |
| 2:55–3:00 | **Submit** | — | Worksheet PDF (with both captures embedded) → this course's Classroom, per [SUBMISSION.md](../../SUBMISSION.md)'s `Wk<NN>_<StudentID>.pdf` convention; no code push this week | Submission receipt |

**Formative checkpoints.** *(All of the following were reproduced against the files currently in
`labs/week14-authentication`, run from a local copy.)*

- **The one that catches silent failures.** A student who runs `down` *before* the two `grep -c`
  commands gets `0` for the wrong reason: the containers are gone, so `docker compose … logs`
  returns nothing at all and every `grep -c` prints `0`. Verified — after `down`, the logs output
  was **0 lines** and both counts were still `0`. This bites harder here than in Week 5, because
  the fixed side's evidence is *entirely* absence-based. Require the positive
  `SERVER SAW: nonce=… proof=…` line, `LOGIN OK`, **and** both zeros in the *same* capture taken
  before teardown; a `0` on its own proves nothing.
- **`grep -c` exits nonzero when the count is zero** — verified: both required greps returned `0`
  with exit status `1`. That is normal `grep` behaviour and exactly what a correct fixed run
  produces. A student who checks `$?`, or wraps the command in a script running under `set -e`,
  will read the correct result as a failure.
- **The mode banner is the authoritative check**, not which command was typed: `(PAKE=False)` is
  the vulnerable run, `(PAKE=True)` the fixed one. Both compose files declare the same
  `container_name`s (`week14-server`, `week14-client`), so bring the previous mode `down` before
  starting the next.
- **The real log is messier than the README's sample.** An actual run also prints the Flask
  development-server banner and werkzeug access lines — including one for the client's readiness
  probe, `GET /challenge?username=__probe__`, which answers **400** in vulnerable mode and **404**
  in fixed mode (`client.py`'s `wait_for_server()` treats *any* HTTP response as "server is up").
  Neither is an error.
- **Interleaving varies.** In the verified fixed run, `LOGIN OK` printed *before*
  `SERVER SAW: nonce=…` — two containers' output streams interleave. Grade on the presence (or
  absence) of the named lines, not on their order or on matching the README transcript.
- **`week14-server exited with code 137` is expected**, not a crash: the client exits `0` after
  authenticating and `--abort-on-container-exit` then stops the long-running server.
- A student who can produce both captures but cannot walk through how the server decides the login
  is valid **without** ever holding the password — what exactly it compares against — has evidence
  without understanding. That is viva question 2, and it is graded there, not in the log capture;
  the companion question, why a recorded nonce and proof cannot be replayed tomorrow, is Part 2a's
  written one-line reflection.

**Instructor note — the deck and the README disagree about what a stolen verifier costs you.**
`slides/week14.md`'s speaker note on "How verification works without the plaintext" asks whether a
thief holding `v` can log in as alice directly and answers **yes, trivially** — `v` is
password-equivalent in this demo, so the thief requests a fresh nonce and computes the proof. The
README's honest-scope box frames the same leak only as *"an attacker could brute-force weak
passwords against it offline."* The code supports the deck: `server.py`'s fixed path verifies with
`verify_proof(DEMO_VERIFIER, nonce, proof)`, and `client.py` derives the verifier then HMACs the
nonce — no password needed by anyone who already holds `v`. Teach the deck's version (direct
impersonation is the primary consequence; offline cracking matters because it recovers a password
the victim has reused elsewhere), and **accept either framing** at viva question 3 and in Q4, since
both are supported by material students were told to read. Do not edit the worksheet or README to
resolve this — it is reported for the content owner.

**Instructor note — the README's pointer to the slides is stale.** The lab README's "This week —
what to do" step 2 describes `slides/week14.md` as *"(not yet written — see
`course-plan-19weeks.md`)"*. The deck exists and is complete (18 slides with speaker notes). A
covering instructor prepping from the README alone would conclude there are no slides.

**Instructor note on the time budget (do not change the worksheet to fit it).** Both compose runs
complete in seconds once the images are built, so the 0:15–1:45 runnable blocks are generously
budgeted, while eight 120–200-word essays cannot realistically be finished inside the 40-minute
conceptual block. Treat Part 1 as start-in-class/finish-as-homework and let the surplus from the
run blocks flow into it. [AGENDA.md](../../AGENDA.md) flags this itself in its closing open item:
*"Confirm actual worksheet task counts fill the 180-min lab block per week … has not been
re-checked against this course's own worksheets yet."* Any permanent re-balancing belongs in the
worksheet and its answer key together, not in this plan.

## 6. Assessment for this week

Worksheet 14's own rubric is out of 100: Part 1 essays 40, Part 2a lab evidence 20, Part 2b
*Audit the AI* 15, Part 2c EiPE 10, Part 2d *Prompt Problem* 10, Part 2e viva 5.

| Instrument | Evidence | Outcome | Weight |
|---|---|---|---|
| Worksheet 14, Part 1 (8 essay questions) — Conventional arm | Written answers on TLS-vs-endpoint, the three factors, challenge-response, PAKE, TOTP vs FIDO2, credential stuffing, verifier storage, SSO/OAuth | CLO1, CLO4 | Part of the 30% worksheet component |
| Worksheet 14, Part 2a (lab evidence, both modes) — AIR-Sec arm | `SERVER SAW PASSWORD: correct-horse-battery` + `LOGIN OK`; then `SERVER SAW: nonce=… proof=…` + `LOGIN OK` + two `grep -c` outputs of `0` — with identity proof | CLO2, CLO6 | Part of the same 30% |
| Worksheet 14, Part 2b (*Audit the AI*) | Flaw named (with CWE if they can), lines `(A)` and `(B)` identified, the two logging lines rewritten | CLO5 | Part of the same 30% |
| Worksheet 14, Part 2c (EiPE) | Plain-English proof-without-revealing explanation + one named PAKE property this demo lacks | CLO5 | Part of the same 30% |
| Worksheet 14, Part 2d (*Prompt Problem*) | Exact prompt + full AI response + bullet-by-bullet critique | CLO5 | Part of the same 30% |
| Weekly quiz (start of lecture) | Quiz score | CLO1, CLO4 | Part of the 10% quiz/participation component |
| Viva spot-check / micro-demo (Part 2e) | Live reproduction of both captures and the three questions answered without notes | CLO2, CLO6 | 5 of the worksheet's 100 |

**Artefact type — check this before grading.** Week 14 issues **no `FLAG_{…}` string**. Flag keys
are no longer a hand-maintained list in this repo's `instructor/seed_flags.py` — that file is now
a thin shim forwarding to the curriculum monorepo's `tools/seed_flags.py`, which derives the valid
key set from each scheduled lesson's own `flag_keys` in
`../KOSEN69 - curriculum/lessons/<slug>/lesson.yml`. Week 14's own lesson manifest
(`lessons/authentication/lesson.yml`) carries `flag_keys: []`; the six lessons that do mint a flag
this course (hash, macs, aes-modes, aead, signatures-zkp, pqc) carry a non-empty `flag_keys` —
seven keys in total, since `pqc` mints two (`pqc`, `hndl`). (`course-plan-19weeks.md`'s Decisions
#5 entry still describes a pre-refactor `CHALLENGES = [hash, macs, aes, aead, sig, pqc]` list
hardcoded in `instructor/seed_flags.py`; that description is stale relative to the current code and
is reported for the content owner, not corrected here.) The attributable artefact this week is the
pair of evidence captures, and what makes a submission the student's own is the identity proof
beside it: `correct-horse-battery` is a lab constant, identical for every student.
Both [AGENDA.md](../../AGENDA.md)'s HYBRID callout and [SUBMISSION.md](../../SUBMISSION.md)'s
per-week table warn that this is **not** uniform across HYBRID weeks — Week 11 does ship a real
flag — so a grader working from a LAB-week habit will look for a flag that does not exist here.

**Grading note for viva question 3** — accept either framing of the stolen-verifier scenario
(direct impersonation *or* offline dictionary attack); see the instructor note in §5 for why both
are defensible from the materials as they currently stand.

**CLO bookkeeping.** The header row follows the schedule table in
[`course-specification.md`](../course-specification.md) §6, which lists CLOs **1 and 4** for
Week 14 — narrower than the week's actual worksheet, and notably without CLO2/CLO3 despite the
runnable demo. Section §4 of the same document maps the recurring worksheet parts to outcomes, and
by that mapping Worksheet 14 also carries CLO2 (the demonstration task), CLO5 (*Audit the AI*,
EiPE, *Prompt Problem*) and CLO6 (*Evidence & Integrity*). The table above uses the §4 mapping part
by part; the §6 row is narrower. CLO3 ("rebuild the construction correctly") is genuinely **not**
assessed this week — nobody writes the fix; the fixed mode ships built.

## 7. Materials

- Lab: `labs/week14-authentication/` — `README.md`, `worksheet.md`, `common.py`, `server.py`,
  `client.py`, `Dockerfile`, `requirements.txt` (`flask>=3.1.3`), `docker-compose.vulnerable.yml`,
  `docker-compose.fixed.yml`
- Slides: `slides/week14.md`
- Answer key (instructor-held, git-ignored): `instructor/week14-authentication-answer-key.md`
- Weekly retrieval quiz (~10 min, opens the lecture per [AGENDA.md](../../AGENDA.md)): ⬚ —
  `quizzes/weekly/` currently contains only the two cumulative review quizzes
  (`week07-review-quiz.md`, `week17-review-quiz.md`); there is no Week 14 item set in the repo, so
  the opening quiz must be drawn from elsewhere or written before the session
- Reading list for this week ([readings.md](../../readings.md)): ⭐ OWASP *Authentication Cheat
  Sheet*; an SRP/OPAQUE PAKE explainer (RFC 2945 for SRP); W3C *Web Authentication (WebAuthn)
  Level 2* and the FIDO Alliance specifications overview
- Further references named in the lab README: NIST SP 800-63B; OWASP *Credential Stuffing
  Prevention Cheat Sheet*; `draft-irtf-cfrg-opaque`; RFC 6238 (TOTP)
- Submission channels: [SUBMISSION.md](../../SUBMISSION.md) · Rules of engagement:
  [ETHICS.md](../../ETHICS.md)

## 8. Risks and contingencies

| Risk | Mitigation |
|---|---|
| Fixed-mode evidence is a **false pass** — a student runs `down` first, so `docker compose … logs` returns nothing and both `grep -c` commands print `0` regardless of whether anything worked | Require both zeros *plus* the `SERVER SAW: nonce=… proof=…` line and `LOGIN OK` in one capture taken before teardown; spot-check that the same screenshot shows the `(PAKE=True)` banner |
| `grep -c` returns exit status 1 on a zero count — and this week **both** required greps return zero; a student checking `$?` or running under `set -e` reads the correct answer as a failure | Say in the briefing that `0` *is* the pass condition and that the nonzero exit status is normal `grep` behaviour, not an error |
| Evidence captured from the wrong mode — both compose files declare the same `container_name`s (`week14-server`, `week14-client`), so a leftover stack confuses the picture | Tear the previous mode `down` before starting the next; grade on the `(PAKE=False)` / `(PAKE=True)` startup banner, not on which command the student says they typed |
| Werkzeug access lines, the `__probe__` request answering 400 (vulnerable) or 404 (fixed), and `week14-server exited with code 137` are read as failures | Brief all three as expected: the probe is `client.py`'s readiness check, and 137 is the server being stopped by `--abort-on-container-exit` after the client exits `0` |
| Slow first `up --build` across the room — both services build the same image from `python:3.12-slim` and install `flask>=3.1.3` | Pre-build before the session; keep an offline copy of the base image (`docker save` / `docker load`) |
| `docker build` fails on `COPY` when the checkout lives in a cloud-synced folder (the README's own *Verified* note records this — OneDrive placeholders) | Have students clone or copy the repo to a plain local path before building |
| A student hunts for a `FLAG_{…}` string that does not exist this week | The briefing and §6 say it: the artefact is the captured log lines plus identity proof; only Weeks 2, 3, 4, 6, 11 and 15 mint flags in this course |
| A student presents the fixed demo as SRP/OPAQUE — the exact overclaim the lab warns against | The honest-scope box, the deck's guardrail slide, Q4, Part 2c and viva Q3 all probe it; mark an answer that calls this "a PAKE" as incorrect regardless of how fluent it is |
| Students search for or paste `correct-horse-battery` into an online tool, treating it as a secret to crack | It is a published lab constant, not a secret; the attributable part is the identity proof. Reinforce ETHICS.md rule 5 on handling credentials — the habit, not this string, is the point |
| A student finishes both runs long before 1:45 | Extension: read `server.py`'s `/challenge` handler and the fixed `login()` path, and say precisely which line stops a captured proof from being replayed, and why the salt can safely be public; or write out viva question 2 (what the server compares against) in full |
| Copy-pasted captures — the vulnerable-mode line is identical for every student (the fixed-mode nonce/proof are random per run) | The identity proof in the same capture is the attributable part; viva spot-check anyone whose capture lacks it |

## 9. Post-teaching reflection

*Complete after the session — this also feeds the course's engagement data.*

- Attendance / completion: ⬚
- Time actually taken per block (vs. plan), especially whether the 1:35–1:55 lecture block over-ran: ⬚
- How many students produced a `0` from an already-torn-down stack: ⬚
- Where the class got stuck, and what unblocked them: ⬚
- Misconception that showed up in the Part 2c EiPE answers (did anyone claim the demo *is* a PAKE?): ⬚
- Quality of the Part 2b critiques — did students catch **both** `(A)` and `(B)`, or only the obvious one? ⬚
- Did the stolen-verifier question (deck vs README framing) confuse anyone at the viva? ⬚
- Anything to change before this week runs again: ⬚
