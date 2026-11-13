# Challenge 2 — Implement Authentication in TaskFlow

**Time:** 30 minutes  
**Application:** Day 5 protected TaskFlow, port 8055

## Scenario

Northbridge has two fictional employees:

- `reader` — can view bookings.
- `dispatcher` — can view and create bookings.

Before the application can enforce their permissions, it must securely establish who is making each request.

Your task is to implement sign-in and bearer-token verification.

## Step 1 — Initialise your fictional accounts

From your project root:

```powershell
python -m exercises.day05_identity
```

The terminal will prompt you for two different fictional passphrases.

Choose passphrases of at least 12 characters.

The input will be hidden. The generated password hashes and signing key are stored privately under your operating-system user account, outside the repository.

**Do not share, screenshot or commit credentials or token strings.**

If you've already completed this initialisation, do not run it again.

## Step 2 — Start the protected API

```powershell
python -m uvicorn exercises.day05_api:create_secure --factory --host 127.0.0.1 --port 8055 --reload
```

Open:

`http://127.0.0.1:8055/docs`

You should see the protected TaskFlow API.

## Step 3 — Find the incomplete functions

Open:

`exercises/day05_api.py`

Locate:

```python
def sign_in(credentials: SignIn, response: Response):
```

and:

```python
def current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)) -> Principal:
```

These are your first two implementation tasks.

The original starter intentionally returns HTTP 501 at sign-in.

## Step 4 — Inspect the supplied security functions

Open:

`exercises/day05_identity.py`

Locate the `LocalIdentity` methods:

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
| Correct reader credentials | 200 with access token |
| Correct dispatcher credentials | 200 with access token |
| Incorrect password | 401 |
| Unknown username | 401 |
| Protected request without a token | 401 |

**Important:** A successful login does not mean booking creation is ready. The role gate remains unfinished until Challenge 3.

## Evidence to record

- Which functions you completed.
- HTTP results for successful and failed logins.
- The token type and expiry duration.
- Where the password is checked.
- Where token signature and expiry are verified.
- One error you encountered and how you resolved it.

Keep actual passwords and tokens private.
