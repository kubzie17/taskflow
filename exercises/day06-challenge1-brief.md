# Mini-Task — Investigate TaskFlow's Dependencies

**Time:** Approximately 10 minutes

## Step 1 — Open the requirements

Inspect:

`requirements.txt`

Identify the entry for FastAPI.

## Step 2 — Inspect installed packages

From the activated project environment:

```powershell
python -m pip show fastapi starlette
```

Record:

- Installed FastAPI version.
- Installed Starlette version.
- The `Requires` and `Required-by` fields.

## Step 3 — Check dependency metadata

```powershell
python -c "from importlib.metadata import version,requires; print(version('fastapi'),version('starlette')); print([d for d in requires('fastapi') if d.lower().startswith('starlette')])"
```

## Step 4 — Explain the relationship

Answer:

1. Which package does our application select directly?
2. Which package is required by that dependency?
3. How could the version of a transitive dependency change?
4. What evidence would you need to reproduce your current environment?

**Success:** You can explain and demonstrate one real direct-to-transitive dependency relationship using your installed environment.
