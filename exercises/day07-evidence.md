# Team record | use a digital copy
Save this Markdown file outside the repository if Excel is unavailable. Use team labels A/B/C. Record role type, Region and outcomes only. The shared matrix has one row per team and operation; a nominated scribe may merge three copies or everyone may use the same authorised class document.

## 1 · Access
| Team / role type | Region | Service + precise operation | Available / Denied / Not tested | Observation (empty vs denied?) | Limit / expiry / reset | Route, owner and next check |
|---|---|---|---|---|---|---|
| | | Console launch / role | | | | |
| | | CLI / STS identity | | | | |
| | | IAM / list or view assigned role | | | | |
| | | VPC / subnet / route table | | | | |
| | | Security group / inbound | | | | |
| | | EC2 / instance + volume | | | | |
| | | S3 / list vs read assigned properties | | | | |
| | | CloudWatch / log groups list | | | | |
| | | ECS / cluster and service | | | | |
| | | S3 / approved object operations | | | | |
Budget and cost owner: ____  Session lifetime: ____  Resources survive session? ____  How known: ____  Route: ____

### Fictional offline evidence for Route C
This teaching inventory models a single Region, two AZs and a synthetic office client. Use `day07-network.json` for the six subnet records, route associations and candidate inbound rules. It models a VPC local route and an edge route to an internet gateway. No real AWS account is involved.
- Training EC2 exhibit: instance state running, AZ A, private address in app-a, no public address; inbound group sg-app; root gp3 delete-on-termination yes, data gp3 in same AZ with delete-on-termination no. Application health and SSH reachability have not been tested. Determine what can be inferred from these facts.
- Training S3 exhibit: private general purpose bucket, never versioned, block public access enabled, Object Ownership bucket owner enforced, default SSE-S3, no workload approval to write. A fictional list request for the assigned prefix succeeds; attempting IAM list roles is denied. Nothing here establishes rights in a live AWS account.
- Training hosting exhibit: one existing container image starts app.main:app, a prospective ECS cluster has zero services; deployment authority, approved budget and platform recovery objectives unknown. No production DB migration has been tested.

## 2–5 · Observation log
| Challenge / time | Prediction | Command or page | Observed result, redacted | Changed one thing | Retest / reviewer |
|---|---|---|---|---|---|
| 2 / caller + port | | | | | |
| 2 / row and identity | | | | | |
| 3 / two rejected or unsafe paths | | | | | |
| 3 / revised rule and model limit | | | | | |
| 4 / actual AWS or explicitly local | | | | | |
| 4 / fault, direct probe and repair | | | | | |
| 4 / exact-key cleanup if used | | | | | |
| 5 / last checkpoint and failure time | | | | | |
| 5 / recovered + original IDs / time | | | | | |
Diagram file: ____   API mode: ____   Container entry point verified how? ____   Important unverified inference: ____
Could we deploy on the assigned target? ____  Missing authority/cost, build, TLS, storage, monitoring or rollback: ____
Age of checkpoint at failure: ____   Observed time from failed probe to readable service: ____   Lost writes: ____   Proposed RPO / RTO: ____

## 6 · Client panel
| Decision | Pilot | Resilient |
|---|---|---|
| Request path and boundary | | |
| State, backup and restore | | |
| Failure and peak-load limit | | |
| Required code or deployment change | | |
| Security, monitoring and operator workload | | |
| Rate × units; monthly USD | | |
| Exclusions / sensitivity | | |
Client verdict and dissent: ____  Independent reviewer: ____  Changed assumption: ____
Terraform input/owner: ____  PR hardening owner: ____  Failing security check / package proof owner: ____  Independent release reviewer: ____
