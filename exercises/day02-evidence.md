# Day 2 evidence | Testing a pull request

Save a personal copy under your own name outside the repository or use a new unused evidence filename inside it. Keep URLs redacted where required. Record actual values. In each line identify your role as **ran**, **observed** or **pending**. Add **hosted PR**, **clean local replay**, **working copy** or **supplied case** for the execution route.

| Checkpoint | Your evidence |
| --- | --- |
| Repository, Day 1 review base and short SHA, Day 2 branch and materials revision | Repo kubzie17/taskflow (origin). Day 1 base: feature/health-service-tyreece. Day 2 branch: ci/day02-checks-tyreece. Materials from origin/main. (working copy, git history) |
| Day 1 TF-01 status, original test retained, new field assertion, collected/passing counts | TF-01 done: commit 0055136 'Identify the service in the health response'. Original health test kept, test_health_identifies_service asserts service == taskflow. Now 8 collected in tests/test_api.py, 81 passing in the full suite. (ran, working copy) |
| Debug ticket, symptom, two hypotheses, discriminating check, recovery and verification | pending: not recorded. Fill in from your chosen ticket (A interpreter, B HTTP method or C port). |
| Day 2 test node ID, rejected input, both assertions, baseline → actual passing count | tests/test_api.py::TestTaskFlow::test_rejects_overlong_title_without_writing. Input 101 x 'X', expects 422, and the task list before and after is equal. (ran, working copy) |
| Workflow path, triggering event, job ID, runner, commands, token access | .github/workflows/taskflow-ci.yml (commit d778e35 on ci/day02-checks-tyreece). Event pull_request, job ID test, runner ubuntu-latest, commands pip install -r requirements.txt and python -m pytest, permissions contents: read. (git history) |
| Red source revision, run URL or replay evidence, step, first useful line, actual and expected | 8cfa6b6 'Lab drill: introduce a wrong status expectation' on ci/day02-checks-tyreece. Run URL, failed step and error line pending: not captured in this record. |
| Green source revision, run URL or replay evidence, test count and repair | d9828ff 'fix(tests): expect 422 for overlong booking title' on ci/day02-checks-tyreece. Run URL and test count pending: not captured in this record. |
| PR base/compare, link or redacted local diff, partner’s specific review point | pending: add PR link or redacted diff, and your partner's review point. |
| Your decision, owner, condition, one uncovered risk and what would change the decision | pending: your release decision, owner, condition and uncovered risk. |
| Day 3 handover: working branch/ref, personal role, last successful check, blocker/next action | Working branch feature/health-service-tyreece, suite 81 passed locally. Blocker: hosted run evidence and peer review still to collect. (ran) |

For a hosted PR, record its source revision alongside the displayed run URL and the tested merge SHA when visible. If personal access is blocked, name what still needs to run on your device or hosted repository. Do not copy a partner’s evidence as your own.
