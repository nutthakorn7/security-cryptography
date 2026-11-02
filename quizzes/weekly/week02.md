# Weekly Quiz — Week 2 (Hash Functions)

**~10 min · 6 questions · low-stakes** (lowest scores dropped). Individual.
Taken at the start of Week 3 as a recap of Week 2.

**Name:** ____________  **Student ID:** ________

## MCQ (5 × 1)
1. You store a password as its hash. An attacker steals the file. What do they actually do to find a password?
   a) they run the hash backwards to get the password  b) they guess common passwords, hash each guess, and look for a match  c) they ask the server to decrypt it  d) nothing — a hash cannot be attacked
2. An unsalted MD5 password file leaks and the passwords fall in milliseconds. What went wrong?
   a) nothing is "broken" about MD5 here — it is just fast and unsalted, so guessing is cheap  b) MD5 was reversed directly  c) the attacker found two files with the same hash  d) the salt was guessed
3. A per-user random **salt** is stored in the clear, right next to the hash. That is fine because the salt's job is to:
   a) keep the hash secret from whoever steals the file  b) make the hash slower to compute  c) fix MD5's known weaknesses  d) make each stored hash unique, so one list of guesses can't crack the whole file at once
4. A slow password hash (bcrypt/Argon2) has a tunable **cost**. Raising it hurts the attacker far more than the real user because:
   a) it makes the salt longer  b) the real user pays it once per login; the attacker pays it on every guess, for every user  c) it turns the hash collision-resistant  d) it blocks offline guessing completely
5. A leaked password file's rows all start with `$2b$` (bcrypt). You run one list of MD5-hashed guesses against it. The result is:
   a) it cracks every row whose password is in the list  b) it cracks only the admin row  c) it matches nothing, and these passwords can never be recovered  d) it matches nothing, but a much slower per-user bcrypt attack could still find a weak password

## Short answer (1 × 3)
6. A developer says: *"I store `SHA-256(password)` with no salt, and SHA-256 has never been broken, so I'm fine."* In your own words: what does an attacker who steals that file actually do, and what does (a) a per-user salt and (b) a slow password hash each change about that work?
