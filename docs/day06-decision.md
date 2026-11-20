1. The proposed change
Downgrade PyJWT from version 2.15.1 to 2.13.0.


2. Current declared and installed versions.
- The version declared in the requirements: 2.15.1
- The version actually installed: 2.15.1
- The proposed version: 2.13.0
- Your Python interpreter version: 3.14.7

3. Advisory findings.
- Advisory ID: `GHSA-9v7f-9g4p-ffgj`
- Affected version range: <2.14.0 (<= 2.13.0)
- First patched version: 2.14.0
- Which part of PyJWT is affected: PyJWKClient (HTTP fetching logic)
- What conditions are required for exploitation: must actively use PyJWKClient, requires attacker-influenced HTTP redirect from a configured trusted JWKS endpoint

4. Whether the affected code path is used by TaskFlow.
- The normal local identity implementation encodes using HS256, using locally held signing key 
- The optional Cognito/external-key implementation may retrive public keys from remote endpoint, uses PyJWKClient


5. Whether to approve, reject or request more evidence.
Reject it. Should never downgrade to a vulnerable version

6. Test results
- test pin without install: BLOCK: the proposed 2.13.0 pin is in the archived advisory's affected range.
- test approved course pin: PASS: PyJWT 2.15.1 matches the reviewed class pin.

- test_day05_access: ERROR: file or directory not found: tests/test_day05_access.py
- test full suite: [100%] 34 passed in 4.08s

7. Remaining security uncertainty.
- the latest versions might have vulnerabilities, if the vendor already ran it with the downgraded version they might be attacked

8. The next action and its owner.
- tell them no 