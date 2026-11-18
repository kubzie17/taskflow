# Day 8 | Build the TaskFlow AWS pilot with Terraform
**Wednesday 18 November · Teams · 09:30–15:30 UK.** Today your team creates one real AWS foundation and proves how a reviewed change affects it. Thursday’s deployment will use this same host, disk and state. Tuesday reached the network repair; the planned gateway failure and booking recovery are still ahead.

Work in Teams rooms of two, two and three. Nominate one state custodian with an approved encrypted machine. Only that machine applies changes for the team. Rotate who explains the plan, authors an edit or checks AWS; partners can edit an unconfigured checkout or share control of the custodian’s screen. Post only redacted observations. Keep actual IDs and state in the owner's private ledger. Save a copy of [the digital evidence record](day08-evidence.md) outside the repo.

## Before joining the first workshop
1. Merge the Day 8 materials into the existing checkout using the root README. Save earlier work on its own branch. In VS Code open the root containing app/, exercises/ and infra/. All commands in this guide use Windows PowerShell. Terraform does not need a Python virtual environment.
2. Verify `terraform version` and `aws --version` in a fresh terminal. Use Terraform CLI 1.9 or later in the 1.x line and AWS CLI v2. If Terraform is missing, visit the [official install page](https://developer.hashicorp.com/terraform/install), select Windows and your architecture, download the binary ZIP, verify the SHA-256 against the signed release checksums, extract terraform.exe to an approved user tools directory, add that directory to your user Path and reopen VS Code. Use your organisation’s approved AWS CLI v2 installer. The optional Session Manager plugin is needed only for a local CLI session/port forward; the Console shell works without it.
3. Your trainer provides the approved Region (normally eu-west-1), expected account, training subnet, pinned regional AL2023 image and unique team alias. Confirm your assigned Identity Center profile once. Reuse last session’s profile. If new, use `aws configure sso --profile taskflow-training`, enter the owner's SSO start URL and **SSO Region**, select the assigned account/role and use the assigned workload Region. The SSO Region and workload Region can differ.
```powershell
$env:AWS_PROFILE = Read-Host 'Approved training CLI profile'
$env:AWS_REGION = Read-Host 'Approved workload Region, normally eu-west-1'
aws sso login --profile $env:AWS_PROFILE
aws sts get-caller-identity --query Account --output text
```
4. Privately compare the returned account with the instructor's expected account. Only the custodian enters `infra/day08` and makes the private values file. If it already exists, open it and preserve its values.
```powershell
Set-Location .\infra\day08
if (!(Test-Path .\team.auto.tfvars)) { Copy-Item .\team.auto.tfvars.example .\team.auto.tfvars }
code .\team.auto.tfvars
git check-ignore team.auto.tfvars terraform.tfstate w1.tfplan
```
Replace the four placeholders with the actual values. Check the Region. Keep this team alias, subnet and AMI fixed through Friday. The private values file may include identifiers. Never put passwords, access keys or a JWT key in it. Git should report all three filenames as ignored. If blocked for five minutes, tell the trainer the first failing operation and use the fallback below while they investigate.

## Core 1 | Give dispatch a place to deploy | 85 minutes
**Scenario.** Dispatch needs a controlled host and a disk that can survive a host replacement. The next team must reach it through Systems Manager. **Outcome.** Provision and verify an encrypted, single-AZ EC2 foundation. **Start:** `infra/day08/foundation.tf`, `identity.tf`, `outputs.tf`, `versions.tf` and your private inputs. You need the approved subnet, active AWS session and Terraform provider download or prepared mirror.
1. In `versions.tf` identify the provider version and expected-account guard. In `foundation.tf` label one `data` block that reads an existing object and one `resource` block Terraform will own. Draw or type the path from the instance to the Systems Manager endpoints. Explain why there can be no inbound SSH rule.
2. Implement the missing outbound management port in `locals`. The host needs encrypted HTTPS to reach the public AWS management endpoints. Inspect both ends of the egress rule and its precondition. Leave the inbound rule list empty. This simple lab allows outbound TLS to any IPv4 destination; record the trade-off.
3. In `outputs.tf` author an output named `data_volume_id` for the separate bookings EBS disk. The disk resource uses `count`, so consider the full-host case and the no-host case. Use the existing instance output as a pattern. Identify why the root disk is the wrong answer. Show your change to the reviewer.
4. From the AWS root, run these separately. Stop at the first unexpected error. `init` downloads the pinned provider and creates `.terraform.lock.hcl`. `fmt` may make whitespace changes.
```powershell
terraform fmt
terraform init
terraform validate
terraform plan -out=w1.tfplan
terraform show -no-color w1.tfplan
```
5. Review the **actual** planned additions. Find EC2 t3.micro, auto public IPv4, encrypted 8 GiB root, encrypted 4 GiB bookings disk in the same AZ, its attachment, group with zero ingress and one TCP egress rule, and the EC2 instance profile. The standard course-created role path has eight managed additions; a trainer-supplied profile has five. Data lookups and outputs are not additional managed resources. On a resumed state fewer additions may be correct. Stop for wrong account, a replacement, a second host, unexpected deletion, public inbound or unapproved cost.
6. The reviewer states what will be created and the custodian applies the reviewed saved plan **once**: `terraform apply w1.tfplan`. Wait for exit. Reuse the same state if the run fails partway. Never restart from a new folder to fix an error.
7. Verify independently. Read `terraform output` and `terraform state list` privately. AWS Console in the approved Region → **EC2 → Instances → select your tagged instance**. Check ID, state, IAM role and subnet. **Security → Security groups → Inbound rules / Outbound rules**: inspect sources, destinations and protocol. **EC2 → Volumes → select the returned bookings volume**: confirm encrypted, 4 GiB, same AZ and attached to this instance. The Console device mapping may say /dev/sdf; Linux may use a different device name.
8. **Systems Manager → Fleet Manager → Managed nodes**, or **EC2 → Instances → Connect → Session Manager**. Record Online or the actual blocker. If available, click **Connect** and run `hostname` and `lsblk` in the remote Linux shell. Close the session with `exit`. Leave both disks intact. Run `terraform plan -detailed-exitcode` in local PowerShell and immediately inspect `$LASTEXITCODE`: 0 means no changes, 1 error, 2 changes to review.
**Acceptance:** actual resource(s) observed in AWS, scope, identity and one storage observation recorded, safe no-change plan or a specific remaining drift/error. State owner named. Share a redacted result, never a plan binary or full account screen. **Stretch:** explain which portion of the path the public IP enables despite zero inbound rules.

## Core 2 | Promote the same infrastructure | 85 minutes
**Scenario.** Support wants a visible release milestone before Thursday. Rebuilding the host would risk the handover. **Outcome.** Refactor a literal into a validated Terraform input, make one controlled in-place change and verify both IDs. **Start:** same AWS root, same state, `variables.tf`, `foundation.tf`, `outputs.tf` and `team.auto.tfvars`. Your SG from Core 1 is enough for the reduced route.
1. Record the current SG ID and `ReleaseStage` tag, plus host/data IDs when present. Do not change team, subnet, AMI, storage or inbound rules. Predict the symbol you expect for a tag edit and how a replacement would appear.
2. In `variables.tf` declare input `release_stage`, type string, default `"foundation"`. Write a validation that admits exactly `"foundation"` and `"deploy-ready"`, with a helpful error. In `foundation.tf` replace the hardcoded SG tag value with a reference to your variable. In `outputs.tf` add a `release_stage` output reading the tag from the group. Run `terraform fmt`, `terraform validate` and `terraform plan`. With the original default your infrastructure should require no change. The new output alone can appear in the plan.
3. Add `release_stage = "deploy-ready"` to the private `team.auto.tfvars`. An automatically loaded variable file overrides the default; an explicit `-var-file` passed last can override it again. A local value derives a name from other values. An output is a result you expose to another operator. Marking a variable/output sensitive can hide display, while values may still be present in state and saved plans.
4. Run `terraform plan -out=w2.tfplan` and `terraform show -no-color w2.tfplan`. Identify address, old/new values and whether the ID will change. In the clean reference, the only managed change is the existing security group’s tag. Pay attention to `+`, `~`, `-` and `-/+`. If it plans a host replacement or destroy, save the reason privately and repair the input before any apply.
5. Apply `terraform apply w2.tfplan`. Refresh **EC2 → Security Groups → your group → Tags**. Compare actual tag and old/new SG, instance and data-volume IDs. Read `terraform output release_stage`. Run a fresh detailed-exitcode plan. Explain the different roles of source, variable file, provider lock file and state.
6. Partner challenge: would changing the pinned launch AMI resemble a tag edit? Make a written prediction. A stretch learner may ask the trainer for another approved same-Region AMI and inspect a **plan only**; revert the input and confirm a clean plan. Never apply the replacement.
**Acceptance:** validated input, controlled plan, new AWS tag, stable IDs, fresh plan result, named state owner and one example of replacement risk. **Stretch:** make an owner-approved reversible tag-only out-of-band edit in the Console, run a normal plan, explain drift and reconcile by applying the reviewed plan. Use the same tag, never an inbound rule.

## Short challenge | Repair a failed promotion | 25 minutes
**Scenario.** A colleague’s environment override fails during a release rehearsal. The last known good AWS configuration must remain in service. **Start:** completed Core 2, same root, `exercises/day08-fault.case`; copy the exhibit to an ignored filename. **Tools:** Terraform, PowerShell and editor.
1. From `infra/day08` run `Copy-Item ..\..\exercises\day08-fault.case .\fault.tfvars` on first use. Inspect the proposed override and predict the failure boundary.
2. Run `terraform plan -var-file=fault.tfvars`. Capture the first useful diagnostic in your own words. Determine whether this is syntax, variable validation, AWS authentication or infrastructure drift.
3. Repair **only your local copy** to represent the intended Thursday stage. Repeat the same plan. Compare `terraform output release_stage` with the real AWS tag. Leave the cloud as it is.
4. In Teams give a partner the symptom, smallest fix and verification. Keep your private evidence before removing the disposable `fault.tfvars`.
**Acceptance:** reproduce the failure, explain the variable’s origin, make a passing plan and verify unchanged cloud state. **Stretch:** explain why `terraform validate` alone cannot prove a specific variable file is acceptable.

## Progressive hints
Open only after a first attempt; the trainer holds the completed files.
- **Core 1.** First, follow the egress rule back to the local it reads. Next, compare the output naming pattern with the counted resource for the secondary disk. Finally, separate a missing provider, a precondition diagnostic and an actual AWS denial.
- **Core 2.** First, trace where ReleaseStage is set. Next, read the existing validation blocks and look up Terraform's `contains` function. Finally, ask which single AWS object's Tags page should change.
- **Short challenge.** First, read the variable name in the diagnostic. Next, compare effective inputs with the intended stage. Finally, distinguish the last explicitly supplied file from the auto-loaded default.

## If a real blocker appears
- If IAM creation is denied, ask for the trainer's existing approved instance **profile** name. Inspect partial state and re-plan before changing the mode.
- If compute is blocked, a real **network-only** route can still create the SG and outbound rule. Start that route with `enable_host = false` only on a fresh or verified network-only team state. Changing it on a live host stack proposes removing the host and disk. Keep the same tag/variable challenge and schedule the host for Thursday.
- If AWS or provider access is blocked, use the [separate local exercise](day08-fallback.md). Label evidence AWS, Terraform local or Python simulation. Record one next action to resume the actual AWS configuration without resetting it.

## Handover before 15:30
Record private IDs and observed stage, AWS Region, state custodian, encrypted backup location, next operator and Friday cleanup owner in [the evidence record](day08-evidence.md). If retention is approved, stop the EC2 instance as directed, wait for Stopped and keep state, role, security group and both disks. If retention has no owner, follow the trainer through a reviewed `terraform plan -destroy -out=close.tfplan` and `terraform apply close.tfplan`. Keep data/state until ownership and verification are settled. Thursday starts from that recorded position.
