# Challenge 3 — Investigate a Deleted Secret in Git History

**Time:** Approximately 30 minutes

## Scenario

A developer accidentally committed a local configuration file:

`app/dispatch.local.env`

They noticed the mistake and deleted the file in a later commit.

The developer believes the problem is solved because the file no longer exists in the working directory.

Your task is to investigate that claim using Git and improve TaskFlow's safeguards.

**All values in this exercise are fictional and cannot access any real service.**

## Step 1 — Generate a disposable incident

From your normal TaskFlow project root, run:

```powershell
python exercises/day06_incident.py
```

The script prints the location of a newly created temporary Git repository.

Do not delete or replace your normal TaskFlow project.

## Step 2 — Open a second PowerShell terminal

Change into the temporary folder printed by the script:

```powershell
Set-Location "<TEMPORARY_FOLDER_FROM_SCRIPT>"
```

Replace the placeholder with the actual path printed.

Run:

```powershell
git status -sb
git log --oneline --all -- app/dispatch.local.env
```

Record the two commit IDs related to the diagnostic file.

## Step 3 — Investigate the previous revision

Run:

```powershell
git show HEAD~1:app/dispatch.local.env
```

What value does the file contain?

Does the file still exist in the current working directory?

Explain how both observations can be true.

## Step 4 — Return to your normal TaskFlow repository

In your original terminal, open:

- `.gitignore`
- `.dockerignore`
- `.env.example`

Do not make changes to the disposable incident repository.

## Step 5 — Test the current Git ignore rules

From the real project root:

```powershell
git check-ignore -v --no-index app/dispatch.local.env
```

Then check the exit code:

```powershell
$LASTEXITCODE
```

Also test:

```powershell
git check-ignore -q --no-index .env.example
$LASTEXITCODE
```

And:

```powershell
git ls-files -- .env.example
```

Record what you observe before making changes.

## Step 6 — Improve the safeguards

Modify your existing `.gitignore` and `.dockerignore` files so that:

1. Files ending in `.local.env` are excluded appropriately.
2. Necessary TaskFlow application files are still included.
3. The safe `.env.example` template is still trackable.
4. Existing useful ignore rules are preserved.

Do not replace the entire ignore files or remove important project files.

## Step 7 — Verify your changes

Repeat:

```powershell
git check-ignore -q --no-index app/dispatch.local.env
$LASTEXITCODE
```

Expected after a correct Git ignore repair: exit code **0**.

Then:

```powershell
git check-ignore -q --no-index .env.example
$LASTEXITCODE
```

Expected: exit code **1**, meaning the example is not ignored.

Verify it remains tracked:

```powershell
git ls-files -- .env.example
```

## Step 8 — Investigate the Docker build context

If Docker Buildx is available, run:

```powershell
python exercises/day06_context_probe.py
```

The provided probe creates a disposable build context with harmless files.

You need to determine whether the fictional diagnostic marker is excluded while an ordinary application source file remains included.

If Docker is unavailable, inspect the rules and document that an actual build-context check remains untested.

## Step 9 — Write your incident response

Record what should happen if this were a real credential leak.

Include:

1. Who should be informed.
2. How the exposed credential should be revoked or rotated.
3. Which additional locations would need investigation.
4. How to verify the old credential no longer works.

Distinguish what you actually observed from what might have happened.

## Acceptance criteria

You can demonstrate:

- The file was committed in an earlier revision.
- It was removed from the current working tree.
- Its previous contents remained accessible through Git history.
- Your Git ignore safeguard works.
- `.env.example` remains trackable.
- Your Docker exclusion was tested, or its verification limitation was recorded.
- Deleting a secret is not equivalent to revoking it.
