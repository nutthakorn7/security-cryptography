# Worksheet 14 — User Authentication: The Server Sees Your Password (Unless It Can't)

> **Course:** Cryptography and Network Security (KOSEN69) · **Week 14**
> **Aligned to:** NIST SP 800-63B · OWASP Authentication / Credential Stuffing Cheat Sheets ·
> CWE-522 (Insufficiently Protected Credentials), CWE-532 (Sensitive Info in Log File).
> The demo uses HTTP on an isolated Docker network; CWE-319 applies to that unencrypted transport,
> not to a server receiving plaintext after TLS termination.
> **Kind:** Hybrid — a runnable password-sent-vs-never-sent demo (Part 2a) alongside conceptual
> content that stays theoretical this week (TOTP/FIDO2/SSO comparison, Part 1 + Part 2c EiPE).

## 100-minute class and assigned worksheet version

**In class:** 10 min Week 13 retrieval quiz/review + 10 min brief explanation + 60 min practice/analysis + 15 min debrief + 5 min evidence capture = 100 min. The scored Week 14 quiz opens in Week 15.

**Shared core — every student:** Run password-submission and challenge-response scenarios; capture successful login and the log differences; explain replay protection, verifier theft and the limits of this simplified protocol.

**Preparation and extensions:** Prepare images and read the authentication overview. Complete the full factor/MFA/SSO essays or AIR-Sec critique/EiPE/Prompt outside the core block as needed.

**Assessment:** everyone completes the shared core (60 points) plus **one assigned version** (40 points): Conventional written analysis, or AIR-Sec Audit-the-AI 20 + EiPE 10 + Prompt Problem 10. Both versions total 100. All questions remain available; complete the assigned version's full questions, using out-of-class time for extended responses. The other version is ungraded reference practice, not an additional requirement. Viva/micro-demo questions are formative checks of the submitted explanation, with no separate points or automatic pass/fail score gate.

**Evidence:** record reproducible observations or reasoning and your name/student ID. Where the local target prints a shared placeholder flag, record it as observed; a personalized flag or live CTFd account is not a prerequisite. Follow SUBMISSION.md for the announced hand-in channel.

## Part 0 — Student Information
| Name | Student ID | Date | Group |
|---|---|---|---|

*Disclose any AI assistance used anywhere in this worksheet here (tool + what you asked it).*

---

## Part 1 — Conventional Arm: Essay Questions

Answer each in your own words (roughly 120–200 words per answer — enough to show you understand the
mechanism, not so much that you're padding).

**Q1.** Why is sending a password to the server — **even over TLS** — a risk? Name at least three
distinct ways the server-side plaintext password can be exposed.

**Q2.** What is the difference between the three authentication factors (something you *know* /
something you *have* / something you *are*)? Give one concrete example of each, and state one
weakness of each.

**Q3.** What does a challenge-response protocol achieve that plain password submission does not?
Explain what actually travels on the wire in each case.

**Q4.** What is a PAKE (e.g. SRP, OPAQUE)? Explain mutual authenticated key exchange and resistance to offline guessing from protocol transcripts. Then distinguish that threat from a stolen credential file/full server compromise: what does OPAQUE's pre-computation resistance add, and why can offline guesses remain possible after compromise? Use [RFC 9807 Sections 1 and 10.11](https://www.rfc-editor.org/rfc/rfc9807.html#section-10.11).

**Q5.** How does TOTP (an authenticator app) work? Why can a lookalike site relay a TOTP code,
while a correctly implemented FIDO2/WebAuthn sign-in resists that origin-based phishing?
(Consider what the user types vs. what the authenticator does, and what each is bound to.)

**Q6.** What is credential stuffing? Which single control most reduces its blast radius, and why
does that control help even when the leaked passwords are genuinely correct for some accounts?

**Q7.** Password-storage recap (ties to Week 2): why should the server's stored verifier use
bcrypt/argon2 **with a per-user salt**, rather than a plain fast hash? What does the salt stop, and
what does the slow/memory-hard work factor stop?

**Q8.** SSO / OpenID Connect: what does delegated sign-in buy you (for users and for the relying
application)? What new concentration-of-risk does introducing an identity provider create?
Distinguish OpenID Connect authentication from OAuth 2.0 authorization.

---

## Part 2 — Shared Lab Core and Assigned AIR-Sec Tasks

AI is a power tool you must **distrust** — several parts below are graded on your *critique*, not on
how well you can prompt an AI. Full run instructions: [`README.md`](README.md).

### Part 2a — Shared lab steps + evidence artifact (required for both versions)

**Setup.** `server.py` is a Flask auth server whose behaviour is set by the `PAKE` env var (baked
into each compose file). `client.py` runs the matching login flow. The demo account is `alice` with
password `correct-horse-battery`.

1. Run **vulnerable mode** (plain password login):
   ```bash
   cd labs/week14-authentication
   docker compose -f docker-compose.vulnerable.yml up --build --abort-on-container-exit
   ```
   Capture the full log output. Your required evidence line is:
   ```
   SERVER SAW PASSWORD: correct-horse-battery
   ```
   plus `LOGIN OK` from the client. **This `SERVER SAW PASSWORD` line is your
   attributable artifact for this HYBRID week, in place of a CTF flag.** The password
   string is a lab constant (the same for every student), so what makes your submission *yours* is
   the attribution you attach: include your name/student ID and a reproducible capture or annotated transcript from your own run, as described in Evidence & Integrity. In one line, note **which service printed the password and why** — i.e. what does the
   server having your plaintext in a request handler let a malicious operator do that TLS did not
   prevent?
2. Tear down: `docker compose -f docker-compose.vulnerable.yml down`.
3. Run **fixed mode** (challenge-response):
   ```bash
   docker compose -f docker-compose.fixed.yml up --build --abort-on-container-exit
   ```
   Capture the full log output. Your required evidence is **all** of:
   - a `SERVER SAW: nonce=... proof=...` line (the server logged what it *did* receive),
   - `LOGIN OK` from the client (authentication still succeeded), and
   - the **absence** of any `SERVER SAW PASSWORD` line and of the password string itself.
   Confirm the absence explicitly in the **server log** and record what you see:
   ```bash
   docker compose -f docker-compose.fixed.yml logs server
   docker compose -f docker-compose.fixed.yml logs client
   ```
   Search the server output visually for `correct-horse-battery` and `SERVER SAW PASSWORD`:
   neither should appear. The client output must show `LOGIN OK`. These commands work in
   Windows PowerShell and Mac Terminal. A missing match in a log is evidence only for this run;
   inspect the code and the honest-scope box before making a broader security claim.
4. Tear down: `docker compose -f docker-compose.fixed.yml down`.

**Submit:** both captured logs (with your name/student ID and reproducible attribution), your one-line note from step 1, and
the two log outputs from step 3 and your explicit no-match observation for the server log.

**One-line reflection to include with your logs** *(graded on reasoning, not copied text)*: in the
fixed mode the client still proves it knows `correct-horse-battery`, yet the server never sees it.
In your own words: what does the client send *instead* of the password, and why can't an attacker
who records that (the nonce and the proof) reuse it to log in later?

### Part 2b — Assigned AIR-Sec Audit-the-AI

A teammate asked an AI assistant to "write a Flask login handler with good logging for debugging."
The AI produced the handler below. It runs, it authenticates correctly, and the logging "looks
professional." **Find the security flaw, name it, and say exactly which line leaks what to whom.**

```python
import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("auth")

@app.post("/login")
def login():
    body = request.get_json(force=True)
    # Log the full request so we can debug failed logins in production.
    log.info("login attempt: %s", body)           # <-- (A)
    user = users.get(body["username"])
    if user and bcrypt.checkpw(body["password"].encode(), user.pw_hash):
        log.info("login OK for %s", body["username"])
        return {"status": "ok"}
    log.warning("login FAILED for %s (pw=%s)", body["username"], body["password"])  # <-- (B)
    return {"status": "denied"}, 401
```

Answer, in your own words:
1. **What is the flaw?** Name the vulnerability class (and the CWE if you can) — note that the
   password *storage* here (`bcrypt.checkpw` against `pw_hash`) is actually *correct*; the flaw is
   elsewhere.
2. **Which line(s), and what exactly leaks?** Point to `(A)` and `(B)` specifically. What ends up in
   the logs? Who can read production logs (think: log-aggregation services, on-call engineers,
   anyone who breaches the log store)?
3. **Why does this partly defeat the point of hashing the stored password?** (Even though
   `pw_hash` is a proper bcrypt hash, what has the log now captured in *plaintext*?)
4. **Fix it.** Rewrite the two logging lines so the handler is still debuggable (you can tell *that*
   a login failed and *for which username*) without ever logging the password or the raw body.
5. **Tie-back:** how does this planted flaw relate to what you observed in Part 2a's **vulnerable**
   mode? (Both are the same underlying mistake — the credential reaching a place it should never
   reach. Name that place in each case.)

### Part 2c — Assigned AIR-Sec EiPE: proving knowledge without sending the password

The lab's fixed mode lets the client prove it knows the password **without sending it**. This
section is the conceptual half of this HYBRID week: explain the idea **in plain English to someone
who has never taken a crypto course** (no "HMAC," "KDF," or "nonce" used without first explaining
what you mean in ordinary words). In 4–6 sentences, cover:
- The everyday intuition: how can you convince a doorman you know the day's password *without
  saying the password out loud* where someone could overhear and reuse it? (Hint: the doorman
  shouts a fresh random word each time and you have to combine it with the secret in an agreed
  way.)
- Why the fixed-mode server can check your answer while storing a password-derived "verifier"
  rather than the plaintext password (the demo preloads this verifier).
- Why an eavesdropper who records one exchange (the random challenge and your answer) **cannot**
  reuse it tomorrow.
- The honest limit (see README's honest-scope box): this demo proves *only* that the password is
  never sent. Name **one** thing a real PAKE also protects against that this demo does **not**.

### Part 2d — Assigned AIR-Sec Prompt Problem

Ask an AI assistant a single prompt along the lines of: *"How should I securely handle user login
so the server never learns the user's password?"* Paste its full response, then critique it. At
minimum, check whether the AI's answer:
- Distinguishes *protecting the password on the wire* (TLS) from *keeping the password away from the
  server endpoint* (challenge-response / PAKE) — a weak answer says "just use HTTPS" and stops
  there, missing that the server still sees the plaintext.
- Names a real mechanism correctly (SRP, OPAQUE, WebAuthn) rather than hand-waving "use a secure
  library" — and doesn't **hallucinate** a made-up protocol or misattribute an RFC.
- If it recommends a PAKE, does it distinguish mutually authenticated key exchange and transcript resistance from server compromise? For OPAQUE, does it distinguish pre-computation resistance from the incorrect claim that a fully compromised server can never test password guesses? Does it overclaim client-side hashing as a PAKE, even though the hash can become a reusable password-equivalent secret?
- Mentions verifier storage correctly (a slow, salted KDF such as bcrypt/argon2) and does **not**
  suggest storing anything reversible.

**Submit:** your exact prompt, the AI's full response, and a bullet-by-bullet critique quoting the
specific sentence(s) that are correct, hand-waved, or wrong.

### Part 2e — Formative Viva Spot-Check (no separate points)

Be ready to answer these live, in your own words, with no notes:

1. In **vulnerable** mode the server prints `SERVER SAW PASSWORD: correct-horse-battery`. If the
   whole connection had been wrapped in TLS, would that line still appear in the server's log? Why
   or why not — what does TLS actually protect, and what does it not?
2. In **fixed** mode the client still proves it knows the password, but the server only logs a
   `nonce` and a `proof`. Walk through how the server decides the login is valid **without** ever
   having the password. What does the server compare against?
3. The README is explicit that this fixed demo is **not** a full PAKE. Explain the missing mutually authenticated key exchange and transcript-guessing resistance; then distinguish verifier theft from OPAQUE's full-server-compromise limits. Give a concrete scenario for each threat.

---

## Grading rubric (100)

| Criterion | Conventional | AIR-Sec |
|---|---:|---:|
| Shared practical core: complete the assigned run or coding steps | 20 | 20 |
| Shared control and limitations: compare the secure control and explain what it does and does not show | 20 | 20 |
| Shared reproducible evidence and reasoning: attributable observations, commands/results and explanation | 20 | 20 |
| Assigned Conventional written questions | 40 | — |
| Assigned AIR-Sec Audit-the-AI | — | 20 |
| Assigned AIR-Sec Explain-in-Plain-English | — | 10 |
| Assigned AIR-Sec Prompt Problem | — | 10 |
| **Total for the assigned version** | **100** | **100** |

**Deadline and late work:** hand in by 23:59 Thai time (ICT) on the Sunday before the next week's
class (KOSEN rule); the exact date is in your codes email and in the week's Classroom post.
Late work loses 10% of this worksheet's score for each day late (a part day counts as a day), down to 0.
Uploading or replacing a file after the deadline makes the whole hand-in late.

Viva/micro-demo checks are formative: no separate points and no automatic score gate. The 60 shared points apply to both versions; do not add the unassigned version's 40 points.

See the instructor answer key *(instructor use only, not in this file)* for model answers to all 8
essay questions, the Audit-the-AI fix, and the detailed lab/viva grading notes.

---

## Evidence & Integrity (required)

- **Attribution and reproducibility (both versions):** put your name/student ID on the submitted work and provide your own commands, observations and explanation. A screenshot or annotated transcript is acceptable; shared placeholder output is not per-student proof by itself.
- **Optional terminal-stamp example:** `printf '%s | %s | ' "$(whoami)" '<YOUR-STUDENT-ID>'; date '+%F %T %Z'`. This is one way to label a capture, not a separate requirement, point allocation or live-personalization prerequisite.
- **Personalized/attributable artifact:** the `SERVER SAW PASSWORD: correct-horse-battery` line from
  Part 2a vulnerable mode, submitted **together with** your attributed screenshot or annotated transcript — the identity
  proof is what makes it yours, not the password text (which is a lab constant). For fixed mode, the
  artifact is the *absence* of that line in the fixed-mode server log, together with the
  server/client log capture and your explicit no-match observation. Submitting
  someone else's captured log without your own attribution is a violation.
- **Explain in your own words** *(graded on your reasoning, not copied text)*:
  1. In vulnerable mode, **who** ended up with the plaintext password and **why did TLS not
     prevent it**?
  2. In fixed mode, **what did the client send instead of the password**, and **why can't a
     recorded challenge+proof be replayed** to log in again later?
