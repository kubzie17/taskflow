# Day 8 — Workshop 2: Manage Terraform Variables and AWS Changes

**Time:** 85 minutes, split around the afternoon break.

## Scenario

Northbridge wants its Terraform configuration to support a controlled infrastructure milestone.

The current security-group tag is hardcoded:

`ReleaseStage = foundation`

Your task is to make that value configurable, validate the permitted values and demonstrate an in-place update to the existing AWS resource.

This is a classroom configuration exercise, not authorisation to deploy TaskFlow.

## Step 1 — Continue in the same Terraform directory

Use:

`infra/day08/`

Continue with your team's existing Terraform configuration and state.

Do not create a new working directory.

Do not change the approved AWS account, Region, subnet, AMI or team alias.

## Step 2 — Record the existing resource identities

From PowerShell:

```powershell
terraform output
terraform state list
```

Record the existing security-group ID.

If your team created the full infrastructure, also record the EC2 instance ID and separate bookings-volume ID.

Keep complete identifiers in the private evidence record.

## Step 3 — Find the hardcoded tag

Open:

`foundation.tf`

Find the security-group resource:

```hcl
resource "aws_security_group" "pilot" {
```

Locate:

`ReleaseStage`

Identify its current hardcoded value.

## Step 4 — Create a Terraform input variable

Open:

`variables.tf`

Add a variable called:

`release_stage`

Your variable must:

- Use the string type.
- Default to `foundation`.
- Accept only `foundation` and `deploy-ready`.
- Reject other values with a useful error message.

Look at the existing variable-validation examples in the file for guidance.

## Step 5 — Connect the variable to the security group

Return to:

`foundation.tf`

Replace the hardcoded `ReleaseStage` value with a reference to your new variable.

Do not change any inbound or outbound security-group rules.

## Step 6 — Add an output

Open:

`outputs.tf`

Create an output called:

`release_stage`

It must expose the `ReleaseStage` tag from the managed security-group resource.

## Step 7 — Check the default configuration

Run:

```powershell
terraform fmt
terraform validate
terraform plan
```

With the default value of `foundation`, the existing infrastructure should not require replacement or a new security group.

A new output may appear in the plan.

## Step 8 — Override the value

Open your private:

`team.auto.tfvars`

Add an override assigning the permitted value:

`deploy-ready`

Do not edit your account, subnet or AMI settings.

## Step 9 — Predict the changes

Before running Terraform, answer:

1. Which resource should change?
2. Which attribute should change?
3. What plan symbol do you expect?
4. Should the EC2 instance ID change?
5. Should the data-volume ID change?

## Step 10 — Save and inspect the plan

```powershell
terraform plan -out=w2.tfplan
terraform show -no-color w2.tfplan
```

Check the actual changes.

If Terraform proposes deleting or replacing the instance, security group or data disk, **stop and investigate**.

Do not apply an unexpected destructive change.

## Step 11 — Apply the approved plan

The nominated state custodian runs:

```powershell
terraform apply w2.tfplan
```

Wait for Terraform to finish.

## Step 12 — Verify in AWS

In AWS Console:

**EC2 → Security Groups → select your security group → Tags**

Refresh the page.

Find the `ReleaseStage` tag and inspect its value.

Compare the security-group ID before and after.

If the full infrastructure exists, also confirm the EC2 instance and data-volume IDs are unchanged.

## Step 13 — Verify the Terraform output

Run:

```powershell
terraform output release_stage
```

Then:

```powershell
terraform plan -detailed-exitcode
$LASTEXITCODE
```

Record the result.

## Success criteria

Your team can demonstrate:

- A validated Terraform input variable.
- A Terraform output.
- A reviewed plan.
- A real AWS tag update.
- Stable resource identities.
- A final plan with no unexpected changes.

Explain why a tag update is different from replacing a cloud resource.

**Remember:** `deploy-ready` is the permitted value for this classroom exercise. Actual TaskFlow deployment still requires its own security and release checks.
