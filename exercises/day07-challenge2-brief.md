# Challenge 2 — Trace TaskFlow to SQLite

**Time: 25 minutes**

## Step 1 — Open your TaskFlow repository

Open three PowerShell terminals in VS Code.

Activate your existing Python environment as needed.

## Step 2 — Start the API

**Terminal 1:**

```powershell
python -m exercises.day07_lab api --mode protected --store primary
```

The protected API should listen on port **8071**.

If the protected application cannot start, tell the trainer. Do not reset your Friday work.

## Step 3 — Start the gateway

**Terminal 2:**

```powershell
python -m exercises.day07_lab gateway
```

## Step 4 — Configure and test the gateway

**Terminal 3:**

```powershell
python -m exercises.day07_lab point 8071
python -m exercises.day07_lab call health
```

Expected: HTTP 200.

## Step 5 — Test the application's permissions

Run the following separately:

```powershell
python -m exercises.day07_lab call list
```

```powershell
python -m exercises.day07_lab call list --as reader
```

```powershell
python -m exercises.day07_lab call book --as reader --title "Reader test"
```

```powershell
python -m exercises.day07_lab call book --as dispatcher --title "Dispatch test"
```

Enter your fictional passphrase privately when prompted.

## Step 6 — Inspect SQLite

```powershell
python -m exercises.day07_lab rows --store primary
```

Find the dispatcher's booking.

Record its ID and title.

## Step 7 — Explain what happened

Answer these questions:

1. Which port receives the gateway request?
2. Which port runs FastAPI?
3. What checks the user's permissions?
4. Where is the database located?
5. Why does a successful health check not prove booking permissions work?

**Success:** You can show a dispatcher booking that appears in SQLite and explain why a reader cannot create one.
