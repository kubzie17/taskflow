"""Offline inbound security-group exercise in one VPC. No AWS calls, routes, IAM, NACL or DNS emulation."""
import argparse
import ipaddress
import json
from pathlib import Path

# Inputs describe observed caller addresses and attached groups in the fictional pilot.
CALLERS = {
    "office": ("203.0.113.18", None), "other-internet": ("198.51.100.9", None),
    "edge": ("10.70.0.15", "sg-edge"), "app": ("10.70.10.15", "sg-app"),
    "other-workload": ("10.70.10.25", "sg-other"),
}
CASES = [
    ("office","sg-edge",443,True), ("other-internet","sg-edge",443,False),
    ("other-internet","sg-app",8000,False), ("office","sg-app",22,False),
    ("edge","sg-app",8000,True), ("other-workload","sg-app",8000,False),
    ("app","sg-db",5432,True), ("other-workload","sg-db",5432,False),
    ("other-internet","sg-db",5432,False),
]


def allows(rules, address, group, port):
    for rule in rules:
        if rule["port"] != port:
            continue
        if "cidr" in rule and ipaddress.ip_address(address) in ipaddress.ip_network(rule["cidr"]):
            return True
        if group is not None and rule.get("source_group") == group:
            return True
    return False


def check(path):
    doc = json.loads(path.read_text(encoding="utf-8-sig"))
    groups = doc["inbound_tcp"]
    for group in {"sg-edge","sg-app","sg-db"}:
        for rule in groups[group]:
            if set(rule) not in ({"port","cidr"},{"port","source_group"}) or type(rule["port"]) is not int:
                raise ValueError("Each supported TCP rule needs an integer port and one cidr or source_group.")
            if "cidr" in rule:
                ipaddress.ip_network(rule["cidr"])
    misses = 0
    for caller, target, port, wanted in CASES:
        actual = allows(groups[target], *CALLERS[caller], port)
        print("OK" if actual == wanted else "REVIEW", caller, "->", target, port, "ALLOW" if actual else "BLOCK")
        misses += actual != wanted
    print("Matched", len(CASES)-misses, "of", len(CASES), "client cases (offline inbound model).")
    return int(bool(misses))


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("inventory", type=Path)
    args = cli.parse_args()
    try:
        raise SystemExit(check(args.inventory))
    except (OSError, ValueError, TypeError, KeyError) as exc:
        raise SystemExit(f"Unable to read this exercise configuration: {exc}")
