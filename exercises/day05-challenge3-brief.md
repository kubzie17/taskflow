# Challenge 3 — Enforce Reader and Dispatcher Permissions

**Time:** 50 minutes  
**Application:** Day 5 protected TaskFlow  
**Port:** 8055  
**File to modify:** `exercises/day05_api.py`

## Scenario

Northbridge uses TaskFlow to manage fictional repair tasks.

Two employees have different responsibilities:

- **reader** — can view existing tasks but cannot create new ones.
- **dispatcher** — can view existing tasks and create new ones.

A visitor who has not authenticated cannot access either protected operation.

In Challenge 2, you implemented authentication. TaskFlow can now establish who is making a request using signed bearer tokens.

However, being authenticated does not automatically mean someone should be allowed to perform every operation.

Your challenge is to implement **role-based authorisation** so TaskFlow can decide what each authenticated user is permitted to do.

By the end of this challenge, the application should correctly distinguish between a reader, a dispatcher and an unauthenticated visitor.

**Important:** Challenge 2 established identity. Challenge 3 enforces permissions.

---

## Step 1 — Start TaskFlow

Open a terminal in your TaskFlow project root.

If your server is not already running, start it using:

```powershell
python -m uvicorn exercises.day05_api:create_secure --factory --host 127.0.0.1 --port 8055 --reload
```

Keep the terminal running.

Open your browser:

http://127.0.0.1:8055/docs

You should see the following endpoints:

| Endpoint | Purpose |
|---|---|
| `POST /session` | Sign in and receive an access token |
| `GET /health` | Public service health check |
| `GET /support/status` | Public support status |
| `GET /tasks` | View existing tasks |
| `POST /tasks` | Create a new task |

Notice that both `/tasks` endpoints display a padlock icon.

**Discussion question:** If two users can both log in successfully, should they automatically have permission to perform the same operations? Why or why not?

## Step 2 — Observe the application before changing anything

Before implementing permissions, establish the current behaviour.

### Test A — Sign in as reader

1. Expand `POST /session`.
2. Select **Try it out**.
3. Enter the username `reader` and the fictional passphrase you created during Challenge 2.
4. Select **Execute**.
5. Confirm the response is HTTP `200 OK`.
6. Copy the `access_token` value privately.

Do not screenshot or share the token.

### Test B — Authorise Swagger

1. Scroll to the top of the Swagger page.
2. Select **Authorize**, next to the padlock icon.
3. Paste the token into the bearer authentication field.
4. Do not manually add `Bearer` unless the interface explicitly requests it.
5. Select **Authorize**.
6. Select **Close**.

Swagger should now include the bearer token when making requests to protected endpoints.

### Test C — Attempt to view tasks

1. Expand `GET /tasks`.
2. Select **Try it out**.
3. Select **Execute**.
4. Record the response code and response body.

**Expected before Challenge 3 is implemented:** HTTP `403 Forbidden`.

You may see a message similar to:

```json
{
  "detail": "Permission denied"
}
```

This is because the starter permission function currently rejects every authenticated user.

### Test D — Attempt to create a task

1. Expand `POST /tasks`.
2. Select **Try it out**.
3. Enter a valid fictional task title using Swagger's request-body format.

For example, if the request body uses the `title` field:

```json
{
  "title": "Inspect fictional signal cabinet"
}
```

4. Select **Execute**.
5. Record the response code.

**Expected before implementation:** HTTP `403 Forbidden`.

Even a dispatcher would currently receive 403 because the permission decision has not been completed.

**Checkpoint:** You have now confirmed that authentication is working but authorisation is still preventing access.

## Step 3 — Locate the unfinished permission function

Open the following file in VS Code:

`exercises/day05_api.py`

Find:

```python
def permit(*allowed: str):
```

Read the entire function, including the nested `gate()` function.

Next, find the two protected API routes:

```python
@api.get("/tasks", ...)
```

and:

```python
@api.post("/tasks", ...)
```

Examine how each route uses `permit()`.

The routes already specify which roles are permitted to perform the corresponding operations.

**Your task is to implement the permission decision, not redesign the routes.**

Before coding, answer:

1. Where does `gate()` obtain the authenticated user's identity?
2. Where are the allowed roles for each endpoint defined?
3. Why does the current implementation return 403 for everyone?
4. What should happen when the authenticated user's role is permitted?
5. What should happen when it is not permitted?

Do not change `sign_in()` or `current_user()` if they are already working correctly from Challenge 2.

## Step 4 — Implement role-based authorisation

Complete the `permit()` function in `exercises/day05_api.py`.

Your implementation must:

1. Use the already authenticated `Principal` supplied by `current_user()`.
2. Determine the trusted role associated with the authenticated identity.
3. Compare that role against the roles permitted for the requested operation.
4. Allow the operation to continue when the role is permitted.
5. Reject an authenticated user with HTTP `403 Forbidden` when their role is not permitted.
6. Never accept a role supplied through an untrusted request header or task body.

The decision must happen before the protected operation is allowed to access or change the database.

**Do not hard-code a username-specific exception.** Your decision should be based on the authenticated role and the endpoint's permitted roles.

Save your file.

Because Uvicorn is running with `--reload`, it should automatically restart the application.

Watch the server terminal for errors before continuing.

## Step 5 — Understand the database checks

This challenge is not only about returning the correct HTTP response.

You must also demonstrate that an unauthorised request **does not create or modify database records**.

TaskFlow stores its lab tasks in:

`data/day05-lab.db`

Open a second terminal in your project root.

Leave the API server running in the first terminal.

Run the following command:

```powershell
python -c "import sqlite3; c=sqlite3.connect('file:data/day05-lab.db?mode=ro',uri=True); print(c.execute('select id,title from tasks order by id').fetchall()); c.close()"
```

This reads existing task IDs and titles from the SQLite database.

Example output might resemble:

```text
[(1, 'Inspect signal cabinet'), (2, 'Review maintenance record')]
```

Your own database may contain different records or may initially be empty:

```text
[]
```

Both are fine.

The important thing is to compare the results **before and after** requests that should be rejected.

### How to check whether a request changed the database

1. Run the SQLite command.
2. Record the existing list of IDs and titles.
3. Submit the API request you want to test.
4. Run the same SQLite command again.
5. Compare both results.

If a request was denied, the complete list should remain identical.

If a dispatcher successfully creates a task, you should see one new record.

**Important:** The database is being inspected directly for testing purposes. Do not manually insert or delete rows to make your results match.

## Step 6 — Test an unauthenticated visitor

First, remove any existing Swagger authorisation.

1. Select **Authorize**.
2. Select **Logout**.
3. Close the authorisation window.

### Test E — Visitor tries to view tasks

1. Expand `GET /tasks`.
2. Select **Try it out**.
3. Select **Execute**.

**Expected:** HTTP `401 Unauthorized`.

An unauthenticated visitor should not be able to view protected tasks.

### Test F — Visitor tries to create a task

Before starting, run the SQLite inspection command from Step 5 and record its output.

Then:

1. Expand `POST /tasks`.
2. Select **Try it out**.
3. Enter a valid task body, for example:

```json
{
  "title": "Visitor attempted repair task"
}
```

4. Select **Execute**.

**Expected:** HTTP `401 Unauthorized`.

Now run the SQLite inspection command again.

**Expected database result:** No new record. The before and after lists should be identical.

**Checkpoint:** Both protected operations reject visitors without valid authentication.

## Step 7 — Test the reader account

Now check whether the reader can perform only the operations appropriate to their role.

### Test G — Sign in and authorise

1. Expand `POST /session`.
2. Select **Try it out**.
3. Enter the correct `reader` username and passphrase.
4. Select **Execute**.
5. Confirm HTTP `200`.
6. Copy the access token privately.
7. Select **Authorize** at the top of Swagger.
8. Paste the token and select **Authorize → Close**.

### Test H — Reader views tasks

1. Expand `GET /tasks`.
2. Select **Try it out**.
3. Select **Execute**.

**Expected:** HTTP `200 OK`.

The response should contain a JSON list of tasks. An empty list is acceptable when no tasks have been created.

This confirms the reader is permitted to perform a read operation.

### Test I — Reader attempts to create a task

First, run the SQLite inspection command and record the existing rows.

Then:

1. Expand `POST /tasks`.
2. Select **Try it out**.
3. Enter:

```json
{
  "title": "Reader attempted repair task"
}
```

4. Select **Execute**.

**Expected:** HTTP `403 Forbidden`.

The reader is authenticated but does not have permission to create tasks.

Run the SQLite inspection command again.

**Expected database result:** The existing rows must be unchanged. There should be no new task with the attempted title.

**Checkpoint:** The reader can view tasks but cannot create them.

## Step 8 — Test the dispatcher account

The dispatcher should be able to view and create tasks.

### Test J — Switch accounts

Before testing another user, remove the reader's token.

1. Select **Authorize**.
2. Select **Logout**.
3. Close the window.
4. Expand `POST /session`.
5. Sign in using the correct `dispatcher` credentials.
6. Select **Execute**.
7. Confirm HTTP `200`.
8. Copy the new dispatcher access token privately.
9. Select **Authorize**, paste the dispatcher token and select **Authorize → Close**.

You should now be making authenticated requests as `dispatcher`.

### Test K — Dispatcher views tasks

1. Expand `GET /tasks`.
2. Select **Try it out**.
3. Select **Execute**.

**Expected:** HTTP `200 OK`.

You should see the current task list.

### Test L — Dispatcher creates a task

First, run the SQLite inspection command and record the existing rows.

Next:

1. Expand `POST /tasks`.
2. Select **Try it out**.
3. Enter:

```json
{
  "title": "Inspect fictional station equipment"
}
```

4. Select **Execute**.

**Expected:** HTTP `201 Created`.

The response should include the newly created task's ID and title.

Record the ID and title without changing them.

### Test M — Confirm the new task was stored

1. Run the SQLite inspection command again.
2. Compare it with the earlier output.
3. Look for the newly created task ID and title.

**Expected:** One additional task should appear.

Next, return to Swagger:

1. Expand `GET /tasks`.
2. Select **Try it out → Execute**.
3. Find the new task in the returned JSON list.

**Expected:** HTTP `200 OK`, with the newly created task included.

**Checkpoint:** The dispatcher can successfully create a task, and it is stored in SQLite.

## Step 9 — Test request validation

Being authorised does not mean a user can submit any data they want.

TaskFlow must still validate incoming request bodies.

Remain authenticated as `dispatcher`.

### Test N — Submit an excessively long title

The application should reject task titles exceeding its permitted length.

Your task is to test a title containing exactly **101 characters**.

To generate 101 characters without counting manually, run this in a separate terminal:

```powershell
python -c "print('X' * 101)"
```

Copy the resulting string.

Before making the request, inspect and record the current SQLite rows.

Then:

1. Open `POST /tasks`.
2. Select **Try it out**.
3. Enter the required JSON request body.
4. Paste the 101-character string as the title.
5. Select **Execute**.

**Expected:** HTTP `422 Unprocessable Entity`.

The request should fail validation.

Run the SQLite inspection command again.

**Expected database result:** No new task has been added.

**Discussion question:** What is the difference between rejecting a request because a user lacks permission and rejecting it because the submitted data is invalid?

## Step 10 — Verify public endpoints still work

Authentication and authorisation should protect only the endpoints that require protection.

Remove Swagger authorisation:

**Authorize → Logout → Close**

Now open these URLs directly in your browser:

http://127.0.0.1:8055/health

http://127.0.0.1:8055/support/status

### Public health endpoint

**Expected:** HTTP `200 OK`.

The response should contain the service's health information.

### Public support status

**Expected:** HTTP `200 OK`.

The response body must contain exactly these two fields:

- `status`
- `service`

Neither public endpoint should require a bearer token.

**Checkpoint:** Protected operations enforce access rules while public status endpoints remain accessible.

---

## Step 11 — Complete the testing checklist

Record the actual HTTP results from Swagger.

| Test | Expected HTTP | Actual HTTP |
|---|---|---|
| Visitor — `GET /tasks` | 401 | |
| Visitor — `POST /tasks` | 401 | |
| Reader — `GET /tasks` | 200 | |
| Reader — `POST /tasks` | 403 | |
| Dispatcher — `GET /tasks` | 200 | |
| Dispatcher — valid `POST /tasks` | 201 | |
| Dispatcher — 101-character title | 422 | |
| Public `GET /health` | 200 | |
| Public `GET /support/status` | 200 | |

### Expected database behaviour

| Request | Database result |
|---|---|
| Visitor attempts to create a task | No change |
| Reader attempts to create a task | No change |
| Dispatcher creates a valid task | One new row |
| Dispatcher submits 101-character title | No change |

If your actual result differs from the expected result, investigate it before marking the test as passed.

## Step 12 — Troubleshooting

### Problem: GET /tasks still returns 403 for dispatcher

Check that you saved the file, the server reloaded successfully and the permission function no longer rejects all authenticated requests.

Also verify that Swagger is using the dispatcher token rather than the reader token.

### Problem: GET /tasks returns 401

Check that you are authorised in Swagger and that the access token has not expired.

Tokens issued during Challenge 2 last 600 seconds (10 minutes).

If necessary, sign in again to obtain a new token.

### Problem: POST /tasks returns 422 instead of 201

Inspect the request-body format in Swagger.

Check that the JSON contains the expected field and that the title meets the application's validation requirements.

### Problem: POST /tasks returns 403 for dispatcher

Confirm that you logged out of the reader account and authorised Swagger with a new dispatcher token.

Then inspect the permission decision and the roles declared by the route.

### Problem: A rejected POST changes the database

This indicates that the security or validation behaviour needs investigation.

Check that requests are rejected before the operation that writes to SQLite is permitted to run.

Do not consider the challenge complete until denied writes leave the database unchanged.

### Problem: The SQLite command fails

Check that:

- You are in the TaskFlow project root.
- The server has started successfully and initialised the lab database.
- The expected database file exists at `data/day05-lab.db`.

Do not create or edit SQLite tables manually as part of troubleshooting this challenge.

---

## Step 13 — Evidence to record

At the end of the challenge, record:

1. The file and function you modified.
2. Where the allowed roles for each route are declared.
3. The HTTP results for the visitor, reader and dispatcher.
4. Which requests successfully read or created tasks.
5. The SQLite rows before and after each attempted task creation.
6. Evidence that the reader's denied request did not create a row.
7. Evidence that the dispatcher's successful request created exactly one row.
8. Evidence that a 101-character title was rejected without changing the database.
9. One error you encountered and how you resolved it.

Do not include actual passwords, access tokens or signing keys in your evidence.

## Completion criteria

You have completed Challenge 3 when:

- Unauthenticated visitors receive HTTP 401 for protected operations.
- The reader can view tasks but cannot create them.
- The dispatcher can view and create tasks.
- Valid task creation returns HTTP 201.
- Requests containing an invalid task title are rejected with HTTP 422.
- Denied or invalid writes do not modify the database.
- Public health and support endpoints remain accessible.

### Final discussion

Consider these questions:

**1. Authentication vs authorisation:** Why is a valid access token not sufficient to grant every operation?

**2. Least privilege:** Why should the reader be denied permission to create tasks?

**3. Database integrity:** Why is checking the SQLite rows important, even when the API returns the expected HTTP error?

**4. Security design:** What could go wrong if TaskFlow trusted a role supplied in a request header or JSON body?

**5. Real-world application:** How might these permission rules apply to a railway maintenance, booking or work-order management system?

**End of Challenge 3 — Role-Based Authorisation**