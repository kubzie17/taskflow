# Challenge 1 — Secure the TaskFlow build and deployment configuration

**115 minutes · 09:40–10:45 and 11:00–11:50 · review 11:50–12:00**

## Scenario and desired outcome

Northbridge's infrastructure exists, but the old Dockerfile starts an earlier application. The service must enforce its reader and dispatcher permissions before anyone releases it. Build a pipeline that checks the current dependencies, tests the application, packages the protected entry point and publishes only a passing image to your team's private ECR repository.

Your team will deliberately fail a harmless test, capture the blocked jobs, repair it and produce a passing release. A tag on the security group cannot substitute for this evidence.

## Starting files and prerequisites

Start at the existing repository root with Python 3.12, Git and Docker Linux containers available. The trainer has prepared your GitHub environment and AWS publishing role. Use the protected factory in `exercises/day05_api.py`, its identity helper, `requirements.txt` and `exercises/day05-requirements.txt`. Keep the earlier application available for its existing tests.

Open these new files in VS Code.

| File | Your work |
|---|---|
| `exercises/day09_entry.py` | Complete TODO A so the runtime identity file comes from configuration. |
| `Dockerfile.day09` | Replace TODO_FACTORY with the wrapper factory you have inspected. Explain how it calls the protected API. |
| `docs/day09-workflow-starter.yml` | Bind TODO C and D to the correct GitHub configuration values, then complete TODO E to execute the full test suite. |
| `Dockerfile.day09.dockerignore` | Inspect the allow-list and explain which imports are needed. |
| `tests/test_day09_runtime.py` | Read the contracts for missing configuration, authentication and persistent data. |

The provided probe, image checker and SSM submitter support verification. Your task is to connect and explain the release configuration and prove the gate.

## 1. Establish the local baseline

In **local PowerShell**, from the repo root and the activated virtual environment, run one line at a time. Check the exit code after failures.

```powershell
git status -sb
python --version
docker version
python -m pip install -r requirements.txt -r exercises/day05-requirements.txt
python exercises/day06_gate.py check
python -m pytest -q
```

The Day 9 starter produces failing runtime tests until TODO A is completed. Read the first relevant failure. Older tests should still run. Do not edit a test simply to change its expected security behaviour.

## 2. Connect startup and packaging

Inspect the original factory's parameters. Implement TODO A using the named environment variable. The adapter already validates required paths and passes a `LocalIdentity` provider to `create_secure`.

Inspect the function name exported by the adapter and complete `Dockerfile.day09`. Uvicorn must run it in factory mode. Follow the imports through `day05_api`, `day05_identity`, `day04_candidate`, `app.main` and `app.database`. Explain why copying only `app/` would be insufficient.

Run the tests again, then build and exercise the actual image.

```powershell
python -m pytest -q
if ($LASTEXITCODE -ne 0) { throw 'Tests failed. Stop here.' }
$Revision = git rev-parse HEAD
docker build --platform linux/amd64 --build-arg "SOURCE_REVISION=$Revision" -f Dockerfile.day09 -t taskflow:day09-local .
if ($LASTEXITCODE -ne 0) { throw 'Build failed.' }
python -m exercises.day09_image_check taskflow:day09-local
if ($LASTEXITCODE -ne 0) { throw 'Built-image checks failed.' }
```

The local revision label is provisional while you have uncommitted changes. The CI image uses the actual checked-out release commit. The image checker uses temporary synthetic identities and an isolated database, then removes its container. It should report working access controls and persistence after a restart.

## 3. Configure GitHub values

In GitHub open the team's repository, then **Settings → Secrets and variables → Actions → Variables**. Add `PYTHON_VERSION` with `3.12`. This optional build setting has a documented default.

Open **Settings → Environments → your assigned team environment**. Enter the non-sensitive environment variables from the private trainer handover. Use the configuration worksheet to record their purpose. The trainer configures the branch restriction and any available required-reviewer protection.

| Required environment variable | Value source |
|---|---|
| `AWS_REGION` | Wednesday's approved Region |
| `AWS_ACCOUNT_ID` | Approved training account |
| `AWS_ROLE_ARN` | Trainer's scoped GitHub role |
| `ECR_REPOSITORY` | Team's `taskflow-…` private repository name |
| `APP_ENVIRONMENT` | `training` |
| `INSTANCE_ID` | Original Wednesday instance, when available |
| `APP_PORT` | `8055` |
| `SSM_DOCUMENT` | Trainer's `TaskFlow-Day09-…` document name |

In the same GitHub environment, add an **environment secret** named `DEMO_RELEASE_NOTE` containing a new fictional disposable phrase. Its demonstration step reports presence only. The actual runtime identity is stored in AWS. AWS authentication uses OIDC.

## 4. Implement and review the workflow

Complete TODO C, D and E in the starter. Compare the `dependency`, `test`, `package`, `publish` and `deploy` jobs with `docs/day06-workflow-review.yml`. Identify the earlier ignored dependency failure and incomplete dependency wiring. Explain what the `needs` relationships in this workflow enforce.

Create `.github/workflows/` if needed, then copy your completed file to `.github/workflows/taskflow-day09.yml`. If your team's repo already has an active workflow, review it with your partner. Keep its useful checks and make sure it cannot deploy an unprotected image in parallel. The current trainer source has its earlier examples under `docs/`.

```powershell
New-Item -ItemType Directory -Force .github/workflows | Out-Null
Copy-Item docs/day09-workflow-starter.yml .github/workflows/taskflow-day09.yml
git diff
```

There are no AWS credentials in the dependency, test or package jobs. Publishing and deployment run only through `workflow_dispatch` on `main`, using the selected protected GitHub environment. Inspect workflow-level `env`, job-level `env` and the step-level mapping from `vars` to shell environment variables. The named GitHub environment values are mapped when those steps execute.

## 5. Prove the gate blocks a failed test

Use a short-lived team branch. Add `tests/test_day09_gate_demo.py` containing a test with a deliberately false assertion and an explanatory name. This test exercises the gate without weakening the application. Commit only the intended learner files, push that branch, and open a pull request to your team release branch.

In **Actions → TaskFlow Day 9 → the PR run**, capture the failing test and skipped package/publish/deploy jobs. The PR route has no cloud credentials. Inspect the first failure to prove the intended test caused it.

Remove the deliberately failing test in a new commit on the same branch. Rerun the checks. Record the green commit and review the diff with another learner before merging. If the dependency audit finds a real problem, investigate and repair the dependency with the trainer while deployment remains blocked.

## 6. Publish the passing image

Once the changes are on `main`, open **Actions → TaskFlow Day 9 → Run workflow**. Select `main`, your assigned environment and leave `deploy` unchecked. Approve the environment run if your repository requires it.

All checks run again. The package job tests the actual image, audits the packages installed inside it, and saves that image. The publish job uses that same image artifact, obtains short-lived AWS credentials, pushes it with a unique commit/run tag and records its digest. Inspect **Amazon ECR → Private repositories → team repository → Images** and compare the digest with the Actions summary.

## Acceptance and evidence

Save the red run link, repaired green commit, successful run link, ECR image digest, and a short explanation of one build variable, one deployment variable and the runtime secret. Demonstrate a skipped package job after your deliberately failed test. Explain why a failing security check stops the release even if all other jobs pass.

If packaging is unfinished at lunch, record the exact failure. The trainer can supply a separately gated reference build and image identity for the afternoon. Mark whose build you used.

## Progressive hints and stretch

Ask for one hint at a time from the separate hints file after showing your diagnosis. A team that finishes early can review another team's `needs` relationships, prove the missing-variable error is clear, or inspect image metadata for secret values. Avoid displaying actual secret contents. Keep the afternoon deployment for Challenge 2.
