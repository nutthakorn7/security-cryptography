---
marp: true
theme: default
paginate: true
header: "Cryptography and Network Security · Week 12"
---

<!-- Delivery: 100-minute lab session. 10 retrieval review + 10 brief + 60 practice + 15 debrief + 5 evidence. Short talk, then the lab (Docker compose files and alice_student.py). Everyone completes the common 60 plus the assigned Conventional 40 or AIR-Sec 20/10/10. The viva is formative, no extra points. -->

# Week 12
## TLS — "encrypted" is not "encrypted to the right person"
Cryptography and Network Security · Nutthakorn Chalaemwongwan

<!-- Hook: ask "if the padlock is green and the address says https, is the connection safe?" Most say yes. Today's answer: it means encrypted, not necessarily encrypted to the party you think you are talking to. -->

---

## Today

- What TLS gives you: **key exchange**, **server authentication**, **CertificateVerify**
- What a **certificate** and a **CA** are, and why anyone can make a certificate
- 🔓 **Lab:** Alice sends a secret. With **no certificate check**, Eve reads it. With a check, she cannot.
- You **fix Alice's code yourself** (3 lines) and test it

<!-- Roadmap. Spine line to say out loud: "the connection really was encrypted, to the wrong party". Most of the class is the lab. -->

---

## Recap — Weeks 10 and 11

- **Week 10:** hybrid encryption, and a nonce must not repeat
- **Week 11:** a valid signature does not mean the same transaction
- **Today:** a valid **encrypted channel** does not mean the **right endpoint**

<!-- Bridge. Same spine all term: a good primitive with a missing check. Today the missing check is who signed the certificate. -->

---

## What a TLS handshake does

- **Key exchange:** both sides agree on a session key (secrecy)
- **Server authentication:** the client checks the server's **certificate** (is this really bob?)
- **`CertificateVerify`:** the server proves it holds the private key for that certificate
- Skip any one of the three and a man in the middle is back

<!-- Worksheet Q3. Write the three jobs on the board. This week's bug lives entirely in job number two: the client never checks whether to believe the certificate. -->

---

## Certificates and CAs

- A certificate is a **claim**: "this public key belongs to `bob`"
- **Anyone** can make a certificate that claims to be `bob`, it costs nothing
- A **CA** (certificate authority) your computer already trusts **signs** the real one, which makes the claim **checkable**
- No signature from a trusted CA ⇒ no chain ⇒ nothing backs the claim

<!-- Worksheet steps 4 to 6 and Q2. Analogy: a passport office or a notary: it does not change what the document says, it changes who is willing to vouch for it. Hostname check (the SAN field, RFC 9525) is a second check on top of the chain. -->

---

## The lab: three characters

| Who | Role | Certificate |
|---|---|---|
| **Alice** | the client, sends `the vault code is 7731` | decides whether to trust |
| **Bob** | the real server | **real**, signed by the demo CA |
| **Eve** (`mitm`) | sits in the middle | **self-signed impostor**, also says `CN=bob` |

- Alice is told to dial Eve's address: an attacker on the network path answers instead of Bob

<!-- Draw the topology. The key line: "Alice's PEER_HOST is literally mitm, not bob". That is the premise of an attacker who controls the network path (DNS spoofing, ARP poisoning, a rogue Wi-Fi). Worksheet step 1. -->

---

## The break: Alice does not check

```
ALICE: TLS handshake succeeded WITHOUT verifying the server cert
MITM INTERCEPTED: the vault code is 7731
```

- The handshake **succeeds**, the data **is** encrypted, but to **Eve**
- **CWE-295** Improper Certificate Validation · **CWE-300** Channel Accessible by Non-Endpoint
- Alice never asks "did someone I trust vouch that this is bob?"

<!-- Worksheet steps 2 and 3 and the first viva question. Ask: "the log says the handshake succeeded, was the traffic encrypted?" Yes. So why did Eve read it? Because she is the other end of that encrypted channel. -->

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

![One impostor certificate, self-signed and claiming CN=bob, is shown to two clients. A validating client checks that the name matches, then finds no chain from the self-signed certificate to the CA it trusts, and aborts before any secret is sent. A client with certificate validation turned off accepts it, completes the handshake and sends the secret to the impostor.](img/cert-validation-bypass.svg)

<!-- Worksheet steps 4 to 6. The reason is "self-signed certificate", not a name mismatch: only the signature chain can catch an impostor that has the right name. -->

```sim
cert-bypass
```

<!-- The sim uses small textbook-RSA numbers (toy, not real TLS) on three scenarios. Run it right after this slide: the default self-signed case, then the "compromised CA" toggle, which shows what this week's lab does NOT cover (a dishonest CA). -->

---

## Your fix: three lines

```python
def build_client_context():
    ca_path = wait_for_ca_cert()
    ctx = ssl.create_default_context(cafile=ca_path)
    return ctx
```

- `create_default_context(cafile=...)` trusts **only** that CA and checks the **chain** and the **name** for you
- Test **both ways**: the impostor must be **rejected** and the real Bob must be **accepted**
- A client that rejects **everything** would also pass the first test

<!-- Worksheet steps 7 to 10. The three lines are shown in alice.py (step 7), so this is a guided edit. The two tests are the point: reject Eve AND accept Bob. The GitHub fork and commit link is a Week 12 submission requirement (see SUBMISSION.md). -->

---

## The real-world version

- `verify=False` (Python `requests`) · `CERT_NONE` (Python `ssl`) · `InsecureSkipVerify` (Go)
- Almost always copied to silence an SSL error: "just make it work"
- **"It's HTTPS, so it's secure"** is true and irrelevant if nobody checked **who** is on the other end
- The right fix for an **internal CA** is to **tell the client to trust that CA**, not to turn checking off

<!-- Direct preview of the AIR-Sec audit (an AI adds verify=False and calls the connection secure). Limits to say once: if a trusted CA is hacked or dishonest, a fake certificate can still chain to it. The lab does not cover that. -->

---

## 🔓 Lab today — what to do

| Mode | Alice checks the certificate? | Eve reads the secret? |
|---|---|---|
| `vulnerable` | **no** | **yes** |
| `fixed` | **yes** | **no** |

- **Everyone (common 60):** A1 Alice does not check · A2 Alice checks · A3 fix `alice_student.py` and test it with Eve and Bob
- **Your form (40):** student ID ends **odd** → Conventional · **even** → AIR-Sec
- **Answer sheet:** Classroom → Week 12 → file for your form → type in the grey boxes → File → Download → PDF
- Hand in `Wk12_<StudentID>.pdf` at `learn.zcr.ai/submit`, **plus the GitHub commit link** of `alice_student.py`

<!-- Exact commands are in the worksheet. Start Docker early and run the build step before class. The GitHub fork and commit link has no marks of its own but is required this week. -->

---

## Takeaway

- Encrypted ≠ talking to the **right party**: only **certificate validation** ties the channel to an identity
- A certificate says "I am bob"; a **trusted CA's signature** is what makes it checkable
- The fix is small (**trust only the right CA, keep the name check**), the cost of skipping it is large
- Next week: **end-to-end encryption** (who can read the message, even the server?)

<!-- Land the spine: "the connection was encrypted, to the wrong party". Cold-call: "name the one property of the real certificate that the impostor lacked." (a signature from a CA we trust). -->
