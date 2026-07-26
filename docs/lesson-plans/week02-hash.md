# Lesson Plan — Week 2: Hash Functions & Password Storage

| | |
|---|---|
| **Course** | Security & Cryptography (⬚ course code) |
| **Week / date** | 2 · ⬚ |
| **Contact time** | 300 min = 120 lecture + 180 laboratory |
| **Lab folder** | `labs/week02-hash` |
| **Slides** | `slides/week02.md` |
| **Kind** | LAB — runnable vulnerable/fixed pair + captured flag |
| **Signature game** | 🔓 "Crack the Leaked DB" |
| **Standards** | CWE-916 (insufficient computational effort) · CWE-327 (broken/risky algorithm) · CWE-759 / CWE-760 (one-way hash without a salt / with a predictable salt) · NIST SP 800-63B · OWASP Password Storage Cheat Sheet |
| **CLOs addressed** | **CLO1** select & justify · **CLO2** break · **CLO3** rebuild (schedule §6). The recurring worksheet parts additionally carry **CLO5** (Audit-the-AI, EiPE/Prompt) and **CLO6** (Evidence & Integrity), per course-spec §4 |

---

## 1. Session objectives

By the end of this week a student can:

**Knowledge (K)**
- K1 — State the three hash security properties — preimage, second-preimage, collision resistance — and name one concrete attack each prevents.
- K2 — Explain why an *unsalted, fast* hash (MD5/SHA-256) is the wrong tool for storing passwords, and what a slow KDF's *work factor / cost* actually controls about the attacker's per-guess cost.
- K3 — Explain what a *per-user random* salt defeats (precomputed rainbow tables; shared-hash correlation) and why the salt need not be secret.
- K4 — State the *one* property a plain hash, a MAC, and encryption each provide, and what a *pepper* adds over a salt.

**Skills (P)**
- P1 — Crack a leaked unsalted-MD5 admin hash with an offline dictionary attack (Python REPL over `wordlist.txt`, or `hashcat -m 0` / `john --format=raw-md5`), recovering the plaintext, and state why it was so fast.
- P2 — Turn the cracked password into a captured flag: log in and carry the *same session cookie* to `GET /admin`, then confirm `GET /admin` without the cookie returns `403`.
- P3 — Run `exploit.py` end-to-end and read the two `PASS` lines and exit code 0.
- P4 — Empirically confirm the bcrypt store resists the *same* md5-precompute technique (0 matches), and identify the one-line `/login` difference between `vulnerable_app.py` and `fixed_app.py`.
- P5 — Rewrite an insecure `store_password` / `verify_password` using a proper password KDF (bcrypt or argon2id) with a per-user random salt and a constant-time verify.

**Attitude (A)**
- A1 — Crack only the hashes shipped in this lab (`users_vulnerable.csv`, `wordlist.txt`) on the two local containers, under [ETHICS.md](../../ETHICS.md); keep recovered passwords and the flag inside the lab.
- A2 — Submit identity-stamped evidence (`whoami` / login email / student ID + timestamp) and a per-student flag that is attributable and reproducible live at a viva spot-check.
- A3 — Treat AI-generated cryptographic code as something to be verified, not trusted.

## 2. Key ideas (the through-line)

Storing a password is not "hashing" — it is deliberately *slow, per-user-salted key derivation*. A fast,
unsalted hash makes a leaked database cheap to break in two ways at once: one precomputed table
cracks *every* row of the file simultaneously (no per-user salt), and two users who chose the same
password produce the *same* stored hash. The fix is structural, not a smarter hash: a per-user random
salt kills the single-table / rainbow-table attack, and a tunable work factor raises the cost of each
individual guess by orders of magnitude. But bcrypt buys *work factor, not invincibility* — a weak,
in-wordlist password is still recoverable by a slow per-hash dictionary, just far more expensively.
That is why the correct construction is bcrypt/argon2/scrypt **paired with a strong-password policy**,
and why "SHA-256 has never been broken" answers the wrong question for password storage.

## 3. Prior knowledge and preparation

- **Students, before class:** Docker Desktop working (same Docker-first setup as `software-security`);
  skim the course intro on what a cryptographic hash is (a one-way, fixed-size digest). Have Python
  3.12 — or at least the `requests` package — on the host, which is all `exploit.py` needs to run.
- **Instructor, before class:** pre-pull the compose image `python:3.12-slim` before the session. Each
  container runs `pip install --no-cache-dir -r requirements.txt` (flask, requests, bcrypt) *at start*
  — a room of students pulling and installing at once is the most common way to lose the first 15–20
  minutes; keep an offline fallback ready (`docker save` / `docker load`). Confirm ports **8094** and
  **8095** are free. Decide the flag mode: the default `FLAG_HASH` is a shared placeholder, or mint a
  per-student flag now via `python3 ../../instructor/seed_flags.py env <STUDENT_ID> > .env` before
  `docker compose up` — this course's `instructor/seed_flags.py` exists and is verified end-to-end
  (course-plan-19weeks.md, "Decisions" item 5; it needs the sibling `KOSEN69 - curriculum` monorepo
  checkout and an `SC_FLAG_SALT` env var to run). What is *not* yet live is automatic, roster-checked
  attribution against a real cohort — there is no running CTFd instance for this course yet
  (course-plan-19weeks.md item 6, still open), so until then even a seeded per-student build's
  attribution still rests on identity-stamped evidence and the viva, not an automated roster check.
  (The lab's own `README.md` still carries the older "may not yet exist... open decision #4" hedge —
  that citation is itself stale, since course-plan-19weeks.md item 4 is the unrelated
  `airsec_flag_bridge` de-inline; this is a lab-content staleness, out of scope for this plan to fix.)
- **Prerequisite concept:** what a one-way digest is; the idea of a dictionary / wordlist attack;
  basic SQL is *not* needed this week.

## 4. Lecture — 120 min

| Time | Block | Content | Method |
|---|---|---|---|
| 0:00–0:10 | Weekly quiz + recap | ~10-min retrieval quiz (lowest 1–2 dropped); recap of Week 1 (threat-modelling / snake-oil); today's agenda | Individual quiz |
| 0:10–0:55 | Core concepts | Cryptographic hash as a one-way fixed-size digest; the three resistance properties and an attack each prevents; hash vs. MAC vs. encryption — which property each one actually provides (Q7) | Lecture + live coding (compute `md5` / `sha256` in a REPL on the projector) |
| 0:55–1:05 | Break | | |
| 1:05–1:35 | Misuse deep-dive + real cases | Why MD5 and SHA-1 are *broken*, and why that matters *differently* for password storage vs. digital signatures (which property is broken, which does each use rely on); why a fast hash is the wrong tool for passwords; how an unsalted store lets one precomputed table crack every row and reveals shared passwords; brief real leaks | Lecture + short discussion: "what would have stopped this?" |
| 1:35–1:55 | Correct construction / defences | Per-user random salt (defeats precomputed rainbow tables; need not be secret); slow KDFs (bcrypt / argon2 / scrypt) and what the work factor / cost controls; pepper vs. salt; the *don't-overclaim* point — bcrypt raises cost, it is not invincibility, so pair it with a strong-password policy | Lecture with a `vulnerable_app.py` vs. `fixed_app.py` `/login` code-diff |
| 1:55–2:00 | Brief the game | "Crack the Leaked DB" — crack the unsalted MD5 admin hash, capture the flag on `:8094`, then watch the identical attack bounce off the bcrypt store on `:8095` | Instruction → to lab |

**Checks for understanding during lecture**
- After the core concept: cold-call *"which resistance property does password storage actually rely on — and is that the one MD5 broke?"* (sets up Q2).
- Before the break: one-minute paper — *"why is 'SHA-256 is fast' a problem, not a feature, for stored passwords?"*

## 5. Laboratory — 180 min

Targets: `docker compose up -d` in `labs/week02-hash` → `vulnerable_app.py` on `:8094` (unsalted MD5)
and `fixed_app.py` on `:8095` (bcrypt). `exploit.py` scripts the full attack; students also reproduce
it by hand. Tasks, names and minute budgets below are taken verbatim from `worksheet.md` Part 3.

**Environment setup (from the worksheet):**
```bash
cd labs/week02-hash
docker compose up -d        # vulnerable_app.py on :8094, fixed_app.py on :8095
curl localhost:8094/        # confirm it's up
```

| Time | Task | Student does | Evidence produced |
|---|---|---|---|
| 0:00–0:10 | **Task 0 — Onboarding (10 min)** | Stand the two apps up; open `users_vulnerable.csv` and `vulnerable_app.py`; find the `/login` line that checks the password and confirm it is `hashlib.md5(password.encode()).hexdigest() == stored` (fast, no salt) | The quoted line + which of Q3/Q6's failure modes it matches |
| 0:10–0:35 | **Task 1 — Crack the admin hash by hand-ish (25 min)** | Read the `admin` row's md5 from `users_vulnerable.csv`; in a Python REPL, loop `wordlist.txt` computing `hashlib.md5(word.encode()).hexdigest()` until one equals it (may also confirm with `hashcat -m 0` or `john --format=raw-md5`) | Recovered plaintext + ~time taken + one line on *why* it was so fast (fast + unsalted → one table covers every row; CWE-916/759) |
| 0:35–0:50 | **Task 2 — Log in and capture the flag (15 min)** | Reproduce the login+flag manually, *keeping the cookie jar*, then hit `/admin` on the same jar; then try `GET /admin` *without* `-b "$JAR"` and confirm `403` | The flag + both curl outputs (with-jar → flag, without-jar → `403`) + one sentence on why the session cookie is required |
| 0:50–1:00 | **Task 3 — Run the full exploit (10 min)** | `python exploit.py`; note the two `PASS` lines and exit code 0 | The full script output pasted into the write-up |
| 1:00–1:20 | **Task 4 — Confirm bcrypt resists the fast technique (20 min)** | Open `users_fixed.csv` (hashes start `$2b$`); rebuild the md5 table over `wordlist.txt` and confirm it matches *none* of the bcrypt strings; read `fixed_app.py`'s `/login` and name the one-line change (`bcrypt.checkpw` vs. `md5(...) ==`) | The "0 matches" result + the one-line diff (in words) between the two `/login` checks |
| 1:20–1:40 | **Task 5 — Explain the cost, precisely (20 min)** | Answer in own words: (a) why one md5 table cracks every vulnerable row but zero bcrypt rows; (b) the admin's weak password *is* in the wordlist — could a patient attacker still recover it from bcrypt, and what stops that being cheap; (c) what *second* control makes a weak password safe | 3 short paragraphs, one per sub-question |
| 1:40–2:25 | **Write-up + Evidence & Integrity** (no worksheet minute budget — buffer) | Capture identity-stamped evidence (`whoami` / student ID + timestamp) for Tasks 1–4; record the personalised flag; finish Part 3 write-ups; catch-up time for anyone still on Tasks 1–2 | Identity-stamped screenshots + personalised flag entry |
| 2:25–2:45 | **AI-resilient tasks** (AGENDA standard block) | *Audit the AI* (find the planted flaw(s) in the AI's `store_password`/`verify_password`, then write the correct KDF-based version), *Explain-in-Plain-English*, *Prompt Problem* | Written answers + corrected KDF code (start in class, finish as homework) |
| 2:45–2:55 | **Rotating micro-demo** | 2–3 rotating students give a 2–3 min "show your crack / show the bcrypt bounce" | — |
| 2:55–3:00 | **Submit** | Worksheet PDF → Classroom; corrected code → GitHub (see [SUBMISSION.md](../../SUBMISSION.md)) | Submission confirmation |

**Formative checkpoints.**
- A student who "cracked it" but gets `403` from `/admin` almost always broke the *session*: two separate
  `curl` calls without the shared `$JAR`, or `requests` without a single `Session()`. Point them at the
  cookie-jar block in Task 2 (and the `requests.Session()` line in `exploit.py`) — this is the built-in
  teaching failure, not a bug.
- Tasks 1–4 must be finished by 1:40 for the write-up/AI block to fit; a student still stuck on Task 1
  at that point should pair for the crack, then complete Tasks 4–5 alone.
- **Timing note for the instructor:** the worksheet's Part 3 is headed "(180 min)" but its numbered
  Tasks 0–5 budget only **100 min** (10 + 25 + 15 + 10 + 20 + 20). The remaining lab time is the
  write-up/Evidence block plus the AI-resilient / micro-demo / submit blocks above. This is the exact
  open item AGENDA.md (lines 240–242) flags — "confirm actual worksheet task counts fill the 180-min
  block." It is reported in `escalated`; **do not shorten the worksheet's task budgets to make a table
  add up.**

## 6. Assessment for this week

| Instrument | Evidence | Outcome | Weight |
|---|---|---|---|
| Worksheet 2 — Part 2 (Q1–Q8), Part 3 (Tasks 0–5), Evidence & Integrity, Audit-the-AI, EiPE/Prompt | Essays, recovered password, curl session proof, "0 matches" result, corrected KDF code, personalised flag | K1–K4, P1–P5, A1–A3 | Part of the 30% worksheet component |
| Weekly quiz (start of lecture) | Quiz score | K1–K2 | Part of the 10% quiz/participation component |
| Viva spot-check / micro-demo | Live reproduction and explanation of the crack, the bcrypt bounce, and the one-line `/login` diff | P1–P5, A2 | Pass/fail gate on the Lab + Audit-the-AI scores (per the worksheet), not separately scored |
| Per-student flag | Attributable flag value tied to the individual student | A1, A2 | Integrity control, not a mark |

The worksheet carries its own 100-point rubric (Part 2 = 25, Part 3 = 30, Evidence & Integrity = 10,
Audit the AI = 20, Comprehension & Prompt = 15). Partial credit is available where a student explains
the mechanism correctly but could not land the crack.

## 7. Materials

- Lab: `labs/week02-hash/` — `vulnerable_app.py`, `fixed_app.py`, `exploit.py`, `users_vulnerable.csv`,
  `users_fixed.csv`, `wordlist.txt`, `docker-compose.yml`, `requirements.txt`, `worksheet.md`, `README.md`
- Slides: `slides/week02.md`
- Optional cracking tools named by the worksheet: `hashcat` (`-m 0`), `john` (`--format=raw-md5`)
- References (from the lab README): NIST SP 800-63B *Digital Identity Guidelines*; OWASP *Password
  Storage Cheat Sheet*; Boneh & Shoup, *A Graduate Course in Applied Cryptography*, ch. 8; Provos &
  Mazières, *A Future-Adaptable Password Scheme* (bcrypt paper, USENIX 1999); Wikipedia — *Rainbow table*
- Submission channels: [SUBMISSION.md](../../SUBMISSION.md) · Rules of engagement: [ETHICS.md](../../ETHICS.md)

## 8. Risks and contingencies

| Risk | Mitigation |
|---|---|
| Slow image pull / `pip install` storm at start | Containers run `pip install --no-cache-dir -r requirements.txt` (flask, requests, bcrypt) on `python:3.12-slim` at boot; pre-pull the image and pre-warm a pip cache before class; keep a `docker save`/`load` copy offline |
| A student's host `pip install bcrypt` fails to build | `exploit.py` needs only `requests` on the host — its bcrypt-store check uses `hashlib` + a string compare, so bcrypt is only needed *inside* the fixed container; tell them not to install bcrypt on the host |
| Ports 8094 / 8095 already in use | Override the published ports in `docker-compose.yml`; the two apps are hard-coded to 8094 (vulnerable) and 8095 (fixed) |
| "Cracked it" but `/admin` returns `403` | Session cookie not carried between requests — reuse the cookie jar (`$JAR`) or one `requests.Session()` (Task 2 / `exploit.py`); this is the intended formative failure, mark the fix |
| Students over-claim "bcrypt = uncrackable" | The admin's password is in the shipped `wordlist.txt`; a slow per-hash bcrypt dictionary would still recover it. Require Task 5(b)+(c) so they name the work-factor cost *and* the second control (strong-password policy) |
| Flag not attributable | The default `FLAG_HASH` is a shared placeholder used only if the instructor skips the seeding step; `instructor/seed_flags.py` exists and is verified for this course (course-plan-19weeks.md item 5) — run it before class to mint a per-student `.env`. Because there is no live CTFd instance/roster for this course yet (item 6, still open), even a seeded flag's attribution isn't roster-checked automatically — lean on identity-stamped evidence and the viva for attribution in the meantime |
| Copy-paste of a classmate's recovered password / flag | Per-student flags, minted via `instructor/seed_flags.py`, + identity-stamped evidence + a viva "reproduce it live" spot-check on the pair |

## 9. Post-teaching reflection

*Complete after the session — this also feeds the course's engagement data.*

- Attendance / completion: ⬚
- Time actually taken per task (vs. plan), and whether Tasks 0–5 really needed only ~100 min: ⬚
- Where the class got stuck, and what unblocked them (expected: the session-cookie step in Task 2): ⬚
- Misconception that showed up in the *Explain-in-Plain-English* answers (expected: "reversing" a hash vs. "guess-and-hash"): ⬚
- Quality of the *Audit the AI* critiques — did students catch the planted flaw(s) the worksheet hints at, without being told? ⬚
- Did anyone over-claim bcrypt as invincibility rather than work factor? ⬚
- Anything to change before this week runs again: ⬚
