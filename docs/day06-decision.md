CHALLENGE 2 - PyJWT 2.13.0 PROPOSAL (NB 206)

STEP 2 
- Declared: PyJWT==2.15.1 (exercises/day05-requirements.txt). The root requirements.txt has no PyJWT entry.
- Installed: 2.15.1
- Proposed: 2.13.0
- Python: 3.12.16

STEP 3 
- Affected: up to and including 2.13.0
- First patched: 2.14.0
- Affected part: PyJWKClient, which followed redirects when fetching signing keys
- Conditions: an attacker must be able to influence the trusted key endpoint's redirect response. A token key ID alone is not enough.
- Scope: a specific part of the library (remote key fetching), not every verification path

STEP 4 
Q: Which path uses a locally held signing key?

A: The local identity path (day05_identity.py). It uses jwt.decode with a locally held HS256 key.
Q: Which path may retrieve public keys from a remote endpoint?
A: The optional Cognito path (day05_cognito.py). It creates jwt.PyJWKClient pointing at the issuer's JWKS URL.
Q: Does a successful local login show the remote-key path is secure?

A: No. The local path never uses PyJWKClient, so a passing local login says nothing about the affected code.

KEY QUESTION 
- Local path: no, there is no remote key fetch.
- Cognito path: yes in principle, because it uses PyJWKClient at an affected version. It needs an attacker who can influence the key endpoint's redirect.

STEP 5 
BLOCK: the proposed 2.13.0 pin is in the archived advisory's affected range. Exit code 1.

STEP 6 
PASS: PyJWT 2.15.1 matches the reviewed class pin. Exit code 0.

STEP 7 
- tests/test_day05_access.py: 18 passed
- full suite: 29 passed

DECISION: REJECT
The downgrade moves TaskFlow from 2.15.1 (past the 2.14.0 fix) back into the affected range. The vendor's passing demo only covers the unaffected local path.

REMAINING UNCERTAINTY
- The advisory is a dated snapshot of one finding; a live scanner may show others
- The Cognito path was not tested live
- Unknown whether an attacker could realistically influence the key endpoint's redirect

NEXT ACTION

Tell the vendor the proposal is declined and keep 2.15.1.
