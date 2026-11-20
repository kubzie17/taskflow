**Goal:** Deploy the reviewed protected TaskFlow Docker image to your original EC2 host, use persistent EBS storage, and verify application security and booking persistence.

## Part A — Confirm the AWS infrastructure

### Step 1 — Open the original Terraform working directory

Use Wednesday's actual `infra/day08` working directory and authoritative state.

In local PowerShell:

```powershell
terraform state list
terraform output
```

Identify the original EC2 instance ID and separate bookings EBS volume ID.

### Step 2 — Confirm AWS identity

Use your approved AWS profile and the Region that actually contains the instance.

```powershell
$env:AWS_PROFILE = "YOUR_APPROVED_PROFILE"
$env:AWS_REGION = "YOUR_APPROVED_REGION"

aws sso login --profile $env:AWS_PROFILE
```

Confirm the correct account privately.

### Step 3 — Inspect EC2

In AWS Console:

**EC2 → Instances → select your original team instance**

Inspect:

- Instance state.
- Security group.
- IAM instance profile.
- Storage attachments.

If the instance was stopped, start that same instance.

Do not create a replacement.

### Step 4 — Connect through Systems Manager

When the instance is Running and SSM Online:

**EC2 → Instances → select instance → Connect → Session Manager → Connect**

This opens a remote Linux shell.

## Part B — Prepare persistent EBS storage

### Step 5 — Inspect the disks

Inside the remote Linux session:

```bash
sudo lsblk -o NAME,SERIAL,SIZE,FSTYPE,UUID,MOUNTPOINTS
findmnt /
sudo cat /etc/fstab
```

Identify the root disk and the separate bookings volume.

Compare the EBS volume ID from AWS with the Linux NVMe device serial.

**Do not format anything yet.**

### Step 6 — Prepare the bookings volume with the trainer

The trainer will inspect the original bookings disk and demonstrate the safe mounting helper.

An existing valid filesystem must be preserved.

A newly created empty course disk may be initialised only after its identity and contents have been verified.

The intended host directory is:

`/srv/taskflow-data/app`

Verify that it is backed by the original bookings EBS volume.

## Part C — Runtime configuration

### Step 7 — Inspect the application configuration

Open:

`docs/day09-runtime.example.json`

Create your own private copy outside the repository.

Use the trainer-approved configuration for your:

- AWS Region.
- AWS account.
- ECR repository.
- Original EBS volume.
- Runtime parameter name.

### Step 8 — Inspect Parameter Store

In AWS Console:

**Systems Manager → Parameter Store**

Find your team's approved parameter:

`/taskflow/TEAM/runtime-identity`

Record the parameter name and version number.

Do not display its value in Teams or GitHub.

Discuss how the EC2 instance role retrieves it and how Docker receives a read-only mounted file.

## Part D — Deploy through GitHub Actions

### Step 9 — Run the approved deployment workflow

In GitHub:

**Actions → TaskFlow Day 9 → Run workflow**

Choose:

- Branch: `main`
- Environment: your assigned team environment
- Deploy: **true**

The workflow must pass the required checks and publish its image before deployment proceeds.

Record the digest from this run.

### Step 10 — Inspect the AWS deployment

In AWS Console:

**Systems Manager → Run Command → Command history**

Find the corresponding command and check its status.

The expected deployment is a container called:

`taskflow`

It should be bound to the EC2 host's loopback port:

`127.0.0.1:8055`

## Part E — Test the application

### Step 11 — Open an SSM port-forwarding session

In a new local PowerShell terminal:

```powershell
$env:AWS_PROFILE = "YOUR_APPROVED_PROFILE"
$env:AWS_REGION = "YOUR_APPROVED_REGION"
$InstanceId = "YOUR_ORIGINAL_INSTANCE_ID"

aws ssm start-session --target $InstanceId --document-name AWS-StartPortForwardingSession --parameters 'portNumber=8055,localPortNumber=8055'
```

Keep the session running.

### Step 12 — Run the protected API probe

In another local PowerShell terminal, from your TaskFlow repository with the virtual environment active:

```powershell
python -m exercises.day09_probe --url http://127.0.0.1:8055
```

Enter your fictional reader and dispatcher passphrases privately.

Expected:

| Action | Result |
|---|---|
| GET /health | 200 |
| Visitor GET /tasks | 401 |
| Visitor POST /tasks | 401 |
| Invalid token POST /tasks | 401 |
| Reader GET /tasks | 200 |
| Reader POST /tasks | 403 |
| Dispatcher GET /tasks | 200 |
| Dispatcher POST /tasks | 201 |

Rejected requests must not add database records.

Record the booking ID created by the dispatcher.

## Part F — Test persistence

### Step 13 — Restart the container

Inside the remote Linux session:

```bash
sudo docker restart taskflow
```

Wait for the application to start.

### Step 14 — Verify the original booking still exists

Back in local PowerShell:

```powershell
python -m exercises.day09_probe --url http://127.0.0.1:8055 --expect-booking YOUR_RECORDED_INTEGER_ID
```

Replace the placeholder with the booking ID from Step 12.

The restart check must find the same booking without creating another one.

### Step 15 — Record evidence

Record:

- Source commit and workflow run.
- ECR image digest.
- Original EC2 instance ID.
- Original EBS volume ID.
- EBS mount UUID.
- Runtime parameter name and version.
- Visitor, reader and dispatcher results.
- Booking ID retained after restart.
- One useful log observation.
- Any outstanding issue and next action.

**Success:** A checked protected TaskFlow image runs on the existing EC2 host, enforces both roles and retains bookings on the correct EBS volume after a container restart.

Do not reveal signing keys, password records, bearer tokens or raw Terraform state.