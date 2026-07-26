# Lesson Plan — Week 15: Post-Quantum Cryptography — Lamport One-Time Signatures & Key Reuse

| | |
|---|---|
| **Course** | Security & Cryptography (⬚ course code) |
| **Week / date** | 15 · ⬚ |
| **Kind** | LAB (runnable vulnerable/fixed pair + per-student flag) |
| **Contact time** | 300 min = 120 lecture + 180 laboratory |
| **Lab folder** | `labs/week15-pqc` |
| **Slides** | `slides/week15.md` |
| **Signature game** | 🔑 "Forge the Admin Signature" |
| **Standards** | Analogous CWE (per lab README / `lesson.yml`): CWE-323 (Reusing a Nonce/Key Pair in Encryption — the vulnerable app's exact flaw) · CWE-347 (Improper Verification of Cryptographic Signature) |
| **CLOs addressed** | **CLO2** break the misuse · **CLO3** rebuild/confirm the fix · **CLO4** reason about the PQC migration (schedule table, spec §6) — plus **CLO5** (Audit the AI, EiPE, Prompt Problem) and **CLO6** (Evidence & Integrity) via the recurring worksheet parts (spec §4) |

---

## 1. Session objectives

By the end of this week a student can:

**Knowledge (K)**
- K1 — Distinguish **Shor** from **Grover**: Shor breaks **RSA and ECC outright** (it solves factoring / discrete log efficiently), whereas Grover only **square-roots** symmetric/hash security — a quadratic speedup, mitigated by **doubling** the key/output length, not a break.
- K2 — Explain "**harvest now, decrypt later**" and why it makes PQC migration urgent *today* even though no large quantum computer yet exists, naming one data category with a long confidentiality lifetime.
- K3 — Name the **four PQC families** (lattice, hash-based, code-based, multivariate) and state what NIST's **ML-KEM** (from Kyber, a KEM) and **ML-DSA** (from Dilithium, a signature) are each *for*.
- K4 — Explain the **Lamport** construction (private key = two preimages per message bit, `pk[i] = (H(a_i), H(b_i))`, a signature reveals one preimage per bit) and its defining limitation: a Lamport keypair is a **one-time signature (OTS)** — provably secure **iff** it signs exactly one message.

**Skills (P)**
- P1 — In `vulnerable_app.py`, identify (a) the line generating the private key as *two preimages per bit*, (b) the line that reuses the one keypair on every `/sign`, and (c) the shared-baseline line that refuses to sign the admin message directly (Task 0).
- P2 — `POST /sign {"message_hex":"00000000"}` against `:8100`, then verify by hand that `SHA256(sig[0]) == pk[0][0]` but `SHA256(sig[0]) != pk[0][1]`, and state which half of bit 0's key stays secret (Task 1).
- P3 — `POST /sign {"message_hex":"ffffffff"}` (the complement); for one chosen bit position print **both** recovered preimages and show both `SHA256(...)` matching `pk[i][0]` and `pk[i][1]` (Task 2).
- P4 — Run `python exploit.py`, read the personalised flag, then reproduce the forgery manually and `POST /admin {sig}` with `curl` against the admin message `0xA5A5C3C3` (Task 3).
- P5 — Run the identical attack against `:8101`, observe the **second** `/sign` refused (`403` "one-time key already used"), and identify the **one block** in `fixed_app.py`'s `sign_endpoint` that differs from the vulnerable app (Task 4).

**Attitude (A)**
- A1 — Attack only the two local containers this lab spins up (`:8100` / `:8101`); forging signatures or authentication tokens against systems you do not own is illegal — keep the key, the signatures and `FLAG_PQC` inside the lab. See [ETHICS.md](../../ETHICS.md).
- A2 — Submit identity-stamped evidence (`whoami` / login email / student ID + a timestamp) and a **per-student** flag that is your own, and be able to reproduce it live on request.
- A3 — Treat AI-generated cryptographic code as something to *verify, not trust* — the *Audit the AI* snippet runs, type-checks and produces signatures that verify, yet reuses one key for every message.

## 2. Key ideas (the through-line)

A hash-based signature is **textbook-secure on a single assumption** — the preimage resistance of a
hash, which Grover only dents rather than breaks — which is exactly why it is a post-quantum family.
But that security is conditional: a Lamport keypair is a **one-time** signature. Signing one message
reveals, per bit, only the *one* preimage that bit's value selects; the other half of the key stays
secret, so a single signature is safe. Sign a second message that differs — and the **bitwise
complement `~M` differs in every bit** — and the attacker now holds *both* preimages for *every*
position: the entire private key, recovered by algebra, no brute force. From there any message can be
forged, including the `grant_admin` message the server *refused* to sign. The fix is **operational,
not mathematical**: refuse the second signature. No bigger key, no new algorithm — "one signature,
period." This is the week's spine: a **textbook-secure primitive that fails in the real system when
the usage discipline is broken**, and the engineering lesson that outlives any single algorithm is
**crypto-agility** — the difference between *a scheme being secure* and *a scheme being used
securely*.

## 3. Prior knowledge and preparation

- **Students, before class:** Docker Desktop working (same Docker-first setup as `software-security`);
  skim **Week 3 (MACs)** and **Week 5 (Key Exchanges)** — this week is where the *quantum* threat to
  those primitives lands. Have Python 3.12 (or at least the `requests` package) on the host to run
  `exploit.py` (worksheet Part 3 prerequisites).
- **Instructor, before class:** both lab containers `pip install --no-cache-dir -r requirements.txt`
  (`flask`, `requests`) at container start, so the *first* `docker compose up` needs working network
  to pull `python:3.12-slim` and install the dependencies. Pre-pull the base image and do one dry run
  so the room is not installing simultaneously. If per-student flags are in use, generate the `.env`
  first (see §5). Decide up front whether to set `LAMPORT_SEED` (reproducible keypair for grading) or
  leave it unset (fresh random key each boot) — see §8.
- **Prerequisite concepts:** what a cryptographic hash and preimage resistance are; the idea of a
  digital signature (integrity + non-repudiation) from the signatures/authentication weeks; reading
  a small Flask app.

## 4. Lecture — 120 min

Content and speaker prompts track `slides/week15.md`.

| Time | Block | Content | Method |
|---|---|---|---|
| 0:00–0:10 | Weekly quiz + recap | ~10-min retrieval quiz on Week 14 (authentication); bridge (a signature proves *what was said*; the primitive behind signatures is itself under quantum threat); today's agenda | Individual quiz, lowest 1–2 dropped |
| 0:10–0:55 | Core concepts | Shor vs. Grover (Shor breaks RSA/ECC outright; Grover only halves symmetric/hash security → double the length); "harvest now, decrypt later"; the four PQC families + NIST ML-KEM / ML-DSA (FIPS 203 / 204 / 205); the Lamport OTS construction; **what one signature reveals** (live: `POST /sign 00000000`, show `SHA256(sig[0]) == pk[0][0]` but `!= pk[0][1]`) | Lecture + board work + live demo on the projector |
| 0:55–1:05 | Break | | |
| 1:05–1:35 | Misuse deep-dive | The break — sign `M = 0x00000000` **and** its complement `~M = 0xFFFFFFFF`; every bit differs, so the two signatures reveal both preimages for every position (the whole private key); worked example: forge a signature on the admin message `0xA5A5C3C3` **offline**; **CWE-323** | Lecture + walk `exploit.py`'s `recover_and_forge` line by line |
| 1:35–1:55 | Correct construction / defences | The fix is operational: `fixed_app.py` signs **at most once**, any 2nd `/sign` → `403`; "one signature, period" (a retry must cache the first signature, never re-sign); stateful (XMSS/LMS) vs. stateless (SPHINCS+ / SLH-DSA, FIPS 205); crypto-agility; **CWE-347** | Lecture with code-diff comparison of `vulnerable_app.py` vs `fixed_app.py` |
| 1:55–2:00 | Signature-game briefing | 🔑 "Forge the Admin Signature" — recover the key from two reused signatures on `:8100`, forge, capture the flag; then prove the identical attack is *defeated* on `:8101` | Instruction → to lab |

**Checks for understanding during lecture**
- After Shor vs. Grover: cold-call — *"if Grover roughly halves AES-256's effective security, is AES-256 still safe post-quantum?"* (yes — hence the doubling mitigation; contrast RSA/ECC, where no length increase saves them).
- Before the break: one-minute paper — *"why sign the complement `~M` specifically, rather than any second message?"* (it guarantees every bit differs, so both preimages leak for every position — nothing wasted).
- At the end: cold-call — *"name the CWE for the vulnerable app's flaw."* (CWE-323).

## 5. Laboratory — 180 min

Targets: `docker compose up -d` in `labs/week15-pqc` → `vulnerable_app.py` (reuses one Lamport
keypair) on **`:8100`**, `fixed_app.py` (enforces one-time use) on **`:8101`**. Both hold ONE fixed
Lamport keypair over a 32-bit message signed **directly** (no pre-hash); both expose
`POST /sign`, `POST /verify`, `POST /admin` and `GET /pubkey`, and both **refuse to sign the reserved
admin message `0xA5A5C3C3` directly** (`403`) — the shared baseline, so the flag is never a one-line
`curl`. The *only* difference between the two apps is the one-time enforcement.

**Environment setup** (from the worksheet, quoted exactly):
```bash
cd labs/week15-pqc
docker compose up -d        # vulnerable_app.py on :8100, fixed_app.py on :8101
curl localhost:8100/        # confirm it's up
curl localhost:8100/pubkey  # inspect the public key + admin message (0xA5A5C3C3)
```
Per-student flag (from the README, run inside `labs/week15-pqc` *before* `docker compose up`):
```bash
python3 ../../instructor/seed_flags.py env <STUDENT_ID> > .env
```
*(challenge key `pqc`; see §8 for a staleness note on the README/compose comments around this recipe.)*

Laboratory table — **one row per actual worksheet task, with the worksheet's own minute budgets**.
The six numbered tasks (0–5) budget to **130 min**; the remaining 50 min is the onboarding and the
recurring AI-resilient / micro-demo / submit blocks from AGENDA.md's LAB-week template. No per-task
budget has been altered (see the note under the table).

| Time | Task | Budget | Student does | Evidence produced |
|---|---|---|---|---|
| 0:00–0:15 | **Onboarding** — stand up the target | 15 min (AGENDA) | `docker compose up -d`; `curl localhost:8100/`; `curl localhost:8100/pubkey` | Both apps up; captured public key + admin message |
| 0:15–0:30 | **Task 0 — Onboarding** (see the construction & the bug) | 15 min | Read `vulnerable_app.py`'s `sign`, `verify`, `sign_endpoint`; identify (a) two-preimages-per-bit key generation, (b) the reused keypair, (c) the admin-message refusal | Quoted lines (a)–(c) + one sentence on why (c) is necessary for the lab to have any challenge |
| 0:30–0:50 | **Task 1 — Understand what one signature reveals** | 20 min | `POST /sign {"message_hex":"00000000"}` on `:8100`; `GET /pubkey`; verify by hand `SHA256(sig[0]) == pk[0][0]` and `SHA256(sig[0]) != pk[0][1]` | The two hash comparisons for bit 0 + one sentence: which half of bit 0's key is still secret |
| 0:50–1:20 | **Task 2 — Recover the whole key with two signatures** | 30 min | `POST /sign {"message_hex":"ffffffff"}` (the complement); read `exploit.py`'s `recover_and_forge` self-check | For **one** bit position: both recovered preimages + both `SHA256(...)` matching `pk[i][0]` and `pk[i][1]` |
| 1:20–1:40 | **Task 3 — Forge and cash in the flag** | 20 min | `python exploit.py` → note the flag; then reproduce the forgery by hand and `POST /admin {sig}` with `curl` | The flag + the `curl` command and its output + one sentence on why the server accepts a signature on a message it refused to sign for you |
| 1:40–2:00 | **Task 4 — Confirm one-time enforcement defeats the attack** | 20 min | Run the same attack against `:8101` (`exploit.py` already does); observe the 2nd `/sign` → `403`; read `fixed_app.py`'s `sign_endpoint` | The rejection evidence + the one-block diff (in words) between the two `sign_endpoint` functions + one sentence on why one signature cannot forge admin |
| 2:00–2:25 | **Task 5 — Explain why, precisely** | 25 min | Answer in own words: (a) why one signature leaks half the key but `M`+`~M` leaks all; (b) *scheme secure* vs *scheme used securely*; (c) how SPHINCS+ stays stateless yet dodges reuse | Three short paragraphs, one per sub-question |
| 2:25–2:45 | **AI-resilient tasks** | 20 min (AGENDA) | *Audit the AI* (find the catastrophic key-reuse flaw in the `LamportSigner` snippet, explain why hashing-first does **not** save it, rewrite it safely); *Explain-in-Plain-English*; *Prompt Problem* | Written answers (start in class, finish as homework) |
| 2:45–2:55 | **Rotating micro-demo** | 10 min (AGENDA) | 2–3 rotating students give a 2–3 min "show your exploit / show the fix" | Live reproduction |
| 2:55–3:00 | **Submit** | 5 min (AGENDA) | Everyone submits | Worksheet PDF + flag → Classroom; exploit code → GitHub ([SUBMISSION.md](../../SUBMISSION.md)) |

> **Timing note for the instructor.** The worksheet titles Part 3 "Hands-on Lab (180 min)", which is
> the whole lab-session length; its six numbered tasks (0–5) budget to **130 min** (15 + 20 + 30 + 20
> + 20 + 25). The table above places those 130 min at 0:15–2:25 exactly as the worksheet states them,
> and fills the rest of the 180-min session with the onboarding and the recurring AI-resilient /
> micro-demo / submit blocks from AGENDA.md's LAB-week template — no per-task budget has been altered.
> **Evidence & Integrity** is not a separate block here: the worksheet requires the identity-stamped
> screenshots (`whoami` / login email / student ID + timestamp) to be captured *during* Tasks 1–4, so
> that evidence is produced inside the task rows above. If a group races ahead, start the AI-resilient
> tasks early; if they stall, Task 5 (reasoning) is the one to begin in class and finish as homework.

**Formative checkpoints.** A student stuck at Task 2 is usually trying to run `exploit.py` before
grasping *why* signing `M` and `~M` yields both preimages — send them back to Task 1's hash
comparison and the observation that the two messages differ in **every** bit, not to more `curl`.
Tasks 0–3 must be done by ~1:40 for the fix confirmation (Task 4) and the reasoning (Task 5) to fit;
a student who cannot land the forgery by then should switch to Task 4/5 (both run off the same
`python exploit.py`) and return.

## 6. Assessment for this week

Worksheet 15's own rubric (100 points):

| Criterion | Points | Assesses |
|---|---|---|
| Part 2 — Conventional written questions (Q1–Q8) | 25 | CLO1, CLO4 |
| Part 3 — Lab tasks 0–5 (hash comparisons, recovered preimages, curl output) | 30 | CLO2, CLO3 |
| Evidence & Integrity (flag capture + own-words explanation) | 10 | CLO6 |
| Audit the AI (catastrophic flaw found + hashing-first nuance + corrected design) | 20 | CLO5 |
| Comprehension & Prompt (EiPE + Prompt Problem) | 15 | CLO5 |

How the 100-point worksheet feeds the course marks (spec §4):

| Instrument | Outcome | Course weight |
|---|---|---|
| Worksheet 15 (all parts above) | CLO1–CLO6 | Part of the 30% weekly-worksheet component |
| Weekly quiz (start of lecture) | CLO1–CLO2 | Part of the 10% quiz + participation component |
| Viva spot-check / micro-demo | Live reproduction and explanation | Pass/fail gate on the Lab + Audit-the-AI scores (worksheet.md's own rubric footer — spec §9 only establishes that viva spot-checks sample submitted work weekly, not this specific gate mechanism) — an instructor who is not convinced you did the work may re-score those sections down |
| Per-student flag | Attributable evidence | Integrity control, not a separate mark |

The three viva spot-check questions are printed in the student worksheet itself (`worksheet.md`,
"🎤 Viva spot-check" heading) — students already see them when they open the file to do the lab, so
there is nothing to pre-circulate; the viva is a live-reproduction/explanation check, not a
surprise-question test. What is instructor-only is the *expected answers*, held in
`instructor/week15-pqc-answer-key.md` (not reproduced here). Grading detail and partial-credit
rules are in the worksheet's own rubric.

## 7. Materials

- Lab: `labs/week15-pqc/` — `vulnerable_app.py` (`:8100`), `fixed_app.py` (`:8101`), `exploit.py`,
  `docker-compose.yml`, `requirements.txt` (`flask>=3.1.3`, `requests>=2.33.0`), `worksheet.md`,
  `README.md`.
- Slides: `slides/week15.md`.
- Per-student flags: `instructor/seed_flags.py` (git-ignored thin shim → the curriculum monorepo's
  `tools/seed_flags.py`; challenge key `pqc`). See §5 for the `.env` recipe; `LAMPORT_SEED` makes the
  keypair deterministic for reproducible grading (unset = fresh random key each boot).
- Optional companion confidentiality lab: `labs/week15-pqc/hndl/` — 👀 "Harvest Now, Decrypt Later" +
  hybrid KEM (vulnerable `:8120` / fixed `:8121`, challenge key `hndl`, extra deps `pycryptodome`,
  `sympy`, `kyber-py`). The signature half (Lamport OTS, above) is the graded game this week; run
  `hndl/` as an extension if time allows (see §8).
- References (from the lab README and `readings.md`): NIST FIPS 203 (ML-KEM / Kyber), FIPS 204
  (ML-DSA / Dilithium), FIPS 205 (SLH-DSA / SPHINCS+); Bernstein & Lange, *Post-Quantum Cryptography*
  (survey); Lamport (1979), *Constructing Digital Signatures from a One-Way Function*; NIST,
  *Migration to Post-Quantum Cryptography* (NCCoE); the Wikipedia "Lamport signature" and "Shor's
  algorithm" articles.
- Submission channels: [SUBMISSION.md](../../SUBMISSION.md) · Rules of engagement: [ETHICS.md](../../ETHICS.md).

## 8. Risks and contingencies

| Risk | Mitigation |
|---|---|
| First `docker compose up` stalls because the containers `pip install` `flask` / `requests` at startup and the room's network is slow | Pre-pull `python:3.12-slim` and do one dry run; `exploit.py`'s `wait_for` waits up to 40 s per app, so confirm both answer `curl localhost:8100/` and `localhost:8101/` before students start |
| Ports **8100** / **8101** already bound on a student's machine | Override the published ports in `docker-compose.yml`; note these are 8100/8101, not 8080/5000, so the macOS AirPlay-on-5000 clash does not apply here |
| Keypair is **random each boot** when `LAMPORT_SEED` is unset — a student who collects one `/sign`, then restarts the container, gets a *different* key and their preimages no longer match | Collect both `/sign` responses against the **same running container**; for reproducible grading (or to hand-check a student's numbers) set `LAMPORT_SEED=<anything>` before `docker compose up` |
| `fixed_app.py` keeps **module-level one-time state** (`_signed_message`): once `:8101` has signed *once*, every later `/sign` is refused for the life of the container — so a student who wastes the first signature on `:8101` on the wrong message is stuck | This is the intended behaviour (one signature, period). To retry, `docker compose restart fixed` (or `down`/`up`) to reset the state; warn students the fixed app's first `/sign` is their only one |
| Student fires the exploit at the wrong port, or expects `:8101` to yield a flag, and concludes "the attack fails" | Each app's `/` index states which it is (`:8100` REUSES the key = vulnerable; `:8101` enforces one-time = fixed). The win condition is flag captured on `:8100` **and** attack *defeated* on `:8101` — no flag on `:8101` is the *correct* result |
| Student tries the "one-line `curl`" shortcut — signing the admin message `a5a5c3c3` directly | **Both** apps `403` that request (verified); it is the shared baseline. The forgery must be assembled offline from the two collected signatures |
| Per-student `.env` not generated, so everyone recovers the same default flag → non-attributable submissions | Generate `python3 ../../instructor/seed_flags.py env <STUDENT_ID> > .env` before `docker compose up`; the personalised flag + identity-stamped screenshots are the integrity control |
| Optional `hndl/` companion pulls heavier dependencies (`pycryptodome`, `sympy`, `kyber-py`) and doubles the network/build time | Only offer `hndl/` as an early-finisher extension; pre-pull/warm those deps beforehand, and keep the graded game on the lighter Lamport lab (`flask` + `requests` only) |
| README and `docker-compose.yml` comments carry a **stale** per-student-flag note — they say `seed_flags.py` does not yet exist and tell you to "add a `pqc` entry to its `CHALLENGES` list", but the tool now exists as a shim and `pqc` is already registered via the monorepo's `lessons/pqc/lesson.yml` `flag_keys` (there is no hand-maintained `CHALLENGES` list) | Use the recipe in §5 as-is (it works); ignore the "once … exists / add to `CHALLENGES`" wording. Reported in `escalated` — do not edit the lab content to fix it here |
| `slides/week15.md` (lines 22 and 140) labels the signature game with 🔓, not 🔑 — that is the emoji `course-specification.md` §6 and `course-plan-19weeks.md` (line 85) assign to **Week 2**'s game ("Crack the Leaked DB"), so the deck now collides with a different week's marker | This plan's own 🔑 (§header, §4 briefing row) already matches `course-specification.md` §6 and `course-plan-19weeks.md`, so nothing here needs correcting — but say the emoji aloud when projecting the deck so it doesn't read as Week 2's game. Reported in `escalated`; do not edit the deck to fix it here |

Remember to `docker compose down` at the end of the session (and, if the companion ran,
`docker compose down` inside `hndl/` too).

## 9. Post-teaching reflection

*Complete after the session — this also feeds the course's engagement data.*

- Attendance / completion: ⬚
- Time actually taken per task (vs. plan — the 130-min task budget is unexercised with real students): ⬚
- Where the class got stuck (Task 2 intuition vs. Task 3 execution), and what unblocked them: ⬚
- Misconception that showed up in the *Explain-in-Plain-English* answers (e.g. "quantum breaks all crypto", or that hashing-first fixes reuse): ⬚
- Quality of the *Audit the AI* critiques — did students catch the key reuse *and* correctly reason that hashing-first only changes *which* bits leak, not *whether* reuse leaks?: ⬚
- Anything to change before this week runs again: ⬚
