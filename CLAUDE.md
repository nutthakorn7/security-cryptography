# Working rules for this repo

## When you change lab content, three things must move together

1. **`labs/weekNN-<slug>/`** — the student-facing worksheet / README / code.
2. **The curriculum monorepo** (`../KOSEN69 - curriculum/lessons/<slug>/`) holds a
   byte-identical copy, enforced by a parity gate:
   `cd "../KOSEN69 - curriculum" && .venv/bin/python -m pytest tests/ -q`
   Apply the *same* edit to both — don't `cp` the `.md` files, the monorepo copies
   carry template tokens (`{{ slot_label }}`, `{{ labpath }}`).
3. **`instructor/weekNN-<slug>-answer-key.md`** — what grades that lab.
   **`instructor/` is git-ignored**, so neither CI nor the diff will remind you. A
   worksheet fix that leaves its key stale means students get marked wrong for
   correct answers. Also check `week07-/week17-review-quiz-answers.md` and
   `week17-jeopardy-bank.md` when a fact changes.

## Watch for state that persists across requests

Several labs keep module-level state (e.g. `week11-signatures-zkp`'s `_seen_txids`
and `_total_withdrawn`). Exact numbers in a worksheet or answer key are only
reproducible in a specific order against a freshly started container — say so
explicitly rather than printing a transcript that students cannot reproduce.

## Audit-the-AI exercises contain deliberate errors

In the CONCEPTUAL weeks, the quoted "AI answer" is *supposed* to be wrong — that is
the exercise. Only the surrounding narration and the answer key's stated correction
must be right. Never "fix" the planted claim.

## Verify by running, not by reading

Payloads, expected output and line-number citations are executed literally by
students. Run the command before claiming it works.

## Dependencies

Lab requirements pin `>=` current versions on purpose (unlike the software-security
repo, nothing here is deliberately outdated). The one exception is `ecdsa` in
`labs/week11-signatures-zkp`, which has an unfixable advisory (CVE-2024-23342) and
is documented as an accepted risk in that lab's `requirements.txt` — leave it.
