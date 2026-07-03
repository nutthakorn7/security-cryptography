# Weekly Agenda & Time Plan (DRAFT for review)

**Standard contact time:** 5 hrs/week = **120 min lecture + 180 min lab** (per syllabus: 2 lecture + 3 lab hrs).
**Quizzes:** a short **weekly quiz (~10 min) at the start of every teaching week** (retrieval
practice, low-stakes, drop lowest 1–2). Two **cumulative review quizzes** (25 pts) run in the
review weeks (W7 pre-midterm, W17 pre-final).

This is the agenda for **Security & Cryptography**, a companion course to `software-security`
with its own Google Classroom instance and its own GitHub repo/CTFd deployment (see this
repo's README.md, "Relationship to `software-security`"). Nothing here is shared live with the
sibling course — no joint roster, no joint scoreboard.

---

## Week types in this course

Not every teaching week runs the same lab shape. Per `course-plan-19weeks.md`, each teaching
week is one of:

- **LAB** (Wk2, 3, 4, 6, 15) — a Docker target with a real exploit and a genuine captured
  flag (`FLAG_...`), same pattern as `software-security`.
- **HYBRID** (Wk5, 11, 12, 13, 14) — a smaller, genuinely demonstrable exploit/demo alongside
  content that stays conceptual. **For most of these weeks the thing students "submit" is a
  captured evidence log line, not a CTF flag string — except Wk11, which is a hybrid week that
  still uses a real flag** — see the callout below for exactly which is which.
- **CONCEPTUAL** (Wk1, 10) — no exploitable Docker target; the week is protocol-design/math
  analysis. No lab task, no flag/evidence line — graded via Audit-the-AI, EiPE, and Prompt
  Problem only.

> ### ⚠️ HYBRID weeks: check which artifact type before grading — it is NOT uniform
> "HYBRID" describes the lecture/lab content split (small demonstrable exploit + conceptual
> remainder), not a single submission format. Verified against each week's own
> `worksheet.md`/`README.md` in this repo:
>
> - **Wk5 (Key Exchanges) — evidence log line, not a flag.** There is no `FLAG_{...}`. The
>   worksheet calls it a "required evidence line": the MITM's recovered/decrypted
>   `SECRET_MESSAGE`, captured from the log once the unauthenticated DH exchange is
>   intercepted, plus the abort evidence from the authenticated (fixed) run.
> - **Wk11 (Signatures/ZKP) — a real flag, same pattern as LAB weeks.** Despite being
>   classified HYBRID, `week11-signatures-zkp` ships a genuine per-student `FLAG_SIG`
>   (`FLAG{ecdsa_malleable_double_spend}` by default, overridable via `seed_flags.py`) returned
>   by the vulnerable bank on the second (malleated) withdrawal. Do **not** describe Wk11 as a
>   log-line week — students submit the captured `FLAG_SIG` exactly as in a LAB week, plus the
>   `(r, s)`/`(r, n−s)` pair that produced it.
> - **Wk12 (Secure Transport) — evidence log line.** `MITM INTERCEPTED: the vault code is 7731`
>   (cert-validation-bypass run, `VERIFY` unset) vs. `CERT VERIFICATION FAILED — ABORTING`
>   (fixed run, `VERIFY=1`).
> - **Wk13 (E2E Encryption) — evidence log line.** `SERVER SAW: meet at pier 39 at midnight`
>   (server-side plaintext log, `E2E` unset) vs. the server logging only ciphertext (`E2E=1`).
> - **Wk14 (Authentication) — evidence log line.** `SERVER SAW PASSWORD: correct-horse-battery`
>   (plaintext password over the wire) vs. `nonce=...proof=...` only (challenge-response,
>   `PAKE=1`).
>
> For the four genuine log-line weeks (5, 12, 13, 14), students paste **both** the
> vulnerable-run log line and the fixed-run log line into the worksheet as their personalized,
> attributable evidence artifact — this is what viva spot-checks probe ("show me your
> terminal, reproduce that line"). For Wk11, the attributable artifact is the captured
> `FLAG_SIG` string, same as a LAB week. Grading rubrics, the worksheet template, and
> instructor answer keys must reflect this per-week distinction, or Wk11 students will waste
> lab time hunting for a log line that isn't the graded artifact (it's a flag), while Wk5/12/13/14
> students waste time hunting for a flag string that doesn't exist.
>
> **LAB weeks (2, 3, 4, 6, 15) are unaffected** — those five keep a real `FLAG_...` string
> exactly like `software-security`'s pattern.

---

## Standard teaching-week template — LAB weeks (2, 3, 4, 6, 15)

### Lecture — 120 min
| Time | Block |
|------|-------|
| 0:00–0:10 | **Weekly quiz** (retrieval) + recap + today's agenda |
| 0:10–0:55 | Core concepts (the primitive, how it's meant to be used) |
| 0:55–1:05 | Break |
| 1:05–1:35 | Misuse deep-dive + real-world cases (where this primitive broke in practice) |
| 1:35–1:55 | Correct construction / defenses |
| 1:55–2:00 | Signature-game briefing → to lab |

### Lab — 180 min
| Time | Block |
|------|-------|
| 0:00–0:15 | Onboarding: stand up target (`docker compose up`), confirm it runs |
| 0:15–1:45 | Exploitation tasks (the signature game) — ~4–5 tasks, ends with capturing `FLAG_...` |
| 1:45–2:25 | Defend / fix task (apply the secure version, prove exploit fails) |
| 2:25–2:45 | **AI-resilient tasks:** Audit-the-AI + EiPE + Prompt Problem (start in class, finish as homework) |
| 2:45–2:55 | **Rotating micro-demo:** 2–3 students give a 2–3 min "show your exploit/fix" (different students each week → everyone presents ~1–2× per term) |
| 2:55–3:00 | Submit worksheet (PDF → this course's Classroom) + push fix (this course's GitHub) + wrap-up |

## Standard teaching-week template — HYBRID weeks (5, 11, 12, 13, 14)

Same lecture shape and lab time budget as LAB weeks, with two adjustments: the lab's
exploitation block is smaller (one demonstrable exploit/demo, not 4–5 tasks) because the rest
of the week's content stays conceptual; and the captured artifact is, **for Wk5/12/13/14, the
evidence log line** described above — **Wk11 is the exception and captures a real
`FLAG_SIG`** (see the callout above), so swap "log line" for "flag" in the lab blocks below
when running Wk11.

### Lecture — 120 min
| Time | Block |
|------|-------|
| 0:00–0:10 | **Weekly quiz** (retrieval) + recap + today's agenda |
| 0:10–0:55 | Core concepts (the conceptual material for the week) |
| 0:55–1:05 | Break |
| 1:05–1:35 | The demonstrable half: the specific failure this hybrid week exploits |
| 1:35–1:55 | Correct construction / defenses + what stays out of scope for the demo (named explicitly, e.g. "this is not a full PAKE") |
| 1:55–2:00 | Demo/evidence-capture briefing → to lab |

### Lab — 180 min
| Time | Block |
|------|-------|
| 0:00–0:15 | Onboarding: stand up target (`docker compose up`), confirm it runs |
| 0:15–1:20 | Demo/exploit task — run the vulnerable configuration, capture the "before" evidence log line |
| 1:20–1:45 | Fix task — flip the flag/env var to the secure configuration, capture the "after" evidence log line, confirm the attack no longer works |
| 1:45–2:25 | Conceptual extension: EiPE/worksheet questions on the part of the topic that has no demo (e.g. Schnorr/ZKP theory in Wk11, FIDO2/SSO/TOTP comparison in Wk14) |
| 2:25–2:45 | **AI-resilient tasks:** Audit-the-AI + EiPE + Prompt Problem (start in class, finish as homework) |
| 2:45–2:55 | **Rotating micro-demo:** 2–3 students give a 2–3 min "show your before/after log lines" |
| 2:55–3:00 | Submit worksheet (PDF → this course's Classroom) + push fix (this course's GitHub) + wrap-up |

## CONCEPTUAL-week template (Weeks 1, 10)

No Docker target, no flag, no evidence log line. The lab block becomes design/audit work
instead of exploitation.

### Lecture — 120 min
| Time | Block |
|------|-------|
| 0:00–0:10 | **Weekly quiz** (retrieval) + recap + today's agenda |
| 0:10–0:55 | Core concepts |
| 0:55–1:05 | Break |
| 1:05–1:35 | Worked analysis (threat-model or protocol walkthrough, on paper/whiteboard, not Docker) |
| 1:35–1:55 | Design trade-offs / where real systems get this wrong |
| 1:55–2:00 | Briefing → to lab |

### Lab — 180 min
| Time | Block |
|------|-------|
| 0:00–0:15 | Onboarding: this week's design/audit brief (no `docker compose up`) |
| 0:15–1:45 | Design/analysis tasks — e.g. Wk1: threat-model a small crypto system end-to-end; Wk10: work through a hybrid-encryption (KEM+DEM) design and where it can go wrong |
| 1:45–2:25 | Structured peer critique of another team's design/analysis |
| 2:25–2:45 | **AI-resilient tasks:** Audit-the-AI + EiPE + Prompt Problem (start in class, finish as homework) |
| 2:45–2:55 | **Rotating micro-demo:** 2–3 students walk through their design/critique |
| 2:55–3:00 | Submit worksheet (PDF → this course's Classroom) + wrap-up (no fix to push — no code this week) |

> **Week 1 exception:** Week 1's lab also carries **term-wide environment setup** (Docker
> Desktop install/verify, repo clone, first `docker compose up` on a throwaway container) since
> it is the first lab session of the term and later LAB/HYBRID weeks assume Docker already
> works. Budget ~30–40 min of the 180-min block for this before the threat-modeling task.

> **No formal weekly presentation** (impossible for N≈80–120 in the time budget). Instead,
> "explain it live" is delivered by the **rotating micro-demo** above + random **viva spot-checks**
> (2–3 students reproduce/explain their own work — for Wk5/12/13/14 this means reproducing the
> before/after log line; for Wk11, reproducing the captured flag) — which also double as
> anti-AI controls. Full presentations are reserved for the **capstone** (W16 WIP + W19 demo).
>
> **Every teaching week's worksheet** has four graded parts beyond the lab tasks:
> **Evidence & Integrity** (identity-stamped proof — a real flag for LAB weeks and Wk11, a
> captured log line for the other HYBRID weeks (5, 12, 13, 14), a design artifact for
> CONCEPTUAL weeks), **Audit the AI** (critique an AI answer), **Explain-in-Plain-English** +
> **Prompt Problem**. The live **CTFd / Houses scoreboard** for this course (once its own
> deployment is live — see README.md status note) is shown at the start/end of class.
>
> The **weekly quiz** is the first ~10 min of the lecture block (every teaching week) — no
> separate session needed. The two **cumulative review quizzes** run in the review weeks (7, 17).

---

## Per-week time table

| Wk | Type | Lecture | Lab | Quiz | Exam | Total |
|----|------|:---:|:---:|:---:|:---:|:---:|
| 1 | Conceptual — Intro / Threat-Modeling a Crypto System | 120 | 180* | 10† | — | 300 |
| 2 | Lab — Hashing (unsalted-hash password cracking) | 120 | 180 | 10† | — | 300 |
| 3 | Lab — MACs (hash-only cookie forgery / length-extension) | 120 | 180 | 10† | — | 300 |
| 4 | Lab — AES Modes (CBC bit-flipping / malleability) | 120 | 180 | 10† | — | 300 |
| 5 | Hybrid — Key Exchanges (unauthenticated DH MITM) | 120 | 180 | 10† | — | 300 |
| 6 | Lab — AEAD (CBC padding-oracle attack) | 120 | 180 | 10† | — | 300 |
| 7 | 🔁 Review (pre-midterm) | — | — | 25‡ | — | 300 |
| 8 | 📝 Midterm — Written | — | — | — | 120 | 120 |
| 9 | 📝 Midterm — CTF (covers Wk1–6) | — | — | — | 150 | 150 |
| 10 | Conceptual — Hybrid (Asymmetric+Symmetric) Encryption | 120 | 180 | 10† | — | 300 |
| 11 | Hybrid — Signatures / Zero-Knowledge Proofs | 120 | 180 | 10† | — | 300 |
| 12 | Hybrid — Secure Transport (cert-validation-bypass MITM) | 120 | 180 | 10† | — | 300 |
| 13 | Hybrid — End-to-End Encryption | 120 | 180 | 10† | — | 300 |
| 14 | Hybrid — Authentication | 120 | 180 | 10† | — | 300 |
| 15 | Lab — Post-Quantum Cryptography (Lamport OTS key reuse) | 120 | 180 | 10† | — | 300 |
| 16 | Capstone Studio (CryptoVault project) | — | 300 | — | — | 300 |
| 17 | 🔁 Review (pre-final) | — | — | 25‡ | — | 300 |
| 18 | 📝 Final — Written | — | — | — | 150 | 150 |
| 19 | 📝 Final — CTF + Demos (cumulative, emphasis Wk10–16) | — | — | — | 240 | 240 |

*W1 lab includes term-wide environment setup (~30–40 min) — onboarding block is longer; see the
CONCEPTUAL-week template note above.
†Weekly quiz (~10 min) is the first part of the 120-min lecture block — not extra time.
‡Cumulative review quiz (25 pts) used to prep for the exam.

---

## Special-week agendas

### Week 7 & 17 — Review (300 min)
| Time | Block |
|------|-------|
| 0:00–0:30 | **Cumulative review quiz** (quiz1 / quiz2 — 25 pts) |
| 0:30–1:45 | Crypto Jeopardy team review |
| 1:45–2:00 | Break |
| 2:00–4:30 | Mock CTF (exact format of the upcoming exam — LAB-week + Wk11 flags, plus Wk5/12/13/14 evidence-log-line tasks, mixed) |
| 4:30–5:00 | Debrief: common mistakes + exam logistics |

### Week 8 / 18 — Written exam
- Single block: **120 min (midterm) / 150 min (final)**. No lab.

### Week 9 — Midterm CTF practical (150 min)
- 0:00–0:10 rules + target check · 0:10–2:30 solve challenges · submit flags (Wk2–4, 6 style) and
  evidence log lines (Wk5 style, since Wk5 is the only hybrid week before the midterm).

### Week 16 — Capstone Studio (300 min)
CryptoVault project (see `project/README.md` for the full brief/rubric).

| Time | Block |
|------|-------|
| 0:00–2:00 | Team WIP demos (design decision → failure mode → fix) + peer review |
| 2:00–2:15 | Break |
| 2:15–4:45 | Practice CTF tournament (previews Week 19) |
| 4:45–5:00 | Feedback + finalize checklist before the final |

### Week 19 — Final CTF + project demos (240 min)
| Time | Block |
|------|-------|
| 0:00–2:30 | Capstone CTF tournament (whole term: LAB + Wk11 flags, plus Wk5/12/13/14 evidence lines, cumulative) |
| 2:30–4:00 | Graded final CryptoVault project demos (10-min demo + 5-min Q&A per team) |

---

## Open items carried from `course-plan-19weeks.md`

This course's own CTFd deployment, `instructor/seed_flags.py`, and Classroom roster are not yet
live (see README.md status note) — the timings above are the *intended* live-course agenda, not
yet exercised end-to-end with real students. Confirm actual worksheet task counts fill the
180-min lab block per week (this course's worksheets are newly built, not ported verbatim from
`software-security`, so its "drift to resolve" durations note does not automatically apply here
and has not been re-checked against this course's own worksheets yet).
