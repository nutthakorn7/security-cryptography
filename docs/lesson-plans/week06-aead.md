# Lesson Plan — Week 6: Authenticated Encryption (AEAD) — the CBC Padding Oracle

| | |
|---|---|
| **Course** | Security & Cryptography (⬚ course code) |
| **Week / date** | 6 · ⬚ |
| **Kind** | LAB (runnable vulnerable/fixed pair + per-student flag) |
| **Contact time** | 300 min = 120 lecture + 180 laboratory |
| **Lab folder** | `labs/week06-aead` |
| **Slides** | `slides/week06.md` |
| **Signature game** | 🔮 "Read the Secret Without the Key" |
| **Standards** | Analogous CWE (per lab README): CWE-347 (Improper Verification of Cryptographic Signature) · CWE-757 (Selection of Less-Secure Algorithm) · CWE-204 (Observable Response Discrepancy — the side channel) |
| **CLOs addressed** | **CLO1** select & justify the primitive · **CLO2** break the misuse · **CLO3** rebuild it correctly (schedule table, spec §6) — plus **CLO5** (Audit the AI, EiPE, Prompt Problem) and **CLO6** (Evidence & Integrity) via the recurring worksheet parts (spec §4) |

---

## 1. Session objectives

By the end of this week a student can:

**Knowledge (K)**
- K1 — State what **AEAD** stands for and the three guarantees it delivers in one primitive (confidentiality, integrity, authenticity), naming the attack each stops.
- K2 — Explain why unauthenticated CBC is *malleable* using `P_i = D(C_i) XOR C_{i-1}`, and why a padding-validity side channel turns that malleability into full decryption ("malleability weaponised into full decryption").
- K3 — Give the two independent reasons AES-GCM has no padding oracle — it is a *stream* mode (no padding to probe) and it verifies the tag *before* releasing plaintext — and say why returning a single *uniform* error also matters.
- K4 — Distinguish **encrypt-then-MAC** (the provably safe generic composition) from **MAC-then-Encrypt** and **Encrypt-and-MAC**, in terms of what the verifier gets to touch before the MAC is checked.

**Skills (P)**
- P1 — In `vulnerable_app.py`'s `/decrypt`, identify the exact line where a `200` and a `403` diverge and confirm that *only* the `pkcs7_valid` PKCS#7 check distinguishes them (Task 0).
- P2 — Capture the target from `GET /secret`, base64-decode it, and state its length in bytes and how many 16-byte blocks that is after subtracting the IV block (Task 1).
- P3 — Explain one oracle query: derive `D(C_t)[15] = winning_guess XOR 0x01`, and describe the `…0x02 0x02` false-positive and the neighbour-byte re-query that disambiguates it (Task 2).
- P4 — Run `python exploit.py` to recover the plaintext byte-by-byte without the key, read the personalised flag, and reproduce **one** oracle query manually with `curl` against `/decrypt` (Task 3).
- P5 — Run the identical attack against `:8099` (AES-GCM), confirm the "no usable padding signal … nothing recovered" evidence, and point to the two `fixed_app.py` lines that (a) make every failure a uniform `403` and (b) verify the tag before any plaintext is used (Tasks 4–5).

**Attitude (A)**
- A1 — Attack only the two local containers this lab spins up (`:8098` / `:8099`); a padding oracle is a real, deployed-in-the-wild attack (POODLE, Lucky-13, named in the worksheet's ethics note) and running it against systems you do not own is illegal — keep key, ciphertext and flag inside the lab. See [ETHICS.md](../../ETHICS.md).
- A2 — Submit identity-stamped evidence (`whoami` / login email / student ID + a timestamp) and a per-student flag that is your own, and be able to reproduce it live on request.
- A3 — Treat AI-generated cryptographic code as something to *verify, not trust* — the *Audit the AI* helper "looks careful" yet reintroduces the padding oracle through its error handling.

## 2. Key ideas (the through-line)

Authentication is not optional decoration on top of encryption; it is what makes ciphertext safe to
*receive*. This week is the capstone of the symmetric block: Week 3 gave a MAC (integrity), Week 4
gave AES-CBC (confidentiality) and showed CBC ciphertext is *malleable*. Bolt those two together
**wrong** — confidentiality with no integrity, plus an endpoint that reveals one observable
difference about ciphertext it never authenticated (here, whether PKCS#7 padding was valid) — and
you get a **padding oracle**: the attacker decrypts the secret byte-by-byte, without ever learning
the key, from nothing but a `200`-vs-`403` signal. Bolt them together **right** — encrypt-then-MAC,
or a single **AEAD** primitive such as AES-GCM — and the attack evaporates, because the cipher checks
a tag *before* any padding logic runs and returns one uniform error. The fix is structural, not a
smarter filter: make the ciphertext unforgeable in the first place, so the question the oracle asks
("is this padding valid?") is never answerable to an attacker.

## 3. Prior knowledge and preparation

- **Students, before class:** Docker Desktop working (same Docker-first setup as `software-security`);
  re-skim **Week 4** (AES-CBC, bit-flipping malleability) and **Week 3** (MACs) — this week is those
  two combined. Have Python 3.12 (or at least the `requests` package) on the host to run `exploit.py`.
- **Instructor, before class:** the lab containers `pip install --no-cache-dir -r requirements.txt`
  at container start, so the *first* `docker compose up` needs working network to pull
  `python:3.12-slim` and install `flask` / `cryptography` / `requests`. Pre-pull the base image and
  do one dry run so the room is not installing dependencies simultaneously. If per-student flags are
  in use, generate the `.env` first (see §5).
- **Prerequisite concepts:** the CBC decryption relation `P_i = D(C_i) XOR C_{i-1}`; what PKCS#7
  padding is; what a MAC provides that a bare cipher does not.

## 4. Lecture — 120 min

| Time | Block | Content | Method |
|---|---|---|---|
| 0:00–0:10 | Weekly quiz + recap | ~10-min retrieval quiz on Week 5 (key exchanges); today's agenda | Individual quiz, lowest 1–2 dropped |
| 0:10–0:55 | Core concepts | What AEAD guarantees (confidentiality + integrity + authenticity in one primitive); the three safe/unsafe compositions — Encrypt-then-MAC vs MAC-then-Encrypt vs Encrypt-and-MAC and why only the first is provably safe; the AEAD API idea (RFC 5116) | Lecture + board work |
| 0:55–1:05 | Break | | |
| 1:05–1:35 | Misuse deep-dive + real cases | Why unauthenticated CBC leaks to a padding oracle: `P_i = D(C_i) XOR C_{i-1}`, forcing padding `0x01`, then `0x02 0x02`, … to recover one byte of `D(C_t)` per round; brief real cases named in the worksheet — POODLE and Lucky-13 | Lecture + live walkthrough on the projector |
| 1:35–1:55 | Correct construction / defences | Why AES-GCM has no padding step (stream/CTR mode) and checks the 128-bit tag *before* releasing plaintext; why a *uniform* error closes the side channel; associated data (the AD in AEAD); the "forgot to check the tag" trap | Lecture with code-diff comparison of `vulnerable_app.py` vs `fixed_app.py` |
| 1:55–2:00 | Signature-game briefing | 🔮 "Read the Secret Without the Key" — recover the secret from the `:8098` oracle, then prove `:8099` (AES-GCM) gives no signal | Instruction → to lab |

**Checks for understanding during lecture**
- After the core concept: cold-call — *"which of the three compositions lets the verifier touch attacker-chosen plaintext before the MAC is checked, and why is that fatal?"* (ties to worksheet Q2).
- Before the break: one-minute paper — *"the endpoint never returns the plaintext, only 200 or 403 — why is that still enough to decrypt the whole secret?"* (ties to Q3 and viva question 2).

## 5. Laboratory — 180 min

Targets: `docker compose up -d` in `labs/week06-aead` → `vulnerable_app.py` (AES-256-CBC,
unauthenticated) on **`:8098`**, `fixed_app.py` (AES-256-GCM, AEAD) on **`:8099`**. Both serve the
same secret (which contains the flag) at `GET /secret` as `base64(IV||ct)` / `base64(nonce||ct||tag)`
and expose `POST /decrypt {"ciphertext": "<base64>"}`.

**Environment setup** (from the worksheet, quoted exactly):
```bash
cd labs/week06-aead
docker compose up -d        # vulnerable_app.py on :8098, fixed_app.py on :8099
curl localhost:8098/        # confirm it's up
curl localhost:8098/secret  # base64(IV||ct) of the secret that contains your flag
```
Per-student flag (from README, run inside `labs/week06-aead` *before* `docker compose up`):
```bash
python3 ../../instructor/seed_flags.py env <STUDENT_ID> > .env
```

Laboratory table — **one row per actual worksheet task, with the worksheet's own minute budgets**.
The six numbered tasks (0–5) budget to **100 min**; the remaining lab time is the onboarding and
the recurring AI-resilient / micro-demo / submit blocks per AGENDA.md's LAB-week template, plus
Evidence & Integrity from `worksheet.md`'s own required section (AGENDA's LAB-week template has no
Evidence & Integrity row — see the note under the table).

| Time | Task | Budget | Student does | Evidence produced |
|---|---|---|---|---|
| 0:00–0:15 | **Onboarding** — stand up the target | 15 min (AGENDA) | `docker compose up -d`; `curl localhost:8098/`; `curl localhost:8098/secret` | Both apps up; captured `base64(IV\|\|ct)` |
| 0:15–0:25 | **Task 0 — Onboarding** (see the oracle) | 10 min | Read `vulnerable_app.py`'s `/decrypt` handler and `pkcs7_valid`; find the exact line where a `200` and a `403` diverge; confirm only the PKCS#7 check distinguishes them | The quoted line + one sentence on why "never returns the plaintext" is not safe |
| 0:25–0:30 | **Task 1 — Grab the ciphertext** | 5 min | `curl localhost:8098/secret`; base64-decode; note its length | Ciphertext length in bytes + block count *after* subtracting the IV block |
| 0:30–1:00 | **Task 2 — Understand one oracle query** | 30 min | Read `exploit.py`'s `recover_intermediate`; on paper, work the last block `C_t` submitted as `forged_prev \|\| C_t` | Three short answers + the formula `D(C_t)[15] = winning_guess XOR 0x01` |
| 1:00–1:20 | **Task 3 — Recover the plaintext & read the flag** | 20 min | `python exploit.py`; then reproduce **one** oracle query manually with `curl` (POST a `forged_prev \|\| C_t` blob to `/decrypt`) | Recovered plaintext, the personalised flag, and one manual `curl` query + its status code |
| 1:20–1:35 | **Task 4 — Confirm AES-GCM rejects the same attack** | 15 min | Watch `exploit.py` re-run against `:8099`; read `fixed_app.py`'s `/decrypt` for (a) the uniform-`403` line and (b) where the tag is verified relative to plaintext use | "nothing recovered" evidence + the two identified lines, one sentence each |
| 1:35–1:55 | **Task 5 — Explain why, precisely** | 20 min | Answer (a) per-byte oracle on `D(C_t)`, (b) why GCM's stream structure has no padding question, (c) why tag-first + uniform error kills the oracle even if GCM did pad | Three short paragraphs |
| 1:55–2:25 | **Evidence & Integrity** (+ buffer) | 30 min | Capture identity-stamped screenshots (`whoami` / login email / student ID + timestamp) for Tasks 1–4; record the personalised flag; write the two own-words explanations | Flag + own-words explanation of *why it worked* and *why GCM stops it* |
| 2:25–2:45 | **AI-resilient tasks** | 20 min (AGENDA) | *Audit the AI* (find the padding-oracle-via-error-codes flaw + the deeper design flaw in the AI "safe CBC decrypt" helper, then rewrite it as AEAD); *Explain-in-Plain-English*; *Prompt Problem* | Written answers (start in class, finish as homework) |
| 2:45–2:55 | **Rotating micro-demo** | 10 min (AGENDA) | 2–3 rotating students give a 2–3 min "show your exploit / show the fix" | Live reproduction |
| 2:55–3:00 | **Submit** | 5 min (AGENDA) | Everyone submits | Worksheet PDF → Classroom; exploit notes/fix → GitHub ([SUBMISSION.md](../../SUBMISSION.md)) |

> **Timing note for the instructor.** The worksheet titles Part 3 "Hands-on Lab (180 min)", which is
> the whole lab-session length; its six numbered tasks (0–5) budget to **100 min**. The table above
> places those 100 min at 0:15–1:55 exactly as the worksheet states them, and fills the rest of the
> 180-min session with the onboarding and recurring AI-resilient / micro-demo / submit blocks from
> AGENDA.md's LAB-week template, plus an Evidence & Integrity block drawn from `worksheet.md`'s own
> required section (AGENDA's LAB-week template has no such row; its equivalent slot reads "Defend /
> fix task," which this week's worksheet replaces with its own task 0–5 structure) — no per-task
> budget has been altered. If a group races ahead, the 1:55–2:25 window absorbs the slack; if they
> stall, Task 5 (reasoning) is the one to start in class and finish as homework.

**Formative checkpoints.** A student stuck on Task 2 is usually trying to run the exploit before
understanding *why* forcing padding to `0x01` reveals `D(C_t)[15]` — send them back to
`recover_intermediate` and the `pad_val == 1` branch, not to more `curl`. Tasks 0–3 must be done by
~1:20 for the GCM confirmation (Task 4) and reasoning (Task 5) to fit; a student who cannot land the
recovery by then should switch to Task 4/5 (which run off the same `python exploit.py`) and return.

## 6. Assessment for this week

Worksheet 6's own rubric (100 points):

| Criterion | Points | Assesses |
|---|---|---|
| Part 2 — Conventional written questions (Q1–Q8) | 25 | CLO1, CLO3 |
| Part 3 — Lab tasks 0–5 (block count, one manual oracle `curl`, GCM "no signal") | 30 | CLO2, CLO3 |
| Evidence & Integrity (flag capture + own-words explanation) | 10 | CLO6 |
| Audit the AI (oracle-via-error-codes flaw found + corrected AEAD design) | 20 | CLO5 |
| Comprehension & Prompt (EiPE + Prompt Problem) | 15 | CLO5 |

How the 100-point worksheet feeds the course marks (spec §4):

| Instrument | Outcome | Course weight |
|---|---|---|
| Worksheet 6 (all parts above) | CLO1, CLO2, CLO3, CLO5, CLO6 | Part of the 30% weekly-worksheet component |
| Weekly quiz (start of lecture) | CLO1–CLO2 | Part of the 10% quiz + participation component |
| Viva spot-check / micro-demo | Live reproduction and explanation | Pass/fail gate on the Lab + Audit-the-AI scores (worksheet.md's own rubric note) — an instructor who is not convinced you did the work may re-score those sections down |
| Per-student flag | Attributable evidence | Integrity control, not a separate mark |

The three viva spot-check questions are printed verbatim inside `worksheet.md` itself, under its
own "🎤 Viva spot-check" heading — the same file every student completes and exports to PDF as
their graded submission ([SUBMISSION.md](../../SUBMISSION.md)), so they are **not** confidential
by construction; a student can read them before the instructor ever asks live. If secrecy is
intended, redact that section before distributing the worksheet, or move the three questions into
the git-ignored `instructor/week06-aead-answer-key.md`. Grading detail and partial-credit rules are
in the worksheet's own rubric.

## 7. Materials

- Lab: `labs/week06-aead/` — `vulnerable_app.py` (CBC, `:8098`), `fixed_app.py` (AES-GCM, `:8099`),
  `exploit.py`, `docker-compose.yml`, `requirements.txt`, `worksheet.md`, `README.md`.
- Slides: `slides/week06.md`.
- Per-student flags: `instructor/seed_flags.py` (git-ignored; see README for the `.env` recipe and
  the `FLAG_AEAD` env override — the exploit derives the block count from `/secret`, so flags of any
  length work).
- References (from the lab README): Boneh & Shoup, *A Graduate Course in Applied Cryptography*, ch. 9
  (Authenticated Encryption); Vaudenay (2002), *Security Flaws Induced by CBC Padding*; NIST SP
  800-38D (*GCM and GMAC*); RFC 5116 (*An Interface and Algorithms for Authenticated Encryption*);
  the Wikipedia "Padding oracle attack" article.
- Submission channels: [SUBMISSION.md](../../SUBMISSION.md) · Rules of engagement: [ETHICS.md](../../ETHICS.md).

## 8. Risks and contingencies

| Risk | Mitigation |
|---|---|
| First `docker compose up` stalls because the container installs `flask` / `cryptography` / `requests` at startup and the room's network is slow | Pre-pull `python:3.12-slim` and do one dry run; `exploit.py`'s `wait_for` only waits 60 s, so confirm both apps answer `curl localhost:8098/` and `localhost:8099/` before students start |
| Ports **8098** / **8099** already bound on a student's machine | Override the published ports in `docker-compose.yml`; note these are 8098/8099, not the 8080/5000 of the sibling `software-security` course, so the macOS AirPlay-on-5000 clash does not apply here |
| The padding-oracle run fires thousands of requests and exhausts local ephemeral ports against the Flask dev server (Errno 49 / connection resets) | `exploit.py` already reuses one keep-alive session and retries with a 0.25–2 s backoff; warn students *not* to write a naive tight-loop oracle of their own, and to let TIME_WAIT sockets drain rather than assuming a dropped socket is a padding signal |
| Student fires the exploit at the wrong port and concludes "the attack fails" | The `/` index page of each app states which cipher it is; reinforce `:8098` = vulnerable CBC (oracle), `:8099` = fixed GCM (no signal) |
| Per-student `.env` not generated, so everyone recovers the same default flag → non-attributable submissions | Generate `python3 ../../instructor/seed_flags.py env <STUDENT_ID> > .env` before `docker compose up`; the personalised flag + identity-stamped screenshots are the integrity control |
| OneDrive placeholder files break an in-place container/build on the instructor machine | Per the README's verification note, run from a scratch copy of the lab folder if an in-place run misbehaves |
| A student finishes recovery early | Extension: reproduce a *second* oracle query by hand and predict its `200`/`403` before sending; or explain (viva q.3) one *different* bug — e.g. ignoring `InvalidTag`, or GCM nonce reuse (Week 10) — that would reintroduce a decryption oracle even "using AEAD" |

Remember to `docker compose down` at the end of the session.

## 9. Post-teaching reflection

*Complete after the session — this also feeds the course's engagement data.*

- Attendance / completion: ⬚
- Time actually taken per task (vs. plan — the 100-min task budget is unexercised with real students): ⬚
- Where the class got stuck (Task 2 reasoning vs. Task 3 execution), and what unblocked them: ⬚
- Misconception that showed up in the *Explain-in-Plain-English* answers: ⬚
- Quality of the *Audit the AI* critiques — did students catch *both* the error-code oracle and the deeper "switch to AEAD" fix, or stop at hiding the status codes?: ⬚
- Anything to change before this week runs again: ⬚
