# Monday Catch-Up — Complete Friday's Challenge 5

**Time:** Until 10:25  
**Application:** Day 5 protected TaskFlow

We're continuing the pytest security challenge from Friday, not starting authentication again.

### Step 1 — Open your existing test file

Open:

`tests/test_day05_access.py`

If you didn't create it on Friday, copy the supplied starter:

```powershell
Copy-Item .\exercises\day05_test_starter.py .\tests\test_day05_access.py
```

Inspect the supplied `lab` fixture and `rows(db_path)` helper.

### Step 2 — Complete the essential tests

| Test | Required result |
|---|---|
| Visitor POST /tasks | 401, database unchanged |
| Reader POST /tasks | 403, database unchanged |
| Dispatcher POST /tasks | 201, booking stored |
| Malformed bearer token POST /tasks | 401, database unchanged |

For the reader and dispatcher tests, authenticate through `POST /session` and use the returned token privately.

**Stretch, if you have time:** Expired token, tampered token, dispatcher invalid title (422).

### Step 3 — Run pytest

```powershell
python -m pytest tests/test_day05_access.py -q
```

Fix or document any failures.

Then run the whole suite:

```powershell
python -m pytest -q
```

### Step 4 — Record your results

Record:

- Tests completed and passing.
- Any outstanding failures.
- Proof that rejected requests leave SQLite unchanged.
- Your Git revision.

**Success:** You have automated evidence that TaskFlow permits authorised booking creation and prevents unauthorised database writes.

If you finish early, investigate why these tests are important to a CI/CD pipeline — we'll use them again in today's GitHub Actions workshop.
