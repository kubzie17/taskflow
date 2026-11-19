# Day 9 — Challenge 1: Secure the TaskFlow Build

**Time:** Morning workshop until 11:50  
**Objective:** Produce a tested protected Docker image and publish it to AWS ECR through a controlled GitHub Actions workflow.

## Scenario

Northbridge wants to release TaskFlow, but the original Docker image runs the historical application.

You need to package the protected version and ensure that any failing security check blocks the release.

## Step 1 — Open the new files

In your existing TaskFlow repository, open:

- `exercises/day09_entry.py`
- `Dockerfile.day09`
- `Dockerfile.day09.dockerignore`
- `docs/day09-workflow-starter.yml`
- `tests/test_day09_runtime.py`
- `exercises/day09-challenge1-brief.md`

Do not overwrite your existing Day 5–8 work.

## Step 2 — Run a baseline

In local PowerShell, with your existing virtual environment active:

```powershell
git status -sb
python --version
docker version
python -m pip install -r requirements.txt -r exercises/day05-requirements.txt
python exercises/day06_gate.py check
python -m pytest -q
```

The Day 9 starter contains an unfinished runtime adapter, so failing Day 9 tests are expected initially.

Record the first useful error.

## Step 3 — Complete the protected application adapter

Open:

`exercises/day09_entry.py`

Find `TODO A`.

The code needs the identity file path from the `TASKFLOW_IDENTITY_FILE` environment variable.

Inspect how the existing `database` path is handled.

Complete the missing code so that the application loads its identity through the protected factory.

Do not hardcode a signing key or password.

## Step 4 — Complete the Dockerfile

Open:

`Dockerfile.day09`

Find:

`TODO_FACTORY`

Inspect the function exported by `exercises/day09_entry.py`.

Replace the placeholder with the correct factory function.

The Docker image must run the protected application, not the older `app.main:app`.

## Step 5 — Run the full test suite

```powershell
python -m pytest -q
```

Fix implementation issues, not the security expectations in the tests.

## Step 6 — Build and test the actual Docker image

From the repository root:

```powershell
$Revision = git rev-parse HEAD

docker build --platform linux/amd64 --build-arg "SOURCE_REVISION=$Revision" -f Dockerfile.day09 -t taskflow:day09-local .
```

After a successful build:

```powershell
python -m exercises.day09_image_check taskflow:day09-local
```

Record whether the real container passed its authentication and persistence checks.

## Step 7 — Configure GitHub Actions variables

In GitHub, open:

**Repository → Settings → Secrets and variables → Actions**

Add the repository variable:

`PYTHON_VERSION = 3.12`

Then navigate to:

**Settings → Environments → your assigned team environment**

Use the trainer-approved values for:

| Variable | Purpose |
|---|---|
| `AWS_REGION` | Deployment Region |
| `AWS_ACCOUNT_ID` | Correct training account |
| `AWS_ROLE_ARN` | Scoped GitHub deployment role |
| `ECR_REPOSITORY` | Team container repository |
| `APP_ENVIRONMENT` | `training` |
| `INSTANCE_ID` | Wednesday's original EC2 instance |
| `APP_PORT` | `8055` |
| `SSM_DOCUMENT` | Approved deployment document |

Do not invent these values.

Add the optional fictional environment secret:

`DEMO_RELEASE_NOTE`

The workflow checks its presence without printing its contents.

## Step 8 — Complete the GitHub workflow

Open:

`docs/day09-workflow-starter.yml`

Find:

- `TODO C`
- `TODO D`
- `TODO E`

Complete the missing configuration mappings and the test command.

Review the five jobs:

1. `dependency`
2. `test`
3. `package`
4. `publish`
5. `deploy`

Explain which jobs should be skipped when an earlier check fails.

## Step 9 — Activate the workflow

From the repository root:

```powershell
New-Item -ItemType Directory -Force .github/workflows | Out-Null

Copy-Item docs/day09-workflow-starter.yml .github/workflows/taskflow-day09.yml
```

Review your changes before committing them.

If your repository already contains an active deployment workflow, have it reviewed before introducing a second one.

## Step 10 — Demonstrate a failing release gate

On a short-lived branch, create:

`tests/test_day09_gate_demo.py`

Write a harmless pytest test with a deliberately false assertion.

Commit and push the branch.

Open a pull request.

In GitHub:

**Actions → TaskFlow Day 9 → select the pull-request run**

Record:

- Which test failed.
- Which jobs were skipped.
- Whether packaging or publishing proceeded.

## Step 11 — Repair the failing gate

Remove the deliberately failing test in a new commit.

Push the change.

Verify the test and package jobs pass.

Review and merge the approved changes to `main`.

## Step 12 — Publish the checked image

In GitHub:

**Actions → TaskFlow Day 9 → Run workflow**

Select:

- Branch: `main`
- Environment: your approved team environment
- Deploy: **false**

Run the workflow.

It must pass the dependency, test, package and publish jobs.

Find the resulting image in:

**AWS Console → Amazon ECR → Private registry → Repositories → your team repository → Images**

Record the image digest.

## Success criteria

Your team demonstrates:

- The protected Docker entry point.
- Passing Python and actual-container checks.
- A deliberately failing security gate.
- The skipped downstream jobs.
- A repaired passing workflow.
- A checked image published to ECR.
- A recorded digest identifying the actual image.

Explain the difference between a build variable, a deployment variable and a runtime secret.

If an AWS publishing step is blocked, record the exact error and use the instructor's separately verified reference route.