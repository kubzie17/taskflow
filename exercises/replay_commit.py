"""Run the TaskFlow install and tests in a fresh copy of one local Git revision."""
import argparse
import os
import re
import subprocess
import sys
import tempfile
import venv
import zipfile
from pathlib import Path


def git_text(*args):
    result = subprocess.run(
        ["git", *args], text=True, stdout=subprocess.PIPE, check=True
    )
    return result.stdout.strip()


def replay(revision, wheelhouse):
    if sys.version_info[:2] != (3, 12):
        raise ValueError("Start this helper with Python 3.12, matching the course runner.")
    if wheelhouse is not None and not wheelhouse.is_dir():
        raise ValueError("The wheelhouse must be an existing folder for this OS and Python.")
    root = Path(git_text("rev-parse", "--show-toplevel"))
    sha = git_text("-C", str(root), "rev-parse", "--verify", "--end-of-options",
                   revision + "^{commit}")
    if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", sha):
        raise ValueError("Git did not resolve the requested commit.")
    print(f"CLEAN LOCAL REPLAY | source commit {sha}", flush=True)
    with tempfile.TemporaryDirectory(prefix="taskflow-day2-") as scratch:
        work = Path(scratch)
        archive = work / "source.zip"
        subprocess.run(["git", "-C", str(root), "archive", "--format=zip",
                        "--output", str(archive), sha], check=True)
        checkout = work / "source"
        with zipfile.ZipFile(archive) as zf:
            zf.extractall(checkout)
        if not (checkout / "requirements.txt").is_file():
            raise ValueError("This commit has no requirements.txt at the repository root.")
        virtualenv = work / "venv"
        venv.EnvBuilder(with_pip=True).create(virtualenv)
        python = virtualenv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        env = os.environ.copy()
        for key in ("PYTHONHOME", "PYTHONPATH", "PYTEST_ADDOPTS", "PYTEST_PLUGINS",
                    "TASKFLOW_DB", "PIP_TARGET", "PIP_PREFIX", "PIP_USER"):
            env.pop(key, None)
        env["VIRTUAL_ENV"] = str(virtualenv)
        env["PATH"] = str(python.parent) + os.pathsep + env.get("PATH", "")
        env["PIP_DISABLE_PIP_VERSION_CHECK"] = "1"
        install = [str(python), "-m", "pip", "install", "-r", "requirements.txt"]
        if wheelhouse is not None:
            install.extend(["--no-index", "--find-links", str(wheelhouse)])
        print("STEP | Install dependencies", flush=True)
        installed = subprocess.run(install, cwd=checkout, env=env)
        if installed.returncode:
            return installed.returncode
        print("STEP | Run tests", flush=True)
        return subprocess.run([str(python), "-m", "pytest", "-q"],
                              cwd=checkout, env=env).returncode


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("revision", nargs="?", default="HEAD")
    parser.add_argument("--wheelhouse", type=Path,
                        help="Use only wheels in this approved platform-specific directory.")
    args = parser.parse_args()
    try:
        status = replay(args.revision, args.wheelhouse.resolve() if args.wheelhouse else None)
    except (OSError, subprocess.CalledProcessError, ValueError, zipfile.BadZipFile) as err:
        print(f"Replay could not start or finish: {err}", file=sys.stderr)
        status = 2
    raise SystemExit(status)
