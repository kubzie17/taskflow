# Challenge 2 — Investigate a Vulnerable Dependency Proposal

**Time:** Approximately 45–50 minutes

## Scenario

Northbridge has received a vendor proposal to downgrade PyJWT to version 2.13.0.

The vendor claims their login demonstration passed, so they believe the older version is suitable.

The current reviewed TaskFlow requirements specify PyJWT 2.15.1.

You must investigate the proposed change and decide whether it should be approved.

**Do not install PyJWT 2.13.0.** The proposed value is supplied as inert text for investigation.

## Step 1 — Open the evidence

Open these files:

- `requirements.txt`
- `exercises/day05-requirements.txt`
- `exercises/day06-case.md`
- `exercises/day06-proposal.case`

Read **Exhibit A** in `day06-case.md`.

## Step 2 — Identify the actual version

In PowerShell, run:

```powershell
python -c "from importlib.metadata import version; print(version('PyJWT'))"
```

Record:

- The version declared in the requirements.
- The version actually installed.
- The proposed version.
- Your Python interpreter version.

Do not assume the installed version is correct just because the requirements file contains a particular pin.

## Step 3 — Investigate the advisory

Using Exhibit A, record:

- Advisory ID: `GHSA-9v7f-9g4p-ffgj`
- Affected version range.
- First patched version.
- Which part of PyJWT is affected.
- What conditions are required for exploitation.

Identify whether the finding affects every possible JWT verification path or a more specific part of the library.

## Step 4 — Inspect TaskFlow's use of PyJWT

Open:

- `exercises/day05_identity.py`
- `exercises/day05_cognito.py`

Find how each implementation verifies tokens.

Compare:

1. The normal local identity implementation.
2. The optional Cognito/external-key implementation.

Answer:

- Which path uses a locally held signing key?
- Which path may retrieve public keys from a remote endpoint?
- Does a successful local login demonstrate that the remote-key path is secure?

## Step 5 — Test the proposed pin without installing it

From the project root:

```powershell
python exercises/day06_gate.py check --pin-file exercises/day06-proposal.case
```

In PowerShell, immediately check:

```powershell
$LASTEXITCODE
```

Record the message and exit code.

## Step 6 — Test the approved course pin

Run:

```powershell
python exercises/day06_gate.py check
```

Again record:

```powershell
$LASTEXITCODE
```

Compare the two outcomes.

## Step 7 — Test existing application behaviour

Run:

```powershell
python -m pytest -q tests/test_day05_access.py
python -m pytest -q
```

Record the actual results.

If the Day 5 test file is missing or unfinished, report that limitation instead of claiming a clean regression run.

## Step 8 — Write your engineering decision

Create:

`docs/day06-decision.md`

Include:

1. The proposed change.
2. Current declared and installed versions.
3. Advisory findings.
4. Whether the affected code path is used by TaskFlow.
5. Whether to approve, reject or request more evidence.
6. Test results.
7. Remaining security uncertainty.
8. The next action and its owner.

## Acceptance criteria

You can demonstrate:

- One real dependency relationship.
- The difference between a proposed and installed version.
- The vulnerability's affected range and technical preconditions.
- An observed blocked proposal check.
- An observed approved-pin check.
- A justified decision supported by actual evidence.

**Do not change the policy checker to make the proposed vulnerable version pass.**
