# Challenge 5 — Prove Your Security Controls Work

**Time:** 35 minutes  
**Application:** Day 5 TaskFlow, port 8055

## Step 1 — Create your test file

From your project root:

```powershell
Copy-Item .\exercises\day05_test_starter.py .\tests\test_day05_access.py
```

Open:

`tests/test_day05_access.py`

The starter provides a temporary database, a test client, fictional accounts and the `rows(db_path)` helper.

## Step 2 — Write these automated tests

**Test A — Visitor**

- Attempt `POST /tasks` without credentials.
- Expect HTTP 401.
- Verify SQLite is unchanged.

**Test B — Reader**

- Authenticate as reader through `POST /session`.
- Attempt `POST /tasks`.
- Expect HTTP 403.
- Verify SQLite is unchanged.

**Test C — Dispatcher**

- Authenticate as dispatcher.
- Create a valid booking.
- Expect HTTP 201.
- Verify exactly one new booking was stored.

**Test D — Invalid token**

- Attempt to create a booking using a malformed token.
- Expect HTTP 401.
- Verify SQLite is unchanged.

**Stretch:** Test an expired token, a tampered token and a 101-character title submitted by a dispatcher.

## Step 3 — Run the tests

```powershell
python -m pytest tests/test_day05_access.py -q
```

Fix any implementation or test failures.

Then run:

```powershell
python -m pytest -q
```

## Success criteria

You can demonstrate the correct responses for visitors, readers and dispatchers, and prove through automated tests that rejected booking requests do not change the database.

Record your test results and Git revision.
