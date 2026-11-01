# Weekly Quiz — Week 1 (Cryptography Basics & the Security Mindset)

**~10 min · 6 questions · low-stakes** (lowest scores dropped). Individual. Taken at the start of
Week 2 as a recap of Week 1. You may answer the short question in Thai or English.

**Name:** ____________  **Student ID:** ________

## MCQ (5 × 1)
1. Kerckhoffs' principle says a cryptosystem should stay secure even if the attacker knows everything except:
   a) the ciphertext  b) the algorithm  c) the key  d) the length of the message
2. Alice wants to send Bob a secret message using **asymmetric** encryption. Which key does she use to lock (encrypt) it?
   a) Alice's private key  b) Bob's public key  c) Bob's private key  d) a password they both memorised
3. A website must store its users' passwords. Which tool is right for this job?
   a) AES encryption with one key for the whole table  b) one plain SHA-256 hash per password  c) a digital signature on each password  d) a slow password KDF such as bcrypt or Argon2
4. In the seed-crack simulation, your browser recovered the private key in well under a second. What went wrong?
   a) the hash used in the design was broken  b) the private key was too short for its algorithm  c) the key came from a seed with only a few thousand possible values  d) the server sent the private key to the browser
5. In the notes app, the note database is encrypted and the app server uses the key to read it. Can the app server see the plaintext notes?
   a) yes — it holds the key and decrypts the notes to show them  b) no — encryption hides the notes from everyone  c) only if the user's browser sends it the key  d) only while the nightly backup is running

## Short answer (1 × 3)
6. AES-256 and RSA-4096 have no known practical attack, yet systems that use them still get broken. In 2–3 sentences: name **one** way this happens, give **one** example (from this week's slides, the seed-crack activity or your own idea), and say why a longer key would not help.
