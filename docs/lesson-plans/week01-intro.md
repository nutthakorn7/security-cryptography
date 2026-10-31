# Lesson Plan — Week 1: Security mindset and threat modelling

**02005104 · Cryptography and Network Security · Year 4 · Semester 2 AY2026 · Lecture**
**Contact time: 100 minutes.** Kind: CONCEPTUAL.
Lab/analysis: [`labs/week01-intro`](../../labs/week01-intro/README.md) · slides: `slides/week01.md`.

## Objectives and preparation

Identify assets, adversaries and trust boundaries; select hash, MAC, encryption or signature for a stated goal.

No Docker target or flag is required. Students check their environment in class after the brief introduction; troubleshoot long installations outside the core analysis block.

Images, dependencies and long readings are preparation; the in-class environment check confirms them.
Students may consult the supplied helper after explaining the bounded manual checkpoint. Only
authorized local targets/test data are used. An unavailable environment is handled with a
prepared trace/code example and documented follow-up, not a fabricated successful result.

## In-class run sheet

| Minutes | Activity |
|---|---|
| 0–10 | Ungraded orientation diagnostic and baseline review; no graded retrieval quiz this week. |
| 10–20 | Brief introduction, safety scope and expected evidence; students check their environment. |
| 20–35 | Draw assets, data flows and trust boundaries for the supplied small system. |
| 35–60 | Map confidentiality, integrity and authenticity requirements to primitives; identify three misuse risks. |
| 60–80 | Test the design against one changed attacker assumption and document a correction. |
| 80–95 | Compare results; Snake Oil Bingo on the AI Exhibit (whole class; AIR-Sec groups also analyse the Bingo claims, alongside their Audit-the-AI); feedback on security goals and trust assumptions. |
| 95–100 | Save evidence and submit the in-class checkpoint. |

**Core artifact:** Threat model and primitive-selection diagram.

## Assessment and after-class work

Worksheet 1 is **100 raw points → 2.5 course points**, one of 12 equally weighted worksheets:

| Part | Conventional | AIR-Sec |
|---|---:|---:|
| Core work / observation | 20 | 20 |
| Control verification / limitations | 20 | 20 |
| Reproducible evidence / reasoning | 20 | 20 |
| Conventional technical written questions | 40 | — |
| Audit-the-AI | — | 20 |
| Explain-in-Plain-English | — | 10 |
| Prompt Problem | — | 10 |
| **Total** | **100** | **100** |

Everyone completes shared 60; finish only the assigned form's 40. In Weeks 1/10 shared work is
analysis/diagram/proof, with no Docker or flag requirement. Week 12 code/testing belongs in
shared 60. Preserve and complete the full assigned question text outside class as needed:
Snake-oil claims, terminology and extended CIA/STRIDE questions stay available for the assigned written form and further reading.

The Week 1 orientation diagnostic is ungraded; the Week 1 retrieval bank opens Week 2
within the existing quiz/participation component. Reproduction checks and
short explanations are feedback/authenticity checks within work, with no extra viva score or
automatic AIR-only gate. Use name/ID and cite tools/sources equally in both forms. Flags are
accepted only where the target provides them; a personal flag is required only if configured
and issued, never assumed from a shared default.

## Instructor checks and reflection

- Check that the vulnerable/control experiment produces distinct, interpretable results before class.
- Check evidence, code and explanations together; an output string alone is not full understanding.
- Keep all further-reading questions available; do not turn extension work into an unannounced requirement.
- Record attendance, time actually taken, environment failures, misconceptions and corrections after teaching.
- This 100 minute allocation is a plan; do not claim a human timing pilot has been completed.

See [agenda](../../AGENDA.md), [assessment policy](../../syllabus.md) and [submission rules](../../SUBMISSION.md).
