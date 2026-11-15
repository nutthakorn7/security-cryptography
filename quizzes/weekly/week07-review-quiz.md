# Weekly Quiz — Cumulative Review (Weeks 1–6)

**Course:** Cryptography and Network Security (KOSEN69) · **~10 min · 6 questions · 8 points · low-stakes**
Individual, closed book. Covers threat modelling, hashing, MACs, AES modes, key exchange and AEAD, one question each.

**Name:** ____________________  **Student ID:** ____________  **Date:** ________

---

## Multiple choice (5 × 1 pt)

1. A team encrypts data with AES-256, but the key is written in a file in a public GitHub repository. The data is stolen. The root cause is best described as:
   a) AES-256 is a weak cipher
   b) a key-management mistake, not a cipher mistake
   c) the encrypted data was too short
   d) symmetric encryption should not be used

2. A random salt, different for every user, mainly stops an attacker from:
   a) guessing the password of one single user
   b) reading the hash from the database
   c) using one table of pre-computed hashes against every user at once
   d) seeing which users chose the same website

3. You want to check that a message was not changed by someone who does not know a secret key. The right tool is:
   a) a plain SHA-256 hash of the message, because it is one-way
   b) base64, because it hides the message
   c) HMAC with the secret key
   d) AES-ECB with the secret key

4. Two blocks of the same plaintext are encrypted with AES-ECB. The two ciphertext blocks are:
   a) always different, because the key changes
   b) identical, so patterns in the data can still be seen
   c) identical only when the key is short
   d) random, because AES is a secure cipher

5. Plain Diffie-Hellman (no authentication) keeps the key secret from someone who only listens, but not from:
   a) a slow network
   b) a weak password
   c) an attacker who sits in the middle and replaces the public values
   d) a padding oracle

## Short answer (3 pts)

6. In your own words, with no formulas: in the Week 6 lab the CBC server answered 200 or 403 and the script recovered the secret, but the GCM server gave the script nothing. What does AEAD (for example AES-GCM) add that plain CBC does not have, and why does that stop the script?
