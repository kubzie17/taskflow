"""Capture actual local observations; optionally upload one sanitized CloudWatch event."""
import argparse
from datetime import datetime, timezone
import json
import os
import re
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path


def run(*args):
    return subprocess.run(args, check=True, capture_output=True, text=True, timeout=30).stdout


def lifecycle_lines(raw):
    # Full-line allow-list excludes request bodies, credentials and arbitrary log text.
    pattern = r"^(\S+)\s+INFO:\s+(Application startup complete\.|Application shutdown complete\.|Shutting down|Started server process \[[0-9]+\]|Finished server process \[[0-9]+\])$"
    result = []
    for line in raw.splitlines():
        m = re.fullmatch(pattern, line)
        if m:
            result.append({"docker_timestamp": m[1], "message": m[2]})
    return result[-12:]


def capture(container, port, phase):
    inspected = json.loads(run("docker", "inspect", container))[0]
    started = time.monotonic()
    status, health_ok = None, False
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=3) as r:
            body = json.load(r)
            status = r.status
            health_ok = status == 200 and isinstance(body, dict) and body.get("service") == "taskflow" and body.get("status") == "ok"
    except urllib.error.HTTPError as e:
        status = e.code
    except (OSError, ValueError):
        pass
    probe_ms = round((time.monotonic()-started)*1000, 1)
    logs = subprocess.run(["docker", "logs", "--timestamps", "--since", "15m", "--tail", "80", container],
                          capture_output=True, text=True, timeout=15)
    return {"captured_utc": datetime.now(timezone.utc).isoformat(), "phase": phase,
            "collection": "manual_snapshot", "container": container,
            "container_status": inspected["State"]["Status"], "image": inspected["Config"]["Image"],
            "protected_factory_configured": "exercises.day09_entry:application" in (inspected["Config"].get("Cmd") or []),
            "health_http_status": status, "application_healthy": health_ok,
            "probe_ms": probe_ms,
            "authorisation": "verify_separately_with_day09_probe",
            "lifecycle": lifecycle_lines(logs.stdout + logs.stderr)}


def upload(observation, account, region, group, stream):
    if not re.fullmatch(r"[0-9]{12}", account or "") or not re.fullmatch(r"[a-z]{2}-[a-z]+-[0-9]", region or ""):
        raise ValueError("Supply the approved account and actual Region")
    if not re.fullmatch(r"/taskflow/[a-z0-9-]+/day10", group or "") or not re.fullmatch(r"i-(?:[0-9a-f]{8}|[0-9a-f]{17})", stream or ""):
        raise ValueError("Use the team log group and original instance ID as stream")
    caller = json.loads(run("aws", "sts", "get-caller-identity", "--region", region, "--output", "json", "--no-cli-pager"))
    if caller["Account"] != account:
        raise ValueError("Unexpected AWS account")
    events = [{"timestamp": int(time.time()*1000), "message": json.dumps(observation, separators=(",", ":"))}]
    fd, filename = tempfile.mkstemp(prefix="taskflow-observation-", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(events, f)
        response = json.loads(run("aws", "logs", "put-log-events", "--log-group-name", group,
            "--log-stream-name", stream, "--log-events", "file://" + filename, "--region", region,
            "--output", "json", "--no-cli-pager"))
        if response.get("rejectedLogEventsInfo"):
            raise ValueError("CloudWatch rejected an event; inspect time and retention")
    finally:
        Path(filename).unlink(missing_ok=True)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--container", default="taskflow", choices=["taskflow", "taskflow-day09-local", "taskflow-recovery"])
    p.add_argument("--port", type=int, choices=[8055, 8056, 18055, 18056], default=8055)
    p.add_argument("--phase", choices=["baseline", "fault", "recovered"], required=True)
    p.add_argument("--upload", action="store_true")
    for name in ("account", "region", "group", "stream"):
        p.add_argument("--"+name)
    a = p.parse_args()
    try:
        result = capture(a.container, a.port, a.phase)
        print(json.dumps(result, indent=2))
        if a.upload:
            upload(result, a.account, a.region, a.group, a.stream)
            print("CloudWatch accepted this snapshot. Open the actual stream to verify it.")
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        raise SystemExit("Observation stopped. Check Docker, target, AWS identity, log permission and clock. " + type(error).__name__) from None


if __name__ == "__main__":
    main()
