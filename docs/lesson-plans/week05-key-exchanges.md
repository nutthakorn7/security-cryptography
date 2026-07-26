# Lesson Plan — Week 5: Key Exchanges (MITM Against Unauthenticated Diffie–Hellman)

| | |
|---|---|
| **Course** | Security & Cryptography (⬚ course code) |
| **Week / date** | 5 · ⬚ |
| **Week kind** | **HYBRID** — a runnable MITM demo plus material that stays theoretical (small-subgroup confinement, public-key validation, group choice) |
| **Contact time** | 300 min = 120 lecture + 180 laboratory |
| **Lab folder** | `labs/week05-key-exchanges` |
| **Slides** | `slides/week05.md` (Marp deck, complete) |
| **Standards** | CWE-322 (Key Exchange without Entity Authentication) · CWE-300 (Channel Accessible by Non-Endpoint) · RFC 3526 MODP Group 14 (2048-bit) — the group `common.py` uses |
| **CLOs addressed** | **CLO2** break · **CLO3** rebuild · **CLO4** protocol reasoning — the schedule row in [`course-specification.md`](../course-specification.md) §6. Worksheet 5 additionally carries the *Explain-in-Plain-English + Prompt Problem* (CLO5) and *Evidence & Integrity* (CLO6) parts that §4 of the same document maps to those outcomes — see §6 below. |

---

## 1. Session objectives

By the end of this week a student can:

**Knowledge (K)**
- K1 — Explain why Alice and Bob need a *key exchange* rather than simply sending a symmetric key, and what an eavesdropper gains if they skip it.
- K2 — Trace a full Diffie–Hellman handshake (private exponent → public value → shared secret) and explain why the discrete-logarithm problem makes the shared secret hard for an eavesdropper to recover.
- K3 — Explain why authenticating the DH public keys (here: an HMAC under a pre-shared key) defeats the MITM **without** giving up the property DH exists for in the first place — forward secrecy of the session key.
- K4 — Recognise the related pitfalls this week's code does *not* exploit but that Q7–Q9 ask about: weak/non-standard groups, missing public-key validation, and small-subgroup confinement — and say which is a missing *identity* check and which is a missing *input-validation* check.

**Skills (P)** — P1–P3 are produced by running the demo; P4–P5 are written analysis with no runnable counterpart this week.
- P1 — Execute the vulnerable topology and capture the interception evidence line, `RELAY INTERCEPTED: the launch code is 4471`.
- P2 — Read the vulnerable-mode log and state which two `RELAY: completed independent DH handshake…` lines precede the interception, and why `relay` needed both before it could decrypt-and-relog.
- P3 — Execute the fixed topology and capture the abort evidence: `AUTH FAILED - ABORTING` from **both** `alice` and `bob`, plus the confirmed **absence** of any `RELAY INTERCEPTED` line (`grep -c` prints `0`).
- P4 — Explain a small-subgroup attack in plain English to someone who has never heard of group theory, and distinguish it from the MITM just run (Worksheet Part 2b — written, not demonstrated).
- P5 — Critique an AI explanation of authenticated Diffie–Hellman against the five checks in Worksheet Part 2c, quoting the sentences that are correct, hand-waved or wrong (written).

**Attitude (A)**
- A1 — Attack only the Docker targets supplied in `labs/`, under [ETHICS.md](../../ETHICS.md).
- A2 — Submit evidence stamped with their own identity (`whoami` / login / student ID + timestamp) and be able to reproduce the captured lines live at a viva spot-check.
- A3 — Treat a confident AI explanation of a handshake as something to be checked against a mechanism, not trusted.

## 2. Key ideas (the through-line)

Diffie–Hellman is a textbook-secure primitive that answers the wrong question. Its mathematics
defeats a **passive** eavesdropper — recovering `a` from `g^a mod p` is the discrete-logarithm
problem — but it gives neither side any way to check *who* they just agreed a secret with. Over a
network an **active** attacker controls, "whoever answers when I dial Bob's address" is not the
same claim as "Bob." The attacker simply runs the protocol twice, once with each victim, and both
handshakes complete cleanly because nothing is ever verified. The fix is not a better exchange but
an *authenticated* one: bind each DH public key to an identity (here an HMAC tag under a
pre-shared `AUTH_KEY`, in the real world a signature or certificate) and check the binding before
deriving any session key — which keeps the ephemeral exponents, and therefore forward secrecy,
intact.

Two forward links worth naming in class:
- Week 5 is the only HYBRID week before the midterm, so the Week 9 practical mixes flags with
  "Wk5-style evidence log lines" ([AGENDA.md](../../AGENDA.md), Week 9 block). The evidence
  discipline practised today is examined in four weeks.
- The CryptoVault term project requires composing "KDF + AEAD + **key exchange** + signatures +
  TLS correctly" ([`course-specification.md`](../course-specification.md) §4) — the authenticated-DH
  pattern from today is one of its components.

## 3. Prior knowledge and preparation

- **Students, before class:** Docker Desktop working (the same Docker-first setup as
  `software-security` and this course's Week 3); skim last week's recap.
- **Prerequisite concepts:** the "basic Discrete Math/Number Theory" named in
  [syllabus.md](../../syllabus.md) — modular arithmetic and exponentiation — plus, from Week 4,
  that AES-GCM needs a key; this week is where that key comes from.
- **Instructor, before class:** get the images onto the room's machines ahead of the session by
  running the lab once and tearing it down
  (`docker compose -f docker-compose.vulnerable.yml up --build`, then `Ctrl-C` and
  `docker compose -f docker-compose.vulnerable.yml down`) — the first build pulls
  `python:3.12-slim` and installs `cryptography>=48.0.1` for each of the three services, and a
  room doing that simultaneously is the usual way to lose the onboarding block.
- **Non-issue, so nobody chases it:** neither compose file publishes a port to the host — `5000`
  is reachable only on the internal `labnet` bridge. The macOS "AirPlay squats on 5000" warning
  does **not** apply to this lab.
- **Instructor note (deck timing).** The speaker notes in `slides/week05.md` carry their own
  minute estimates; they total ~69 min against the 100 min of non-quiz, non-break lecture time in
  the [AGENDA.md](../../AGENDA.md) HYBRID template. The gap is real teaching work, not slack: the
  DH slide says "walk the algebra on the board", and the cold-calls in §4 absorb the rest. The
  final briefing block is the opposite case — its four slides total ~10 min of notes against a
  5-min block, so start the briefing before 1:55 or let it run into the lab's onboarding.

## 4. Lecture — 120 min

Block boundaries are the HYBRID lecture template in [AGENDA.md](../../AGENDA.md); the content
column maps `slides/week05.md` onto it.

| Time | Block | Content | Method |
|---|---|---|---|
| 0:00–0:10 | Weekly quiz + recap | ~10-min retrieval quiz on Week 4 (AES block-cipher modes); Week 4 assumed Alice and Bob already share a key — today is where that key comes from | Individual quiz, lowest 1–2 dropped |
| 0:10–0:55 | Core concepts | Why "just send the key" fails; DH — public `p`, `g`, secret `a`/`b`, shared `g^(ab) mod p`; why the discrete-logarithm problem stops a passive eavesdropper; why the lab uses standard RFC 3526 Group 14 rather than home-made parameters; the pivot — DH secures the maths, not the identity (slides 1–7) | Lecture + algebra worked on the board |
| 0:55–1:05 | Break | | |
| 1:05–1:35 | The demonstrable half | The lab topology (`bob.py` server, `alice.py` client dialling `relay` and never `bob`, `relay.py` on the path); the attack — two independent handshakes, two shared secrets, decrypt/re-log/re-encrypt; why neither endpoint notices (CWE-322, CWE-300); read the vulnerable-mode log line by line (slides 8–11) | Lecture + walk `relay.py`'s `handle_mitm()` on the projector |
| 1:35–1:55 | Correct construction + what stays out of scope | HMAC-SHA256 over the DH public key under a pre-shared `AUTH_KEY`, verified *before* any session key is derived; why that keeps forward secrecy instead of "just send a symmetric key"; how TLS/SSH do the same with signatures/certificates; then the hard line — weak groups (Q7), missing public-key validation (Q8) and small-subgroup confinement (Q9) are **not** demonstrated by this week's code (slides 12–15) | Lecture with the vulnerable/fixed log contrast side by side |
| 1:55–2:00 | Brief the game | 🕵️ "The Silent Third Wheel" — be the silent third party, read their "secure" channel, then watch one HMAC tag shut you out with no other code change; which compose file you point `-f` at is the *only* thing that selects the mode | Instruction |

**Checks for understanding during lecture**
- After the DH slide: cold-call — *"the eavesdropper sees `p`, `g`, `g^a` and `g^b`. What exactly
  is it that they cannot compute, and what is that problem called?"*
- After the vulnerable log: *"which two lines must appear before `RELAY INTERCEPTED`, and why does
  relay need both first?"* — this is viva question 1, so answering it now is rehearsal.
- Before the briefing: *"why does fixed mode still run a fresh DH exchange every session, instead
  of just using `AUTH_KEY` as the encryption key?"* (forward secrecy — viva question 3).

## 5. Laboratory — 180 min

Target: the three-service stack in `labs/week05-key-exchanges` (`alice`, `bob`, `relay` on an
internal bridge network). This is a **read/run/observe** lab — no student code changes, so nothing
is pushed to GitHub this week; the deliverable is captured evidence plus reasoning.

Block boundaries are the HYBRID lab template in [AGENDA.md](../../AGENDA.md). The **Kind** column
says which tasks are the runnable demo and which are written analysis.

| Time | Task | Kind | Student does | Evidence produced |
|---|---|---|---|---|
| 0:00–0:15 | **Onboarding** | Runnable | `cd labs/week05-key-exchanges`; read the README's topology table; confirm Docker is up | Stack builds; `BOB: listening on 0.0.0.0:5000 (SIGNED=False)` visible |
| 0:15–1:20 | **Vulnerable run — capture the "before" evidence** (Worksheet Part 2a, steps 1–2) | Runnable | `docker compose -f docker-compose.vulnerable.yml up --build`; capture the full log; note in one line which two `RELAY: completed independent DH handshake…` lines precede the interception and why relay needed both; tear down with `Ctrl-C` then `docker compose -f docker-compose.vulnerable.yml down` | `RELAY INTERCEPTED: the launch code is 4471` (+ `BOB RECEIVED: …`) with identity proof visible; the one-line note |
| 1:20–1:45 | **Fixed run — capture the "after" evidence** (Worksheet Part 2a, steps 3–4) | Runnable | `docker compose -f docker-compose.fixed.yml up --build`; capture the full log; **while the containers still exist**, run `docker compose -f docker-compose.fixed.yml logs \| grep -c "RELAY INTERCEPTED"`; then tear down | Two `AUTH FAILED - ABORTING` lines (one from `alice`, one from `bob`) + the `grep -c` output `0`, in the same capture |
| 1:45–2:25 | **Conceptual extension** | Written analysis | Worksheet Part 1 (10 essay questions, ~120–200 words each) — start here, finish as homework; Part 2b EiPE: small-subgroup attacks in plain English, and why that failure differs from the MITM just run | Draft essay answers; the 4–6 sentence EiPE |
| 2:25–2:45 | **AI-resilient task** | Written analysis | Worksheet Part 2c *Prompt Problem*: prompt an AI on why authenticated DH prevents MITM, then critique it against the five checks (eavesdropper-vs-identity, what is actually bound and verified, the trust bootstrap, forward secrecy, hallucinated mechanisms) | Exact prompt + full AI response + bullet-by-bullet critique (start in class, finish as homework) |
| 2:45–2:55 | **Rotating micro-demo** | Runnable | 2–3 students show their before/after log lines and explain them in 2–3 min | Live reproduction |
| 2:55–3:00 | **Submit** | — | Worksheet PDF (with both captures embedded) → this course's Classroom, per [SUBMISSION.md](../../SUBMISSION.md); no code push this week | Submission receipt |

**Formative checkpoints.**
- **The one that catches silent failures:** a student who runs `down` *before* the `grep -c` gets
  `0` for the wrong reason — the containers are gone, so `docker compose … logs` returns nothing at
  all and any `grep -c` prints `0`. Require the two `AUTH FAILED - ABORTING` lines and the `0` in
  the *same* capture; a `0` on its own proves nothing. Verified: after `down`, the logs output is
  empty and the count is still `0`.
- `grep -c` **exits nonzero when the count is zero** — that is normal, expected, and exactly what
  the fixed run should produce. A student who checks `$?`, or who wraps the command in a script
  running under `set -e`, will read the correct result as a failure.
- Before capturing anything, check the mode banner in the startup log: `(SIGNED=False)` is the
  vulnerable run, `(SIGNED=True)` is the fixed run. The two compose files use the same fixed
  `container_name`s, so bring the previous mode `down` before starting the next one.
- A student who cannot say *why* two handshakes are needed has evidence but not understanding —
  that is viva question 1 and it is graded there, not in the log capture.

**Instructor note on the time budget (do not change the worksheet to fit it).** Both compose runs
complete in well under a minute once the images are built, so the 0:15–1:45 runnable blocks are
generously budgeted, while ten 120–200-word essays cannot realistically be finished inside the
40-minute conceptual block. Treat Part 1 as start-in-class/finish-as-homework and let the surplus
from the run blocks flow into it. [AGENDA.md](../../AGENDA.md) flags this itself in its closing
open item: *"Confirm actual worksheet task counts fill the 180-min lab block per week … has not
been re-checked against this course's own worksheets yet."* Any permanent re-balancing belongs in
the worksheet and its answer key together, not in this plan.

## 6. Assessment for this week

Worksheet 5's own rubric is out of 100: Part 1 essays 40, Part 2a lab evidence 20, Part 2b EiPE
15, Part 2c Prompt Problem 15, Part 2d viva 10.

| Instrument | Evidence | Outcome | Weight |
|---|---|---|---|
| Worksheet 5, Part 1 (10 essay questions) — Conventional arm | Written answers | CLO1, CLO4 | Part of the 30% worksheet component |
| Worksheet 5, Part 2a (lab evidence, both modes) — AIR-Sec arm | Vulnerable-run interception line + fixed-run abort lines + `grep -c` = 0, with identity proof | CLO2, CLO3, CLO6 | Part of the same 30% |
| Worksheet 5, Part 2b (EiPE) | Plain-English small-subgroup explanation | CLO5 | Part of the same 30% |
| Worksheet 5, Part 2c (Prompt Problem) | Prompt + AI response + critique | CLO5 | Part of the same 30% |
| Weekly quiz (start of lecture) | Quiz score | CLO1, CLO2 | Part of the 10% quiz/participation component |
| Viva spot-check / micro-demo (Part 2d) | Live reproduction of the before/after log lines and the three questions answered without notes | CLO2, CLO3, CLO6 | 10 of the worksheet's 100 |

**Artefact type — check this before grading.** Week 5 issues **no `FLAG_{…}` string**. The
attributable artefact is the pair of evidence log lines, and what makes a submission the student's
own is the identity proof beside it — `SECRET_MESSAGE` is a lab constant, identical for every
student. [AGENDA.md](../../AGENDA.md)'s HYBRID callout warns explicitly that this is not uniform
across HYBRID weeks (Week 11 does ship a real flag), so a grader working from a LAB-week habit will
look for a flag that does not exist.

**CLO bookkeeping.** The header row follows the schedule table in
[`course-specification.md`](../course-specification.md) §6, which lists CLOs 2, 3, 4 for Week 5.
Section §4 of the same document maps the recurring worksheet parts to outcomes, and by that mapping
Worksheet 5 also carries CLO1 (conceptual analysis, Part 1), CLO5 (Explain-in-Plain-English +
Prompt Problem — §4's combined row, so both Part 2b and Part 2c carry it) and CLO6 (Evidence &
Integrity). The table above uses the §4 mapping part by part; the §6 row is narrower.

## 7. Materials

- Lab: `labs/week05-key-exchanges/` — `README.md`, `worksheet.md`, `common.py`, `alice.py`,
  `bob.py`, `relay.py`, `Dockerfile`, `requirements.txt`,
  `docker-compose.vulnerable.yml`, `docker-compose.fixed.yml`
- Slides: `slides/week05.md`
- Answer key (instructor-held, git-ignored): `instructor/week05-key-exchanges-answer-key.md`
- Reading list for this week ([readings.md](../../readings.md)): RFC 3526 (⭐), a
  Diffie–Hellman/MITM explainer, Boneh & Shoup *A Graduate Course in Applied Cryptography*
  (key-exchange chapter)
- Further references named in the lab README: NIST SP 800-56A Rev. 3 (public-key validation —
  relevant to Q8/Q9)
- Submission channels: [SUBMISSION.md](../../SUBMISSION.md) · Rules of engagement:
  [ETHICS.md](../../ETHICS.md)

## 8. Risks and contingencies

| Risk | Mitigation |
|---|---|
| Fixed-mode evidence is a **false pass** — a student runs `down` first, so `docker compose … logs` returns nothing and `grep -c "RELAY INTERCEPTED"` prints `0` regardless of whether the fix worked | Require the `0` and both `AUTH FAILED - ABORTING` lines in one capture, taken before teardown; spot-check that the same screenshot shows the `(SIGNED=True)` banner |
| `grep -c` returns exit status 1 on a zero count; a student checking `$?` or running under `set -e` reads the correct answer as a failure | Say in the briefing that a `0` count is the pass condition and the nonzero exit status is normal `grep` behaviour, not an error |
| Slow first `up --build` across the room — three services each pull `python:3.12-slim` and install `cryptography>=48.0.1` | Pre-build the images before the session; keep an offline copy of the base image (`docker save`/`docker load`) |
| A student captures evidence from the wrong mode — both compose files declare the same `container_name`s (`week05-alice`, `week05-bob`, `week05-relay`), so a leftover stack from the other mode confuses the picture | Tear the previous mode `down` before starting the next; the authoritative check is the `(SIGNED=False)` / `(SIGNED=True)` banner in the startup lines, not which command was typed |
| Interleaving differs from the README's sample log, and a student thinks their run went wrong | The README states it: interleaving, ports and IPs vary run to run; the container names and message text do not. Grade on the presence/absence of the named lines and their relative order, not on an exact transcript |
| A student treats the demo as proof that DH itself is broken | The out-of-scope slide and the README both state the boundary: this week runs a key-substitution MITM (missing *identity* check), not a small-subgroup attack (missing *input validation*, Q8/Q9). Ask for the distinction at the viva |
| A student finishes both runs long before 1:45 | Extension: read `relay.py`'s `handle_mitm_signed()` and say precisely which line makes the attack fail, and what `relay` would need in order to succeed; or answer viva question 3 in writing (why not just use `AUTH_KEY` as the session key) |
| Copy-pasted logs — the intercepted message is identical for every student | The identity proof (`whoami`/login/student ID + timestamp) in the same capture is the attributable part; viva spot-check anyone whose capture lacks it |

## 9. Post-teaching reflection

*Complete after the session — this also feeds the course's engagement data.*

- Attendance / completion: ⬚
- Time actually taken per block (vs. plan), especially whether the essay block over-ran: ⬚
- How many students produced a `0` from an already-torn-down stack: ⬚
- Where the class got stuck, and what unblocked them: ⬚
- Misconception that showed up in the Part 2b EiPE answers (identity check vs input validation): ⬚
- Quality of the Part 2c critiques — did students catch a hand-waved trust bootstrap? ⬚
- Anything to change before this week runs again: ⬚
