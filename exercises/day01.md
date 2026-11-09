# Day 1 lab • Monday 9 November • Online

Keep this page open next to your terminal. Record short answers in a private note or [your evidence sheet](day01-evidence.md). Paste short outputs into the class chat when asked. You can send them privately, describe them aloud or use a partner's screen. Mark partner observations as **observed** and your own runs as **ran**.

## A • An 08:05 handover incident • 09:30–10:10

**Scenario and goal.** Dispatch says yesterday's release worked on the developer's laptop, yet this morning the next shift cannot see a job. Work out what you can verify and who needs to act. You need only the chat and this page. Edit your evidence sheet.

1. Write one observation, one assumption and one person you would speak to. Keep them distinct.
2. In pairs, one person plays dispatch and one plays the engineer. Ask for an example of the missing job and what a successful handover would look like. Switch roles.
3. Each pair submits one client question and a check it could lead to. If working alone, write both sides in chat.

**Check:** A peer can perform the proposed check and say how they would recognise success. If your suggestion is “improve communication”, give it an owner and a moment in the release. **Stretch:** name a signal that could detect the problem after release.

## B • Give yourself a working copy • 10:10–10:45

**Goal.** Show that your own project and Python interpreter serve the untouched application. You need the starter URL or learner ZIP, Python 3.12, Git and an editor. Use README sections 1–4. No source edits.

1. Generate **your own** repository from the trainer's template and clone yours. If GitHub is unavailable, use the README's ZIP and local Git route.
2. In the folder with requirements.txt, create and activate .venv, install the packages and start Uvicorn in terminal A.
3. Open /health. In terminal B, check your working folder and interpreter. Record the health JSON and the owner shown by `git remote -v` (or “offline repository”).
4. Send **green** for a local health response, **amber** for files but no response, or **red** for no copy. Include the last successful step, without account credentials.

**Check:** the local process returns HTTP 200 and `status` is `ok`. If a second terminal sees the wrong Python, activate the environment there as well. **Stretch:** open /openapi.json and identify which methods exist on /tasks.

## C • Does a new shift still see the job? • 11:00–12:00

**Scenario.** The dispatcher enters a booking and closes the app. Does a colleague see it after a restart? Work in pairs. One controls their own machine, one predicts the result. Swap after the first request sequence. You need a running starter; navigators can use the sample transcript below. Use the evidence sheet. No code changes.

1. Predict what GET /tasks will return on a new database. Use /docs or README section 4 to send the request. Make a note if your list already contains rows.
2. Create a task called `Book van service`. Record the POST status, generated id and title. Then GET the list and find that same id.
3. Stop A with Ctrl+C and restart it from the same folder. Retrieve the list again. Keep the same TASKFLOW_DB setting. Explain what survived.
4. Try POST /tasks with `{"title":"   "}`. Predict, run and record the status. Check whether a new row was added.
5. In B, activate .venv and run `python -m pytest -q`. Read one test in tests/test_api.py. Explain whether it touches your live data.

**Check:** show a 201, the same id after restart, the invalid request outcome and the baseline test count. A different id from your partner is fine. If the list looks empty after restart, check the working folder and database setting. **Stretch:** create the same title twice. Decide what the two ids tell you, and what requirement you would ask about before changing the behaviour.

**Navigator transcript for restricted devices.** A colleague recorded `POST /tasks → 201 {"id":7,"title":"Book van service"}`, `GET /tasks → 200 [{"id":7,"title":"Book van service"}]`, then restarted the server and saw id 7 again. A blank title returned 422. Write the command or HTTP method you would ask the driver to run next. Record that this evidence was observed. Reattempt B on your own machine when available.

## D • Agree a release decision • 13:00–13:20

**Goal.** Give dispatch a defensible release decision. The live monitor is green, but nobody has tried saving and reopening a task since the change. Use your morning evidence and a partner or chat. Edit only your evidence sheet.

1. Vote “release”, “hold” or “limited trial”. Give one reason.
2. Ask the client one question about the impact of losing a booking. Write a condition under which you would change your vote, plus an owner for the check.
3. Read a peer's answer. Underline the part a dispatcher could act on today.

**Check:** your recommendation contains a condition, evidence and an owner. If you start listing tools, translate one into an observable outcome. **Stretch:** propose a concrete rollback trigger.

## E • First change ticket TF-01 • 13:20–14:15

**Client request.** “Our support screen checks several services. When TaskFlow answers its health check, show which service answered. Keep the existing status so the old monitor still works.” It expects the new JSON field `service` with value `taskflow`. Use **app/main.py** and **tests/test_api.py**. Begin with the two passing tests on your own copy.

1. Run `git switch -c feature/health-service`. Inspect the existing health test and the handler for GET /health.
2. In the existing test class add a new test method starting with `test_`. Use the existing health test as a pattern. Ask whether the returned body identifies the service. Keep both original tests.
3. Run `python -m pytest -q`. Save the first useful failure. If it is an import or syntax error, fix that before counting it as the intended red test.
4. Change the health handler to meet the request. Re-run the suite, restart A and check /health in a browser or terminal.
5. Review the diff with a peer or in private chat. Use README section 6 to commit the source and test, then push to **your** remote if available. Save the hash and final JSON.

**Check:** the baseline status still works, the new field has the agreed value, and all three tests pass. Git shows a feature-branch commit. If existing tests disappear, compare the test names with the starter. **Stretch:** explain why a green health test does not prove a booking can be saved, then propose a separate readiness check in plain English.

## F • Debugging clinic and handover • 14:30–15:30

**Goal.** Turn an error report into evidence for the next engineer. Use terminal A/B, this page and your note. Keep your working branch intact. Deliberately reproduce tickets only on your own local server.

| Ticket | Observation | Your task |
| --- | --- | --- |
| A · environment | Terminal A serves requests. B prints `No module named pytest`. | Name two possible causes. Choose a read-only command that distinguishes them and show a recovery. |
| B · HTTP | A request to GET /tasks works; PUT /tasks returns 405. The dispatcher wants to create a task. | Use the API contract to determine the appropriate method and body. Verify the result and read back the id. |
| C · wrong process | A colleague launched on port 8001; their bookmarked 8000 address refuses the connection. | Use the server log to state which URL to check. Explain what could happen if another service owned 8000. |

1. Choose A for an entry challenge, B for intermediate, or C plus a second ticket for stretch. Work independently for four minutes before asking a peer.
2. Exchange evidence with a peer. Show the symptom, your hypothesis, the check and its result. Paste a short transcript or explain by voice.
3. Volunteer a 60-second demo or let the trainer read your text. Complete the exit quiz and submit one personal checkpoint, one blocker and your next step for Tuesday.

**Check:** someone else can repeat your diagnostic step and see what changed. If you cannot run it, use the supplied symptom to propose the next command and mark it “not yet run”. **Stretch:** explain why re-installing everything might hide the original cause.
