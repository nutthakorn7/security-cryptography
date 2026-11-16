---
marp: true
theme: default
paginate: true
header: "Cryptography and Network Security · Week 13"
---

<!-- Delivery: 100-minute lab session. 10 retrieval review + 10 brief + 60 practice + 15 debrief + 5 evidence. Short talk, then the lab (docker compose, two modes). The scored Week 13 quiz opens Week 14. Everyone completes the common 60 plus the assigned Conventional 40 or AIR-Sec 20/10/10. The viva is formative, no extra points. -->

# Week 13
## End-to-end encryption — HTTPS is not enough
Cryptography and Network Security · Nutthakorn Chalaemwongwan

<!-- Hook: ask "your chat app uses HTTPS. Can the company still read your messages?" Most say no. Today's answer: yes, unless the app is end-to-end encrypted. -->

---

## Today

- Two different promises: **transport encryption** (HTTPS) and **end-to-end** encryption
- Why the **server** can still read everything when only HTTPS is used
- 🔓 **Lab:** see the server's own log in both cases
- What the lab **does not** prove (whose key is it?), and how Signal helps

<!-- Roadmap. Spine line to say out loud: "HTTPS protects the road, not the destination". Most of the class is the lab. -->

---

## Recap — Weeks 10 to 12

- **Week 10:** hybrid encryption (a public key locks an AES key)
- **Week 12:** TLS, and a client must check the certificate
- **Today:** TLS ends **at the server**, so who else can read?

<!-- Bridge. Week 10 gives the tool (encrypt to a public key), Week 12 gives the transport, today puts them together in a real messaging shape. -->

---

## Two different guarantees

| | **HTTPS / TLS** | **End-to-end (E2EE)** |
|---|---|---|
| Protects against | someone on the network | the network **and the provider** |
| Where it ends | at the **server** | at the **recipient's device** |
| Server sees | readable messages | only **ciphertext** |

- The padlock means "encrypted **to the server**", not "private from the server"

<!-- Worksheet Q1 and steps 1 to 3. The server terminates TLS: it decrypts, stores and can log the message. -->

---

## The break: the server reads everything

```
week13-server | SERVER SAW: meet at pier 39 at midnight
week13-bob    | BOB RECEIVED: meet at pier 39 at midnight
```

- Alice sends **readable** text, the server stores and logs it
- **CWE-311** Missing Encryption of Sensitive Data · **CWE-532** Sensitive Information in a Log File
- Not a broken cipher: a **threat model mismatch**. HTTPS was never meant to hide the message from the provider

<!-- Worksheet step 2. The demo does not model TLS literally. The lesson is that even with perfect transport encryption the operator reads everything. -->

---

## The fix: move encryption to the endpoints

```
week13-server | SERVER SAW: eyJlbmNfa2V5IjogIlFsUWxz...
week13-bob    | BOB DECRYPTED: meet at pier 39 at midnight
```

- Bob makes a key pair and shares only the **public** key
- Alice **encrypts on her own device** with Bob's public key (Week 10)
- The server code is **unchanged**, it just stores unreadable data
- Only Bob's **private key** (never leaves his device) opens it

![Two lanes show Alice sending toward Bob through a server. In the top lane, a TLS-only design ends encryption at the server, which logs readable plaintext. In the bottom lane, Alice encrypts on her own device to the public key the server relays, so the server stores and logs only ciphertext and Bob decrypts on his device.](img/encryption-boundary.svg)

<!-- Worksheet steps 4 to 8. Step 7 shows the two lines in alice.py that differ (payload = hybrid_encrypt(...) vs payload = SECRET_MESSAGE). The difference is on Alice's side, not the server's. -->

---

## What this lab does NOT prove

- Alice trusts **whatever public key the server gives her**
- A dishonest server could swap in **its own key**, then read the message and pass it on
- Same shape as Week 12 (a fake certificate) and Week 5 (a man in the middle)
- The lab shows an **honest** server cannot read the message, not that the key is really Bob's

<!-- Worksheet steps 9 and 10, Q3. Say this explicitly so students do not overclaim. Ask: "how would Alice know the key came from Bob?" Out-of-band safety numbers, a QR scan, a CA, key transparency. -->

---

## How Signal helps

- **Safety numbers / QR:** compare keys **outside** the server
- **Automatic key management:** no keyring to look after (PGP's weakness)
- **Double Ratchet:** keys change all the time, old messages stay safer if a key leaks later
- A limit: a **seized phone** or saved chat history can still reveal messages

<!-- Worksheet step 10 and Q4. PGP failed on usability (Whitten and Tygar, Why Johnny Can't Encrypt), not on math. Current Signal documentation uses PQXDH; X3DH is the earlier design. Do not claim a seized phone cannot reveal old plaintext. -->

---

## 🔓 Lab today — what to do

| Mode | Alice sends | Server sees |
|---|---|---|
| `vulnerable` | readable text | **readable** |
| `fixed` | encrypted text | **unreadable** |

- **Everyone (common 60):** A1 the server reads · A2 the server cannot read · A3 find the two differing lines and name the limit
- **Your form (40):** student ID ends **odd** → AIR-Sec · **even** → Conventional
- **Answer sheet:** Classroom → Week 13 → file for your form → type in the grey boxes → File → Download → PDF
- Hand in `Wk13_<StudentID>.pdf` at `learn.zcr.ai/submit`

<!-- Exact commands are in the worksheet. Start Docker early and run the build step before class. The unreadable line is long base64: students copy about 60 characters. -->

---

## Takeaway

- **HTTPS protects the road, not the destination**: the server still reads
- **E2EE** encrypts on the sender's device, only the recipient's key opens it
- It still needs the **right key**: safety numbers check that outside the server
- Next week: **authentication** (how a password or a proof gets checked)

<!-- Land the spine. Cold-call: "who could read the secret in the first mode, and why did HTTPS not help?" Remind them the worksheet is due the Sunday before next class. -->
