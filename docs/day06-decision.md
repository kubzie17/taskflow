**Day 6 Decision: PyJWT Downgrade Proposal (NB 206)**

Date: 16 November 2026

**Decision**

Rejected the proposal to downgrade PyJWT to 2.13.0. TaskFlow stays on PyJWT 2.15.1.

**Reason**

- 2.13.0 is inside the affected range of advisory GHSA-9v7f-9g4p-ffgj. The first patched version is 2.14.0.
- The affected code (PyJWKClient) is used by the Cognito verification path in TaskFlow.
- The vendor's passing login demo only shows the local login works. It does not show the Cognito path is safe.

**Proposed change**

A vendor support engineer proposed pinning PyJWT to 2.13.0, stating the pin was in place and their login demo passed. The change was not merged. 2.13.0 was not installed and was only read as text from exercises/day06-proposal.case. The policy checker (exercises/day06_gate.py) was not changed.

**Investigation walkthrough**

Step 1: Read the evidence

Four files were compared: the root requirements.txt, exercises/day05-requirements.txt, Exhibit A in exercises/day06-case.md, and exercises/day06-proposal.case.

- The reviewed pin in exercises/day05-requirements.txt is PyJWT 2.15.1.
- The proposal is PyJWT 2.13.0.
- The root requirements.txt has no PyJWT entry, so a fresh install from it alone would not reproduce the reviewed version.

Step 2: Find the actual installed version

A pin in a file only shows intent, so the installed version was checked directly. All commands were run from the project root.

1. System Python:
   `python -c "from importlib.metadata import version; print(version('PyJWT'))"`
   Output: PackageNotFoundError (PyJWT is not installed in system Python).

2. Project environment:
   `.\.venv\Scripts\python.exe -c "from importlib.metadata import version; print(version('PyJWT'))"`
   Output: 2.15.1

3. Interpreter version:
   `.\.venv\Scripts\python.exe --version`
   Output: Python 3.12.10

Result: declared (2.15.1) and installed (2.15.1) match inside .venv. The proposed version (2.13.0) is different from both. The same command gives different answers depending on which Python runs it, so the interpreter must always be stated.

Step 3: Investigate the advisory

Source: offline extract in exercises/day06-case.md (Exhibit A). It was not checked against the live advisory.

- ID: GHSA-9v7f-9g4p-ffgj (CVE-2026-102267).
- Affected versions: up to and including 2.13.0.
- First patched version: 2.14.0.
- Affected part: PyJWKClient, which fetches public signing keys from a remote address.
- Issue: it followed redirects, so keys could come from another destination and custom headers could be exposed.
- Conditions: an attacker must be able to influence the redirect response of the trusted key endpoint. A token key ID alone is not enough.
- Scope: remote key retrieval only, not every JWT verification path.

Step 4: Inspect how TaskFlow uses PyJWT

- Local identity (exercises/day05_identity.py): verifies with jwt.decode and a locally held HS256 key. Does not use PyJWKClient. Not affected.
- Cognito (exercises/day05_cognito.py): uses jwt.PyJWKClient to fetch keys from a remote JWKS endpoint, then verifies with RS256. This is the affected code path.

Answers to the questions in the exercise:

- The local path uses a locally held signing key.
- The Cognito path may retrieve public keys from a remote endpoint.
- A successful local login does not show the remote-key path is secure, because the two paths share no key-fetching code.

Step 5: Test the proposed pin without installing it

`python exercises/day06_gate.py check --pin-file exercises/day06-proposal.case`
`$LASTEXITCODE`

Output: BLOCK: the proposed 2.13.0 pin is in the archived advisory's affected range.
Exit code: 1

The checker only reads the file as text, so nothing was installed.

Step 6: Test the approved course pin

`python exercises/day06_gate.py check`
`$LASTEXITCODE`

Output: PASS: PyJWT 2.15.1 matches the reviewed class pin.
Exit code: 0

Comparison: the proposed pin is blocked (exit 1) and the approved pin passes (exit 0). Only the pin value differs between the two runs.

Step 7: Test existing application behaviour

Both runs used the project environment, because system Python has no pytest.

1. `.\.venv\Scripts\python.exe -m pytest -q tests/test_day05_access.py`
   Output: 49 passed in 3.69s. Exit code: 0

2. `.\.venv\Scripts\python.exe -m pytest -q`
   Output: 81 passed in 7.00s. Exit code: 0

The Day 5 test file exists and was complete, so a full regression run was possible. These tests ran against 2.15.1, not 2.13.0, so they say nothing about how 2.13.0 would behave.

Step 8: Record the decision

This document.

**Other versions and dependencies**

- Dependency link confirmed with pip show in .venv: FastAPI 0.162.2 depends on Starlette (1.10.0 installed). Pydantic 2.14.3 depends on pydantic-core (2.50.4 installed).
- Python in .venv: 3.12.10.

**Evidence summary**

- The proposed pin is blocked by the checker and sits inside the advisory's affected range.
- The approved pin passes the checker and all 81 tests.
- The affected code path is used by the Cognito verifier but not the local verifier.
- No secrets, tokens or credentials were used or recorded.

**Remaining uncertainty**

- Advisory data is an offline extract and was not verified online.
- Only one advisory is covered. A live scanner such as pip-audit may report others.
- The gate checks the text of a pin file, not the installed version, so it cannot detect drift between the two.
- Passing tests do not prove the Cognito path is safe from redirect manipulation.
- It is unknown whether the Cognito path is enabled in any real deployment.
- Root requirements.txt has no PyJWT pin.

**Next actions**

- Change reviewer: notify the vendor the rollback is rejected and ask them to test with 2.15.1.
- TaskFlow engineer: run pip-audit and keep the output as evidence. Add PyJWT 2.15.1 to the root requirements.txt.
- Platform or deployment owner: confirm whether the Cognito path is used in any live environment.
- Second reviewer: review this decision before it is final.
