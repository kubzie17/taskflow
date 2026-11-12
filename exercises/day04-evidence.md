# Northbridge pilot evidence hunt

Workshop 3 • Fictional training evidence • Local pilot review

Each pair starts with the exhibit the trainer assigns. Open it on your laptop, then switch the driver and read the next exhibit. Read the extract as if it has just arrived in a release review. Record what it establishes, what remains uncertain, who could be affected, the next evidence you would request and a possible control with a check. Pick an OWASP Web Top 10:2025 category and defend it. Another table may reasonably prioritise a different risk.

## Exhibit A | Request capture

A tester is using an isolated pilot with a fresh local database. These are the complete application request headers recorded for the first call. The access policy supplied by dispatch says that only authorised dispatchers may create bookings.

~~~http
POST /tasks HTTP/1.1
Host: 127.0.0.1:8044
Content-Type: application/json
Content-Length: 30

{"title":"Inspect north gate"}
~~~

~~~text
Response: HTTP 201
Body: {"title":"Inspect north gate","id":17}
Later list: HTTP 200
Body: [{"title":"Inspect north gate","id":17}]
~~~

Only the shown route and lab have been observed. Which deployment details would change the importance of this finding?

## Exhibit B | Container run record

A service desk ticket describes a training diagnostic viewer that was intended for use on its operator’s laptop. The team has sent this output from its isolated rehearsal. There are no credentials or live addresses in this exhibit.

~~~text
Application health: HTTP 200
Application startup: diagnostics enabled
Published port: 0.0.0.0:8044 -> 8000/tcp
Operator notes: tested from a browser on the same laptop
~~~

The ticket contains no firewall rules, remote connection test, inventory of diagnostic fields or approved audience. What would you ask the operator to verify?

## Exhibit C | Dependency review

This is an invented package and an invented pull request. Inspect the text only. The package has no role in the TaskFlow installation.

~~~diff
- northbridge-format==1.4.2
+ northbridge-format==1.5.0
~~~

~~~text
PR message: "Picked up the newest formatter to unblock the pilot."
CI summary: application tests passed
Review attachments: none
Request from the release lead: "What evidence connects this change to a trusted release?"
~~~

What would a green test tell you, and what evidence is still missing before the team can judge the update?

## Table record

| Exhibit | Observed fact | Uncertainty | Potential harm and affected party | Web category and reason | Next evidence | Proposed control and check |
| --- | --- | --- | --- | --- | --- | --- |
| A | | | | | | |
| B | | | | | | |
| C | | | | | | |

During on-screen peer review, record one conclusion that your peers supported and one assumption they persuaded you to revise.
