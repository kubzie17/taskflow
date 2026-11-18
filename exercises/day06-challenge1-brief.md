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

Name: fastapi
Version: 0.162.2
Summary: FastAPI framework, high performance, easy to learn, fast to code, ready for production
Home-page: https://github.com/fastapi/fastapi
Author: 
Author-email: Sebastián Ramírez <tiangolo@gmail.com>
License-Expression: MIT
Location: /Users/hannah.blake/Library/Python/3.14/lib/python/site-packages
Requires: annotated-doc, opentelemetry-api, pydantic, starlette, typing-extensions, typing-inspection
Required-by: 
---
Name: starlette
Version: 1.10.0
Summary: The little ASGI library that shines.
Home-page: https://github.com/Kludex/starlette
Author: 
Author-email: Tom Christie <tom@tomchristie.com>
License-Expression: BSD-3-Clause
Location: /Users/hannah.blake/Library/Python/3.14/lib/python/site-packages
Requires: anyio
Required-by: fastapi

## Step 3 — Check dependency metadata

```powershell
python3 -c "from importlib.metadata import version,requires; print(version('fastapi'),version('starlette')); print([d for d in requires('fastapi') if d.lower().startswith('starlette')])"
```
0.162.2 1.10.0
['starlette>=0.46.0']

## Step 4 — Explain the relationship

Answer:

1. Which package does our application select directly? FastAPI
2. Which package is required by that dependency? starlette
3. How could the version of a transitive dependency change? a new version of fastapi could be released with an updated version of starlette
4. What evidence would you need to reproduce your current environment? the current versions of all dependencies

**Success:** You can explain and demonstrate one real direct-to-transitive dependency relationship using your installed environment.
