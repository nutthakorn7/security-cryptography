# Lesson Plan — Week 13: End-to-End Encryption (TLS Is Not Enough — the Server Still Reads Your Messages)

| | |
|---|---|
| **Course** | Security & Cryptography (⬚ course code) |
| **Week / date** | 13 · ⬚ |
| **Week kind** | **HYBRID** — a runnable TLS-only-vs-E2EE demo plus material that stays theoretical (the root-of-trust / key-distribution problem, why PGP failed, Signal's TOFU/X3DH/Double Ratchet, open problems in E2EE) |
| **Contact time** | 300 min = 120 lecture + 180 laboratory |
| **Lab folder** | `labs/week13-e2e-encryption` |
| **Slides** | `slides/week13.md` (Marp deck, complete — 17 slides with speaker notes) |
| **Standards** | CWE-311 (Missing Encryption of Sensitive Data) · CWE-319 (Cleartext Transmission of Sensitive Information — here, cleartext *storage on the relay* even when transit is encrypted) · NIST SP 800-56B Rev. 2 (RSA-OAEP key transport — the wrapping scheme `common.py` uses) |
| **CLOs addressed** | **CLO3** rebuild · **CLO4** protocol reasoning — the schedule row in [`course-specification.md`](../course-specification.md) §6. Note this row does **not** list CLO2: nothing is broken this week. Worksheet 13 additionally carries the conceptual analysis (CLO1), *Audit the AI* / EiPE / *Prompt Problem* (CLO5) and *Evidence & Integrity* (CLO6) parts that §4 of the same document maps to those outcomes — see §6 below. |

---

## 1. Session objectives

By the end of this week a student can:

**Knowledge (K)**
- K1 — State the difference between **transport encryption** (TLS/HTTPS — protects data *in transit* between client and server) and **end-to-end encryption** (protects data *from the server operator itself*), and explain why the first does not imply the second.
- K2 — Explain *why* the plaintext genuinely exists at the server: the server **terminates** TLS, decrypts, holds the plaintext and re-encrypts to forward — it is a trusted third party by construction, not by accident.
- K3 — Trace the E2EE message shape the lab implements: recipient publishes a public key; sender fetches it and performs **hybrid encryption** *client-side* — a fresh AES-256-GCM key per message, RSA-OAEP-wrapped to the recipient (`common.hybrid_encrypt`) — before the message ever reaches the server.
- K4 — Name the related ideas this week's code does *not* solve but that the worksheet's essay questions ask about: the root-of-trust / key-distribution problem (Q2), why PGP/S-MIME never reached mass adoption (Q3), how Signal's TOFU, X3DH and Double Ratchet improve on it (Q4), and one open problem — group fan-out, multi-device key sync, or Key Transparency (Q5).

**Skills (P)** — P1–P3 are produced by running the demo; P4–P5 are written analysis with no runnable counterpart this week.
- P1 — Execute the vulnerable configuration and capture the leak evidence: `SERVER SAW: meet at pier 39 at midnight`, alongside `BOB RECEIVED: meet at pier 39 at midnight`.
- P2 — Execute the fixed configuration and capture both required lines: a `SERVER SAW:` line that is now long base64, and `BOB DECRYPTED: meet at pier 39 at midnight` — i.e. delivery still works while the provider holds only ciphertext.
- P3 — Prove the *absence* of the plaintext from the provider's own log with `docker compose -f docker-compose.fixed.yml logs server | grep -c "meet at pier 39 at midnight"` printing `0`, and explain why an absence, captured before teardown, is the evidence.
- P4 — State precisely what the demo does **not** prove — that Alice is talking to the real Bob — and explain the public-key substitution a malicious server could perform (Worksheet Q2; viva question 3). Written.
- P5 — Critique an AI-written "secure chat backend" that calls itself end-to-end encrypted because it uses HTTPS, naming the two guarantees it has conflated and who can still read every message (Worksheet Part 2b), and critique a fresh AI answer against the four checks in Part 2d. Written.

**Attitude (A)**
- A1 — Run and observe only the local containers this lab spins up (`server.py`, `alice.py`, `bob.py`), under [ETHICS.md](../../ETHICS.md) and the worksheet's own ethics note — reading or logging other people's messages on systems they do not own is illegal.
- A2 — Submit evidence stamped with their own identity (`whoami` / login / student ID + timestamp) and be able to reproduce the captured lines live at a viva spot-check.
- A3 — Treat confident prose about encryption ("we use industry-standard TLS, so this is end-to-end encrypted") as a claim to be checked against where the plaintext actually lives.

## 2. Key ideas (the through-line)

The primitive is not broken; the assumption about it is. TLS does exactly what it promises —
confidentiality on the wire — and then people read that promise as covering something it never
claimed: confidentiality *from the party at the other end of the wire*. The lab makes that visible
with one design choice: **the server always logs what it stores, and what it stores is whatever
Alice chose to hand it.** `server.py` is byte-for-byte identical in both modes and has no idea
whether E2EE is on. In vulnerable mode Alice hands it plaintext, so its own log leaks the secret;
in fixed mode she hands it an opaque envelope, so the same `print(f"SERVER SAW: {payload}")`
statement leaks nothing useful. The guarantee comes from the **clients**, not from trusting the
provider — that is the whole of end-to-end encryption.

The second half of the week is the honest limit. Moving the encryption boundary to the endpoints
answers *"can the provider read this?"* and leaves *"is this really Bob's key?"* wide open. Alice
here trusts whatever key the server hands her, which a malicious server could substitute — the
messaging cousin of Week 5's Diffie–Hellman MITM. That question is where TOFU, safety numbers,
certificate authorities and key transparency live, and it stays conceptual this week.

Three links worth naming in class:
- **Back to Week 12.** TLS asked "is this channel going to the right endpoint?" This week: even when
  it is, that endpoint is the *server* — encryption *to* the server is not encryption *from* it
  (deck slide 3).
- **Back to Week 10.** The AES-GCM-key-wrapped-in-RSA-OAEP pattern is the same hybrid construction
  from the asymmetric/hybrid-encryption week, deployed here into an actual messaging shape (deck
  slide 7).
- **Forward to the exams.** [AGENDA.md](../../AGENDA.md) lists Wk13 evidence-log-line tasks in the
  Week 17 mock CTF and the Week 19 capstone CTF, and Week 17's Jeopardy covers Wk10–16. The
  evidence discipline practised today is examined twice more.

## 3. Prior knowledge and preparation

- **Students, before class:** Docker Desktop working (the same Docker-first setup as
  `software-security` and this course's earlier weeks); skim the recap named in the lab README
  under "This week — what to do".
- **Prerequisite concepts:** public-key encryption and the hybrid (symmetric-key-wrapped-to-a-
  public-key) construction from the asymmetric/hybrid-encryption week; from Week 12, what a TLS
  endpoint is and what certificate validation does — this week is about what TLS never covered.
- **Instructor, before class:** get the images onto the room's machines ahead of the session by
  running the lab once and tearing it down
  (`docker compose -f docker-compose.vulnerable.yml up --build`, then `Ctrl-C` and
  `docker compose -f docker-compose.vulnerable.yml down`) — the first build pulls
  `python:3.12-slim` and installs `cryptography>=48.0.1`, `Flask>=3.1.3` and `requests>=2.33.0`,
  and a room doing that simultaneously is the usual way to lose the onboarding block. The three
  services share one build context and one `Dockerfile`, so the base image is pulled once and the
  `pip install` layer is built once and reused across the three tagged images.
- **Non-issue, so nobody chases it:** neither compose file publishes a port to the host. The three
  services talk on the internal `labnet` bridge on port `8080`; nothing is reachable from a browser
  and "port 8080 is already in use on my laptop" cannot break this lab. Say so in the briefing — it
  is the first thing a student who has done Weeks 2–6 will assume.
- **Instructor note (deck timing).** The speaker notes in `slides/week13.md` carry their own minute
  estimates; they total ~65 min against the 100 min of non-quiz, non-break lecture time in the
  [AGENDA.md](../../AGENDA.md) HYBRID template. The gap is real teaching work — the two-guarantees
  table is meant to be drawn on the board, and the cold-calls in §4 absorb the rest. The closing
  blocks are the opposite case: the game brief (~3 min), the Worksheet 13 slide (~3 min), key
  takeaways (~2 min) and the closing slide (~2 min) total ~10 min of notes against the 5-min
  briefing block, so start the briefing before 1:55 or let it run into the lab's onboarding.
- **Instructor note (deck order).** The deck teaches the fix (slide 7, hybrid encryption at the
  endpoints) *before* the demo slides, so the 1:35–1:55 "correct construction + out of scope" block
  carries the boundary-setting slide and the PGP/Signal comparative material rather than a fresh
  construction. That is a deliberate ordering, not a gap — but do not go looking for a defence
  slide at 1:35 that has already been taught.

## 4. Lecture — 120 min

Block boundaries are the HYBRID lecture template in [AGENDA.md](../../AGENDA.md); the content
column maps `slides/week13.md` onto it.

| Time | Block | Content | Method |
|---|---|---|---|
| 0:00–0:10 | Weekly quiz + recap | ~10-min retrieval quiz on Week 12 (secure transport); the bridge — TLS answered "am I talking to the right endpoint?", and that endpoint is the server | Individual quiz, lowest 1–2 dropped |
| 0:10–0:55 | Core concepts | Hook poll: "if an app is HTTPS everywhere, can the company running the server still read your messages?"; the two-guarantees table (what each protects, whom it hides plaintext from, where plaintext can exist); why the server *terminates* TLS and is a trusted third party by construction; the break framed as a threat-model mismatch, not a broken primitive (CWE-311, CWE-319); the fix in principle — fresh AES-256-GCM key per message, RSA-OAEP-wrapped to the recipient (slides 1–7) | Lecture + both definitions drawn side by side on the board |
| 0:55–1:05 | Break | | |
| 1:05–1:35 | The demonstrable half | The lab shape (`server.py` the provider, logging `SERVER SAW: <payload>` verbatim and identical in both modes; `alice.py` the sender; `bob.py` the recipient); run vulnerable mode live and let students spot the leak line themselves; run fixed mode and the `grep -c` side by side (slides 8–10) | Lecture + live `docker compose … up --build` on the projector |
| 1:35–1:55 | The boundary + what stays conceptual | What the lab does **not** prove — Alice trusts whatever public key the server hands her, so a malicious server could substitute its own (public-key MITM, the cousin of Week 5's DH MITM); why PGP/S-MIME failed on key discovery, metadata and usability; how Signal's TOFU, X3DH and Double Ratchet (forward secrecy + post-compromise security) address that (slides 11–13) | Lecture; state the boundary out loud so nobody over-claims the demo |
| 1:55–2:00 | Brief the game | 👀 "Who's Reading Your Mail?" — play the provider, `tail` your own server's log while a "private" message goes through, then flip the client to encrypt client-side and watch your own log turn to gibberish while the recipient still decrypts; which compose file you point `-f` at is the *only* thing that selects the mode (slides 14–15) | Instruction |

**Checks for understanding during lecture**
- After the two-guarantees table: cold-call — *"name the party each of the two guarantees excludes
  from reading the message."*
- After the fixed-mode log: *"`server.py` is the same file in both runs and still prints every
  payload it stores. So where did the difference come from?"* — this is viva question 1, so
  answering it now is rehearsal.
- Before the briefing: *"name one concrete thing a provider can no longer do once messages are
  truly E2EE"* (hand over readable messages on request, scan them for ads, leak them in a breach).

## 5. Laboratory — 180 min

Target: the three-service stack in `labs/week13-e2e-encryption` (`server`, `alice`, `bob` on the
internal `labnet` bridge, port `8080`, **no host port published** — you never point a browser at
this, you read the container logs). This is a **read/run/observe** lab: the README states the code
is unchanged this week, so the deliverable is captured evidence plus reasoning, not a code fix.

Block boundaries are the HYBRID lab template in [AGENDA.md](../../AGENDA.md). The **Kind** column
says which tasks are the runnable demo and which are written analysis.

| Time | Task | Kind | Student does | Evidence produced |
|---|---|---|---|---|
| 0:00–0:15 | **Onboarding** | Runnable | `cd labs/week13-e2e-encryption`; read the README's service table (`server.py` / `alice.py` / `bob.py`); confirm Docker is up | Stack builds; `SERVER: listening on 0.0.0.0:8080 (E2E=False)` visible |
| 0:15–1:20 | **Vulnerable run — capture the "before" evidence** (Worksheet Part 2a, steps 1–2) | Runnable | `docker compose -f docker-compose.vulnerable.yml up --build`; capture the full log; note in one line *who* could read the secret and why "but the connection could be HTTPS" does not change the answer; tear down with `Ctrl-C` then `docker compose -f docker-compose.vulnerable.yml down` | `SERVER SAW: meet at pier 39 at midnight` and `BOB RECEIVED: meet at pier 39 at midnight`, with identity proof visible; the one-line note |
| 1:20–1:45 | **Fixed run — capture the "after" evidence** (Worksheet Part 2a, steps 3–4) | Runnable | `docker compose -f docker-compose.fixed.yml up --build`; capture the full log; **while the containers still exist**, run `docker compose -f docker-compose.fixed.yml logs server \| grep -c "meet at pier 39 at midnight"`; then tear down | A base64 `SERVER SAW:` line, `BOB DECRYPTED: meet at pier 39 at midnight`, and the `grep -c` output `0` — all in the same capture, with the `(E2E=True)` banner visible |
| 1:45–2:25 | **Conceptual extension** | Written analysis | Worksheet Part 1 (5 essay questions, ~150–250 words each): TLS is not enough; the root-of-trust problem and two concrete roots of trust; why encrypted email failed plus the student's own redesign opinion; how Signal improves on PGP; one open problem in E2EE. Start here, finish as homework | Draft essay answers |
| 2:25–2:45 | **AI-resilient tasks** | Written analysis | Worksheet Part 2b *Audit the AI* — the AI "secure chat backend" that stores and `log.info`s the plaintext while claiming TLS makes it end-to-end encrypted: quote the offending lines, name the conflated guarantees, and produce the corrected design; Part 2c EiPE (the WhatsApp "lock icon" friend, 4–6 sentences, plain language); Part 2d *Prompt Problem* (prompt an AI on TLS vs. E2EE, then critique it against the four checks) | The critique, the EiPE answer, and the exact prompt + full AI response + bullet-by-bullet critique (start in class, finish as homework) |
| 2:45–2:55 | **Rotating micro-demo** | Runnable | 2–3 students show their before/after `SERVER SAW:` lines and explain, in 2–3 min, where the difference came from | Live reproduction |
| 2:55–3:00 | **Submit** | — | Worksheet PDF (with both captures embedded) → this course's Classroom, per [SUBMISSION.md](../../SUBMISSION.md); no code change to push this week | Submission receipt |

**Formative checkpoints.**
- **The false pass that looks like success.** A student who runs `down` *before* the `grep -c` gets
  `0` for the wrong reason: the containers are gone, `docker compose … logs server` returns nothing,
  and any `grep -c` prints `0`. Verified in preparing this plan — after `down`, the vulnerable-mode
  server log is empty and `grep -c "meet at pier 39 at midnight"` still prints `0`. Require the `0`
  *and* the base64 `SERVER SAW:` line *and* `BOB DECRYPTED: …` in the **same** capture; a `0` on its
  own proves nothing.
- **The opposite error — dropping the service name.** The worksheet's command greps the **server**
  log specifically. Verified: in fixed mode,
  `docker compose -f docker-compose.fixed.yml logs | grep -c "meet at pier 39 at midnight"` (no
  `server`) prints **1**, because `bob`'s own `BOB DECRYPTED: meet at pier 39 at midnight` line
  matches. A student who drops the word `server` will conclude the E2EE failed. The claim being
  evidenced is "the *provider* never saw it", so the service name is load-bearing.
- **`grep -c` exits nonzero when the count is zero** — that is normal `grep` behaviour and exactly
  what the fixed run should produce. Verified: the fixed-mode server-log grep printed `0` with exit
  status `1`. A student who checks `$?`, or wraps the command in a script running under `set -e`,
  will read the correct result as a failure.
- **`up --build` runs in the foreground** as the worksheet quotes it, so the step-3 grep needs a
  second terminal, or must be run after `Ctrl-C` but *before* `down`. Say this in the briefing; the
  worksheet's step order is correct, but the hazard is invisible until a student has already torn
  the stack down.
- **Check the mode banner, not the command you think you typed.** `(E2E=False)` in the startup line
  is the vulnerable run, `(E2E=True)` is the fixed run. Both compose files declare the same
  `container_name`s (`week13-server`, `week13-alice`, `week13-bob`), so bring the previous mode
  `down` before starting the next.
- A student who can paste both log lines but cannot say *why* they differ has evidence without
  understanding — that is viva question 1, and it is graded there, not in the capture.

**Instructor note on the time budget (do not change the worksheet to fit it).** Both compose runs
complete in well under a minute once the images are built — in verification, `alice` and `bob` were
one-shot containers that exited `0` within seconds while `server` stayed up — so the 0:15–1:45
runnable blocks are generously budgeted, whereas five 150–250-word essays plus three AI-resilient
tasks will not all finish inside the 1:45–2:45 window. Treat Part 1 and Parts 2b–2d as
start-in-class/finish-as-homework and let the surplus from the run blocks flow into them.
[AGENDA.md](../../AGENDA.md) flags this itself in its closing open item: *"Confirm actual worksheet
task counts fill the 180-min lab block per week … has not been re-checked against this course's own
worksheets yet."* Any permanent re-balancing belongs in the worksheet and its answer key together,
not in this plan.

## 6. Assessment for this week

Worksheet 13's own rubric is out of 100: Part 1 essays 40, Part 2a lab evidence 20,
*Audit the AI* (Part 2b) 15, EiPE + *Prompt Problem* (Parts 2c–2d) 15, viva spot-check (Part 2e) 10.

| Instrument | Evidence | Outcome | Weight |
|---|---|---|---|
| Worksheet 13, Part 1 (5 essay questions) — Conventional arm | Written answers on TLS-vs-E2EE, root of trust, PGP's failure, Signal, one open problem | CLO1, CLO4 | Part of the 30% worksheet component |
| Worksheet 13, Part 2a (lab evidence, both modes) — AIR-Sec arm | Vulnerable-run `SERVER SAW:` plaintext line + fixed-run base64 `SERVER SAW:` line + `BOB DECRYPTED: …` + `grep -c` = `0`, with identity proof | CLO3, CLO6 | Part of the same 30% |
| Worksheet 13, Part 2b (*Audit the AI*) | Quoted flaw lines, the conflated-guarantees explanation, the corrected design | CLO5 | Part of the same 30% |
| Worksheet 13, Parts 2c–2d (EiPE + *Prompt Problem*) | Plain-language WhatsApp explanation; prompt + full AI response + bullet-by-bullet critique | CLO5 | Part of the same 30% |
| Weekly quiz (start of lecture) | Quiz score | CLO1, CLO4 | Part of the 10% quiz/participation component |
| Viva spot-check / micro-demo (Part 2e) | Live reproduction of the before/after log lines and the three questions answered without notes | CLO3, CLO4, CLO6 | 10 of the worksheet's 100 |

**Artefact type — check this before grading.** Week 13 issues **no `FLAG_{…}` string**. The
attributable artefact is the pair of evidence log lines, and what makes a submission the student's
own is the identity proof beside it — `SECRET_MESSAGE` is a lab constant, identical for every
student, and the worksheet says so explicitly. [AGENDA.md](../../AGENDA.md)'s HYBRID callout warns
that this is not uniform across HYBRID weeks (Week 11 does ship a real flag), so a grader working
from a LAB-week habit will look for a flag that does not exist.

**CLO bookkeeping.** The header row follows the schedule table in
[`course-specification.md`](../course-specification.md) §6, which lists CLOs 3 and 4 for Week 13 —
narrower than Weeks 5, 11 and 12, and correctly so: this is a read/run/observe week in which nothing
is broken, so CLO2 does not apply. Note also that the CLO3 "rebuild" here is *running the supplied
fixed configuration and demonstrating the provider can no longer read the message*, not writing the
fix — §6 of the same document records Week 12 as the one week in which students write the fix
themselves. Section §4 maps the recurring worksheet parts to outcomes, and by that mapping
Worksheet 13 also carries CLO1 (conceptual analysis), CLO5 (*Audit the AI*, EiPE, *Prompt Problem*)
and CLO6 (Evidence & Integrity). The table above uses the §4 mapping part by part.

## 7. Materials

- Lab: `labs/week13-e2e-encryption/` — `README.md`, `worksheet.md`, `common.py`, `server.py`,
  `alice.py`, `bob.py`, `Dockerfile`, `requirements.txt`, `docker-compose.vulnerable.yml`,
  `docker-compose.fixed.yml`
- Slides: `slides/week13.md`
- Answer key (instructor-held, git-ignored): `instructor/week13-e2e-encryption-answer-key.md`
- Weekly retrieval quiz items: ⬚ — `quizzes/weekly/` currently holds only the two cumulative
  review quizzes (`week07-review-quiz.md`, `week17-review-quiz.md`), so the 0:00–0:10 block has no
  item source in this repository yet
- Reading list for this week ([readings.md](../../readings.md)): ⭐ Signal — *The X3DH Key Agreement
  Protocol*; Signal — *The Double Ratchet Algorithm*; a "why TLS isn't E2EE" explainer
- Further references named in the lab README: Signal Protocol documentation (https://signal.org/docs/);
  Unger et al., *SoK: Secure Messaging*, IEEE S&P 2015; Whitten & Tygar, *Why Johnny Can't Encrypt*,
  USENIX Security 1999; NIST SP 800-56B Rev. 2 (RSA-OAEP key transport)
- Submission channels: [SUBMISSION.md](../../SUBMISSION.md) · Rules of engagement:
  [ETHICS.md](../../ETHICS.md)

## 8. Risks and contingencies

| Risk | Mitigation |
|---|---|
| Fixed-mode evidence is a **false pass** — a student runs `down` first, so `docker compose … logs server` returns nothing and `grep -c "meet at pier 39 at midnight"` prints `0` regardless of whether E2EE worked | Require the `0`, the base64 `SERVER SAW:` line and `BOB DECRYPTED: …` in one capture taken before teardown; spot-check that the same screenshot shows the `(E2E=True)` banner |
| A student drops `server` from the grep and gets `1` in fixed mode (bob's own `BOB DECRYPTED:` line matches), then reports the E2EE as broken | Brief the command as written: the claim is "the *provider* never saw it", so it is the **server's** log that must be grepped. Verified: the all-services grep prints `1` in fixed mode |
| `grep -c` returns exit status 1 on a zero count; a student checking `$?` or running under `set -e` reads the correct answer as a failure | Say in the briefing that `0` is the pass condition and the nonzero exit status is normal `grep` behaviour, not an error |
| `up --build` holds the terminal in the foreground, so a student cannot run the step-3 grep without either a second terminal or `Ctrl-C` first — and reaching for `down` at that moment produces the false pass above | Tell students up front: `Ctrl-C` stops the stack but leaves the containers, so the grep still works; only `down` destroys the evidence |
| Evidence captured from the wrong mode — both compose files declare the same `container_name`s (`week13-server`, `week13-alice`, `week13-bob`), so a leftover stack confuses the picture | Tear the previous mode `down` before starting the next; the authoritative check is the `(E2E=False)` / `(E2E=True)` banner in the startup line, not which command was typed |
| Slow first `up --build` across the room — the build pulls `python:3.12-slim` and installs `cryptography>=48.0.1`, `Flask>=3.1.3` and `requests>=2.33.0` | Pre-build the images before the session; keep an offline copy of the base image (`docker save`/`docker load`) |
| A student waits for a web page or hunts for a busy port | Neither compose file publishes a host port — the services talk on the internal `labnet` bridge on `8080`. State it in the briefing and in the onboarding block; the evidence is in `docker compose … logs`, never in a browser |
| Interleaving differs from the README's sample log and a student thinks their run went wrong | The README states it: interleaving, ports and IPs vary run to run; the container names and message text do not. Grade on the presence/absence of the named lines, not on an exact transcript |
| A student over-claims — "fixed mode proves alice was really talking to bob" | The README's "What this lab does *not* show" section and the deck's boundary slide both draw the line: it proves only that the **server** cannot read the message. This is viva question 3 and essay Q2 |
| Copy-pasted logs — `SECRET_MESSAGE` is identical for every student, so the evidence string is not by itself attributable | The identity proof (`whoami` / login / student ID + timestamp) in the same capture is the attributable part; viva spot-check anyone whose capture lacks it |
| A student finishes both runs long before 1:45 | Extension: read `common.hybrid_encrypt` and say exactly which field of the base64 envelope the server would need to decrypt, and why holding it does not help; or answer viva question 2 in writing (what alice does with bob's public key, and why the relay that carried both cannot decrypt) |

## 9. Post-teaching reflection

*Complete after the session — this also feeds the course's engagement data.*

- Attendance / completion: ⬚
- Time actually taken per block (vs. plan), especially whether the essay block over-ran: ⬚
- How many students produced a `0` from an already-torn-down stack, or a `1` from a grep missing
  `server`: ⬚
- Where the class got stuck, and what unblocked them: ⬚
- Misconception that showed up in the Part 2c EiPE answers (did they explain the lock icon in
  ordinary words, or fall back on jargon?): ⬚
- Quality of the Part 2b critiques — did students attack the TLS claim instead of the stored/logged
  plaintext? ⬚
- How many students over-claimed what the demo proves (authentication vs. confidentiality)? ⬚
- Anything to change before this week runs again: ⬚
