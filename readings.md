# Readings & Resources (per week)

Curated, **free**, authoritative resources to read **before/after** each week. Primary sources
(RFCs, NIST/FIPS, OWASP cheat sheets, official protocol docs) — skim the starred ⭐ one before class.

This is the Security & Cryptography course's own reading list — a separate GitHub repo and
Google Classroom instance from the companion Software Security course, even though both follow
the same 19-week AIR-Sec skeleton.

## Foundations
- **W1 — Intro: Why Crypto Fails in Practice**
  - ⭐ Moxie Marlinspike — *The Cryptographic Doom Principle* — https://moxie.org/2011/12/13/the-cryptographic-doom-principle.html
  - "Crypto Fails" writeups (search for: cryptofails.com archive — real-world crypto implementation failures)
  - NIST — Cryptographic Standards and Guidelines overview — https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines
  - CISA — Secure by Design — https://www.cisa.gov/securebydesign
- **W2 — Hash Functions**
  - ⭐ OWASP Password Storage Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
  - NIST SP 800-63B (Digital Identity Guidelines — Authentication) — https://pages.nist.gov/800-63-3/sp800-63b.html
  - A cryptographic hash function primer (search for: "Cryptographic hash function" overview — properties: preimage/second-preimage/collision resistance)
  - Cryptopals Set 1 (practice) — https://cryptopals.com/
- **W3 — MACs**
  - ⭐ RFC 2104 — HMAC: Keyed-Hashing for Message Authentication — https://www.rfc-editor.org/rfc/rfc2104
  - A length-extension-attack writeup (search for: "hash length extension attack" explainer, e.g. Skull Security's classic writeup)
  - Cryptopals Set 4 — MAC/hash attacks (practice) — https://cryptopals.com/
- **W4 — AES Modes of Operation**
  - ⭐ NIST SP 800-38A — Recommendation for Block Cipher Modes of Operation — https://csrc.nist.gov/pubs/sp/800/38/a/final
  - A CBC padding-oracle / bit-flipping (malleability) writeup (search for: "CBC bit flipping attack" or "padding oracle attack" explainer)
  - Cryptopals Set 2 — CBC/padding (practice) — https://cryptopals.com/
- **W5 — Key Exchanges**
  - ⭐ RFC 3526 — More MODP Diffie-Hellman groups for IKE — https://www.rfc-editor.org/rfc/rfc3526
  - A Diffie-Hellman / MITM explainer (search for: "Diffie-Hellman man-in-the-middle attack" explainer)
  - Boneh & Shoup — *A Graduate Course in Applied Cryptography*, key-exchange chapter — https://toc.cryptobook.us/ (PDF: https://crypto.stanford.edu/~dabo/cryptobook/BonehShoup_0_6.pdf)
- **W6 — AEAD**
  - ⭐ NIST SP 800-38D — Recommendation for Block Cipher Modes of Operation: GCM and GMAC — https://csrc.nist.gov/pubs/sp/800/38/d/final
  - Serge Vaudenay — *Security Flaws Induced by CBC Padding* (the classic padding-oracle paper) (search for: "Vaudenay CBC padding oracle" paper PDF)
  - OWASP Cryptographic Storage Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html

## Asymmetric & applied protocols
- **W10 — Hybrid Encryption**
  - ⭐ RFC 8017 — PKCS #1: RSA Cryptography Specifications (RSA-OAEP) — https://www.rfc-editor.org/rfc/rfc8017
  - An ECIES / hybrid-encryption explainer (search for: "Elliptic Curve Integrated Encryption Scheme (ECIES)" explainer)
  - Boneh & Shoup — *A Graduate Course in Applied Cryptography*, public-key encryption chapters — https://toc.cryptobook.us/
- **W11 — Signatures & ZKP**
  - ⭐ RFC 8032 — Edwards-Curve Digital Signature Algorithm (EdDSA) — https://www.rfc-editor.org/rfc/rfc8032
  - Schnorr identification protocol paper/explainer (search for: "Schnorr identification protocol" paper or explainer)
  - A signature-malleability / Mt. Gox writeup (search for: "Mt. Gox transaction malleability" explainer)
- **W12 — Secure Transport**
  - ⭐ RFC 8446 — The Transport Layer Security (TLS) Protocol Version 1.3 (at least §1-2 overview) — https://www.rfc-editor.org/rfc/rfc8446
  - A Web PKI / Certificate Transparency explainer (search for: "Certificate Transparency" overview, e.g. certificate.transparency.dev)
  - The Noise Protocol Framework spec — https://noiseprotocol.org/noise.html
- **W13 — E2E Encryption**
  - ⭐ Signal — The X3DH Key Agreement Protocol — https://signal.org/docs/specifications/x3dh/
  - Signal — The Double Ratchet Algorithm — https://signal.org/docs/specifications/doubleratchet/
  - A "why TLS isn't E2EE" explainer (search for: "TLS vs end-to-end encryption" explainer)
- **W14 — Authentication**
  - ⭐ OWASP Authentication Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
  - An SRP / OPAQUE PAKE explainer (search for: "OPAQUE protocol" PAKE explainer, or RFC 2945 for SRP)
  - W3C Web Authentication (WebAuthn) Level 2 spec — https://www.w3.org/TR/webauthn-2/ · FIDO Alliance specifications overview — https://fidoalliance.org/specifications/
- **W15 — Post-Quantum Cryptography**
  - ⭐ NIST FIPS 203 — Module-Lattice-Based Key-Encapsulation Mechanism Standard (ML-KEM) — https://csrc.nist.gov/pubs/fips/203/final
  - NIST FIPS 204 — Module-Lattice-Based Digital Signature Standard (ML-DSA) (search for: "NIST FIPS 204 final" csrc.nist.gov/pubs/fips/204/final)
  - A Lamport / hash-based signature primer (search for: "Lamport signature" explainer; also see NIST FIPS 205 — SLH-DSA, stateless hash-based signatures)
  - A "harvest now, decrypt later" explainer (search for: "harvest now decrypt later" quantum threat explainer)

## Cross-cutting (any week)
- Cryptopals challenges (hands-on practice, all sets) — https://cryptopals.com/
- Boneh & Shoup — *A Graduate Course in Applied Cryptography* (free textbook) — https://toc.cryptobook.us/
- NIST Computer Security Resource Center — Cryptographic publications index — https://csrc.nist.gov/publications
- IACR ePrint Archive (primary-source crypto papers) — https://eprint.iacr.org/
- OWASP Cheat Sheet Series (index) — https://cheatsheetseries.owasp.org/

> Review weeks (7, 17) and capstone (16): revisit the starred ⭐ items for the units covered.
> Exam blocks — W8 (written) + W9 (practical CTF), midterm, covers W1-6; W18 (written) + W19
> (practical CTF), final, cumulative with emphasis on W10-16.
> Links are official/free; if one moves, search the resource title — do not guess a replacement URL.
