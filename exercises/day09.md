# Day 9 — From GitHub to AWS

**Thursday 19 November 2026 · in person · 09:30–15:30 UK**

Northbridge Repairs has an AWS foundation. Today your team must produce a tested container and use it to run protected TaskFlow with persistent bookings. Use three teams of 2, 2 and 3. Rotate the keyboard operator after each checkpoint. Your partner reviews the next command and predicts its result. In the three-person team, the third person records evidence and challenges the release decision.

Wednesday's two main challenges are complete. The tag `ReleaseStage=deploy-ready` records that infrastructure exercise. Today's test, image and application evidence determines whether the application can be released.

## Begin from your actual team handover

Save intended changes on their owning branch and inspect `git status -sb`. A clean branch tracking the published class branch can use `git pull --ff-only`. On a personal branch in the same repo, use `git fetch origin`, then `git cherry-pick MATERIALS_COMMIT`. The trainer supplies that actual commit. For an independent template repo, use `git fetch https://github.com/kubzie17/taskflow.git main`, then cherry-pick the supplied materials commit. Resolve conflicts with your trainer or use `git cherry-pick --abort` to return to the start of that operation. Keep the existing working Terraform directory and private state with its custodian.

Open the Day 8 private handover, and in **that team's existing** `infra/day08` directory run `terraform state list` and `terraform output`. Record the actual instance and bookings-volume IDs. If either is missing or the state directory is unavailable, tell the trainer while your team begins the build workshop. The trainer's reference host is the continuation route for an infrastructure blocker.

The cloud operator runs the continuity commands in Challenge 2 while the other learners begin Challenge 1. Allow ten minutes for this check. AWS Console observations decide whether your host is usable. Public course source still contains Wednesday's starter placeholders, so use your completed local files and state.

## Today's resources

- [Challenge 1](day09-challenge1-brief.md) builds and checks the release.
- [Challenge 2](day09-challenge2-brief.md) deploys and proves the application.
- [Configuration worksheet](day09-configuration.md) records which system owns each value.
- [Evidence and Friday handover](day09-evidence.md) stays in a personal file outside Git.
- [Progressive hints](day09-hints.md) opens when your trainer releases a hint.
- [Optional fault](day09-fault.md) takes ten minutes if the deployment is complete.
- [Local continuation](day09-fallback.md) uses the same protected package when AWS is blocked.

## Team setup

Use Windows PowerShell, VS Code, Python 3.12 in the existing virtual environment, Git, Docker Desktop running Linux containers, Terraform, AWS CLI v2 and the AWS Session Manager plugin. Your trainer prepares a scoped GitHub environment, OIDC role, private ECR repository, SSM deployment document and instance-role permissions before class. The AWS account, Region, team alias and original resources come from Wednesday's handover. The normal Region is Ireland `eu-west-1`.

Choose one team repository and one approved `main` branch for the release. Use a unique GitHub environment from `training-team-a`, `training-team-b` or `training-team-c`. Its environment name can differ from Wednesday's team alias. Match the environment to the correct ECR repository, role and instance. Each team has one release operator at a time.

## Completion

A completed day has a red gate that blocks packaging, a green release with a recorded image digest, a running protected API reached over an SSM tunnel, correct reader/dispatcher results, and the same booking after a container restart. Record partial completion precisely if the day ends earlier. Friday starts from that record.
