# Weekly Quiz — Week 3 (MACs: Hash-Only Cookies & Length-Extension)

**~10 min · 6 questions · low-stakes** (lowest scores dropped). Individual.
Taken at the start of Week 4 as a recap of Week 3.

**Name:** ____________  **Student ID:** ________

## MCQ (5 × 1)
1. `cookie = username || SHA-3(username)` fails to provide authenticity because:
   a) SHA-3 allows length-extension  b) the digest is too short to be unforgeable  c) no secret is involved, so anyone can recompute it for `username=admin`  d) the cookie is sent without encryption
2. What does a MAC give you that a plain hash on its own does not?
   a) it hides the message from anyone reading it  b) it runs faster than a hash  c) it makes the output shorter  d) proof that the data wasn't changed and came from someone who knows the key
3. In the lab, the script got a valid `sig` from `:8092` while knowing only:
   a) one ordinary cookie and how long the secret is  b) the value of `MAC_SECRET`  c) a cookie issued to the real admin  d) the flag
4. SHA-256 was not "broken" in this lab. What was actually wrong with `SHA256(secret + data)`?
   a) the secret was too short  b) the hash's output is where it stopped, so someone can carry on from it and sign a longer message  c) SHA-256 can be run backwards  d) the data was not encrypted
5. The same script is refused by the HMAC copy on `:8093` because:
   a) `fixed_app.py` compares tags with `hmac.compare_digest()`  b) HMAC's tag is longer than a SHA-256 digest  c) HMAC uses SHA-3 inside  d) HMAC hashes twice with the key mixed in, so you can't carry on from the tag to sign a longer message

## Short answer (1 × 3)
6. `vulnerable_app.py` and `fixed_app.py` differ by one line in `make_cookie`. In your own words, with no formulas, explain to a junior developer why that one line stops the forgery: say what the vulnerable signature hands the attacker that the HMAC tag does not.
