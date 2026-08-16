# Lesson Plan — Week 10: Asymmetric & Hybrid Encryption

| | |
|---|---|
| **Course** | Security & Cryptography · course code `21025117` (per [syllabus.md](../../syllabus.md); [course-specification.md](../course-specification.md) §1 leaves the field ⬚ — *"Confirm against the registrar before print if in doubt."*) |
| **Week / date** | 10 · ⬚ |
| **Contact time** | 300 min = 120 lecture + 180 studio (AGENDA.md per-week table; the ~10-min weekly quiz sits *inside* the 120-min lecture block, not on top of it) |
| **Kind** | **CONCEPTUAL** — no Docker target, no flag, rubric-graded ([course-specification.md](../course-specification.md) §6) |
| **Lab folder** | `labs/week10-hybrid-encryption` — `README.md`, `worksheet.md`, `audit_the_ai/README.md`, `audit_the_ai/broken_hybrid_encrypt.py`. **That is the whole folder**: no `docker-compose.yml`, no `requirements.txt`, no flag |
| **Slides** | `slides/week10.md` (17 slides, Marp) |
| **Standards** | NIST SP 800-56A Rev. 3 (pair-wise key establishment) · NIST SP 800-38D (GCM/GMAC), §8.2 nonce-uniqueness requirement · OWASP Cryptographic Storage Cheat Sheet · SEC 1 §5.1 (ECIES) · CWE-323 (Reusing a Nonce, Key Pair in Encryption) · Joux, *Authentication Failures in NIST version of GCM* (2006) |
| **CLOs addressed** | **CLO1** select & justify the primitive · **CLO4** protocol-level reasoning · **CLO5** evaluate AI-generated code & communicate — schedule row, [course-specification.md](../course-specification.md) §6. **CLO6** (evidence & ethics) is carried by the worksheet's *Evidence & Integrity* section per §4 |
| **Signature game** | 🔬 "Nonce Detective" |

> **Standards note.** CWE-323 is named on `slides/week10.md`; the NIST, OWASP, SEC 1 and Joux
> references are the ones listed in `labs/week10-hybrid-encryption/README.md` and
> `audit_the_ai/README.md`. No OWASP Top-10 category is mapped to this week anywhere in the
> repository and none is invented here.

---

## 1. Session objectives

Taken from `labs/week10-hybrid-encryption/README.md` "Objectives", the worksheet's own Parts 2–5,
and `audit_the_ai/README.md`. By the end of this week a student can:

**Knowledge (K)**
- K1 — Explain why asymmetric encryption alone is unsuitable for bulk data — **both** the
  performance cost and the message-size ceiling — and why hybrid encryption exists to solve that.
  The deck states the concrete figure: RSA-4096-OAEP has *"roughly a **446-byte plaintext
  ceiling**"*, and the fix *"isn't 'use a bigger RSA key'"*. **Fixed — see *Escalations* #13
  (resolved)** — 446 bytes is the correct ceiling for the OAEP-SHA256 this lab actually uses;
  teach the *shape* of the limit (bulk data doesn't fit), and the figure on the slide is now
  accurate too.
- K2 — Trace the complete hybrid-encryption flow end to end: key generation, key wrapping,
  symmetric encryption, transmission, unwrapping, decryption — Bob's side, the wire, Alice's side.
- K3 — Explain how a published public key lets **anyone** encrypt to a recipient, while only the
  holder of the matching private key can decrypt, and why Bob cannot decrypt his own ciphertext.
- K4 — Explain asymmetric key exchange (how two parties derive a shared secret an eavesdropper who
  sees both public values cannot compute) and connect it to **ECIES** as a concrete hybrid scheme
  built on ECDH — ephemeral key pair → ECDH → **KDF** → AEAD, with the ephemeral public key and
  nonce travelling in the clear.
- K5 — State what NIST SP 800-38D §8.2 requires of a GCM nonce (**unique** per (key, nonce) pair —
  not merely "random") and what a violation costs: on the slides' own algebra,
  `C1 = P1 ⊕ KS` and `C2 = P2 ⊕ KS` give `C1 ⊕ C2 = P1 ⊕ P2`, and per Joux (2006) reuse under GCM
  also puts the **authentication** guarantee at risk, not only confidentiality.

**Analysis skills (P)** — this week's skills are analytical and code-audit skills; there is no
running target to exploit.
- P1 — Verify *for themselves* that `broken_hybrid_encrypt.py`'s RSA-OAEP usage, AES-256 key
  generation and GCM tag handling are genuinely correct — and recognise that a passed checklist,
  and a round trip that succeeds, are not evidence that a scheme is secure.
- P2 — Find the one planted bug and quote the exact line(s) — *"It is not in the RSA/OAEP code."*
- P3 — Write a short proof script that uses `HybridEncryptor` to send **two** different messages in
  one session and demonstrates a concrete consequence available to an attacker who sees only the
  two ciphertexts, and report the script's output. *"Prove it, don't just assert it."*
- P4 — Produce `fixed_hybrid_encrypt.py` — the **smallest** correct fix — that satisfies all three
  constraints stated in `audit_the_ai/README.md`: RSA key size / OAEP scheme / AES key size
  unchanged; Bob can still send multiple messages per session without re-wrapping the key per
  message; and anything the fix needs beyond the AES key must travel to Alice *with the ciphertext,
  in the clear*.
- P5 — State explicitly **why the RSA/OAEP portion of the file did not need to change**.
- P6 — Write one prompt asking an AI assistant to implement ECIES in Python, run it, and critique
  the result bullet-by-bullet against the worksheet's five-point checklist (standard curve · KDF
  from the ECDH shared secret rather than the raw secret · authenticated encryption · nonce
  handling and transmission of the ephemeral public key · point validation, constant-time
  comparison, error messages that leak *where* decryption failed), marking each item
  correct / incorrect / hand-waved **with the specific line quoted**.
- P7 — Explain to a non-technical stakeholder, in 3–5 sentences with no jargon, why real systems
  mix AES into an RSA design instead of using RSA for everything.

**Attitude (A)**
- A1 — Work within [ETHICS.md](../../ETHICS.md). There is no target to attack this week; the only
  third-party system any student touches is the AI assistant used in Part 4B, and ETHICS rule 5
  (handle credentials and secrets safely) governs what may be pasted into it.
- A2 — Disclose AI assistance in Part 1 (tool + what was asked), and submit work they can defend
  live, with no notes, in the Part 5 viva.
- A3 — Treat AI-generated cryptographic code as something to be verified, not trusted: *"It runs.
  It round-trips correctly. It has exactly one planted bug."*

## 2. Key ideas (the through-line)

The course spine — *textbook-secure primitive, real-system failure* — reaches the primitive that
**fixed** the previous failure. Week 6 introduced AEAD as the answer to the padding oracle; Week 10
takes a file in which AES-GCM, RSA-OAEP and AES-256 are all used correctly and shows the system
broken anyway.

Two ideas do the work. First, **hybrid encryption is a division of labour**: asymmetric
cryptography is priced per operation and capped in message size, so it is spent once, on something
small — a session key — and symmetric AEAD carries every message after that. ECIES is the same
shape with ECDH standing in for RSA-OAEP as the key-delivery step. Second, **the guarantee lives in
the discipline around the primitive, not in the primitive**: GCM's keystream is a function of
(key, nonce), so the moment a (key, nonce) pair repeats, `C1 ⊕ C2 = P1 ⊕ P2` and any crib peels
both plaintexts apart — with no key, no interaction, and no need to touch RSA at all. Where Week 6's
padding oracle needed an **active** attacker running queries, this needs only a **passive**
eavesdropper with two recorded messages, which is a large step down in what an attack costs to
mount.

That is why this is a CONCEPTUAL week rather than a lab with a missing flag: *"Nothing here is a
'break into a running service' exploit — it's protocol design and correctness analysis."* The
hands-on core is an audit, and what is graded is the reasoning, the proof and the fix.

## 3. Prior knowledge and preparation

**Students, before class**
- Per the lab README: *"No environment setup needed — this week is Python-only, standard library +
  `cryptography` (already used in earlier weeks)."* See the instructor caveat below — that
  sentence is true about Docker and misleading about `cryptography`.
- The README says to *"skim last week's recap (Key Exchanges)"*. Note the mismatch before you send
  this instruction out: Key Exchanges is **Week 5**, the previous *teaching* week is **Week 6**
  (AEAD), and Weeks 7–9 (review + the two midterm sittings) sit in between. `slides/week10.md`
  recaps **Week 6**. Tell students which recap you actually want. See *Escalations*.
- Starred pre-reading for W10 ([readings.md](../../readings.md)): ⭐ RFC 8017 — PKCS #1 (RSA-OAEP);
  an ECIES / hybrid-encryption explainer; Boneh & Shoup, *A Graduate Course in Applied
  Cryptography*, public-key encryption chapters.

**Instructor, before class**
- **Check that `cryptography` is importable on the student machines, not just in Docker.** This is
  the one environment risk this week actually has. The lab folder ships **no `requirements.txt`**
  and **no container**; earlier weeks installed the package *inside* their images (e.g.
  `labs/week04-aes-modes/requirements.txt` pins `cryptography>=48.0.1`), so a student whose only
  exposure to it was through `docker compose up` may have it nowhere on the host. Verified
  reference run for this plan: Python 3.14.3 with `cryptography` 49.0.0, and
  `python broken_hybrid_encrypt.py` — including the RSA-4096 key generation — completes in about
  **0.4 s** end to end (five repeated RSA-4096 key generations measured 0.07–1.19 s). Nothing here
  is slow; the only way to lose time is a missing package or a missing interpreter alias (§8).
- **Decide the 0:00–0:10 quiz slot.** `quizzes/weekly/` contains only `week07-review-quiz.md` and
  `week17-review-quiz.md`; there is **no Week 10 instrument**. Week 10 quiz item: ⬚.
- **Decide the studio-timing question in §5 and the per-student-variant question in §6** *before*
  the session and before marking, not during. Record both in §9.
- **Decide the submission channel for `fixed_hybrid_encrypt.py`** — the lab README and
  SUBMISSION.md disagree (§7, *Escalations*).
- Have `instructor/week10-hybrid-encryption/answer-key.md` and `reference_fixed.py` open for the
  Part 3 rubric bands and the viva expected-answer notes. **Instructor-only, git-ignored** — never
  shown to students, pasted into slides, or reproduced in this plan.
- Run `python broken_hybrid_encrypt.py` yourself once on the room's standard image, so you know
  which interpreter alias works before thirty students ask.

**Prerequisite concepts:** XOR over byte strings; what a nonce/IV is and why AEAD needs one
(Week 6); Diffie–Hellman as a shared-secret construction (Week 5). Python at the level of reading
a class with a constructor and two methods.

## 4. Lecture — 120 min

Row boundaries are AGENDA.md's **CONCEPTUAL-week** lecture template; the content column maps
`slides/week10.md` onto it in deck order, with each slide's own speaker-note time hint in brackets.

| Time | Block | Content (slides) | Method |
|---|---|---|---|
| 0:00–0:10 | Weekly quiz + recap | Quiz instrument: ⬚ (none exists for Week 10). Opening hook — *"if RSA can encrypt anything, why does every real system — TLS, Signal, age, PGP — bolt AES onto it instead of just using RSA?"* [~2] · "Today" roadmap, including "no Docker target this week" [~1] · "Recap — Week 6": AEAD closed the padding-oracle hole; today AES-GCM returns, *"genuinely correct, and still breakable"* [~3] | Hook question, hold the answer; cold-call the recap |
| 0:10–0:55 | Core concepts | "Why not just use RSA for everything?" — speed, the ~446-byte RSA-4096-OAEP ceiling *(deck figure — verified correct; see Escalations #13, resolved)*, OAEP overhead [~6] · "Hybrid encryption: wrap once, encrypt many" — the five-step flow [~8] · "Public-key encryption in one slide" [~6] · "Asymmetric key exchange" — ECDH, discrete-log hardness [~8] · "ECIES: hybrid encryption on ECDH" [~8] | Lecture + board work: draw the flow as a numbered diagram (Bob's side / the wire / Alice's side) and connect it to the TLS handshake. |
| 0:55–1:05 | Break | | |
| 1:05–1:35 | Worked analysis (whiteboard, not Docker) | "A shallow review would stop here" — the four checks a rushed reviewer makes, all genuinely passing [~5] · "The failure mode: nonce reuse under GCM" — SP 800-38D §8.2, CWE-323, the *shape* of the bug [~6] · "The break: what a passive eavesdropper gets" — derive `C1 ⊕ C2 = P1 ⊕ P2` [~8] | Set the trap explicitly, then walk the algebra slowly on the board — this is the "aha" the studio is built around |
| 1:35–1:55 | Design trade-offs / where real systems get this wrong | "Worse: it's not just confidentiality" — active oracle (Wk 6) vs. passive eavesdropper; Joux 2006, the forbidden attack [~6] · "The fix — general principle": random-per-message **or** counter, pick one, don't mix; the nonce is not secret and travels in the clear; RSA/OAEP untouched [~6] | Lecture + contrast of attacker models; ask *"why doesn't this fix touch the RSA/OAEP code at all?"* and get it said out loud before the studio |
| 1:55–2:00 | Brief the studio | 🔬 "Signature game — Nonce Detective" [~4] · "Lab today" — Worksheet 10 Parts 1–5, start at `audit_the_ai/README.md` [~4] · "Key takeaways" [~3] · "Questions?" [~1] | Instruction. **Explain the game; do not demo the answer** |

**Capacity note — the closing row is over-subscribed.** The deck's own speaker-note budgets total
**≈85 min**; with the 10-min quiz slot and the 10-min break that accounts for ≈105 of the 120 min,
leaving ≈15 min of genuine discussion slack. But that slack is not evenly spread: the four slides
assigned to the 1:55–2:00 briefing row carry **≈12 min** of notes against a **5-min** row. The
0:10–0:55 and 1:05–1:35 rows each run ≈9–11 min under their boundary, so start the briefing early
rather than compressing it — the "Lab today" slide is what points students at
`audit_the_ai/README.md`, and cutting it costs studio time later.

**Checks for understanding during lecture**
- On the Week 6 recap slide: *"what made GCM immune to the padding oracle?"* (No padding step; the
  tag is verified before any plaintext is released.) Then the pivot: immune to *that* attack is not
  the same as unbreakable.
- After "Hybrid encryption: wrap once, encrypt many": *"what's the biggest thing you could
  RSA-encrypt directly?"* — get them to the size ceiling themselves.
- After "A shallow review would stop here": *"what would you check next, if anything?"*
- After the break-algebra slide: *"does the attacker need to break RSA to do this?"* (No — RSA-OAEP
  is never touched; the break is entirely downstream of the key.)
- **Teach the failure mode in general, not the file.** The deck's own note is explicit that the
  nonce-reuse slide is *"genuinely new content, not the lab spoiler — teach the general shape of
  the bug … not the specific file's line."* Do not open `broken_hybrid_encrypt.py` on the
  projector; the 35-point task is finding it.

## 5. Studio / analysis — 180 min

No `docker compose up`, no target, no flag. Row boundaries are AGENDA.md's **CONCEPTUAL-week** lab
template; the "Student does" column is built from Worksheet 10's own Parts and from
`audit_the_ai/README.md`'s six numbered steps. **Worksheet 10 publishes no minute budgets of its
own** — none are invented here, so within a row the ordering is the worksheet's and the boundary is
the AGENDA's.

| Time | Block (AGENDA) | Student does (worksheet task) | Evidence produced |
|---|---|---|---|
| 0:00–0:15 | **Onboarding** — this week's design/audit brief (no `docker compose up`) | Part 1: name, student ID, date, group; disclose any AI assistance used anywhere in the worksheet (tool + what was asked). Open `audit_the_ai/README.md` and read *The scenario* and *Constraints on your fix* before touching code | Completed Part 1 header |
| 0:15–1:45 | **Design/analysis tasks** — AGENDA names Wk10's as *"work through a hybrid-encryption (KEM+DEM) design and where it can go wrong"* | **Part 3, Audit the AI — the headline task.** Step 1: read the code first and confirm the fundamentals a rushed reviewer checks (RSA-OAEP not textbook RSA; 256-bit CSPRNG key; AES-GCM not CBC/ECB; tag actually checked) are all genuinely correct. Step 2: run it — `python broken_hybrid_encrypt.py` — and confirm the round trip succeeds. Step 3: find the one planted bug and quote the exact line(s). Step 4: write a proof script that sends **two** messages in one session and demonstrates a concrete consequence available to someone holding only the two ciphertexts. Step 5: explain the attack in 3–5 sentences. Step 6: write `fixed_hybrid_encrypt.py` — smallest possible change, within the three stated constraints — and state why the RSA/OAEP portion did not need to change | Quoted buggy line(s) · proof script **and its output** · the 3–5 sentence explanation · `fixed_hybrid_encrypt.py`, still round-tripping |
| 1:45–2:25 | **Structured peer critique of another team's design/analysis** | ⬚ — **Worksheet 10 contains no peer-critique task and the 100-pt rubric has no line for it.** Repo-grounded option if you run it anyway (ungraded): pair students and have each check the other's `fixed_hybrid_encrypt.py` against `audit_the_ai/README.md`'s three *Constraints on your fix*, and re-run the partner's proof script against the partner's fixed file. Otherwise fold this time into Part 2 and Part 4, which are the two blocks with no room of their own | ⬚ (nothing the rubric scores) |
| 2:25–2:45 | **AI-resilient tasks** (start in class, finish as homework) | **Part 4A EiPE** — answer the stakeholder's *"Why not just use RSA for everything? Why bother mixing in AES at all?"* in 3–5 sentences with no jargon (explicitly no "OAEP", "GCM", "asymptotic complexity"). **Part 4B Prompt Problem** — write one prompt asking an AI to implement ECIES in Python, run it, critique it bullet-by-bullet against the worksheet's five checks | Part 4A answer · Part 4B: the exact prompt, the AI's **full** response, and a per-bullet critique marking each correct / incorrect / hand-waved with the specific line quoted |
| 2:45–2:55 | **Rotating micro-demo** | 2–3 students walk through their audit: the line they quoted, what their proof script printed, and the one change they made | Live walk-through |
| 2:55–3:00 | **Submit** | Worksheet → PDF → this course's Google Classroom as `Wk10_<StudentID>.pdf`. Whether `fixed_hybrid_encrypt.py` and the proof script also go to GitHub is the open question in §7 — announce your decision here | Submission receipt |

**Where Part 2 goes — decide before the session.** Worksheet 10's Conventional arm is five essay
questions (Q1 bulk-data limits · Q2 the full Bob→Alice flow · Q3 public-key encryption · Q4 key
exchange · Q5 ECIES), *"120–200 words per answer is a reasonable target"*, worth 30 of the 100
points. The AGENDA's CONCEPTUAL lab template has **no row for a conventional essay arm at all**, so
this plan does not manufacture one: either take the 1:45–2:25 block (the only block with no rubric
line attached to it) or set Part 2 as homework and say so out loud. Do **not** resolve this by
editing the worksheet or the AGENDA — both are graded, parity-gated material (see *Escalations*).

**Part 5 (viva spot-check) is instructor-run and live**, worth 10 of the 100 points, and the AGENDA
places viva spot-checks alongside the micro-demo rather than in a slot of their own. Its three
questions are published in the worksheet; students answer with no notes.

**Formative checkpoints**
- **By ~0:45, a student still reading has not started running anything.** Step 2 of the audit brief
  is a 30-second run. Push them: the brief's own prompt is *"what would happen if Bob sent a
  **second** message in the same session?"*
- **The predictable stall is the proof script, not the bug.** Students who reach for the tag will
  trip: `encrypt()` returns *"the ciphertext with the 16-byte GCM authentication tag appended"*, so
  the tag has to come off before any byte-wise comparison means anything.
- **Watch for silent truncation.** The shipped `demo()`'s two messages are **not the same length**
  (`b"Meet me at the usual place, 9pm."` is 32 bytes, `b"Bring the documents we discussed."` is 33),
  so a `zip`-based XOR quietly stops at the shorter one and drops the final byte. A student who
  does not notice will either report a result that looks one character wrong and conclude the
  attack failed, or will "pass" a test that never checked the last byte. Ask what the length
  difference does to their comparison — verified live while writing this plan: the relation holds
  over the first 32 bytes, and the 33rd byte is simply absent from a zipped result.
- **A fix that Alice cannot decrypt is the second-most-common failure.** The third constraint in
  `audit_the_ai/README.md` is explicit — whatever the fix needs beyond the AES key *"must travel
  with the ciphertext to the recipient, in the clear"*. If their own round trip no longer passes,
  that is the tell.
- **A fix that re-wraps the session key per message is out of scope by the brief's own constraint**
  — *"that defeats the point of hybrid encryption and isn't what real protocols do."* Send them
  back to the constraints list rather than marking it later.
- **A student critiquing the RSA key size has not found the bug.** The brief says so up front:
  *"It is not in the RSA/OAEP code."* Redirect before they spend the block there.
- Part 4B: if the AI's ECIES answer is actually good, that is a gradable outcome, not a failed
  task — the fifth check asks whether it hand-waved anything, and every mark must quote a line.
  Require tool name, exact prompt and date; the same prompt will not reproduce the same response.

## 6. Assessment for this week

| Instrument | Evidence | Outcome | Weight |
|---|---|---|---|
| Worksheet 10, Parts 1–5 | Essays, the quoted buggy line(s), proof script + output, `fixed_hybrid_encrypt.py`, prompt artefacts, live viva | K1–K5, P1–P7, A2 | Part of the 30% worksheet component ([course-specification.md](../course-specification.md) §4) |
| Weekly quiz (start of lecture) | Quiz score | K1–K5 | Part of the 10% quiz/participation component — but ⬚ *no Week 10 instrument exists* |
| Micro-demo + viva spot-check (Part 5) | Live walk-through and no-notes defence | P2–P5, A2 | Scored inside the worksheet rubric (10 pts), not separately |
| Per-student planted-error variant | See the note below | A2, CLO6 | ⬚ — **not defined for Week 10** |

**How the analysis is graded.** Worksheet 10 publishes its own 100-point split, and it is weighted
towards the audit rather than the essay arm:

| Criterion | Points |
|---|---|
| Conventional arm — 5 essay questions (Part 2) | 30 |
| Audit-the-AI — bug ID + proof script + explanation + fix (Part 3) | 35 |
| EiPE (Part 4A) | 10 |
| Prompt Problem (Part 4B) | 15 |
| Viva spot-check (Part 5, instructor-run) | 10 |

The worksheet states the marking stance for each arm. Part 2 is *"graded on the accuracy and
completeness of your reasoning, not length"* — these are *"conceptual questions with no single
'correct' sentence to copy"*. Part 3 is graded on the **critique and the proof**, which is why the
worksheet demands four separate artefacts (quoted line, script, output, fix) rather than a verdict.
Part 4B is graded on the critique, not on the AI's answer.

Detailed full / partial / no-credit bands for Part 3, the deduction rules, and the expected-answer
notes for the viva live in `instructor/week10-hybrid-encryption/answer-key.md` — **instructor-only,
git-ignored, and not reproduced in this plan, the slides, or anything a student sees**. Two
practical consequences for marking consistency, both derivable from the published worksheet:

- Part 3 has a **countable floor**: a quoted line, a script, that script's *output*, a 3–5 sentence
  explanation, a `fixed_hybrid_encrypt.py`, and an explicit statement of why the RSA/OAEP portion
  was left alone. Six artefacts, six checkboxes — mark those before the prose, and mark a
  submission that names the bug but ships no working proof differently from one that proves it.
- Part 4B has a **countable floor** too: five checklist bullets, each marked correct / incorrect /
  hand-waved, each with a quoted line. Mark the count first.

Also settle one grading policy in advance, because the worksheet does not: the brief allows more
than one legitimate way to make each message's encryption unique, and a fix that differs from the
reference is not thereby wrong. Judge it against the three published constraints and against
whether the student's own round trip still passes.

**How the per-student planted-error variant is assigned.** ⬚ — **no mechanism is defined for
Week 10 anywhere in this repository, and this plan will not invent one.** The tension is real and
worth stating plainly:

- [course-specification.md](../course-specification.md) §7 says CONCEPTUAL weeks *"use per-student
  planted-error variants instead"* of flags, and `course-plan-19weeks.md` says a CONCEPTUAL week's
  personalised artefact is *"typically a seeded flaw instance or a per-student prompt seed"* —
  naming the two candidate categories, but no assignment rule for either.
- Week 10's material does the opposite: **one** `broken_hybrid_encrypt.py`, byte-identical for the
  whole class. The worksheet states *"**No personalized flag this week** — this is a Conceptual
  week, graded entirely on your written reasoning, proof script, and viva performance"*, and
  SUBMISSION.md's by-week table puts Wk10 under submission mechanism **"No lab/flag"**.
- `instructor/seed_flags.py` mints per-student values for the six **flag-gated** weeks only
  (Wk2, 3, 4, 6, 11, 15); it has nothing for Week 10 and is not a variant generator.
- `instructor/research/planted-error-bank.md` is the study's separate **H2** instrument, with its
  own parallel-form assignment, its own proctored administration and its own pre/post schedule. It
  is **not** a Week 10 worksheet variant and must not be repurposed as one without amending the
  research protocol — the crossover treats `course` as a replication factor, so an ad-hoc change
  here is not a local decision.

What Week 10 *does* produce per student, and what therefore carries the attribution load until a
variant scheme is decided: the **proof script and its printed output** are the student's own run
(no two are identical in structure, and an assistant that never executed the file cannot supply the
output); `fixed_hybrid_encrypt.py` is a written artefact that MOSS/JPlag can compare, per
SUBMISSION.md's anti-cheating controls; Part 4B's prompt is student-authored and its response is
unique to that run; Part 1 carries the identity stamp and the AI-assistance disclosure; and Part 5
is a live, no-notes defence, where *"answers you can't explain in your own words score zero."*

If a per-student seed is to be introduced, **decide and document it before the session** —
retrofitting it after submissions are in makes marks incomparable across the cohort, and both
course arms feed one preregistered study.

## 7. Materials

- Lab: `labs/week10-hybrid-encryption/` — `README.md`, `worksheet.md`,
  `audit_the_ai/README.md`, `audit_the_ai/broken_hybrid_encrypt.py`. No `docker-compose.yml`, no
  `requirements.txt`, no flag (by design).
- Slides: `slides/week10.md` (17 slides, Marp).
- Week 10 quiz: ⬚ (not in the repository — `quizzes/weekly/` holds the two review quizzes only).
- Software on the student's own machine: Python + the `cryptography` package. Nothing else; no
  Docker this week.
- Readings ([readings.md](../../readings.md), W10): ⭐ RFC 8017 — PKCS #1 (RSA-OAEP) ·
  an ECIES / hybrid-encryption explainer · Boneh & Shoup, *A Graduate Course in Applied
  Cryptography*, public-key encryption chapters.
- References cited by the lab and audit READMEs: NIST SP 800-56A Rev. 3 · NIST SP 800-38D (§8.2 for
  the nonce-uniqueness requirement) · OWASP Cryptographic Storage Cheat Sheet · SEC 1 §5.1 (ECIES)
  · Joux, *Authentication Failures in NIST version of GCM* (2006).
- Answer key and reference fix: `instructor/week10-hybrid-encryption/answer-key.md`,
  `reference_fixed.py` (instructor-only, git-ignored).
- Submission channels: [SUBMISSION.md](../../SUBMISSION.md) · Rules of engagement:
  [ETHICS.md](../../ETHICS.md).

> **Open question to settle before class — where does the code go?** The lab README's step 4 says
> *"code (`audit_the_ai/fixed_hybrid_encrypt.py`, your proof script) → GitHub"*. SUBMISSION.md says
> the opposite twice: its file table restricts the GitHub "Code fix" row to **"Wk12 only"**, and its
> weekly-lab section states that the Audit-the-AI rewrite *"goes **in the worksheet itself**, not as
> a code commit."* [course-specification.md](../course-specification.md) §6 likewise calls Week 12
> *"the one week in which students **write the fix themselves**"* — which Week 10 also asks for.
> Announce one channel; do not let half the cohort submit through each. See *Escalations*.

## 8. Risks and contingencies

| Risk | Mitigation |
|---|---|
| `python broken_hybrid_encrypt.py` fails with *command not found* — the audit brief and the worksheet both say `python`, but on a macOS or Linux machine with only Python 3 installed the `python` alias frequently does not exist (confirmed on the machine this plan was verified on: `command -v python` returns nothing, while `python3` works) | Announce the interpreter alias at the 0:00–0:15 onboarding, not at 1:30. `python3 broken_hybrid_encrypt.py` is the same command; inside an activated virtual environment `python` resolves too. Quote the command from the brief but say the alias out loud |
| **The `cryptography` package is not installed on the host.** This week ships no `requirements.txt` and no container, so unlike Weeks 2–6 there is nothing to `docker compose up` that would install it. The README's *"already used in earlier weeks"* is true of the images, not of the students' machines | Tell students in the pre-class instruction to install it and confirm `import cryptography` **before** the session. Fallback in the room: install it into a virtual environment, or run the file inside any earlier week's image, which already carries the dependency (e.g. `labs/week04-aes-modes/requirements.txt` pins `cryptography>=48.0.1`) |
| The lecture teaches nonce reuse (CWE-323, SP 800-38D §8.2, the XOR algebra) **before** the studio asks students to find exactly that bug — the 35-point task is partly pre-answered from the front of the room | This is by design, and the deck's own note draws the line: teach the *shape* of the failure, never open the file on the projector. The graded weight sits on the proof script, its output, the fix and the viva — the parts a student who merely heard the lecture still cannot produce |
| A student searches the bug class online (or asks an assistant) and pastes back a correct-sounding paragraph without running anything | The worksheet requires the script **and its output**, and Part 5 is a live no-notes defence — SUBMISSION.md: *"Answers you can't explain in your own words score zero."* At the micro-demo, ask for the printed output, not the diagnosis |
| The proof script "proves" something trivially true — e.g. compares two values that were never going to differ, or asserts a property of the plaintexts rather than of the intercepted ciphertexts | The brief's step 4 is explicit: *"Prove it, don't just assert it"*, using only what an attacker who sees the two ciphertexts has. Check at ~1:15 while the block is still live, not at marking |
| Byte-level errors sink the proof: the 16-byte tag is left attached, or the two demo messages' one-byte length difference silently truncates a `zip`-based comparison | Both are stated or derivable from the shipped file's own docstring. Prompt with a question about lengths rather than the answer — measured while verifying this plan: 32-byte and 33-byte plaintexts give 48-byte and 49-byte outputs |
| The "smallest fix" quietly breaks the round trip — a per-message nonce that is never sent to Alice | `audit_the_ai/README.md`'s third constraint requires it to travel *"with the ciphertext … in the clear"*. Require the fixed file to still round-trip; that check catches this without any marking judgement |
| A student "fixes" it by wrapping the session key with RSA for every message | Explicitly excluded by the second constraint. Redirect to the constraints list — this is a comprehension failure about hybrid encryption itself, so it is worth two minutes at the whiteboard rather than a deduction |
| Part 4B sends a prompt to a third-party AI service | Covered by ETHICS.md — nothing course-confidential and no real secrets go into the prompt; disclose the tool in Part 1. The critique, not the AI's output, is what is marked |
| No Week 10 quiz instrument exists, so the 10% quiz component silently skips a week | Decide before class: run something, or record that Week 10 has no quiz — "drop lowest 1–2" changes meaning if the denominator changes |
| Four calendar weeks separate Week 6 from Week 10 (review + two midterm sittings in between), so AEAD is cold when the lecture leans on it | The deck's Week 6 recap slide is placed exactly for this; run it as a cold-call, not as a read-through, and expect the padding-oracle contrast to need re-explaining |
| Copy-paste between students — there is no flag this week to make evidence attributable | Attribution rests on the artefacts named in §6: the student's own script output, the code-similarity check on `fixed_hybrid_encrypt.py`, the unique Part 4B transcript, and the viva. Spot-check pairs whose scripts match structurally |
| A student finishes the audit early | Extension that stays inside the material: have them answer the Part 5 viva questions in writing — particularly *"If a program only ever sends exactly one message per `HybridEncryptor` session and then discards it, is the code in `broken_hybrid_encrypt.py` secure? Is it still bad practice?"* — or start the Part 4B ECIES critique, which is the week's other 15 points |

## 9. Post-teaching reflection

*Complete after the session — this also feeds the course's engagement data.*

- Attendance / completion: ⬚
- Where Part 2 (the five essays) actually ran — in the 1:45–2:25 block, or as homework: ⬚
- Time actually taken per block (vs. plan), and whether the 1:55–2:00 briefing over-ran: ⬚
- How many students found the bug unaided, and how many needed the "second message" prompt: ⬚
- How many produced a proof script that actually demonstrated the consequence (vs. asserting it): ⬚
- Which byte-level trap cost the most time — the attached tag, or the length mismatch: ⬚
- Quality of the Part 4B critiques — did students quote lines, or summarise impressions: ⬚
- Misconception that showed up in the EiPE answers: ⬚
- Whether any submitted fix broke the round trip, and how that was marked: ⬚
- Decision recorded on the per-student variant question (§6): ⬚
- Decision recorded on the submission channel for `fixed_hybrid_encrypt.py` (§7): ⬚
- Anything to change before this week runs again: ⬚

---

### Escalations — defects in lab/course content, recorded here rather than fixed

These are content issues found while writing this plan. They are **not** corrected in `labs/`,
`AGENDA.md`, `SUBMISSION.md` or the course specification, because that material is graded,
parity-gated against the curriculum monorepo, and mirrored by an instructor answer key.

1. `labs/week10-hybrid-encryption/README.md` step 2 says the slides are *"(not yet written — see
   `course-plan-19weeks.md`)"*, but `slides/week10.md` exists and is a complete 17-slide Marp deck
   with speaker notes. Stale note.
2. The same README tells students to *"skim last week's recap (Key Exchanges)"*. Key Exchanges is
   **Week 5**; the previous teaching week is **Week 6** (AEAD), with Weeks 7–9 (review, midterm
   written, midterm practical) in between — and `slides/week10.md` recaps Week 6, not Week 5. The
   student instruction and the deck point at different weeks.
3. The README's step 4 sends `audit_the_ai/fixed_hybrid_encrypt.py` and the proof script to
   **GitHub**, while SUBMISSION.md restricts the GitHub "Code fix" row to **"Wk12 only"** and states
   that the Audit-the-AI rewrite *"goes in the worksheet itself, not as a code commit."* Students
   following one document submit to a channel the other does not grade.
4. Relatedly, `course-specification.md` §6 states that Week 12 is *"the one week in which students
   **write the fix themselves** … rather than confirm a supplied one"*. Week 10 also requires
   students to write a fix (`fixed_hybrid_encrypt.py`), and no `solution`/`fixed` file ships in the
   student-visible lab folder for them to confirm against. The specification's claim is inaccurate
   for this week.
5. AGENDA.md's CONCEPTUAL-week lab template places *"Audit-the-AI + EiPE + Prompt Problem"*
   together in a single **20-minute** row (2:25–2:45). For Week 10 the Audit-the-AI *is* the
   headline task — 35 of 100 points, requiring a code read, a run, a written proof script with its
   output, an explanation and a corrected file — and the AGENDA's own description of Wk10's
   90-minute design/analysis block (*"work through a hybrid-encryption (KEM+DEM) design and where it
   can go wrong"*) describes that same task. The two rows cannot both be followed literally, and
   Worksheet 10 publishes no minute budgets that would settle it.
6. AGENDA.md's CONCEPTUAL template includes a 40-minute *"structured peer critique of another
   team's design/analysis"*; Worksheet 10 has no peer-critique task and its 100-point rubric has no
   line for one. (Identical to the Week 1 gap.)
7. The AGENDA's CONCEPTUAL lab template has **no row for the Conventional arm**, yet Worksheet 10's
   Part 2 essays are 30 of the 100 points and the dual-arm requirement in `course-plan-19weeks.md`
   makes that arm non-negotiable. As written, the template fills 180 minutes without ever placing
   the essays.
8. AGENDA.md states the Evidence & Integrity artefact for CONCEPTUAL weeks is *"a design
   artifact"*; Worksheet 10's Evidence & Integrity section collects an identity stamp plus a 1–2
   sentence restatement. No design artefact is collected and the rubric has no line for one.
9. `course-specification.md` §7 promises per-student planted-error variants for CONCEPTUAL weeks;
   Worksheet 10 and SUBMISSION.md both state Week 10 has no personalised artefact, and no
   assignment mechanism is defined anywhere in the repository. See §6. (Course-level gap, also
   raised for Week 1.)
10. No Week 10 weekly-quiz instrument exists (`quizzes/weekly/` holds only the Week 7 and Week 17
    review quizzes), although the specification, AGENDA.md and the lab README all place a ~10-min
    quiz at the start of every teaching week.
11. `audit_the_ai/README.md` step 2 and Worksheet 10 both give the run command as
    `python broken_hybrid_encrypt.py`. On a machine with only Python 3 installed and no `python`
    alias — the default on current macOS and many Linux distributions — that command fails. A
    parenthetical (`python3` on most systems) would remove a predictable first-15-minutes stall.
12. The lab ships no `requirements.txt` and no container, but the code imports `cryptography`. The
    README's *"standard library + `cryptography` (already used in earlier weeks)"* is true of the
    earlier weeks' **images**, not of a student's host machine, where the package may never have
    been installed.
13. **RESOLVED.** `slides/week10.md` used to state *"RSA-4096-OAEP: roughly a **470-byte
    plaintext ceiling**"*, which was wrong for the padding this course actually uses.
    RSA-OAEP's maximum plaintext is `k − 2·hLen − 2` bytes (`k` = modulus size in bytes,
    `hLen` = hash output size); the lab's own `audit_the_ai/broken_hybrid_encrypt.py` builds
    OAEP with `hashes.SHA256()` for both the OAEP hash and the MGF1 hash (`hLen = 32`), and
    generates a 4096-bit key (`k = 512`), giving `512 − 64 − 2 = 446` bytes — confirmed
    empirically (`cryptography`'s RSA-OAEP encrypt succeeds at 446 bytes and raises at 447).
    470 bytes is only correct for OAEP with SHA-1 (`512 − 40 − 2 = 470`), which nothing in
    this course's code or worksheet uses. `slides/week10.md` line 41 now reads *"roughly a
    446-byte plaintext ceiling"* — the §1 K1 and §4 lecture-table notes above have been
    updated to match, and the number can be taught as verified.
