"""Exercise the actual built image with disposable identities and storage."""
import argparse
import json
import secrets
import subprocess
import tempfile
import time
import urllib.error
from pathlib import Path

from exercises.day05_identity import make_state
from exercises.day09_probe import request, verify


def run(*args):
    return subprocess.run(args, check=True, text=True, capture_output=True).stdout.strip()


def check_image(image):
    name = "taskflow-ci-" + secrets.token_hex(5)
    passwords = {role: secrets.token_urlsafe(24) for role in ("reader", "dispatcher")}
    with tempfile.TemporaryDirectory(prefix="taskflow-image-") as folder:
        root = Path(folder)
        identity = root / "identity.json"
        identity.write_text(json.dumps(make_state(passwords["reader"], passwords["dispatcher"])))
        identity.chmod(0o444)  # Synthetic CI-only bundle under private temporary parent.
        data = root / "data"
        data.mkdir(mode=0o777)
        data.chmod(0o777)  # Disposable smoke-test data. EC2 uses UID 10001 and mode 0750.
        try:
            run("docker", "run", "-d", "--name", name, "--read-only", "--cap-drop", "ALL",
                "--security-opt", "no-new-privileges", "--tmpfs", "/tmp",
                "-p", "127.0.0.1::8000", "-e", "APP_ENVIRONMENT=ci",
                "-e", "TASKFLOW_DB=/var/lib/taskflow/taskflow.db",
                "-e", "TASKFLOW_IDENTITY_FILE=/run/secrets/identity.json",
                "--mount", f"type=bind,src={identity},dst=/run/secrets/identity.json,readonly",
                "--mount", f"type=bind,src={data},dst=/var/lib/taskflow", image)
            binding = run("docker", "port", name, "8000/tcp").splitlines()[0]
            base = "http://" + binding
            wait_healthy(base)
            proof = verify(base, passwords)
            run("docker", "restart", name)
            wait_healthy(base)
            verify(base, passwords, proof["created_booking_id"])
            print("PASS: built image enforces roles and retains SQLite data across container restart")
        finally:
            subprocess.run(["docker", "rm", "-f", name], capture_output=True)


def wait_healthy(base):
    for _ in range(45):
        try:
            if request(base, "GET", "/health")[0] == 200:
                return
        except (OSError, ValueError):
            pass
        time.sleep(1)
    raise RuntimeError("Image did not become healthy within 45 seconds")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image")
    args = parser.parse_args()
    try:
        check_image(args.image)
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError):
        raise SystemExit("Image verification failed. Packaging/publishing must remain blocked.") from None
