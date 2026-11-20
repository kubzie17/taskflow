"""Create or inspect fictional TaskFlow bookings through a local/SSM endpoint."""
import argparse
from datetime import datetime, timezone
import getpass
import json
import urllib.error
import urllib.parse
import urllib.request


def request(base, path, token=None, data=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request(base + path, data=None if data is None else json.dumps(data).encode(), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        raise ValueError(f"Request rejected with HTTP {e.code}") from None


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("operation", choices=["create", "list"])
    p.add_argument("--url", default="http://127.0.0.1:8055")
    p.add_argument("--label", choices=["A", "B"])
    p.add_argument("--role", choices=["reader", "dispatcher"], default="dispatcher")
    a = p.parse_args()
    base = a.url.rstrip("/")
    u = urllib.parse.urlsplit(base)
    if u.scheme != "http" or u.hostname != "127.0.0.1" or u.path or u.query or u.fragment or u.username:
        p.error("Use the loopback HTTP endpoint of the approved tunnel or local pilot")
    if a.operation == "create" and (a.role != "dispatcher" or not a.label):
        p.error("Creation requires dispatcher and --label A or B")
    password = getpass.getpass("Fictional " + a.role + " phrase: ")
    try:
        _, session = request(base, "/session", data={"username": a.role, "password": password})
        token = session["access_token"]
        if a.operation == "create":
            status, result = request(base, "/tasks", token,
                {"title": "Day 10 booking " + a.label + " " + datetime.now(timezone.utc).strftime("%H:%M:%S")})
            if status != 201:
                raise ValueError("Expected HTTP 201")
        else:
            status, result = request(base, "/tasks", token)
            if status != 200:
                raise ValueError("Expected HTTP 200")
        print(json.dumps({"observed_utc": datetime.now(timezone.utc).isoformat(), "status": status, "result": result}, indent=2))
    except (OSError, ValueError, KeyError) as error:
        raise SystemExit("Booking check stopped: " + str(error)) from None


if __name__ == "__main__":
    main()
