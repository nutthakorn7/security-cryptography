---
marp: true
theme: default
paginate: true
header: "Security & Cryptography · Week 14"
---

# Week 14
## User Authentication (challenge-response, PAKE, MFA)
Security & Cryptography · Nutthakorn Chalaemwongwan

<!-- Hook: ask "when you type your password into a login form, who actually sees it?" Most students say "nobody, it's HTTPS." Wrong — the server does, in the clear, inside a request handler. Today's spine: the challenge-response math is textbook-sound; "just send the password over TLS" is the real-system failure baked into almost every login form on earth. ~2 min. -->

---

## Today

- Why sending a password to the server is a risk — **even over TLS**
- Challenge-response: proving you know a secret without saying it
- PAKE (SRP, OPAQUE) and what our demo does *not* give you
- Auth factors, TOTP vs FIDO2, credential stuffing, SSO/OAuth
- 🗝️ Game: **Never Say the Password**

<!-- Roadmap, 1 min. Flag the lab up front: run the same login demo in vulnerable and fixed mode, grep your own server logs for the password in each. Also flag this is a HYBRID week — half runnable demo, half conceptual essays (TOTP/FIDO2/SSO). ~1 min. -->

---

## Recap — Week 13

- E2E encryption: the **server** can't read message content, only the endpoints can
- Same server, same log line — plaintext vs. ciphertext, purely by *where* encryption happens
- This week: same question, different secret — can the server even avoid **learning your password**?

<!-- Bridge from W13. W13 = protect message *content* from the server operator. W14 = protect a *credential* from the server operator. Same underlying move: shrink what the "trusted" server structurally holds. Ask: "if E2EE keeps your messages from the server, why does almost every login form just... hand the server your password?" ~3 min. -->

---

## The premise: TLS protects the wire, not the endpoint

- TLS encrypts the **network path** between client and server
- The server **terminates** TLS — it decrypts the request and sees it in the clear
- "Log in by sending your password" hands the **plaintext** to the server itself
- A malicious, compromised, or merely over-logging server has it — TLS never touches this

<!-- The core misconception to kill. Draw it: client --[TLS: encrypted]--> server --[decrypts]--> plaintext in a Python dict. TLS solved the eavesdropper-on-the-wire problem decades ago; it says nothing about what the server *does* with the plaintext once it has it. This is the textbook-secure/real-system-failure split for this week: TLS is textbook-sound crypto; "send the password to the endpoint" is the real-system misuse. ~5 min. -->

---

## Worked example: vulnerable mode

```
POST /login {"username":"alice","password":"correct-horse-battery"}
```

```
week14-server  | SERVER SAW PASSWORD: correct-horse-battery
week14-client  | LOGIN OK
```

- The plaintext password is now **in the server's request handler** — CWE-522 / CWE-319
- One `log.info(...)` line away from sitting in application logs — CWE-532
- Login still "works" — that's what makes this easy to ship and easy to miss

<!-- This is the exact `docker-compose.vulnerable.yml` output from the lab — point at the literal log line they'll capture. Ask: "TLS was doing its job here — so why did the password still leak?" Answer: it leaked *after* TLS did its job, at the endpoint. ~5 min. -->

---

## The fix: challenge-response, in three steps

1. Server sends a fresh random **nonce** (never reused)
2. Client combines `nonce + password` **locally** → a **proof**
3. Server checks the proof against a stored **verifier** — never against the password

> The server doesn't ask "what's your password?" — it asks "prove you know it."

<!-- Draw the three-step exchange on the board. Emphasize "locally" in step 2 — the combination happens on the client, the password never leaves the machine that typed it. This is the shape every "prove knowledge of a secret without revealing it" protocol uses. ~5 min. -->

---

## How verification works without the plaintext

- Server stores a **verifier** `v = KDF(salt, password)` — computed once, at signup, never the password itself
- Client computes `proof = HMAC(v, nonce)` locally, using the password it just typed
- Server independently recomputes the same proof from its stored `v` and the nonce it issued, and **compares**
- Match → `LOGIN OK`. The password never crossed the network, so there was nothing to log

<!-- Walk the symmetry: both sides end up computing the same HMAC, but only the client ever touches the raw password. The server's "knowledge" is entirely mediated through v. Ask: "if an attacker steals the server's database and gets v, can they log in as alice directly?" (YES, trivially — in THIS demo v is password-equivalent: the thief just requests a fresh nonce and computes HMAC(v, nonce), authenticating without ever cracking the password. The fresh nonce only stops replay by someone who does NOT hold v. Verifier-theft resistance is exactly what a real PAKE — SRP/OPAQUE — adds and this demo deliberately lacks; foreshadow next slide's honest limits.) ~6 min. -->

---

## Worked example: fixed mode

```
GET /challenge -> nonce=327decae...
POST /login {"username":"alice","nonce":"327decae...","proof":"40e70117..."}
```

```
week14-server  | SERVER SAW: nonce=327decaec7e5... proof=40e701177990...
week14-client  | LOGIN OK
```

```bash
docker compose -f docker-compose.fixed.yml logs | grep -c "correct-horse-battery"   # -> 0
```

- Same successful login, same demo account — the password string appears **nowhere**

<!-- The payoff slide — same LOGIN OK, completely different log content. Have them literally run the grep in lab and watch it return 0. This absence *is* the evidence, not a screenshot of something present. ~4 min. -->

---

## Honest scope — this is NOT a full PAKE

This demo proves exactly **one** property: *the password is never transmitted.*

A real PAKE (SRP, OPAQUE) also gives you two more:

1. **Offline-dictionary resistance** on the stored verifier — ours is fast salted SHA-256; a DB leak lets an attacker brute-force weak passwords offline
2. **Mutual authentication** — the client also verifies *the server*, so it can't be tricked into proving its password to an impostor

<!-- Guardrail slide — do not let students walk away thinking they built SRP/OPAQUE. Tie property 1 back to Week 2 (bcrypt/argon2, high work factor) — a real system's verifier KDF must be slow, not a bare SHA-256. Property 2 previews SSO/phishing later in this deck. This is also Worksheet Q4 and Part 2b. ~4 min. -->

---

## Audit the AI — a "professional-looking" login handler

```python
log.info("login attempt: %s", body)                                   # (A)
...
log.warning("login FAILED for %s (pw=%s)", body["username"],
            body["password"])                                         # (B)
```

- `bcrypt.checkpw(...)` against the stored hash is **correct**
- But `(A)` logs the **full request body**, `(B)` logs the **raw password** — CWE-532
- The bcrypt hash was never the leak. The **log file** is.

<!-- Mirrors the model's "worked example: what each tool catches" — same idea, a plausible AI-generated snippet with a planted flaw. Ask: "who can read production logs?" (log-aggregation SaaS, on-call engineers, anyone who breaches the log store). This is Worksheet Part 2b — point them at it directly, and ask them to name what place the credential reaches in Part 2a-vulnerable vs. here (answer: the log file, in both cases). ~5 min. -->

---

## Authentication factors

| Factor | Example | Weakness |
|---|---|---|
| **Know** | password, PIN | phishable, reusable, guessable |
| **Have** | phone, FIDO2 key | can be lost/stolen; SIM-swap for SMS |
| **Are** | fingerprint, face | can't be rotated if compromised |

- **MFA** = combine factors from *different* rows — not two passwords

<!-- Standard NIST 800-63B taxonomy. Ask for one example + one weakness of each before revealing the table. Stress: two "know" factors (password + security question) is not MFA — it's one factor asked twice. ~5 min. -->

---

## TOTP vs FIDO2/WebAuthn

- **TOTP** (authenticator app): a shared secret + current time → a 6-digit code you **type**
  - Phishable — a fake login page can relay your code to the real site in real time
- **FIDO2/WebAuthn**: a private key on your device signs a challenge **bound to the origin**
  - Not phishable — the signature is invalid for any domain but the real one

<!-- Key contrast: what the user types vs. what the authenticator does, and what each is bound to. TOTP is bound to nothing — you can paste that 6-digit code into any site that asks. FIDO2 is cryptographically bound to the origin, so a phishing clone at a lookalike domain gets a signature that simply doesn't verify. This is Worksheet Q5. ~5 min. -->

---

## Credential stuffing

- Attacker takes passwords leaked from **breach A**, tries them against **site B**
- Works because people **reuse** passwords across sites
- Best single mitigation: **MFA** — a correct, reused password alone no longer logs the attacker in

<!-- Worksheet Q6. Ask "why does reusing your own login as the mitigation still help even when the leaked password really is correct for that account?" — because credential stuffing is *automated, password-only* login; add any second factor and the automation breaks even with a 100% correct password. ~3 min. -->

---

## Delegated authentication: SSO / OAuth

- User authenticates once with an **identity provider** (Google, institutional SSO…)
- Relying apps never see the password at all — only a token
- Fewer passwords to phish or reuse — but the IdP becomes a **single point of failure**

<!-- Worksheet Q8. The IdP is now the one account that, if compromised, unlocks everything federated to it — "don't put all your eggs in one basket" cuts both ways. Connect back to mutual authentication from the honest-scope slide: SSO buys you a lot, but concentrates trust. ~4 min. -->

---

## 🗝️ Signature game — Never Say the Password

- Play server operator: run **vulnerable mode**, watch your own log hand you the plaintext password
- Flip to **challenge-response mode**, log in successfully, then **grep your own logs** for the password and find nothing
- Proving you know a secret without ever saying it out loud — the same trick every "Sign in with…" button quietly relies on

<!-- Explain the game before lab: it's not a CTF flag hunt, it's watch-it-happen-yourself. The "win" is the grep returning 0 after a successful login. Emphasize this is *their own* log, on *their own* machine — nobody's trusting a slide, they're trusting their own terminal. ~3 min. -->

---

## Lab today

> 📋 **Worksheet 14** — `labs/week14-authentication/worksheet.md` · run: `docker compose -f docker-compose.vulnerable.yml up --build --abort-on-container-exit`, then the `.fixed.yml` variant

- Capture both logs: the `SERVER SAW PASSWORD` line (vuln) and its **absence** + `grep -c 0` (fixed)
- **Audit the AI** on the planted logging flaw (Part 2b)
- **EiPE**: explain proof-without-revealing in plain English (Part 2c)
- **Prompt Problem** + **viva prep** (Part 2d–e) — plus 8 conventional essay questions (Part 1)

<!-- The graded output for this HYBRID week. Remind: this is a read/run/observe lab, not an exploit-and-fix lab — code is unchanged, evidence is captured logs + identity proof. Point to the "Honest scope" box in the README before they write Part 2c/2d so they don't overclaim PAKE properties this demo doesn't have. -->

---

## Key takeaways

- TLS protects the **wire**; it says nothing about what the **endpoint** does with your plaintext
- Challenge-response proves knowledge of a secret without ever transmitting it
- "Textbook-secure primitive, real-system failure": challenge-response math is sound — "just use HTTPS and send the password" is the real-system misuse

<!-- Recap, 3 lines. Cold-call: "your friend says their login is secure because the login page uses HTTPS — what's missing from that claim?" ~3 min. -->

---

# Questions?
Next week: Post-Quantum Cryptography

<!-- Cliffhanger: "the public-key math we've leaned on all semester — RSA, Diffie-Hellman — assumes a certain kind of problem is hard. Next week we ask what happens when a quantum computer makes that assumption false. (Note: our hash-based verifiers today SURVIVE — Grover only halves symmetric/hash strength; it's the public-key primitives that break.)" Remind: Docker stacks ready for both compose files before lab starts. -->
