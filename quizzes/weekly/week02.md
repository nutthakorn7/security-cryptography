# Weekly Quiz — Week 2 (Hash Functions)

**~10 min · 6 questions · low-stakes** (lowest scores dropped). Individual.

**Name:** ____________  **Student ID:** ________

## MCQ (5 × 1)
1. Given only a digest **h**, an attacker who could find *any* input **m** with `H(m) = h` would be defeating:
   a) collision resistance  b) second-preimage resistance  c) preimage resistance  d) the avalanche effect
2. An unsalted MD5 password store leaks and the passwords fall in milliseconds. Which hash security property actually failed?
   a) none of them — the properties hold; the attacker simply guesses and hashes at enormous speed  b) collision resistance, since practical MD5 collisions exist  c) preimage resistance, since an MD5 digest can be inverted directly  d) second-preimage resistance, since the attacker already holds one input
3. A per-user random **salt** is stored in the clear, right next to the hash. That is acceptable because the salt's job is to:
   a) keep the digest secret from anyone who steals the database file  b) make each hash slower to compute  c) repair the underlying hash's known collision weakness  d) make every stored hash unique, so one precomputed table cannot cover the whole file
4. Raising a slow KDF's **cost / work factor** hurts the attacker far more than the defender because:
   a) it lengthens the salt, so a rainbow table has to be bigger  b) the defender pays it once per real login, the attacker pays it per guess, per row  c) it makes the hash collision-resistant as well as slow  d) it stops the hash being computed offline, forcing the attacker through the login page
5. A leaked password store's rows all begin `$2b$…`. You run one precomputed MD5 table over the wordlist against it. The result is:
   a) it cracks every row whose password is in the wordlist  b) it cracks only the `admin` row  c) it matches nothing, and no attack could ever recover these passwords  d) it matches nothing, but a slow per-hash bcrypt attack could still find a wordlist password

## Short answer (1 × 3)
6. A developer says: *"I store `SHA-256(password)` with no salt, and SHA-256 has never been broken, so I'm fine."* In your own words, explain the mechanism that makes them wrong: what does an attacker who steals that file actually do, and what does (a) a per-user random salt and (b) a slow KDF each change about that work?
