# Challenge 2 — Deploy protected TaskFlow on the original AWS host

**110 minutes · 13:00–14:15 and 14:30–15:05**

## Scenario and desired outcome

Northbridge needs the reviewed container running on Wednesday's EC2 host. Bookings must live on the separate EBS volume. The application must receive its identity configuration at runtime, enforce both roles, and retain a booking after a container restart.

Your team owns the deployment decision. Verify the host, mounted disk, image and application behaviour, then give Friday's operator enough evidence to continue.

## Prerequisites and starting files

Use Wednesday's actual `infra/day08` working directory and state, the original instance and data-volume IDs, an approved SSO session, a passing image from Challenge 1 and your assigned GitHub environment. The trainer supplies the reviewed host helper and safe EBS mounting procedure from the private pack. Inspect and discuss those operations together before executing them. AWS CLI v2 and the Session Manager plugin are required locally for the tunnel.

Open `docs/day09-runtime.example.json`, `exercises/day09_probe.py`, your completed workflow, and your personal copy of the evidence record. Keep generated host configuration and full account/resource IDs in your private working folder.

## 1. Confirm continuity and restart if required

In **local PowerShell**, use the existing team Terraform directory. Set the profile and Region from Wednesday, then run the commands below. Renew SSO if needed. Assign IDs from the actual outputs or verified private ledger. A missing output is a prompt to inspect the original state and AWS Console with the trainer.

```powershell
$env:AWS_PROFILE = 'YOUR_APPROVED_PROFILE'
$env:AWS_REGION = 'YOUR_EXISTING_TARGET_REGION'
aws sso login --profile $env:AWS_PROFILE
aws sts get-caller-identity
terraform state list
terraform output
$InstanceId = 'YOUR_ORIGINAL_INSTANCE_ID'
$VolumeId = 'YOUR_ORIGINAL_BOOKINGS_VOLUME_ID'
aws ec2 describe-instances --instance-ids $InstanceId --query 'Reservations[0].Instances[0].[InstanceId,State.Name,IamInstanceProfile.Arn,MetadataOptions]' --output json
aws ec2 describe-volumes --volume-ids $VolumeId --query 'Volumes[0].[VolumeId,AvailabilityZone,Attachments]' --output json
```

If the instance is `stopped`, start that instance and wait for its health checks.

```powershell
aws ec2 start-instances --instance-ids $InstanceId
aws ec2 wait instance-status-ok --instance-ids $InstanceId
aws ssm describe-instance-information --filters "Key=InstanceIds,Values=$InstanceId" --query 'InstanceInformationList[0].[InstanceId,PingStatus,AgentVersion]' --output json
```

In **EC2 → Instances → select instance → Connect → Session Manager**, connect when it is Online. The instance ID stays authoritative after a restart. An automatically assigned public IP may change. Give an actual blocker five minutes with the trainer, then use the instructor target or local continuation while recording the missing step.

## 2. Prepare the real bookings volume

Inside the **remote Linux SSM session**, inspect before changing anything.

```bash
sudo lsblk -o NAME,SERIAL,SIZE,FSTYPE,UUID,MOUNTPOINTS
findmnt /
sudo docker ps -a
```

The trainer leads the safe mounting procedure. Match the AWS EBS ID to its NVMe serial, identify the root device, check filesystem signatures and existing contents, and mount the bookings volume using its filesystem UUID. Formatting is permitted only after the trainer has verified that the exact bookings volume is newly empty. An existing filesystem is mounted and inspected. A partitioned or unexpected disk needs individual review.

The expected application directory is `/srv/taskflow-data/app`, owned by UID/GID `10001:10001`. The deployment helper checks that it is on the expected EBS volume before starting the container. Verify the mount with `findmnt --target /srv/taskflow-data/app`.

## 3. Complete runtime configuration

Save your own copy of `docs/day09-runtime.example.json` outside the repository. Supply the approved account, Region, team ECR name, original data-volume ID and parameter path. Determine the path from **Systems Manager → Parameter Store** and compare it with the exact parameter ARN permitted by the instance role. The trainer checks and installs this non-secret JSON at `/etc/taskflow/node.json`.

With the trainer, create two different fictional passphrases through the private identity helper. It creates a signing key and salted password records in memory and stores the resulting JSON as one Standard `SecureString`. The helper keeps the required application structure intact. Retain the fictional passphrases privately for the HTTP tests.

Predict how the secret reaches the application. The EC2 host's instance role retrieves it, writes an owner-restricted file under `/run/taskflow`, and mounts that file read-only at `/run/secrets/identity.json`. The container gets the file path through `TASKFLOW_IDENTITY_FILE`. Its database path is `/var/lib/taskflow/taskflow.db` on the EBS-backed bind mount. The metadata hop limit stays at 1, so the application does not depend on retrieving instance credentials inside Docker.

## 4. Deploy through the controlled workflow

The trainer confirms the root-owned host helper, safe mount and fixed SSM document are ready. Open **Actions → TaskFlow Day 9 → Run workflow** on `main`, select your environment, and set `deploy` to true.

This runs all checks and builds a new checked release. Record the **digest from this run**, even if the source commit matches the morning run. The deployment job sends that digest to the team's fixed SSM document on the original host. It waits for the command result. Inspect **Systems Manager → Run Command → Command history** for the same command ID.

Expected results are a successful command, a container named `taskflow`, a loopback binding `127.0.0.1:8055`, health returning 200, and anonymous `/tasks` returning 401. Complete the role checks yourself before declaring the release accepted.

If OIDC is blocked, the trainer can use approved SSO credentials to publish and deploy a gated reference image with the private instructions. Record the actual delivery route and image digest.

## 5. Reach the API through an SSM tunnel

Open a **new local PowerShell terminal** using the same AWS profile and Region. Keep it open while testing.

```powershell
$env:AWS_PROFILE = 'YOUR_APPROVED_PROFILE'
$env:AWS_REGION = 'YOUR_EXISTING_TARGET_REGION'
$InstanceId = 'YOUR_ORIGINAL_INSTANCE_ID'
aws ssm start-session --target $InstanceId --document-name AWS-StartPortForwardingSession --parameters 'portNumber=8055,localPortNumber=8055'
```

In another local terminal, at the repo root with its virtual environment active, run the following. Enter the fictional passphrases when prompted. The probe prints evidence while keeping tokens and passphrases out of its output.

```powershell
python -m exercises.day09_probe --url http://127.0.0.1:8055
```

If port 8055 is already occupied locally, stop your earlier local TaskFlow or choose local port 18055 in the tunnel and use `--url http://127.0.0.1:18055`. The remote port stays 8055.

| Operation | Expected evidence |
|---|---|
| Visitor reads or creates a task | 401 and no new row |
| Invalid token creates a task | 401 and no new row |
| Reader signs in and reads | 200 |
| Reader creates a task | 403 and no new row |
| Dispatcher signs in, reads and creates | 200, 200 and 201 with exactly one new row |

Optional browser view is `http://127.0.0.1:8055/docs`. The sign-in route is `POST /session`, and the booking collection is `/tasks`. Keep the tester terminal as the authoritative role and persistence evidence.

## 6. Prove persistence and inspect logs

Record the probe's `created_booking_id`. In the **remote Linux session** run the following.

```bash
sudo docker restart taskflow
sudo docker ps --filter name=taskflow
sudo docker logs --tail 40 taskflow
sudo docker inspect taskflow --format '{{.Config.Image}}'
sudo findmnt --target /srv/taskflow-data/app
```

Wait for application startup. In **local PowerShell** run the probe again with your actual recorded ID.

```powershell
python -m exercises.day09_probe --url http://127.0.0.1:8055 --expect-booking YOUR_RECORDED_INTEGER_ID
```

The second probe checks that booking and the denials without creating another booking. Logs should show startup and shutdown information. HTTP access logging is disabled for this training package. Friday adds operational signals and CloudWatch.

## Acceptance and handover

Record the instance ID, EBS ID, mount UUID, source commit, deployed digest, parameter name/version, successful role results, retained booking ID, first log observation and any unresolved issue. Record the one operator who owns state and Friday restart. Do not capture secret values, bearer tokens or raw state in screenshots or Git.

Stop the container cleanly and stop the original instance when your trainer closes the lab. EBS and ECR storage remain billable while retained. The secret file under `/run` disappears after a host stop/reboot. Friday must verify the EBS mount, retrieve the secret again and redeploy the known passing digest before resuming tests. The original data volume and Terraform state are retained.

## Progressive hints and stretch

Use the separate hints file one level at a time. A finished team can inspect the parameter ARN granted to its instance role, compare it with the GitHub role, and explain which identity can do each action. With the trainer, inspect a stopped previous container and describe how image rollback preserves the data volume. Keep CloudWatch and data recovery for Friday.
