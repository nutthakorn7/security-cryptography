---
marp: true
theme: default
paginate: true
header: "Cryptography and Network Security · Week 6"
---

# Week 6
## AEAD — a yes/no answer can leak a secret
Cryptography and Network Security · Nutthakorn Chalaemwongwan

<!-- Lab week: short talk, then the lab. Hook: ask "if a server never shows you the secret, only says ok or error, can you still read the secret?" Let them say no. The lab shows you can, in a few seconds. Bring a laptop with Docker; one guided path, no math. -->

---

## Today

- A **10-minute quiz** on Week 5 to start (one question at a time)
- Last time: CBC can be changed without the key. Today: a **yes/no answer** can leak the whole secret
- **Padding**: how the last block is filled, and how the server checks it
- 🔓 **Lab:** read a secret **without the key** from `200` / `403` answers, then see **GCM** give nothing away

<!-- Roadmap. Spine line to say out loud: "the server never shows the secret, and it still leaks it". Most of the class is the lab, not these slides. No project milestone this week: the CryptoVault KDF + AEAD-at-rest vault is due in Week 7. -->

---

## Recap — Weeks 3 to 5

- **Week 3:** a MAC checks that a message was **not changed**
- **Week 4:** CBC has **no check**, so an encrypted token can be changed; GCM adds a **tag**
- **Week 5:** key exchange needs authentication, or someone sits in the middle
- This week: what happens when the server answers differently to different mistakes?

<!-- Bridge. All three weeks are "a good primitive, a missing check". Today the missing check is again integrity: CBC without a tag, and a server that is chatty about what went wrong. -->

---

## Padding: filling the last block

![A 34-character message is cut into 16-byte blocks; the last block holds only two characters so 14 padding bytes, each with the value 14, fill it. After decrypting, the server checks the padding: valid gives 200 ok, invalid gives 403 bad padding.](img/w6-padding-blocks.svg)

- AES works on **16-byte blocks**, so the end of a message is **padded**
- Common rule (PKCS#7): pad with the **number of bytes added**, repeated
- After decrypting, the server **checks the padding**

<!-- Worksheet step 2. RFC 5652 §6.3 defines this padding: k − (length mod k) bytes, each with that value, and a full block when the length is already a multiple of k. Our message is 34 bytes, so 14 bytes of 0x0e. Say: "padding is not a security feature, it only fills the block". -->

---

## The server's yes/no is a leak

![The attacker changes one letter of the ciphertext and sends it to the CBC server. The server decrypts it, with no tag to check, and checks only the padding. Valid gives 200 ok, invalid gives 403 bad padding. Two different answers are a yes or no question the attacker can ask again and again.](img/w6-oracle-yes-no.svg)

```python
if pkcs7_valid(plaintext):
    return jsonify({"status": "ok"}), 200
return jsonify({"error": "bad padding"}), 403
```

- The server **never shows the secret**, but `200` vs `403` is a **yes/no question**
- That is a **padding oracle** (CWE-204: different answers reveal inside information)

<!-- Worksheet steps 3-5: ask.py original (200), start (200), end (403). The answer depends on WHERE the letter was changed. Not leaking the plaintext is not the same as leaking nothing. CWE-204 (Observable Response Discrepancy) is the right label; CWE-208 is for timing differences. -->

---

## Reading a secret with questions

![To find one hidden byte the helper script tries every value from 0 to 255 in one position of a forged block and asks the server each time. Almost all answers are 403; the one value that gets 200 tells the script what the hidden byte is. It repeats for each byte and each block.](img/w6-guess-bytes.svg)

- Like guessing a number: ask up to **256 times**, the one `200` gives the byte
- 16 bytes per block, 3 blocks: **a few thousand questions, a few seconds**
- **No key** is ever used

```sim
padding-oracle
```

<!-- Worksheet step 7 and 8. The helper (exploit.py) does the work; students never compute it. The optional Extension at the end of Part 2 has the formula for the curious: D(C_t)[15] = guess XOR 0x01, with a neighbour-byte re-check for the false positive. The sim uses a toy cipher, not real AES, with the same CBC and padding checks; say so out loud. -->

---

## This was not a toy

- **Vaudenay, 2002:** the first padding-oracle attack on CBC
- **POODLE, 2014:** padding oracle against SSL 3.0 (CVE-2014-3566)
- **Lucky Thirteen, 2013:** the **timing** version in TLS CBC (CVE-2013-0169)
- **TLS 1.3** keeps only **AEAD** algorithms (RFC 8446 §1.2)

<!-- Ground it. Real HTTPS broke this way. Lucky Thirteen shows that even when the error text is the same, response TIME can still differ, which is why "same message" alone is not the full fix. TLS 1.3 says the remaining symmetric algorithms are all AEAD; the RFC does not name CBC in that bullet. -->

---

## The fix: GCM gives the same answer

![The attacker changes a letter near the start or near the end of a GCM ciphertext. The GCM server first checks the tag, which no longer matches, so it answers 403 decryption failed wherever the letter was changed. Only the untouched ciphertext gets 200 ok.](img/w6-gcm-same-answer.svg)

- Change a letter at the start or at the end: **the same `403`**
- Nothing to ask, **nothing to learn**

<!-- Worksheet steps 11-14: ask.py fixed original (200), start (403), end (403), and the helper getting no signal. -->

---

## Two rules

- **AEAD** = encryption **and** a check that nothing was changed, in one step (RFC 5116 §2)
- **Rule 1:** check the **tag first**, before decrypting or using anything
- **Rule 2:** give the **same answer** for every failure
- Data that must stay readable but tamper-proof is **associated data** (authenticated, not encrypted)

<!-- RFC 5116 §2: an AEAD gives confidentiality and authentication for the plaintext, authenticates the associated data without encrypting it, and decryption returns either the plaintext or one FAIL symbol. Encrypt-then-MAC is the classic safe way to build the same thing from a cipher and a MAC (MAC over IV and ciphertext, separate keys, verify first); keep that for the optional Q2. -->

---

## GCM is not magic

- Ignore the tag error and carry on, and GCM protects nothing (Week 4, step 17)
- Reuse a **nonce** with the same key, and data leaks and tags can be forged (Week 4)
- Other different answers still leak: "user not found" vs "wrong password" (CWE-204)

<!-- Keep it short. The lab repeats one identical shared message with a fixed key and nonce. Different personal flags under that same pair would break GCM's nonce-uniqueness rule across runs. The login message example is the classic CWE-204 case and is Conventional Q3's last bullet. -->

---

## 🔓 Lab today — what to do

| Service | Port | Mode | Answers differ by where we change? |
|---|---|---|---|
| vulnerable | `:8098` | AES-256-CBC | **Yes** (200 or 403) |
| fixed | `:8099` | AES-256-GCM | **No** (403 always) |

- **Everyone (common 60):** A1 ask the CBC server with a changed letter · A2 run the script, read the secret · A3 see GCM give nothing
- **Your form (40):** student ID ends **odd** → Conventional · **even** → AIR-Sec
- **Answer sheet:** Classroom → Week 06 → open the file for your form, type in the grey boxes, then File → Download → PDF
- Hand in `Wk06_<StudentID>.pdf` at `learn.zcr.ai/submit`

<!-- Exact commands are in the worksheet: one known-good path, copy and run. The new helper ask.py avoids typing JSON. The shared demo flag is fine. Start Docker early; wait for Running on ...:8098 and :8099 in the logs. On Windows, use curl.exe. -->

---

## Takeaway

- A server can **leak without showing the secret**: different answers are a yes/no question
- **GCM** checks the tag first and answers the **same** every time
- It only helps if the program **checks the tag** and never reuses a nonce
- Next week: **review** of Weeks 1 to 6 and the CryptoVault KDF + AEAD-at-rest milestone

<!-- Land the spine: "not showing the secret is not the same as leaking nothing". Cold-call: "name one difference between how the CBC and GCM servers answered." Remind them to bring their answer sheets for Week 7. -->
