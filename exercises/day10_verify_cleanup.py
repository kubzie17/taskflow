"""READ ONLY: verify exact resources in a reviewed private cleanup inventory."""
import argparse
from datetime import datetime, timezone
import json
import re
import subprocess
from pathlib import Path


class QueryError(Exception):
    def __init__(self, code):
        self.code = code


def aws(region, *args):
    result = subprocess.run(["aws", *args, "--region", region, "--output", "json", "--no-cli-pager"],
                            capture_output=True, text=True, timeout=45)
    if result.returncode:
        m = re.search(r"\(([^)]+)\)", result.stderr)
        raise QueryError(m[1] if m else "UnclassifiedCLIError")
    try:
        return json.loads(result.stdout)
    except ValueError:
        raise QueryError("InvalidJSON") from None


NOT_FOUND = {
    "instance": "InvalidInstanceID.NotFound", "volume": "InvalidVolume.NotFound",
    "security_group": "InvalidGroup.NotFound", "ecr": "RepositoryNotFoundException",
    "ssm_document": "InvalidDocument", "iam_role": "NoSuchEntity",
    "instance_profile": "NoSuchEntity", "iam_policy": "NoSuchEntity",
    "vpc": "InvalidVpcID.NotFound", "subnet": "InvalidSubnetID.NotFound",
    "internet_gateway": "InvalidInternetGatewayID.NotFound", "route_table": "InvalidRouteTableID.NotFound",
    "elastic_ip": "InvalidAllocationID.NotFound", "nat_gateway": "NatGatewayNotFound",
}
TYPES = set(NOT_FOUND) | {"parameter", "log_group", "alarm"}


def check_resource(region, resource):
    kind, identity = resource["type"], resource["id"]
    try:
        if kind == "instance":
            result = aws(region, "ec2", "describe-instances", "--instance-ids", identity)
            nodes = [i for r in result.get("Reservations", []) for i in r["Instances"]]
            if not nodes:
                return "Unknown", "Instance omitted; check identity and account"
            states = [i["State"]["Name"] for i in nodes]
            return ("Removed" if states == ["terminated"] else "Remaining"), ", ".join(states)
        if kind in {"volume", "security_group", "vpc", "subnet", "internet_gateway", "route_table", "elastic_ip", "nat_gateway"}:
            operation, option, key = {
                "volume": ("describe-volumes", "--volume-ids", "Volumes"),
                "security_group": ("describe-security-groups", "--group-ids", "SecurityGroups"),
                "vpc": ("describe-vpcs", "--vpc-ids", "Vpcs"),
                "subnet": ("describe-subnets", "--subnet-ids", "Subnets"),
                "internet_gateway": ("describe-internet-gateways", "--internet-gateway-ids", "InternetGateways"),
                "route_table": ("describe-route-tables", "--route-table-ids", "RouteTables"),
                "elastic_ip": ("describe-addresses", "--allocation-ids", "Addresses"),
                "nat_gateway": ("describe-nat-gateways", "--nat-gateway-ids", "NatGateways"),
            }[kind]
            rows = aws(region, "ec2", operation, option, identity).get(key, [])
            if kind == "nat_gateway" and rows and rows[0].get("State") == "deleted":
                return "Removed", "NAT gateway state deleted; check its Elastic IP separately"
            return ("Remaining", "Resource still returned") if rows else ("Unknown", "Empty ID lookup; inspect Console")
        if kind == "ecr":
            aws(region, "ecr", "describe-repositories", "--repository-names", identity)
        elif kind == "ssm_document":
            aws(region, "ssm", "describe-document", "--name", identity)
        elif kind == "iam_role":
            aws(region, "iam", "get-role", "--role-name", identity)
        elif kind == "instance_profile":
            aws(region, "iam", "get-instance-profile", "--instance-profile-name", identity)
        elif kind == "iam_policy":
            aws(region, "iam", "get-policy", "--policy-arn", identity)
        elif kind == "parameter":
            rows = aws(region, "ssm", "describe-parameters", "--parameter-filters", "Key=Name,Option=Equals,Values="+identity).get("Parameters", [])
            if not any(r["Name"] == identity for r in rows):
                return "Removed", "No exact parameter returned by metadata query"
        elif kind == "log_group":
            rows = aws(region, "logs", "describe-log-groups", "--log-group-name-prefix", identity).get("logGroups", [])
            if not any(r["logGroupName"] == identity for r in rows):
                return "Removed", "No exact log group returned"
        elif kind == "alarm":
            result = aws(region, "cloudwatch", "describe-alarms", "--alarm-names", identity)
            if not result.get("MetricAlarms") and not result.get("CompositeAlarms"):
                return "Removed", "No exact alarm returned"
        return "Remaining", "Resource still returned"
    except QueryError as error:
        if error.code == NOT_FOUND.get(kind):
            return "Removed", error.code
        return "Unknown", error.code
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        return "Unknown", type(error).__name__


def verify(inventory):
    account, region = inventory.get("account", ""), inventory.get("region", "")
    if not re.fullmatch(r"[0-9]{12}", account) or not re.fullmatch(r"[a-z]{2}-[a-z]+-[0-9]", region):
        raise ValueError("Supply the approved account and actual Region")
    resources = inventory.get("resources")
    if not isinstance(resources, list) or not resources:
        raise ValueError("Inventory must list the actual owned resources")
    for r in resources:
        if r.get("type") not in TYPES or not re.fullmatch(r"[A-Za-z0-9/][A-Za-z0-9/_.:@+=-]*", r.get("id", "")) or not r.get("owner"):
            raise ValueError("Each resource needs a supported type, exact identifier and named owner")
    caller = aws(region, "sts", "get-caller-identity")
    if caller["Account"] != account:
        raise ValueError("Wrong AWS account; no resource checks performed")
    results = []
    for r in resources:
        status, detail = check_resource(region, r)
        results.append({**r, "observed_status": status, "verification": detail})
    return {"checked_utc": datetime.now(timezone.utc).isoformat(), "account": account, "region": region,
            "scope": "Only the exact listed resources. Reconcile the complete course ledger separately.",
            "all_listed_resources_removed": all(r["observed_status"] == "Removed" for r in results), "resources": results}


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("inventory", type=Path)
    a = p.parse_args()
    try:
        result = verify(json.loads(a.inventory.read_text(encoding="utf-8-sig")))
        print(json.dumps(result, indent=2))
        raise SystemExit(0 if result["all_listed_resources_removed"] else 2)
    except (OSError, ValueError, KeyError, QueryError, subprocess.SubprocessError) as error:
        raise SystemExit("Cleanup verification could not complete: " + (error.code if isinstance(error, QueryError) else str(error))) from None
