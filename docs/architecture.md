# How TaskFlow handles a request

Northbridge Repairs is a fictional repair business. Its dispatchers need to record jobs that the next shift can still see. Use invented task titles throughout the course.

| When you… | The request goes to… | What happens |
| --- | --- | --- |
| Open /health | Uvicorn, then the health handler in app/main.py | The process replies with its status. This route never queries the database. |
| Create a task | POST /tasks, TaskInput, then database.create_task | FastAPI validates the JSON. SQLite stores the title and allocates an integer id. |
| List tasks | GET /tasks, then database.list_tasks | SQLite returns committed rows, ordered by id. A fresh database returns an empty list. |
| Run the tests | tests/test_api.py, then a test instance of the same API | Each test uses its own temporary directory and database. Your demonstration data stays separate. |

Uvicorn listens on your computer at 127.0.0.1:8000. A browser, Swagger UI at /docs, or a terminal HTTP client can send requests to it. The SQLite file is data/taskflow.db unless you change TASKFLOW_DB. Start the server from the project root so relative paths resolve consistently. A server restart reopens the same file.

## Where the course takes this project

You will add an identifiable health response, a release check, a workflow in YAML, a container, access rules, risk and architecture decisions, and a small local Terraform deployment description. You will also rehearse a release and a recovery. Later AWS designs consider a network boundary, compute, managed relational storage and monitoring. Moving from a single SQLite file to a managed database requires a database engine choice, changes to the storage layer and a data migration.

The starter accepts local task reads and writes without signing in. Keep the server bound to loopback and use fictitious examples. Decide who should be allowed to do each operation as part of the security block.
