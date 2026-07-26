# Lesson Plan — Week 3: MACs — Hash-Only Cookies and Length-Extension

| | |
|---|---|
| **Course** | Security & Cryptography (⬚ course code) |
| **Week / date** | 3 · ⬚ |
| **Contact time** | 300 min = 120 lecture + 180 laboratory |
| **Lab folder** | `labs/week03-macs` |
| **Slides** | `slides/week03.md` |
| **Kind** | LAB (runnable vulnerable/fixed pair + per-student flag) |
| **Standards** | CWE-347 (Improper Verification of Cryptographic Signature) · CWE-290 (Authentication Bypass by Spoofing) · RFC 2104 (HMAC) · NIST FIPS 198-1 (HMAC) |
| **CLOs addressed** | **CLO1** select/justify the primitive · **CLO2** break · **CLO3** rebuild (schedule §6) · **CLO5** evaluate & communicate · **CLO6** ethics & evidence (recurring worksheet parts) |

---

## 1. Session objectives

By the end of this week a student can:

**Knowledge (K)**
- K1 — State why a bare hash of `key || message` (or `message || key`) is **not** a secure MAC, in terms of what the digest lets an attacker recompute or extend.
- K2 — Explain how SHA-256's Merkle-Damgard construction lets an attacker resume the hash from a captured digest and append attacker-chosen data — `H(secret || data || glue || extra)` — without ever knowing `secret`, given only its *length*.
- K3 — Explain why HMAC's nested `H(key⊕opad || H(key⊕ipad || message))` construction exposes no resumable internal state and so defeats length-extension.

**Skills (P)**
- P1 — Capture a legitimate `(data, sig)` cookie from the vulnerable app on `:8092` and decode the hex `data` back to `user=guest&admin=false`.
- P2 — Compute by hand the SHA-256 glue-padding length for `len(MAC_SECRET) + len(data) = 16 + 22 = 38` bytes using the padding rule (append `0x80`, zero-pad until length ≡ 56 mod 64, then an 8-byte big-endian bit-length), and confirm it against the glue length you can derive from `exploit.py`'s printed forged-data hex (forged length − 22 bytes of original `data` − 11 bytes of `&admin=true`) — the script prints the forged hex, not a labelled glue-length value.
- P3 — Run the length-extension forgery to mint a `(data, sig)` pair that appends `&admin=true` and still validates, and capture the flag from `GET /admin` on `:8092`.
- P4 — Show that the *identical* forgery is rejected (`403`, no flag) by the HMAC app on `:8093`, and point to the one-line difference between the two `make_cookie` functions.
- P5 — Recognise the non-constant-time `!=` tag comparison that *both* apps deliberately keep, and name constant-time comparison (`hmac.compare_digest`) and replay protection as *separate* fixes that switching to HMAC does not provide.

**Attitude (A)**
- A1 — Attack only the two local containers this lab spins up (`vulnerable_app.py` / `fixed_app.py`, ports 8092/8093), under [ETHICS.md](../../ETHICS.md).
- A2 — Submit identity-stamped evidence (`whoami` / login email / student ID + timestamp) and a per-student flag that is identifiably their own.
- A3 — Treat AI-generated cryptographic claims as something to verify, not trust (the *Audit the AI* task hides at least one subtle flaw in a plausible-looking design).

## 2. Key ideas (the through-line)

A hash is not a MAC. A hash proves integrity only against an attacker who cannot recompute it; the
moment you try to make it *authentic* by folding in a secret — `sig = SHA256(secret || data)` —
you have not built a keyed tag, you have published a resumable snapshot of the hash's internal
state. Merkle-Damgard hashes process input in 64-byte blocks and carry forward a chaining value;
the final digest *is* that chaining value. So an attacker who holds `sig`, and knows how many bytes
went in before it, can reload the machine mid-stream and keep hashing their own suffix — forging a
tag for a message they were never given the key to sign. The fix is structural, not a smarter
filter: HMAC binds the key on both sides of a *nested* hash, so the value an attacker sees is the
*outer* hash over an already-finalised inner digest — there is no mid-stream state to resume.
Switching to HMAC closes length-extension and *only* length-extension: the timing-side-channel in
the `!=` tag comparison and the absence of replay protection are separate bugs, left in place on
purpose so students see that "use HMAC" is necessary but not sufficient.

## 3. Prior knowledge and preparation

- **Students, before class:** Docker Desktop working (same Docker-first setup as `software-security`);
  Python 3.12 (or at least the `requests` package) on the host to run `exploit.py`; skim last
  week's recap (Week 2 — hash functions / password cracking).
- **Instructor, before class:** pre-pull the lab image (`python:3.12-slim`) before the session — a
  room of students each triggering `pip install --no-cache-dir -r requirements.txt` on a
  cold-pulled image at once is the most common way to lose the first 15 minutes; keep the offline
  fallback ready (see §8). Run the per-student flag seed before the session: from
  `labs/week03-macs`, `python3 ../../instructor/seed_flags.py env <STUDENT_ID> > .env` before
  `docker compose up` — `instructor/seed_flags.py` exists (a git-ignored thin shim forwarding to
  the curriculum monorepo's `tools/seed_flags.py`; course-plan-19weeks.md item 5, verified
  end-to-end) and needs `SC_FLAG_SALT` set plus the sibling `KOSEN69 - curriculum` repo checked
  out next to this one. If a session's `.env` was not seeded this way, `FLAG_MACS` defaults to
  `FLAG{macs_demo}` for everyone, so per-student attribution falls back to the identity-stamped
  evidence rule. (The lab's own `README.md`/`worksheet.md` still carry a stale "seed_flags.py may
  not yet exist" hedge — the file is present in `instructor/`; flagged in `escalated`, not fixed
  here per the boundary on this review.)
- **Prerequisite concept:** what a cryptographic hash is (Week 2), hex encoding, and that SHA-256
  consumes its input in fixed 64-byte blocks.

## 4. Lecture — 120 min

| Time | Block | Content | Method |
|---|---|---|---|
| 0:00–0:10 | Weekly quiz + recap | ~10-min retrieval quiz on Week 2 (hashing / password cracking); today's agenda | Individual quiz, lowest 1–2 dropped |
| 0:10–0:55 | Core concept | Hashes vs. MACs vs. signatures — what "authenticity" actually requires; why `H(secret ‖ data)` is *not* a MAC; sign one cookie live with a secret-prefix hash and name what the digest exposes | Lecture + live coding on the projector |
| 0:55–1:05 | Break | | |
| 1:05–1:35 | Misuse deep-dive + real framing | SHA-256 length-extension mechanism: Merkle-Damgard chaining, glue padding, resuming compression from a known digest; the length assumption (know the *length*, never the *value*); this is the class of bug behind old API signing schemes that shipped exactly this secret-prefix construction; related pitfalls named but not examined — timing attack on tag comparison (Q4), replay without a nonce (Q3) | Lecture + short discussion: "what would have stopped this?" |
| 1:35–1:55 | Correct construction | HMAC's nested `H(key⊕opad ‖ H(key⊕ipad ‖ message))` and why it exposes no resumable state; the one-line diff `hashlib.sha256(...)` → `hmac.new(...)`; that constant-time comparison (`hmac.compare_digest`) and replay defence are *separate* fixes | Lecture with code-diff comparison |
| 1:55–2:00 | Brief the game | "Forge the Admin Cookie" — forge into `/admin` on `:8092`, watch HMAC bounce the same trick on `:8093` | Instruction |

**Checks for understanding during lecture**
- After the core concept: cold-call *"which value in this cookie is the attacker allowed to hold, and what does holding it let them do?"*
- Before the break: one-minute paper — *"the secret is glued on the front and we never learn it — so why doesn't that protect the message?"*

## 5. Laboratory — 180 min

Targets: `docker compose up -d` in `labs/week03-macs` → `vulnerable_app.py` on `:8092` (secret-prefix
hash) and `fixed_app.py` on `:8093` (HMAC). Rows **Task 0–Task 5** use the worksheet's own names and
minute budgets (`worksheet.md`, Part 3); the onboarding, AI-resilient, micro-demo and submit rows
follow the AGENDA LAB-week lab template.

| Time | Task | Student does | Evidence produced |
|---|---|---|---|
| 0:00–0:15 | **Environment setup** | `docker compose up -d`; `curl localhost:8092/` to confirm it's up | Both containers running |
| 0:15–0:25 | **Task 0 — Onboarding (10 min)** | Read `vulnerable_app.py`'s `make_cookie`/`admin`; identify the line that computes `SHA256(MAC_SECRET + data)`, not HMAC | Quoted line + which of Q1/Q5's failure mode it matches |
| 0:25–0:35 | **Task 1 — Capture a legitimate cookie (10 min)** | `curl -i "localhost:8092/login?user=guest"`; record the `data` and `sig` cookies | Both cookie values + hex-decoded plaintext of `data` |
| 0:35–1:05 | **Task 2 — Run the length-extension forgery (30 min)** | Read `exploit.py`'s `sha256_padding`/`length_extend`; hand-compute the glue-padding length for `16 + 22 = 38` bytes; run `python exploit.py` and check it against the glue length derived from its printed forged-data hex (forged length − 33) | Hand computation + the script's forged `data`/`sig` |
| 1:05–1:15 | **Task 3 — Cash in the flag (10 min)** | Note the flag `exploit.py` printed; manually reproduce with `curl --cookie "data=...;sig=..."` against `/admin` on `:8092` | Flag + `curl` command and its output |
| 1:15–1:30 | **Task 4 — Confirm HMAC rejects the same trick (15 min)** | Confirm `exploit.py` printed `403`/rejected on `:8093`; read `fixed_app.py`'s `make_cookie` and find the one-line change | Rejection evidence + the diff (in words) between the two `make_cookie` functions |
| 1:30–1:50 | **Task 5 — Explain why, precisely (20 min)** | Answer: (a) what SHA-256 state `sig` exposes; (b) why resuming from it computes `H(secret ‖ data ‖ glue ‖ extra)` without `secret`; (c) why HMAC's outer hash exposes no equivalent state | 3 short paragraphs, one per sub-question |
| 1:50–2:25 | **Evidence & Integrity + buffer** | Assemble identity-stamped proof (`whoami`/ID + timestamp) for Tasks 1–4; record the personalised flag; write the own-words explanation; catch-up time | Evidence & Integrity section of the worksheet |
| 2:25–2:45 | **AI-resilient tasks** | *Audit the AI* (find the planted flaw in the AI's Q6 cookie design), *Explain-in-Plain-English*, *Prompt Problem* | Written answers (start in class, finish as homework) |
| 2:45–2:55 | **Rotating micro-demo** | 2–3 rotating students give a 2–3 min "show your forgery / show HMAC rejecting it" | Live reproduction |
| 2:55–3:00 | **Submit** | Everyone submits | Worksheet PDF + flag → Classroom; exploit code → GitHub ([SUBMISSION.md](../../SUBMISSION.md)) |

**Formative checkpoints.** A student stuck on **Task 2** is almost always trying to treat `data` as
a text string — remind them the forged suffix contains raw padding bytes (`0x80`, length bytes)
that are not valid cookie-safe text, which is exactly why the app transports `data` **hex-encoded**
and verifies on raw bytes. Tasks 0–3 must be done by ~1:15 for Task 4's HMAC check to fit; a student
who has not landed the forgery by then should run `exploit.py` to see both PASS lines first, then
return to reproduce Task 2's hand computation.

> **Instructor note (timing / labelling).** The worksheet heads Part 3 "Hands-on Lab (180 min)",
> but its six numbered tasks (0–5) budget only **95 min** (10 + 10 + 30 + 10 + 15 + 20). The
> remaining lab time is the onboarding/setup buffer, the Evidence & Integrity write-up, the
> AI-resilient tasks, the micro-demo and submission — all real, but not part of the numbered task
> count. The AGENDA already flags that this course's newly-built worksheets have not been
> re-checked against the 180-min block (AGENDA §"Open items"). Do **not** pad or trim the
> worksheet's per-task budgets to close the gap — that is graded student material. Flagged in
> `escalated`.

## 6. Assessment for this week

| Instrument | Evidence | Outcome | Weight |
|---|---|---|---|
| Worksheet 3 (Part 2 written Q1/Q4/Q5/Q6; Part 3 lab Tasks 0–5; Evidence & Integrity; Audit the AI; Comprehension & Prompt) | Written answers, hex dumps, `curl` output, hand-computed padding, captured flag, AI critique | K1–K3, P1–P5, A2–A3 (CLO1–3, CLO5, CLO6) | Part of the 30% worksheet component |
| Weekly quiz (start of lecture) | Quiz score | K1–K2 | Part of the 10% quiz/participation component |
| Viva spot-check / micro-demo | Live reproduction of the forgery / HMAC rejection and its explanation | P1–P4, A2 | Pass/fail gate on the Lab + Audit-the-AI scores (not separately scored) |
| Per-student flag | Flag tied to the `MAC_SECRET`/`FLAG_MACS` env override | A2 | Integrity control, not a mark |

The worksheet carries its own 100-point rubric (Part 2 = 25, Part 3 = 30, Evidence & Integrity = 10,
Audit the AI = 20, Comprehension & Prompt = 15); grade against that. Partial credit is available
where a student explains the mechanism correctly but could not land the forgery. Per-student flags
depend on `instructor/seed_flags.py`, which exists and is verified end-to-end for this course (see
§3) — run it before class. If a given session's `.env` was not seeded that way, treat the
identity-stamped evidence (not the flag string) as the attributable artifact.

## 7. Materials

- Lab: `labs/week03-macs/` — `vulnerable_app.py`, `fixed_app.py`, `exploit.py`, `docker-compose.yml`, `requirements.txt`, `worksheet.md`, `README.md`
- Slides: `slides/week03.md`
- References (from the lab README): Boneh & Shoup, *A Graduate Course in Applied Cryptography*, ch. 6 (MACs); RFC 2104 (HMAC); NIST FIPS 198-1 (HMAC); Wikipedia — *Length extension attack*
- Submission channels: [SUBMISSION.md](../../SUBMISSION.md) · Rules of engagement: [ETHICS.md](../../ETHICS.md)
- Per-student flags: `instructor/seed_flags.py` (git-ignored thin shim → the curriculum monorepo's `tools/seed_flags.py`; challenge key `macs`). Run `python3 ../../instructor/seed_flags.py env <STUDENT_ID> > .env` before `docker compose up` (requires `SC_FLAG_SALT`); if not seeded, `FLAG_MACS` defaults to `FLAG{macs_demo}` for everyone.

## 8. Risks and contingencies

| Risk | Mitigation |
|---|---|
| Slow/failed pull of `python:3.12-slim`, or `pip install` of `flask`/`requests` inside the container, at class start | Pre-pull the image before the session; keep a USB copy (`docker save`/`docker load`); the compose already uses `--no-cache-dir -r requirements.txt` so a warm image installs fast |
| Ports 8092 / 8093 already in use on a student's machine | Override the published ports in `docker-compose.yml` (`ports: "NNNN:8092"` / `"NNNN:8093"`) and pass the new ports to `exploit.py` via `VULN_PORT`/`FIXED_PORT` |
| Host has no `requests` (or no Python 3.12) to run `exploit.py` | Install `requests` on the host, or run the script inside a container that already has it; the worksheet lists this as a prerequisite |
| Student overrides `MAC_SECRET` to a length other than 16 bytes | Both apps `assert len(MAC_SECRET) == 16` and will refuse to start; `exploit.py`'s `SECRET_LEN` also assumes 16 — keep any override 16 ASCII bytes (README warns explicitly). Viva Q2 deliberately probes what breaks if this number is wrong |
| Student sends `data` as text and the forgery "mysteriously" fails | The forged suffix carries non-UTF-8 padding bytes; verification is byte-native and transport is hex-encoded — point them back to Task 2's note |
| A student finishes all tasks early | Extension: brute-force `SECRET_LEN` over a small plausible range without being told it is 16; or write a regression test asserting the HMAC app keeps returning 403 to the forged cookie |
| Copy-paste of a classmate's flag or forged cookie | Per-student `MAC_SECRET`/`FLAG_MACS` overrides make evidence attributable — run `instructor/seed_flags.py` before the session (§3); if a session's `.env` was not seeded, rely on the identity-stamped evidence rule and viva spot-checks |

## 9. Post-teaching reflection

*Complete after the session — this also feeds the course's engagement data.*

- Attendance / completion: ⬚
- Time actually taken per task (vs. plan — especially whether Tasks 0–5 really needed only ~95 min): ⬚
- Where the class got stuck, and what unblocked them (string-vs-bytes on `data` is the predicted snag): ⬚
- Misconception that showed up in the *Explain-in-Plain-English* answers: ⬚
- Quality of the *Audit the AI* critiques (did students catch the planted flaw, and did they avoid attacking the *correct* HMAC/length-extension reasoning the hint warns against?): ⬚
- Anything to change before this week runs again: ⬚
