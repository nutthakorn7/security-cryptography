# Weekly Quiz — Week 6 (AEAD and the CBC Padding Oracle)

**Course:** Cryptography and Network Security (KOSEN69) · **~10 min · 6 questions · low-stakes**
(lowest scores dropped). Individual.
Taken at the start of Week 7 as a recap of Week 6.

**Name:** ____________  **Student ID:** ________

## MCQ (5 × 1)
1. **AEAD** (for example AES-GCM) is an encryption mode that gives, in one step:
   a) encryption only, with a separate step to check changes later  b) a hash of the message so the receiver can compare  c) encryption plus a check that nothing was changed  d) a signature that proves who sent the message
2. In the lab, changing a letter near the **start** of the CBC message still got `200 ok`, but changing a letter near the **end** got `403 bad padding`. The answers differed because:
   a) the server picks `200` or `403` at random  b) the key changes with every letter  c) base64 only works at the start of a message  d) the end of the message holds the padding, which the server checks, and the start does not
3. A developer says: *"our decrypt endpoint never shows the plaintext, it only answers `200` or `403`, so an attacker learns nothing."* The flaw in that claim is:
   a) AES-256 can now be guessed in a few seconds  b) the plaintext is always written in the server log  c) base64 hides nothing, so the answers are readable  d) two different answers are a yes/no question the attacker can ask again and again
4. The **GCM** server answered `403` in the same way wherever a letter was changed because it:
   a) checks the tag before decrypting and gives the same answer for every failure  b) uses a longer key than the CBC server  c) pads the last block with a different rule  d) listens on a port that attackers cannot reach
5. The **associated data** (the "AD" in AEAD) is data that is:
   a) encrypted but not checked, so it stays hidden  b) checked for changes but not encrypted, so it stays readable  c) neither encrypted nor checked, because headers hold no secrets  d) encrypted with a second key and sent next to the ciphertext

## Short answer (1 × 3)
6. In your own words, with no formulas: the CBC server never showed the secret, yet the script read all of it. What did the script use, and why did the same script get nothing from the GCM server?
