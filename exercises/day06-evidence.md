# Day 6 personal security evidence

Save a copy under your own name outside the repo or in your existing progress record. Use fictional records, short error names and test counts. An operator can run a command for a partner. Mark who ran it, who observed it and on whose machine it ran. Share an HTTP status or a redacted excerpt, never a token, log dump, credential, AWS account number or private URL.

## Booking clinic

Revision and entry point 05356ec, exercises/day05_api.py via tests/test_day05_access.py  Operator me (ran)  Direct SQLite file or test fixture test fixture (lab temp database)

| Caller and input | Expected HTTP | Actual | Stored IDs and titles before and after | Test or source of evidence |
| --- | --- | --- | --- | --- |
| Visitor POST valid title | 401 | 401 (asserted by test) | Refused write leaves seeded row unchanged | tests/test_day05_access.py (49 passed, local run in .venv) |
| Reader GET known booking | 200 | 200 (asserted by test) | Seeded row visible, no change | tests/test_day05_access.py (49 passed, local run in .venv) |
| Reader POST valid title | 403 | 403 (asserted by test) | Unchanged | tests/test_day05_access.py (49 passed, local run in .venv) |
| Dispatcher POST valid title | 201 | 201 (asserted by test) | New row added | tests/test_day05_access.py (49 passed, local run in .venv) |
| Invalid token POST valid title | 401 | 401 (asserted by test) | Unchanged | tests/test_day05_access.py (49 passed, local run in .venv) |
| Dispatcher POST 101-character title | 422 | 422 (asserted by test) | Unchanged | tests/test_day05_access.py (49 passed, local run in .venv) |

## Dependency decision

| Evidence to establish | Your finding |
| --- | --- |
| Actual declared pin / installed version / interpreter | Declared PyJWT 2.15.1 (exercises/day05-requirements.txt; now also root requirements.txt). Installed 2.15.1 in .venv, Python 3.12.10. System Python has no PyJWT. (ran, working copy) |
| One direct → transitive dependency edge with evidence | FastAPI 0.162.2 depends on Starlette (1.10.0 installed), confirmed with pip show in .venv. (ran, working copy) |
| Proposed version / advisory ID / affected range / first fixed | 2.13.0 / GHSA-9v7f-9g4p-ffgj / up to and including 2.13.0 / 2.14.0 (offline extract in exercises/day06-case.md, not checked live) |
| Which local or optional provider code reaches the affected call? Under what conditions? | exercises/day05_cognito.py uses PyJWKClient (remote key fetch), so it is reachable. The local verifier in day05_identity.py uses jwt.decode with a local HS256 key and is not affected. Exploit needs control of the key endpoint's redirect. |
| Your decision, compatibility check, test outcome and remaining risk | Rejected the downgrade, stay on 2.15.1. Gate: proposal BLOCK (exit 1), approved PASS (exit 0). Full suite 81 passed on 2.15.1 only. Risk: no live advisory scan, Cognito use in deployments unknown. See docs/day06-decision.md. |
| Tool and database used or dated offline evidence | Offline extract in day06-case.md, exercises/day06_gate.py. pip-audit not run (pending). |

## Secret incident

| Commit that introduced the marker / current tree result / clean-up commit | Which destinations are observed? Which are only possible? | Incident actions in order, with owner | Git red → green / sample still tracked | Docker evidence or pending check |
| --- | --- | --- | --- | --- |
| Introduced in b1f4696, removed from current tree in 62e8bf6 (disposable repo), current tree has no file | Observed: earlier commit readable via git show. Only possible: copies in forks, clones, CI caches, images | 1 inform lead and security (owner: engineer), 2 revoke and rotate (owner: service owner), 3 search other locations, 4 verify old credential rejected, 5 clean history last | Red: *.local.env not ignored. Green: ignored (exit 0), .env.example still tracked | Pending: Docker daemon was not running, probe untested. Rerun exercises/day06_context_probe.py. See docs/day06-incident.md |

## Pipeline and independent review

| Scenario at tested revision | Expected dependency / test / package | Actual result and evidence level (hosted, local execution, static or pending) |
| --- | --- | --- |
| Rejected proposal | Dependency BLOCK, tests and package skipped | day06_gate.py rehearse with proposal: BLOCK, TESTS SKIPPED, PACKAGE SKIPPED, exit 1 (local execution) |
| Approved pin and a deliberately failing disposable test | Dependency PASS, tests fail, package skipped | PASS, 1 failed 81 passed, TESTS FAILED, PACKAGE SKIPPED, exit 1 (local execution, disposable copy, since deleted) |
| Approved pin and passing booking + full tests | PASS, 49 and 81 passed, package eligible | PASS, 49 passed, 81 passed, PACKAGE ELIGIBLE, image build not run, exit 0 (local execution). Hosted run pending, needs push and Actions |

Reviewer pending (no peer review done yet)  Revision inspected pending  Independent input chosen pending

One verified result approved pin passes and proposal blocks, 81 tests pass (local)  One limitation hosted CI run and Docker build not done  Next action and owner push branch and open PR (me), start Docker and rerun probe (me)

## Tuesday handover

Use the existing `exercises/day05-aws.md` matrix for the class observations. Carry forward one specific service/action, region, observed status, permitted fallback and owner. Record locally what you personally established.
