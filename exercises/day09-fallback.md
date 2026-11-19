# Day 9 local continuation

Use this when a real cloud blocker remains after brief troubleshooting. Record the AWS step and error, then complete the same protected application, configuration and persistence checks locally. The trainer can separately demonstrate the cloud deployment on their rehearsed target.

## Build and verify

Complete the learner edits first. From the repository root with the Python environment active, run the Day 6 dependency policy, install and run `pip-audit==2.10.1` against both requirements files, run all pytest tests, and build `Dockerfile.day09`. Every required check must pass. Then run `python -m exercises.day09_image_check taskflow:day09-local`. This tests an isolated container and cleans up its temporary resources.

## Keep a local Docker deployment for Friday

Use a dedicated private directory such as `$HOME\.taskflow-day09-local`. Generate the identity with the existing `make_state` and `initialise_file` helpers. The trainer's private runbook gives the exact interactive command. The fictional passphrases are entered with `getpass` and the file remains outside the repo. This local route uses a private file in place of the unavailable AWS retrieval step.

Create a named Docker volume and initialise its app ownership using the reviewed image. All commands below are **local PowerShell**. Set `$IdentityFile` to the generated identity file's absolute path.

```powershell
docker volume create taskflow-day09-local-data
docker run --rm --user 0 --entrypoint chown --mount type=volume,src=taskflow-day09-local-data,dst=/var/lib/taskflow taskflow:day09-local 10001:10001 /var/lib/taskflow
docker run -d --name taskflow-day09-local --read-only --cap-drop ALL --security-opt no-new-privileges --tmpfs /tmp -p 127.0.0.1:18055:8000 --env APP_ENVIRONMENT=local --env TASKFLOW_DB=/var/lib/taskflow/taskflow.db --env TASKFLOW_IDENTITY_FILE=/run/secrets/identity.json --mount "type=bind,src=$IdentityFile,dst=/run/secrets/identity.json,readonly" --mount type=volume,src=taskflow-day09-local-data,dst=/var/lib/taskflow taskflow:day09-local
python -m exercises.day09_probe --url http://127.0.0.1:18055
docker restart taskflow-day09-local
```

Wait for startup and repeat the probe with `--expect-booking YOUR_RECORDED_INTEGER_ID`. On Windows Docker Desktop, check that the identity directory is shared and readable by the Linux container. On native Linux, the trainer should give UID 10001 read access to the specific file while keeping its parent private. Never change permissions recursively on an unrelated home directory.

Stop this named container at close. Retain its named volume and fictional identity for Friday. After the Friday recovery demonstration, remove the stopped container, remove this named volume when its data is confirmed disposable, and delete the private fictional identity. Keep the exact names so other Docker work is unaffected.

If Docker itself is unavailable, run the same adapter with Uvicorn on loopback using absolute local paths. Prove the Python process restart and record that Docker, EBS and AWS execution remain unverified.


For that Python-only continuation, keep the generated `$IdentityFile` from the trainer step. Start at the repository root with the virtual environment active. These are **local PowerShell** commands:

```powershell
$LocalData = Join-Path $HOME '.taskflow-day09-local\data'
New-Item -ItemType Directory -Force $LocalData | Out-Null
$env:APP_ENVIRONMENT = 'local'
$env:TASKFLOW_DB = Join-Path $LocalData 'taskflow.db'
$env:TASKFLOW_IDENTITY_FILE = $IdentityFile
python -m uvicorn exercises.day09_entry:application --factory --host 127.0.0.1 --port 18055 --no-access-log
```

Keep that terminal running. In another terminal, return to the same repository, activate the same virtual environment, and run `python -m exercises.day09_probe --url http://127.0.0.1:18055`. Record the booking ID. Stop Uvicorn with Ctrl+C, restart it with the same command in its original terminal, and use `--expect-booking YOUR_RECORDED_INTEGER_ID` in the tester terminal. This proves local process persistence; the cloud/container checks remain outstanding.
