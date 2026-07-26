# Lesson Plan — Week 4: AES / Block-Cipher Modes (CBC Bit-Flipping & Malleability)

| | |
|---|---|
| **Course** | Security & Cryptography (⬚ course code) |
| **Week / date** | 4 · ⬚ |
| **Week kind** | LAB (runnable vulnerable/fixed pair + attributable flag) |
| **Contact time** | 300 min = 120 lecture + 180 laboratory |
| **Lab folder** | `labs/week04-aes-modes` |
| **Slides** | `slides/week04.md` |
| **Standards** | NIST SP 800-38A (ECB/CBC modes) · NIST SP 800-38D (GCM/GMAC) · CWE-353 (Missing Support for Integrity Check) · CWE-649 (Reliance on Obfuscation/Encryption Without Integrity) · CWE-347 (Improper Verification of a Cryptographic Signature) |
| **CLOs addressed** | **CLO1** select & justify · **CLO2** break · **CLO3** rebuild — from the §6 schedule row; plus **CLO5** evaluate AI/communicate and **CLO6** evidence & ethics, carried by the worksheet's *Audit the AI* / *EiPE* / *Evidence & Integrity* parts (course-spec §4) |

> Standards are the *analogous* CWEs named in `labs/week04-aes-modes/README.md`; this is a
> cryptographic-misuse week, so there is no OWASP category mapping in the repo — none is invented
> here.

---

## 1. Session objectives

By the end of this week a student can:

**Knowledge (K)**
- K1 — State the difference between AES **the block cipher** (textbook-secure, one 16-byte block) and the **mode** (ECB/CBC/GCM) that wraps it, and explain that the mode — not AES — decides whether the scheme is secure.
- K2 — Explain why an unauthenticated mode gives **confidentiality only**: "encrypted" and "tamper-proof" are different properties, and CBC alone never provided the second (source Q3 / Q9).
- K3 — Explain, from the CBC decryption relation `P1 = AES_decrypt(C1) XOR C0`, why editing the **previous** ciphertext block predictably flips the **next** plaintext block without the key.

**Skills (P)**
- P1 — Capture a legitimate `role=guest` token from `:8096`, base64-decode it into `IV ‖ C0 ‖ C1`, and identify the exact byte range to edit (`token[21..25]`).
- P2 — Run the CBC bit-flip (`guest` → `admin`) and cash the tampered token in at `/admin` for the flag, and reproduce it by hand with `curl` to prove the script hides nothing.
- P3 — Confirm empirically that the same tamper against the AES-256-GCM app on `:8097` is **rejected** (403, no flag), and state why GCM's tag check closes the gap.
- P4 — Audit an AI-written "encrypt the role field" snippet, find the malleability flaw, and rewrite it with authenticated encryption (AES-GCM / encrypt-then-HMAC).

**Attitude (A)**
- A1 — Attack only the two local containers this lab spins up (`:8096` / `:8097`), under [ETHICS.md](../../ETHICS.md).
- A2 — Submit identity-stamped evidence that is their own work (per-student flag), reproducible live on request at the viva.
- A3 — Treat AI-generated cryptographic code as something to be verified, not trusted — the *Audit the AI* snippet "runs, uses a real AES library, and looks professional" yet is confidently wrong.

## 2. Key ideas (the through-line)

Nobody breaks AES this week, or in practice — every attack is a **mode / usage** attack. The
course spine is one sentence repeated: *textbook-secure primitive, real-system failure.* Week 3
showed a keyed hash is not automatically a MAC; Week 4 shows **encryption is not integrity**. An
unauthenticated CBC token is *malleable*: because CBC decrypts block *i* as `D(C_i) XOR C_{i-1}`,
an attacker who cannot read the plaintext can still XOR a chosen delta into the previous
ciphertext block and flip predictable bytes of the next plaintext block — turning `role=guest`
into `role=admin` without ever touching the key. The fix is structural, not a smarter filter: use
**authenticated encryption** (AES-GCM / AEAD), whose tag is recomputed over the ciphertext on
every decrypt, so any edit is rejected — and only if the developer actually checks the tag and
does not swallow the exception (source Q10, in the spirit of CWE-347).

## 3. Prior knowledge and preparation

- **Students, before class:** Docker Desktop working (same Docker-first setup as `software-security`); skim the Week 3 recap (MACs / length-extension) and notice the through-line "keyed hash ≠ MAC → encryption ≠ integrity". Per the worksheet's own prerequisites: Docker, and Python 3.12 with the `requests` package on the host to run `exploit.py` — *or* run it inside the `vulnerable` container.
- **Instructor, before class:** pre-pull the lab image ahead of the session — both services use `python:3.12-slim` and `pip install --no-cache-dir -r requirements.txt` on first `docker compose up` (`flask>=3.1.3`, `cryptography>=48.0.1`, `requests>=2.33.0`). A room pulling the image and building the `cryptography` wheel at once is the single most common way to lose the first 15 minutes; have the offline fallback ready (see §8).
- **Prerequisite concepts:** XOR, base64, and the CBC decrypt relation `P_i = D(C_i) XOR C_{i-1}` — this is the whole exploit, and Task 2 is derivation on paper before any tool runs.

## 4. Lecture — 120 min

Standard LAB-week lecture shape (AGENDA.md). Content and the per-slide time hints come from
`slides/week04.md`.

| Time | Block | Content | Method |
|---|---|---|---|
| 0:00–0:10 | Weekly quiz + recap | ~10-min retrieval quiz (drop lowest 1–2); Week 3 recap (keyed hash ≠ MAC → today: encryption ≠ integrity); today's agenda | Individual quiz |
| 0:10–0:55 | Core concepts | AES the primitive vs. the mode; **ECB** leaks patterns (the "ECB penguin", Q1); **CBC** chaining `C_i = E(P_i XOR C_{i-1})`, the IV's job, and why reusing an IV leaks a shared prefix (Q2) | Lecture + board derivation both directions |
| 0:55–1:05 | Break | | |
| 1:05–1:35 | Misuse deep-dive | The gap: CBC gives confidentiality only, nothing detects tampering (Q3/Q9; CWE-353 / CWE-649); the target token layout (`comment=FILLER!!` ‖ `role=guest;xpad0`); why flipping **C0** changes **P1** deterministically without the key | Lecture + live derivation of `P1 = D(C1) XOR C0` |
| 1:35–1:55 | Correct construction | AES-GCM / AEAD (Q4): AES-CTR + a GHASH tag over the ciphertext, checked on decrypt; empirical proof the same flip yields 403; Q10 trap (GCM only helps if the tag is actually checked, CWE-347); the wider family — reused GCM nonce (Q5/Q6), AES-XTS for disks (Q8), GCM vs ChaCha20-Poly1305 on mobile/IoT (Q7) | Lecture with CBC-vs-GCM contrast |
| 1:55–2:00 | Game briefing | "Flip Your Way to Admin" — capture on `:8096`, XOR `token[21..25]`, replay to `/admin`, then watch the identical trick fail on `:8097` | Instruction → to lab |

**Checks for understanding during lecture**
- After the CBC slide: cold-call *"if you can't read the plaintext, can you still change it?"* (Yes — that is the whole lab.)
- Before the break: one-minute paper — *"name one thing GCM checks that CBC never does."*

## 5. Laboratory — 180 min

Targets: `cd labs/week04-aes-modes` → `docker compose up -d` → `vulnerable_app.py` on `:8096`
(AES-256-CBC, no MAC — malleable) and `fixed_app.py` on `:8097` (AES-256-GCM, AEAD — rejects the
tamper). Rows use the worksheet's own task names and stated minute budgets (Part 2A, Tasks 0–5);
the rotating micro-demo and submit rows are the AGENDA.md standard LAB-week closing blocks — the
35-min buffer is this plan's own addition to reconcile the worksheet's stated task budgets with the
180-min block (see the instructor note below). Default flag is
`FLAG{aes_cbc_is_malleable}` unless a per-student `.env` is seeded (see §7).

| Time | Task | Student does | Evidence produced |
|---|---|---|---|
| 0:00–0:10 | **Task 0 — Onboarding (10 min)** | `docker compose up -d`; `curl localhost:8096/`; read `vulnerable_app.py`'s `issue_token` / `parse_role` and the BLOCK LAYOUT comment; confirm it is AES-CBC with no MAC/tag (`_aes_cbc_encrypt`), not GCM | Quoted encrypt line + which of Q3/Q4 failure modes it matches |
| 0:10–0:20 | **Task 1 — Capture a legitimate token (10 min)** | `curl -i "localhost:8096/login"`; record the `token` cookie; `curl --cookie "token=<...>" localhost:8096/whoami` → `{"role":"guest"}` | Token value + `/whoami` output |
| 0:20–0:50 | **Task 2 — Locate the bytes you must flip (30 min)** | base64-decode the token into `IV ‖ C0 ‖ C1` (16 bytes each); on paper derive that `guest` sits at `P1[5..9]`, so to change it you XOR into **C0** at token indices `16+5 .. 16+9 = 21..25`; write the five deltas `guest[i] ^ admin[i]` | Five hex deltas + the absolute token indices they apply to |
| 0:50–1:10 | **Task 3 — Run the flip and cash in the flag (20 min)** | read `exploit.py`'s `bitflip_cbc_token` (confirm it edits `token[21..25]`); `python exploit.py`; reproduce by hand — take the forged token and `curl --cookie "token=<forged>" localhost:8096/admin` | The flag + the `curl` command and its JSON output |
| 1:10–1:30 | **Task 4 — Confirm GCM rejects the same trick (20 min)** | observe `exploit.py`'s tamper against a `:8097` GCM token print `403`/rejected; read `fixed_app.py`'s `issue_token` / `parse_role` and identify the change (CBC → `AESGCM`, decrypt now *raises* on a bad tag) | Rejection evidence + in-words diff + why the CBC byte offsets don't map to GCM's `nonce ‖ ct ‖ tag` |
| 1:30–1:50 | **Task 5 — Explain why, precisely (20 min)** | answer (a) why editing C0 changes P1 but not in a way that matters for C0's own block, (b) why `guest → admin` is a clean flip but `user → admin` is not, (c) what GCM computes over the ciphertext that makes the edit fail | Three short paragraphs, one per sub-question |
| 1:50–2:10 | **Parts 2C + 2D — AI-resilient (20 min; start in class, finish as homework)** | *Audit the AI* — find the flaw in the AI's "the client also cannot change the role" claim and rewrite `make_token`/`read_role` with AEAD; *Explain-in-Plain-English*; *Prompt Problem* | Written answers (started in class) |
| 2:10–2:20 | **Rotating micro-demo (10 min)** | 2–3 rotating students give a 2–3 min "show your flip / show why GCM rejects it" | — |
| 2:20–2:25 | **Submit (5 min)** | Worksheet → PDF → this course's Google Classroom as `Wk04_<StudentID>.pdf` | Submission receipt |
| 2:25–3:00 | **Buffer / slower groups (35 min)** | Catch-up on Tasks 2–4 (byte-indexing is the usual stall); re-seed `.env` and restart if flags collided; begin the Part 1 written questions | — |

> **Instructor note — the 180-min fit is a labelling gap, not a solved sum.** The worksheet
> labels Part 2A "Hands-on Lab (180 min)", but its named Tasks 0–5 sum to **110 min**
> (10+10+30+20+20+20), and Parts 2C/2D/2E carry **no** minute budget in the worksheet. This plan
> keeps every worksheet budget **as written** and absorbs the difference into the AGENDA's
> standard closing blocks plus an explicit 35-min buffer — it does **not** reshape any task
> budget to make the numbers meet. AGENDA.md's own open item flags this exact thing: *"Confirm
> actual worksheet task counts fill the 180-min lab block per week … has not been re-checked
> against this course's own worksheets yet."* Treat the buffer as real slack until a live run
> confirms the fit. See `escalated`.

**Formative checkpoints.** A student stuck on Task 2 after 15 minutes is almost always mis-indexing
the token — prompt them to base64-decode first and count `16 + 5 = 21`, not guess. Tasks 1–3 must
be done by 1:10 for Tasks 4–5 to fit; a student still stuck should read `exploit.py`'s
`bitflip_cbc_token` to see the exact `token[21..25]` edit, then return to their own derivation.

## 6. Assessment for this week

Points below are the worksheet's own rubric (100 pts total). The whole worksheet is part of the
30% weekly-worksheet component (syllabus §3 / course-spec §4).

| Instrument | Evidence | Outcome | Weight |
|---|---|---|---|
| Worksheet 4 Part 1 — written Q1–Q10 (Conventional arm) | Essay answers (ECB/CBC/GCM/XTS, nonces, AEAD) | CLO1 | 25 pts |
| Worksheet 4 Part 2A — lab Tasks 0–5 | Token hex dump, computed XOR deltas, curl output, flag | CLO2, CLO3 | 30 pts |
| Worksheet 4 Part 2B — Evidence & Integrity | Identity-stamped proof + per-student flag + own-words explanation | CLO6 | 10 pts |
| Worksheet 4 Part 2C — Audit the AI | Flaw found + AEAD-corrected, verified rewrite | CLO5 | 20 pts |
| Worksheet 4 Part 2D — Comprehension & Prompt | EiPE + Prompt Problem | CLO5 | 15 pts |
| Weekly quiz (start of lecture) | Quiz score | K1–K2 | Part of the 10% quiz/participation component |
| Viva spot-check (Part 2E) | Live reproduction of the flipped byte range + why GCM rejects it | P1–P3, A2 | Pass/fail gate on 2A + 2C (not separately scored) |

Per-student flags (via the `AES_KEY` / `FLAG_AES` env override) make submitted evidence
attributable; duplicate flags are detectable. The written Part 1 is the Conventional arm of the
preregistered crossover design — "no AI-resilience layer applies to this part; answer it
yourself".

## 7. Materials

- Lab: `labs/week04-aes-modes/` — `vulnerable_app.py`, `fixed_app.py`, `exploit.py`, `docker-compose.yml`, `requirements.txt`, `worksheet.md`, `README.md`
- Slides: `slides/week04.md`
- Readings (`readings.md`, W4): ⭐ NIST SP 800-38A (block-cipher modes) · a CBC bit-flipping / padding-oracle explainer · Cryptopals Set 2 (CBC/padding practice)
- Also see the lab's own `README.md` References section: NIST SP 800-38D (GCM/GMAC) · Boneh & Shoup, *A Graduate Course in Applied Cryptography*, ch. 4–5 · RFC 5116 (AEAD interface)
- Per-student flag: `python3 ../../instructor/seed_flags.py env <STUDENT_ID> > .env` before `docker compose up` (README); until seeded, `FLAG_AES` defaults to `FLAG{aes_cbc_is_malleable}`
- Submission channel: [SUBMISSION.md](../../SUBMISSION.md) (`Wk04_<StudentID>.pdf` → Google Classroom) · Rules of engagement: [ETHICS.md](../../ETHICS.md)

## 8. Risks and contingencies

| Risk | Mitigation |
|---|---|
| Slow image pull / `pip install` at class start — both services build `python:3.12-slim` + the `cryptography` wheel on first `docker compose up` (note: `requirements.txt` is installed `--no-cache-dir`, so a local pip cache does not help) | Pre-pull the image before the session; keep a USB copy (`docker save`/`docker load`) |
| Ports `8096` / `8097` already in use on a student's machine | Change the **host** side of the port mapping in `docker-compose.yml` (the left of `"8096:8096"` / `"8097:8097"`; the container apps hard-code `8096`/`8097`), then point `exploit.py` at the new host ports via the `VULN_PORT` / `FIXED_PORT` (or `VULN_HOST` / `FIXED_HOST`) environment variables it reads |
| `exploit.py` run on the host without the `requests` package (a stated prerequisite) | `pip install requests` on the host, or run `exploit.py` inside the `vulnerable` container as the worksheet allows |
| Student mis-indexes the flip (off-by-one) and edits the wrong bytes | Anchor them on `16 + 5 + i = 21 + i`; the flip is `token[21..25]`, editing **C0** (not the role block itself); `parse_role` returns `?` on a broken layout, which is the tell |
| `.env` not seeded before `docker compose up`, so every student captures the default `FLAG{aes_cbc_is_malleable}` and submissions are non-attributable | Seed the per-student `.env` first (README command); the viva spot-check (2E) is the backstop; note the README's own hedge that `seed_flags.py` "may not yet exist" is stale — the file is present in `instructor/` (see `escalated`) |
| Student assumes they must *write* the fix (as in `software-security`) | Week 4 is a confirm-the-fix week: `fixed_app.py` is already built; SUBMISSION.md states most weeks you confirm and explain, you do not commit code (only Week 12 writes a fix) |
| Copy-paste of a classmate's forged token or flag | Per-student flags make evidence attributable; viva spot-check the pair and require live reproduction of the exact byte range |
| GCM-side confusion — a student expects the same `token[21..25]` recipe to work on `:8097` | That is the intended lesson (Task 4): GCM's layout is `nonce ‖ ct ‖ tag` with no previous block to XOR into, and *any* edit fails the tag — 403, no flag |

## 9. Post-teaching reflection

*Complete after the session — this also feeds the course's engagement data.*

- Attendance / completion: ⬚
- Time actually taken per task (vs. plan) — **especially whether the ~35-min buffer was consumed or the 180-min block over/under-ran**: ⬚
- Where the class got stuck, and what unblocked them (byte-indexing in Task 2 is the predicted stall): ⬚
- Misconception that showed up in the *Explain-in-Plain-English* answers (e.g. "CBC encrypts each block independently" — that is ECB): ⬚
- Quality of the *Audit the AI* critiques (did students catch that the false claim is the *last sentence*, "they'd have to break AES"?): ⬚
- Anything to change before this week runs again: ⬚
