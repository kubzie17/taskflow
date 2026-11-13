# Day 5 · Who can create a Northbridge booking?

Friday 13 November · Online · 09:30–15:30 UK

Yesterday a visitor booked a repair without signing in. Today you own the fix. By the end a second engineer should be able to tell who can book, who can read and what happened to the database after each attempt.

## Set up on your machine

1. Start in the repository root that contains `app/`, `exercises/` and `tests/`. Check `git status -sb` and `git branch --show-current`. Save intended Day 4 edits on their own branch before bringing in the trainer's Day 5 materials commit. The root README gives the pull/cherry-pick routes. In a clean working tree create your personal working branch, for example `git switch -c day05-yourname`.
2. Activate Thursday’s Python 3.12 virtual environment. In Windows PowerShell use `.\.venv\Scripts\Activate.ps1` (or `.\venv\Scripts\Activate.ps1` if yours is called `venv`). On macOS/Linux use `source .venv/bin/activate`. If activation is unavailable on Windows, use your environment's `.\.venv\Scripts\python.exe` wherever these instructions say `python`. Run these commands from the repo root.

```text
python --version
python -m pip install -r requirements.txt -r exercises/day05-requirements.txt
python -c "from importlib.metadata import version; print(version('PyJWT'))"
python -m pytest -q
```

3. Confirm the JWT package reports `2.15.1`. If package installation is restricted, pair with a prepared machine while the trainer checks the approved package source. Record the initial result, branch and any outstanding failure. Thursday’s intended public response is exactly `{"status":"ok","service":"taskflow"}`. Check the live candidate before claiming the repair. If it differs, save the branch and ask for the short recovery route. A partner can run the compatible copy while you drive the investigation. Your Day 5 tests can still run independently of the state of Thursday’s copy.
4. Start Thursday’s candidate for the baseline in challenge 1. `Ctrl+C` stops it. Friday uses a different port and database so each result has an identifiable source.

```text
python -m uvicorn exercises.day04_candidate:create_candidate --factory --host 127.0.0.1 --port 8044
```

5. After the baseline, initialise the Friday lab once in your own OS account. Choose different fictional passphrases of at least 12 characters for the built-in names `reader` and `dispatcher`. The prompt hides input. The local hashes and signing key live in `.taskflow-lab/day05.json` under your user home, outside the repo. Keep this file private. It is sufficient to initialise once. Start Friday’s candidate from the repo root.

```text
python -m exercises.day05_identity
python -m uvicorn exercises.day05_api:create_secure --factory --host 127.0.0.1 --port 8055 --reload
```

6. Open `http://127.0.0.1:8055/docs`. The page title contains **protected bookings**. Use a second terminal in the same environment for tests and Git. The untouched starter returns 501 at sign-in and rejects protected calls. This is your starting point. Keep any terminal showing tokens or passphrases off screen share. Refresh Swagger or use **Logout** before testing another identity.

## Your workbench

| File | Use |
| --- | --- |
| `exercises/day05_api.py` | Your main edit. Three marked sections implement sign-in, verified request identity and the role decision. The two booking routes already use those dependencies. |
| `exercises/day05_identity.py` | Provided cryptographic building blocks. Read `check_password`, `issue` and `verify`. Identify who selects the role, which claims are checked and what happens to a bad signature. |
| `exercises/day05_test_starter.py` | Copy to `tests/test_day05_access.py`, then author your own cases. The fixture supplies a temporary database and fictional credentials. |
| `exercises/day05_probe.py` | Optional private-input helper for presenting a deliberately damaged bearer without displaying it. Run `python -m exercises.day05_probe`. Choose `login` for terminal-only sign-in, two reads and a booking attempt. This mode never prints the token. |
| `exercises/day05-aws.md` | Editable discovery matrix for the afternoon. Save your own copy outside the repo. |
| `exercises/day05-cognito.md` | Optional real identity-provider investigation once your local proof is complete. |

### What the client agreed

| Operation | Visitor | Signed-in reader | Signed-in dispatcher |
| --- | --- | --- | --- |
| View public health and support status | 200 | 200 | 200 |
| List this pilot team's bookings | 401 | 200 | 200 |
| Create a valid booking | 401 | 403 | 201 |
| Submit a 101-character title as dispatcher | — | — | 422 and no change to stored bookings |

For this pilot, both roles see the same fictional team list. Different client organisations sharing a deployment would need an additional ownership check. Only server-controlled identities can supply a role.

## 1 · Reproduce Thursday’s booking

**Scenario.** Dispatch received a booking nobody recognises. **Outcome.** Describe an observed access failure against the original candidate. On port 8044, use `/docs` to list bookings, submit a unique fictional title without signing in and list again. Verify the same ID and title in the right SQLite file. Inspect `/support/status` separately and report the actual fields. **Acceptance.** Give the port, caller, status and before/after evidence. Record any divergence from the class baseline. Stop 8044 after recording it.

Use this read-only command from the repo root in another terminal. For Friday’s database substitute `day05-lab.db`.

```text
python -c "import sqlite3; c=sqlite3.connect('file:data/day04-lab.db?mode=ro',uri=True); print(c.execute('select id,title from tasks order by id').fetchall()); c.close()"
```

## 2 · Introduce an identity

**Scenario.** Northbridge needs to distinguish two fictional colleagues. **Outcome.** A correct local sign-in returns a short-lived signed access token. A wrong passphrase or unknown user receives a generic 401. Complete the two identity sections in `day05_api.py` using the supplied primitives. Passwords and roles must come from the correct places. **Acceptance.** Prove a valid sign-in for each role, identical public failure for wrong credentials and an anonymous 401 on a protected resource. Identify where expiry and signature are checked. **Evidence.** Status, token type/lifetime and a short explanation. Keep actual token strings private. The role decision stays locked until challenge 3.

In Swagger, use **POST /session → Try it out**. Privately copy only the returned `access_token` value, without quotes. Open **Authorize**, paste the raw token once, then close the dialog. Swagger supplies the Bearer prefix. A new login by itself does not change the identity Swagger is using.

## 3 · Enforce the booking policy

**Scenario.** A contractor can view the rota. Only dispatch can add a booking. **Outcome.** Enforce the table above on the API, even for a direct HTTP client. Complete the remaining gate, inspect where it runs relative to the SQLite insert, then test each caller using a valid title. Preserve the existing title rules and the two public status fields. **Acceptance.** Show 401, 403 and 201, both permitted reads, the exact stored dispatcher row and a 422 for an invalid authorised title. **Evidence.** Record caller, method, status and before/after rows. Swap driver midway. At lunch, save your branch or note the next failing check.

## 4 · Try to bypass your own fix

**Scenario.** A caller can control headers and request bodies. **Outcome.** Challenge the server on your own localhost with a missing, malformed, expired and edited token and a forged role. First predict what each request will do, then run it. Retain a token from challenge 2 privately and retry after its ten-minute lifetime, or use a short-lived synthetic token in an isolated test. Editing an expiry in an existing token also damages its signature and cannot isolate the expiry check. **Acceptance.** Each invalid credential is rejected with 401, an authentic reader still gets 403 and all denied calls leave the exact same rows. **Evidence.** For one attempt record what you changed, what you held constant and what the result actually proves.

## 5 · Prove it in pytest

**Scenario.** A later release could return a convincing error after already writing the row. **Outcome.** Give the next developer repeatable regression evidence. Copy the scaffold, write the tests, seed a known booking and use the fixture’s direct SQLite reader. Cover the agreed status matrix, invalid/expired/tampered tokens, both allowed reads, title boundaries and public status. Include a real failed test from an isolated red/green attempt (for example, add the next assertion before the feature works). Never weaken an old assertion to get a green run. **Acceptance.** Show targeted and complete test commands, an authenticated valid create/read, an authenticated invalid title, and identical rows around denied calls. **Evidence.** Preserve a safe failure line and its passing rerun. Separate a pre-existing Day 4 failure from a new regression.

```text
python -m pytest tests/test_day05_access.py -q
python -m pytest -q
```

## 6 · Independent security review

**Scenario.** The author believes the branch can ship. **Outcome.** Have a different learner choose a check without telling them which example to copy. Share a sanitised diff or a screen after clearing credentials. The reviewer chooses an input or role, predicts the outcome, requests independent storage evidence and gives a release decision. Reverse the roles if time permits. **Acceptance.** Record tested revision, observed evidence, a remaining risk and a named next action. **Evidence.** Write “ready for this local pilot” or “hold”, with the reason. Label work you directed or observed separately from work run on your own machine.

## 7 · Map the AWS sandbox

At 14:55 open `day05-aws.md`. Use the allocated sandbox for approved non-provisioning checks. Give read and manage actions separate results. If access is blocked, record the exact point and a fallback, then continue the local project. The extension uses the same booking policy with a real provider only after the class has its local proof.

## Personal evidence record

Copy this table into a local Markdown file or your existing progress record. Use fictional titles and masked identifiers. Do not include passwords, tokens, cloud account IDs, ARNs, emails, cookies or command histories.

| Run / revision / port | Caller and action | Prediction | Actual HTTP and SQLite before → after | What I proved / next action |
| --- | --- | --- | --- | --- |
| Thursday baseline | | | | |
| Good and bad sign-in | | | | |
| Visitor, reader and dispatcher POST (one row each) | | | | |
| Reader/dispatcher GET and authorised title validation | | | | |
| Malformed, expired, edited and spoofed calls (one row each) | | | | |
| Targeted and full pytest • support response | | | | |
| Independent reviewer • verdict | | | | |
| AWS observed / blocked / next owner | | | | |

Before finishing, inspect `git status -sb` and your diff. Commit your own code, tests and a sanitised evidence note on your working branch. Share the commit ID and one remaining question about Monday.

**Optional stretches.** (1) Prove a valid token minted for a different API fails here. (2) Design an object-level access test for contractors attached to different sites. (3) When access, time and cleanup are confirmed, follow the Cognito extension and re-run the same role matrix.
