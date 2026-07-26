# Lesson Plan — Week 17: Reflection & Review (pre-Final)

| | |
|---|---|
| **Course** | Security & Cryptography (course code `21025117`, per [syllabus.md](../../syllabus.md); the [course specification](../course-specification.md) §1 still records the code as ⬚ — confirm with the registrar before print) |
| **Week / date** | 17 · ⬚ |
| **Contact time** | 300 min ([AGENDA.md](../../AGENDA.md), "Week 7 & 17 — Review (300 min)" — the review weeks run as one continuous block, not the usual 120 lecture + 180 lab split) |
| **Lab folder** | `labs/week17-review` — **`README.md` + `mock-ctf.md`**. No worksheet, no code, no flag (the folder ships a mock brief that Week 7's folder carries inline in its README) |
| **Slides** | ⬚ — there is no `slides/week17.md` in the repository (decks exist for Weeks 01–06 and 10–15) |
| **Type** | Review — **no new content**. Consolidates Weeks 10–16, with a callback round to Weeks 2–6 |
| **Standards consolidated** | The `**Analogous CWE:**` lines of the weeks under review: CWE-347, CWE-345 (Wk11) · CWE-295, CWE-300 (Wk12) · CWE-311, CWE-319 (Wk13) · CWE-522, CWE-319, CWE-532 (Wk14) · CWE-323, CWE-347 (Wk15; CWE-327 in the `hndl/` companion). **Wk10 has no such line** — `labs/week17-review/mock-ctf.md` assigns it CWE-323 (see §3). Callback round, per `mock-ctf.md`: CWE-916/759 (Wk2) · CWE-347/290 (Wk3) · CWE-353/347 (Wk4) · CWE-322/300 (Wk5) · CWE-347/208 (Wk6) |
| **CLOs addressed** | **CLO1–CLO5** (course specification §6, week 17 row) |

---

## 1. Session objectives

By the end of this week a student can:

**Knowledge (K)**
- K1 — Recall, without notes, the one-line core lesson of each of Weeks 10–16 as recorded in the lab README's recap table, and name the analogous CWE that goes with it.
- K2 — State the through-line the mock brief asks them to be able to say out loud: confidentiality, integrity and authenticity are three *separate* properties, and nearly every challenge in the term is a system that bought one and assumed it got the others for free.
- K3 — Explain how the post-midterm arc (Wk10–15) is the asymmetric/protocol-layer sequel to the symmetric-primitives arc (Wk2–6), in the terms the lab README's "First-half callback" paragraph sets out.
- K4 — Describe the shape of both final blocks — Week 18 written (90 min, cumulative with emphasis on Weeks 10–16) and Week 19 practical plus graded CryptoVault demos (240 min, team) — well enough to plan revision time against them.

**Skills (P)**
- P1 — Re-run **any** of the Week 10–15 lab targets cold and recapture the flag or evidence log line solo, in the format the Week 19 practical will use.
- P2 — For each challenge attempted, write down the payload/command **and a one-line mitigation**, then self-check against that lab's own `exploit.py` and `worksheet.md`.
- P3 — For any two challenges, state the analogous CWE and the attack class in one sentence each, and give the one control or discipline that would have prevented it (the mock's warm-up task).
- P4 — Identify honestly which of the post-midterm topics they cannot yet do unaided, and say so in the debrief.

**Attitude (A)**
- A1 — Work only against the sandbox targets supplied by the course, under [ETHICS.md](../../ETHICS.md) — the mock brief restates this, and it holds in a practice run exactly as in a graded one.
- A2 — Treat the mock as calibration rather than performance: an unsolved challenge discovered today is worth more than a solved one copied from a neighbour.
- A3 — Keep treating confident cryptographic prose — from an AI or from a classmate — as something to verify (course specification §7); the Week 10 exhibit is the model case.

## 2. Key ideas (the through-line)

The lab README states the arc this review has to make retrievable, and it is a single argument told
seven times. Week 10 shows that wrapping a fast symmetric key with public-key crypto does nothing
for you if the symmetric layer underneath reuses a nonce. Week 11 shows that a signature proves
authenticity, not uniqueness — the `(r, s)` you verified has a twin `(r, n−s)` that verifies just as
well. Week 12 shows that "the traffic is encrypted" is not "encrypted to the right party"; the
guarantee lives in certificate validation, not in the handshake. Week 13 shows that even a correct
TLS deployment leaves the server inside the trust boundary, reading plaintext. Week 14 shows the
same thing one layer up: a password sent over TLS is a password handed to the server. Week 15 shows
that a mathematically quantum-resistant signature is still forgeable if the one-time key is used
twice — the failure is operational, not mathematical. Week 16 asks them to compose all of it
correctly in their own build.

So the exam question, in whatever costume it arrives, is the Final Wager question: **which of
confidentiality, integrity and authenticity does this construction actually give me, and which am I
assuming it gives me for free?** Today's job is retrieval under time pressure, not re-teaching. The
second job is calibration — students consistently over-rate what they can reproduce with the
worksheet closed, and a 150-minute mock is the cheapest place to find that out, one week before the
written paper and two before the practical that together carry 25% of the mark.

## 3. Prior knowledge and preparation

- **Students, before class** (lab README, step 1): review **Weeks 10–16**, plus the first-half
  callbacks (Wk2 hash, Wk3 MACs, Wk4 AES modes, Wk5 key exchange, Wk6 AEAD). Bring the machine they
  intend to sit Week 19 on.
- **Instructor, before class — the Jeopardy bank already exists.** The lab README says the question
  bank is "**not yet built** — add it as `../../instructor/week17-jeopardy-bank.md` … when this week
  is staffed". That sentence is stale: `instructor/week17-jeopardy-bank.md` is present (git-ignored),
  with all seven categories at five tiers, a Final Wager and running notes for the instructor. Open
  it and confirm before you spend an evening rebuilding a board you already have. **Do not fix the
  README from this plan** — see §10 and the escalation note there.
- **Instructor, before class — Wk10 has no `Analogous CWE:` line.** The bank's dispute rule says the
  course-assigned CWE numbers "are in each week's README header (`**Analogous CWE:**` line); those
  are authoritative for this game". `labs/week10-hybrid-encryption/README.md` carries no such line;
  the only place CWE-323 is attached to Week 10 is `labs/week17-review/mock-ctf.md`. Decide before
  the game which source you will rule from, and say it when you open the category.
- **Instructor, before class — three of the six targets build their own images.** Weeks 12, 13 and 14
  each ship a `Dockerfile` and are started with `--build`; Weeks 11 and 15 run `python:3.12-slim`
  with the lab bind-mounted and `pip install --no-cache-dir -r requirements.txt` **at container
  start** (two containers each). Build and pull everything on the room network the day before. The
  Week 6 README records that verification had to be run from a scratch copy because OneDrive
  placeholder files can break an in-place `docker build` — today there are three build-dependent
  labs, so pin the tree as "always keep on this device" or copy to a local scratch path first.
- **Instructor, before class — host-side dependencies for the exploit scripts.**
  `labs/week11-signatures-zkp/exploit.py` imports `requests` **and** `ecdsa`;
  `labs/week15-pqc/exploit.py` imports `requests`; `labs/week15-pqc/hndl/exploit.py` additionally
  needs `pycryptodome` and `sympy` if it is run on the host. The containers install
  these; a bare host does not. Note that `ecdsa` carries CVE-2024-23342 as a documented accepted risk
  (course specification §10, and that lab's `requirements.txt`) — a student "helpfully" removing or
  bumping it breaks the lab.
- **Instructor, before class — two decisions to announce today.** Whether the cumulative quiz runs on
  paper or as a Google Form (SUBMISSION.md routes quizzes through a Form posted in Classroom): ⬚.
  Whether Week 19's teams are the CryptoVault project teams or freshly drawn: ⬚. Both change how
  students spend the next two weeks.
- **Prerequisite state:** the Week 10–15 labs have been completed and submitted, and each team has a
  CryptoVault build in progress from the Week 16 studio. A student who never stood up one of those
  targets will lose the mock block to environment setup.

## 4. Consolidation — the weeks under review

| Wk | Topic (kind) | Signature game | Must be retrievable cold | Re-tested today by |
|---:|---|---|---|---|
| 10 | Asymmetric & hybrid encryption (CONCEPTUAL) | 🔬 "Nonce Detective" | Why asymmetric alone is unsuitable for bulk data (performance + message-size limits); the full hybrid flow — RSA-OAEP wraps a fresh AES-GCM session key; that a *fixed or reused* GCM nonce gives `XOR(C1,C2) = XOR(P1,P2)` and also enables tag forgery; ECIES as ECDH-based hybrid | Jeopardy *Asymmetric & Hybrid*; mock challenge 1; quiz Q1–Q2 |
| 11 | Signatures & zero-knowledge proofs (HYBRID) | 💰 "Double-Spend the Bank" | Signature vs. MAC (anyone verifies vs. key-holders only); malleability — a valid `(r, s)` has the valid twin `(r, n−s)`; why hashing the signature bytes into a transaction id turns that into a double-spend; low-S / BIP-62 as the fix; Schnorr + Fiat–Shamir; SUF-CMA vs. EUF-CMA | Jeopardy *Signatures & ZKP*; mock challenge 2; quiz Q3, Q14 |
| 12 | Secure transport, TLS & Noise (HYBRID) | 🎭 "The Impostor's Certificate" | What the handshake authenticates and what it does not; the CA chain of trust; that the fixed client aborts **before** the secret is sent, with a *trust/issuer* error (`self-signed certificate`), not a hostname mismatch; `verify=False` / `CERT_NONE` / `InsecureSkipVerify` as the real-world shape of the bug | Jeopardy *Transport & TLS*; mock challenge 3; quiz Q4 |
| 13 | End-to-end encryption (HYBRID) | 👀 "Who's Reading Your Mail?" | Transport vs. end-to-end encryption; the server as trusted third party; the E2EE message shape (fetch recipient's public key, fresh AES-256-GCM key per message, RSA-OAEP-wrapped, client-side); that this lab does *not* solve key distribution / root of trust (PGP vs. Signal's TOFU, X3DH, Double Ratchet) | Jeopardy *E2EE*; mock challenge 4; quiz Q5, Q12 |
| 14 | User authentication (HYBRID) | 🗝️ "Never Say the Password" | TLS terminates *at the server*, so the plaintext password is handed over even on a perfect channel; what challenge-response proves and how the server checks it from a stored verifier `v = KDF(salt, password)`; know/have/are, TOTP, FIDO2/WebAuthn, credential stuffing, SSO/OAuth; that the demo proves only "password never transmitted" and is **not** a full PAKE | Jeopardy *Authentication*; mock challenge 5; quiz Q6, Q13 |
| 15 | Post-quantum cryptography (LAB) | 🔑 "Forge the Admin Signature" | Shor breaks RSA/ECC outright, Grover only halves symmetric/hash strength; harvest-now-decrypt-later; the four PQC families and what ML-KEM and ML-DSA are each *for*; Lamport as a one-time signature — two signatures under one key leak the private key; the fix is operational (refuse the second signature); stateful XMSS/LMS vs. stateless SPHINCS+ | Jeopardy *PQC*; mock challenge 6; quiz Q7–Q9, Q15 |
| 16 | Capstone studio — CryptoVault (studio week, no lab dir by design) | 🏗️ CryptoVault build | The five primitives composed *correctly*: slow KDF (Argon2id/bcrypt), AEAD at rest with a fresh nonce per encryption, ECDH/X25519 or public-key wrapping for sharing, signatures on shared entries (low-S, not `hash(secret + message)`), TLS with validation on every link; plus the crypto-agility stretch note | **Quiz Q10 only** — see the coverage gap below |

**First-half callback (Wk2–6).** The lab README's chain, which the wildcard Jeopardy row and mock
challenges 7–11 both re-test: unsalted hashing is crackable (Wk2) → a MAC must be purpose-built, not
`hash(secret+data)` (Wk3, length extension) → encryption without integrity is malleable (Wk4, CBC
bit-flip) → an unauthenticated key exchange is MITM-able (Wk5) → combining confidentiality and
integrity correctly is AEAD, and doing it naively leaks a padding oracle (Wk6). The quiz reaches the
callback through Q11 (unauthenticated DH, Wk5).

**Two coverage gaps to name out loud.**
1. **Week 16 is examined but not rehearsed today.** The review folder, the quiz and the exam-prep
   note all say "Weeks 10–16", but the Jeopardy board has no capstone category and the mock has no
   capstone challenge; Week 16 is carried by quiz Q10 and by the project itself. Since Week 19 spends
   0:00–2:30 on the CTF and **2:30–4:00 on graded CryptoVault demos**, a student who revises only
   from today's mock will have rehearsed nothing for the half of Week 19 that is actually graded.
   (Week 16's own agenda block did include a practice CTF tournament at 2:15–4:45 — that was the
   rehearsal for the CTF half, not for the demo.)
2. **The `hndl/` companion lab is not in the mock.** `labs/week15-pqc/hndl/` — harvest-now-decrypt-
   later plus hybrid KEM, vulnerable `:8120` / fixed `:8121`, `**Analogous CWE:** CWE-327` — is a
   built, runnable Week 15 lab. It appears in neither the mock's target list nor the PQC Jeopardy
   category, yet HNDL is examined conceptually (quiz Q9) and hybrid mode is the deployable mitigation
   students are expected to name. If a team finishes the main round early, send them there (§5.3).

## 5. Session run-sheet — 300 min

Timings are AGENDA.md's "Week 7 & 17 — Review (300 min)" block; the lab README states that its own
sequence (quiz → Jeopardy → mock final CTF/practical → debrief) follows that block.

| Time | Block | What happens |
|---|---|---|
| 0:00–0:30 | **Cumulative review quiz** | `quizzes/weekly/week17-review-quiz.md` — individual, closed book |
| 0:30–1:45 | **Security Jeopardy: Champions Edition** | Team quiz-show, seven categories |
| 1:45–2:00 | **Break** | Students start their mock targets during the break, not at 2:00 |
| 2:00–4:30 | **Mock final CTF** | `labs/week17-review/mock-ctf.md`, in the Week 19 practical format |
| 4:30–5:00 | **Debrief** | Common mistakes (§6) + final logistics (§7) |

### 5.1 Cumulative review quiz — 0:00–0:30

| Field | Value |
|---|---|
| Instrument | `quizzes/weekly/week17-review-quiz.md` — "Week 17 — Cumulative Review Quiz (Weeks 10–16)" |
| Blueprint as written | Part A MCQ 10 × 1 pt + Part B short answer 3 × 3 pts + Part C applied 2 × 3 pts = **25 pts**, 15 questions |
| Stated duration | "**Time:** 30 min" in the file header — which matches the 30-minute slot above |
| Covers | Asymmetric/hybrid encryption · signatures & ZKP · secure transport (TLS) · E2E encryption · authentication · PQC · capstone, plus a light callback to Wk2–6 fundamentals |
| Conditions | Individual, closed book |
| Delivery | Google Form posted in this course's Classroom at quiz time (SUBMISSION.md); the markdown file prints as the paper fallback (it carries name / student-ID / date fields) |
| Where it counts | The 10% weekly-quizzes / participation component (course specification §4) |

Unlike the Week 7 file, this one already totals the 25 pts AGENDA.md records for a cumulative review
quiz — no rescaling decision is needed before printing. Weeks 7 and 17 carry no six-question weekly
quiz of their own; the cumulative quiz **is** this week's retrieval practice (AGENDA.md).

**Cohort rotation.** The quiz file is static and reused each cohort, which is a leak risk. Swap two
or three items from `instructor/exams/item-bank.md` into a cohort copy, holding the total at 25 and
keeping the A/B/C part weights intact, and update `instructor/week17-review-quiz-answers.md` in the
same pass.

### 5.2 Security Jeopardy: Champions Edition — 0:30–1:45

- **Name.** The lab README and the instructor bank both call it **"Security Jeopardy: Champions
  Edition"**; the course specification §6 abbreviates it as "🏆 Jeopardy: Champions Edition (Wk 10–16)".
- **Categories** — exactly the seven rows in the README's table: *Asymmetric & Hybrid (Wk10) ·
  Signatures & ZKP (Wk11) · Transport & TLS (Wk12) · E2EE (Wk13) · Authentication (Wk14) · PQC (Wk15)
  · ★ First-Half Callback (Wk2–6)*, the last a wildcard row at higher point values.
- **Board** — five tiers per category, **100 / 200 / 300 / 400 / 500**, higher value = harder or more
  applied ("explain why" rather than "define"). The wildcard callback row is worth **double**
  (200 / 400 / 600 / 800 / 1000); in the bank each of its five tiers is pinned to one callback week —
  200 Hashing (Wk2), 400 MACs (Wk3), 600 AES modes (Wk4), 800 Key exchange (Wk5), 1000 AEAD (Wk6).
  Then a **Final Wager** round in which teams wager any or all of their points.
- **Play format** — mirrors Week 7's "Crypto Jeopardy": the clue is phrased as a statement and teams
  **respond in question form**. Award the point for the idea, not the exact wording.
- **Source of clues** — `instructor/week17-jeopardy-bank.md` (git-ignored; it exists, despite the
  README's note — §3). Its clues are grounded in each week's own README and worksheet, and it flags
  its own Daily-Double candidates. Keep any clue you add phrased close to the worksheets, so the game
  reinforces vocabulary rather than ambushing students with new terms.
- **Teams** — run by Houses; scores feed the season-long Houses/XP leaderboard. This course has no
  live CTFd deployment yet (README status note, SUBMISSION.md), so tally on the whiteboard; nothing
  today is graded on those points.
- **Timing reality.** Thirty-five clues plus a Final Wager in 75 minutes is roughly two minutes per
  clue including the read, the buzz and the correction. Decide in advance which tier you drop if you
  fall behind — the honest choice is to drop 100-tier "define" clues, since the 300–500 tiers are the
  ones that rehearse exam-shaped reasoning. Do not sacrifice the Final Wager: it is the only item on
  the board that asks for the through-line whole.

### 5.3 Mock final CTF — 2:00–4:30

Ungraded, participation only (`mock-ctf.md`: "**Ungraded** (participation)", teams, **sandbox targets
only** under [ETHICS.md](../../ETHICS.md)). The brief is a practice run **with hints**: every
challenge is a repeat of a lab already completed, so the self-check points back to that lab's own
`exploit.py` / evidence check and `worksheet.md`. No flags are printed in it, deliberately.

> **Instructor note — the published budget does not fit the published slot.** `mock-ctf.md`'s header
> says "**Time:** ~165 min"; AGENDA.md's review-week block gives the mock 2:00–4:30, i.e. **150 min**,
> for eleven challenges. Resolve it by *scoping the attempt*, not by editing the worksheet — announce
> at 2:00 that teams attempt a fixed subset (for example three from the main round plus one callback),
> which also keeps the session's emphasis on Wk10–16 where the final's is. The 15-minute discrepancy
> is a defect in the lab file; it belongs in that file, not in this plan (§10).

**Main round — post-midterm (Weeks 10–15).** Commands are quoted exactly as the labs' own READMEs
have them.

| # | Challenge | Topic (analogous CWE) | Target and start command |
|---|---|---|---|
| 1 | Recover the leaked plaintext from two intercepted "hybrid-encrypted" messages | GCM nonce reuse, Wk10 (CWE-323 per `mock-ctf.md`) | `labs/week10-hybrid-encryption` — **no running service**; audit `audit_the_ai/` (`broken_hybrid_encrypt.py`). Deliverable is a proof script that prints the recovered plaintext, checked against `fixed_hybrid_encrypt.py` and the worksheet rubric |
| 2 | Double-spend a single authorised withdrawal | ECDSA malleability, Wk11 (CWE-347) | `labs/week11-signatures-zkp` — `docker compose up -d` (vulnerable `:8102`, fixed `:8103`), then `python exploit.py`. Expect two `PASS` lines and exit `0` |
| 3 | Intercept a secret from a TLS client that trusts the wrong server | Improper cert validation, Wk12 (CWE-295/300) | `labs/week12-secure-transport` — `docker compose -f docker-compose.vulnerable.yml up --build`, then `docker compose -f docker-compose.vulnerable.yml down -v`; fixed mode `docker compose -f docker-compose.fixed.yml up --build`. **No published host ports** — read the container logs |
| 4 | Prove the messaging server can (then cannot) read a "private" message | Transport vs. end-to-end, Wk13 (CWE-311/319) | `labs/week13-e2e-encryption` — `docker compose -f docker-compose.vulnerable.yml up --build`; fixed check `docker compose -f docker-compose.fixed.yml logs server \| grep -c "meet at pier 39 at midnight"`; tear down `docker compose -f docker-compose.vulnerable.yml down` |
| 5 | Log in without the server ever seeing your password | Credential transmission, Wk14 (CWE-522/532) | `labs/week14-authentication` — `docker compose -f docker-compose.vulnerable.yml up --build --abort-on-container-exit`, then the fixed file the same way; checks `docker compose -f docker-compose.fixed.yml logs \| grep -c "correct-horse-battery"` and `... \| grep -c "SERVER SAW PASSWORD"` |
| 6 | Forge a signature on the admin message you're forbidden to sign | Lamport one-time-key reuse, Wk15 (CWE-323/347) | `labs/week15-pqc` — `docker compose up -d` (vulnerable `:8100`, fixed `:8101`), then `python exploit.py` |

**Callback round — first-half primitives (Weeks 2–6).** Fewer challenges, lower weight; the final
emphasises Wk10–16, but the symmetric arc is fair game.

| # | Challenge | Topic (analogous CWE) | Target and start command |
|---|---|---|---|
| 7 | Crack the admin password from a leaked user store | Fast/unsalted hash, Wk2 (CWE-916/759) | `labs/week02-hash` — `docker compose up -d` (`:8094` / `:8095`), then `python exploit.py` |
| 8 | Forge an admin auth-cookie without knowing the secret | Hash-as-MAC length extension, Wk3 (CWE-347/290) | `labs/week03-macs` — `mock-ctf.md` gives no ports for this row; the lab's own README runs `docker compose up -d`, `:8092` (vulnerable) / `:8093` (HMAC fixed) |
| 9 | Turn `role=guest` into `role=admin` in a token you can't decrypt | CBC bit-flipping, Wk4 (CWE-353/347) | `labs/week04-aes-modes` — `docker compose up -d` (`:8096` / `:8097`), then `python exploit.py` |
| 10 | Sit in the middle of a key exchange and read the agreed "secret" | Unauthenticated DH MITM, Wk5 (CWE-322/300) | `labs/week05-key-exchanges` — `docker compose -f docker-compose.vulnerable.yml up --build`, then `docker compose -f docker-compose.vulnerable.yml down`; signed mode `docker compose -f docker-compose.fixed.yml up --build`. No published ports; read the logs |
| 11 | Decrypt a ciphertext byte-by-byte using only yes/no error responses | CBC padding oracle, Wk6 (CWE-347/208) | `labs/week06-aead` — `docker compose up -d` (`:8098` / `:8099`), then `python exploit.py`, `docker compose down` |

**For each challenge attempted** (`mock-ctf.md`): write down the payload/command **and a one-line
mitigation**, then compare against that lab's own `exploit.py` and `worksheet.md`. The brief is
explicit that full solutions live in each lab directory and that no spoiler-free copy is needed,
because these are repeat labs.

**Warm-up / early-finisher work**, straight from the brief: for any two challenges, state the
analogous CWE and the attack class in one sentence each; for any two, give the one control or
discipline that would have prevented it. A team that clears the main round early should take
`labs/week15-pqc/hndl/` — `docker compose up` (vulnerable `:8120`, fixed `:8121`), then
`python exploit.py` — which is the one built post-midterm target the mock never touches (§4).

**Formative checkpoints.** By the midpoint of the 2:00–4:30 block every team should have at least one
challenge landed end-to-end; a
team with none is usually still fighting the environment rather than the cryptography — put them on
challenge 2 or 6, the two that are a `docker compose up -d` plus a single script. A team that
finishes fast should prefer 3, 4 or 5 next: those are the log-reading weeks, where the evidence is an
*absence* and the reasoning is what earns the mark.

### 5.4 Debrief — 4:30–5:00

Run §6's list against the room ("hands up who is still shaky on this one") and drill the two or three
that draw the most hands. Then read out the Week 18/19 logistics from §7, and take the names of
anyone whose targets did not come up today onto the support list.

## 6. Misconceptions to re-test

Every row below is a correction that already exists somewhere in Weeks 10–16 or in the callback
weeks, because the naive version was wrong when it met the running lab.

| # | Misconception | Where it comes from | How to re-test it today |
|---:|---|---|---|
| 1 | "The right primitives were used, so the implementation is sound" | The Week 10 *Nonce Detective* exhibit is built so that every box a rushed reviewer checks — RSA-OAEP, AES-GCM — is genuinely ticked; `slides/week10.md`'s presenter note sets the trap explicitly and asks "what would you check next, if anything?" | Jeopardy *Asymmetric & Hybrid* 300; mock challenge 1 — ask for the buggy line quoted, then the recovered plaintext |
| 2 | "A nonce is just a number, reusing one is untidy at worst" | Week 10's core lesson and quiz Q2: reuse gives `XOR(C1,C2) = XOR(P1,P2)`, and it also breaks GCM's authentication | Quiz Q2; Jeopardy *Asymmetric & Hybrid* 400/500 — require the XOR relation *and* the forgery consequence |
| 3 | "ECDSA malleability is the same bug as ECDSA nonce reuse" | `slides/week11.md`'s opening presenter note names this conflation and tells the instructor to separate the two out loud; nonce reuse is a *key-recovery* bug, malleability is not | Jeopardy *Signatures & ZKP*; ask which one recovers the private key and which does not |
| 4 | "If the signature verifies, the transaction is the one that was authorised" | Week 11's whole premise — the bank derives a transaction id by hashing the signature bytes, so the twin `(r, n−s)` is a *different* txid on the same authorisation | Jeopardy *Signatures & ZKP* 300; mock challenge 2 — ask for the txid change, not the flag; quiz Q14 |
| 5 | "The traffic is encrypted, so it is safe" | Week 12's core lesson; the vulnerable run completes a genuinely encrypted TLS handshake — with the attacker | Jeopardy *Transport & TLS* 100; ask which of C/I/A the vulnerable session actually had |
| 6 | "`verify=False` is a reasonable way to get past a certificate error" | `slides/week12.md` previews the Audit-the-AI exhibit: an AI assistant "fixes" SSL errors with `verify=False` and then calls the connection secure because it is HTTPS | Jeopardy *Transport & TLS* 200; Week 18 written, spot-the-vulnerability items |
| 7 | "The fix works because the impostor's hostname doesn't match" | Week 12's README is explicit: the impostor also claims `CN=bob` with `SAN=DNS:bob`; the abort reason is `self-signed certificate` — a **trust/issuer** failure. The only difference is the missing CA signature | Jeopardy *Transport & TLS* 300; mock challenge 3 — make them read the abort reason aloud from the log |
| 8 | "HTTPS everywhere means the provider can't read my messages" | `slides/week13.md`'s poll ("if a service is 'all HTTPS,' is your data safe from the company running it?") records that most hands go up — this is the misconception the week dismantles | Quiz Q5 and Q12; mock challenge 4 — the `SERVER SAW:` line is the answer |
| 9 | "End-to-end encryption solves key distribution too" | Week 13's objectives name what the lab does *not* solve: how Alice knows the public key is really Bob's (PGP's failure, Signal's TOFU / X3DH / Double Ratchet) | Jeopardy *E2EE* 500 (a scope clue); ask what remains broken if the server lies about Bob's key |
| 10 | "Sending the password over TLS is fine — the wire is encrypted" | `slides/week14.md` calls this "the core misconception to kill" and draws it: client →[TLS]→ server →decrypts→ plaintext in a Python dict | Quiz Q6 and Q13; mock challenge 5 — grep the logs for the password in both modes |
| 11 | "This challenge-response demo is a PAKE, so we've covered PAKE" | Week 14's README carries an explicit honest-limits box: the fixed side proves only "password never transmitted"; it is **not** a full PAKE | Jeopardy *Authentication* 400 (the honest-scope clue) — ask what the demo does *not* prove |
| 12 | "Quantum breaks all cryptography" | Week 15's objectives: Shor breaks RSA/ECC outright; Grover only halves symmetric/hash security, which doubling the key or digest length mitigates | Quiz Q7; Jeopardy *PQC* 100/200 |
| 13 | "A bigger RSA key buys time against quantum" | The `hndl/` README names this as the classic wrong fix: Shor scales past any RSA size — only a different, quantum-hard problem helps | Jeopardy *PQC* 100; then ask what "hybrid mode" changes that key size cannot |
| 14 | "Nothing needs to change until a quantum computer exists" | Week 15's harvest-now-decrypt-later objective and quiz Q9: today's recorded ciphertext is the attack surface | Jeopardy *PQC* 300; quiz Q9; send the early finishers to `hndl/` (§5.3) |
| 15 | "A quantum-resistant signature scheme is safe to use like any other" | Week 15's defining limitation: a Lamport keypair is secure **iff** it signs once, and the fix is *operational* — refuse the second signature — not mathematical | Jeopardy *PQC* 400; quiz Q8 and Q15; mock challenge 6 — ask which bits of the private key the second signature revealed |
| 16 | "Stateless SPHINCS+ means the reuse problem is engineered away" | `slides/week15.md`'s note on Worksheet Task 5c: statefulness is itself an operational risk — a VM snapshot rollback replays old state and reuses a key catastrophically | Jeopardy *PQC* 500 (the fix is operational, not mathematical); ask how a snapshot rollback reintroduces the Week 15 attack |
| 17 | "We used every primitive on the list, so the build is correct" | The CryptoVault brief grades **correct composition**, not feature count: a fast hash as KDF, a reused nonce, or a shared key sent in the clear each reproduce a weekly lab's failure inside the team's own code | Quiz Q10; in the debrief, ask each team which of the five primitives their self-audit is weakest on |
| 18 | "Add a secret to a hash and you have a MAC" (callback) | Week 3's premise; the mock's challenge 8 hint spells out that length extension needs the secret's *length*, not its value | Wildcard row **400 — MACs (Wk3)**; mock challenge 8 — make them name the glue padding |
| 19 | "To change a plaintext block, tamper with that block" (callback) | Week 4 / mock challenge 9: flipping bytes in one ciphertext block flips the matching bytes of the **next** plaintext block | Wildcard row **600 — AES modes (Wk4)**; mock challenge 9 — ask for the byte range edited, not the flag |
| 20 | "DH gives us a secure channel" (callback) | Week 5 / mock challenge 10: the relay completes two clean handshakes and nobody errors until the public keys are HMAC-tagged (`SIGNED=1`) and both sides abort | Wildcard row **800 — Key exchange (Wk5)**; quiz Q11; mock challenge 10 — ask what the signed mode changed and what it did *not* cost |
| 21 | "If the endpoint never returns plaintext, it leaks nothing" (callback) | Week 6 / mock challenge 11: the naive MAC-then-encrypt app leaks padding validity as `200` vs `403`; the AEAD version answers `403` uniformly | Wildcard row **1000 — AEAD (Wk6)**; mock challenge 11 — then "what did the `200` tell you?" |

## 7. Exam preparation

### 7.1 Week 18 — written

- **Format:** single **90-minute** block, no lab (AGENDA.md, "Week 8 / 18 — Written exam"; SUBMISSION.md's
  exam table agrees). Delivered on paper or by Google Form in class.
- **Covers:** cumulative, with emphasis on Weeks 10–16 (SUBMISSION.md: "cumulative, emphasis Wk10–16
  (Hybrid-Encryption → Capstone)"; course specification §6, week 18 row).
- **Weighting to state plainly**, from the review README's exam-prep note: the item bank should run
  roughly **60–70% Wk10–16** and **30–40% Wk1–6 plus review-week callbacks**. That is the same ratio
  as today's Jeopardy board (six post-midterm categories against one double-weighted callback row) —
  point at the board when you say it, so the number lands as something they have already seen.
- **Parallel forms:** the written exam runs as Form A / Form B from a maintained item bank (course
  specification §9). Papers, marks and the item pool are instructor-held under `instructor/exams/`
  (git-ignored); published here as ⬚.
- **Say this explicitly:** the conceptual halves of the HYBRID weeks and the whole of Week 10 —
  the parts with no flag attached — are examinable, and Week 16 is examinable, since those are
  precisely the parts a revision plan built around re-running labs will miss.
- **What today does not rehearse.** Unlike Week 7 — whose README publishes a four-section mock
  written half (A Concepts · B Spot the vulnerability · C Attack walkthrough · D Design) — this
  review folder publishes **no written-half mock**: `mock-ctf.md` is practical-only. Students go into
  the final paper having last rehearsed the written format ten weeks ago, in Week 7, on first-half
  material. If you want a written rehearsal today, take twenty minutes off the mock and run a
  Section-B-style "spot the vulnerability" round on Wk10–16 snippets from
  `instructor/exams/item-bank.md` — decide before the session, not at 4:00.

### 7.2 Week 19 — practical + capstone demos

- **Format:** 240 minutes, in two graded halves (AGENDA.md, "Week 19 — Final CTF + project demos"):
  `0:00–2:30 Capstone CTF tournament` (whole term: LAB + Wk11 flags, plus Wk5/12/13/14 evidence
  lines, cumulative), then `2:30–4:00 Graded final CryptoVault project demos (10-min demo + 5-min
  Q&A per team)`.
- **Mode:** team (course specification §4: "Final — W18 written (individual) + W19 practical (team)"),
  the pair worth **25%** of the final mark. Project marks are scaled by peer-contribution evaluation
  (course specification §8).
- **Submission:** flags/evidence via the Form, plus the live CryptoVault demo graded by rubric
  (SUBMISSION.md). As in the midterm, the one-line mitigation is the cheapest mark on the paper and
  the most often left blank — say so today.
- **Artefact type is not uniform, and students still get this wrong.** Wk2, 3, 4, 6, 11 and 15 gate on
  a `FLAG_*` string; Wk5, 12, 13 and 14 gate on the **evidence log line** from the worksheet, and no
  flag string exists for those weeks (AGENDA.md's HYBRID callout; SUBMISSION.md's by-week table).
  A student hunting for a flag in the Week 13 logs will burn the block.
- **Instructor note:** reconcile that public description against the instructor-held Week 19 key
  (`instructor/exams/week19-final-ctf-capstone-answers.md`) before you tell students what to revise.
  Today's mock and the exam's own selection are not identical, and students calibrate on whichever
  they hear first.
- **Attribution caveat.** SUBMISSION.md's status note is honest that per-student flags are built but
  not yet live: `instructor/seed_flags.py` exists and is verified, but this course has no running
  CTFd deployment. Until it does, a submitted flag proves little on its own — the payload, the
  mitigation and the viva spot-check are what carry attribution.

### 7.3 What today's mock does *not* reproduce — say this explicitly

| | Mock (today) | Week 19 |
|---|---|---|
| Stakes | ungraded, participation | part of the 25% final (course specification §4) |
| Material | a *repeat* of labs already completed, with hints | the same labs, sat cold, no hints |
| Aids | each lab's `exploit.py` and `worksheet.md` sit in the student's own checkout, and `mock-ctf.md` tells them to self-check against those | none of that is available in the exam |
| Challenge set | eleven published, scoped down in class to fit the slot (§5.3) | fixed by the instructor-held key |
| Capstone | not rehearsed at all | 90 of the 240 minutes are graded demos |

The third row is the one that quietly ruins the calibration: "sat cold" is a request, not a technical
control, because the solution script is one directory away. Ask teams to attempt each challenge with
the lab folder closed and to open `exploit.py` only for the self-check.

### 7.4 Logistics to read out in the debrief

None of these are recorded in the repository:

- Week 18 (written) — date / time / room: ⬚
- Week 19 (practical + demos) — date / time / room: ⬚
- Whether Week 19's CTF teams are the CryptoVault project teams: ⬚
- Whether any aid (one-page sheet, formula card) is admitted to Week 18: ⬚ — announce **today**, it
  changes how the week before the paper gets spent
- Machine readiness: anyone whose targets did not come up today must be fixed before Week 19, not on
  the day

### 7.5 Deliverable

Week 17 publishes **no student deliverable**: unlike Week 7, `labs/week17-review/README.md` asks only
that students review, play, attempt the mock and prepare — there is no cheat-sheet or write-up
requirement, and no worksheet. Whether to require one anyway (for example, the mock's warm-up task
written up: two CWEs, two controls) is an instructor decision: ⬚. If you add one, say so at 2:00,
not at 4:30.

## 8. Assessment for this week

| Instrument | Evidence | Outcome | Weight |
|---|---|---|---|
| Cumulative review quiz | Quiz score | K1, K2 | Part of the 10% weekly-quizzes / participation component |
| Security Jeopardy: Champions Edition | Team points | K1–K3 | Non-graded engagement (Houses/XP); no live CTFd scoreboard for this course yet |
| Mock final CTF | Payload/command + one-line mitigation per challenge attempted | P1, P2, A1 | **Ungraded** — participation |
| Mock warm-up (CWE + control, two challenges each) | Written answers | P3, K2 | **Ungraded** — participation |
| Debrief self-assessment | Named weak areas | P4, A2 | Formative — feeds the instructor's Week 18/19 support list |

There is **no worksheet for Week 17**: the 12 graded worksheets are Weeks 1–6 and 10–15 (course
specification §4). The graded final follows in Weeks 18–19 and is worth 25%; the CryptoVault project
demoed in Week 19 is a further 15%.

## 9. Materials

- Lab: `labs/week17-review/README.md` and `labs/week17-review/mock-ctf.md` (the only two files in the
  folder)
- Quiz: `quizzes/weekly/week17-review-quiz.md`
- Slides: ⬚ — none for this week; the decks under review are `slides/week10.md` … `slides/week15.md`,
  with `slides/week01.md` … `slides/week06.md` behind the callback round
- Mock targets: `labs/week10-hybrid-encryption` (`audit_the_ai/`), `labs/week11-signatures-zkp`,
  `labs/week12-secure-transport`, `labs/week13-e2e-encryption`, `labs/week14-authentication`,
  `labs/week15-pqc`; callback round `labs/week02-hash`, `labs/week03-macs`, `labs/week04-aes-modes`,
  `labs/week05-key-exchanges`, `labs/week06-aead`; early-finisher extension `labs/week15-pqc/hndl`
- Capstone brief and rubric: `project/README.md`, `project/REPORT-TEMPLATE.md`
- Self-check files already in the student's checkout: each lab's `exploit.py`, `fixed_app.py` /
  `docker-compose.fixed.yml` and `worksheet.md`
- Course documents: [AGENDA.md](../../AGENDA.md) (review-week block) ·
  [course-plan-19weeks.md](../../course-plan-19weeks.md) · [syllabus.md](../../syllabus.md) ·
  [SUBMISSION.md](../../SUBMISSION.md) · [ETHICS.md](../../ETHICS.md) ·
  [course specification](../course-specification.md) · [readings.md](../../readings.md)
- Instructor-only, git-ignored: `instructor/week17-jeopardy-bank.md`,
  `instructor/week17-review-quiz-answers.md`, `instructor/exams/item-bank.md`,
  `instructor/exams/week18-final-written-formA.md` / `-formB.md` and their answer files,
  `instructor/exams/week19-final-ctf-capstone-answers.md`,
  `instructor/week10-hybrid-encryption/answer-key.md`,
  `instructor/week11-signatures-zkp-answer-key.md` … `instructor/week15-pqc-answer-key.md`,
  `instructor/seed_flags.py`
- What comes next: the Week 18 written exam and the Week 19 practical plus demos — both
  instructor-held, with no lab folder in the repository (course specification §6 records ⬚ for both)

## 10. Risks and contingencies

| Risk | Mitigation |
|---|---|
| **The lab README says the Jeopardy bank "not yet built" — it is.** An instructor who trusts the README rebuilds a 35-clue board from scratch the night before, or arrives with nothing for the 75-minute middle block | Open `instructor/week17-jeopardy-bank.md` (git-ignored) during preparation; it holds all seven categories, five tiers each, the Final Wager and running notes. **Escalation:** the stale sentence needs fixing in `labs/week17-review/README.md` *and* its curriculum-monorepo copy together, per [CLAUDE.md](../../CLAUDE.md) — not from this plan |
| **`mock-ctf.md` budgets ~165 min into a 150-min slot**, for eleven challenges | Scope the attempt at 2:00 (three main + one callback per team) rather than editing the brief. The timing defect belongs in the lab file, with the monorepo copy and the answer key updated in the same pass |
| **Week 10's CWE is not where the game's dispute rule looks.** The bank rules from each week's `**Analogous CWE:**` line; Week 10's README has none, and CWE-323 for Wk10 appears only in `mock-ctf.md` | Announce the ruling source before the *Asymmetric & Hybrid* category opens. Escalate the missing line rather than patching it here |
| **Weeks 12, 13 and 14 publish no host ports.** Their services listen on `8443` (Wk12) and `8080` (Wk13/14) *inside* the compose network only, so a student hunting `localhost` concludes the lab is broken | Brief all three as log-reading exercises before the block starts: the evidence is a `docker compose … logs` line — `MITM INTERCEPTED: …`, `SERVER SAW: …`, `SERVER SAW PASSWORD: …` — and in fixed mode the evidence is its **absence** (`grep -c` returning `0`) |
| **Vulnerable and fixed modes cannot be up at once** in Weeks 5, 12, 13 and 14: both compose files pin the same `container_name` values (`week12-alice`, `week13-server`, `week14-server`, `week05-relay`, …), and a stale scrollback reads exactly like this run's evidence | Enforce the READMEs' order: `Ctrl-C`, then the matching `docker compose -f … down` (Week 12 uses `down -v`), then start the other file. Grade the `grep -c` count, which is only meaningful in a clean log |
| **Module-level state survives inside a running container.** `labs/week15-pqc/fixed_app.py` signs at most once per container lifetime (a second `/sign` → `403`), and `labs/week11-signatures-zkp` accumulates `_seen_txids` / `_total_withdrawn` | Restart the stack between attempts (`docker compose down` then `up -d`). Warn that the exact `r`, `s`, txids and totals differ every run — the READMEs say so, and a transcript copied from a neighbour will not match |
| **Image builds and container-start `pip install`s on the room network.** Weeks 12, 13 and 14 build from a `Dockerfile`; Weeks 11 and 15 each run `pip install --no-cache-dir -r requirements.txt` in two containers at start | Pre-pull `python:3.12-slim` and build the three image-based stacks the day before; have students start their first target during the 1:45–2:00 break; keep an offline copy (`docker save` / `docker load`) |
| **The repository lives under OneDrive**, and the Week 6 README records that verification had to be run from a scratch copy because placeholder files can break an in-place `docker build` — today three labs build | Pin the tree as "always keep on this device", or copy the lab directory to a local scratch path before building |
| **`python exploit.py` fails on the host.** Week 11's script needs `requests` **and** `ecdsa`; Week 15's needs `requests`; `hndl/`'s needs `pycryptodome` and `sympy` | Have students install the host-side dependencies beforehand or run the exploit from inside a container. Do **not** let anyone "fix" the `ecdsa` advisory (CVE-2024-23342) — it is a documented accepted risk of that lab |
| **Container memory, not port clashes, is the limit.** Ports 8092–8103 plus `hndl`'s 8120/8121 are all distinct, so nothing collides across labs | Run one lab at a time; the challenges are independent and the mock asks for a subset anyway |
| **35 clues plus a Final Wager in 75 minutes** | Decide the drop order in advance (100-tier "define" clues first); protect the Final Wager, which is the only whole-arc item on the board |
| **Revision built only on today's mock skips Week 16** — which has no target and no Jeopardy category, yet carries 90 graded minutes in Week 19 and 15% as a project | Say the gap out loud in the debrief (§4) and ask each team which of the five CryptoVault primitives their self-audit is weakest on |
| **Flags are not yet per-student** (SUBMISSION.md status note; no live CTFd for this course), so a flag pasted between teams is undetectable today | Grade the payload, the mitigation and the viva reproduction, not the string. Say plainly that Week 19 will be marked the same way until the pipeline is live |
| **A student cannot sit the Form quiz** (Forms are posted in this course's Classroom, and only this course's) | Print `quizzes/weekly/week17-review-quiz.md` — it carries name / student-ID / date fields — and mark to the same 25 pts |
| **Someone points the mock at a non-course target** ("it's only practice") | `mock-ctf.md` restates the sandbox-only rule and links [ETHICS.md](../../ETHICS.md); repeat it at 2:00, and treat the practice run under the same rules as the graded one |

## 11. Post-teaching reflection

*Complete after the session — this also feeds the course's engagement data.*

- Attendance / completion: ⬚
- Time actually taken per block (vs. plan), especially whether Jeopardy overran the 1:45 break: ⬚
- Number of mock challenges each team actually landed, and which were left unattempted: ⬚
- Where the class got stuck, and what unblocked them (environment vs. cryptography): ⬚
- Misconceptions from §6 that actually surfaced in the debrief (and any new ones): ⬚
- Whether the Jeopardy clue phrasing tracked the worksheets closely enough to feel like revision
  rather than ambush: ⬚
- Whether the absence of a written-half rehearsal (§7.1) showed up in Week 18 marks: ⬚
- CryptoVault readiness by team, two weeks out from the graded demo: ⬚
- Anything to change before this week runs again: ⬚
