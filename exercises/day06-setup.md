# Day 6 — TaskFlow Setup

**Date:** Monday 16 November 2026

We are continuing the same TaskFlow repository from Days 1–5. Do not start a new project.

## Step 1 — Open your existing project

Open VS Code in the folder containing:

- `app/`
- `exercises/`
- `tests/`
- `requirements.txt`

Open PowerShell and run:

```powershell
git status -sb
git branch --show-current
git rev-parse --short HEAD
```

Record your branch and revision.

If you have unfinished Friday work, save or commit your intended changes before bringing in the new files.

## Step 2 — Import the Day 6 materials

Use the Git update method provided by the trainer.

If your branch cleanly tracks the class materials branch:

```powershell
git pull --ff-only
```

If you have a personal working branch, fetch and cherry-pick the specific Day 6 materials commit supplied by the trainer:

```powershell
git fetch origin
git cherry-pick <DAY6_MATERIALS_COMMIT>
```

Replace `<DAY6_MATERIALS_COMMIT>` with the real published commit ID.

If you cloned your own repository from a template, you may need to fetch the materials from the trainer's repository first.

If you have a conflict, **do not force the operation or discard your work**. Ask for assistance.

If Git updates are unavailable, the trainer can supply the incremental Day 6 learner ZIP.

## Step 3 — Check the Day 6 files

You should now have:

```text
exercises/
  day06.md
  day06-evidence.md
  day06-case.md
  day06-proposal.case
  day06_gate.py
  day06_incident.py
  day06_context_probe.py
  day06_workflow_check.py

docs/
  day06-workflow-review.yml
```

These are supporting materials and challenge files. Some are deliberately insecure or incomplete for investigation.

## Step 4 — Activate Python

Use your existing Python 3.12 virtual environment.

For example:

```powershell
.\.venv\Scripts\Activate.ps1
```

If yours is called `venv`, use that folder instead.

## Step 5 — Check your environment

From the project root:

```powershell
python --version
python exercises/day06_gate.py check
python -c "from importlib.metadata import version; print(version('PyJWT'))"
python -m pytest -q
git ls-files .github/workflows
```

The published Day 5 course file specifies PyJWT 2.15.1.

If your installed version differs, report it. Do not install the older version suggested by today's fictional vendor.

If required, install the existing approved course dependencies:

```powershell
python -m pip install -r requirements.txt -r exercises/day05-requirements.txt
```

## Step 6 — Prepare your evidence

Open:

`exercises/day06-evidence.md`

Save a personal copy for recording your results.

Create a Day 6 working branch from your saved Friday work when your repository is in a suitable state:

```powershell
git switch -c day06-yourname
```

Replace `yourname` with your identifier.

Keep fictional credentials and actual access tokens out of Teams, screenshots and Git.
