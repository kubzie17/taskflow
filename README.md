# TaskFlow starter

Build and operate a small task API for the dispatch team at Northbridge Repairs. It can report that the process is alive, save a task and list saved tasks. There is no separate frontend. You can use the built-in API documentation in a browser or send requests in PowerShell.

Over ten days your copy will acquire release tests, a GitHub Actions workflow, a container, security controls, an AWS design and local Terraform infrastructure exercises. Today you need only Python, Git, an editor and this folder. Start with invented tasks and keep the server on your own computer.

**Course exercises** · [Day 1](exercises/day01.md) · [Day 2](#8-day-2) · [Day 3](#9-day-3)

## 1. Check your tools

The classroom uses Python **3.12.x** and Git **2.28 or later**. A free GitHub account is needed for your hosted copy. VS Code is the suggested editor. Internet access is needed for the initial download and package installation.

Windows: open **PowerShell** from Start. Enter one line at a time. A terminal is where you type commands. Its current folder determines which files each command can find.

```powershell
py -3.12 --version
git --version
```

Expect `Python 3.12.x` and `git version …`. If Python is missing, install the Python install manager from [Python for Windows](https://www.python.org/downloads/windows/), open a new PowerShell window and run `py install 3.12` with the current install manager. Recheck the version. If your school supplies Python through IT, use its approved installation. If `py` is missing but `python --version` shows 3.12.x, use `python` in place of `py -3.12`. Install Git from [Git downloads](https://git-scm.com/downloads) if needed, then reopen the terminal. [VS Code download](https://code.visualstudio.com/download) is optional.

On macOS/Linux, open Terminal. Run `python3.12 --version` and `git --version`. If missing, use the OS package manager or [Python downloads](https://www.python.org/downloads/) for Python 3.12 and [Git downloads](https://git-scm.com/downloads) for Git. Some Linux distributions package the matching Python venv component separately. If your device blocks installs, start with the navigator route in the Day 1 exercise.

## 2. Start a fresh repository of your own

Your trainer supplies the **template URL** in chat. Open it while signed in, choose **Use this template → Create a new repository**, choose **your own account**, name it **taskflow-lab**, select a visibility permitted by your course and create it. The new repository starts with its own history. On **your** repository choose **Code → HTTPS** and copy the URL. Edit the one placeholder below to your own username before running the command.

```text
git clone https://github.com/YOUR-USERNAME/taskflow-lab.git
cd taskflow-lab
git remote -v
```

Both origin lines should show your account and `taskflow-lab`. If they show the trainer's account, return to the template step. In the project folder, run `code .` or open VS Code, choose **File → Open Folder** and select the folder containing `README.md`, `app` and `requirements.txt`. **Terminal → New Terminal** opens a terminal there.

**ZIP or offline route.** Use **Code → Download ZIP** on the starter, or obtain the learner ZIP from the trainer. Extract all files. The supplied ZIP has a folder called `taskflow-starter`; GitHub usually adds `-main`. Open the inner folder containing `requirements.txt`. A ZIP has no Git history. In this extracted project run the following once. If prompted for a name and email, see section 7.

```text
git init -b main
git add .
git commit -m "Start TaskFlow from the class starter"
```

You can work and commit locally. When you have GitHub access, create an **empty** repository called `taskflow-lab` in your own account, then run these commands from that same folder. If you already created a repository from the template, clone it separately and copy only your edited source/test files into a feature branch there.

```text
git remote add origin https://github.com/YOUR-USERNAME/taskflow-lab.git
git push -u origin main
```

## 3. Create an isolated Python environment

In **Windows PowerShell**, run the following in the folder containing `requirements.txt`. A virtual environment is a project-specific Python installation that keeps its packages together. The final command should print a path inside `.venv`.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -c "import sys; print(sys.executable)"
python -m pip install -r requirements.txt
```

If PowerShell blocks the activation script, use the environment's interpreter directly below. You do not need to change the computer's security settings. For every later command that starts with `python`, substitute `.\.venv\Scripts\python.exe`.

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

On **macOS/Linux**:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## 4. Run the API and make your first requests

In your activated terminal (**A**) run:

```text
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Look for `Application startup complete` and the local address. Leave A running. Open [health](http://127.0.0.1:8000/health) in your browser. Before you edit the code you should see `{"status":"ok"}`. Open [interactive API docs](http://127.0.0.1:8000/docs). On a new database, **GET /tasks → Try it out → Execute** returns `[]`. Under **POST /tasks**, choose **Try it out**, replace the request body with `{"title":"Book van service"}` and execute it. Expect HTTP **201**, a numeric `id` and your title. Execute **GET /tasks** again to find that id. Repeating POST creates another task.

**Terminal alternative if the docs page cannot load.** Open a second PowerShell terminal (**B**) and use the following. GET reads the list. POST sends a new task. The first line prints the health response as compact JSON.

```powershell
$base = 'http://127.0.0.1:8000'
Invoke-RestMethod "$base/health" | ConvertTo-Json -Compress
Invoke-RestMethod "$base/tasks" -Method Post -ContentType 'application/json' -Body '{"title":"Book van service"}'
Invoke-RestMethod "$base/tasks"
```

On macOS/Linux:

```bash
curl -i http://127.0.0.1:8000/health
curl -i -X POST http://127.0.0.1:8000/tasks -H 'Content-Type: application/json' -d '{"title":"Book van service"}'
curl -i http://127.0.0.1:8000/tasks
```

Use Ctrl+C in A to stop the server. Restart it from the same folder and GET the list again. Your task survives because it is stored in `data/taskflow.db` on disk. After editing Python code, stop and restart A to load the change.

## 5. Run the starter tests

In B, check you are in the project folder and activate the environment **in this terminal too**. On Windows run `.\.venv\Scripts\Activate.ps1`; on macOS/Linux run `source .venv/bin/activate`. Then run:

```text
python -m pytest -q
```

Expected on the untouched starter: **2 passed**. The tests start their own in-process API with a temporary database. They work even if A is stopped. To run the same tests using the standard-library test runner, use `python -m unittest discover -s tests -v` after installing the application and test-client dependencies. Two passing tests, a 200 health response, and a saved task visible after restart are your setup checks.

## 6. Make and record your first change

Open [exercises/day01.md](exercises/day01.md). Before the afternoon code change, create a feature branch. A branch lets you work on a change before proposing it for your main version.

```text
git switch -c feature/health-service
git status -sb
```

Complete the exercise, rerun the tests, then review, stage and commit only your intended changes. A commit records a local snapshot. A push sends the branch to your own repository.

```text
git diff
git add app/main.py tests/test_api.py
git diff --staged
git commit -m "Identify TaskFlow in the health response"
git log -1 --oneline
git remote -v
git push -u origin feature/health-service
```

If offline, keep the local commit and save its short hash. On GitHub, you may open a pull request from your feature branch into **your own** main and share the link or paste a redacted diff. The same branch will be available on Tuesday.

## 7. When something goes wrong

| Symptom | What to try |
| --- | --- |
| Git asks who you are | Set a repository-local identity with `git config user.name "Your Name"` and `git config user.email "YOUR-GITHUB-NOREPLY-EMAIL"`. Substitute your own GitHub-provided no-reply address from account email settings, then repeat the commit. |
| File requirements.txt is missing / cannot import app | Enter the extracted or cloned folder containing README.md, requirements.txt and app. Use `Get-Location` and `Get-ChildItem` (macOS/Linux: `pwd` and `ls`). |
| No module named fastapi, uvicorn, httpx2 or pytest | Check `python -c "import sys; print(sys.executable)"`. Activate the project environment in this terminal or invoke its Python directly. Re-run `python -m pip install -r requirements.txt`. |
| Address already in use | Stop your own previous server with Ctrl+C, or change the start command to `--port 8001` and use 8001 in every URL. |
| Connection refused / wrong response after an edit | Read terminal A. Check the host and port, save the file, then stop and restart your own server. |
| 404 / 405 / 422 | Check the exact route, then the HTTP method, then the JSON body. POST /tasks needs a title of 1–100 characters after trimming whitespace. OpenAPI lists the accepted request. |
| Package downloads blocked / no GitHub access | Use an approved network or the trainer's local copy. Take the navigator role now and record exactly which personal setup check is pending. |
| Branch already exists | Use `git switch feature/health-service` to resume it. If push is rejected, check `git remote -v` and your signed-in account. |
| /docs is blank | Its interactive interface loads browser assets. Use the local PowerShell or curl commands in section 4. |
| SQLite cannot open the file | Run from a writable project folder. A custom database path must point to a writable location. |

The optional configuration template is [.env.example](.env.example). The application reads the **shell environment**. To change the database path before launching the server, run `$env:TASKFLOW_DB = 'data/another.db'` in PowerShell or `export TASKFLOW_DB='data/another.db'` on macOS/Linux. The default needs no setup.

[Read the project architecture](docs/architecture.md) · [Start the Day 1 exercises](exercises/day01.md)

## 8. Day 2

Continue in this repository. You will test the booking title limit, run the check on a pull request and show how you diagnosed and repaired a failed run.

Open the [Day 2 exercises](exercises/day02.md) and record your results in the [Day 2 evidence sheet](exercises/day02-evidence.md). Exercise C uses the [CI workflow scaffold](docs/ci-workflow-starter.yml).

If the Day 2 files are already in your working copy, go straight to exercise A. If you still need the update, check `git status -sb` first and save and commit your Day 1 work on its current branch.

- **You cloned the trainer’s repo directly.** On the branch tracking the trainer’s published branch, run `git pull --ff-only`. If your Day 1 changes are on a separate branch, start from that branch and use the single-commit route below.
- **You used “Use this template” to create your own repo.** From the branch holding your Day 1 work, run `git switch -c ci/day02-checks`, or `git switch ci/day02-checks` if the branch already exists. Use the trainer’s repository URL and the hash of the Day 2 materials commit in these commands:

  ```text
  git fetch TRAINER_REPO_URL HEAD
  git cherry-pick DAY2_COMMIT
  ```

  If the trainer published to a different branch, replace `HEAD` with its name. This brings the Day 2 changes into your own history. If Git flags a conflict, use `git cherry-pick --abort` to return to your starting point and compare the conflicting file with the trainer. An offline learner can obtain the same files from the Day 2 learner ZIP.
