# Lesson Plan — Week 12: Secure Transport (TLS & Noise) — the Certificate-Validation-Bypass MITM

| | |
|---|---|
| **Course** | Security & Cryptography (⬚ course code) |
| **Week / date** | 12 · ⬚ |
| **Kind** | HYBRID — a runnable cert-bypass MITM demo alongside content that stays theoretical (the wider Web PKI trust model, and Noise). The attributable artefact is an **evidence log line, not a flag** (AGENDA.md HYBRID callout; SUBMISSION.md submission-mechanism table) |
| **Contact time** | 300 min = 120 lecture + 180 laboratory (AGENDA.md per-week table, Wk 12) |
| **Lab folder** | `labs/week12-secure-transport` |
| **Slides** | `slides/week12.md` |
| **Signature game** | 🎭 "The Impostor's Certificate" |
| **Standards** | Analogous CWE (per lab README/worksheet): CWE-295 (Improper Certificate Validation) · CWE-300 (Channel Accessible by Non-Endpoint). Worksheet "Aligned to": RFC 8446 (TLS 1.3) · RFC 5280 (X.509 PKI) · RFC 6125 (hostname verification) |
| **CLOs addressed** | **CLO2** break the misuse · **CLO3** rebuild it correctly · **CLO4** reason about protocol-level designs (schedule table, spec §6) — plus **CLO1** (Part 1's conceptual-analysis half), **CLO5** (Audit the AI, EiPE, Prompt Problem) and **CLO6** (Evidence & Integrity) via the recurring worksheet parts (spec §4) |

---

## 1. Session objectives

By the end of this week a student can:

**Knowledge (K)** — the first three carry the demonstrable half, the last two the theoretical half

- K1 — Name the three jobs of the TLS handshake (key exchange, server authentication, and the
  `CertificateVerify` message proving possession of the private key) and say what an attacker could
  do if any *one* of them were missing (worksheet Q2; `slides/week12.md`, "The TLS handshake — three
  jobs").
- K2 — Explain the Web PKI chain of trust: why a server certificate is believed because a
  **Certificate Authority signed it**, and why a self-signed certificate claiming the same name
  proves nothing (lab README, Objectives).
- K3 — Distinguish a **trust/issuer** failure from a **hostname mismatch**: both `bob.crt` and
  `impostor.crt` carry `CN=bob` and `SAN=DNS:bob`, so the *only* distinguishing property is the CA
  signature — which is why the fixed client's abort reason is `self-signed certificate` and not a
  name error.
- K4 — Reason about the parts of transport security this week does **not** demonstrate: why the SSL
  family was retired and what TLS 1.3 changed (Q1); forward secrecy versus the legacy static-RSA key
  exchange removed in TLS 1.3, illustrated with Heartbleed (Q3); the 0-RTT early-data
  performance-versus-replay trade-off and why it should be restricted to idempotent operations (Q4);
  and the three mitigations for a *misbehaving or compromised* CA — certificate pinning, revocation
  (CRL / OCSP / OCSP stapling) and Certificate Transparency (Q5).
- K5 — Compare TLS and the Noise Protocol Framework across flexibility, runtime/negotiation
  complexity, upgradeability and security assumptions, and argue when Noise suits two endpoints you
  control — and what is given up by choosing it (Q6). **Noise has no code in this lab**; it is
  examined as written analysis only.

**Skills (P)**

- P1 — *(runnable)* Stand up the vulnerable topology and capture the required evidence line
  `MITM INTERCEPTED: the vault code is 7731`, then state in one line why an *encrypted* channel did
  not protect the secret (Part 2a step 1).
- P2 — *(runnable)* Stand up the fixed topology, capture `CERT VERIFICATION FAILED - ABORTING` with
  its reason line `ALICE: (reason: self-signed certificate)`, and prove the negative with
  `grep -c "MITM INTERCEPTED"` returning `0` (Part 2a step 3).
- P3 — *(runnable, and the only code students write all term)* Implement `build_client_context()` in
  `alice_student.py` so the client trusts only the demo CA, verifies the chain and verifies the
  hostname, then demonstrate it against `docker-compose.student-task.yml` and explain each line
  (Part 2a step 5; SUBMISSION.md's Week-12 coding-scope note).
- P4 — *(written)* Find the `verify=False` flaw in the AI-written "robust HTTPS client", explain the
  attack it enables against a bearer token, name the true-but-misleading reassurance, and produce a
  corrected version that fixes the *root cause* (an internal CA the client was never told to trust)
  rather than disabling verification (Part 2b).
- P5 — *(written)* Explain in plain English why a CA signature turns an unverifiable claim into a
  checkable one, and state the limit of that trust model — what happens if the trusted authority is
  itself dishonest or compromised, which the demo deliberately does not cover (Part 2c).

**Attitude (A)**

- A1 — Attack only the containers this lab spins up; a certificate-validation bypass is a real
  machine-in-the-middle attack, and mounting it against traffic that is not yours is out of scope
  under [ETHICS.md](../../ETHICS.md).
- A2 — Submit identity-stamped evidence (`whoami` / login email / student ID plus a timestamp)
  alongside the captured log lines — the message text is a lab constant, so the identity proof is
  what makes the submission the student's own — and be able to reproduce it live on request.
- A3 — Treat AI-generated security code as something to *verify, not trust*: the Part 2b snippet
  runs, silences the errors and sounds confident, and is exactly the bug the lab just demonstrated.

## 2. Key ideas (the through-line)

Encryption protects a *channel*; it says nothing about *who is on the other end of it*. This week's
demo keeps every piece of TLS's cryptography intact — the key exchange runs, a session key is
negotiated, the bytes on the wire really are ciphertext, and `CertificateVerify` genuinely passes
because the attacker holds the private key for the certificate it presented. The one check the
client skipped is whether anybody it trusts vouched for that certificate. The attacker's cert claims
`CN=bob` with `SAN=DNS:bob`, exactly like the real server's; it is missing one property only, the CA
signature. Turn validation back on and the same forged certificate is rejected *during the
handshake, before the secret is sent* — a trust failure, not a name failure. That is the shape of
almost every real TLS incident: not a broken cipher, but `verify=False` / `CERT_NONE` /
`InsecureSkipVerify` pasted in to silence an error. The theoretical half of the week is where that
picture is completed: forward secrecy, 0-RTT replay, and what happens when the trusted authority
itself is the problem — a case this demo cannot show, because a compromised CA would issue a
*validly chained* certificate and pass the very check that saves us here.

## 3. Prior knowledge and preparation

- **Students, before class:** Docker Desktop working (same Docker-first setup as the earlier weeks);
  skim the **Week 5** (Key Exchanges) MITM recap — the lab README frames this week as its TLS-layer
  sequel — and the **Week 11** signatures material, since a certificate *is* a signature over "this
  key belongs to this name".
- **Instructor, before class:** dependencies are installed at **image build** time (the `Dockerfile`
  does `RUN pip install --no-cache-dir -r requirements.txt` over `cryptography>=48.0.1`), so the
  first `up --build` in the room is a build, not a startup race — pre-pull `python:3.12-slim` and do
  one full dry run of both compose files so nothing is downloading during the session. Per the lab
  README's own *Verified* note, run from a local scratch copy of the lab folder if OneDrive
  placeholder files break the `COPY` step of the build.
- **Prerequisite concepts:** what a digital signature proves; what a self-signed certificate is;
  that a hostname is a name, not an identity.

## 4. Lecture — 120 min

Blocks follow AGENDA.md's HYBRID-week lecture template; content is `slides/week12.md`.

| Time | Block | Content | Method |
|---|---|---|---|
| 0:00–0:10 | Weekly quiz + recap | ~10-min retrieval quiz on Week 11 (signatures & ZKP); recap slide — a certificate **is** a CA's signature over "this key belongs to this name"; today's agenda | Individual quiz, lowest 1–2 dropped |
| 0:10–0:55 | Core concepts | The TLS handshake's three jobs (key exchange, server authentication, `CertificateVerify`); X.509 and the chain of trust — anyone can self-sign a claim, only a trusted CA's signature makes it checkable; hostname verification and why SAN (RFC 6125), not just the legacy CN, is what gets matched | Lecture + board work (draw root → intermediate → leaf) |
| 0:55–1:05 | Break | | |
| 1:05–1:35 | The demonstrable half | The lab's four services on one Docker network (`gen_certs.py`, `bob.py`, `mitm.py`, `alice.py`) and the premise that Alice's `PEER_HOST` is `mitm`, never `bob`; the break — `CERT_NONE` with `check_hostname=False`, CWE-295 / CWE-300 — and the counter-intuitive fact that the handshake genuinely *succeeded* | Lecture + live walkthrough on the projector |
| 1:35–1:55 | Correct construction, defences, **and what stays out of scope** | The fix: load the demo CA as the only trust anchor and keep hostname checking — the MITM's code does not change at all; the real-world form of the bug (`verify=False`, `CERT_NONE`, `InsecureSkipVerify`). Then name explicitly what the demo does *not* show (lab README, "What this lab does *not* show"): a compromised or misbehaving CA, certificate pinning, revocation (CRL/OCSP/stapling), Certificate Transparency — and Noise, which has no code here at all. Those are Part 1 Q5/Q6 and Part 2c | Lecture with a code-diff of Alice's two context branches |
| 1:55–2:00 | Signature-game briefing | 🎭 "The Impostor's Certificate" — capture the interception, then flip validation on and watch the same forged cert bounce; flag Part 2a step 5 as the one week students write the fix themselves | Instruction → to lab |

**Checks for understanding during lecture**
- After the core concept: cold-call — *"if the impostor's name is correct, what is left to catch
  it?"* (only the issuer/signature — this sets up the trust-versus-name distinction the lab turns
  on).
- Before the break: one-minute paper — *"the log says the handshake succeeded and the traffic is
  encrypted; so how did the attacker read the message?"* (ties to Part 2e viva question 1).

## 5. Laboratory — 180 min

Target: `labs/week12-secure-transport`. Four services on one Docker network — `gen_certs` (init),
`bob` (legitimate server, CA-signed cert), `mitm` (attacker, self-signed impostor cert, `CN=bob`)
and `alice` (client). **No host port is published** by any of the three compose files: `8443` is
container-internal, so all evidence comes from the compose logs, not from `curl` on the host.

Environment commands, quoted exactly as the worksheet and README have them:

```bash
cd labs/week12-secure-transport
docker compose -f docker-compose.vulnerable.yml up --build
```
```bash
docker compose -f docker-compose.vulnerable.yml down -v
```
```bash
docker compose -f docker-compose.fixed.yml up --build
```
```bash
docker compose -f docker-compose.fixed.yml logs | grep -c "MITM INTERCEPTED"
```
```bash
docker compose -f docker-compose.fixed.yml down -v
```
```bash
docker compose -f docker-compose.student-task.yml up --build
```
```bash
docker compose -f docker-compose.student-task.yml down -v
```

Laboratory table — one row per actual worksheet task. **Worksheet 12 states no per-task minute
budgets**, so the block boundaries below are AGENDA.md's HYBRID lab template; the task names,
commands and evidence strings are the worksheet's. The **Half** column marks which tasks are the
runnable demo and which are written or oral analysis.

| Time | Task | Half | Student does | Evidence produced |
|---|---|---|---|---|
| 0:00–0:15 | **Onboarding** — stand up the target | Runnable | `cd labs/week12-secure-transport`; `docker compose -f docker-compose.vulnerable.yml up --build`; confirm `gen_certs` completed and `mitm` is listening | `GEN_CERTS: wrote ca.crt, bob.crt …` and `MITM: TLS server listening on 0.0.0.0:8443 …` visible in the logs |
| 0:15–1:20 | **Part 2a steps 1–2** — vulnerable run + teardown | Runnable | Capture the full log; note in one line why encryption did not protect the secret; `Ctrl-C`, then `docker compose -f docker-compose.vulnerable.yml down -v` | The required evidence line `MITM INTERCEPTED: the vault code is 7731`, with identity proof visible; the one-line note |
| 1:20–1:45 | **Part 2a steps 3–4** — fixed run + prove the negative | Runnable | `docker compose -f docker-compose.fixed.yml up --build`; capture the log; run the `grep -c "MITM INTERCEPTED"` command and record that it prints `0`; `Ctrl-C`, then `down -v` | `CERT VERIFICATION FAILED - ABORTING`, the reason line `ALICE: (reason: self-signed certificate)`, and the `grep -c` output `0` |
| 1:45–2:25 | **Part 2a step 5** — write the fix yourself; then start the conceptual extension | Runnable **+** written | Implement `build_client_context()` in `alice_student.py`; run `docker compose -f docker-compose.student-task.yml up --build` until Alice prints the abort line (not a traceback, not `TLS handshake succeeded`); `down -v`. Then begin Part 1 Q1–Q6 (SSL→TLS 1.3, handshake roles, forward secrecy, 0-RTT, Web PKI mitigations, TLS vs Noise) | The completed `build_client_context()` (diff or full function) + a 2–3 sentence explanation of each line; branch `wk12` pushed with the commit hash recorded in the worksheet (SUBMISSION.md); Q1–Q6 drafts |
| 2:25–2:45 | **AI-resilient tasks** — Parts 2b, 2c, 2d | Written | *Audit the AI* (the `verify=False` "robust HTTPS client": quote the line, explain the attack on the bearer token, name the false reassurance, rewrite it correctly); *Explain-in-Plain-English* (why a CA signature matters, and the limit of the trust model); *Prompt Problem* (prompt for a secure HTTPS client against a private CA, then critique the answer against the four checks) | Written answers (start in class, finish as homework) |
| 2:45–2:55 | **Rotating micro-demo** | Runnable, oral | 2–3 rotating students give a 2–3 min "show your before/after log lines" | Live reproduction |
| 2:55–3:00 | **Submit** | — | Everyone submits | Worksheet PDF → Classroom; completed `alice_student.py` on branch `wk12` → GitHub ([SUBMISSION.md](../../SUBMISSION.md)) |

Part **2e** (viva spot-check, three questions held in the worksheet) is instructor-run and live — do
not pre-circulate it; sample it during the micro-demo slot and afterwards.

> **Timing note for the instructor.** AGENDA.md's HYBRID lab template describes its 1:20–1:45 block
> as "flip the flag/env var to the secure configuration" — it budgets **no** slot for Part 2a
> step 5, the write-your-own-`build_client_context()` task, which is unique to this week (spec §6;
> SUBMISSION.md's coding-scope note). The table above places step 5 at the front of the 1:45–2:25
> conceptual-extension window; that placement is this plan's own allocation, not a budget the repo
> states. The consequence is real and should be planned for: on a full session, most of Part 1's six
> essay questions will be started in class and finished as homework. **No worksheet task budget has
> been altered** — the worksheet does not publish any.

> **Instructor note — the step-5 pass criterion does not discriminate.** The worksheet's stated
> done-condition for step 5 is seeing `CERT VERIFICATION FAILED - ABORTING`. A student who writes
> only `return ssl.create_default_context()` — with **no** `cafile=`, never calling the provided
> `wait_for_ca_cert()` — produces that exact line *and* the exact same reason line
> `ALICE: (reason: self-signed certificate)`, because the impostor cert is self-signed and so is
> rejected by the default system trust store too. (Reproduced outside the container against an
> openssl-generated self-signed `CN=bob` certificate: `check_hostname` `True`, `verify_mode` `2`,
> same two output lines.) Such a context trusts the wrong anchors and would also reject the *real*
> Bob — but the lab topology never dials `bob`, so no compose file exposes the difference. Grade
> this on the code and the explanation, not the log line: the worksheet already requires a
> line-by-line explanation of `build_client_context()`, so probe for the `cafile=` argument and ask
> what the client would do when it meets Bob's CA-signed certificate. Do not change the lab files.

**Formative checkpoints.** The commonest step-5 failure is copying `alice.py`'s `if VERIFY:` branch
verbatim — `alice_student.py` defines no `VERIFY`, so that produces a `NameError` traceback rather
than the abort line. The file's own docstring does warn against copying that branch, but for a
different reason: it says not to copy it "without understanding why each line is there," since
students must be able to explain their own code in the worksheet and viva — it does not call out
this specific `NameError` crash. A student who reports
"nothing happens" after a run is usually looking at a stack that has not stopped: `alice` exits
(`0` in vulnerable mode, `1` in fixed mode) while `bob` and `mitm` keep serving, so the session must
be ended with `Ctrl-C` before teardown. Steps 1–4 must be complete by ~1:45 for step 5 to fit; a
student still stuck on the fixed run at that point should move to step 5 (which is independent of
it) and return.

## 6. Assessment for this week

Worksheet 12's own rubric (100 points):

| Criterion | Points | Assesses |
|---|---|---|
| Conventional arm — 6 essay questions (Part 1) | 36 | CLO1, CLO4 |
| Lab evidence — both modes captured, evidence lines present/absent as required (Part 2a) | 18 | CLO2, CLO3 |
| Audit the AI — `verify=False` flaw found + corrected, false-reassurance named (Part 2b) | 20 | CLO5 |
| EiPE — why a CA signature matters, in plain English (Part 2c) | 12 | CLO5 |
| Prompt Problem (Part 2d) | 8 | CLO5 |
| Viva spot-check (Part 2e, instructor-run) | 6 | CLO2, CLO3, CLO6 |

How the 100-point worksheet feeds the course marks (spec §4):

| Instrument | Outcome | Course weight |
|---|---|---|
| Worksheet 12 (all parts above) | CLO1–CLO6 | Part of the 30% weekly-worksheet component |
| Completed `alice_student.py` on branch `wk12`, commit hash recorded in the worksheet | CLO3 | Graded within Part 2a; this is the only code push of the term (SUBMISSION.md) |
| Weekly quiz (start of lecture) | CLO1, CLO2, CLO4 | Part of the 10% quiz + participation component |
| Viva spot-check / micro-demo | Live reproduction and explanation | Pass/fail gate on the lab and Audit-the-AI scores — an instructor who is not convinced may re-score those sections down (per the pass/fail-gate line in the Weeks 6/11/15 instructor answer keys, not spec §9, which only says viva spot-checks "sample submitted work each week"; Week 12's own `instructor/week12-secure-transport-answer-key.md` does not yet carry this line) |
| Evidence log lines + identity proof | Attributable evidence | Integrity control, not a separate mark |

**This week issues no flag.** AGENDA.md's HYBRID callout and SUBMISSION.md's submission-mechanism
table both classify Week 12 as evidence-log-gated: students submit the vulnerable-run line and the
fixed-run line, and `SECRET_MESSAGE` is a lab constant identical for every student — the identity
proof, not the string, is what attributes the work. Model answers and detailed grading notes are in
the instructor-held `instructor/week12-secure-transport-answer-key.md`; the three Part 2e viva
questions stay in the worksheet and are not reproduced here.

## 7. Materials

- Lab: `labs/week12-secure-transport/` — `gen_certs.py`, `bob.py`, `mitm.py`, `alice.py`,
  `alice_student.py`, `docker-compose.vulnerable.yml`, `docker-compose.fixed.yml`,
  `docker-compose.student-task.yml`, `Dockerfile`, `requirements.txt`, `worksheet.md`, `README.md`.
- Slides: `slides/week12.md`.
- References (from the lab README): RFC 8446 (*TLS 1.3*); RFC 5280 (*X.509 PKI Certificate and CRL
  Profile*); RFC 6125 (*Domain-Based Application Service Identity* — hostname verification and
  SubjectAltName); OWASP *Transport Layer Security Cheat Sheet* and *Testing for Weak Transport
  Layer Security*; the Python `ssl` module docs (`create_default_context`, `check_hostname`,
  `CERT_NONE` vs `CERT_REQUIRED`); Trevor Perrin (ed.), *The Noise Protocol Framework*.
- Student reading list for this week ([readings.md](../../readings.md), W12): RFC 8446 (at least
  §1–2), a Web PKI / Certificate Transparency explainer, the Noise Protocol Framework spec.
- Submission channels: [SUBMISSION.md](../../SUBMISSION.md) · Rules of engagement:
  [ETHICS.md](../../ETHICS.md).

## 8. Risks and contingencies

| Risk | Mitigation |
|---|---|
| The first `up --build` in the room builds the image and installs `cryptography>=48.0.1` (a `Dockerfile` `RUN`, not a container-start step), stalling the session on a slow network | Pre-pull `python:3.12-slim` and pre-build both compose files before class; the build is cached afterwards, so only the first run pays it |
| OneDrive placeholder files break the `COPY` step of `docker build` on the instructor's machine | Per the README's *Verified* note, run the lab from a local scratch copy of the folder |
| `docker-compose.vulnerable.yml` and `docker-compose.fixed.yml` share container names (`week12-gencerts`, `week12-bob`, `week12-mitm`, `week12-alice`) **and** the `certs` volume — starting one while the other is up collides, and skipping `down -v` reuses stale certificates | Enforce the worksheet's teardown order: `Ctrl-C`, then `down -v` on the file just used, before starting the next mode. `docker-compose.student-task.yml` is safe to run alongside — it uses `-student` container names, `certs_student` and `labnet_student` |
| Students report the run "hangs" and never returns a prompt | Expected: `alice` exits (`0` vulnerable / `1` fixed) while `bob` and `mitm` are long-running servers. Stop with `Ctrl-C`, then tear down — the README says so explicitly |
| A student tries to reach the target from the host (`curl localhost:8443`, browser) and concludes the lab is broken | No compose file publishes a host port; `8443` exists only on the `labnet` bridge network. All evidence is compose log output |
| Step 5 produces a `NameError` traceback because the student pasted `alice.py`'s `if VERIFY:` branch | `alice_student.py` defines no `VERIFY`; point them at the file's docstring — one `ssl.create_default_context(cafile=…)` call does chain and hostname validation correctly |
| Step 5 "passes" with a context that loads no CA at all (see the instructor note in §5) | Grade the code and the line-by-line explanation, and probe the `cafile=` argument in the viva; the abort line alone does not prove the fix is right |
| A student copies a classmate's log lines — the intercepted message is identical for everyone | Identity-stamped captures (`whoami` / login email / student ID + timestamp) are the control, backed by the viva spot-check ("reproduce that line now") |
| A pair finishes everything early | Extension: have them explain what an attacker holding a certificate that *does* chain to the trusted CA (Q5's compromised-CA case) would defeat, and why nothing in this demo would catch it; or diff the two compose files and confirm for themselves that Alice's `VERIFY` line is the only behavioural difference |

Remember to `down -v` every stack at the end of the session so the next run regenerates fresh
certificates.

## 9. Post-teaching reflection

*Complete after the session — this also feeds the course's engagement data.*

- Attendance / completion: ⬚
- Time actually taken per block (vs. plan — the write-your-own-fix step is unbudgeted by AGENDA.md
  and this is its first exercise with real students): ⬚
- How many students landed step 5 in class, and how many needed the `NameError` hint: ⬚
- How many step-5 submissions omitted `cafile=` yet still showed the abort line: ⬚
- Where the class got stuck, and what unblocked them: ⬚
- Misconception that showed up in the *Explain-in-Plain-English* answers (especially the
  compromised-CA limit): ⬚
- Quality of the *Audit the AI* critiques — did students attack `verify=False` and the
  true-but-misleading "it's encrypted" claim, or waste the critique arguing the traffic was not
  encrypted?: ⬚
- Whether Part 1's six essays fitted the session or slipped entirely to homework: ⬚
- Anything to change before this week runs again: ⬚
