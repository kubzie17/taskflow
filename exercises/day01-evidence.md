# My Day 1 evidence

Work in this copy or a private note. Use fictional task names. For each entry mark **ran on my machine**, **observed with partner**, or **pending**. Share extracts or a redacted screenshot with the trainer.

| Checkpoint | My evidence |
| --- | --- |
| Incident observation, assumption and client question | |
| Repository owner or offline route; branch | origin → github.com/kubzie17/taskflow; branch `feature/health-service`. Commit `9a34eed` made locally; push pending (GitHub unavailable) — run `git push -u origin feature/health-service` when back online |
| Python path and baseline /health response | **ran on my machine** — interpreter `.../taskflow/.venv/bin/python`; `GET /health` → 200 `{"status":"ok"}` |
| POST status and id; GET result after restart | **ran on my machine** — `POST /tasks {"title":"Book van service"}` → 201, `id: 1`; after stopping and restarting the server, `GET /tasks` still returned `[{"title":"Book van service","id":1}]` (persisted in `data/taskflow.db`) |
| Invalid title result; what the test database isolates | **ran on my machine** — `POST /tasks {"title":""}` → 422 Unprocessable Content (`string_too_short`, min 1 char). Tests use a throwaway temporary database (`TemporaryDirectory()` → `test.db`), so they never touch my real `data/taskflow.db`; my booking stayed in the on-disk database |
| Release vote; condition; owner | **Hold** the release. Condition: no proof a booking can be saved and reopened since the change. Evidence needed: one test (or manual run) of the save-and-reopen flow passing. Owner: the developer who made the change |
| First meaningful red-test message | **ran on my machine** — `FAILED tests/test_api.py::TestTaskFlow::test_health_identifies_service - KeyError: 'service'` (describes the missing behaviour, not a setup error) |
| Final health JSON; test count; branch commit hash | **ran on my machine** — `/health` → `{"status":"ok"}`; baseline test count **2 passed** (before TF-01); after TF-01 **3 passed**; final `/health` JSON `{"status":"ok","service":"taskflow"}`; branch `feature/health-service`, commit `9a34eed` |
| Debug ticket; hypothesis; command; result | |
| Feedback I received or gave | |
| One thing I can explain; one blocker; Tuesday's next step | |
