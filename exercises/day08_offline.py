"""Last-resort local change rehearsal for a team without the Terraform executable."""
import argparse
import json
from pathlib import Path
import os
import secrets
import sys
import tempfile

DEFAULT = Path(__file__).resolve().parents[1] / "data" / "day08-offline"
STAGES = ("foundation", "deploy-ready")


def read(path):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def write(path, value):
    with tempfile.NamedTemporaryFile("w", dir=path.parent, encoding="utf-8", delete=False) as f:
        json.dump(value, f, indent=2)
        name = f.name
    os.replace(name, path)


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--directory", type=Path, default=DEFAULT)
    actions = cli.add_subparsers(dest="action", required=True)
    actions.add_parser("plan").add_argument("stage", choices=STAGES)
    for name in ("apply", "show", "destroy"):
        actions.add_parser(name)
    args = cli.parse_args()
    directory = args.directory
    directory.mkdir(parents=True, exist_ok=True)
    state, plan = directory / "simulated-state.json", directory / "simulated-plan.json"
    old = read(state)
    if args.action == "plan":
        action = "create" if old is None else ("no change" if old["stage"] == args.stage else "update in place")
        write(plan, {"prior": old, "desired": args.stage})
        print(f"LOCAL SIMULATION: {action}; desired stage {args.stage}")
    elif args.action == "apply":
        change = read(plan)
        if change is None or change["prior"] != old:
            sys.exit("Missing or stale local plan. Plan again.")
        if change["desired"] not in STAGES:
            sys.exit("Invalid stage in the local plan.")
        write(state, {"id": old["id"] if old else "sim-" + secrets.token_hex(4), "stage": change["desired"]})
        plan.unlink()
        print("Applied locally:", read(state))
    elif args.action == "show":
        print("LOCAL SIMULATION:", json.dumps(old))
    else:
        state.unlink(missing_ok=True)
        plan.unlink(missing_ok=True)
        print("Removed only the two local simulation records.")


if __name__ == "__main__":
    main()
