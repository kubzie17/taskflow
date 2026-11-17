## The proposed change.
Downgrade the PyJWT to 2.13.0 instead of keeping the pin to a newer version PyJWT 2.15.1. 

## Current declared and installed versions.
The version declared in the requirements is 2.15.1,actually installed: 2.15.1 - "the proposed 2.13.0 pin is in the archived advisory's affected range." 

## Advisory findings.

- Advisory ID: GHSA-9v7f-9g4p-ffgj
- Affected version range: 2.13.0 
- First patched version:  2.14.0
- Which part of PyJWT is affected: the attacker must  use PyJWKClient, and an attacker must influence the redirect from the trusted key endpoint, aka PyJWKClient, and a token key ID alone is not enough.
- What conditions are required for exploitation: attacker that influences the trusted endpoint's redirect


## Whether the affected code path is used by TaskFlow.
The local identity implementation in day05_identity.py verifies its key with HS256 using a locally held key and so it doesn't use PyJWKClient.
The cognito/external-key retrieves its public keys from a remote endpoint and uses PyJWKClient (affected dependency) which is the affected path thats been described in the report.

## Whether to approve, reject or request more evidence.
To reject it would include the 2.15.0 is inside the affected range and the fix is in 2.13.0 because it is only demoed by the vendor

## Test results.

- BLOCK: the proposed 2.13.0 pin is in the archived advisory's affected range + $LASTEXITCODE
1
- py check
PASS: PyJWT 2.15.1 matches the reviewed class pin. + $LASTEXITCODE
0

- tests/test_day05_access.py: 7 passed
- python -m pytest -q: ERROR during collection

## Remaining security uncertainty.
- The Cognito key path was not run against a real env or real key endpoint, so its untested end to end wise.
- 2.15.1 might still have vulnerabilities we don't know about and passing tests don't prove it is safe.


## The next action and its owner.
Tell the vendor to downgrade as 2.13.0 is in the affected range, and a local login demo does not cover PyJWKClient. And the owner would be ourselves (The shopsmat crew 😁)