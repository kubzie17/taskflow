# Opening check — What did the Day 9 homework establish?

**09:30–10:15, a firm 45-minute limit.** Use the existing Day 9 deployment, your private evidence and the original state custodian. Tools are PowerShell, AWS CLI, Session Manager plugin, Docker on the host, and the project Python environment.

## 1. Establish the real target

**LOCAL WINDOWS POWERSHELL**, in the existing `infra/day08` directory. Replace the placeholders with the actual approved values. Use the profile's established sign-in method; run SSO login only for an SSO-configured profile.

```powershell
$env:AWS_PROFILE = 'YOUR_APPROVED_PROFILE'
$env:AWS_REGION = 'YOUR_EXISTING_REGION'
$InstanceId = 'YOUR_ORIGINAL_INSTANCE_ID'
$VolumeId = 'YOUR_ORIGINAL_BOOKINGS_VOLUME_ID'
aws sts get-caller-identity
terraform state list
terraform output
aws ec2 describe-instances --instance-ids $InstanceId --query 'Reservations[0].Instances[0].[InstanceId,State.Name,IamInstanceProfile.Arn,MetadataOptions]' --output json
aws ec2 describe-volumes --volume-ids $VolumeId --query 'Volumes[0].[VolumeId,Attachments]' --output json
```

If stopped, use `aws ec2 start-instances --instance-ids $InstanceId`, then `aws ec2 wait instance-status-ok --instance-ids $InstanceId`. Check `aws ssm describe-instance-information --filters "Key=InstanceIds,Values=$InstanceId" --output json`. Connect via **EC2 → Instances → your instance → Connect → Session Manager** when Online. An empty state list is an unresolved state-location issue, not permission to create replacement infrastructure.

## 2. Verify the running release

**REMOTE AWS EC2 LINUX SESSION**

```bash
sudo findmnt --target /srv/taskflow-data/app
sudo lsblk -o NAME,SERIAL,FSTYPE,UUID,MOUNTPOINTS
sudo docker ps -a --filter name=taskflow
sudo docker inspect taskflow --format '{{.Config.Image}}'
sudo docker inspect taskflow --format '{{json .Config.Cmd}}'
sudo docker logs --tail 30 taskflow
sudo cat /var/lib/taskflow-release/current.json
```

Match the mounted disk serial to the original EBS ID. The image must be the recorded passing ECR digest and the command must use `exercises.day09_entry:application --factory`. The ledger is non-secret; do not open the mounted identity file. A host restart clears `/run`, so the trainer must use the existing fixed release document with the known passing digest to retrieve the identity again. A plain `docker start` is insufficient when that file is missing.

## 3. Prove application behaviour

In a **new local PowerShell** window set the three values again, because ordinary variables do not carry between windows.

```powershell
$env:AWS_PROFILE = 'YOUR_APPROVED_PROFILE'
$env:AWS_REGION = 'YOUR_EXISTING_REGION'
$InstanceId = 'YOUR_ORIGINAL_INSTANCE_ID'
aws ssm start-session --target $InstanceId --document-name AWS-StartPortForwardingSession --parameters 'portNumber=8055,localPortNumber=8055'
```

Keep the tunnel open. From another local terminal at the repository root with the Python environment active, run `python -m exercises.day09_probe --url http://127.0.0.1:8055`. Enter the team's fictional phrases. Record the actual new booking ID, then run `sudo docker restart taskflow` remotely. After startup, run `python -m exercises.day09_probe --url http://127.0.0.1:8055 --expect-booking YOUR_RECORDED_ID` locally. The second probe must find that booking without adding another.

Required results: visitor 401, reader reads 200 and creates 403, dispatcher creates 201, invalid-token write 401, denied writes leave counts unchanged. Keep source commit, CI evidence, ECR digest, original IDs, mount UUID and retained booking ID together.

## Route A — Evidence passes

Record your verified target and move to the monitoring baseline. Do not rebuild or repeat deployment just because another team is catching up. The trainer installs the small Day 10 host helpers before the monitoring task.

## Route B — First incomplete step

Record the first failing component, exact message and next action. Use the existing [Day 9 challenge](day09-challenge2-brief.md) with the trainer for a focused repair. A source/CI problem remains a release blocker. Use an independently passing instructor image if necessary and label its provenance.

**Observed repository layout issue:** the published Day 9 Dockerfile and matching ignore file are under `exercises/`, while the workflow expects them at the root. In your repository, inspect both locations. If a completed root pair exists, preserve it. If only the exercises pair exists, complete your marked work there and copy both files to the root, then review and commit the intended changes. From the repository root:

```powershell
Test-Path Dockerfile.day09
Test-Path exercises/Dockerfile.day09
Select-String -Path exercises/day09_entry.py -Pattern 'TODO|raise RuntimeError'
# Only when the root pair is absent and your exercises pair is the reviewed completed version:
Copy-Item exercises/Dockerfile.day09 Dockerfile.day09
Copy-Item exercises/Dockerfile.day09.dockerignore Dockerfile.day09.dockerignore
```

The adapter may still contain TODO A, and the Dockerfile TODO_FACTORY. Complete and test these through the Day 9 gates; never substitute the historical Dockerfile. Do not overwrite a teammate's completed version.

At **10:15**, the trainer assigns either a working instructor AWS target or [local protected Docker continuation](day10-local.md). Record the missing AWS outcome and owner. Continue with real monitoring/recovery work, keeping its evidence scope explicit.

**Acceptance:** a peer has observed the checks, or the exact missing check and prepared continuation are recorded. Optional stretch: explain why image identity, healthy HTTP and correct mounted storage are three different observations.
