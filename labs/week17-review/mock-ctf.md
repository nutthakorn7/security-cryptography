# Week 17 — Mock Final CTF (Final dry-run)

**Covers:** the whole term, **emphasis Weeks 10–16** · **Format:** same as the Week 19 final
practical · **Ungraded** (participation) · **Time:** ~165 min · teams · **sandbox targets only**
(the [ethics policy](../../ETHICS.md) applies — attack only these lab containers).

> A practice run **with hints**. Every challenge is a *repeat* of a lab you already completed this
> term, so the self-check points back to that lab's own `exploit.py` / evidence check and
> `worksheet.md` — no answers or flags are printed here. The flags themselves are per-student and
> generated at deploy time (see [`../../SUBMISSION.md`](../../SUBMISSION.md)); the values below are
> deliberately omitted.

**Targets (this term's built labs):** `labs/week10-hybrid-encryption` (Nonce Detective audit) ·
`labs/week11-signatures-zkp` · `labs/week12-secure-transport` · `labs/week13-e2e-encryption` ·
`labs/week14-authentication` · `labs/week15-pqc` · plus a first-half callback round from
`labs/week02-hash` … `labs/week06-aead`.

---

## Main round — post-midterm (Weeks 10–15)

| # | Challenge | Topic (analogous CWE) | Hint | Self-check |
|---|-----------|-----------------------|------|-----------|
| 1 | Recover the leaked plaintext from two intercepted "hybrid-encrypted" messages | GCM nonce reuse, Wk10 (CWE-323) | No running service — audit `audit_the_ai/`. The RSA-OAEP + AES-GCM looks textbook; find the one *fixed/reused* nonce, then use `XOR(C1,C2)=XOR(P1,P2)` to recover the text. | Your proof script prints the recovered plaintext; compare with `fixed_hybrid_encrypt.py` + the worksheet rubric. |
| 2 | Double-spend a single authorized withdrawal | ECDSA signature malleability, Wk11 (CWE-347) | `GET /sign` (:8102) for a valid `(r, s)`; submit it, then submit the twin `(r, n−s)` — same message/key, different txid. Not nonce reuse — pure malleability. | `python exploit.py` → two `PASS` lines; the fixed bank (:8103) rejects the high-S twin with `403`. |
| 3 | Intercept a secret from a TLS client that trusts the wrong server | Improper cert validation (MITM), Wk12 (CWE-295/300) | Alice dials `mitm` believing it's `bob`; the vulnerable client uses `CERT_NONE`. The fix loads the demo CA and keeps `check_hostname=True`. Read the container logs, not a browser. | Vulnerable log shows `MITM INTERCEPTED: …`; fixed mode shows `CERT VERIFICATION FAILED` and `grep -c "MITM INTERCEPTED"` = `0`. |
| 4 | Prove the messaging server can (then cannot) read a "private" message | Transport vs. end-to-end encryption, Wk13 (CWE-311/319) | No host port — `tail` the server log. Vulnerable mode logs `SERVER SAW: <plaintext>`; with `E2E=1` Alice encrypts client-side and the log holds only base64. | `docker compose … logs server \| grep -c "meet at pier 39 at midnight"` = `1` vulnerable / `0` fixed, while Bob still prints `BOB DECRYPTED`. |
| 5 | Log in without the server ever seeing your password | Credential transmission / challenge-response, Wk14 (CWE-522/532) | Vulnerable mode logs `SERVER SAW PASSWORD: …`; with `PAKE=1` the client sends `proof = HMAC(verifier, nonce)` and the password appears nowhere. | Fixed mode: `grep -c "correct-horse-battery"` = `0` and `grep -c "SERVER SAW PASSWORD"` = `0`, yet the client still prints `LOGIN OK`. |
| 6 | Forge a signature on the admin message you're forbidden to sign | Lamport one-time-key reuse, Wk15 (CWE-323/347) | `/sign` refuses the admin message directly. Sign `M=0x00000000` and `~M=0xFFFFFFFF` (:8100) → both preimages per bit → the full private key → forge on `0xA5A5C3C3` offline. | `python exploit.py` → `PASS` on :8100 (forgery + flag) and `PASS` on :8101 (2nd `/sign` refused `403`, forgery rejected). |

## Callback round — first-half primitives (Weeks 2–6)

*Fewer challenges, lower weight — the final emphasizes Wk10–16, but the symmetric arc is fair
game. Each is a lab you already ran.*

| # | Challenge | Topic (analogous CWE) | Hint | Self-check |
|---|-----------|-----------------------|------|-----------|
| 7 | Crack the admin password from a leaked user store | Fast/unsalted password hash, Wk2 (CWE-916/759) | The vulnerable store (:8094) is unsalted MD5 — run a dictionary against it, then log in. Watch the identical attack bounce off the bcrypt store (:8095). | `exploit.py` cracks the hash and logs into :8094; the bcrypt store is not cracked by the fast-dictionary technique. |
| 8 | Forge an admin auth-cookie without knowing the secret | Hash-as-MAC length extension, Wk3 (CWE-347/290) | The vulnerable app signs cookies with `sha256(secret‖data)` — a Merkle–Damgård construction. Append your admin claim and compute a valid new digest via length extension (you'll need the secret *length*, not the secret). | `exploit.py` forges the cookie and captures the flag; the HMAC-based fixed app rejects the same forged cookie with `403`. |
| 9 | Turn `role=guest` into `role=admin` in a token you can't decrypt | CBC bit-flipping malleability, Wk4 (CWE-353/347) | Unauthenticated CBC: flip chosen bytes in one ciphertext block to flip the matching bytes of the *next* plaintext block. The AES-GCM fixed app (:8097) detects the tamper. | Bit-flip succeeds and captures the flag on :8096; the tampered token is rejected `403` on :8097. |
| 10 | Sit in the middle of a key exchange and read the "secret" both sides agree on | Unauthenticated DH MITM, Wk5 (CWE-322/300) | Relay two independent DH handshakes (one per side). `SIGNED=1` (HMAC-tagged public keys) makes both sides abort with `AUTH FAILED`. Read the container logs. | Vulnerable log shows `RELAY INTERCEPTED: …`; signed mode's `grep -c "RELAY INTERCEPTED"` = `0` and both peers exit `1`. |
| 11 | Decrypt a ciphertext byte-by-byte using only yes/no error responses | CBC padding oracle, Wk6 (CWE-347/208) | The naive MAC-then-encrypt app (:8098) leaks padding validity via `200` vs `403`. Recover `/secret` one byte at a time. The AES-GCM fixed app (:8099) returns a uniform `403`. | Your oracle recovers the full `/secret` plaintext on :8098; the same attack recovers nothing on :8099. |

**For each challenge you attempt:** write down your payload / command **and a one-line
mitigation**, then compare against that lab's own `exploit.py` and `worksheet.md`. (These are
repeat labs — full solutions live in each lab directory; no separate spoiler-free copy is needed.)

## Warm-up (concepts) — do this if you finish early or get stuck

- For any **two** challenges above, state the **analogous CWE** and the **attack class** in one
  sentence each (the CWE is on each lab README's `**Analogous CWE:**` line).
- For any **two**, give the **one control or discipline** that would have prevented it — e.g.
  *authenticate the key exchange* (10), *enforce low-S / BIP-62* (2), *never reuse a nonce or a
  one-time key* (1, 6), *validate the certificate chain* (3), *move encryption to the endpoints*
  (4), *never transmit the password* (5).
- **Through-line to be able to say out loud:** confidentiality, integrity, and authenticity are
  three *separate* properties — nearly every challenge here is a system that bought one and assumed
  it got the others for free.

---

> Review your weak spots, then it's the **Week 18 written exam** (cumulative, emphasis Wk10–16)
> and the **Week 19 capstone practical**. See [`README.md`](README.md) for how this dry-run maps to
> the real final.
