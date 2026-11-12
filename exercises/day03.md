# Day 3 | Will the booking survive the next release?

Northbridge Repairs wants to put its booking API through a local release rehearsal. Work on your own copy of TaskFlow and use fictional bookings. Each brief below describes the outcome dispatch needs. Choose how to achieve it and bring evidence for another learner to inspect.

## Before the workshop

Use the branch containing your repaired Day 2 test. Record your branch, commit and latest test result. The class reached **Repair and push**. If your evidence is incomplete, record the missing check and agree a working base with the trainer. On a shared repository, keep using your assigned branch and agreed PR target.

The workshop uses Python 3.12, Git and an approved local container engine running Linux containers. If you use Docker, `docker version` should report a reachable server as well as a client. If your engine or image download is blocked, join a partner’s screen share. You can author the build and workflow on your own machine, direct their investigation and record exactly what you observed.

**TaskFlow’s interface.** The application is `app.main:app` and the dependencies are in `requirements.txt`. `GET /health` reports process health. `POST /tasks` accepts a title and returns an id. `GET /tasks` returns saved bookings. The service reads `TASKFLOW_DB` at startup and otherwise uses `data/taskflow.db`. Use your own lab names, port and disposable local data.

## Package the dispatch API

**Scenario.** A colleague with a container engine and a clean checkout needs to run your proposed release.

**Outcome.** Produce a versioned candidate, its build definition and build-context exclusions. The colleague can reach TaskFlow locally. Your development environment, local database and private settings stay outside the build context.

**Evidence.** Record the source revision, image tag and image ID, running instance ID and an API response. A partner should be able to identify precisely what they tested.

## Keep an existing booking through replacement

**Scenario.** Operations is replacing the running instance on the same host. Dispatch has already entered a fictional repair.

**Outcome.** The original booking is retrievable after replacement. Use the same image for the two instances. Create the booking once.

**Evidence.** Record the original id and exact title, the first and replacement instance IDs and the observed result on each. Have a partner check that this was a genuine replacement.

## Decide when packaging can proceed

**Scenario.** A failing booking test must prevent a broken revision being packaged. Passing tests should allow the packaging job to run.

**Outcome.** Extend your existing pull-request workflow and rehearse a manual decision about a local release. Keep the deliberate fault on your own lab branch. Keep production services and registries outside the rehearsal.

**Evidence.** Identify the revisions and results for both cases, including the state of the packaging job. Record which local candidate you checked, your decision and the observation that justified it. Label hosted, local and pending evidence accurately.

## Investigate the missing booking

**Scenario.** Instance A accepted booking 27, “Inspect east gate Q7”, and returned it in the list. Following maintenance, instance B answers its health check with HTTP 200 and returns an empty list. Dispatch is waiting for a release decision.

**Outcome.** Agree two plausible explanations in your breakout. Request one observation from the trainer or operator that distinguishes them. State what you would do next.

**Evidence.** Give dispatch your recommendation, the observation behind it and the condition that would change it.

## Record your own release evidence

Copy this record into your own notes. If you are using a shared course repository, keep your completed record in your individual workspace or submit it in the meeting.

| Item | Your evidence |
| --- | --- |
| Day 2 source branch, revision and actual test result | |
| Image tag and image ID, with build revision | |
| First instance ID and original booking id and title | |
| Replacement instance ID and same booking retrieved | |
| Failed test revision and package job outcome | |
| Passing revision, tested commit if available and package job outcome | |
| Local smoke check, decision and evidence a reviewer confirmed | |
| Outstanding risk, owner and next check | |

Mark each observation **ran**, **directed**, **observed** or **pending**. A local process rehearsal can establish that a database file retained a booking. A claim about replacing containers also needs instance and mount evidence.

## Optional booking check

Once you have created a fictional booking, you can use [check_booking.py](check_booking.py) from the project root to read back its id and exact title. The probe only reads your loopback service. Supply the port you actually published. For example, if the service returned id 7 for the title below:

```text
python exercises/check_booking.py --port 8083 7 "Inspect bay door Q7"
```

A successful result reports the health response and matching booking. A missing row, mismatched title, unreachable service or invalid response returns a non-zero exit code. Capture results for the candidate you actually ran.
