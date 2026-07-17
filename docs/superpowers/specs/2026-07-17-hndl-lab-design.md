# Lab design — "Harvest Now, Decrypt Later" (HNDL) + Hybrid KEM

**Status:** Approved by user 2026-07-17. Not yet implemented (build gated on a subagent quota
reset). Security & Cryptography course.

## Why

The Week 15 diagram's centre is the *confidentiality* migration story — harvest-now-decrypt-later
(HNDL), crypto agility, and **hybrid mode** (classical + PQC KEM combined). The existing Week 15
lab (`labs/week15-pqc/`) is a **signature** lab (Lamport OTS key reuse) — it teaches the hash-based
PQC family and one-time-key discipline, but leaves HNDL and hybrid-KEM as lecture-only concepts.
This lab makes the confidentiality half hands-on, filling that gap. It is a **companion to**, not a
replacement for, the Lamport lab.

## Learning objective (one sentence)

Experience *why recording encrypted traffic today is a real threat* — capture a session now, break
its classical KEM "later", decrypt it — and see that a **hybrid** KEM (two independent secrets
combined) keeps the same captured traffic confidential because breaking one half is not enough.

## Shape — the course's standard break → fix pair

Two services, same as every lab in this course (`vulnerable` + `fixed`, Docker Compose, per-student
flag via env, an `exploit.py` that automates the attack, `worksheet.md` with the Conventional +
AIR-Sec arms).

### Vulnerable channel (`:8120`)
- Establishes a session key with a **single classical KEM** whose parameters are deliberately
  breakable — modelling "today's ECDH/RSA that a future quantum computer breaks with Shor".
- Concretely: **RSA-KEM with a small modulus** (~48–64-bit `n`, factorable in seconds with Pollard
  rho / sympy). The server publishes `(n, e)`; a random secret `s` is encapsulated as
  `ct = s^e mod n`; `session_key = HKDF(s)`; then a secret message **containing the flag** is
  sealed with `AES-GCM(session_key)`.
- Endpoint `GET /capture` returns the exact transcript a **passive eavesdropper** would sniff:
  `{n, e, kem_ct, aes_nonce, aes_ct}`. The student harvests this — no live interaction with the
  crypto, which is the whole point of HNDL.
- The **break happens offline, "later"** (in `exploit.py`), not via any server endpoint: factor
  `n` → recover `d` → `s = kem_ct^d mod n` → `session_key = HKDF(s)` → AES-GCM-decrypt → flag.

### Fixed channel (`:8121`) — hybrid
- Same `/capture`, but the transcript carries **two** KEM ciphertexts and
  `session_key = HKDF(s_classical || s_pqc)`. The classical half is the same small-`n` RSA-KEM;
  the **PQC half** is the part the attacker cannot break from the capture.
- Factoring the small classical `n` yields `s_classical` only → `HKDF(s_classical || <unknown>)`
  ≠ the real session key → AES-GCM auth-tag fails → **flag stays confidential**. Running the same
  `exploit.py` against `:8121` visibly fails to decrypt — that is the fix, demonstrated.

## The one real build decision — how to realise the "PQC half"

**Option A (recommended first): real ML-KEM via `kyber-py`.** Pure-Python Kyber/ML-KEM, pip-installable,
no C/liboqs build. If it installs cleanly in `python:3.12-slim` at lab boot (verify during build),
the fixed channel's second half is genuine ML-KEM-512 encapsulation — the most authentic version,
and it lets the worksheet say "hybrid = X25519-style classical ⊕ real ML-KEM" honestly.

**Option B (fallback): teaching-simulation.** If `kyber-py` is flaky, model the PQC half with a
second, **securely-sized** classical KEM (e.g. 2048-bit RSA) that the attacker simply can't factor
in the lab — with an explicit, loud caveat (matching the Lamport lab's "N=32 for speed, lesson
identical" honesty): *"the second half stands in for ML-KEM; we simulate 'quantum-unbreakable-here'
with a large classical modulus purely to keep the lab dependency-light. The structural lesson —
two independent secrets combined so breaking one is insufficient — is identical."*

Decide at build time by actually trying `kyber-py` in the container; fall back to B if it misbehaves.
Either way the attack/fix flow and the worksheet are unchanged.

## Files (mirror `labs/week15-pqc/` conventions)

Directory: **`labs/week15-pqc/hndl/`** (a subfolder of the PQC week, keeping Week 15 cohesive and
its own compose/ports/flag separate from the Lamport lab).
- `README.md` — topic/kind/CWE header (CWE-327 use of a broken/risky crypto algorithm; the HNDL
  threat model), what-to-do, objectives, the honest caveat about parameter sizes / PQC stand-in.
- `vulnerable_app.py` — Flask, small-`n` RSA-KEM, `/capture`, detailed docstring (crypto + the bug),
  `FLAG_HNDL` from env.
- `fixed_app.py` — hybrid KEM `/capture`.
- `exploit.py` — harvest → factor → derive → decrypt against `:8120` (prints the flag); then the
  same against `:8121` and shows it fails.
- `docker-compose.yml` — `vulnerable` on 8120, `fixed` on 8121, `python:3.12-slim`, volume-mounted,
  `pip install -r requirements.txt` at boot, `FLAG_HNDL=${FLAG_HNDL:-FLAG{harvest_now_decrypt_later}}`.
- `requirements.txt` — `flask`, `pycryptodome` (AES-GCM) or `cryptography`; `sympy` (factoring);
  `kyber-py` if Option A.
- `worksheet.md` — Part 1 Conventional (essays: what HNDL is and why migrate *now*; why hybrid
  rather than "just bigger RSA keys"; crypto agility as the engineering lesson) + Part 2 AIR-Sec
  (per-student flag evidence; **Audit-the-AI** on an AI answer that says "to be quantum-safe just
  increase your RSA key size" — the classic wrong fix; EiPE; Prompt Problem; viva prep).

## Flag wiring (matches this course's pattern)

Add key **`hndl`** to `instructor/seed_flags.py`'s `CHALLENGES` list (currently
`hash, macs, aes, aead, sig, pqc`), then run `instructor/check_flag_keys.py` so the drift guard
stays green — same procedure used when the `devsecops` key was added in `software-security`.

## Verification bar (this course's "prove it, don't assert it" rule)

- `docker compose up`, then `exploit.py` against `:8120` recovers the flag end-to-end (harvest →
  factor → decrypt) — real run, output captured.
- The same `exploit.py` against `:8121` **fails** to decrypt (auth-tag failure) — the fix proven,
  not just claimed.
- The small-`n` factoring completes in a few seconds on a laptop (tune `n` size so it's fast but
  not instant-trivial); the large/PQC half is genuinely not recoverable from the capture.

## Explicitly out of scope (v1)

- A live downgrade/negotiation attack (MITM strips the hybrid half) — a natural Week-15b/stretch,
  but v1 stays focused on HNDL + the hybrid fix.
- Real quantum computation (obviously) — the "quantum arrives later" step is modelled by the
  offline classical break, with the caveat stated plainly.
- Any change to the existing Lamport lab.
