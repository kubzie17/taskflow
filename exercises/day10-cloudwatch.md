# CloudWatch investigation and observation capture

Use your team's actual account, Region and original instance. The trainer prepares one log group `/taskflow/TEAM/day10`, a stream named with the instance ID, and permission for the node role to write only that stream. There is no new monitoring agent, custom metric or mandatory alarm.

## Inspect a real infrastructure metric

1. In **AWS Console → CloudWatch → Metrics → All metrics → EC2 → Per-Instance Metrics**, filter by the exact original instance ID.
2. Select `CPUUtilization`. Use **Average**, a **5-minute period** and the most recent hour. Record the real timestamp, value, unit and period. Refresh if the host has only just started; an empty graph is missing evidence, not zero CPU.
3. Inspect `StatusCheckFailed` as a complementary signal if available. Basic EC2 CPU data normally uses 5-minute periods; status checks have their own 1-minute cadence.
4. Predict whether those host metrics alone would prove that a dispatcher can create a booking.

## Capture actual application evidence

Day 9 uses Docker's `local` log driver. Those files are not automatically CloudWatch streams and are not plain-text files to tail with an agent.

The supplied helper reads actual Docker status, a loopback `/health` response and a narrow allow-list of startup/shutdown log lines. With `--upload`, it sends one JSON observation to the trainer-prepared CloudWatch stream. It never reads the identity file or sends tokens, passwords, booking titles or the complete Docker configuration. It is a **manual snapshot**, not continuous monitoring. Repeated captures can contain the same earlier lifecycle line; inspect each line's timestamp.

**REMOTE AWS EC2 LINUX SESSION** — replace the placeholders once and retain this terminal.

```bash
ACCOUNT='YOUR_APPROVED_12_DIGIT_ACCOUNT'
REGION='YOUR_EXISTING_REGION'
TEAM='YOUR_WEDNESDAY_ALIAS'
INSTANCE='YOUR_ORIGINAL_INSTANCE_ID'
sudo python3 /opt/taskflow-day10/day10_observe.py --phase baseline --account "$ACCOUNT" --region "$REGION" --group "/taskflow/$TEAM/day10" --stream "$INSTANCE" --upload
```

A successful uploader says CloudWatch accepted the snapshot. This means the observation was accepted, even when its application-health field is false. Verify the event itself next.

Open **CloudWatch → Logs → Log groups → exact team group → Log streams → original instance ID**. Select the current time window and refresh. Expand the JSON event. Record `captured_utc`, `phase`, `container_status`, `application_healthy`, HTTP status and a real lifecycle line where available. A missing lifecycle line is possible if there was no matching startup/shutdown within the last 15 minutes.

Later repeat the same command with `--phase fault` and `--phase recovered`. Do not fabricate a CloudWatch event if upload fails. Capture the actual error and use the trainer's live stream for the CloudWatch investigation while retaining local observations separately.

## Interpret and improve

A metric measures a value over time; a log event records something observed at a particular time. A log group groups related streams and sets retention. A stream holds an ordered source's events. An alarm compares a metric against a threshold over evaluation periods, with a chosen missing-data policy and optional action. Today you propose a useful alarm; you do not need to create a paid alarm resource.

Describe a future signal that would detect a failed authenticated booking operation, including collection interval and missing-data behaviour. A real production design needs automated collection and alerting. Today's manual snapshots cannot provide unattended detection.

**Costs:** basic EC2 monitoring is used as already configured. Log ingestion/storage and some query/API features can be billable depending on allowance and Region. The trainer requests one-day log retention and verifies the effective policy. Delete the course-owned group after preserving evidence at cleanup; retention alone is not immediate deletion.
