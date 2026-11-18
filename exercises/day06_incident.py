"""Make a fresh LOCAL Git history using only fictional content. No remote or service credentials."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
MARKER = "TRAINING_ONLY_NOT_A_CREDENTIAL"


def git(folder, *args):
    env = {**os.environ, "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull}
    # Keep this disposable repo independent of personal hooks, signing and author identity.
    return subprocess.run(["git", "-c", "user.name=Fictional Lab", "-c", "user.email=lab@example.invalid",
                           "-c", "commit.gpgSign=false", "-c", "core.hooksPath=" + str(folder / "no-hooks"),
                           *args], cwd=folder, env=env, check=True, capture_output=True, text=True)


def create():
    folder = Path(tempfile.mkdtemp(prefix="taskflow-day06-incident-"))
    git(folder, "init", "-q")
    for name in (".gitignore", ".dockerignore"):
        if (ROOT / name).is_file():
            shutil.copyfile(ROOT / name, folder / name)
    (folder / ".env.example").write_text("TASKFLOW_ENV=training\n", encoding="utf-8")
    app = folder / "app"
    app.mkdir()
    (app / "main.py").write_text("# harmless example application\n", encoding="utf-8")
    git(folder, "add", "-f", "--", ".env.example", "app/main.py")
    for name in (".gitignore", ".dockerignore"):
        if (folder / name).is_file():
            git(folder, "add", "-f", "--", name)
    git(folder, "commit", "-qm", "Prepare fictional training project")
    suspect = app / "dispatch.local.env"
    suspect.write_text("DISPATCH_DIAGNOSTIC=" + MARKER + "\n", encoding="utf-8")
    git(folder, "add", "-f", "--", "app/dispatch.local.env")
    git(folder, "commit", "-qm", "Add temporary diagnostic settings")
    git(folder, "rm", "-q", "--", "app/dispatch.local.env")
    git(folder, "commit", "-qm", "Remove diagnostic file from current tree")
    return folder


if __name__ == "__main__":
    print("Disposable incident repository (copy this path into a second terminal):")
    print(create())
