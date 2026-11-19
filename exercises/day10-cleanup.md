# Final practical — Verify AWS cleanup

**14:30–15:25, 55 minutes.** This is compulsory. Your team must account for every course resource it owns. Deletion requires the trainer's confirmation and the resource owner's authority. Shared academy, production and other teams' resources are outside your deletion scope.

## 1. Preserve evidence and review ownership

Save your release/recovery evidence privately. Confirm the fictional database and checkpoint may be disposed of. Fill the resource ledger with exact IDs, account/Region, owner, Terraform/manual ownership, approved action, verification, remaining issue and deadline. Record root and bookings volumes separately. The trainer reconciles shared resources across teams.

**LOCAL WINDOWS POWERSHELL**, in the original completed Terraform directory:

```powershell
$env:AWS_PROFILE = 'YOUR_APPROVED_PROFILE'
$env:AWS_REGION = 'YOUR_EXISTING_REGION'
aws sts get-caller-identity
terraform workspace show
terraform state list
terraform output
```

Do not create a new state, reset the working folder or use the public Terraform starter in place of your completed files. Stop and ask the state custodian if the state is missing or unfamiliar.

## 2. Stop the writers and block further course deployments

After saving final evidence, the trainer checks the named course containers and stops the original/recovery writers. Close the SSM tunnels. Confirm no GitHub deployment is in progress. Remove only the selected team's disposable environment configuration when instructed. Keep source and CI evidence.

The trainer removes the exact Day 9/10 inline policies added manually to the node role before Terraform deletes that role. The original Terraform-managed agent policy is left to Terraform. Externally supplied roles remain with their owner.

## 3. Review the destroy plan before applying it

Save the plan outside Git. The trainer first preserves a private state backup using the detailed runbook.

```powershell
$PrivateWork = Join-Path $HOME '.taskflow-day10-private'
New-Item -ItemType Directory -Force $PrivateWork | Out-Null
$DestroyPlan = Join-Path $PrivateWork ('reviewed-destroy-' + (Get-Date -Format 'yyyyMMddHHmmss') + '.tfplan')
terraform plan -destroy "-out=$DestroyPlan"
if ($LASTEXITCODE -ne 0) { throw 'Plan failed. Stop and inspect.' }
terraform show -no-color $DestroyPlan
```

Compare **every deletion** with the approved ledger. Check the actual instance, storage, security group and owned IAM resources. A data-source subnet is not owned by this state. Stop for unexpected resources or proposed creates/replacements.

Only after the trainer and owner approve this specific plan:

```powershell
$Approval = Read-Host 'Type DELETE REVIEWED TEAM RESOURCES to apply the reviewed plan'
if ($Approval -cne 'DELETE REVIEWED TEAM RESOURCES') { throw 'Not confirmed' }
terraform apply $DestroyPlan
if ($LASTEXITCODE -ne 0) { throw 'Cleanup incomplete. Record the error.' }
terraform state list
```

A saved plan applies without Terraform asking again. Never use an unreviewed `-auto-approve` shortcut. If the plan becomes stale, create and review a new one.

## 4. Reconcile manual resources with the trainer

Terraform only knows resources in its state. Using the trainer's exact-name procedures, account for the ECR repository/images, fictional Parameter Store identity, fixed SSM document, GitHub OIDC role and course policies, CloudWatch log group and any actually created alarms. Do not delete the shared GitHub identity provider. Shared VPC/network cleanup is performed last by its named owner after all team dependencies are removed.

## 5. Independently verify

Refresh the relevant AWS Console pages and check exact IDs. `terminated` can still be shown in EC2. EBS volumes need separate checks. A missing item in the wrong account or Region is not evidence. Access denied and timeouts are unresolved, not deleted.

Copy `docs/day10-cleanup-inventory.example.json` outside Git, fill real values and ask the trainer to review the complete list. From the repo root run:

```powershell
python -m exercises.day10_verify_cleanup 'C:\YOUR_PRIVATE_FOLDER\cleanup-inventory.json'
```

This read-only helper makes no deletion. Exit 0 means all listed resources are observed removed. Exit 2 means one or more remains or is unknown. It does not discover every account resource. Retained shared resources still appear as remaining and need an owner/decision in the ledger.

## 6. Submit the final ledger

At 15:20 report each failure with resource ID, owner, exact error, potential ongoing charge, next action and deadline. Stopping EC2 does not remove storage or all address/log/registry charges. Remove course-only local containers, volumes and fictional identity files when authorised; do not prune unrelated Docker work.

**Acceptance:** every course resource has an observed deletion or explicit retained/unresolved ownership. Preserve cleanup time even when a previous challenge remains incomplete. Stretch is a careful reconciliation of an additional real ledger item, not account-wide discovery or deletion.
