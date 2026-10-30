# Cryptography and Network Security — Course Syllabus

**Course code:** 02005104 · **Level:** Year 4 · **Credits:** 1
**Semester:** 2, Academic Year 2026 (2569) · **Programme:** Computer · **Type:** Compulsory
**Instructor:** Nutthakorn Chalaemwongwan
**Class format:** Lecture, with hands-on laboratory or practical analysis as the main in-class activity.
**Contact time:** 100 minutes per week, 20 weeks (2,000 scheduled minutes).
**Prerequisites:** Programming and basic discrete mathematics/number theory.

## Course description

Students select, misuse-test and correctly compose cryptographic mechanisms in controlled local
environments: hashes and password KDFs, MACs, AES modes, authenticated key exchange, AEAD,
hybrid encryption, signatures, secure transport, end-to-end messaging, authentication and
post-quantum migration. Practical evidence and explanations matter together. Conceptual Weeks 1
and 10 use diagrams, calculations and counterexamples rather than a forced Docker/flag target.

## Learning outcomes

1. Select and justify a primitive for confidentiality, integrity, authenticity and freshness.
2. Analyse cryptographic misuse and demonstrate a bounded attack with reproducible evidence.
3. Use vetted libraries and verify that a correct construction rejects the original attack.
4. Explain protocol trust, key authentication, compromise limits and post-quantum migration.
5. Evaluate technical claims and communicate reasoning, including checking AI-generated claims.
6. Work ethically on authorized targets and disclose sources, tools and individual contributions.

## Teaching and workload

An ordinary teaching week uses **10 minutes retrieval quiz/review + 10 minutes briefing +
60 minutes practical work + 15 minutes feedback/reasoning + 5 minutes submission**. Weeks 11
and 15 reserve 70 minutes for their stateful practical and 10 minutes for evidence/feedback,
alongside the same 10-minute quiz and 10-minute briefing. Installation, image pulls and long
readings happen before class; complete written answers and extension tasks after class. All
original questions remain available; only the named core sequence is planned inside the slot.
Week 1 orientation is an ungraded diagnostic; its retrieval bank is used in Week 2.
Week 12 includes a student-written `build_client_context()` and tests in both worksheet forms.

## Assessment

| Component | Weight | Mode and timing |
|---|---:|---|
| 12 worksheets: Weeks 1–6 and 10–15 | 30% | Individual; each worksheet contributes 2.5 course points |
| Midterm written, Week 8 | 8% | Individual; 90 minutes writing + 10 minutes administration |
| Midterm practical, Week 9 | 12% | Individual; 80 minutes tasks + 20 minutes administration |
| Final written, Week 18 | 10% | Individual; 90 minutes writing + 10 minutes administration |
| Final practical, Week 19 | 15% | Team; 80 minutes tasks + 20 minutes administration |
| CryptoVault project | 15% | Teams of 3 normally, 2 where needed; see project brief |
| Quizzes and participation | 10% | Retrieval quizzes and class participation |
| **Total** | **100%** | |

### Two worksheet forms: shared 60 + assigned-form 40

Every student does the same core practical work. Each worksheet is scored out of 100:

| Scored part | Conventional | AIR-Sec |
|---|---:|---:|
| Core work / observation | 20 | 20 |
| Control verification / limitations | 20 | 20 |
| Reproducible evidence and reasoning | 20 | 20 |
| Conventional technical written questions | 40 | — |
| Audit-the-AI | — | 20 |
| Explain-in-Plain-English | — | 10 |
| Prompt Problem | — | 10 |
| **Total** | **100** | **100** |

For Weeks 1 and 10, the common 60 is practical analysis, diagrams, calculations or proofs, with
control/counterexample reasoning. No Docker flag is required. In Week 12 the code and its tests
are part of common 60. Students complete the form assigned for that week; the other form is not
an additional 40 points. Score to course points as `worksheet score / 100 × 2.5`.

Feedback, reproduction checks and short oral explanations sample understanding within the
existing work. They add no separate viva points and create no automatic AIR-only grade gate.
Name/ID and ordinary academic integrity requirements apply equally. A personal flag is required
only if the instructor has actually configured and issued that instance; a shared default flag
alone proves neither identity nor understanding.

### Ability categories

| Ability category | Lab | Midterm | Final | Project | Quiz/participation | Total |
|---|---:|---:|---:|---:|---:|---:|
| Basic | 0 | 10 | 5 | 0 | 5 | 20 |
| Technical | 25 | 10 | 20 | 10 | 5 | 70 |
| Interdisciplinary | 5 | 0 | 0 | 5 | 0 | 10 |
| **Total** | **30** | **20** | **25** | **15** | **10** | **100** |

Written/practical subtotals and ability categories are two views of the same marks; neither is
added twice. Item-level exam allocations are held with the instructor blueprint.

The existing late-work rule remains −10% of the item's score per day for up to three days,
unless an extension is approved. In-class quizzes have no late window; the existing lowest
1–2 quiz drop policy applies. Documented emergencies are handled individually.

## Weekly outline

| Week | Topic / class purpose |
|---:|---|
| 1 | Security mindset, threat modelling and primitive selection |
| 2 | Hash functions and password storage |
| 3 | MACs and length extension |
| 4 | AES modes and CBC malleability |
| 5 | Authenticated key exchange and DH MITM |
| 6 | AEAD and the CBC padding oracle |
| 7 | Review and bounded mock practical |
| 8 | Midterm written |
| 9 | Midterm individual practical |
| 10 | Asymmetric and hybrid encryption |
| 11 | Signatures/ZKP; ECDSA signature malleability |
| 12 | TLS/Noise; implement and test the client context |
| 13 | End-to-end encryption and key trust |
| 14 | Authentication; toy challenge-response and real PAKE limits |
| 15 | PQC; Lamport one-time key reuse; optional HNDL extension |
| 16 | CryptoVault studio, feedback and project clarification |
| 17 | Review and bounded final rehearsal |
| 18 | Final written |
| 19 | Final team practical; no project Q&A in the timed CTF |
| 20 | Feedback, returned work, project clarification and closure |

Teams submit a **video no longer than five minutes before Week 19**, alongside the final build
and report. Project clarification is scheduled in Weeks 16/20 and stays within the existing
project rubric. Cryptocurrency/UTXO/BFT legacy bank items are not scored in this syllabus.

See [AGENDA.md](AGENDA.md), [course specification](docs/course-specification.md),
[project brief](project/README.md) and [submission rules](SUBMISSION.md).

## References

- Boneh & Shoup, *A Graduate Course in Applied Cryptography*.
- OWASP Cryptographic Storage and Transport Layer Protection Cheat Sheets.
- NIST SP 800-38D; SP 800-56A; FIPS 203, 204 and 205.
- [RFC 9807: OPAQUE](https://www.rfc-editor.org/rfc/rfc9807.html), particularly § 10.11.
