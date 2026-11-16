"""Offline Northbridge exercise. Check the Friday identity pin before running untrusted inputs."""
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PIN = ROOT / "exercises/day05-requirements.txt"
DEFAULT_AUTH = "tests/test_day05_access.py"
APPROVED = "2.15.1"


def check_pin(path):
    """This one-package teaching policy deliberately accepts a single reviewed literal pin."""
    try:
        lines = [line.split("#", 1)[0].strip() for line in path.read_text(encoding="utf-8-sig").splitlines()]
    except (OSError, UnicodeError):
        print("REVIEW: cannot read the selected identity requirements file.")
        return 2
    entries = [line for line in lines if line]
    match = re.fullmatch(r"pyjwt\s*==\s*([0-9]+\.[0-9]+\.[0-9]+)", entries[0], re.I) if len(entries) == 1 else None
    if not match:
        print("REVIEW: this lab policy expects one exact PyJWT pin. Check missing, duplicate or changed entries.")
        return 2
    version = match.group(1)
    if version == APPROVED:
        print(f"PASS: PyJWT {version} matches the reviewed class pin.")
        return 0
    if version == "2.13.0":
        print("BLOCK: the proposed 2.13.0 pin is in the archived advisory's affected range.")
        return 1
    print(f"REVIEW: PyJWT {version} is outside the class allow-list. Check the advisory and compatibility.")
    return 2


def rehearse(path, auth_tests, build):
    result = check_pin(path)
    if result:
        print("TESTS SKIPPED | PACKAGE SKIPPED")
        return result
    for target in ([auth_tests], []):
        result = subprocess.run([sys.executable, "-m", "pytest", "-q", *target], cwd=ROOT).returncode
        if result:
            print("TESTS FAILED OR COULD NOT RUN | PACKAGE SKIPPED")
            return result
    if not build:
        print("TESTS PASSED | PACKAGE ELIGIBLE (image build was not run)")
        return 0
    print("TESTS PASSED | running the local Docker build", flush=True)
    try:
        return subprocess.run(["docker", "build", "-t", "taskflow:day06-local", "."], cwd=ROOT).returncode
    except FileNotFoundError:
        print("Docker is unavailable. No image was built.")
        return 2


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["check", "rehearse"])
    parser.add_argument("--pin-file", type=Path, default=DEFAULT_PIN,
                        help="Read a trusted manifest or the inert workshop exhibit as plain text.")
    parser.add_argument("--auth-tests", default=DEFAULT_AUTH, help="Path of your actual Friday test file.")
    parser.add_argument("--build", action="store_true", help="Build the historical image locally after both tests pass.")
    args = parser.parse_args()
    if args.mode == "check":
        raise SystemExit(check_pin(args.pin_file))
    raise SystemExit(rehearse(args.pin_file, args.auth_tests, args.build))
