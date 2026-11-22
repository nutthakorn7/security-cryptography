---
marp: true
theme: default
paginate: true
header: "Cryptography and Network Security · Week 14"
---

<!-- Delivery: 100-minute lab session. 10 Week 13 retrieval quiz + 10 brief + 60 practice + 15 debrief + 5 evidence. Short talk, then the lab (docker compose, two modes). The scored Week 14 quiz opens Week 15. Everyone completes the common 60 plus the assigned Conventional 40 or AIR-Sec 20/10/10. The viva is formative, no extra points. -->

# Week 14
## User authentication — the server sees your password (unless it can't)
Cryptography and Network Security · Nutthakorn Chalaemwongwan

<!-- Hook: ask "when you type your password into a login form, who actually sees it?" TLS protects the path, but the receiving server handles the plaintext. Password submission over TLS is a common, legitimate design when the server handles credentials safely; the deliberate logging in this lab is the flaw. Logic of the deck: TLS hides the password on the wire, but the server ends TLS and sees it; the plain login shows that in a log line; a challenge-response login sends a proof instead of the password; the honest-scope slide says what that still does not give; the lab lets everyone see both. Each slide answers one question and ends with the question the next slide answers. -->

---

## Today

![Today in order: who sees the password even over TLS, what the plain login logs, a challenge-response login that sends a proof, what the demo does not give you, and then the lab where you watch both modes.](img/w14-roadmap.svg)

- A **10-minute quiz** on Week 13 to start (one question at a time)
- Why sending a password to the server is a risk — **even over TLS**
- Challenge-response: proving you know a secret without sending it
- What our demo does **not** give you (it is not a real PAKE)
- 🔓 **Lab:** watch the server log your password, then log in without sending it

**Timing (100 min):** 10 quiz · 10 brief · 60 lab · 15 feedback · 5 save evidence

<!-- Roadmap. Spine line to say out loud: "the math is fine; the way it was used is not". Most of the class is the lab. This is a hybrid week: the lab is the runnable part; TOTP/FIDO2 are discussed on paper (worksheet Q4, optional Q5-Q8). Logic: the questions run in order: who sees the password (TLS premise), what does that look like (plain login), what can we send instead (challenge-response), is that enough (honest scope), then the lab. -->

---

## Recap — Week 13

![Week 13: the client encrypts the message, so the server stores only ciphertext and cannot read it. Week 14: the client sends the password itself, so the server receives the secret and can read it. Today the question is whether the server can avoid learning the password.](img/w14-recap.svg)

- E2EE moved encryption to the **endpoints**: the server stored only ciphertext
- Same server, same log line — readable or unreadable depending on **where** encryption happens
- This week: same question, different secret — can the server avoid **learning your password**?

```
W13:  c = E(k, m)           # the server stores c and cannot read m
W14:  request = password    # the server receives the secret itself
```

<!-- Bridge from W13. W13 = protect message content from the server operator. W14 = protect a credential from the server operator. Ask: "if E2EE keeps your messages from the server, why does almost every login form hand the server your password?" Logic: W13 moved the key to the endpoints so the server only held ciphertext; a login cannot do that in the same way, because the server must be able to check the password. Next question: if the connection is encrypted with TLS, who still sees the password? -->

---

## The premise: TLS protects the wire, not the endpoint

![The client sends the password through a TLS tunnel. A listener on the wire sees only ciphertext. But the TLS connection ends at the server, so the server decrypts the request and its handler reads the plaintext password and could log, store, forward or leak it.](img/w14-tls-endpoint.svg)

- TLS encrypts the **network path** between client and server
- The server **terminates** TLS — it decrypts the request and sees it in the clear
- "Log in by sending your password" hands the **plaintext** to the server itself
- A malicious, compromised or merely over-logging server has it — TLS never touches this

```
wire:    c = TLS_enc(key, request)     # a listener sees only c
server:  request = TLS_dec(key, c)     # TLS ends here, so the password is readable
```

<!-- Draw the boundary: TLS protects the network path; the server decrypts the request and can process its contents. The failure in this lab is logging the plaintext password, not ordinary password submission over TLS. Worksheet Steps 1 and 3 and Conventional Q1. Logic: the session key is known to both ends of the TLS connection, so the server can always decrypt; the protection is against the people in between, not against the receiver. Next question: what does that look like in a real log? -->

---

## Worked example: the plain login

![The client posts the actual password to the login handler. The handler prints it, so the server log contains the line SERVER SAW PASSWORD followed by the password. The login still succeeds, so nobody notices the leak. The flaw is CWE-532 and CWE-522.](img/w14-plain-login.svg)

```
POST /login {"username":"alice","password":"correct-horse-battery"}
```

```
week14-server  | SERVER SAW PASSWORD: correct-horse-battery
week14-client  | LOGIN OK
```

- The plaintext password reaches the **server's request handler** by design
- The deliberate log line exposes it — **CWE-532** (and insufficient credential protection, **CWE-522**)
- Login still "works" — that is what makes this easy to ship and easy to miss

```
log("SERVER SAW PASSWORD: " + password)    # the flaw: the secret goes to the log
ok = KDF(salt, password) == v_stored      # the check itself is fine
```

<!-- This is the exact output of the lab's first mode (worksheet Step 2): point at the literal line they will copy. The lab uses HTTP only inside Docker. Hypothetical TLS would protect the path, but the server would still receive plaintext after terminating it. CWE-319 describes unencrypted transport, not this endpoint exposure. Logic: the server must compute something from the password to check it, so the plaintext is in its memory by design; the flaw is the line that copies it to the log. Next question: can the client prove it knows the password without sending it? -->

---

## Challenge-response in three steps

![Step 1: the server sends a fresh random nonce and the public salt. Step 2: on its own computer the client derives the verifier from the salt and password, computes the proof as an HMAC of the nonce under the verifier, and sends the nonce and proof, never the password. Step 3: the server recomputes the HMAC from its stored verifier and compares; if equal the login is OK.](img/w14-challenge-response.svg)

1. Server sends a fresh random **nonce** (never reused)
2. Client combines the nonce with the password **on its own computer** → a **proof**
3. Server checks the proof against a stored **verifier** — never against the password

> The server asks for a fresh proof each time. In this toy protocol, a thief who holds the stored verifier can answer too.

```
v     = KDF(salt, password)               # client, locally; the server stored the same v
proof = HMAC(v, nonce)                    # client sends (nonce, proof)
proof == HMAC(v_stored, nonce) ?          # server checks: yes means LOGIN OK
```

<!-- Draw the three-step exchange on the board (worksheet Step 4). Emphasise "on its own computer" in step 2: the login request carries no password. The server holds v = KDF(salt, password), preloaded in this demo (there is no signup flow); client computes proof = HMAC(v, nonce) and the server recomputes the same proof and compares. This proves possession of the verifier or the ability to derive it, not password-only knowledge against verifier theft. Ask: "if an attacker steals v, can they log in as alice?" (YES, in this demo v is password-equivalent). Logic: HMAC(v, nonce) can only be computed by someone who has v, and the nonce is fresh, so an old proof is useless; the server never needs the password, only v. Next question: who sees what in each mode, side by side? -->

---

## Who sees the secret?

![Two lanes compare password logging with a fixed-mode nonce and proof exchange. The fixed-mode server log omits the plaintext password, but a stolen verifier permits impersonation and a known-salt transcript permits offline guessing.](img/log-boundary.svg)

```sim
cred-harvest
```

<!-- The sim runs REAL SHA-256 and HMAC-SHA256 in the browser, not a toy hash. The three login scenarios and their reused-password second accounts are invented framing, not literal lab code. Run it live right here: flip Mode from plain to challenge-response on one preset and read the log line change, then click "Replay the captured request" in fixed mode to show the single-use nonce rejecting its own captured request. The offline-guess panel previews the honest-scope slide: do not over-explain it yet. Logic: this puts the two modes next to each other so students see where the secret ends up in each; the dashed warning box is the bridge to the limits slides. Next question: what does the fixed-mode login look like in the real lab? -->

---

## Worked example: the challenge-response login

![The plain request carries the username and the password, and the server log prints the password. The challenge-response request carries the username, a nonce and a proof and no password, and the server log prints only the nonce and proof. Both end with LOGIN OK.](img/w14-two-requests.svg)

```
GET /challenge?username=alice -> nonce=cafdff0d..., salt=...
POST /login {"username":"alice","nonce":"cafdff0d...","proof":"e2c3481f..."}
```

```
week14-server  | SERVER SAW: nonce=cafdff0da9a1... proof=e2c3481fe4a6...
week14-client  | LOGIN OK
```

- Same successful login, same demo account — no password string in the **server log**
- Step 7: the two request lines in `client.py` show what each mode sends

<!-- The payoff slide (worksheet Steps 5 and 7): same LOGIN OK, different log content. Students look through the server lines for the password and then run the grep over client.py. A log with no password is limited evidence: it cannot prove what crossed the network, which is why they inspect the request code. Commands work in PowerShell and Mac Terminal. Logic: the result is the same LOGIN OK, so only the request content shows the difference; that is why the lab ends with reading client.py. Next question: is this a complete answer to the password problem? -->

---

## Honest scope — this is NOT a full PAKE

![Three limits of the toy protocol. A stolen verifier lets a thief make a correct proof and log in. A recorded nonce and proof plus the public salt let an attacker test password guesses offline. The client never checks the server, so there is no mutual authentication. A real PAKE adds a mutually authenticated key exchange and resistance to offline guessing from transcripts.](img/w14-honest-scope.svg)

This demo shows one property: *its login request omits the password.*

- A **stolen verifier** works like a password (impersonation)
- A recorded nonce and proof plus the known salt allow **offline guessing**
- The client never checks the server (no mutual authentication)

A real PAKE adds a **mutually authenticated key exchange** and resistance to offline guessing from **transcripts**. Even **OPAQUE** does not stop guesses after full server compromise: it prevents pre-computation. [RFC 9807, Sections 1 and 10.11](https://www.rfc-editor.org/rfc/rfc9807.html#section-10.11)

```
proof == HMAC(KDF(salt, guess), nonce) ?     # offline test of one guess, from a recorded (nonce, proof)
```

<!-- Worksheet Steps 9 and 10 and Conventional Q3. Compare the toy protocol's password-equivalent verifier and known-salt transcript attack with PAKE transcript security. Keep transcript, credential-file and full-server compromise distinct. Do not present this toy as SRP/OPAQUE, a production login design or phishing-resistant WebAuthn. Logic (equation): the attacker knows the public salt, the nonce and the proof, so each guess costs one KDF and one HMAC and needs no contact with the server; the fast SHA-256 in this demo makes that cheap. Next question: what if the leak is not the protocol but the code around it? -->

---

## Audit the AI — a "professional-looking" login handler

![The login handler checks the password correctly with bcrypt, which is fine. But line A logs the whole request body and line B logs the raw password, so the credential reaches the log file. People who can read the log, such as a log service, an engineer on call, or anyone who breaches the log store, can read it. The bcrypt hash was never the leak; the log file is.](img/w14-audit-log.svg)

```python
log.info("login attempt: %s", body)                                   # (A)
...
log.warning("login FAILED for %s (pw=%s)", body["username"],
            body["password"])                                         # (B)
```

- `bcrypt.checkpw(...)` against the stored hash is **correct**
- But (A) logs the **whole request body** and (B) logs the **raw password** — CWE-532
- The bcrypt hash was never the leak. The **log file** is.

<!-- This is worksheet Part 3 (AIR-Sec). A plausible AI snippet with a planted flaw. Ask: "who can read production logs?" (log services, engineers on call, anyone who breaches the log store). Ask them to name the place the credential reaches in the lab's first mode and here (answer: the log, in both cases). Do not "fix" the exhibit on the slide. Logic: a correct check does not make the whole handler safe, because the secret can leave through any side channel the code writes to; follow the password through every line, not only the one that compares it. Next question: what do real systems use besides passwords? -->

---

## TOTP vs FIDO2 / WebAuthn

![TOTP: your authenticator app makes a six-digit code from a shared secret and the time, you type it, and a fake login page can relay it to the real site, because the code is bound to nothing. FIDO2 or WebAuthn: a private key on your device signs a challenge together with the site origin, so a signature made for a fake domain does not verify on the real site.](img/w14-totp-fido.svg)

- **TOTP** (authenticator app): a shared secret + the current time → a 6-digit code you **type**
  - Phishable — a fake login page can relay your code to the real site in real time
- **FIDO2 / WebAuthn**: a private key on your device signs a challenge **bound to the real site (origin)**
  - Resists lookalike-site phishing: a signature for the fake domain will not verify on the real site

```
code = TOTP(secret, time)                 # bound to nothing: a fake page can relay it
sig  = sign(sk, challenge, origin)        # bound to the site origin it was made for
```

<!-- Worksheet Conventional Q4. Key contrast: what the user types versus what the authenticator does, and what each is bound to. TOTP is bound to nothing: you can paste that code into any site that asks. Optional (no marks) Q5-Q8 cover the three factors, credential stuffing and MFA, password storage with a slow salted hash, and SSO/OIDC; use them for early finishers. Logic: the question is what each proof is bound to; a code you type can be used anywhere, a signature over the origin is only valid for that origin. Next question: back to the lab: what exactly do we do today? -->

---

## 🔓 Lab today — what to do

![Three lab steps. A1: start the vulnerable compose file and read the server log, which shows the password. A2: start the fixed compose file and read the server log, which shows only a nonce and a proof, and the client prints LOGIN OK. A3: find the two request lines in client.py and name the limits. Then hand in Wk14 student ID PDF at learn.zcr.ai/submit by Sunday 7 February 23:59. Student ID ends odd: Conventional; ends even: AIR-Sec.](img/w14-lab-flow.svg)

| Mode | Login request contains | Server log |
|---|---|---|
| `vulnerable` | the **password** | `SERVER SAW PASSWORD: ...` |
| `fixed` | a **nonce** and a **proof** | `SERVER SAW: nonce=... proof=...` |

- **Everyone (common 60):** A1 watch the server log your password · A2 log in without sending it · A3 find the two request lines and name the limits
- **Your form (40):** student ID ends **odd** → Conventional · **even** → AIR-Sec
- **Answer sheet:** Classroom → Week 14 → file for your form → type in the grey boxes → File → Download → PDF
- Hand in `Wk14_<StudentID>.pdf` at `learn.zcr.ai/submit` by **Sun 7 Feb, 23:59**

<!-- Exact commands are in the worksheet (11 steps). Start Docker early and run the build step before class. The password is a lab constant, the same for everyone; nonce and proof are random per run. Both modes share one project, so one down at the end (Step 11) removes everything. Logic: the three steps check the slides. A1: the plain login puts the password in the server log. A2: the challenge-response login puts only a nonce and a proof there, and still gives LOGIN OK. A3: the request lines in client.py show why, and the limits show what the demo does not prove. -->

---

## Key takeaways

![TLS protects the wire from listeners. The endpoint, the server, still sees whatever you send, including a password. Challenge-response sends a proof instead of the password, but in this toy a stolen verifier still works. HTTPS does not mean the server cannot see your password.](img/w14-takeaway.svg)

- TLS protects the **wire**; it says nothing about what the **endpoint** does with your plaintext
- This toy sends no password in the login request, but accepts anyone who holds its verifier
- Password submission over TLS can be fine — if the server protects the credential and never logs it
- Next week: **post-quantum cryptography**

```
request = password           # the server reads it, even over TLS
request = (nonce, proof)     # no password sent; a stolen v still works in this toy
```

<!-- Recap in four lines. Cold-call: "a friend says their login is secure because the page uses HTTPS: what is missing from that claim?" Cliffhanger for Week 15: the public-key maths we have used all semester (RSA, Diffie-Hellman) assumes certain problems are hard; what happens if a quantum computer breaks that assumption? Hash-based verifiers survive: Grover only halves symmetric and hash strength. Remind: Docker and laptop ready for next week too. Logic: the deck went from where the password is exposed (the endpoint), to a way to send a proof instead, to the limits of that proof; the next deck asks what happens to the public-key maths when a quantum computer arrives. -->
