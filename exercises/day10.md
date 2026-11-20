# Day 10 — Can Northbridge Trust, Recover and Release TaskFlow?

Friday 20 November 2026 · Microsoft Teams · 09:30–15:30 UK

Northbridge needs evidence that its pilot works, that engineers can detect and recover a failure, and that every course resource has an owner at close. Day 9 Challenge 2 was homework. Its completion must be demonstrated today.

Work in three teams of 2, 2 and 3. Rotate operator, reviewer and evidence reporter. The pair combines reviewer/reporter. Each learner explains one observation rather than watching the same person operate all day. Use your existing repository and original AWS target. Keep a private copy of the [evidence workbook](Day_10_Assessment_and_Resource_Ledger.xlsx) or [Markdown evidence form](day10-evidence.md) outside Git.

| Time | Work |
|---|---|
| 09:30–10:15 | [Verify homework or complete a focused continuation](day10-homework-check.md) |
| 10:15–10:45 | [Challenge 1](day10-challenge1-brief.md): monitoring baseline |
| 10:45–11:00 | Break |
| 11:00–12:00 | Challenge 1: diagnose and recover |
| 12:00–13:00 | Lunch |
| 13:00–14:00 | [Challenge 2](day10-challenge2-brief.md): checkpoint and restore |
| 14:00–14:15 | [Independent release review](day10-release-review.md) |
| 14:15–14:30 | Break |
| 14:30–15:25 | [Verified cleanup](day10-cleanup.md) |
| 15:25–15:30 | Course closure and outstanding ownership |

Bring new files into your existing checkout without discarding work. First save intended source edits on their owning branch and check `git status -sb`. On a clean branch tracking the trainer use `git pull --ff-only`. On a clean personal branch use `git fetch origin`, then `git cherry-pick MATERIALS_COMMIT` with the actual published hash. An independent template repository uses `git fetch https://github.com/kubzie17/taskflow.git main` before the cherry-pick. If a conflict needs investigation, use `git cherry-pick --abort` and compare with the trainer. Never reset or replace Wednesday's private Terraform state.

Run new helper tests with `python -m pytest tests/test_day10_operations.py -q`. This does not deploy anything. The full release suite still requires your Day 9 work to be completed. The Day 10 helpers do not require new Python packages or an image rebuild.

Post only a short redacted status in the main Teams chat at 10:15, before lunch, 14:00 and 15:20. Use `Team | AWS/local/instructor observed | last verified result | first blocker | next action`. Keep passwords, bearer tokens, account-specific configuration, state and raw secrets off screen and out of Git.

The trainer has separate progressive hints. [Local continuation](day10-local.md) preserves the operations/recovery objectives if a genuine cloud blocker remains. An AWS observation on the instructor host is labelled as such; local evidence is never labelled as your AWS recovery.
