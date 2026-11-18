# Day 6 workshop · Is this TaskFlow change safe to build?

**Monday 16 November 2026 · Teams · 09:30–15:30 UK.** Use your existing TaskFlow checkout, VS Code, two terminals and fictional bookings. Open `exercises/day06-evidence.md` and save a personal copy. Each workshop has one client question. Predict the result privately before your partner takes the keyboard. If you cannot share your screen, send your redacted prediction/result pair in chat.

## Before you start at 09:30

1. From the folder containing `app/`, `requirements.txt` and `exercises/`, run `git status -sb`, `git branch --show-current` and `git rev-parse --short HEAD`. Preserve Friday’s edits on their current branch. See the Day 6 section of the root README for the materials commit, pull or cherry-pick route. Create your Monday branch from your saved Friday work, e.g. `git switch -c day06-yourname`.
2. Activate your existing Python 3.12 environment. Windows PowerShell: `.\.venv\Scripts\Activate.ps1` (use `venv` if yours has that name). macOS/Linux: `source .venv/bin/activate`. If activation is restricted use the environment's Python executable directly. In the commands below `python` means that interpreter.
3. Inspect Friday’s dependency file before installing. The published Day 5 learner file pins `PyJWT==2.15.1`. A differing pin or inaccessible approved package index is a preflight finding. Use your existing working partner’s setup while the trainer checks the mismatch. Keep the proposal exhibit as plain text.
4. Run the following from the repo root. Note the interpreter, declared pin, installed version and starting tests. Install only the reviewed course files when setup is needed. The optional YAML checker uses PyYAML 6.0.3 in a tooling environment. It is separate from the application dependencies. All core investigations have an offline route.

```text
python --version
python exercises/day06_gate.py check
python -c "from importlib.metadata import version; print(version('PyJWT'))"
python -m pytest -q
git ls-files .github/workflows
```

On a prepared Python 3.12 machine, the approved installation is `python -m pip install -r requirements.txt -r exercises/day05-requirements.txt`. A hired runner, AWS account, Docker installation or paid scan is unnecessary for the core evidence. Record a failed install as an environment blocker and use the paired route. Keep the returned bearer token and local passphrases off screen share.

## 1 · Can you prove the booking permissions? · 09:40–10:25

**Client and files.** Northbridge wants the reader/dispatcher boundary demonstrated on Friday’s protected factory. Open `exercises/day05_api.py`, `exercises/day05_test_starter.py` and your existing `tests/test_day05_access.py`. If that test file is missing, copy the starter to that filename. It supplies `lab` → `(client, db_path, passwords)` and `rows(db_path)`. Keep any authored cases. Preserve the booking model, title validation, public support fields and historical tests.

1. Inspect `current_user`, `permit` and the dependencies on the two booking routes. Identify what is unfinished on your branch. Start the protected server using the command below if you are testing interactively. Open `http://127.0.0.1:8055/docs`. Sign in through `POST /session` for each fictional role. In Swagger **Authorize**, paste only the access-token value privately. **Logout** between roles. The terminal-only Friday helper `python -m exercises.day05_probe` also supports `login`.
2. Run and record all six rows of the clinic table in `day06-evidence.md`. Use a valid title for the access tests. Test one title of 101 characters as a dispatcher. Seed a booking, then compare all stored IDs/titles before and after every refusal. A 201 should create exactly one matching row.
3. Complete Friday’s existing unfinished role check if needed. Write executable pytest cases for the role decisions or extend yours. Use a real authenticated request and direct SQLite evidence. Run the dedicated test file and full suite. Save a revision or clearly mark an uncommitted result.

```text
python -m uvicorn exercises.day05_api:create_secure --factory --host 127.0.0.1 --port 8055
python -m pytest -q tests/test_day05_access.py
python -m pytest -q
```

Use a second terminal for the test commands. Browser runs write to `data/day05-lab.db`. Tests use their own temporary database. Read the browser database with `python -c "import sqlite3; c=sqlite3.connect('file:data/day05-lab.db?mode=ro',uri=True); print(c.execute('select id,title from tasks order by id').fetchall()); c.close()"`. If there is no identity file, run `python -m exercises.day05_identity` once with new fictional passphrases. Check the port before trusting a result. The old 8044 and `app.main:app` entries have a different purpose.

**Acceptance.** Visitor POST 401, reader GET 200, reader POST 403, dispatcher POST 201, invalid bearer POST 401, dispatcher invalid title 422. Signed reader must see the seeded row. All refused writes preserve it. **Stretch.** Make a reader send a forged role header, or isolate expiry with a genuinely signed expired fixture. **10:25 hard stop.** Save your next failing check and owner. Pair with a working operator for the remaining workshops. The trainer can run the known Friday baseline in a separate folder. Your evidence must identify where it was obtained.

## 2 · Should dispatch accept the vendor’s pin? · 11:00–12:00

**Client and files.** In the short 10:25 briefing open `exercises/day06-case.md` (Exhibit A), `exercises/day06-proposal.case`, root `requirements.txt` and `exercises/day05-requirements.txt`. Inspect the local and optional cloud verifier code named in the exhibit. The proposal is a fictional ticket about a real advisory. Keep the proposed file out of package installers.

1. Compare one direct pin against your installed interpreter. Trace one transitive dependency from actual distribution metadata. If offline and dependencies are missing, use the dated manifest in Exhibit A and label it as supplied evidence.
2. Record the advisory identifier, affected range, first patched version and necessary precondition. Distinguish the normal local sign-in path from the optional remote-key verification path. Find the relevant lines in your branch and decide whether a passing login test settles exposure.
3. Run both checks below and read their exit codes (`$LASTEXITCODE` in PowerShell, `echo $?` in Bash). Decide whether to accept, amend or decline the proposal. If your own branch has an affected pin, use the trainer-approved version from the published course file and its approved package source before retesting. If already on the approved pin, retain it and commit your decision record. Never deliberately downgrade.
4. Create `docs/day06-decision.md` with your evidence, choice, compatibility test, one remaining uncertainty and owner. Run your Friday targeted test and the full suite with the same interpreter. Keep historical assertions and the approved packaging behaviour intact.

```text
python -c "from importlib.metadata import version,requires; print(version('fastapi'),version('starlette')); print([d for d in requires('fastapi') if d.lower().startswith('starlette')])"
python exercises/day06_gate.py check --pin-file exercises/day06-proposal.case
python exercises/day06_gate.py check
python -m pytest -q
```

**Acceptance.** One verified dependency edge, a documented decision on the version and code path, a blocked proposal, an eligible approved file and a real test result or labelled partner observation. **Stretch.** Audit a trusted installed environment with pip-audit using the optional instructions below. Explain why a one-package gate cannot discover a new advisory in a transitive dependency.

## 3 · Where did the deleted diagnostic go? · 13:00–13:25

**Client and files.** Exhibit B describes an inert diagnostic marker once committed as `app/dispatch.local.env`. Open `.gitignore`, `.env.example` and the root `.dockerignore` from Day 3. Keep the existing app files included in the Docker context and the safe example trackable. The real `.env.example` contains a harmless database path.

1. Run `python exercises/day06_incident.py` from your course repo. In a **second terminal**, change directory to the printed temporary path. Inspect `git status -sb`, `git log --oneline --all -- app/dispatch.local.env` and `git show HEAD~1:app/dispatch.local.env`. Compare the current tree with the earlier commit. The generator never reads a secret.
2. Predict what happens to a new file of that name. Back in the **course repo**, run the probes below before editing. `git check-ignore` can test the name without creating the file. An initial match is possible on a hardened branch. Label that observation. Check `git ls-files -- .env.example` still lists the template.
3. Edit your existing Git and Docker ignore rules to protect this pattern anywhere it might be saved under the app. Keep the example and necessary source usable. Repeat the probes. If your Dockerfile/context rules are missing, ask for the previous Day 3 recipe in a sibling copy. When Docker is unavailable, inspect the ordered patterns, make a prediction and mark the actual build untested.
4. Add four lines to your incident record covering containment, simulated issuer-side revocation/rotation, the places to investigate, and how to prove replacement and revoke the old credential. Distinguish confirmed Git history from possible logs, clones and images. Only fictional values appear in this exercise.

```text
git check-ignore -v --no-index app/dispatch.local.env
git check-ignore -v --no-index .env.example
git ls-files -- .env.example
python exercises/day06_context_probe.py
```

Use `git check-ignore -q --no-index .env.example` and inspect its exit code to settle ambiguous verbose output (1 = not ignored). For the marker, 0 = ignored. The optional BuildKit probe copies only the ignore rules and synthetic files into a disposable context. **Acceptance.** Record the two history revisions, old versus current contents, a working Git safeguard, retained sample and Docker observation or labelled limitation. **Stretch.** Explain how you would handle a file already tracked and why an environment variable can still leak in a CI log.

## 4 · Can a failed check reach packaging? · 13:25–14:15 and 14:30–14:50

**Client and files.** Open your live `.github/workflows/taskflow-ci.yml`, if present, and Exhibit C at `docs/day06-workflow-review.yml`. The latter is an untrusted practice exhibit, safely outside the active workflows directory. The Day 2 starter was `docs/ci-workflow-starter.yml`. The Day 3 recipe built the candidate only after tests. Monday's task is to extend the working pipeline on your own branch.

1. Sketch what happens in the exhibit if the proposed dependency fails or pytest fails. Inspect event, permission scopes, checkout credentials, the checker’s input and exit handling, tests, and the `needs` relationships. Compare with your revision. Never activate the weak exhibit as supplied.
2. Edit your workflow. If it is absent, work on a copy in `docs/day06-working.yml` first. Use the earlier test/build jobs as a starting point. Exhibit C contains the verified release commit digests for offline rooms. Add a blocking dependency job against the **actual Friday requirements file** before dependency installation, explicitly exercise your booking permission test file and the full suite, then gate the existing package build on both checks. Keep a PR trigger, least privilege and a reviewed checkout. Verify full action SHAs against the publisher. Do not use a secret, push an image, publish an artefact containing credentials or grant deployment rights.
3. Run the checker below on your own candidate. Replace the path and, if different, pass `--jobs YOUR_DEP_JOB YOUR_TEST_JOB YOUR_PACKAGE_JOB`. This bounded tool parses YAML and checks the class workflow shape. It cannot certify arbitrary shell code or GitHub behaviour. Alternatively run `actionlint PATH` if available. If neither tool is installed, review the actual YAML line-by-line with a partner, then run the two execution checks.
4. Run a rejected proposal and then the approved path. For the test-failure case use a **disposable copy** with the approved pin and one intentionally failing assertion in a new `tests/test_day06_rehearsal_failure.py`. Check the failure is real and packaging is skipped. Remove only your own temporary test in that disposable folder and rerun. Review the diff before committing. The local helper reproduces the gate and test commands. It does not execute or emulate the workflow YAML.
5. On a clean exercise branch, only after reviewing the candidate, put the hardened workflow in `.github/workflows/taskflow-ci.yml`. If authorised, open or update a normal pull request and inspect **Actions → TaskFlow CI → jobs** at its actual revision. For a negative hosted run, use a disposable PR with a deliberately failing test and its repair. Keep the rejected dependency as text in the offline scenario. If you lack push or Actions rights, capture the static findings and local gate results instead.

```text
python exercises/day06_workflow_check.py docs/day06-workflow-review.yml
python exercises/day06_workflow_check.py .github/workflows/taskflow-ci.yml
python exercises/day06_gate.py rehearse --pin-file exercises/day06-proposal.case
python exercises/day06_gate.py rehearse
```

The default clinic test is `tests/test_day05_access.py`. Supply `--auth-tests PATH` to match your own regression file. A missing file or empty test collection blocks the local package. Local `PACKAGE ELIGIBLE` means the two prerequisite checks passed. To actually build the historical image on a trusted local branch with Docker, an existing Day 3 Dockerfile and sufficient time, add `--build`. Check the image entry point separately before making any claim about the Friday API being packaged.

**Acceptance.** Show the changed workflow path and revision, least-privilege reasoning, the three outcome rows and the source of each observation. A failure must prevent packaging. Use the normal Day 3 build on the green route. **Stretch.** Identify how a malicious PR could alter the policy checker itself and what an independent reviewer or separately controlled required check could add.

## 5 · Independent release review · 14:50–15:05

1. Open a sanitised diff at the author's revision. Swap authors and reviewers across breakout rooms. A third learner in a trio chooses the input and challenges the evidence.
2. Reviewer picks one test without coaching: repeat a rejection and its SQL query, reproduce the blocked dependency, verify the historical file, or challenge the workflow with a failed prerequisite. Ask the author which exact file, process or revision was exercised.
3. Record one observed result, one remaining limitation and one action with an owner. Ask for **ready for the tested scope** or **hold**, and a reason. The review is evidence about this revision. **Stretch.** Re-run a case that would still look green if the wrong API or workflow were tested.

## AWS readiness · 15:05–15:20

Open your existing `exercises/day05-aws.md` checklist. Its Friday heading refers to the earlier plan. Use the action table at 15:05 on Monday. First note sandbox/account type, region, remaining session time, persistence guidance and visible budget or “unknown”. Assign **2 learners** to IAM/Cognito reads, **3** to EC2/S3/VPC/security-group visibility plus CLI/Terraform readiness, and **2** to CloudWatch log groups, metrics and alarms. A learner in each room reports one exact action and result. A temporary STS identity check does not establish permission to create or delete resources. An installed Terraform CLI does not establish AWS-provider access.

Use only approved read-only actions. Record **Available / Denied / Not tested**, evidence source, region, usable scope and fallback. A blocked session or expired credentials leave downstream permissions untested. Leave write/delete untested unless prior approved evidence establishes that exact action. Avoid creating resources, alarm tests, Logs Insights queries and access keys. If core work is still running, a ready pair and the trainer sample one check per lane and send the sanitised results in chat. If AWS cannot be accessed, record the blocker and next owner. Save a kind of proof for Tuesday that you could show a colleague.

## Optional tools and finishing up

- **YAML checker.** Use an existing approved tools environment with PyYAML 6.0.3, or prepare one outside the repository (`python -m venv PATH_TO_TOOLS` then its Python `-m pip install PyYAML==6.0.3`). Use that interpreter only for `day06_workflow_check.py`. Use the **TaskFlow** interpreter for the application tests. If YAML tooling is blocked, use the supported manual/local route in W4.
- **Live audit.** In a separate tooling environment install approved `pip-audit==2.10.1` using its Python. In the TaskFlow environment run `python -c "import sysconfig; print(sysconfig.get_paths()['purelib'])"`. In the tool environment run `python -m pip_audit --path "PRINTED_TASKFLOW_SITE_PACKAGES" --format json`. Replace the placeholder with that path. This can contact the advisory service. Read the result and error text as well as its exit code. A network failure is an inconclusive scan. Use Exhibit A offline. Keep other findings for triage and never run automatic fixes on the class repo.
- Before 15:30 inspect `git diff` and `git status -sb`. Commit only intended changes on your work branch, record the revision and whether you tested the historical image, the protected localhost API or the proposed workflow. The service credentials stay outside Git.
