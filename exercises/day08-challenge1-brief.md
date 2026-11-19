# Day 8 — Workshop 1: Provision the TaskFlow AWS Foundation

**Time:** 85 minutes, split around the morning break  
**Tools:** VS Code, PowerShell, Terraform, AWS CLI, AWS Console  
**Application:** Existing TaskFlow repository

## Scenario

Northbridge Repairs needs infrastructure to host the protected TaskFlow application.

Your team must complete the supplied Terraform configuration, create the approved AWS resources and prove that they exist.

The goal is to prepare infrastructure for Thursday's application deployment.

## Step 1 — Open the Terraform starter

From the TaskFlow repository root, open:

`infra/day08/`

Inspect these files:

- `versions.tf`
- `variables.tf`
- `foundation.tf`
- `identity.tf`
- `outputs.tf`
- `team.auto.tfvars.example`

Do not edit the IAM policy or resource ownership settings unless instructed.

## Step 2 — Prepare the approved AWS configuration

Check:

```powershell
terraform version
aws --version
```

Sign in using your approved AWS CLI profile:

```powershell
$env:AWS_PROFILE = Read-Host "Approved AWS CLI profile"
$env:AWS_REGION = Read-Host "Approved workload Region"

aws sso login --profile $env:AWS_PROFILE
```

Check the signed-in account privately:

```powershell
aws sts get-caller-identity --query Account --output text
```

Compare it with the expected account supplied by the trainer.

## Step 3 — Prepare your team's input file

From the repository root:

```powershell
Set-Location .\infra\day08
```

Create the private configuration file if it doesn't already exist:

```powershell
if (!(Test-Path .\team.auto.tfvars)) {
    Copy-Item .\team.auto.tfvars.example .\team.auto.tfvars
}
```

Open it:

```powershell
code .\team.auto.tfvars
```

Enter the actual approved account ID, Region, team alias, subnet ID and regional AMI ID supplied by the trainer.

Do not invent resource identifiers.

Do not include passwords, tokens, private keys or signing secrets.

Check that Terraform state and private variable files will be ignored by Git:

```powershell
git check-ignore team.auto.tfvars terraform.tfstate w1.tfplan
```

## Step 4 — Investigate the configuration

Open:

`foundation.tf`

Locate:

```hcl
locals {
  ...
}
```

Then find:

`aws_vpc_security_group_egress_rule.management`

Investigate how `local.management_port` is used.

The Systems Manager agent must initiate an encrypted HTTPS connection to the approved AWS service endpoint.

Complete the missing configuration so that the outbound management rule works as intended.

Do not open inbound SSH access.

## Step 5 — Add the missing data-volume output

Open:

`outputs.tf`

Find the existing instance output.

Your task is to add:

`data_volume_id`

The output should identify the separately managed bookings EBS volume, not the root disk.

Consider how the output should behave if the optional no-host route is used.

## Step 6 — Prepare Terraform

Run:

```powershell
terraform fmt
terraform init
terraform validate
```

Address any errors before proceeding.

## Step 7 — Create a saved plan

```powershell
terraform plan -out=w1.tfplan
```

Then:

```powershell
terraform show -no-color w1.tfplan
```

As a team, review the plan and establish:

1. What resources will be created?
2. Which existing AWS resources are being read?
3. Whether the EC2 instance is `t3.micro`.
4. Whether the root and data volumes are encrypted.
5. Whether the security group has unnecessary inbound access.
6. Whether any resource is being destroyed or replaced.
7. Whether the planned infrastructure matches the approved account and Region.

**Do not apply the plan until your team has reviewed it.**

## Step 8 — Apply the reviewed plan

The nominated state custodian runs:

```powershell
terraform apply w1.tfplan
```

Do not run another apply simultaneously from another machine.

If Terraform fails, record the first error and ask for help before trying a different working directory.

## Step 9 — Verify in AWS

In the AWS Console, inspect:

**EC2 → Instances**

Find your team's instance.

Record its state, instance type and assigned subnet.

**EC2 → Security Groups**

Open the security group associated with the instance.

Inspect inbound and outbound permissions.

**EC2 → Volumes**

Find the separate data volume.

Verify its size, encryption, Availability Zone and attachment.

**Systems Manager → Fleet Manager → Managed nodes**

Look for the instance and its reported connection status.

If Session Manager is available, connect and inspect the machine using:

```bash
hostname
lsblk
```

Do not format, mount or delete any disk.

## Step 10 — Check Terraform state

Return to your local PowerShell:

```powershell
terraform state list
terraform output
```

Then:

```powershell
terraform plan -detailed-exitcode
$LASTEXITCODE
```

A result of:

- `0` means no changes are proposed.
- `1` means an error occurred.
- `2` means changes are proposed and need investigation.

## Success criteria

You can show real evidence of the AWS resource you created.

Your team can identify the EC2 instance, security group and data volume, explain how Systems Manager management works and demonstrate its current Terraform state.

Record your findings privately in the Day 8 evidence record.

Do not post complete resource IDs, state files, saved plans or AWS account details in the public Teams chat.
