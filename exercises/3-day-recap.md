# TaskFlow: a 3-day recap (from the very basics)

This is a plain-English walkthrough of everything we built over three days. It
assumes almost no prior knowledge and explains each tool as it appears.

---

## The big picture

We worked on a small web service called **TaskFlow** — an app that stores
"bookings" (tasks) for a fictional company, Northbridge Repairs.

The story driving everything: a dispatcher's booking went **missing after a
software release**, even though all the monitoring looked healthy. Over three
days we learned how to build, check, package, and prove a service actually
works — so that kind of silent failure gets caught.

The single most important idea of the week:

> **"It responds" is not the same as "it works."**
> A service can reply "I'm fine" while quietly losing your data.

---

## Core concepts (the vocabulary)

- **API** – a way for programs to talk to each other over the web. Instead of
  clicking buttons on a page, you send a request to an address and get data back.
- **Endpoint** – one specific address/action in the API. TaskFlow has three:
  - `GET /health` – "are you alive?"
  - `POST /tasks` – "create a booking"
  - `GET /tasks` – "list the bookings"
- **HTTP status codes** – short numbers that say how a request went:
  - `200 OK` – handled successfully
  - `201 Created` – a new thing was created
  - `422 Unprocessable` – your input was rejected (e.g. an empty title)
- **JSON** – the text format used to send data, e.g. `{"title": "Book van service"}`.

---

## The tools we used (names worth knowing)

The app is written in **plain Python 3.12**, using these libraries:

- **FastAPI** – the web framework. Defines the endpoints and validates requests.
- **Pydantic** – validation rules (e.g. "a title must be 1–100 characters").
- **Uvicorn** – the web server that runs the app and listens on a port.
- **SQLite** – the database; stores bookings in a file on disk.
- **pytest** – the tool that runs our automated tests.

And the surrounding tools:

- **Git / GitHub** – track changes and host the code (branches, commits, PRs).
- **GitHub Actions** – runs our tests automatically (a "CI pipeline").
- **Docker** – packages the app into a portable "container".

### The files we worked in

- `app/main.py` – the application itself (the three endpoints).
- `app/database.py` – the SQLite storage layer (already written for us).
- `tests/test_api.py` – the automated tests.
- `.github/workflows/taskflow-ci.yaml` – the CI pipeline.
- `Dockerfile` and `.dockerignore` – packaging the app into a container.
- `requirements.txt` – the list of libraries the app needs.

---

## Day 1 — run the app and make a safe change

### 1. Set up an isolated environment

A **virtual environment** (`.venv`) is a private copy of Python for one project,
so its libraries don't clash with anything else on the machine.

```bash
python3 -m venv .venv          # create it
source .venv/bin/activate      # switch into it
python -m pip install -r requirements.txt   # install the app's libraries
```

### 2. Run the app

```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Then visit `http://127.0.0.1:8000/health` in a browser → `{"status":"ok"}`.
`127.0.0.1` means "this computer"; `8000` is the port it's listening on.

### 3. The key lesson

`GET /health` returned `200 OK` — but that only means the **service answered**.
It never looks at the database. So a booking can be missing while health stays
green. That's exactly how the dispatcher's booking "disappeared".

### 4. Our first change — using Test-Driven Development (TDD)

The ticket (TF-01): make `/health` also say **which service** answered, while
keeping the old `"status": "ok"` so existing monitoring doesn't break.

**TDD** means: write the test first, watch it fail, then write the code to make
it pass. The cycle is called **red → green**.

1. **Red:** added a test expecting `"service": "taskflow"` → ran `pytest` → it
   failed with `KeyError: 'service'` (because the code didn't do that yet).
2. **Green:** changed one line in `app/main.py`:
   ```python
   return {"status": "ok", "service": "taskflow"}
   ```
   Ran `pytest` again → all tests passed.

### 5. Record it with Git

```bash
git switch -c feature/health-service-oliver   # a branch = a safe workspace
git add app/main.py tests/test_api.py
git commit -m "Identify TaskFlow service in the health response (TF-01)"
git push -u origin feature/health-service-oliver   # upload to GitHub
```

---

## Day 2 — automate the checking (CI)

### 1. A boundary test

We added a test proving that an over-long title (101+ characters) is **rejected
with 422** *and* doesn't change the existing bookings. (A rejected request must
leave stored data untouched — a `422` alone doesn't prove that.)

### 2. Continuous Integration (CI)

**CI** means: every proposed change is automatically tested in a clean,
shared environment before a human approves it. We used **GitHub Actions**.

A **workflow** is a YAML file describing *when* to run and *what* to do. Ours
(`.github/workflows/taskflow-ci.yaml`) says: when a pull request is opened,
spin up a fresh Ubuntu machine, install Python 3.12, install our dependencies,
and run `pytest`.

A **pull request (PR)** is a proposal to merge your branch's changes. Opening
one triggers the workflow.

We also solved a subtle requirement: make the job run **only for our own branch**
(so other learners' PRs don't trigger it):

```yaml
if: github.head_ref == 'feature/health-service-oliver'
```

`github.head_ref` is the PR's source branch. The job only runs when that matches.

### 3. The "break and repair" drill

To prove the pipeline actually catches mistakes:

1. Deliberately broke a test (expected `400` instead of the correct `422`),
   pushed it → CI went **red** (failed).
2. Restored it to `422`, pushed again → CI went **green**.

Important nuance: the app was never broken — the **test's expectation** was
wrong. A red check means "something doesn't match"; your job is to work out
*which side* is wrong.

---

## Day 3 — package it and prove data survives

### 1. Containers and Docker

A **container** is a sealed box holding the app plus everything it needs to run,
so anyone can run it identically without installing Python or the libraries by
hand. **Docker** builds and runs containers.

- A **Dockerfile** is the recipe for building the box (an **image**).
- A **`.dockerignore`** lists things to keep *out* of the box (your `.venv`,
  local database, secrets) — just like `.gitignore` for Git.

Our `Dockerfile` (simplified): start from Python 3.12, install
`requirements.txt`, copy the `app/` code, and run Uvicorn on `0.0.0.0:8000`
(`0.0.0.0` so it's reachable from outside the container).

Build and run:

```bash
docker build -t taskflow:ed71818 .          # build an image, tagged with the git revision
docker run -d -p 8083:8000 taskflow:ed71818  # run it; map our port 8083 -> container's 8000
```

- An **image** is the built box (identified by a tag like `taskflow:ed71818`
  and an ID).
- A **container** is a running instance of that image.
- Tagging the image with the git revision links the running thing back to the
  exact source code it came from.

### 2. Making data survive a replacement

By default, a container's data vanishes when the container is deleted. To keep
bookings, we store the SQLite file on a **volume** — storage that lives
*outside* the container.

We proved it:

1. Started container **A** with a volume, created one booking
   ("Inspect east gate Q7", id 1).
2. **Deleted container A entirely** and started a fresh container **B** from the
   same image with the **same volume**.
3. `GET /tasks` on B still showed the booking — **it survived** because the data
   was on the volume, not inside the container.

```bash
docker volume create taskflow-data
docker run -d -p 8083:8000 -v taskflow-data:/data taskflow:ed71818
```

### 3. Stretch — reproducing the "missing booking" on purpose

We started a container with **no volume**. The result:

- `GET /health` → `200 OK` (looks healthy)
- `GET /tasks` → `[]` (booking gone!)

**Why:** with no volume, the container made a brand-new empty database inside
itself and never saw the real data. Health stays green because it never checks
the database. This is the Day 1 incident reproduced deliberately — and the real
lesson of the whole week:

> A green health check does **not** prove the data is there.

---

## One-line summary of each day

- **Day 1:** Run the app, understand that "200 OK" ≠ "data saved", and make a
  safe code change using test-first development, recorded in Git.
- **Day 2:** Automatically test every change with a GitHub Actions CI pipeline,
  and prove it catches failures.
- **Day 3:** Package the app with Docker so anyone can run it, and prove that
  stored bookings survive replacing the running container.

Everything built toward one goal: having real **evidence** that a release is
safe, instead of trusting a green light.
