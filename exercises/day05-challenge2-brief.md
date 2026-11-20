# Challenge 2 — Implement Authentication in TaskFlow

**Time:** 30–40 minutes  
**Application:** Day 5 protected TaskFlow  
**Port:** 8055  
**File to modify:** `exercises/day05_api.py`

## Scenario

Northbridge has two fictional employees:

- **reader** — should be able to view tasks.
- **dispatcher** — should be able to view and create tasks.

Before TaskFlow can decide what each employee is allowed to do, it must first establish who is making each request.

Your challenge is to implement authentication using usernames, passwords and signed bearer tokens.

By the end, both fictional employees should be able to sign in, receive a token and use that token when requesting protected resources.

**Important:** You are implementing authentication (who someone is), not authorisation (what they are allowed to do). Role-based permissions will be completed in Challenge 3.

---

## Step 1 — Initialise your fictional accounts

Open a terminal in your TaskFlow project root.

Run:

```powershell
python3 -m exercises.day05_identity
```

Follow the terminal instructions to set up two fictional accounts:

- `reader`
- `dispatcher`

Choose a different passphrase for each account, with at least 12 characters.

The passphrase input will be hidden.

The application securely stores the generated password hashes and signing key outside your project repository.

**Security rules:**

- Never share your passphrases.
- Never screenshot or share access tokens.
- Never commit credentials or tokens to GitHub.

**Already completed this step?** Do not run the initialisation again.

## Step 2 — Start the protected TaskFlow API

From your project root, run:

```powershell
python3 -m uvicorn exercises.day05_api:create_secure --factory --host 127.0.0.1 --port 8055 --reload
```

Keep this terminal running.

Open your browser and navigate to:

http://127.0.0.1:8055/docs

You should see the TaskFlow Swagger interface containing these endpoints:

| Endpoint | Purpose |
|---|---|
| `POST /session` | Sign in to receive a token |
| `GET /health` | Public health check |
| `GET /support/status` | Public service status |
| `GET /tasks` | Protected endpoint for viewing tasks |
| `POST /tasks` | Protected endpoint for creating tasks |

Notice that both `/tasks` endpoints have a lock icon.

**Discussion question:** Why do some endpoints have lock icons while others do not?

## Step 3 — Test the application before changing any code

Before implementing authentication, observe what currently works and what does not.

### Test A — Check the public health endpoint

1. Expand `GET /health`.
2. Select **Try it out**.
3. Select **Execute**.
4. Look at the response code and body.

**Expected:** HTTP `200 OK`, with a JSON response indicating that the service is running.

This endpoint does not require authentication.

### Test B — Attempt to sign in

1. Expand `POST /session`.
2. Select **Try it out**.
3. Enter the following JSON, replacing the placeholder password with the fictional passphrase you created:

```json
{
  "username": "reader",
  "password": "YOUR_READER_PASSPHRASE"
}
```

4. Select **Execute**.
5. Read the HTTP response code.

**Expected before implementation:** HTTP `501 Not Implemented`.

This is intentional. The starter application has an unfinished sign-in function.

### Test C — Attempt to view tasks without signing in

1. Expand `GET /tasks`.
2. Select **Try it out**.
3. Select **Execute**.
4. Record the HTTP response code.

**Expected:** HTTP `401 Unauthorized`, provided the missing-token check is already implemented. Otherwise, record the result for comparison after your changes.

**Think about:** Why should a protected endpoint behave differently from `/health`?

## Step 4 — Locate the unfinished authentication functions

Open the following file in VS Code:

`exercises/day05_api.py`

Find these two functions:

```python
def sign_in(credentials: SignIn, response: Response):
```

```python
def current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer)
) -> Principal:
```

These are the **only two functions you need to complete for Challenge 2**.

Before making changes, identify:

- Which function handles usernames and passwords?
- Which function handles tokens supplied with API requests?
- What currently happens when either function cannot complete its task?

Do not modify the role-based permission function `permit()` yet.

## Step 5 — Inspect the existing identity provider

Open:

`exercises/day05_identity.py`

Find the `LocalIdentity` class and examine these methods:

- `check_password(username, password)`
- `issue(principal)`
- `verify(token)`

Identify what each method accepts and returns.

Do not modify the supplied password-hashing or token-verification implementation for this challenge.

## Step 5 — Implement sign-in

Complete `sign_in()` so that:

1. It accepts a fictional username and password.
2. It checks the credentials against the supplied local identity provider.
3. It rejects unknown users and incorrect passwords with HTTP 401.
4. It issues a signed access token when credentials are correct.
5. It returns the token, bearer type and its 600-second lifetime.
6. It sets `Cache-Control: no-store` on a successful token response.

Do not accept a role from the caller's login request. Roles must come from the trusted identity store.

curl -X 'POST' \
  'http://127.0.0.1:8055/session' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "reader",
  "password": "password123456789"
}'

	
Response body
200
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1cm46bm9ydGhicmlkZ2U6dGFza2Zsb3c6bGFiIiwiYXVkIjoidXJuOm5vcnRoYnJpZGdlOnRhc2tmbG93OmJvb2tpbmdzIiwic3ViIjoicmVhZGVyIiwiaWF0IjoxNzk0NTY5OTIzLCJleHAiOjE3OTQ1NzA1MjMsInRva2VuX3VzZSI6ImFjY2VzcyIsInJvbGVzIjpbInJlYWRlciJdfQ.pTEU1-vhVr0wus280Ifzv9AMUO0vzJiPCQf7BAHQ7UM",
  "token_type": "bearer",
  "expires_in": 600
}

Response headers
 cache-control: no-store 
 content-length: 365 
 content-type: application/json 
 date: Fri,13 Nov 2026 11:38:42 GMT 
 server: uvicorn 


curl -X 'POST' \
  'http://127.0.0.1:8055/session' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "dispatcher",
  "password": "password987654321"
}'

	
Response body
200
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1cm46bm9ydGhicmlkZ2U6dGFza2Zsb3c6bGFiIiwiYXVkIjoidXJuOm5vcnRoYnJpZGdlOnRhc2tmbG93OmJvb2tpbmdzIiwic3ViIjoiZGlzcGF0Y2hlciIsImlhdCI6MTc5NDU3MDAzOSwiZXhwIjoxNzk0NTcwNjM5LCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJyb2xlcyI6WyJkaXNwYXRjaGVyIl19.YVKSwKyDtHKa-a8TDbkVsnHCtKj4S7Zn5H_90IUi4_4",
  "token_type": "bearer",
  "expires_in": 600
}
Response headers
 cache-control: no-store 
 content-length: 375 
 content-type: application/json 
 date: Fri,13 Nov 2026 11:40:39 GMT 
 server: uvicorn 


curl -X 'POST' \
  'http://127.0.0.1:8055/session' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "dispatcher",
  "password": "wrongpassword"
}'
	
Response body
401
{
  "detail": "Authentication required"
}
Response headers
 content-length: 36 
 content-type: application/json 
 date: Fri,13 Nov 2026 11:42:15 GMT 
 server: uvicorn 
 www-authenticate: Bearer 

curl -X 'POST' \
  'http://127.0.0.1:8055/session' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "wrongusername",
  "password": "password123456789"
}'

Response body
401
{
  "detail": "Authentication required"
}
Response headers
 content-length: 36 
 content-type: application/json 
 date: Fri,13 Nov 2026 11:43:02 GMT 
 server: uvicorn 
 www-authenticate: Bearer 

## Step 6 — Implement the current-user check

Complete `current_user()` so that:

1. A request without a bearer token is rejected with HTTP 401.
2. A malformed or invalid bearer token is rejected with HTTP 401.
3. A valid token is verified using the supplied identity provider.
4. The trusted `Principal` is returned for the request.

## Step 7 — Verify your implementation

In `/docs`, open `POST /session`.

Select **Try it out**.

Sign in using your fictional `reader` account.

Check the HTTP result without sharing the actual access token.

Repeat for `dispatcher`.

Then test an incorrect password and an unknown username.

Finally, attempt to access a protected route without a token.

**Expected outcomes**

| Test | Expected |
|---|---|
| `check_password(username, password)` | Checks whether supplied credentials are valid |
| `issue(principal)` | Creates a signed access token |
| `verify(token)` | Verifies a token and retrieves the trusted identity |

For each method, determine what arguments it expects and what it returns.

**Important:** The password-hashing and token-signing functionality has already been supplied. Your job is to integrate it into the TaskFlow API.

Do not modify `day05_identity.py`.

## Step 6 — Implement sign-in

Return to:

`exercises/day05_api.py`

Complete the `sign_in()` function.

Your implementation must:

1. Accept a fictional username and password.
2. Check the credentials using the existing identity provider.
3. Reject incorrect passwords and unknown users with HTTP `401`.
4. Issue a signed access token for valid credentials.
5. Return the access token, bearer token type and lifetime of `600` seconds.
6. Set the successful response header `Cache-Control: no-store`.

Roles must come from the trusted identity provider. Do not accept a role supplied by someone attempting to sign in.

**Checkpoint:** Save your file. Since Uvicorn uses `--reload`, the server should automatically reload your changes.

### Test D — Sign in as reader

Return to Swagger:

http://127.0.0.1:8055/docs

1. Open `POST /session`.
2. Select **Try it out**.
3. Enter the correct `reader` username and passphrase.
4. Select **Execute**.

**Expected:** HTTP `200 OK`.

The response should contain three fields:

- `access_token` — a signed token.
- `token_type` — `bearer`.
- `expires_in` — `600`.

You do not need to understand or decode the token to complete this challenge.

Do not screenshot or share its value.

### Test E — Sign in as dispatcher

Repeat Test D using the `dispatcher` username and its correct passphrase.

**Expected:** HTTP `200 OK`, with the same three response fields.

### Test F — Incorrect password

Attempt to sign in as `reader`, but deliberately enter an incorrect password.

**Expected:** HTTP `401 Unauthorized`, without an access token.

### Test G — Unknown username

Attempt to sign in using an account that does not exist.

For example:

```json
{
  "username": "unknown_employee",
  "password": "incorrect-password"
}
```

**Expected:** HTTP `401 Unauthorized`, without an access token.

**Checkpoint:** If Tests D–G produce their expected responses, your sign-in functionality is behaving correctly.

## Step 7 — Implement bearer-token authentication

Now complete the second function:

`current_user()`

This function is responsible for checking requests to protected endpoints.

Your implementation must:

1. Check whether the request contains bearer credentials.
2. Reject missing bearer tokens with HTTP `401`.
3. Reject malformed or invalid bearer tokens with HTTP `401`.
4. Use the supplied identity provider to verify a token.
5. Return the trusted `Principal` for a successfully verified token.

Do not implement role-based permissions yet.

Save the file and allow the server to reload.

## Step 8 — Test requests without a token

Return to Swagger.

First, make sure you are not already authenticated:

1. Select **Authorize** at the top of Swagger.
2. If a token is already authorised, select **Logout**.
3. Close the authorisation window.

Now:

1. Expand `GET /tasks`.
2. Select **Try it out**.
3. Select **Execute**.

**Expected:** HTTP `401 Unauthorized`.

This means the application did not receive valid authentication credentials.

Repeat the test with `POST /tasks`, supplying a valid task body if Swagger requires one.

**Expected:** HTTP `401 Unauthorized` for a correctly formed request without authentication.

## Step 9 — Test a valid reader token

This test checks whether the application can recognise a signed-in user.

### Part A — Obtain a token

1. Open `POST /session`.
2. Sign in with the correct `reader` credentials.
3. Confirm HTTP `200`.
4. Copy the value of `access_token` from the response.

Keep the token private.

### Part B — Authorise Swagger

1. Scroll to the top of Swagger.
2. Select the **Authorize** button with the padlock icon.
3. Find the bearer authentication field.
4. Paste your access token into the field.
5. Select **Authorize**.
6. Select **Close**.

For HTTP bearer authentication, Swagger normally adds the `Bearer` prefix automatically. Paste the token itself, without quotation marks.

### Part C — Access the protected endpoint

1. Expand `GET /tasks`.
2. Select **Try it out**.
3. Select **Execute**.
4. Observe the HTTP response.

**Expected during Challenge 2: HTTP `403 Forbidden`.**

This is intentional.

Your application should now recognise the token, but the next security check — role-based permission checking — has not been implemented.

The unfinished permission function currently rejects all authenticated users.

**Do not change the permission function to make this test return 200.**

That is the purpose of Challenge 3.

## Step 10 — Test a valid dispatcher token

1. Select **Authorize**.
2. Select **Logout** to remove the reader token.
3. Close the authorisation window.
4. Sign in through `POST /session` using the `dispatcher` credentials.
5. Copy the new access token privately.
6. Select **Authorize** and enter the dispatcher token.
7. Execute `GET /tasks`.

**Expected during Challenge 2:** HTTP `403 Forbidden`.

You can also attempt `POST /tasks` with a valid task body.

**Expected during Challenge 2:** HTTP `403 Forbidden`.

Both roles are authenticated, but neither is permitted through the unfinished role gate.

In Challenge 3, you will implement the rules that allow the dispatcher to create tasks and prevent the reader from doing so.

## Step 11 — Test an invalid token

Next, confirm that the application does not blindly trust any token.

1. Select **Authorize → Logout**.
2. Select **Authorize** again.
3. Enter the following deliberately invalid token:

```text
this.is.not.a.valid.token
```

4. Select **Authorize → Close**.
5. Expand `GET /tasks`.
6. Select **Try it out → Execute**.

**Expected:** HTTP `401 Unauthorized`.

A malformed or invalid token must not be accepted as proof of identity.

## Step 12 — Optional challenge: test token expiry

Access tokens are valid for 600 seconds (10 minutes).

1. Sign in using `POST /session`.
2. Authorise Swagger with the returned token.
3. Wait until at least 10 minutes have passed since the token was issued.
4. Execute `GET /tasks` using that same token without signing in again.

**Expected:** HTTP `401 Unauthorized`.

**Discussion question:** Why might short-lived access tokens be safer than tokens that never expire?

---

## Final testing checklist

Use the table below to confirm your implementation.

| Test | Expected HTTP result |
|---|---|
| Public `GET /health` | 200 |
| Valid reader sign-in | 200 |
| Valid dispatcher sign-in | 200 |
| Incorrect password | 401 |
| Unknown username | 401 |
| `GET /tasks` without token | 401 |
| `GET /tasks` with invalid token | 401 |
| `GET /tasks` with valid reader token | **403** |
| `GET /tasks` with valid dispatcher token | **403** |
| `POST /tasks` with valid dispatcher token | **403** |
| Expired token (optional) | 401 |

### Understanding the response codes

| HTTP code | Meaning in this challenge |
|---|---|
| **200 OK** | The request completed successfully |
| **401 Unauthorized** | Authentication is missing, incorrect or expired |
| **403 Forbidden** | The request reached the permission gate but was denied |
| **501 Not Implemented** | The sign-in functionality has not yet been completed |

**Remember:** A 403 when using a valid token is expected for Challenge 2. Do not attempt to remove it by changing the permission function.

## Evidence to record

At the end of the challenge, record:

Keep actual passwords and tokens private.


{
  "title": "reader-test"
}
Execute
Clear
Responses
Curl

curl -X 'POST' \
  'http://127.0.0.1:8055/tasks' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1cm46bm9ydGhicmlkZ2U6dGFza2Zsb3c6bGFiIiwiYXVkIjoidXJuOm5vcnRoYnJpZGdlOnRhc2tmbG93OmJvb2tpbmdzIiwic3ViIjoicmVhZGVyIiwiaWF0IjoxNzk0NTcxOTU1LCJleHAiOjE3OTQ1NzI1NTUsInRva2VuX3VzZSI6ImFjY2VzcyIsInJvbGVzIjpbInJlYWRlciJdfQ.dK5o_FAspsEi16phhx0eUZir4YdkiJ9Q7MWvLM3BHtM' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "reader-test"
}'
Request URL
http://127.0.0.1:8055/tasks
Server response
Code	Details
403
Undocumented
Error: Forbidden

Response body
Download
{
  "detail": "Insufficient privilege to access resource"
}
Response headers
 content-length: 54 
 content-type: application/json 
 date: Fri,13 Nov 2026 12:14:40 GMT 
 server: uvicorn 



curl -X 'POST' \
  'http://127.0.0.1:8055/tasks' \
  -H 'accept: */*' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1cm46bm9ydGhicmlkZ2U6dGFza2Zsb3c6bGFiIiwiYXVkIjoidXJuOm5vcnRoYnJpZGdlOnRhc2tmbG93OmJvb2tpbmdzIiwic3ViIjoiZGlzcGF0Y2hlciIsImlhdCI6MTc5NDU3MjExNSwiZXhwIjoxNzk0NTcyNzE1LCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJyb2xlcyI6WyJkaXNwYXRjaGVyIl19.d3inMDdO1NVNWVHeua8n_dh-g7TaMn6LoPIIpMuqIcU' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "dispatcher-test"
}'
Request URL
http://127.0.0.1:8055/tasks
Server response
Code	Details
201	
Response body
Download
{
  "title": "dispatcher-test",
  "id": 1
}
Response headers
 content-length: 34 
 content-type: application/json 
 date: Fri,13 Nov 2026 12:15:36 GMT 
 server: uvicorn 
1. The two functions you completed and the file containing them.
2. The HTTP results for successful reader and dispatcher logins.
3. The HTTP results for incorrect passwords and unknown usernames.
4. The response when accessing `GET /tasks` without a token.
5. The response when accessing `GET /tasks` with a valid token.
6. The bearer token type and expiry duration.
7. Where passwords are checked and where token signatures and expiry are verified.
8. One error you encountered and how you resolved it.

**Never include actual passwords, signing keys or access tokens in your evidence.**

## Completion criteria

You have completed Challenge 2 when:

- Both fictional employees can sign in successfully.
- Invalid login credentials are rejected.
- Valid sign-ins return signed bearer tokens.
- Protected endpoints reject missing or invalid tokens.
- Valid tokens are accepted by the authentication check and reach the unfinished permission gate.

**Next: Challenge 3 — Role-Based Authorisation**

You will implement the missing permission rules so that:

- `reader` can view tasks but cannot create them.
- `dispatcher` can view and create tasks.
- Unauthenticated requests continue to be rejected.
