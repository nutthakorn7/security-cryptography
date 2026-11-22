---
marp: true
theme: default
paginate: true
header: "Cryptography and Network Security · Week 12"
---

<!-- Delivery: 100-minute lab session. 10 retrieval review + 10 brief + 60 practice + 15 debrief + 5 evidence. Short talk, then the lab (Docker compose files and alice_student.py). Everyone completes the common 60 plus the assigned Conventional 40 or AIR-Sec 20/10/10. The viva is formative, no extra points. Logic of the deck: a recap says the pattern is a good primitive with a missing check; the handshake slide names three jobs; the certificate slide shows that the second job needs someone to vouch; the lab shows Alice skipping that job and Eve reading the secret, then Alice doing it and Eve failing; the student writes the fix and tests it both ways; the real-world slide shows the same bug in the wild. Each slide answers one question and ends with the next. -->

# Week 12
## TLS — "encrypted" is not "encrypted to the right person"
Cryptography and Network Security · Nutthakorn Chalaemwongwan

<!-- Hook: ask "if the padlock is green and the address says https, is the connection safe?" Most say yes. Today's answer: it means encrypted, not necessarily encrypted to the party you think you are talking to. Logic: the question on this slide is what "safe" is made of; the next slides split it into encryption and identity. -->

---

## Today

![Three lab steps with one secret. Step 1: Alice does not check the certificate and Eve reads the secret. Step 2: Alice checks the certificate and Eve gets nothing. Step 3: you fix Alice in three lines and test her against Eve and against the real Bob.](img/w12-today.svg)

- What TLS gives you: **key exchange**, **server authentication**, **CertificateVerify**
- What a **certificate** and a **CA** are, and why anyone can make a certificate
- 🔓 **Lab:** Alice sends a secret. With **no certificate check**, Eve reads it. With a check, she cannot.
- You **fix Alice's code yourself** (3 lines) and test it

<!-- Roadmap. Spine line to say out loud: "the connection really was encrypted, to the wrong party". Most of the class is the lab. Logic: the lab has three steps (no check, check, your fix) and the talk gives just enough words (handshake, certificate, CA) to read them. Next question: how does this week connect to the last two? -->

---

## Recap — Weeks 10 and 11

![Week 10: hybrid encryption is good, but a nonce must not repeat. Week 11: a valid signature does not mean it is the same transaction. Week 12, today: a valid encrypted channel does not mean it is the right endpoint. Each week is a good primitive with a missing check.](img/w12-recap.svg)

- **Week 10:** hybrid encryption, and a nonce must not repeat
- **Week 11:** a valid signature does not mean the same transaction
- **Today:** a valid **encrypted channel** does not mean the **right endpoint**

<!-- Bridge. Same spine all term: a good primitive with a missing check. Today the missing check is who signed the certificate. Logic: W10 and W11 each had a primitive that worked and a check the code forgot; TLS is the same story with the certificate as the check. Next question: what exactly does a TLS handshake do, and which job is the check? -->

---

## What a TLS handshake does

![A TLS handshake between Alice, the client, and the server has three jobs. Job 1, key exchange: both sides send key shares and agree on a session key, which gives secrecy. Job 2, the server sends its certificate saying it is bob, and Alice must check who vouches for it; this is where this week's bug lives. Job 3, CertificateVerify: the server signs with its private key to prove it holds the key for that certificate. Skip any one of the three and a man in the middle is back.](img/w12-handshake.svg)

- **Key exchange:** both sides agree on a session key (secrecy)
- **Server authentication:** the client checks the server's **certificate** (is this really bob?)
- **`CertificateVerify`:** the server proves it holds the private key for that certificate
- Skip any one of the three and a man in the middle is back

```
K     = shared(a, B)                        # 1  key exchange: secrecy
ok    = verify(ca_pub, cert, sig)           # 2  is the certificate vouched for?
proof = sign(bob_priv, transcript)          # 3  CertificateVerify: Bob holds the key
```

<!-- Worksheet Q3. Write the three jobs on the board. This week's bug lives entirely in job number two: the client never checks whether to believe the certificate. Logic: job 1 uses the same shared(a, B) as Week 5, so it hides the data from listeners but accepts any partner; job 3 only proves the server holds the key inside the certificate it showed, so it proves nothing if the certificate itself is fake; that leaves job 2, the check on the certificate, as the only thing that ties the key to bob. Next question: what is a certificate, and why can anyone make one? -->

---

## Certificates and CAs

![A certificate is a claim that a public key belongs to bob. The demo CA, which Alice already trusts, signs the real certificate for bob, so the signature can be checked and it is accepted. The impostor certificate also says CN=bob but it is signed by itself, so there is no signature from the CA and no chain, and Alice rejects it. Same name, different issuer.](img/w12-chain.svg)

- A certificate is a **claim**: "this public key belongs to `bob`"
- **Anyone** can make a certificate that claims to be `bob`, it costs nothing
- A **CA** (certificate authority) your computer already trusts **signs** the real one, which makes the claim **checkable**
- No signature from a trusted CA ⇒ no chain ⇒ nothing backs the claim

```
sig = sign(ca_priv, cert)               # the CA vouches for "bob" (as in Week 11)
ok  = verify(ca_pub, cert, sig)         # Alice already holds ca_pub, so she can check
```

<!-- Worksheet steps 4 to 6 and Q2. Analogy: a passport office or a notary: it does not change what the document says, it changes who is willing to vouch for it. Hostname check (the SAN field, RFC 9525) is a second check on top of the chain. Logic: a certificate is just a name plus a public key, so by itself it proves nothing; adding a signature from a party Alice already trusts turns it into something Alice can verify with the Week 11 tool, verify(ca_pub, ...). Next question: what happens in the lab, with an impostor who has the right name but no signature? -->

---

## The lab: three characters

![Three characters. Alice, the client, sends the vault code is 7731 and decides whether to trust. Alice is told to dial Eve, the machine in the middle, who shows a self-signed impostor certificate that also says CN=bob. Bob, the real server with a real certificate signed by the demo CA, is not reached.](img/w12-characters.svg)

| Who | Role | Certificate |
|---|---|---|
| **Alice** | the client, sends `the vault code is 7731` | decides whether to trust |
| **Bob** | the real server | **real**, signed by the demo CA |
| **Eve** (`mitm`) | sits in the middle | **self-signed impostor**, also says `CN=bob` |

- Alice is told to dial Eve's address: an attacker on the network path answers instead of Bob

<!-- Draw the topology. The key line: "Alice's PEER_HOST is literally mitm, not bob". That is the premise of an attacker who controls the network path (DNS spoofing, ARP poisoning, a rogue Wi-Fi). Worksheet step 1. Logic: the lab needs an attacker who answers in Bob's place, so Alice dials Eve; Eve's certificate has the right name but no CA signature, which is exactly the case where only the chain check can tell. Next question: what does Alice do if she does not check? -->

---

## The break: Alice does not check

![Alice has certificate checking turned off, with CERT_NONE and check_hostname set to False. She accepts Eve's certificate, the handshake succeeds and the connection is encrypted, but it is encrypted to Eve. Eve decrypts it and logs the vault code is 7731. Both checks, the chain and the name, were skipped.](img/w12-break.svg)

```
ALICE: TLS handshake succeeded WITHOUT verifying the server cert
MITM INTERCEPTED: the vault code is 7731
```

- The handshake **succeeds**, the data **is** encrypted, but to **Eve**
- **CWE-295** Improper Certificate Validation · **CWE-300** Channel Accessible by Non-Endpoint
- Alice never asks "did someone I trust vouch that this is bob?"

```
K = shared(a, E)               # E = Eve's key share; nobody asked who sent it
p = dec(K, c)                  # Eve decrypts the secret: "the vault code is 7731"
```

<!-- Worksheet steps 2 and 3 and the first viva question. Ask: "the log says the handshake succeeded, was the traffic encrypted?" Yes. So why did Eve read it? Because she is the other end of that encrypted channel. Logic: with checking off, the key exchange runs with whoever answered, so the session key K is shared with Eve and she can decrypt. Encryption did its job; the missing job was identity. Next question: what changes if Alice does the check? -->

---

## The fix: check the certificate

```
CERT VERIFICATION FAILED - ABORTING
ALICE: (reason: self-signed certificate)
MITM: handshake aborted by client, intercepted NOTHING
```

- Eve's code is **unchanged**. Only **Alice** changed: she trusts only the **demo CA**
- Eve's certificate has the right **name**, but **no CA signed it**, so it fails
- Alice stops **before** sending the secret

```
ok = chain(cert, ca) and name(cert) == "bob"      # Eve: name ok, chain missing ⇒ False
```

![What the validating Alice does with Eve's certificate. The impostor certificate claims CN=bob but is signed by itself. Check 1, the name, matches bob and passes. Check 2, the chain to the demo CA she trusts, does not exist, so it fails. Alice aborts the handshake before any secret is sent, and Eve intercepts nothing.](img/w12-fix-check.svg)

<!-- Worksheet steps 4 to 6. The reason is "self-signed certificate", not a name mismatch: only the signature chain can catch an impostor that has the right name. Logic: the name check passes (Eve wrote CN=bob), so the only check that can fail is the chain; the failure happens inside the handshake, before Alice's sendall, so no secret leaves. Next question: how do we write this check in the code, and how do we know it is right? -->

```sim
cert-bypass
```

<!-- The sim uses small textbook-RSA numbers (toy, not real TLS) on three scenarios. Run it right after this slide: the default self-signed case, then the "compromised CA" toggle, which shows what this week's lab does NOT cover (a dishonest CA). -->

---

## Your fix: three lines

![Two tests for the fixed Alice. Test 1: Alice dials Eve and must reject, printing CERT VERIFICATION FAILED and exiting with 1, so no secret is sent. Test 2: Alice dials the real Bob with PEER_HOST=bob and must accept, so the handshake succeeds and Bob receives the secret. A client that rejects everything would pass test 1 but fail test 2.](img/w12-two-tests.svg)

```python
def build_client_context():
    ca_path = wait_for_ca_cert()
    ctx = ssl.create_default_context(cafile=ca_path)
    return ctx
```

- `create_default_context(cafile=...)` trusts **only** that CA and checks the **chain** and the **name** for you
- Test **both ways**: the impostor must be **rejected** and the real Bob must be **accepted**
- A client that rejects **everything** would also pass the first test

```
Alice(Eve's cert) = reject        # test 1: no secret sent
Alice(Bob's cert) = accept        # test 2: the secret reaches Bob
```

<!-- Worksheet steps 7 to 10. The three lines are shown in alice.py (step 7), so this is a guided edit. The two tests are the point: reject Eve AND accept Bob. The GitHub fork and commit link is a Week 12 submission requirement (see SUBMISSION.md). Logic: a fix is only proven by a test that can fail both ways; rejecting Eve shows the check exists, accepting Bob shows it is not a blanket refusal. Next question: where does this bug show up outside the lab? -->

---

## The real-world version

![The quick fix that gets copied everywhere turns checking off: verify=False in Python requests, CERT_NONE in Python ssl, InsecureSkipVerify in Go. Then every certificate is accepted. The right fix for an internal CA is to tell the client to trust that CA, so only certificates signed by it are accepted and the name is still checked.](img/w12-real-world.svg)

- `verify=False` (Python `requests`) · `CERT_NONE` (Python `ssl`) · `InsecureSkipVerify` (Go)
- Almost always copied to silence an SSL error: "just make it work"
- **"It's HTTPS, so it's secure"** is true and irrelevant if nobody checked **who** is on the other end
- The right fix for an **internal CA** is to **tell the client to trust that CA**, not to turn checking off

<!-- Direct preview of the AIR-Sec audit (an AI adds verify=False and calls the connection secure). Limits to say once: if a trusted CA is hacked or dishonest, a fake certificate can still chain to it. The lab does not cover that. Logic: an SSL error usually means the check is working and the CA is not trusted yet; turning the check off removes the symptom and the protection, while adding the CA to the trust list removes only the symptom. Next question: what do we keep from today? -->

---

## 🔓 Lab today — what to do

![Today's lab flow in three steps, then your form. A1: run Alice with the vulnerable compose file and Eve reads the secret. A2: run Alice with the fixed compose file and Eve gets nothing. A3: fix alice_student.py and run the student-task compose file; Eve is rejected and Bob is accepted. Then do the 40 points of your form: student ID ends odd is Conventional, even is AIR-Sec. Hand in Wk12 student ID PDF at learn.zcr.ai/submit plus the GitHub commit link of alice_student.py.](img/w12-lab-flow.svg)

| Mode | Alice checks the certificate? | Eve reads the secret? |
|---|---|---|
| `vulnerable` | **no** | **yes** |
| `fixed` | **yes** | **no** |

- **Everyone (common 60):** A1 Alice does not check · A2 Alice checks · A3 fix `alice_student.py` and test it with Eve and Bob
- **Your form (40):** student ID ends **odd** → Conventional · **even** → AIR-Sec
- **Answer sheet:** Classroom → Week 12 → file for your form → type in the grey boxes → File → Download → PDF
- Hand in `Wk12_<StudentID>.pdf` at `learn.zcr.ai/submit`, **plus the GitHub commit link** of `alice_student.py`

<!-- Exact commands are in the worksheet. Start Docker early and run the build step before class. The GitHub fork and commit link has no marks of its own but is required this week. Logic: the three steps run in the order of the talk (break, check, fix), and the picture is the map for the 60 minutes; the form (40) comes after the common 60. -->

---

## Takeaway

![Encrypted plus a certificate check equals encrypted to the right party. The encrypted channel keeps listeners out but does not say who is on the other end. Certificate validation, a signature from a CA we trust and a matching name, ties the channel to an identity. Eve had the first part only.](img/w12-takeaway.svg)

- Encrypted ≠ talking to the **right party**: only **certificate validation** ties the channel to an identity
- A certificate says "I am bob"; a **trusted CA's signature** is what makes it checkable
- The fix is small (**trust only the right CA, keep the name check**), the cost of skipping it is large
- Next week: **end-to-end encryption** (who can read the message, even the server?)

<!-- Land the spine: "the connection was encrypted, to the wrong party". Cold-call: "name the one property of the real certificate that the impostor lacked." (a signature from a CA we trust). Logic: encryption answers "who can listen", the certificate check answers "who is on the other end"; both are needed. Next question for next week: even with the right server, can the server itself read the message? -->
