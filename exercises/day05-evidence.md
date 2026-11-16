# Day 5 personal evidence record

Fictional data only. No passwords, tokens, signing keys or account identifiers appear here.

**AI assistance disclosure:** the commands, the `permit()` fix and the automated tests in this record were run and written with Kiro (an AI assistant) working from the Day 5 briefs. The "In my own words" sections are left for me to complete after I have read the code and can explain it.

## Run details

| Item | Value |
| --- | --- |
| Branch | `feature/health-service-tyreece` |
| Base revision | `4bc733e` (merge of `origin/main` at `b5871ad` into this branch). The Day 5 work below is uncommitted at the time of writing. The evidence rows were gathered on the earlier base `bf06bec`, before the merge. |
| Python | 3.12.10, PyJWT 2.15.1, FastAPI 0.162.2, Uvicorn 0.54.0 |
| Day 4 candidate | port 8044, database `data/day04-lab.db` |
| Day 5 protected API | port 8055, database `data/day05-lab.db` |
| Targeted tests | `python -m pytest tests/test_day05_access.py -q` gave 49 passed |
| Full suite | `python -m pytest -q` gave 57 passed before the merge and **81 passed** after it (49 mine, 24 from the trainer's `exercises/test_day05_access.py`, 8 existing). An empty `tests/__init__.py` was added so the two same-named test files do not clash. |
| Trainer's independent checks | `python -m pytest exercises/test_day05_access.py -q` gave 24 passed against my own `day05_api.py` |

## Evidence table

| Run / revision / port | Caller and action | Prediction | Actual HTTP and SQLite before → after | What I proved / next action |
| --- | --- | --- | --- | --- |
| Thursday baseline, 8044 | Visitor `GET /tasks`, then `POST /tasks` with title "Anonymous gate check 094128", then `GET /tasks` | Anonymous POST succeeds (the Thursday flaw) | GET 200, then POST **201** (id 4), then GET 200. SQLite `[(1,'Haircut'),(2,'Visitor'),(3,'Visitor')]` → `[... (4,'Anonymous gate check 094128')]` | An unauthenticated visitor can create a booking on the Day 4 candidate. The new row is in `day04-lab.db`. Existing rows 1 to 3 were already there before this run. |
| Thursday baseline, 8044 | `GET /support/status` (no token) | Exactly two fields | **200**, `{"status":"ok","service":"taskflow"}` | The public status response exposes only `status` and `service`. |
| Good and bad sign-in, 8055 | `POST /session` as reader and dispatcher | 200, bearer token, short lifetime | Both **200**, `token_type=bearer`, `expires_in=600` | Valid sign-in works for each role. The response body has only `access_token`, `token_type`, `expires_in`. |
| Good and bad sign-in, 8055 | Wrong passphrase for `reader`; unknown user `nobody` | Identical generic 401 | Both **401**, body `{"detail":"Authentication required"}`. Responses compared equal. | The public failure does not reveal whether the username exists. |
| Good and bad sign-in, 8055 | Anonymous `GET /tasks` | 401 | **401** | Protected reads need a token. |
| Visitor, reader, dispatcher POST (`day05-lab.db`) | POST `/tasks` as each caller (automated, isolated temp database seeded with one known booking) | 401 / 403 / 201 | 401, 403, **201**. Rows: unchanged, unchanged, +1 (exact title stored) | Only the dispatcher writes. Denied calls leave every existing row identical. |
| Reader and dispatcher GET and title validation | `GET /tasks` as both roles; dispatcher titles of 1, 100, trimmed, 101, empty, whitespace-only, non-string and missing | Reads 200; 101 and invalid titles 422 | Reads **200** and match SQLite. 1, 100 and trimmed titles **201**. 101, empty, whitespace-only, non-string and missing **422** with rows unchanged. | Authorised users are still subject to validation, and the 100/101 boundary behaves as the brief requires. |
| Malformed, expired, edited and spoofed calls, 8055 (live, real HTTP) | POST `/tasks` with: missing token, malformed token, reader token with roles edited to dispatcher (old signature), signature stripped, `Basic` scheme, reader plus `X-Role: dispatcher` header, reader plus role in JSON body, anonymous plus `X-Role` header, authentic reader | 401 ×5, 403, 403, 401, 403 (written before running) | All 9 matched. Rows unchanged after each. | The server never trusts a role from a header or body. Edited tokens fail on signature. Expiry, wrong key, wrong audience, wrong issuer and an ID-style token are covered in pytest. |
| Targeted and full pytest, support response | Targeted suite, then whole suite | All pass | 49 passed, then 57 passed. `/support/status` contract test passes. | Regression evidence is repeatable. No pre-existing Day 4 failure was observed in this run. |
| Red/green mutation check | Temporarily broke `permit()` two ways, ran the access tests, restored the file | Both mutations make tests fail | **A** (gate allows everyone): 4 tests failed, for example `assert 201 == 403` on reader POST. **B** (write a row, then return 403): 4 tests failed on row comparison, with `Left contains one more item: (2, 'leaked by a denied call')`. File restored and hash-verified identical. | The tests detect an over-permissive gate and the Day 4 pattern of writing a row and then returning an error. Only the direct SQLite assertions catch the second one. |
| Independent reviewer, verdict | **Not done** | | | Needs a second learner. To do with a partner: they choose an input or role, predict the outcome, request independent storage evidence and give a ready/hold decision. |
| AWS observed / blocked / next owner | **Not done** | | | Needs my own sandbox session. Work through `day05-aws.md` outside the repo and record only Available / Denied / Not tested. |

## Error encountered and how it was resolved

I lost the reader and dispatcher passphrases from Challenge 2. I deleted the local identity file outside the repository and recreated both identities. This also rotated the signing key, so older tokens stopped verifying and I signed in again. A second problem: the shell's default `python` was a different installation without the project's packages, so I ran the tests and servers with the interpreter that has the dependencies.

## Observations to check before I submit

- `tests/test_api.py` was changed (by me, before this session). The old test `test_support_status_exposes_only_public_fields` asserted `support_node` and `runbook` were absent. The replacement `test_public_status_contract` asserts exact equality with `{"status":"ok","service":"taskflow"}`, which implies the same thing. I should be able to explain why this is not a weakened assertion.
- `lab-credentials.txt` holds fictional practice passphrases in the repo folder. It is listed in `.gitignore` and must stay out of screenshots, commits and this evidence.
- The Day 4 database now contains the extra row created in the baseline run. That is expected, but note it if asked.

## In my own words (to complete)

1. Where does the role come from, and why can the client not influence it?
2. Why is 401 different from 403, and 403 different from 422?
3. Why does the SQLite check matter when the API already returned the right error code?
4. What did the mutation check show that a status-only test would have missed?
5. One remaining question about Monday:

## Next steps

- Review the diff, then commit on a Day 5 branch with a conventional message, for example `feat(day05): enforce reader and dispatcher permissions`.
- Complete Challenge 6 with a partner and Challenge 7 in the sandbox.
