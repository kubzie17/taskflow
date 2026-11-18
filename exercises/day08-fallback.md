# Continue a blocked workshop on the same day
First give the real failure five minutes. Record the first failed operation and owner; another learner may share an approved live AWS target with read-only observation. One custodian keeps the real state. These exercises use separate local state.

## Terraform available, AWS or provider unavailable
1. From the real `infra/day08` folder run `Set-Location .\offline`. Check `Get-Location` before any apply or destroy. No AWS provider configuration belongs in this directory. It uses Terraform’s built-in terraform_data resource and needs no AWS identity or provider download.
2. Run `terraform fmt`, `terraform init`, `terraform validate`, `terraform plan -out=first.tfplan`, inspect the resource, then `terraform apply first.tfplan`. Record `terraform state list`, `terraform output observed` and `terraform state show terraform_data.pilot`.
3. Add a validated input `release_stage` with default foundation and allowed values foundation/deploy-ready. Reference it from the existing resource's release_tag input. Add `release_stage = "deploy-ready"` to a private `team.auto.tfvars` **in this offline directory**. Plan, approve the single update, apply and verify that the local resource ID stays the same.
4. For the short challenge use `terraform plan -var-file=..\..\..\exercises\day08-fault.case`. Repair a local copy in this directory, then re-plan. Record the diagnostic and the unchanged resource. Label evidence “provider-free local Terraform”.
5. Test the local lifecycle: `terraform plan -destroy -out=end.tfplan`, inspect, `terraform apply end.tfplan`, `terraform state list`. Return with `Set-Location ..`. This does not clean up any real AWS state. Preserve the real team's existing directory and private ledger for Thursday.

## Terraform executable unavailable
From the **repository root** use the Python standard-library rehearsal. This simulates a plan and a state file on disk. It does not validate HCL or exercise AWS. Watch an AWS or Terraform operator in Teams if available.
```powershell
python exercises/day08_offline.py plan foundation
python exercises/day08_offline.py apply
python exercises/day08_offline.py show
python exercises/day08_offline.py plan deploy-ready
python exercises/day08_offline.py apply
python exercises/day08_offline.py plan deploy-raedy
python exercises/day08_offline.py plan deploy-ready
python exercises/day08_offline.py show
python exercises/day08_offline.py destroy
```
Record the simulated ID before/after, the rejected spelling and the successful no-change prediction. C3 asks you to diagnose before progressing. Thursday’s AWS handover still needs a real target and a named owner. No simulated ID is an EC2 instance.
