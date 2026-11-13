# Friday 14:55 · Which AWS labs can our sandbox support?

Make a personal copy in VS Code outside the repo. Work for 25 minutes. Each person checks their own access and one assigned service family. In the last five minutes trade sanitised observations so the trainer can build a class picture. If you cannot sign in, record where access stopped. You can review a partner's observations while you finish your local tests. Leave uncertain rows marked **Not tested**.

## How to collect an observation

1. Open your provider's sandbox launch page. Read the instructions before starting the session. Note the environment type, allowed region, countdown, credit/budget, persistence policy and any published restrictions. Use the assigned lab identity. Write “unknown” for anything the page does not document.
2. Open the Console. Copy the **region name only**. Use the provided temporary CLI profile or approved CloudShell if available. `aws --version` proves the tool is installed. `aws sts get-caller-identity --query 'length(Account)' --output text` returning **12** verifies an AWS session without printing your account number. In Windows PowerShell or a shell this command uses single quotes as shown. A Console login alone does not establish CLI access.
3. Work through your lane below. Choose one of **Available / Denied / Not tested** for each action. “Available” means the named action actually succeeded in your authorised environment. A successful list returning zero items still proves list permission. A visible Create button does not prove permission. A simulator result is evidence about a policy prediction only. Keep the actual write row “Not tested” until an authorised exercise has run it.
4. Record the region (use “global” for IAM inventory), the method and just the relevant error name such as `AccessDeniedException`, `ExpiredToken` or `UnauthorizedOperation`. Expired sessions or network failures leave the permission **Not tested**. Set “usable” to **yes / limited / unknown** and choose a fallback.
5. Share a short summary in Teams. Keep account numbers, ARNs, role/session names, resource IDs, URLs containing pool/account identifiers, tokens, keys, passwords and billing screenshots off the shared record.

### Safe probes for the 25-minute session

- **IAM.** Console → IAM → Users, Roles, Policies. Open a lab role you may inspect and check attached policies. Where enabled, open the IAM Policy Simulator, select an approved lab principal and resource, and compare a read action against a write action such as `s3:ListBucket` and `s3:PutObject`. Record simulated decisions separately. Ask for documented management boundaries about create-user, create-role and `iam:PassRole`. Never create users, keys or roles just to see whether the controls work.
- **Cognito.** In the assigned region open Cognito → User pools. With the owner's permission inspect a designated training pool's app clients, groups, users and login configuration. If only listing works, that is the extent of the observation. Where a trainer supplies an approved pool issuer, open its discovery document and published JWKS URI. Record HTTPS/status and whether public keys were present. These public URLs can work even for someone who cannot administer the pool. The create/delete/login rows belong to an approved follow-on lab or remain untested.
- **Deployment and IaC.** EC2 → Instances. VPC → Your VPCs and Security groups. S3 → Buckets. Inspect a named training example of the agreed hosting option (for example Elastic Beanstalk environments) if available. Record view, launch, network change and cleanup separately. For an authorised CLI check, `aws ec2 describe-instances --dry-run --region REGION` submits a non-mutating probe: `DryRunOperation` means the *describe* action is permitted, `UnauthorizedOperation` means denied. Replace REGION with the assigned region. Neither result proves RunInstances. For Terraform use the identity-only probe below if Terraform and the provider are already available. Never use an apply merely to test permission.
- **Monitoring.** Open CloudWatch → Logs → Log groups, Metrics → All metrics, and Alarms → All alarms. Observe names/counts privately, share only whether access worked. Viewing existing data, publishing custom metrics, starting Logs Insights queries and creating alarms are different operations. Skip paid queries, ingestion and changes during discovery.
- **Time check.** Give the trainer one success, one limit and one follow-up owner. If all you established was Console access, that is a valid result.

## Discovery record

Session type __________  Assigned region __________  Session limit __________  Persistence source __________  Budget/credit or “not visible” __________  Restrictions owner __________

| Service | Required action | Available / Denied / Not tested | Region | Method, error or restriction | Usable for course? | Realistic fallback |
| --- | --- | --- | --- | --- | --- | --- |
| Sandbox | Launch Console and identify sandbox/region | Not tested | | | | Local TaskFlow |
| Sandbox | Read budget, session expiry and persistence rules | Not tested | | | | Ask lab administrator |
| CLI / STS | Use approved temporary credentials and confirm session | Not tested | | | | Console / local CLI rehearsal |
| IAM | List users | Not tested | global | | | Review fictional policy |
| IAM | List roles and inspect one role's attached policies | Not tested | global | | | Sanitised role example |
| IAM | List policies / view permitted policy document | Not tested | global | | | Local policy reading |
| IAM | Simulate allow/deny for a named action | Not tested | global | | | Evaluate a sample policy |
| IAM | Create/manage a user | Not tested | global | | | No user creation needed |
| IAM | Create/manage a role | Not tested | global | | | Use approved existing lab role |
| IAM | Pass a specific role to an approved service | Not tested | | | | Design only / preassigned role |
| Cognito | List or inspect a user pool | Not tested | | | | Local issuer |
| Cognito | Create a pool | Not tested | | | | Trainer pool / local issuer |
| Cognito | Create/configure a public app client | Not tested | | | | Inspect approved example |
| Cognito | Create fictional users | Not tested | | | | Local lab identities |
| Cognito | Create groups / assign membership (record each) | Not tested | | | | Local roles |
| Cognito | Configure domain and code flow with PKCE | Not tested | | | | Trace the local flow diagram |
| Cognito | Obtain and use an access token through approved flow | Not tested | | | | Local JWT / trainer demo |
| Cognito | Read discovery metadata and public JWKS | Not tested | | | | Offline RSA test |
| Cognito | Remove only owned training resources | Not tested | | | | Shared pool owner cleans up |
| EC2 | Describe instances | Not tested | | | | Day 7 deployment diagram |
| EC2 | Launch / terminate an instance (separate outcomes) | Not tested | | | | Local container |
| S3 | List buckets | Not tested | | | | Local file example |
| S3 | Create/delete approved disposable objects or bucket | Not tested | | | | Local directory |
| VPC / security groups | Describe networks and groups | Not tested | | | | Annotated network diagram |
| VPC / security groups | Change a group or network under lab policy | Not tested | | | | Review proposed rules offline |
| Hosting | Inspect agreed application-hosting option | Not tested | | | | Local container design |
| Hosting | Provision / remove hosted application | Not tested | | | | Run TaskFlow locally |
| Terraform | Load AWS provider and resolve identity via a read-only plan | Not tested | | | | Built-in terraform_data locally |
| Terraform | Create an approved resource | Not tested | | | | Local apply |
| Terraform | Delete that approved resource | Not tested | | | | Local destroy |
| CloudWatch | Describe log groups | Not tested | | | | Local Uvicorn logs |
| CloudWatch | List metrics | Not tested | | | | Local request counts |
| CloudWatch | Describe alarms | Not tested | | | | Offline alert rule |
| CloudWatch | Create/delete a log group | Not tested | | | | Local structured log |
| CloudWatch | Create/delete an alarm | Not tested | | | | Local simulated alarm |

Duplicate a row for actions with different outcomes, roles or regions. Write “not attempted” where the timebox ended.

**Optional identity-only Terraform check.** In an empty temporary folder outside the course repo, on a machine with approved temporary credentials and provider download access, create `main.tf` containing the following read-only configuration. Substitute the assigned region. Run `terraform init` then `terraform plan` there. `session_available = true` shows provider connectivity to STS. Initialisation alone only proves the plugin loaded. Share the boolean, never the underlying identity or state. Close the lab session and remove this scratch folder when finished.

```hcl
terraform {
  required_providers {
    aws = { source = "hashicorp/aws" }
  }
}
provider "aws" {
  region = "eu-west-2"
}
data "aws_caller_identity" "lab" {}
output "session_available" {
  value = length(data.aws_caller_identity.lab.account_id) == 12
}
```

**Group handover.** Day 6 can secure local dependencies and secrets whichever rows succeed. For Day 7 name one deployment option you can inspect. For Day 8 distinguish a provider read from an actual create/destroy. For Day 9 name a signal you can inspect and an alarm you can or cannot create. For Day 10 identify what cloud evidence the release review can honestly use.
