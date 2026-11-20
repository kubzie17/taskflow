# Local protected continuation

Use this only after the 10:15 checkpoint or a genuine later AWS blocker. Record the first missing AWS step. The instructor demonstrates actual CloudWatch data on the prepared AWS reference while you complete genuine local Docker/SQLite operations. Mark these as different evidence sources.

## 1. Establish the passing protected image

Use your existing verified local Day 9 container or the trainer's independently gated reference build. Keep the Day 9 dependency rule, current audit, pytest and actual image smoke test. A failed security gate remains a blocker. The current published Docker starters are under `exercises`; the build workflow expects the completed pair at the root. Follow the opening check and the trainer's reference procedure. Do not use the historical `app.main:app` image.

The commands below assume the Day 9 local container is `taskflow-day09-local` on local port 18055, using its fictional identity and persistent volume. The trainer's private runbook supplies exact creation steps if it does not yet exist. These are **LOCAL WINDOWS POWERSHELL** commands from the repository root with the Python environment active.

```powershell
$Original = 'taskflow-day09-local'
$OriginalInfo = (docker inspect $Original | ConvertFrom-Json)[0]
if ($LASTEXITCODE -ne 0) { throw 'The original protected container is not available' }
if ($OriginalInfo.Config.Cmd -notcontains 'exercises.day09_entry:application') { throw 'Wrong application entry point' }
$Image = $OriginalInfo.Config.Image
$IdentityFile = ($OriginalInfo.Mounts | Where-Object Destination -eq '/run/secrets/identity.json').Source
$DataMount = $OriginalInfo.Mounts | Where-Object Destination -eq '/var/lib/taskflow'
if ($DataMount.Type -eq 'volume') {
    $DataSpec = "type=volume,src=$($DataMount.Name),dst=/source"
} elseif ($DataMount.Type -eq 'bind') {
    $DataSpec = "type=bind,src=$($DataMount.Source),dst=/source"
} else { throw 'Review the actual source data mount with the trainer' }
python -m exercises.day09_probe --url http://127.0.0.1:18055
```

Record the actual booking ID. Verify it with `--expect-booking YOUR_RECORDED_ID` after a controlled `docker restart $Original`. Record a local image ID with `docker image inspect $Image --format '{{.Id}}'`; this is not an ECR manifest digest.

## 2. Complete the monitoring incident

Use `python -m exercises.day10_observe --container taskflow-day09-local --port 18055 --phase baseline` for the local baseline. The private fault operator introduces the approved reversible fault. Use the same command with `--phase fault` while investigating, and `--phase recovered` after the repair and protected probe. Do not add `--upload` from this local route. Record the separate actual instructor CloudWatch observation and its target/time.

## 3. Prepare a separate recovery area

Pick a new run directory. The safety helper refuses an existing checkpoint or restore target.

```powershell
$RunName = 'local-friday01'
$LocalRecovery = Join-Path $HOME ('.taskflow-day10-local\' + $RunName)
$Restored = Join-Path $LocalRecovery 'restored'
New-Item -ItemType Directory -Force $Restored | Out-Null
$DbHelper = (Resolve-Path 'exercises/day10_db.py').Path
$HelperSpec = "type=bind,src=$DbHelper,dst=/opt/day10_db.py,readonly"
$RecoverySpec = "type=bind,src=$LocalRecovery,dst=/recovery"
$RestoredSpec = "type=bind,src=$Restored,dst=/var/lib/taskflow"
python -m exercises.day10_client create --label A --url http://127.0.0.1:18055
```

Record A. Run the known helper in a temporary container using the same checked image. It has no network and does not receive an identity file. It opens the original database through SQLite read-only mode; the source mount permits SQLite's WAL shared-memory coordination if needed.

```powershell
docker run --rm --user 0 --network none --read-only --tmpfs /tmp --mount $DataSpec --mount $HelperSpec --mount $RecoverySpec --entrypoint python $Image /opt/day10_db.py checkpoint --source /source/taskflow.db --target /recovery/checkpoint.db
if ($LASTEXITCODE -ne 0) { throw 'Checkpoint failed. Keep the original intact.' }
python -m exercises.day10_client create --label B --url http://127.0.0.1:18055
python -m exercises.day10_client list --role reader --url http://127.0.0.1:18055
```

Record checkpoint time/hash and B's actual ID. Confirm both original records, then predict the restored result. Start the timekeeper's recovery clock, stop the named original container and restore into the separate directory:

```powershell
$RecoveryStart = [DateTimeOffset]::UtcNow
docker stop --time 20 $Original
docker run --rm --user 0 --network none --read-only --tmpfs /tmp --mount $HelperSpec --mount $RecoverySpec --entrypoint python $Image /opt/day10_db.py restore --source /recovery/checkpoint.db --target /recovery/restored/taskflow.db
if ($LASTEXITCODE -ne 0) { throw 'Restore failed. Inspect the error.' }
docker run --rm --user 0 --network none --read-only --tmpfs /tmp --mount $HelperSpec --mount $RecoverySpec --entrypoint python $Image /opt/day10_db.py inspect --source /recovery/restored/taskflow.db
```

## 4. Start a separate protected recovery service

Confirm `taskflow-recovery` does not already exist with `docker ps -a --filter name=taskflow-recovery`. Preserve any previous candidate's evidence before removing only that course container. Prepare ownership of the new restored path, then start the candidate with the existing fictional identity:

```powershell
docker run --rm --user 0 --network none --mount $RestoredSpec --entrypoint sh $Image -c 'chown 10001:10001 /var/lib/taskflow /var/lib/taskflow/taskflow.db && chmod 750 /var/lib/taskflow && chmod 600 /var/lib/taskflow/taskflow.db'
if ($LASTEXITCODE -ne 0) { throw 'Recovery ownership setup failed' }
docker run -d --name taskflow-recovery --restart no --read-only --cap-drop ALL --security-opt no-new-privileges --tmpfs /tmp -p 127.0.0.1:18056:8000 --mount $RestoredSpec --mount "type=bind,src=$IdentityFile,dst=/run/secrets/identity.json,readonly" --env APP_ENVIRONMENT=local --env TASKFLOW_DB=/var/lib/taskflow/taskflow.db --env TASKFLOW_IDENTITY_FILE=/run/secrets/identity.json $Image
if ($LASTEXITCODE -ne 0) { throw 'Recovery container did not start' }
python -m exercises.day10_client list --role reader --url http://127.0.0.1:18056
python -m exercises.day09_probe --url http://127.0.0.1:18056 --expect-booking YOUR_BOOKING_A_ID
```

Wait for startup if necessary; inspect `docker logs --tail 30 taskflow-recovery`. Record the comparison before running a full probe that deliberately creates a recovery-only booking. Stop the clock after the required checks with `$RecoveryEnd = [DateTimeOffset]::UtcNow` and `[math]::Round(($RecoveryEnd - $RecoveryStart).TotalSeconds,1)`. Record the measured scope and compare objectives separately.

The original data volume still contains its original records. Start the original again only if needed for final comparison. A successful local restore does not establish AWS volume/AZ recovery.

If Docker is also unavailable, the trainer's Python-only continuation runs the same protected factory with separate absolute source/restore database paths. Label that as local Python/database evidence and retain the missing Docker/AWS outcomes.

## 5. Local cleanup

After evidence and trainer confirmation, stop and remove only `taskflow-recovery` and the named course original. Remove the exact course data volume only after verifying its name/ownership. Inspect `$LocalRecovery` before deleting this disposable run directory. Delete the fictional local identity file when no other retained course process needs it. Do not run account-wide AWS deletion or broad Docker pruning from this fallback. Your actual AWS ledger still requires reconciliation, even when the application exercise was local.
