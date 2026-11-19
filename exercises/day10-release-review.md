# Final review — Should Northbridge Release TaskFlow?

**14:00–14:15.** Review another team's evidence. Teams rotate A reviews B, B reviews C, C reviews A. Spend 5 minutes reading, 5 minutes questioning and 5 minutes recording the decision. Review a **restricted training pilot** separately from an internet-facing production service.

Record reviewer names, reviewed team, scope, source commit, image digest and evidence location. Choose **Go**, **Conditional Go** or **No-Go** and justify the decision. Missing evidence is recorded as unverified. Conditional Go must name conditions, owners and a deadline; a failed essential security check remains No-Go for release until repaired and verified.

| Area | Evidence to ask for |
|---|---|
| Source and release | Reviewed commit; dependency/security and test results; real failed-gate proof; correct protected image; digest; approved OIDC/manual deployment route |
| Infrastructure and identity | Original Terraform state owner, instance and EBS IDs; correct mount; private access; scoped IAM; runtime identity protected |
| Application behaviour | Visitor/invalid token 401; reader read 200/write 403; dispatcher creation 201; denied writes unchanged |
| Operations | Real CloudWatch observation; fault diagnosis; recovered protected request; consistent checkpoint; preserved original; restore comparison; recovery timings and scope |
| Cost and ownership | Cleanup authorisation and ledger; retained-resource owner; single-host and same-volume recovery limitations; realistic improvements |

For each area record an evidence link or observation, remaining gap and judgement: `Supported`, `Partial` or `Unverified`. The workbook includes editable fields. A well-supported No-Go is a valid engineering outcome.

## Shared assessment rubric

Use the descriptors for evidence quality, not confidence or presentation polish.

| Criterion | Developing | Secure | Strong |
|---|---|---|---|
| Evidence and provenance | Claims lack exact target/time/result | Observations identify target, time, result and scope | Independent checks connect source, release and business behaviour |
| Diagnosis and recovery | Repair attempted without a supported diagnosis | Cause, reversible repair and verification are explained | Explains monitoring blind spots and separates detection from recovery |
| Data and recovery objectives | Copy or timing claims are unclear | Consistent checkpoint, separate restore and RTO/RPO distinction shown | Relates checkpoint age and missing events to proposed objectives and architecture limits |
| Release decision | Decision has unsupported assumptions | Decision follows actual evidence and named conditions | Prioritises residual risks with practical, owned improvements |
| Cleanup discipline | Ownership or verification is missing | Original state, approved scope and exact-resource verification recorded | Reconciles shared/external resources and unresolved cost ownership |

The trainer records individual explanations and contributions separately from the team's outcome. Do not infer that every learner independently completed an AWS operation from one shared screen demonstration.
