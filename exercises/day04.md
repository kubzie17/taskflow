# Day 4 | Can we trust who is using TaskFlow?

Northbridge Repairs wants contractors to view bookings and only authorised dispatchers to create them. Today your team investigates that proposed pilot, repairs a local release candidate and advises the client. Use fictional bookings and your own local copy. Every learner should finish with an individual decision, a repair commit or recorded blocker, and a check to take into Day 5.

## Your digital record

Open [the Day 4 workshop workbook](Day_4_Workshop_Workbook.xlsx) in Excel or LibreOffice Calc. Use **Save As** to make a named copy outside the course repo. Use the tab with the same number as each workshop. On a shared machine each learner saves a separate copy. Review by turning the laptop to a partner or viewing their screen.

**VS Code option.** Save a personal copy of this guide as a Markdown file. Type in the blank fields below and press **Ctrl+S** (or **Cmd+S**). Keep the original course folder open in VS Code to read `exercises/day04-evidence.md`. Enter your name, one verified Day 3 fact and one open question before you begin.

## At your desk

1. Open your existing TaskFlow checkout in VS Code. Use the project’s Python 3.12 environment. Run `git status -sb`. Save your intended Day 3 work on its own branch. The [course README](../README.md) explains how to bring in the class update. If your local README has extra edits, retain them.
2. From the working revision containing your previous work and the Day 4 files, start a new personal branch. Example: `git switch -c day04-jordan`. Use your own unique name. Record `git rev-parse --short HEAD` and the result of `python -m pytest -q`. If a branch of that name already exists, inspect it before reusing it.
3. From the repository root, start the workshop service. Keep that terminal open.
   
   ~~~text
   python -m uvicorn exercises.day04_candidate:create_candidate --factory --host 127.0.0.1 --port 8044
   ~~~
   
   Open `http://127.0.0.1:8044/docs` and `http://127.0.0.1:8044/health` in your browser. If the port is busy, choose another free port and use it in every URL. The workshop uses `data/day04-lab.db`. Your existing TaskFlow factory supplies the booking routes. Use another terminal for tests and Git. A running Day 3 container can keep its own port and data.
4. If the factory import fails on your own branch, keep your changes. Ask for the clean **Day 4 compatibility starter** and open it in a separate empty folder using the same project Python. The trainer has a copy. If the interactive page cannot load, try the plain local URLs and use the fallback at the end of this guide.

## 1 | Map the journey of a booking

A dispatcher reports that a new booking appeared on the list. Build two editable maps on **1 Map**. Each row represents one arrow and can be read aloud to a reviewer. Trace a request and its response across the browser, API, validation and SQLite. Add a second route from a proposed code change through review, tests, packaging and starting the candidate. Mark what is actually connected in your setup.

**Bring back** a labelled asset, actor, entry point and trust boundary, a plausible threat and one assumption. Invite a reviewer to follow both routes on screen, question one boundary and see what you revised.

**VS Code map.** Duplicate rows as needed. Use a return row for a response or repeat a source for a branch.

| Route | From | Data or action | To | Trust boundary and owner | Observed or assumed |
| --- | --- | --- | --- | --- | --- |
| Booking | | | | | |
| Booking | | | | | |
| Release | | | | | |
| Release | | | | | |

Actor, asset and entry point —  
Plausible threat —  
Peer challenge and revision —

## 2 | Can a visitor create a booking?

Dispatch believes that only authorised dispatchers can create jobs. Investigate that statement using your local training service. One partner acts as a visitor without supplying credentials. The other acts as dispatch and reads the list. Use one distinctive fictional title. Swap the operator and reviewer.

**Bring back** the request, status, returned body or refusal, and your read-back observation. Explain who could be affected. Write acceptance criteria covering a visitor, a contractor with reader permission and an authorised dispatcher. Include the expected database effect when a write is denied. Today you test current behaviour and specify the policy for Friday. Record it on **2 Visitor** or below.

| Your local observation | Your evidence |
| --- | --- |
| Caller, request and URL | |
| Status, response and list before/after | |
| Possible harm | |
| Proposed criteria for visitor, reader and dispatcher, including storage effects | |

## 3 | OWASP evidence hunt

Read the three fictional exhibits on **3 Evidence** or in [the local evidence file](day04-evidence.md). Begin with the exhibit assigned to your pair, then take turns at the keyboard. Separate the observation, inference and open question before proposing a web risk category.

**Bring back** a defended category, impact, missing information and a control with a check for each exhibit. Ask another table to challenge one inference. Identify a conclusion that changed or explain why you kept it.

| Exhibit | Fact | Unknown / next evidence | Harm | OWASP category and reason | Control and check |
| --- | --- | --- | --- | --- | --- |
| A | | | | | |
| B | | | | | |
| C | | | | | |

Peer challenge and revision —

## 4 | Repair the pilot candidate

The public monitor reads `GET /support/status`. Its contract is HTTP 200 with exactly two public fields: `status` with value `ok` and `service` with value `taskflow`. Support still needs its existing diagnostic snapshot locally. A tester reports that the public surface reveals internal information. Use the candidate you started at your desk.

**Acceptance.** Reproduce the report, capture what a visitor can see and explain why dispatch should care. Write an automated regression test that fails for the disclosure. Repair the candidate so the public contract holds, the local support capability remains and the existing health and booking workflows still work. Use a temporary database for automated tests. Keep real credentials and customer data out of the exercise.

**Bring back** before and after browser or HTTP observations, the failing assertion, passing test results, a personal repair commit and an independent peer result against that revision. Give your partner the revision and contract before showing your change. Restart the local workshop service after editing so the browser serves the changed code. Learners can make different repairs that meet the same contract. Capture your results on **4 Repair** or here.

| Check | Your evidence |
| --- | --- |
| Before response and risk | |
| Failing assertion | |
| Passing suite and after response | |
| Original functionality checked | |
| Repair commit, reviewer and their independent result | |

## 5 | Decide what blocks the pilot

The pilot owner can fund one engineering slot. Speak as dispatch, engineering or the budget holder. Compare the unrestricted-write question and one other risk your table investigated. Consider the audience for the pilot, the existing controls and the strength of your evidence.

| Risk event and affected asset | Likelihood 1–3 and reason | Impact 1–3 and reason | Score and priority | Control, owner and acceptance check | Residual risk and next review |
| --- | --- | --- | --- | --- | --- |
| | | | | | |
| | | | | | |

Use 1 for low and 3 for high. Multiply likelihood by impact as a starting point. Justify the order in business terms. Mark any assumption that could change the order. Map at least one control to an OWASP category. Use **5 Risks** or this table. Show a partner your register on screen, hear one objection and revise your own copy.

Control to fund first and why —  
Peer objection and revision —

## 6 | Client release panel

Northbridge wants a decision today. Each learner has a minute to recommend proceed, hold or proceed with conditions. A reviewer may ask for one piece of evidence and one uncertainty.

**Bring back** your decision, the specific pilot audience it covers, the supporting observation, a remaining risk with an owner, and the access-control check you will carry into Day 5. Identify which evidence you collected, which you observed and which you still need. Use **6 Panel** or fill in your Markdown copy.

| Role | Question to bring to the panel |
| --- | --- |
| Dispatch lead | What would the dispatcher see and how did you verify it? |
| Engineering reviewer | Which revision and independent check support the claim? |
| Budget holder | Which condition would change the priority and who will check it? |

Name and role —  
Pilot scope and decision —  
Evidence and reviewer’s question —  
Remaining risk, owner and next check —  
Day 5 access rule and expected storage effect —

## Desk support

- In the Swagger page, expand the route you intend to exercise, select **Try it out**, enter fictional data if required and select **Execute**. Record the actual server response. Browser tabs opened directly at `/health`, `/tasks` and `/support/status` are useful for reads.
- If the interactive API controls cannot load, Windows PowerShell can submit the same fictional booking. Use the port of your own service: `Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8044/tasks -ContentType 'application/json' -Body '{"title":"Inspect bay A4"}'`. Read it back in the browser at `http://127.0.0.1:8044/tasks`. On macOS or Linux, an equivalent is `curl -i -H 'Content-Type: application/json' -d '{"title":"Inspect bay A4"}' http://127.0.0.1:8044/tasks`.
- Run `python -m pytest -q` from the repository root and record the count your branch actually reports. Keep test databases in temporary directories. When finished, stop your workshop server with Ctrl+C.
- For peer review, share the repaired branch or let a partner use a separate checkout of the commit at your desk. If GitHub is available, push only your personal lab branch to your course repo and request the agreed review. Show which revision the reviewer actually checked.
