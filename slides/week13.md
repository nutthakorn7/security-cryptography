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

![Alice sends a message to Bob through a server. HTTPS encrypts the road from Alice to the server, but the encryption ends at the server, so the server can read the message. The road from the server to Bob is a new HTTPS road.](img/w13-road.svg)

<!-- Roadmap. Spine line to say out loud: "HTTPS protects the road, not the destination". Most of the class is the lab. Logic of the deck: a chat message goes Alice, server, Bob; HTTPS locks each road but the lock ends at the server; so the server can read it (the break); moving the lock to Alice's device fixes that (the fix); but Alice must lock to the right key (what the lab does not prove); Signal is one answer to that. Each slide answers one question and ends with the next. -->

---

## Recap — Weeks 10 to 12

- **Week 10:** hybrid encryption (a public key locks an AES key)
- **Week 12:** TLS, and a client must check the certificate
- **Today:** TLS ends **at the server**, so who else can read?

![Week 10 gives the tool: a public key locks an AES key. Week 12 gives the transport: TLS, and a client must check the certificate. Week 13 puts them together in a messaging shape and asks who else can read, since TLS ends at the server.](img/w13-recap.svg)

<!-- Bridge. Week 10 gives the tool (encrypt to a public key), Week 12 gives the transport, today puts them together in a real messaging shape. Logic: W10 can hide a message from anyone without the private key, W12 hides it on the road; neither says who sits at the end of the road. Next question: what exactly does each promise cover? -->

---

## Two different guarantees

| | **HTTPS / TLS** | **End-to-end (E2EE)** |
|---|---|---|
| Protects against | someone on the network | the network **and the provider** |
| Where it ends | at the **server** | at the **recipient's device** |
| Server sees | readable messages | only **ciphertext** |

- The padlock means "encrypted **to the server**", not "private from the server"

![Top lane: with HTTPS only, the lock covers Alice to the server and again the server to Bob, but the server itself sees the readable message. Bottom lane: with end-to-end encryption, one lock covers Alice to Bob, and the server in the middle sees only ciphertext.](img/w13-two-guarantees.svg)

```
HTTPS:  server_sees = m               # TLS ends at the server, it decrypts
E2EE:   server_sees = E(pk_B, m)      # only Bob's private key opens it
```

<!-- Worksheet Q1 and steps 1 to 3. The server terminates TLS: it decrypts, stores and can log the message. Logic: a lock protects only between the two ends that hold its key; in TLS the ends are you and the server, in E2EE the ends are you and Bob, so the server's view is m in one case and E(pk_B, m) in the other. Next question: what does "the server sees m" look like in a real log? -->

---

## The break: the server reads everything

```
week13-server | SERVER SAW: meet at pier 39 at midnight
week13-bob    | BOB RECEIVED: meet at pier 39 at midnight
```

- Alice sends **readable** text, the server stores and logs it
- **CWE-311** Missing Encryption of Sensitive Data · **CWE-532** Sensitive Information in a Log File
- Not a broken cipher: a **threat model mismatch**. HTTPS was never meant to hide the message from the provider

![Alice sends the readable message, the server stores it and writes it in its log as SERVER SAW with the readable text, and Bob receives the same readable text. The lab does not run real TLS: it models a server that ends the encryption.](img/w13-break.svg)

```
payload = SECRET_MESSAGE                  # alice.py, vulnerable mode
log("SERVER SAW: " + payload)             # server.py, the same line in both modes
```

<!-- Worksheet step 2. The demo does not model TLS literally. The lesson is that even with perfect transport encryption the operator reads everything. Logic: the server logs exactly what Alice hands it (one print line), and here Alice hands it the readable text, so the log is the evidence. Next question: the server code did not change in the fix, so what did? -->

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

![Four steps. 1: Bob makes a key pair and publishes only the public key. 2: the server hands the public key to Alice. 3: Alice encrypts on her own device with Bob's public key and sends ciphertext. 4: the server stores and logs only ciphertext, and Bob decrypts with his private key, which never leaves his device.](img/w13-fix-flow.svg)

```
payload = hybrid_encrypt(pk_B, m)         # k random; c = E(k, m); w = E(pk_B, k)
m       = hybrid_decrypt(sk_B, payload)   # k = D(sk_B, w); m = D(k, c)
```

<!-- Worksheet steps 4 to 8. Step 7 shows the two lines in alice.py that differ (payload = hybrid_encrypt(...) vs payload = SECRET_MESSAGE). The difference is on Alice's side, not the server's. Equation detail: common.py makes a fresh AES-256 key k, encrypts m with AES-GCM (c), wraps k with RSA-OAEP to Bob's public key (w), and sends the base64 of (w, nonce, c). Logic: Week 10 hybrid encryption moved to the sender's device; the server still logs what it is given, but now that is E(pk_B, m). Next question: Alice got pk_B from the server, so is it really Bob's? -->

---

## What this lab does NOT prove

- Alice trusts **whatever public key the server gives her**
- A dishonest server could swap in **its own key**, then read the message and pass it on
- Same shape as Week 12 (a fake certificate) and Week 5 (a man in the middle)
- The lab shows an **honest** server cannot read the message, not that the key is really Bob's

![Alice asks the server for Bob's public key and trusts whatever comes back. An honest server returns Bob's key. A dishonest server could return its own key, then read the message and pass it on to Bob. The lab never checks that the key really belongs to Bob.](img/w13-key-swap.svg)

```
pk = GET /pubkey                  # whatever the server returns
pk == Bob's real key ?            # the lab never asks this
```

<!-- Worksheet steps 9 and 10, Q3. Say this explicitly so students do not overclaim. Ask: "how would Alice know the key came from Bob?" Out-of-band safety numbers, a QR scan, a CA, key transparency. Logic: encrypting to a key protects the message only if the key is the recipient's; the only link between Bob and pk_B is the server, so we need a check that does not pass through the server. Next question: how does Signal make that check easy? -->

---

## How Signal helps

- **Safety numbers / QR:** compare keys **outside** the server
- **Automatic key management:** no keyring to look after (PGP's weakness)
- **Double Ratchet:** keys change all the time, old messages stay safer if a key leaks later
- A limit: a **seized phone** or saved chat history can still reveal messages

![Four ideas. Safety numbers or a QR code let two people compare keys outside the server. Automatic key management means no keyring to look after, which was PGP's weakness. The Double Ratchet changes keys all the time, so old messages stay safer if a key leaks later. A limit: a seized phone or a saved chat history can still reveal messages.](img/w13-signal.svg)

```
safety_number = fingerprint(pk_A, pk_B)    # both phones show it, compare it outside the server
(ck_next, mk) = KDF(ck)                    # a new message key each time, one way
```

<!-- Worksheet step 10 and Q4. PGP failed on usability (Whitten and Tygar, Why Johnny Can't Encrypt), not on math. Current Signal documentation uses PQXDH; X3DH is the earlier design. Do not claim a seized phone cannot reveal old plaintext. Logic: the check that the lab lacks is "compare the key outside the server", which the safety number does; the ratchet answers a second question, what if a key leaks later. The equations are the idea only (the real Signal derivations are in its documentation), not something the lab runs. Next question: what do you do in the lab today? -->

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

![Three lab steps. A1: start the vulnerable mode and read the server log, which shows the readable message. A2: start the fixed mode and read the server log, which shows unreadable text, while Bob prints the readable message. A3: find the two lines in alice.py that differ and name what the lab does not prove. Then the second part is your form: student ID ending odd does AIR-Sec, even does Conventional. Hand in Wk13 student ID PDF at learn.zcr.ai/submit by Sunday 31 January 2027, 23:59.](img/w13-lab-flow.svg)

<!-- Exact commands are in the worksheet. Start Docker early and run the build step before class. The unreadable line is long base64: students copy about 60 characters. Logic: A1 and A2 run the same server twice and compare its log (readable vs unreadable); A3 finds the one place the two runs differ (alice.py) and names what neither run proves. The odd/even form mapping flips every odd week: odd ID is AIR-Sec this week. -->

---

## Takeaway

- **HTTPS protects the road, not the destination**: the server still reads
- **E2EE** encrypts on the sender's device, only the recipient's key opens it
- It still needs the **right key**: safety numbers check that outside the server
- Next week: **authentication** (how a password or a proof gets checked)

![With HTTPS only, the server sees the readable message. With end-to-end encryption, the server sees only ciphertext. Both still depend on getting the right key: safety numbers check it outside the server.](img/w13-takeaway.svg)

```
HTTPS only:   server_sees = m              ⇒   the provider can read
End-to-end:   server_sees = E(pk_B, m)     ⇒   only Bob can read, if pk_B is really Bob's
```

<!-- Land the spine. Cold-call: "who could read the secret in the first mode, and why did HTTPS not help?" Remind them the worksheet is due the Sunday before next class. Logic: the road is protected by HTTPS, the destination only by E2EE, and E2EE is only as good as the key you lock to; the next question, how a system decides who you are, is authentication. -->
