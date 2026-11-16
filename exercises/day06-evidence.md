# Day 6 personal security evidence

Save a copy under your own name outside the repo or in your existing progress record. Use fictional records, short error names and test counts. An operator can run a command for a partner. Mark who ran it, who observed it and on whose machine it ran. Share an HTTP status or a redacted excerpt, never a token, log dump, credential, AWS account number or private URL.

## Booking clinic

Revision and entry point __________  Operator __________  Direct SQLite file or test fixture __________

| Caller and input | Expected HTTP | Actual | Stored IDs and titles before and after | Test or source of evidence |
| --- | --- | --- | --- | --- |
| Visitor POST valid title | 401 | | | |
| Reader GET known booking | 200 | | | |
| Reader POST valid title | 403 | | | |
| Dispatcher POST valid title | 201 | | | |
| Invalid token POST valid title | 401 | | | |
| Dispatcher POST 101-character title | 422 | | | |

## Dependency decision

| Evidence to establish | Your finding |
| --- | --- |
| Actual declared pin / installed version / interpreter | |
| One direct → transitive dependency edge with evidence | |
| Proposed version / advisory ID / affected range / first fixed | |
| Which local or optional provider code reaches the affected call? Under what conditions? | |
| Your decision, compatibility check, test outcome and remaining risk | |
| Tool and database used or dated offline evidence | |

## Secret incident

| Commit that introduced the marker / current tree result / clean-up commit | Which destinations are observed? Which are only possible? | Incident actions in order, with owner | Git red → green / sample still tracked | Docker evidence or pending check |
| --- | --- | --- | --- | --- |
| | | | | |

## Pipeline and independent review

| Scenario at tested revision | Expected dependency / test / package | Actual result and evidence level (hosted, local execution, static or pending) |
| --- | --- | --- |
| Rejected proposal | | |
| Approved pin and a deliberately failing disposable test | | |
| Approved pin and passing booking + full tests | | |

Reviewer __________  Revision inspected __________  Independent input chosen __________

One verified result __________  One limitation __________  Next action and owner __________

## Tuesday handover

Use the existing `exercises/day05-aws.md` matrix for the class observations. Carry forward one specific service/action, region, observed status, permitted fallback and owner. Record locally what you personally established.
