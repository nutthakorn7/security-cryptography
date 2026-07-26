# Lesson Plan — Week 11: Digital Signatures & Zero-Knowledge Proofs — ECDSA Signature Malleability

| | |
|---|---|
| **Course** | Security & Cryptography (`21025117`, per `syllabus.md` — the registrar's official code is otherwise ⬚) |
| **Week / date** | 11 · ⬚ |
| **Kind** | HYBRID — a runnable malleability/double-spend demo (Part 2, Tasks 0–4) alongside conceptual signature/ZKP material that stays written (Part 1 Q1–Q5, Task 5, EiPE-A). Delivered with the **flag pattern**: a genuine per-student `FLAG_SIG`, same as a LAB week (AGENDA.md's HYBRID callout) |
| **Contact time** | 300 min = 120 lecture + 180 laboratory |
| **Lab folder** | `labs/week11-signatures-zkp` |
| **Slides** | `slides/week11.md` |
| **Signature game** | 💰 "Double-Spend the Bank" |
| **Standards** | Analogous CWE (per lab README + `lessons/signatures-zkp/lesson.yml`): **CWE-347** (Improper Verification of Cryptographic Signature) · **CWE-345** (Insufficient Verification of Data Authenticity) |
| **CLOs addressed** | **CLO2** break the misuse · **CLO3** rebuild it correctly · **CLO4** reason about the protocol-level design (schedule table, spec §6) — plus **CLO5** (Audit the AI, EiPE, Prompt Problem) and **CLO6** (Evidence & Integrity) via the recurring worksheet parts (spec §4) |

---

## 1. Session objectives

By the end of this week a student can:

**Knowledge (K) — spans both halves of the hybrid**
- K1 — State the difference between a digital signature and a MAC — which key *creates* the authenticator, which key *verifies* it, and *who* can verify (anyone with the public key vs. only shared-secret holders) — and say why signatures, not MACs, underpin public PKI (Q1).
- K2 — Explain a signature as a **non-interactive zero-knowledge proof of knowledge** of the private key: the Schnorr commitment→challenge→response, and how the **Fiat–Shamir** transform (replace the live challenge with `hash(commitment, message)`) removes the verifier. State the precise nuance the slides make — EdDSA (Ed25519) *is* a Fiat–Shamir transform of Schnorr, whereas ECDSA is *also* a NIZK proof of knowledge of the private key but **not** a literal Fiat–Shamir/Schnorr construction (its hash covers only the message, not the commitment) (Q2).
- K3 — Define **signature malleability**: for a valid ECDSA `(r, s)`, the twin `(r, n − s)` (n = the SECP256k1 group order) is *also* valid for the *same* message and key but is a different byte string. Name why this is a **SUF-CMA** violation that leaves **EUF-CMA** intact (Q5c).
- K4 — Explain why deduplicating a transaction by a **signature hash** (`sha256(str(r)+str(s))`) lets the twin through, while deduplicating by `(message, pubkey)` would not; and why **low-S / BIP-62** normalisation leaves exactly one canonical signature per `(message, key)` (Q5d, Task 5).

**Skills (P) — the runnable demo half**
- P1 — Read `vulnerable_app.py`'s `txid_of` and `withdraw`, quote the exact line that decides a transaction's identity, and confirm it hashes the *signature* rather than the `(message, pubkey)` (Task 0).
- P2 — Obtain a valid `(r, s)` from `GET /sign` and the bank's key from `GET /pubkey`, then compute the twin `s' = n − s` by hand (using `n = ecdsa.SECP256k1.order`), confirm the two txids differ, and identify which of `s`, `s'` is low-S (Tasks 1–2).
- P3 — Double-spend by hand with `curl` against `:8102` — submit `(r, s)` then `(r, n − s)` in that order against a freshly started container — capture the personalised `FLAG_SIG` and the `double_spend_detected` / `total_withdrawn:200` response, then re-confirm with `python exploit.py` (Task 3).
- P4 — Run the identical `(r, s)` then `(r, n − s)` sequence against `:8103` and show the low-S first submission is accepted (one legitimate withdrawal) while the high-S twin is rejected `403` with no flag; point to the added `is_low_s` guard in `fixed_app.py` (Task 4).

**Attitude (A)**
- A1 — Attack only the two local containers this lab spins up (`:8102` / `:8103`). Forging or replaying transactions against real payment systems, exchanges, or blockchains you do not own is illegal (worksheet ethics note); keep the `FLAG_SIG` inside the lab. See [ETHICS.md](../../ETHICS.md).
- A2 — Submit identity-stamped evidence (`whoami` / login email / student ID + a timestamp) and a per-student flag that is your own, and be able to reproduce it live on request.
- A3 — Treat AI-generated cryptographic code as something to *verify, not trust* — the *Audit the AI* helper "looks robust" yet reintroduces the very dedup-by-signature flaw this lab exploits.

## 2. Key ideas (the through-line)

A signature is a stronger claim than a MAC: it answers "did *you* write this, and can *anyone* check?" using an asymmetric keypair, which is why public PKI is built on signatures and not on shared-secret MACs. Underneath, a signature is a **non-interactive zero-knowledge proof of knowledge** of the private key — the Schnorr identification protocol with its live challenge replaced by a hash (Fiat–Shamir). Keep the slides' precision here: EdDSA is literally that transform of Schnorr; ECDSA is a NIZK proof of knowledge of the private key too, but not a literal Fiat–Shamir/Schnorr construction.

The break this week is **not** about forging a signature — ECDSA's unforgeability (EUF-CMA) holds. It is one level up, in a *system-design* assumption: the demo bank assumed "a valid signature is a unique transaction identity." ECDSA signatures are **malleable** — every `(r, s)` has a valid twin `(r, n − s)` — so a bank that computes `txid = sha256(str(r)+str(s))` sees one authorised withdrawal as two transactions and processes it twice, the root cause of a MtGox-era class of loss. The fix is **canonicalisation, not smarter verification**: enforce low-S (BIP-62) so exactly one of `{s, n − s}` is acceptable, and the twin has nowhere to hide. The deeper, defence-in-depth lesson (Q5d, EiPE) is to derive transaction identity from `(message, pubkey)` or an application-level nonce, so the identity never depends on malleable signature bytes at all.

## 3. Prior knowledge and preparation

- **Students, before class:** Docker Desktop working (same Docker-first setup as `software-security`); skim last week's recap (Week 10 — asymmetric & hybrid encryption). Have Python 3.12 — or at least the `ecdsa` and `requests` packages — on the host to run `exploit.py`, or plan to use the throwaway-container form the README documents.
- **Instructor, before class:** pre-pull `python:3.12-slim` and do one dry run — each container runs `pip install --no-cache-dir -r requirements.txt` (flask, requests, **ecdsa**) *at startup*, so the first `docker compose up` needs working network; a room installing at once is the usual way to lose the first 15–20 minutes. `exploit.py`'s `wait_for` only polls for 40 s, so confirm both apps answer `curl localhost:8102/` and `localhost:8103/` before students start. Decide the flag mode (see §5). Note the accepted `ecdsa` advisory in §8 so it is not mistaken for a lab defect.
- **Prerequisite concepts:** what a public/private keypair is and what "verify with the public key" means; that ECDSA produces a pair `(r, s)`; basic modular arithmetic (`n − s`). The full ECDSA signing/verification equations are re-derived on the slides — students do not need them in advance.

## 4. Lecture — 120 min

| Time | Block | Content | Method |
|---|---|---|---|
| 0:00–0:10 | Weekly quiz + recap | ~10-min retrieval quiz on Week 10 (asymmetric/hybrid encryption); today's agenda | Individual quiz, lowest 1–2 dropped |
| 0:10–0:55 | Core concepts (conceptual half) | Signatures vs. MACs and why PKI needs signatures (Q1); a signature as a non-interactive ZKP — Schnorr commit→challenge→response, then Fiat–Shamir; the EdDSA-is-Schnorr / ECDSA-is-not-literal-Fiat–Shamir nuance (Q2); RSA vs. ECDSA vs. EdDSA and their correctness pitfalls, naming reused-nonce key recovery as a *different* bug from today's (Q3) | Lecture + board work (three arrows: commit → challenge → response) |
| 0:55–1:05 | Break | | |
| 1:05–1:35 | The demonstrable half + real case | Inside an ECDSA `(r, s)`; why `s` enters verification only via a value unchanged when `s → n − s`, so the twin `(r, n − s)` verifies too (malleability); where it bites — dedup by signature hash; the MtGox transaction-malleability incident, stated honestly as *one contributing factor among several claimed*, not the sole cause | Lecture + live walkthrough on the projector |
| 1:35–1:55 | Correct construction / defences + out-of-scope | Low-S / BIP-62 canonicalisation (`s ≤ n//2`) and why exactly one of `{s, n − s}` survives; SUF-CMA vs. EUF-CMA as the precise names for the gap; defence-in-depth (dedup by `(message, pubkey)`); state explicitly what stays out of the demo — the whole ZKP/Schnorr half is *written*, and nonce-reuse key recovery is a *separate* attack this lab does not perform | Lecture with `vulnerable_app.py` vs. `fixed_app.py` code-diff |
| 1:55–2:00 | Signature-game briefing | 💰 "Double-Spend the Bank" — double-spend `:8102`, then prove `:8103` (low-S) rejects the twin. Flag the tricky PASS condition: the fixed app must still accept the *first* legitimate withdrawal; PASS ≠ "both rejected" | Instruction → to lab |

**Checks for understanding during lecture**
- After the core concept: cold-call — *"a signature verifies True — does that guarantee this exact signer signed this exact message, and that it is the only valid signature?"* (sets up Q4 substitution attacks and malleability).
- Before the break: one-minute paper — *"the bank verifies every signature correctly and rejects an exact replay — so how does the same authorisation still get processed twice?"* (ties to Task 0 and viva question 2).

## 5. Laboratory — 180 min

Targets: `docker compose up -d` in `labs/week11-signatures-zkp` → `vulnerable_app.py` (dedup by `sha256(str(r)+str(s))`) on **`:8102`**, `fixed_app.py` (low-S / BIP-62, then dedup) on **`:8103`**. Each bank generates its **own** SECP256k1 keypair fresh at container startup (repo policy: no private key is ever committed); `GET /sign` is the lab convenience that signs the one fixed message `"withdraw 100 to attacker"` with that bank's key.

**Environment setup** (from the worksheet, quoted exactly):
```bash
cd labs/week11-signatures-zkp
docker compose up -d        # vulnerable_app.py on :8102, fixed_app.py on :8103
curl localhost:8102/        # confirm it's up
```
Per-student flag (from README, run inside `labs/week11-signatures-zkp` *before* `docker compose up`):
```bash
python3 ../../instructor/seed_flags.py env <STUDENT_ID> > .env
```
The attributable evidence artifact for this HYBRID week is the captured **`FLAG_SIG`** (env var; manifest key `sig` in `lessons/signatures-zkp/lesson.yml`) returned by the *vulnerable* bank on the second, malleated withdrawal — the fixed bank never emits it. Because a fresh keypair and a random nonce `k` are generated at each boot, the concrete `r`, `s` and txids differ every run; only the flag is stable and attributable — do not expect students to reproduce a fixed transcript.

Laboratory table — **one row per actual worksheet task, with the worksheet's own minute budgets**. The Mode column marks which tasks are the runnable demo and which are written analysis (this is a HYBRID week). The six numbered tasks (0–5) budget to **125 min**; the rest of the 180-min block is the Evidence & Integrity and the recurring AI-resilient / micro-demo / submit blocks from AGENDA.md's HYBRID template (see the note under the table).

| Time | Task | Budget | Mode | Student does | Evidence produced |
|---|---|---|---|---|---|
| 0:00–0:15 | **Onboarding + Task 0** — see the vulnerable design | 15 min (Task 0) | Runnable + read | `docker compose up -d`; while the containers `pip install`, read `vulnerable_app.py`'s `txid_of` (L48–51) and `withdraw`; quote the line that decides transaction identity and confirm it hashes the *signature*, not `(message, pubkey)` | Both apps up; the quoted line + one sentence on why that choice makes malleability exploitable |
| 0:15–0:30 | **Task 1 — Obtain a valid signature** | 15 min | Runnable | `curl localhost:8102/sign` (record `sig_r`, `sig_s`, the fixed `message`); `curl localhost:8102/pubkey` | The `(r, s)` pair + the pubkey hex |
| 0:30–1:00 | **Task 2 — Malleate by hand** | 30 min | Runnable + written | With `n = ecdsa.SECP256k1.order`, compute `s' = n − s`; compute both `sha256(str(r)+str(s))` and `sha256(str(r)+str(s'))`, confirm they differ; state which of `s`, `s'` is low-S (`≤ n//2`) — exactly one is | `s'`, the two txids, and which one is low-S |
| 1:00–1:20 | **Task 3 — Double-spend & capture the flag** | 20 min | Runnable | **By hand with `curl` first**, against a freshly started container: `POST /withdraw` with `(r, s)` then with `(r, n − s)`; *then* run `python exploit.py` as automated confirmation | Flag + the two `curl` commands + the second response showing `double_spend_detected` and `total_withdrawn:200` |
| 1:20–1:40 | **Task 4 — Confirm the fix rejects the trick** | 20 min | Runnable | Watch `exploit.py` repeat `(r, s)` then `(r, n − s)` against `:8103`; confirm the low-S first submission is accepted and the high-S twin is `403` with no flag; read `fixed_app.py`'s `is_low_s` (L50–52) and its guard (L102–103) | The `403` + body + the one-line difference vs. `vulnerable_app.py`'s `withdraw`, in words |
| 1:40–2:05 | **Task 5 — Explain why, precisely** | 25 min | Written | Answer: (a) why `(r, s)` and `(r, n − s)` are *both* valid for the same message and key; (b) why dedup by signature hash lets the twin through while dedup by `(message, pubkey)` would not; (c) why low-S leaves exactly one canonical signature | Three short paragraphs, one per sub-question |
| 2:05–2:25 | **Evidence & Integrity** | 20 min | — | Capture identity-stamped evidence (`whoami` / login email / student ID + timestamp) for Tasks 1–4; record the personalised flag; write the two own-words explanations (why the double-spend worked; why low-S stops it, and what could still break a bank that used low-S but *still* dedups by signature hash) | Flag + own-words explanations |
| 2:25–2:45 | **AI-resilient tasks** | 20 min (AGENDA) | — | *Audit the AI* (find the dedup-by-signature flaw in the AI `process()` helper and rewrite it — canonicalise low-S and/or derive the txid from `(message, pubkey)`); *Explain-in-Plain-English* (ZKP without sending the secret); *Prompt Problem* (why ECDSA is malleable but Ed25519 is not) | Written answers (start in class, finish as homework) |
| 2:45–2:55 | **Rotating micro-demo** | 10 min (AGENDA) | — | 2–3 rotating students give a 2–3 min "show your double-spend / show the fixed app's 403" | Live reproduction |
| 2:55–3:00 | **Submit** | 5 min (AGENDA) | — | Everyone submits | Worksheet PDF → Classroom; exploit notes/fix → GitHub ([SUBMISSION.md](../../SUBMISSION.md)) |

> **Timing note for the instructor.** The worksheet titles Part 2 "Hands-on Lab + Defense (180 min)", which is the whole lab-session length; its six numbered tasks (0–5) budget to **125 min**. Task 0 needs no running container — its steps are "read `vulnerable_app.py`'s `txid_of` and `withdraw`" — so it runs **concurrently** with the 15-min onboarding while both containers `pip install` unattended; the table folds them into one 0:00–0:15 row rather than adding a block. Tasks 1–5 then occupy 0:15–2:05 at exactly the worksheet's stated per-task budgets (15/30/20/20/25). The remaining 55 min holds the Evidence & Integrity block plus the AI-resilient / micro-demo / submit tail from AGENDA.md's HYBRID template — **no per-task budget has been altered.** If a group races ahead, the 2:05–2:25 window absorbs the slack; if they stall, Task 5 (reasoning) is the one to start in class and finish as homework.

**Formative checkpoints.** A student stuck on Task 3 who cannot land `total_withdrawn:200` has almost always already run `exploit.py` (or a repeat submission) against the same container: `vulnerable_app.py`'s `_total_withdrawn` and `_seen_txids` are **module-level, in-memory state that never resets between requests**, so the by-hand `curl` pair must be the *first* withdrawal attempt against a freshly started container. Only restarting the vulnerable container (fresh process, state back to zero) restores the reproducible 100→200 sequence — send them to restart the container, not to a new payload. Tasks 0–3 should be done by ~1:20 for the fix confirmation (Task 4) and reasoning (Task 5) to fit.

## 6. Assessment for this week

Worksheet 11's own rubric (100 points):

| Criterion | Points | Assesses |
|---|---|---|
| Part 1 — Conventional written questions (Q1–Q5) | 25 | CLO1, CLO4 |
| Part 2 — Lab tasks 0–5 (captured `(r,s)`/twin, both txids, `curl` output, `403` on fixed) | 30 | CLO2, CLO3 |
| Evidence & Integrity (flag capture + own-words explanation) | 10 | CLO6 |
| Audit the AI (flaw(s) found + corrected `process()` design) | 20 | CLO5 |
| Comprehension & Prompt (EiPE on ZKP + Prompt Problem) | 15 | CLO5 |

How the 100-point worksheet feeds the course marks (spec §4):

| Instrument | Outcome | Course weight |
|---|---|---|
| Worksheet 11 (all parts above) | CLO1–CLO6 | Part of the 30% weekly-worksheet component |
| Weekly quiz (start of lecture) | CLO1, CLO4 | Part of the 10% quiz + participation component |
| Viva spot-check / micro-demo | Live reproduction and explanation | Pass/fail gate on the Lab + Audit-the-AI scores (worksheet rubric note; spec §9) — an instructor who is not convinced you did the work may re-score those sections down |
| Per-student flag | Attributable evidence (submitting another student's flag is a violation) | Integrity control, not a separate mark |

Viva spot-check questions are held by the instructor in `worksheet.md` (three questions); do not pre-circulate them. Grading detail and partial-credit rules are in the worksheet's own rubric.

## 7. Materials

- Lab: `labs/week11-signatures-zkp/` — `vulnerable_app.py` (`:8102`), `fixed_app.py` (low-S, `:8103`), `exploit.py`, `docker-compose.yml`, `requirements.txt`, `worksheet.md`, `README.md`.
- Slides: `slides/week11.md`.
- Per-student flags: `instructor/seed_flags.py` (git-ignored thin shim to the curriculum monorepo's shared `tools/seed_flags.py`; challenge-key vocabulary `sig` comes from `courses/security-cryptography.yml`). See the README for the `.env` recipe and the `FLAG_SIG` override.
- References (from the lab README and `readings.md`): Boneh & Shoup, *A Graduate Course in Applied Cryptography*, ch. 8 (digital signatures) & the Schnorr / Fiat–Shamir treatment; Bitcoin **BIP-62** and **BIP-146** (the low-S rule); the MtGox transaction-malleability write-ups; NIST FIPS 186-5 (*Digital Signature Standard*); RFC 8032 (*EdDSA*).
- Submission channels: [SUBMISSION.md](../../SUBMISSION.md) · Rules of engagement: [ETHICS.md](../../ETHICS.md).

## 8. Risks and contingencies

| Risk | Mitigation |
|---|---|
| First `docker compose up` stalls because each container installs `flask` / `requests` / `ecdsa` at startup and the room's network is slow | Pre-pull `python:3.12-slim` and do one dry run; `exploit.py`'s `wait_for` only polls for 40 s, so confirm both apps answer `curl localhost:8102/` and `localhost:8103/` before students start |
| Ports **8102** / **8103** already bound on a student's machine | Override the published ports in `docker-compose.yml`; note these are 8102/8103, not the 8080/5000 of the sibling course, so the macOS AirPlay-on-5000 clash does not apply here |
| Task 3 by-hand `curl` never lands on `total_withdrawn:200` | `vulnerable_app.py`'s `_total_withdrawn` / `_seen_txids` are module-level, in-memory state that never resets between requests; a student who ran `exploit.py` (or repeated a submission) first has advanced the counter and gets `409 replay` on an exact repeat or 300/400 on a fresh one. Restart the *vulnerable* container so the process (and its state) starts clean, then do the by-hand pair *first* — exactly the order the worksheet's Task 3 prescribes |
| A `(r, s)` copied from `:8102` and replayed against `:8103` returns a confusing `403` | Each bank generates its **own** keypair at startup, and `fixed_app.py` runs `is_low_s` (L102–103) *before* `VK.verify` (L107–109). A foreign low-S signature clears the low-S gate then fails verification → `403 {"error": "bad signature"}` — a *different* 403 from the expected `403 {"error": "non-canonical signature: s must be <= n/2 (BIP-62 low-S)"}`. Read the JSON body, not just the status code, and call `/sign` on each host separately. `exploit.py` is **not** affected — its `run_double_spend` calls `get_signed_message(host, port)` per target |
| Student sees the fixed app accept the first withdrawal and concludes "the fix is broken" | The PASS condition is *first accepted, malleated twin rejected, no flag* — **not** "both rejected." Reinforce from the README/slides callout; a fixed bank that refused the legitimate withdrawal would be broken in the other direction |
| `ecdsa` flagged by a scanner / Dependabot (CVE-2024-23342, Minerva timing side-channel) mistaken for a lab defect | This is a documented **accepted risk** — no patched version exists, the maintainers declared side channels out of scope, the keypair is ephemeral and in-memory, and this week's actual attack (malleability) is unrelated to a timing side-channel. Leave the pin as-is; do **not** bump it (see the README's "Known dependency risk" note and `requirements.txt`) |
| Host is missing `ecdsa` / `requests`, so `exploit.py` will not run | Use the README's throwaway-container form (run `exploit.py` inside `python:3.12-slim` on the compose network) instead of installing on the host — note it depends on the checkout keeping its directory name, since Compose derives the network name from it |
| Per-student `.env` not generated, so everyone captures the same default flag → non-attributable submissions | Generate `python3 ../../instructor/seed_flags.py env <STUDENT_ID> > .env` before `docker compose up`; the personalised `FLAG_SIG` + identity-stamped evidence + viva spot-checks are the integrity control |
| A student finishes the double-spend early | Extension (viva q.3 / Q5d): implement the *protocol-level* fix — dedup by `(message, pubkey)` — and argue why it defeats malleability even without low-S; or explain one malleability source low-S does **not** close (e.g. non-canonical DER encoding, `scriptSig` mutation in the real Bitcoin case) |

Remember to `docker compose down` at the end of the session.

## 9. Post-teaching reflection

*Complete after the session — this also feeds the course's engagement data.*

- Attendance / completion: ⬚
- Time actually taken per task (vs. plan — the 125-min task budget is untested with real students): ⬚
- Where the class got stuck (Task 2 hand-computation of the twin vs. Task 3 state-order reproduction), and what unblocked them: ⬚
- Misconception that showed up in the *Explain-in-Plain-English* ZKP answers: ⬚
- Quality of the *Audit the AI* critiques — did students reject the "derive the txid from the signature is *better* than hashing the message" claim and rewrite it, or stop at catching the exact-replay case (which the AI already handles)?: ⬚
- Anything to change before this week runs again: ⬚

---

> **Instructor notes — stale cross-references in the lab README (report only; do not edit lab content).** Two pointers in `labs/week11-signatures-zkp/README.md` (the per-student-flag paragraph, ~L93–96) have gone stale and would mislead an instructor setting up flags:
> 1. It says the `seed_flags.py` recipe applies "once this course's `instructor/seed_flags.py` exists" — but that file **now exists** (a thin shim to the monorepo, built and marked DONE in `course-plan-19weeks.md`'s resolved decision #5). The conditional should be dropped.
> 2. It cites "`course-plan-19weeks.md` open decision #4" for the flag-minting deferral, but decision #4 there is the *resolved* `airsec_flag_bridge` de-inline — a different topic; the `seed_flags.py` work is decision #5. The reference points at the wrong (and resolved) item.
>
> Both are **describe-don't-fix**: correcting them means editing `labs/week11-signatures-zkp/README.md` **and** the byte-identical `../KOSEN69 - curriculum/lessons/signatures-zkp/README.md`, or the parity gate trips. The same "open decision #4" pattern also appears in the Week 2/3/4 READMEs, so a fix should be applied consistently. Flagged in this plan's `escalated` output.
