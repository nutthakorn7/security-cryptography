# Week 14 — User Authentication: The Server Sees Your Password (Unless It Can't)

**Topic (course-plan):** User Authentication · **Kind:** HYBRID
**Concepts:** password submission vs. challenge-response / PAKE, verifier storage, authentication
factors, TOTP vs. FIDO2, credential stuffing, delegated authentication (SSO/OAuth) ·
**Analogous CWE:** CWE-522 (Insufficiently Protected Credentials), CWE-319 (Cleartext Transmission
of Sensitive Information — *to the endpoint*, even when the wire itself is TLS), CWE-532 (Insertion
of Sensitive Information into Log File)

## 100-minute class and assigned worksheet version

**In class:** 10 min retrieval quiz + 10 min brief explanation + 60 min practice/analysis + 15 min debrief + 5 min evidence capture = 100 min.

**Shared core — every student:** Run password-submission and challenge-response scenarios; capture successful login and the log differences; explain replay protection, verifier theft and the limits of this simplified protocol.

**Preparation and extensions:** Prepare images and read the authentication overview. Complete the full factor/MFA/SSO essays or AIR-Sec critique/EiPE/Prompt outside the core block as needed.

**Assessment:** everyone completes the shared core (60 points) plus **one assigned version** (40 points): Conventional written analysis, or AIR-Sec Audit-the-AI 20 + EiPE 10 + Prompt Problem 10. Both versions total 100. All questions remain available; complete the assigned version's full questions, using out-of-class time for extended responses. The other version is ungraded reference practice, not an additional requirement. Viva/micro-demo questions are formative checks of the submitted explanation, with no separate points or automatic pass/fail score gate.

**Evidence:** record reproducible observations or reasoning and your name/student ID. Where the local target prints a shared placeholder flag, record it as observed; a personalized flag or live CTFd account is not a prerequisite. Follow SUBMISSION.md for the announced hand-in channel.

## This week — what to do
1. **Before class** — Docker Desktop working (same Docker-first setup as `software-security` and
   this course's earlier weeks); skim the Week 2 password-hashing recap (you will reuse "store a
   verifier, never the password").
2. **Concept preparation and brief explanation (within the 100-minute plan)** — weekly quiz first (~10 min), then the lecture: why "log in by sending
   your password" hands the plaintext to the *server*, and what a challenge-response / PAKE buys
   you. Slides: `slides/week14.md`.
3. **Practice and assigned-version work (core in class; extensions outside class)** — run the demo in both modes below, then complete **Worksheet 14**
   (`worksheet.md`, shared lab evidence plus the assigned Conventional essays or AIR-Sec Audit-the-AI, EiPE and Prompt Problem).
4. **Submit** — shared-core evidence/reasoning plus your assigned 40-point version in the worksheet PDF via [SUBMISSION.md](../../SUBMISSION.md). Include the observed flag/log artifact where applicable. Supplied exploit/reference code does not require an unchanged GitHub commit.

## Objectives
- Explain why sending a password to the server is a risk **even over TLS** — TLS protects the
  *wire*, but the server *terminates* the TLS and therefore holds your plaintext password; a
  malicious, compromised, or merely over-logging server harvests it.
- **Execute and observe** the difference: in plain-password mode the server logs
  `SERVER SAW PASSWORD: correct-horse-battery`; in challenge-response mode the server logs only a
  nonce and a proof (`SERVER SAW: nonce=... proof=...`) and the password appears **nowhere**, yet
  the client still authenticates (`LOGIN OK`).
- Explain what a challenge-response protocol proves (knowledge of the password) *without*
  transmitting the password, and how the server verifies it from a stored verifier `v = KDF(salt,
  password)` it derived without ever needing to keep the plaintext.
- Distinguish the three authentication factors (know / have / are) and reason about TOTP,
  FIDO2/WebAuthn, credential stuffing, and delegated authentication (SSO/OAuth) — the conceptual
  half of this HYBRID week (Part 1 essays + Part 2 EiPE).
- **Understand the honest limits of this demo** (see the box below): the fixed side proves only
  *"password never transmitted."* It is **not** a full PAKE.

## 🗝️ Signature game — "Never Say the Password"
Play server operator and catch your own login system handing you the plaintext password on a
silver platter, sitting right there in your logs. Then flip on challenge-response and log in
successfully **without the password ever crossing the wire at all** — prove it by grepping your
own logs for it and finding nothing.

**Why it's exciting:** proving you know a secret without ever saying it out loud feels like a
magic trick the first time it clicks — and it's the same trick every "Sign in with..." button
quietly relies on.

## How this maps to the concept

Two services, one network:

| Service | Role | What it does |
|---|---|---|
| `server.py` | Flask auth server | Listens on `:8080`. Behaviour set by env var `PAKE`. **Vulnerable** (`PAKE` unset): `POST /login {username, password}` — receives the plaintext password, **logs it** (`SERVER SAW PASSWORD: ...`), checks it. **Fixed** (`PAKE=1`): `GET /challenge` hands out a random nonce; `POST /login {username, nonce, proof}` — the server recomputes the proof from its **stored verifier** and logs only the nonce + proof, **never** the password. |
| `client.py` | Login client | Runs the flow that matches the mode and prints `LOGIN OK` on success. **Vulnerable:** puts the actual password in the request body. **Fixed:** fetches the nonce, derives `verifier = KDF(salt, password)` **locally**, sends `proof = HMAC(verifier, nonce)` — the password never leaves the client. |

The premise: **TLS is not the whole story.** TLS (which this demo omits for clarity — the lesson is
about the *server endpoint*, not the wire) would stop a network eavesdropper from reading the
password in transit. It does **nothing** about the fact that the server on the other end decrypts
the TLS and then holds your plaintext password in a request handler — free to log it, store it,
forward it, or leak it in a breach. Plain-password login trusts the server completely. A
challenge-response protocol removes that trust: the client proves it *knows* the password by
answering a fresh random challenge, and the server checks the answer against a **verifier**
`v = KDF(salt, password)` it can store without ever holding the plaintext. The password is never
transmitted, so a log reader does not directly receive the plaintext password. This does not prevent offline guessing from a known-salt transcript, and a stolen verifier is directly usable for impersonation in this toy protocol.

> ### Honest scope — this fixed demo is NOT a full PAKE
> The simplified HMAC challenge-response shows that the login request omits the password and that a consumed challenge cannot simply be replayed. Its verifier is password-equivalent: theft permits direct impersonation, and a known-salt transcript or stolen fast verifier permits offline guessing.
>
> A real PAKE provides a mutually authenticated key exchange and resists offline guessing from protocol transcripts under its stated assumptions. **OPAQUE does not eliminate offline guessing after full server compromise**; it prevents pre-computation, and key stretching increases guess cost. Read [RFC 9807, Sections 1 and 10.11](https://www.rfc-editor.org/rfc/rfc9807.html#section-10.11). Keep transcript, credential-file and full-server compromise distinct.
>
> Do not present this toy protocol as SRP/OPAQUE, a production login design or phishing-resistant WebAuthn. Explain the actual observed property and its threat-model limits.

## Run it

Vulnerable mode — plain password login, server harvests the plaintext:
```bash
cd labs/week14-authentication
docker compose -f docker-compose.vulnerable.yml up --build --abort-on-container-exit
```
Expected log lines (timestamps/IPs vary run to run — the container names and the
`SERVER SAW PASSWORD` / `LOGIN OK` text do not):
```
week14-server  | SERVER: listening on 0.0.0.0:8080 (PAKE=False)
week14-client  | CLIENT: plain-password login to http://server:8080 as 'alice' (PAKE=False)
week14-server  | SERVER SAW PASSWORD: correct-horse-battery
week14-client  | LOGIN OK
```
`client` exits `0` once it authenticates; `server` is a long-running server. With
`--abort-on-container-exit` the stack stops as soon as `client` exits. Tear it down:
```bash
docker compose -f docker-compose.vulnerable.yml down
```

Fixed mode — challenge-response, password never transmitted:
```bash
docker compose -f docker-compose.fixed.yml up --build --abort-on-container-exit
```
Expected log lines (the `nonce`/`proof` hex values are random every run):
```
week14-server  | SERVER: listening on 0.0.0.0:8080 (PAKE=True)
week14-client  | CLIENT: challenge-response login to http://server:8080 as 'alice' (PAKE=True)
week14-server  | SERVER SAW: nonce=<32 hex chars> proof=<64 hex chars>
week14-client  | LOGIN OK
```
`client` still exits `0` (`LOGIN OK`) — authentication succeeded — but there is **no**
`SERVER SAW PASSWORD` line anywhere, and the string `correct-horse-battery` appears **nowhere** in
the logs. That absence is your evidence the fix worked. Confirm it explicitly:
```bash
docker compose -f docker-compose.fixed.yml logs | grep -c "correct-horse-battery"   # -> 0
docker compose -f docker-compose.fixed.yml logs | grep -c "SERVER SAW PASSWORD"      # -> 0
```
Tear down the same way:
```bash
docker compose -f docker-compose.fixed.yml down
```

Which compose file you point `-f` at is the **only** thing that selects vulnerable vs. fixed mode
(`PAKE` is baked into each file's `environment:` block for both `server` and `client`). No
environment variables need to be set by hand.

**The captured `SERVER SAW PASSWORD: correct-horse-battery` line (vulnerable mode) — submitted with
your attribution — is the attributable evidence artifact for this HYBRID week, in
place of a CTF flag.** The fixed-mode evidence is the *absence* of that line plus the `grep -c`
returning `0`.

## Verified

Both modes were Docker-tested against the actual files in this directory, run fresh from a
scratchpad copy (OneDrive placeholders can break `docker build` COPY in place, so the build was run
from a plain copy), brought up with `--abort-on-container-exit`, and torn down after.

- **Vulnerable:** the run printed `SERVER: listening on 0.0.0.0:8080 (PAKE=False)`,
  `CLIENT: plain-password login ... (PAKE=False)`, `SERVER SAW PASSWORD: correct-horse-battery`,
  and `LOGIN OK`, with `client` exiting `0`. `docker compose -f docker-compose.vulnerable.yml logs
  | grep -c "SERVER SAW PASSWORD: correct-horse-battery"` returned `1` and `grep -c "LOGIN OK"`
  returned `1`.
- **Fixed:** the run printed `SERVER: listening on 0.0.0.0:8080 (PAKE=True)`,
  `CLIENT: challenge-response login ... (PAKE=True)`, a single
  `SERVER SAW: nonce=327decaec7e5d719846da41ed2c55010 proof=40e701177990a639995ceedb524305dacc1dfa6246484327f687426916b65b15`
  line (hex random per run), and `LOGIN OK` — with `client` still exiting `0`.
  `grep -c "correct-horse-battery"` returned **`0`**, `grep -c "SERVER SAW PASSWORD"` returned
  **`0`**, `grep -c "SERVER SAW: nonce="` returned `1`, and `grep -c "LOGIN OK"` returned `1`.
- Both stacks were torn down (`docker compose down`) and their built images removed after
  verification; nothing was left running.

## Deliverable
Complete the shared core (60 points) and only the assigned version (40 points), as listed in the worksheet rubric. Include reproducible evidence/reasoning in your worksheet PDF. All unassigned-version questions remain available for ungraded practice.

## References
- OWASP *Authentication Cheat Sheet* and *Credential Stuffing Prevention Cheat Sheet* — controls,
  MFA guidance, and why not to log credentials.
- NIST SP 800-63B, *Digital Identity Guidelines — Authentication and Lifecycle Management* —
  authenticator types (memorized secrets, OTP, cryptographic/FIDO), verifier storage, phishing
  resistance.
- T. Wu, *The SRP Authentication and Key Exchange System* (RFC 2945), and [RFC 9807](https://www.rfc-editor.org/rfc/rfc9807.html), *OPAQUE* — distinguish transcript guessing, server compromise and pre-computation resistance.
- W3C *Web Authentication (WebAuthn) Level 2* — origin-bound, phishing-resistant FIDO2 credentials
  (contrast with TOTP).
- RFC 6238, *TOTP: Time-Based One-Time Password Algorithm* — how authenticator-app codes work (and
  why a phished code still works for the attacker).
