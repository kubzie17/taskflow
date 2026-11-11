# Day 2 exercises | Can we trust this pull request?

Northbridge Repairs wants to catch a broken booking rule before a change reaches dispatch. You will test the rule in your own TaskFlow repository, run the test on a pull request (PR), investigate a failed check and show a reviewer what you fixed.

Run terminal commands from the project root, where `app/`, `tests/` and `requirements.txt` live. If the Day 2 materials are still only on the trainer’s GitHub page, follow [section 8 of the project README](../README.md#8-day-2). Keep your results in [the Day 2 evidence sheet](day02-evidence.md).

[A. Starting point](#a-starting-point) · [B. Boundary test](#b-boundary-test) · [C. Workflow](#c-workflow) · [D. Failure and repair](#d-failure-and-repair) · [E. Peer review](#e-peer-review) · [Offline replay](#offline-replay)

## A. Starting point

1. Open the same working copy you used on Day 1. Check the branch, remote, interpreter and test baseline.

   ```text
   git status -sb
   git branch --show-current
   git log -1 --oneline
   git log -1 --oneline -- app/main.py tests/test_api.py
   git remote -v
   python -c "import sys; print(sys.executable)"
   python -m pytest --collect-only -q
   python -m pytest -q
   ```

2. Find the test that protects `status == "ok"` and, if you finished TF-01, the test for `service == "taskflow"`. The unmodified starter has two tests. The Day 1 reference with its added health test has three. Record your actual count and commit. If a test or change is missing, use [Day 1 exercise E](day01.md) to complete that piece or record it as pending.
3. Record the branch containing your Day 1 work as your review base. This can be your default branch or the unmerged `feature/health-service` branch. If you already created `ci/day02-checks` while bringing in the materials, continue there. Otherwise, from the verified base, run `git switch -c ci/day02-checks`. For an existing Day 2 branch, use `git switch ci/day02-checks` when your working tree is clean. Check that the Day 2 files are present on the branch you are using.

**Choose one incident.** Write down the symptom, two explanations and a read-only check that separates them. Each partner explains what evidence would confirm recovery.

| Ticket | What you can investigate |
| --- | --- |
| A. Interpreter | The API serves requests but another terminal reports `No module named pytest`. Compare `sys.executable` and `python -m pip show pytest` in the affected terminal. |
| B. HTTP method | `GET /tasks` works and `PUT /tasks` returns 405. Inspect `/docs` or `/openapi.json`. Make a request using the documented creation method, then retrieve the same id. |
| C. Port | Uvicorn reports port 8001 but a bookmark points to 8000. Read the listener address, request its health route and inspect the body. What if another process answers on 8000? |

For a ticket that needs the live API, run `python -m uvicorn app.main:app --host 127.0.0.1 --port 8000`. Use 8001 in both the command and URL for ticket C. The automated tests use an in-process client and can run with the server stopped.

**Check your recall.** Answer individually before comparing with a partner.

- R1. Which status confirms that `POST /tasks` created a booking: 200, 201 or 204?
- R2. Predict the status for a well-formed request whose title contains only spaces.
- R3. Do three passing starter and TF-01 tests establish that only dispatchers can create bookings? What evidence would verify that rule?
- R4. Put these actions in the order used to publish an edit: push, edit, stage, commit.

## B. Boundary test

The booking title accepts 1–100 characters after trimming spaces. A valid creation returns 201. Invalid input returns 422 and should leave the list of bookings unchanged. Just as a rejected stock order could still reduce the stock count, a response code alone cannot tell you whether data changed.

1. Predict the HTTP status and change to the task list for 100 letters, 101 letters and a whitespace-only title. Find the validation rule in `app/main.py`.
2. In `tests/test_api.py`, extend the existing `TestTaskFlow` class with a method named `test_rejects_overlong_title_without_writing`. Keep the existing tests. If you already cover this case, check both assertions below and use the existing test’s collected name.
3. Arrange by reading `GET /tasks`. Send `POST /tasks` with `{"title": "X" * 101}` as a Python dictionary. Check the returned status, read the list again and compare it to the original. The class gives every test its own client and temporary SQLite database.
4. Save, check collection, run your test and then run the whole suite. Substitute the collected node ID if yours differs.

   ```text
   python -m pytest --collect-only -q
   python -m pytest -q tests/test_api.py::TestTaskFlow::test_rejects_overlong_title_without_writing
   python -m pytest -q
   ```

5. Show a peer which assertion would catch an unwanted row. Record the test name and result. If you added or edited the test, use `git add tests/test_api.py`, review `git diff --staged`, then commit with `git commit -m "Check the booking title limit"`.

**Check:** your new test is collected and the original tests still pass. A new test can pass immediately because the application already implements the contract. **Stretch:** test an exactly 100-character valid title and retrieve its id. What defect could the 101-character test miss?

## C. Workflow

Continuous integration (CI) gives the team feedback on a proposed change in a shared environment. A workflow maps an event to a job. Its runner checks out the source, selects Python and executes the listed steps. Each step in the job uses the same workspace. A successful run records evidence about that revision.

**Pair exercise.** Put these actions in order: review the result, commit locally, run tests, push the branch, check out the proposed revision on a runner, open a PR. Explain which actions repeat when the developer pushes to an already-open PR.

1. Open the [workflow scaffold](../docs/ci-workflow-starter.yml). In your editor create `.github/workflows/taskflow-ci.yml` at the repo root and copy the scaffold into it. If that workflow already exists, compare it and add what is missing.
2. Fill in the pull-request event `pull_request` without a branch filter, `contents: read`, the runner `ubuntu-latest`, `actions/checkout@v6` with `persist-credentials: false`, and `actions/setup-python@v6` with Python `'3.12'`. Keep the job ID `test` and job name `API tests`. Use approved full action references if your course repository requires them.
3. Under `steps` add `Install dependencies` running `python -m pip install -r requirements.txt` and `Run tests` running `python -m pytest -q`. Use a dash per step and spaces for nesting. `uses` invokes a reusable action. `with` supplies its inputs. `run` executes a command.
4. Swap driver and reviewer. Point to the event, job, runner and test command. Predict what happens to the test step if installation fails. Confirm that all placeholders have been filled, the job can report failures and each learner has their own committed file.

   ```text
   git add .github/workflows/taskflow-ci.yml
   git diff --staged
   git commit -m "Run TaskFlow tests on pull requests"
   ```

**Check:** your peer can trace how an update to an open PR reaches the test command. **Stretch:** explain why adding a push trigger as well could produce two runs for one change.

## D. Failure and repair

**Release huddle.** Dispatch wants an urgent fix and someone calls the latest red check “probably flaky”. Agree what evidence the reviewer needs, who owns the decision and what would change your recommendation.

1. On your Day 2 branch, check `git remote -v`, then run `git push -u origin ci/day02-checks` to your **own** course repository. Open a PR from `ci/day02-checks` into the review base recorded in A. If your Day 1 feature branch is the base, publish that branch to your own remote first. Open **Checks → TaskFlow CI → API tests → Run tests**, or find the same job in the Actions tab. Compare the run count with the tests you collected locally. If hosted execution is unavailable, use [offline replay](#offline-replay).
2. On the lab branch, change **only** the expected status of the 101-character test from 422 to 400. Run `python -m pytest -q`. Confirm the test failed for the expected reason. Commit the deliberate mismatch and push it to the open PR.

   ```text
   git add tests/test_api.py
   git diff --staged
   git commit -m "Lab drill: introduce a wrong status expectation"
   git log -1 --oneline
   git push
   ```

3. Capture the red result before repairing it. Record the source commit, first failed step, earliest useful error, actual value and expected value. An installation error requires a different investigation from an assertion failure.
4. Restore the test’s expected status to 422. Run the whole suite, stage `tests/test_api.py` and inspect the staged diff. Commit with `git commit -m "Restore the booking validation expectation"` and push. Capture the **new** commit and run. Re-running the old job retests its old revision.

**Check:** show two different revisions, the change responsible for the failure, and evidence that the repair passed. For local work, omit the pushes and replay each recorded revision. Keep the deliberate fault on the lab branch.

## E. Peer review

1. Swap roles. Review the PR’s **Files changed** and **Checks**, or run `git diff BASE...HEAD -- tests/test_api.py .github/workflows/taskflow-ci.yml` locally after replacing `BASE` with your actual review base.
2. Name the rejection assertion, the unchanged-list assertion and one retained original test. Identify the earliest useful line in the failed run. Give the owner one concrete piece of feedback.
3. Compare the [log exhibits](#log-exhibits). Explain how the evidence differs when the install step fails. Give a release recommendation, its owner, a condition and one risk the passing checks leave open.
4. Answer the [exit questions](#exit-questions), then finish the [evidence sheet](day02-evidence.md). Save the reviewed branch and latest verified revision for Day 3.

## Offline replay

The supplied [replay tool](replay_commit.py) installs and runs the committed code in a fresh local environment. Use it from the repository root on the red and then green commit. Replace `HEAD` with a recorded commit if you have already moved on.

```powershell
py -3.12 exercises/replay_commit.py HEAD
```

On macOS/Linux, use `python3.12 exercises/replay_commit.py HEAD`. If package downloads are blocked and the trainer has supplied a matching wheel directory, append `--wheelhouse ../day2-wheels`. Record the printed revision and result as **clean local replay**. Hosted scheduling and the proposed merge still require a GitHub run. If neither route is available, analyse the supplied exhibits and mark personal execution pending.

## Log exhibits

These are extracts from actual local runs on a trainer reference copy. Use your own run links or commits for personal evidence. For each example, identify the last step reached, the most useful line and your next check.

```text
Exhibit A | Recorded on a clean local replay of a committed reference revision
Source revision: 9669f5e05205a1ae36e232fc85bb6c4ae19a09ba
Install dependencies: completed
Run tests: python -m pytest -q
E       AssertionError: 422 != 400
FAILED tests/test_api.py::TestTaskFlow::test_rejects_overlong_title_without_writing
1 failed, 3 passed
Test process exit: 1
```

```text
Exhibit B | Recorded on a clean local replay of the repaired reference revision
Source revision: e545d35b9fe03da9d5e21dd2dc7f510d0ea0e6cd
Install dependencies: completed
Run tests: python -m pytest -q
4 passed
Test process exit: 0
```

```text
Exhibit C | Local installation fault injected in the same project root
Source revision: e545d35b9fe03da9d5e21dd2dc7f510d0ea0e6cd
Install dependencies: python -m pip install --no-index -r requirements-ci.txt
ERROR: Could not open requirements file: [Errno 2] No such file or directory: 'requirements-ci.txt'
Install process exit: 1
Test step: not reached in this exercise
```

## Exit questions

1. You commit a test on your laptop. Has the PR workflow run? Which shared-repository event would trigger it?
2. Why compare the task list before and after a rejected request when the response already says 422?
3. A job fails at **Install dependencies**. What evidence would you need before claiming that an API assertion failed?
4. A run is green but your test is absent from `--collect-only`. Which files, revision or commands would you check?
5. The previous revision was green and the newest PR update is red. Which result bears on the candidate? What does re-running the old build test?
6. Which part of a release does this workflow automate? What else would need to happen for the candidate to reach production?
