# Weekly Agenda — Cryptography and Network Security

**02005104 · Year 4 · 1 credit · Semester 2 AY2026 · Lecture · 100 minutes × 20 weeks.**
The class emphasizes practical work. Preparation and full written answers extend outside class;
the tables below specify the work that must fit inside each contact slot. This is a planned
budget, not a claim that students have completed a timed pilot.

## Ordinary teaching weeks

| Minutes | Activity |
|---|---|
| 0–10 | Retrieval quiz/review of previously taught material |
| 10–20 | Short concept and safety briefing |
| 20–80 | Core laboratory or practical analysis |
| 80–95 | Control comparison, reasoning and feedback |
| 95–100 | Save evidence and submit the in-class checkpoint |

Weeks **11 and 15** instead use 20–90 for the stateful core and 90–100 for evidence, feedback
and checkpoint submission. Work within the slot includes before/after evidence; installation,
image downloads, lengthy background and full-form written answers do not consume the core.
Week 1 uses an ungraded orientation diagnostic/review in its first ten minutes. Weekly banks test that week's
content at the next teaching session: W1 bank opens W2, W6 opens W7, W15 opens W16.

## Weekly core and artifacts

| Wk | In-class core | Artifact | Total min |
|---:|---|---|---:|
| 1 | Environment check; threat model; choose primitives; test a changed attacker assumption; Snake Oil Bingo (AIR-Sec analyses its claims) | Diagram, assumptions and corrected design | 100 |
| 2 | Weak-hash dictionary recovery; persistent-session login; KDF comparison | Recovery/session outputs and KDF limits | 100 |
| 3 | Supplied state-resumption helper; MAC extension; HMAC rejection | Authenticated bytes, glue-length reasoning and before/after result | 100 |
| 4 | Derive CBC same-length XOR delta; test authenticated control; form CryptoVault teams and review the design plan | Byte work, tamper accept/reject outputs and submitted design plan | 100 |
| 5 | Unauthenticated DH MITM versus authenticated exchange | Interception and abort traces | 100 |
| 6 | CBC oracle; derive one byte; recover with helper; compare GCM | Oracle evidence, byte derivation and control rejection | 100 |
| 7 | Review quiz; selected Jeopardy clues; two bounded mock checkpoints; CryptoVault KDF/AEAD milestone | Review answers, repair notes and milestone demonstration | 100 |
| 8 | Written midterm: 90 writing + 10 administration | Individual script | 100 |
| 9 | Individual practical: 80 tasks + 20 administration | Method, result and control evidence | 100 |
| 10 | Hybrid-encryption diagram, nonce counterexample and corrected design | Diagram, calculation/proof and limitations | 100 |
| 11 | Fresh signature 10; twin 15; vulnerable submission 15; fixed controls 15; explanation 15; sharing-flow draft feedback | (r,s)/(r,n−s), transaction IDs and control | 100 |
| 12 | Disabled TLS validation; all students write/test client context | Code, trusted-peer success and MITM rejection | 100 |
| 13 | Server plaintext versus client-encrypted relay | Server output, recipient success and key-trust limits | 100 |
| 14 | Password exposure versus toy challenge/proof; CryptoVault transport/self-audit review | Freshness and exposure comparison; PAKE limitations | 100 |
| 15 | Fresh Lamport key; complementary signatures; forge; single-use control | Signature derivation and control rejection | 100 |
| 16 | CryptoVault studio; every team demonstrates its sharing flow at peer review; scheduled clarification | WIP evidence, feedback and action list | 100 |
| 17 | Review quiz; selected clues; bounded final rehearsal | Review and repair notes | 100 |
| 18 | Written final: 90 writing + 10 administration | Individual script | 100 |
| 19 | Team practical: 80 tasks + 20 administration | Team solution/evidence; no project Q&A | 100 |
| 20 | Returned work, feedback, project clarification and closure | Reflection/action list; no new grade category | 100 |

LAB weeks 2/3/4/6/15 and HYBRID Week 11 may produce real flags. Weeks 5/12/13/14 produce
before/after traces, not invented flags. Weeks 1/10 are shared practical analysis; they do not
need a Docker flag. A personal flag/automatic roster check must never be assumed to be live.

## Shared practical and worksheet forms

Every teaching worksheet uses **common 60 + assigned-form 40**. Common 60 = core work 20 +
control/limitations 20 + reproducible evidence/reasoning 20. Conventional uses technical written
questions 40; AIR-Sec uses Audit-the-AI 20 + Explain-in-Plain-English 10 + Prompt Problem 10.
The 12 worksheets contribute 2.5 course points each, totaling 30. No extra viva points or
automatic AIR-only viva gate apply. Short explanations are feedback/authenticity checks within
the assessed work. See [syllabus](syllabus.md) for the full 100% and ability matrices.

## Special weeks

### Weeks 7 and 17 — review

| Minutes | Activity |
|---|---|
| 0–20 | Cumulative review quiz (existing 25-point quiz instrument) |
| 20–35 | Selected Jeopardy clues targeting misconceptions |
| 35–80 | Two selected mock checkpoints, with working targets already prepared |
| 80–95 | Explain errors and verify a correction; W7 teams demonstrate the CryptoVault KDF/AEAD milestone |
| 95–100 | Save repair plan and read exam logistics |

Full boards and mock banks remain available for further practice; they are not all compulsory
in a 100-minute class. The rehearsal samples the upcoming exam rather than promising every
original challenge fits in the slot.

### Weeks 8 and 18 — written exams

0–5 administration; 5–95 **90 minutes writing**; 95–100 collection. Midterm has 10 bounded
short/applied/design items, final has **20 taught-topic MCQs ×5 points** per form. Each paper is
raw 100; scale to midterm 8 or final 10 course points. No additional weekly quiz or lab.

### Weeks 9 and 19 — practical exams

0–10 rules, identity and target checks; 10–90 **80 minutes tasks**; 90–100 upload/collection.
The midterm is individual, with four bounded checkpoints (15/20/20/25 task minutes). The final
uses teams of **3 normally, 2 where uneven**, with three stations (25/25/30 task minutes).
Raw 100 scales to midterm 12 or final 15 course points. Targets, variants, hints and answer keys
remain instructor-held. Provide a tested equivalent artifact if infrastructure fails; do not
silently reduce a student's task time or introduce an unannounced new grade component.

### Week 16 — CryptoVault studio

| Minutes | Activity |
|---|---|
| 0–10 | Retrieval quiz and brief |
| 10–20 | Self-audit checklist and division of work |
| 20–75 | Teams implement/test; instructor schedules focused clarification during the work; practice challenges available |
| 75–95 | Peer review: each team demonstrates its sharing flow to a partner team |
| 95–100 | Save remaining fixes and final-deliverable plan |

Every team demonstrates its existing sharing flow to its peer-review partner and the instructor,
not as a full presentation to the whole class, so no student headcount is assumed. Existing
practice practical challenges check understanding before the final assessment and add no marks. Team videos
are **≤5 minutes**, submitted before Week 19; final report/build/video are graded using the
project's existing 15%. Remaining clarification happens in Week 20. It never reduces the
Week 19 timed practical.

### Week 20 — feedback and closure

0–15 return work and explain criteria; 15–45 review mechanisms, common errors and control
verification; 45–75 focused project clarification/feedback; 75–95 reflection and remaining
questions; 95–100 closure. Use [Week 20 guide](labs/week20-feedback/README.md). No new worksheet/exam
category or automatic grade increase is created.

## Preparation and instructor verification

Pre-pull images and dependencies; check ports and browser/Python tools before each lab.
Weeks 11/15 require fresh process state before each independent attempt; a fresh server may
also mean fresh keys. Acquire signatures after the active server starts. Set aside the full
written question bank and AI critique for completion after the core rather than dropping text.
HNDL is optional enrichment, not an added scored prerequisite.

Validate each exam variant and its key before use, then record real completion times after
teaching. The older expanded plans and unused questions are retained privately as historical
reference; they do not define the current timetable. See individual [lesson plans](docs/lesson-plans/).
