# Workshop B — Repair the TaskFlow Security Vulnerability

**Client:** Northbridge Repairs

**Scenario**

A tester has reported that TaskFlow's public support-status endpoint is exposing information intended only for internal support.

The public monitoring service requires HTTP 200 and exactly these two values:

```json
{
  "status": "ok",
  "service": "taskflow"
}
```

The support team must still retain its internal diagnostic information.

## Your challenge

Work on your own TaskFlow branch.

### Part 1 — Investigate and reproduce

1. Open `http://127.0.0.1:8044/support/status` in your browser.
2. Compare the actual response with the client's required public response.
3. Identify any information that shouldn't be publicly exposed.
4. Inspect `exercises/day04_candidate.py` to locate the relevant implementation.
5. Record your findings.

### Part 2 — Write a failing security test

Create an automated test using pytest and FastAPI's TestClient.

Your test must verify that the public endpoint returns HTTP 200 and **exactly the approved two-field response**.

Use an isolated temporary SQLite database.

Run your test and capture the failure.

The failure must demonstrate the reported disclosure, not a Python syntax error or incorrect setup.

### Part 3 — Repair the vulnerability

Modify the candidate implementation so that:

- The public endpoint returns only the permitted information.
- The existing local diagnostic function remains available.
- Existing booking and health functionality still works.
- The new regression test passes.

### Part 4 — Independent verification

1. Run the new test.
2. Run the existing pytest suite.
3. Restart the local service and confirm the browser now shows the correct response.
4. Review your Git changes and commit the repair.
5. Have another learner independently verify the exact revision.

## Evidence required

Record in workbook tab **4 Repair**:

- Public response before repair.
- The failing test and its relevant assertion.
- Code changes made.
- Passing test results.
- Public response after repair.
- Git commit reference.
- Partner's independent review result.

## Success criteria

You have demonstrated the vulnerability, written a test that detects it, repaired the implementation without removing the internal support capability, and obtained an independent verification.

**Important:** Investigate first, test second, repair third. Do not skip straight to changing the code.
