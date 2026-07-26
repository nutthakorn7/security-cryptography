# Weekly Quiz — Week 1 (Security Mindset & Threat-Modelling a Cryptographic System)

**~10 min · 6 questions · low-stakes** (lowest scores dropped). Individual.

**Name:** ____________  **Student ID:** ________

## MCQ (5 × 1)
1. Calling a primitive **"cryptographically secure"** promises:
   a) that no attacker will ever break it, however powerful  b) that any system calling it correctly is secure overall  c) that it resists a defined attack class under stated assumptions  d) that NIST has approved it for government and military use
2. In this week's lightweight **threat-modelling** process, the question you ask at each primitive is:
   a) which assumption it relies on, and whether the system upholds it  b) whether its key length still meets current NIST minimum guidance  c) whether the library implementing it has all vendor patches applied  d) how many years a brute-force attack against it would need
3. On its own, **"we encrypted the data"** is a claim about:
   a) confidentiality and integrity  b) confidentiality and availability  c) all three CIA properties  d) confidentiality only
4. The **PS3 firmware-signing** break (fail0verflow, 27C3) happened because:
   a) ECDSA turned out to be mathematically broken  b) the same nonce was reused across signatures  c) the signing key was far too short  d) the firmware hash was MD5, which collides
5. In a system handling cryptographic keys, a **trust boundary** is:
   a) any point where control over key material changes hands  b) the network perimeter between the LAN and the internet  c) the line between encrypted and plaintext database fields  d) the date on which a key is due for rotation

## Short answer (1 × 3)
6. Name **one** category of real-world cryptographic failure that a longer key or a newer algorithm would do nothing to prevent. Give one concrete example of it, and say in one sentence why more key bits do not help.
