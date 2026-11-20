# Challenge 2 — Can Northbridge Recover Its Bookings?

**13:00–14:00, 60 minutes.** A fictional incident occurs after Northbridge's most recent database checkpoint. Establish exactly which bookings can be recovered and how long usable recovery takes. Preserve the original database throughout.

**Starting files and tools:** completed protected Day 9 deployment, `exercises/day10_client.py`, `exercises/day10_db.py`, `docs/day10-recovery-plan.example.json`, SSM, local Python environment and your private evidence form. The trainer has installed the database helper and recovery launcher on EC2. The provided helper is operational scaffolding; your work is to plan, perform, compare and justify recovery. It uses SQLite's online backup API and refuses an existing target.

## 1. Agree the recovery experiment

Save your own copy of the recovery-plan example outside Git. Set a unique lowercase run name, for example `team-a-friday01`. Record the expected source, checkpoint and isolated restore paths. Agree a proposed RTO and RPO with units. Pause additional learner booking writes during the checkpoint boundary so the A/B sequence remains interpretable. Predict the records you expect in the checkpoint and recovery, then keep that prediction for comparison.

## 2. Create Booking A through the protected API

**LOCAL WINDOWS POWERSHELL**, at the repo root with the venv and original tunnel active:

```powershell
python -m exercises.day10_client create --label A --url http://127.0.0.1:8055
```

Enter the fictional dispatcher phrase. Record the actual returned ID and timestamp. Do not assume it is 1.

## 3. Create a consistent checkpoint

**REMOTE AWS EC2 LINUX SESSION** — use the same run name for all following steps:

```bash
RUN='team-a-friday01'
sudo findmnt --target /srv/taskflow-data/app
sudo install -d -m 0700 "/srv/taskflow-data/recovery/$RUN"
sudo python3 /opt/taskflow-day10/day10_db.py checkpoint --source /srv/taskflow-data/app/taskflow.db --target "/srv/taskflow-data/recovery/$RUN/checkpoint.db"
```

Record the completion time, hash, record count and checkpoint path. The helper also creates a `.record.json` file alongside the checkpoint. If a target exists, select a new run name; do not delete or overwrite an existing checkpoint just to make the command pass.

## 4. Create Booking B after the checkpoint

**LOCAL WINDOWS POWERSHELL**

```powershell
python -m exercises.day10_client create --label B --url http://127.0.0.1:8055
python -m exercises.day10_client list --role reader --url http://127.0.0.1:8055
```

Record B's actual ID. Confirm both A and B exist in the original service before the incident. Keep one timekeeper and the same local clock for the recovery interval.

## 5. Start the recovery clock and isolate the failed service

The trainer confirms the reversible failure on the original service, with its data preserved. In the timekeeper's **local PowerShell** tester terminal, record `$RecoveryStart = [DateTimeOffset]::UtcNow` at the announced incident boundary and print `$RecoveryStart.ToString('o')`.

In the **remote Linux session**, after trainer confirmation:

```bash
sudo docker stop --time 20 taskflow
sudo install -d -m 0700 "/srv/taskflow-data/recovery/$RUN/restored"
sudo python3 /opt/taskflow-day10/day10_db.py restore --source "/srv/taskflow-data/recovery/$RUN/checkpoint.db" --target "/srv/taskflow-data/recovery/$RUN/restored/taskflow.db"
sudo python3 /opt/taskflow-day10/day10_db.py inspect --source "/srv/taskflow-data/recovery/$RUN/restored/taskflow.db"
sudo python3 /opt/taskflow-day10/day10_db.py inspect --source /srv/taskflow-data/app/taskflow.db
```

Compare the two actual lists of IDs with your prediction. Record what differs and why. The restore helper writes only the new target. It does not overwrite the preserved original, and the original remains available for comparison.

## 6. Verify usable recovery

With the trainer, start the separate candidate:

```bash
sudo python3 /opt/taskflow-day10/start-recovery.py --run "$RUN"
```

It uses the original passing image digest and the existing identity, with a separate database directory. It binds only to host loopback **8056**, keeping original host port 8055 separate. It never modifies the Day 9 release helper's fixed database path.

In a **new local PowerShell** window:

```powershell
$env:AWS_PROFILE = 'YOUR_APPROVED_PROFILE'
$env:AWS_REGION = 'YOUR_EXISTING_REGION'
$InstanceId = 'YOUR_ORIGINAL_INSTANCE_ID'
aws ssm start-session --target $InstanceId --document-name AWS-StartPortForwardingSession --parameters 'portNumber=8056,localPortNumber=18056'
```

In the local tester terminal run:

```powershell
python -m exercises.day10_client list --role reader --url http://127.0.0.1:18056
python -m exercises.day09_probe --url http://127.0.0.1:18056 --expect-booking YOUR_BOOKING_A_ID
```

The probe confirms the expected retained record and rejection rules without adding a new booking. To prove permitted writing, run the full probe **only after saving the original/restored comparison**, and record its newly created recovery-only booking ID. This creates one additional fictional record in the isolated restored database. A new record can reuse a missing integer ID, so compare the initial recovery evidence and booking title/event before those extra writes.

After the required checks, in the same timekeeper terminal:

```powershell
$RecoveryEnd = [DateTimeOffset]::UtcNow
[math]::Round(($RecoveryEnd - $RecoveryStart).TotalSeconds, 1)
$RecoveryEnd.ToString('o')
```

If the candidate cannot start promptly, verify the restored database's integrity and records, record that result as **database-only recovery**, and measure to that boundary. Do not label it restored service availability. Use the local continuation when needed.

## 7. Decide what this experiment proves

Record proposed RTO/RPO separately from measured interruption, checkpoint age at the incident and actual missing events. The copy helper's `copy_seconds` measures one database copy only; it is not total recovery time. The clock interval includes diagnosis/configuration/verification to your stated endpoint.

A checkpoint on the same EBS volume is useful for this logical recovery exercise. It cannot establish recovery after loss of that entire volume or Availability Zone. Recommend a suitable separately retained backup and an actual restore drill as a next improvement.

**Acceptance:** protected A/B creation, consistent checkpoint identity/time, preserved original, different restore target, observed comparison, actual recovery interval with scope, RTO/RPO analysis and one limitation. Do not assume or prefill the comparison results.

At 14:00 move to the release review with the evidence you actually have. Use separate hints if blocked. Stretch: explain how WAL affects a naive live-file copy and why the supported backup API avoids relying on a lone main database file.
