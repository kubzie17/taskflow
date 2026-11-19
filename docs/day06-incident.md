**Day 6 Incident Review: Deleted Diagnostic File in Git History (Challenge 3)**

Date: 16 November 2026

**Outcome**

Confirmed that deleting app/dispatch.local.env did not remove it from Git history. The fictional value is still readable from the earlier commit. The Git ignore rules were improved so the file type is now ignored, and .env.example is still trackable. The Docker exclusion was updated but could not be tested because the Docker daemon was not running.

All values in this exercise are fictional (TRAINING_ONLY_NOT_A_CREDENTIAL) and cannot access any real service.

**What was observed**

A disposable repository was created with `python exercises/day06_incident.py`. It was a separate temporary repository, so the normal TaskFlow project was not touched. In the disposable repository:

- `git status -sb` printed `## master`, so the working tree was clean.
- `git log --oneline --all -- app/dispatch.local.env` printed two commits:
  - 62e8bf6 Remove diagnostic file from current tree
  - b1f4696 Add temporary diagnostic settings
- `git show HEAD~1:app/dispatch.local.env` printed `DISPATCH_DIAGNOSTIC=TRAINING_ONLY_NOT_A_CREDENTIAL`.
- Checking whether the file exists in the working directory (`Test-Path app/dispatch.local.env`) returned False.

Both observations are true because Git stores every commit as a permanent snapshot. The later commit removed the file from the latest snapshot, which is what the working directory shows. The earlier snapshot still contains the file, and anyone with the repository can read it by asking for that revision.

**Git ignore rules: before and after**

Commands were run from the real project root.

Before changes (the problem):

- `git check-ignore -v --no-index app/dispatch.local.env` printed nothing. Exit code 1, so the file was not ignored.
- `git check-ignore -q --no-index .env.example` exit code 1, so the example was not ignored.
- `git ls-files -- .env.example` printed `.env.example` (tracked).

Cause: the existing rule `.env.*` only matches names that start with `.env.`, so a file named dispatch.local.env slipped through.

Changes made (existing rules were kept, nothing was removed):

- .gitignore: added `*.local.env` below the existing `.env.*` and `!.env.example` rules.
- .dockerignore: added `**/*.local.env` after the existing `**/.env.*` rule. It is placed after the `!app/**` allow rule so it takes priority, because the last matching rule wins.

After changes (the fix):

- `git check-ignore -v --no-index app/dispatch.local.env` printed `.gitignore:14:*.local.env  app/dispatch.local.env`. Exit code 0, so the file is now ignored.
- `git check-ignore -q --no-index .env.example` exit code 1, so the example is still not ignored.
- `git ls-files -- .env.example` printed `.env.example`, so it is still tracked.
- `git check-ignore -q --no-index app/main.py` exit code 1, so the application source is still not ignored.

**Docker build context**

Docker 29.9.3 and Buildx 0.38.2 are installed. `python exercises/day06_context_probe.py` failed with "failed to connect to the docker API ... check if the path is correct and if the daemon is running" and printed "The builder did not complete. Context exclusion is untested." Exit code 1.

Result: the Docker exclusion is untested. This is a limitation, not a pass. By reading the rules only, `**` excludes everything, `!app/**` allows application files, and the new `**/*.local.env` rule comes after it, so it should exclude the marker file while keeping app/main.py. That is a prediction from the rules, not an observed result. To close the gap, start the Docker engine and rerun the probe. It should print `Application file included: True | fictional marker included: False`.

**If this were a real credential leak**

Everything below is what should happen. None of it was observed or done in this exercise.

- Who to inform: the team lead or line manager, the security team (or whoever owns incident handling), and the owner of the service the credential gives access to. Repository admins should be told too, in case others have cloned or forked it.
- Revoke or rotate first: treat the credential as compromised from the moment it was committed. Revoke it at the service that issued it (for example disable the key or reset the password) and issue a new one. Do this before cleaning up Git. Deleting the file is not revoking the credential.
- Where else to look:
  - Whether the commit was ever pushed, and to which remotes and branches.
  - Forks, clones, pull requests and CI caches or artefacts.
  - CI logs, container images or build layers that copied the file, and package or backup archives.
  - Chat messages, tickets and screenshots where it may have been pasted.
  - The issuing service's access logs, for use of the credential since the commit.
- Verify the old credential no longer works: try to use it against the service in a safe, authorised way and confirm it is rejected. Confirm the new credential works and that the application uses it. Check the service's logs for any use of the old one after revocation.
- Clean the history afterwards if needed: rewriting history (for example with git filter-repo) and force-pushing can remove the file from the repository, but it cannot undo copies others already hold. It is a tidy-up step, not a replacement for revoking.

**Observed versus assumed**

Observed in this exercise:

- The file existed in the earlier commit b1f4696 and was removed in 62e8bf6.
- The earlier value was readable with `git show`.
- The ignore rule failed before the change and worked after it.
- .env.example stayed tracked and unignored.
- The Docker probe failed because the daemon was not running.

Not observed, only reasoned about:

- Whether the new Docker rule excludes the file in a real build.
- Anything about a real leak, since no real credential, remote or service was involved.

**Next actions**

- Learner or TaskFlow engineer: start the Docker engine, rerun `python exercises/day06_context_probe.py` and record the printed result.
- TaskFlow engineer: commit the .gitignore and .dockerignore changes on the course branch with a conventional commit message.
- Team: consider a pre-commit secret scan so a file like this is blocked before it reaches history.
- Second reviewer: check this write-up before it is final.
