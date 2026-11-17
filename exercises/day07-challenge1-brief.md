:::writing{variant="document" id="78101"}
# Challenge 1 — AWS Access and Readiness Investigation

**Time:** 20 minutes  
**Working arrangement:** Three teams  
**Objective:** Establish which AWS services and capabilities are available for Days 7–10.

## Scenario

Northbridge wants to explore running TaskFlow in AWS.

Before using real cloud services, we need to understand the training sandbox's available permissions, restrictions, costs and session lifetime.

Your job is to investigate the environment using safe, read-only actions.

## Step 1 — Sign in

Open the AWS sandbox link or training portal provided by the trainer.

Launch your approved AWS session and open **AWS Management Console**.

Record:

- Whether sign-in succeeds.
- Your identity type, such as a temporary training role.
- The approved AWS Region.
- Your session expiry time, if shown.
- Whether the sandbox resets after use.
- Whether the cost and budget owner is known.

Do not share AWS account numbers, complete ARNs, credentials or session URLs.

If you cannot sign in, record the issue and continue using the fictional AWS inventory provided in the learner pack.

## Step 2 — Confirm the Region

Use the AWS Region selector near the top right of the Console.

Do not change to another Region without approval.

If your approved Region is London, it appears as:

`Europe (London) — eu-west-2`

Your sandbox may use a different Region.

## Step 3 — Investigate your assigned services

### Team A — IAM and Networking

Use the Console search bar to locate:

- IAM → Roles
- VPC → Your VPCs
- VPC → Subnets
- VPC → Route tables
- VPC → Security groups

Investigate whether you can view the assigned training resources and their existing configurations.

Do not edit roles, policies, routes or security groups.

### Team B — EC2, S3 and Terraform Readiness

Locate:

- EC2 → Instances
- EC2 → Volumes
- S3 → General purpose buckets
- ECS → Clusters, if approved

Record which existing resources you can inspect.

In your local PowerShell terminal, check whether these tools are installed:

```powershell
aws --version
terraform version
```

These commands only check your local tools.

If Terraform is unavailable, record that. Do not install it unless the trainer approves the installation method.

### Team C — CloudWatch and Monitoring

Locate:

- CloudWatch → Logs → Log groups
- CloudWatch → Metrics
- CloudWatch → Alarms

Investigate whether you can view approved existing monitoring information.

Record whether you can list resources, whether the list is empty or whether the operation is denied.

Do not create alarms, dashboards, log groups or metrics.

## Step 4 — Optional AWS CLI identity check

Only if you already have approved temporary CLI access, use your assigned profile and Region:

```powershell
aws sts get-caller-identity --profile COURSE_PROFILE --region APPROVED_REGION --query "length(Account)" --output text --no-cli-pager
```

Replace the profile and Region placeholders with your actual approved settings.

A result of `12` means AWS returned a 12-digit account identifier without displaying it.

A successful identity check does not establish permission to create other resources.

If CLI access isn't configured, record it as **Not tested**.

## Step 5 — Complete the readiness checklist

Use the checklist below and the **1 Access** tab in:

`exercises/Day_7_Workshop_Workbook.xlsx`

For each capability, record:

- **Available** — the exact approved operation succeeded.
- **Denied** — AWS explicitly refused that operation.
- **Not tested** — no relevant operation was attempted.
- **Session issue** — sign-in or credentials prevented the test.

Include the precise action and your evidence.

For actions involving creation, modification or deletion, do not test them without explicit approval from the sandbox owner. Mark them **Not tested** unless trustworthy prior evidence and authorisation have been provided.

## Step 6 — Decide which route is possible

**Route A:** Approved AWS object write/read/delete activity with a confirmed cost and cleanup owner.

**Route B:** Read-only investigation of existing AWS infrastructure.

**Route C:** Local TaskFlow exercises and the supplied fictional AWS inventory.

Different teams may use different routes.

## Step 7 — Report back

Each team must provide:

1. One successful or denied action.
2. One capability that remains untested.
3. One restriction or cost consideration.
4. Its selected route.
5. One recommendation for Days 8–10.

**Success:** Your team can explain which AWS capabilities have actually been verified and which must be confirmed before using Terraform or deploying TaskFlow.

Do not create, modify or delete cloud resources during this exercise.

:::