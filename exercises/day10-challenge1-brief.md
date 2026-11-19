# Challenge 1 — Can You Detect and Recover a TaskFlow Failure?

**90 minutes: 10:15–10:45 and 11:00–12:00.** Northbridge's pilot is due for review. Your team must establish normal behaviour, investigate an announced incident, restore service and defend the evidence.

**Tools and starting files:** the verified Day 9 target or declared fallback, AWS Console, SSM shell/tunnel, project Python environment, `day09_probe.py`, `day10_observe.py`, [CloudWatch guide](day10-cloudwatch.md) and your private evidence workbook. The trainer has installed the helper at `/opt/taskflow-day10/` on the host. The fault operator follows a separate private instruction. No database or volume damage is permitted.

## 1. Establish normal behaviour before the break

Allocate operator, reviewer/timekeeper and reporter. Record the original instance/EBS IDs, image digest and retained booking ID. In the **remote Linux session** inspect:

```bash
sudo docker ps --filter name=taskflow
sudo docker inspect taskflow --format '{{.Config.Image}}'
sudo docker logs --timestamps --tail 30 taskflow
sudo findmnt --target /srv/taskflow-data/app
```

Through the **local tunnel**, run `python -m exercises.day09_probe --url http://127.0.0.1:8055 --expect-booking YOUR_RECORDED_ID`. Capture a real EC2 CPU observation and a baseline application event using the CloudWatch guide. Label timestamps and evidence source. Predict which signals would distinguish a host problem from an application problem.

## 2. Investigate the announced incident after the break

Before the trainer introduces the reversible fault, agree a classroom recovery-time objective and write it down. This is a proposed pilot objective, not a measured result. Keep one timekeeper and one clock.

In that learner's **local PowerShell** tester terminal, record the starting boundary when the fault operator announces the change:

```powershell
$FaultAt = [DateTimeOffset]::UtcNow
$FaultAt.ToString('o')
try { Invoke-RestMethod http://127.0.0.1:8055/health } catch { $_.Exception.Message }
```

Record the observed request result. Inspect SSM connectivity, container state, startup/shutdown logs, the current image and the infrastructure metric. Capture a `fault` snapshot through the CloudWatch guide if the host can still run it. Decide which component failed and show evidence to the trainer before changing it. The metric might not show a visible change; record what actually happened.

## 3. Repair and prove recovery

Propose the smallest appropriate repair. Execute only the trainer-approved action on the named course service. Keep the original database and EBS volume intact. Verify health and use the retained-booking probe again, including its role and unchanged-denied-write checks. Capture a `recovered` observation.

When those checks pass, stop the same clock:

```powershell
$RecoveredAt = [DateTimeOffset]::UtcNow
[math]::Round(($RecoveredAt - $FaultAt).TotalSeconds, 1)
$RecoveredAt.ToString('o')
```

Record the interval and what its endpoints mean. Compare it with the objective. Do not report merely seeing EC2 Running as application recovery.

## 4. Explain what remains unproven

Answer: What does EC2 Running establish? What does low CPU establish? What does `/health` establish? Which observation proves an authorised booking operation? What cannot be detected while nobody runs the snapshot helper? Suggest one practical improvement with a defined signal and owner.

**Acceptance and evidence:** real CloudWatch observation, normal application result, actual failure, diagnosis tied to evidence, approved repair, successful protected request/retained booking, measured recovery interval and one limitation. Use separate fields for own AWS, instructor AWS observed and local evidence.

Use [progressive hints](day10-hints.md) only after recording a hypothesis. Stretch: propose an alarm threshold, sampling period and missing-data treatment, then explain the false-positive or missed-incident risk. Protect the noon handover and afternoon recovery slot.
