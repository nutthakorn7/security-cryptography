# Weekly Quiz — Week 3 (MACs: Hash-Only Cookies & Length-Extension)

**~10 min · 6 questions · low-stakes** (lowest scores dropped). Individual.

**Name:** ____________  **Student ID:** ________

## MCQ (5 × 1)
1. `cookie = username || SHA-3(username)` fails to provide authenticity because:
   a) SHA-3 allows length-extension  b) the digest is too short to be unforgeable  c) no secret is involved, so anyone can recompute it for `username=admin`  d) the cookie is sent without encryption
2. Besides a captured `(data, sig)` pair, the length-extension forgery against `:8092` needs:
   a) the length of `MAC_SECRET`  b) the value of `MAC_SECRET`  c) a second cookie issued to another user  d) nothing further at all
3. An attacker can resume SHA-256 from a digest they were given because the digest is:
   a) a reversible encoding of the input  b) the 8-byte bit-length SHA-256 appends when padding  c) a summary the original message can be rebuilt from  d) the compression function's internal state after the final block
4. SHA-256 pads with `0x80`, then zero bytes until the length is ≡ 56 mod 64, then an 8-byte bit-length. For `len(MAC_SECRET) + len(data) = 16 + 22 = 38` bytes, the glue padding is:
   a) 18 bytes  b) 26 bytes  c) 34 bytes  d) 64 bytes
5. The same forgery bounces off `:8093` because:
   a) `fixed_app.py` compares tags with `hmac.compare_digest()`  b) HMAC's tag is longer than a SHA-256 digest  c) HMAC's outer hash starts from a `key⊕opad` state the tag never reveals  d) HMAC uses SHA-3 internally, which has no length-extension weakness

## Short answer (1 × 3)
6. `vulnerable_app.py` and `fixed_app.py` differ by one line in `make_cookie`. In your own words — no formulas, and without using the term "Merkle-Damgard" — explain to a junior developer why that one line stops the forgery: say what the vulnerable signature hands the attacker that the HMAC tag does not.
