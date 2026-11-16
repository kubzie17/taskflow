"""Review the shape of a simple TaskFlow Actions workflow. Optional dev dependency: PyYAML 6.0.3."""
import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    raise SystemExit("YAML check unavailable. Use an approved PyYAML 6.0.3 install, actionlint or the manual W4 review.")


class UniqueLoader(yaml.BaseLoader):
    # BaseLoader keeps GitHub's 'on' keyword as a string. Reject duplicate mapping keys.
    def construct_mapping(self, node, deep=False):
        mapping = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, str) or key in mapping:
                raise ValueError("Duplicate or non-scalar YAML key")
            mapping[key] = self.construct_object(value_node, deep=deep)
        return mapping


def as_names(value):
    if isinstance(value, str):
        return {value}
    if isinstance(value, (list, dict)):
        return set(value)
    return set()


def inspect(doc, ids):
    issues = []
    if not isinstance(doc, dict) or not isinstance(doc.get("jobs"), dict):
        return ["Missing workflow jobs mapping"]
    events = as_names(doc.get("on"))
    if "pull_request" not in events or events - {"pull_request", "push", "workflow_dispatch"}:
        issues.append("Check event trust and the permitted PR trigger")
    jobs = doc["jobs"]
    audit, test, package = ids
    for name in ids:
        job = jobs.get(name)
        if not isinstance(job, dict):
            issues.append("Expected job missing: " + name)
            continue
        permissions = job.get("permissions", doc.get("permissions"))
        if permissions != {"contents": "read"}:
            issues.append(name + ": review effective token permissions for checkout")
        if "if" in job or job.get("continue-on-error", "false") != "false":
            issues.append(name + ": inspect branches that could skip or suppress a mandatory check")
        steps = job.get("steps", [])
        if not isinstance(steps, list) or not all(isinstance(s, dict) for s in steps):
            issues.append(name + ": missing or unsupported steps")
            continue
        for step in steps:
            if step.get("continue-on-error", "false") != "false":
                issues.append(name + ": step can hide failure")
            if "if" in step:
                issues.append(name + ": conditional step needs separate review")
            action = step.get("uses", "")
            if action.startswith("actions/checkout@") and step.get("with", {}).get("persist-credentials") != "false":
                issues.append(name + ": checkout retains credentials")
            if action and not re.fullmatch(r"[\w./-]+@[0-9a-fA-F]{40}", action):
                issues.append(name + ": verify the action publisher and pin the reviewed commit")
        runs = "\n".join(str(s.get("run", "")) for s in steps)
        if name == audit and ("day06_gate.py check" not in runs or "day06-proposal.case" in runs):
            issues.append(name + ": inspect which requirements input actually gates this job")
        if name == test and ("pytest" not in runs or "day05-requirements.txt" not in runs):
            issues.append(name + ": review test scope and dependency setup")
        if name == package and ("docker build" not in runs or re.search(r"\b(?:push|login)\b",runs)):
            issues.append(name + ": verify a build with no publishing")
    if isinstance(jobs.get(test), dict) and audit not in as_names(jobs[test].get("needs")):
        issues.append("Check the order of dependency approval and test installation")
    if isinstance(jobs.get(package), dict) and not {test, audit}.issubset(as_names(jobs[package].get("needs"))):
        issues.append("Check the package job's required predecessors")
    # Catch explicit secret expressions across workflow, job and step levels.
    if re.search(r"\bsecrets\s*[.\[]", str(doc), re.IGNORECASE):
        issues.append("A job or workflow references secrets. Inspect the PR trust boundary")
    return issues


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("workflow", type=Path)
    cli.add_argument("--jobs", nargs=3, default=["dependency","test","package"],
                     metavar=("DEPENDENCY", "TEST", "PACKAGE"))
    args = cli.parse_args()
    try:
        document = yaml.load(args.workflow.read_text(encoding="utf-8-sig"), Loader=UniqueLoader)
        issues = inspect(document, args.jobs)
    except (OSError, UnicodeError, ValueError, TypeError, AttributeError, yaml.YAMLError) as exc:
        print("Cannot validate the YAML structure:", type(exc).__name__)
        sys.exit(2)
    for issue in issues:
        print("CHECK:", issue)
    print("Review findings:", len(issues), "| bounded static checks only")
    sys.exit(1 if issues else 0)
