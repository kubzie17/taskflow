# Day 10 — Challenge 1: Investigate and Recover TaskFlow

**Time:** 13:00–13:35  
**Environment:** Your working Day 9 AWS deployment

## Scenario

Northbridge reports that TaskFlow has stopped responding.

You must identify the failing component, restore the service and demonstrate that the original booking data remains available.

## Step 1 — Check the normal state

In your **AWS EC2 Linux session**:

```bash
sudo docker ps --filter name=taskflow
sudo docker logs --timestamps --tail 20 taskflow
sudo findmnt --target /srv/taskflow-data/app
```

In your **local PowerShell terminal**, with the SSM tunnel still connected:

```powershell
python -m exercises.day09_probe --url http://127.0.0.1:8055 --expect-booking YOUR_RECORDED_BOOKING_ID
```

Record the results.

## Step 2 — Predict the fault

Before the trainer introduces the incident, answer:

1. What would happen if FastAPI stopped but EC2 remained Running?
2. Would CloudWatch CPU necessarily show the problem?
3. Which commands could identify the failing component?

## Step 3 — Record the incident time

When the trainer announces the fault, run in local PowerShell:

```powershell
$FaultAt = [DateTimeOffset]::UtcNow
$FaultAt.ToString("o")
```

Try:

```powershell
try {
    Invoke-RestMethod http://127.0.0.1:8055/health
} catch {
    $_.Exception.Message
}
```

Record the result.

## Step 4 — Investigate

Use your EC2 Linux terminal:

```bash
sudo docker ps -a --filter name=taskflow
sudo docker logs --timestamps --tail 30 taskflow
```

Check EC2 and Systems Manager in the AWS Console.

Do not attempt a repair until you have explained your diagnosis to the trainer.

## Step 5 — Repair

Agree the smallest safe repair with the trainer.

Perform only the authorised action.

## Step 6 — Verify

Run the protected application probe again, using the original booking ID.

Record when verification succeeds:

```powershell
$RecoveredAt = [DateTimeOffset]::UtcNow
[math]::Round(($RecoveredAt - $FaultAt).TotalSeconds, 1)
```

## Questions to answer

- Which component failed?
- What evidence established that?
- Was EC2 still running?
- Did the database survive?
- How long did recovery take?
- Which monitoring improvement would help detect this automatically?

**Success:** A supported diagnosis, a safe repair, a working protected API and the original booking still present.
