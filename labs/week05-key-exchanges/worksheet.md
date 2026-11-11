# Worksheet 5 — Key Exchanges: MITM Against Unauthenticated Diffie-Hellman

> **Course:** Cryptography and Network Security (KOSEN69) · **Week 5**
> **Aligned to:** RFC 3526 (MODP groups) · CWE-322 (Key Exchange without Entity Authentication),
> CWE-300 (Channel Accessible by Non-Endpoint)
> **Kind:** Hybrid — a runnable MITM demo and short explanations of its two handshakes.
> Small-subgroup attacks are an optional later-study topic, not assessed this week.

## How to use this worksheet — 100-minute class, two versions

Everyone completes the **same common activity (60 points)**. Complete only the
**Conventional written assessment (40)** or the **AIR-Sec assessment (40)** assigned
by the instructor. AIR-Sec's 40 points are Audit the AI 20, EiPE 10 and Prompt Problem 10.
Each version totals **100**, and neither version requires the other format for marks.

| Common criterion | Points | This week's evidence |
|---|---:|---|
| Core activity / analysis | 20 | Run both DH topologies and trace the relay's two independent handshakes and interception. |
| Control comparison and limitations | 20 | Explain what the HMAC check changes, the pre-shared-key assumption, and why the session still uses fresh DH. |
| Evidence and causal reasoning | 20 | Record both modes, both authentication failures and the interception count, and explain the observations rather than submitting a flag alone. |

**Before class:** complete the stated reading and any environment setup; software
installation and first image downloads are preparation, not extra contact minutes.
**In class (100 minutes):** 10 quiz/review + 10 brief + 60 shared practice/analysis +
15 debrief + 5 evidence capture. The opening quiz reviews Week 4; the Week 5 quiz is
taken at the start of Week 6. The detailed tasks below are a checklist, not
additional timed class blocks: work through the core observations in the guided practice,
draft the explanation in the debrief, then finish the assigned 40-point format before
the published deadline. Questions labelled optional carry no marks.

## Part 0 — Student Information
| Name | Student ID | Date | Group |
|---|---|---|---|

*Disclose any AI assistance used anywhere in this worksheet here (tool + what you asked it).*

---

## Part 1 — Conventional form (40 points; only if assigned)

Answer **Q1–Q4 only**, in about 2–4 sentences each. Each question is worth 10 points.
Use the lab logs and this week's slides; no group-theory calculation is required.

**Q1 (10).** Why not send the AES key directly over the open network? What do the public
values in a DH exchange let Alice and Bob do instead?

**Q2 (10).** In the vulnerable run, who shares the Alice-side secret, and who shares the
Bob-side secret? Explain how Relay reads the message without solving a discrete logarithm.

**Q3 (10).** Plain, unauthenticated DH protects against an observer who only listens,
but Relay can actively substitute public values. What does the HMAC check in the fixed
run stop? Give one condition the fix relies on.

**Q4 (10).** Why does the fixed run still make a fresh DH session key instead of using
the pre-shared `AUTH_KEY` to encrypt messages? Explain what happens to past recorded
traffic if `AUTH_KEY` is exposed later, assuming the ephemeral DH secrets were erased.

**Optional study questions (ungraded):** Why use a vetted large DH group? What happens
if a peer's public value is not validated? How do ECDH and X25519 differ from this finite-field
demo? Small-subgroup attacks are a separate input-validation topic; the running lab does not
demonstrate one, and no answer about them is required for this worksheet.

---

## Part 2 — Shared common practice and assigned AIR-Sec assessment

AI is a power tool you must **distrust** — several parts below are graded on your *critique*,
not on how well you can prompt an AI. Full run instructions: [`README.md`](README.md).

### Part 2a — Shared lab steps and evidence (both versions, 60 points)

**Before class — get to the lab folder.** If you still have the Week 4 course ZIP,
use it if it contains `labs/week05-key-exchanges`; otherwise download a fresh ZIP:
open <https://github.com/nutthakorn7/security-cryptography>, choose **Code → Download ZIP**,
then extract it (Windows: **Extract All**; Mac: double-click). No GitHub account or
host Python installation is needed. Start Docker Desktop and wait for **Engine running**.
Open the extracted `security-cryptography-master/labs/week05-key-exchanges` folder
(there may be two similarly named outer folders after extraction).

- **Windows:** In File Explorer, right-click empty space inside `week05-key-exchanges`
  and choose **Open in Terminal**. If unavailable, Shift-right-click and choose
  **Open PowerShell window here**.
- **Mac:** Open Terminal, type `cd` followed by one space, drag the `week05-key-exchanges`
  folder into Terminal, then press Enter.

Check your location with `dir` on Windows or `ls` on Mac. You should see
`docker-compose.vulnerable.yml` and `docker-compose.fixed.yml`. Keep this Terminal
in the lab folder for every command below. If you closed Docker Desktop since
preparation, start it again and wait for **Engine running**.

**Setup.** `common.py` gives all three services (`alice.py`, `bob.py`, `relay.py`) a shared
RFC3526 Group 14 (2048-bit) DH group. Alice is configured to dial `relay`, never `bob` directly —
that is the premise: an active attacker controls the network path.

1. Run **vulnerable mode**:
   ```bash
   docker compose -f docker-compose.vulnerable.yml up --build
   ```
   Capture the full log output. Your required evidence line is:
   ```
   RELAY INTERCEPTED: the launch code is 4471
   ```
   **This is shared lab evidence for both versions, not a personalised flag.**
   The message is fixed for the class; capture your own run, identify it with your name/student ID,
   and explain it. Note in one line: which two `RELAY: completed independent DH
   handshake...` lines appear *before* the interception, and why relay needed both before it
   could decrypt-and-relog.
2. Tear down: `Ctrl-C`, then `docker compose -f docker-compose.vulnerable.yml down`.
3. Run **fixed mode**:
   ```bash
   docker compose -f docker-compose.fixed.yml up --build
   ```
   Capture the full log output. Your required abort evidence is **both** of:
   ```
   AUTH FAILED - ABORTING
   ```
   (once from `alice`, once from `bob`) and the **absence** of any `RELAY INTERCEPTED` line.
   Confirm the absence explicitly. On Mac/Linux Terminal:
   ```sh
   docker compose -f docker-compose.fixed.yml logs | grep -c "RELAY INTERCEPTED"
   ```
   On Windows PowerShell:
   ```powershell
   (docker compose -f docker-compose.fixed.yml logs | Select-String -SimpleMatch "RELAY INTERCEPTED" | Measure-Object).Count
   ```
   Record the `0` result. The example counts lines; it does not prove a trusted
   Alice–Bob connection succeeds, only that Relay did not log an intercepted message.
4. Tear down: `Ctrl-C`, then `docker compose -f docker-compose.fixed.yml down`.

**Submit:** both captured logs (identified with your name/student ID), your one-line note from step 1,
and the zero-count output from step 3.

### Part 2a-AIR — Audit the AI (AIR-Sec version only, 20 points)

**Deliberately flawed teaching artifact — critique it; do not implement it:**

> "Alice and Bob can run unauthenticated DH, derive a fresh session key, and then
> authenticate every message with HMAC under that derived key. A MITM cannot know
> the session key, so a valid message HMAC proves Bob's identity. There is no need
> to trust a certificate, signature key or pre-shared authentication key first."

Write 1–2 sentences for each numbered item.

1. Quote the claim that fails for the active relay in this lab and explain the difference
   between authenticating data with a negotiated key and authenticating the peer's identity.
2. Explain what the attacker knows after its two exchanges. Compare the artifact's proposal
   with the actual fixed topology and identify the trust assumption that the fix adds.
3. Correct the explanation and state what fresh DH contributes after authentication is added.
   Discuss the limitation if the authentication key is exposed. Submit your critique and
   corrected explanation; no additional exploit or production protocol implementation is required.

### Part 2b — Explain in Plain English (EiPE): the two-secret relay (AIR-Sec only, 10 points)

In 3–4 short sentences, explain the vulnerable run to a classmate who has not studied DH.
Say who shares the first secret, who shares the second, and why Relay can read and forward
the message. Make clear that Alice and Bob do **not** share either secret directly in this
attack. Use everyday words; a formula or group-theory explanation is not required.

### Part 2c — Prompt Problem (AIR-Sec version only, 10 points)

Ask an AI assistant a single prompt along the lines of: *"Explain why authenticated
Diffie-Hellman prevents a man-in-the-middle attack."* Paste its full response, then critique it.
At minimum, check whether the AI's answer:
- Correctly distinguishes *confidentiality against eavesdroppers* (what plain DH already gives
  you) from *authentication of the peer's identity* (what plain DH does **not** give you).
- Explains authentication as binding the DH public key to a verified identity (signature,
  certificate, or pre-shared MAC key) — not just asserting "authenticated DH is secure" without
  saying what is actually being checked or against what.
- Gets the trust bootstrap right: authenticated DH is only as strong as however the
  authentication key/certificate itself was distributed — an AI answer that hand-waves "just use
  a certificate" without noting that the certificate's issuer must itself be trusted in advance
  has hidden the hard part.
- Doesn't quietly conflate "authenticated" with "still gives forward secrecy" — a good answer
  should note that authenticating the exchange does not turn it into "just send a symmetric key,"
  because the DH exponents are still fresh and ephemeral every session.
- Doesn't hallucinate a mechanism (e.g. inventing a made-up "DH-Auth handshake" or misattributing
  a specific RFC/algorithm it doesn't actually name correctly).

**Submit:** your exact prompt, the AI's full response, and one short sentence per check
identifying what the answer gets right, omits, or gets wrong. Quote a relevant phrase where
possible; a closing sentence may summarize the biggest correction.

### Part 2d — Viva Spot-Check (formative/authenticity check; no separate points)

Be ready to answer these live, in your own words, with no notes:

1. In the vulnerable-mode logs, `relay` completes **two** DH handshakes before it prints
   `RELAY INTERCEPTED`. Why two, and what would go wrong for the attacker with only one?
2. In fixed mode, `relay.py`'s `handle_mitm_signed` still runs — it still generates its own DH
   keypairs and still tries to substitute them into both handshakes. What exactly stops the
   attack from succeeding, given that `relay` is running almost the same code as in vulnerable
   mode?
3. `AUTH_KEY` is a value Alice and Bob share ahead of time. Doesn't that mean they could have
   just used `AUTH_KEY` itself as the encryption key and skipped DH entirely? Why or why not —
   what would be lost?

---

## Grading rubric — assigned version totals 100

| Criterion | Conventional | AIR-Sec |
|---|---:|---:|
| Common core activity / analysis | 20 | 20 |
| Common control comparison and limitations | 20 | 20 |
| Common evidence and causal reasoning | 20 | 20 |
| Conventional written questions | 40 | — |
| AIR-Sec Audit the AI | — | 20 |
| AIR-Sec Explain in Plain English (EiPE) | — | 10 |
| AIR-Sec Prompt Problem | — | 10 |
| **Total for the assigned version** | **100** | **100** |

**Deadline and late work:** hand in by 23:59 Thai time (ICT) on the Sunday before the next week's
class (KOSEN rule); the exact date is in your codes email and in the week's Classroom post.
Late work loses 10% of this worksheet's score for each day late (a part day counts as a day), down to 0.
Uploading or replacing a file after the deadline makes the whole hand-in late.

Submit the common work plus **one** assigned assessment format; do not add the two
format columns or complete both formats for extra marks. Optional questions carry no marks.
A viva is a formative/authenticity check within the relevant criteria,
with feedback or a request to clarify/reproduce evidence; it has no separate points and
no automatic-zero rule. Grade the demonstrated work against the published criteria.


## Evidence & Integrity (required)

- **Evidence attribution (the same for both versions):** put your name/student ID and
  date on the worksheet, and capture your own commands and results. Make clear which run
  each observation came from. A terminal timestamp or identity stamp is optional context,
  not an extra scored personal artifact. If evidence is unclear, the instructor may request
  clarification within the common evidence/reasoning criterion.
- **Runtime flag (where this lab returns one):** record the value from your own run. Use a
  personalised configuration only if the instructor supplies it; otherwise the shared demo
  flag is acceptable with your own evidence and reasoning. No automatic roster/flag validation
  is assumed. Do not submit a classmate's capture as your own.
- Optional context stamp: `printf '%s | %s | ' "$(whoami)" '<YOUR-STUDENT-ID>'; date '+%F %T %Z'`.
  You may include this with a terminal/browser capture if useful. A separate terminal or
  whole-screen identity capture is not required; legible own commands/results and the
  worksheet name/student ID are sufficient. All common evidence is within the common 60.
- **Explain in your own words** *(graded on your reasoning, not copied text)*:
  1. What did the attack do, and **why did it work** against unauthenticated DH?
  2. **Why does the HMAC fix actually stop it** — and what would still break it (e.g. if `relay`
     somehow obtained `AUTH_KEY`)?
