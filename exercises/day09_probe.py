"""Check protected HTTP behaviour without printing passphrases or tokens."""
import argparse
import getpass
import json
import sys
import urllib.error
import urllib.request
import uuid
from pathlib import Path


def request(base, method, path, payload=None, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = "Bearer " + token
    data = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(base.rstrip("/") + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.status, json.load(response)
    except urllib.error.HTTPError as error:
        return error.code, json.loads(error.read())


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def verify(base, passwords, expected_id=None):
    require(request(base, "GET", "/health")[0] == 200, "Health probe failed")
    tokens = {}
    for role in ("reader", "dispatcher"):
        status, body = request(base, "POST", "/session", {"username": role, "password": passwords[role]})
        require(status == 200, role + " sign-in failed")
        tokens[role] = body["access_token"]
    code, original = request(base, "GET", "/tasks", token=tokens["reader"])
    require(code == 200, "Reader could not list tasks")
    require(request(base, "GET", "/tasks")[0] == 401, "Visitor read must return 401")
    for token, expected, label in [(None, 401, "Visitor"), ("invalid.value", 401, "Invalid token"),
                                   (tokens["reader"], 403, "Reader")]:
        code, _ = request(base, "POST", "/tasks", {"title": "Fictional denied booking"}, token)
        require(code == expected, label + " write returned unexpected status")
        status, current = request(base, "GET", "/tasks", token=tokens["reader"])
        require(status == 200 and current == original, label + " denial changed bookings")
    require(request(base, "GET", "/tasks", token=tokens["dispatcher"])[0] == 200,
            "Dispatcher could not list tasks")
    if expected_id is not None:
        require(any(row["id"] == expected_id for row in original), "Expected booking did not survive")
        return {"result": "PASS", "persisted_booking_id": expected_id, "row_count": len(original)}
    title = "Day 9 fictional repair " + uuid.uuid4().hex[:8]
    status, created = request(base, "POST", "/tasks", {"title": title}, tokens["dispatcher"])
    require(status == 201 and created.get("title") == title, "Dispatcher booking creation failed")
    status, current = request(base, "GET", "/tasks", token=tokens["reader"])
    require(status == 200 and current == original + [created], "Expected exactly one new booking")
    return {"result": "PASS", "created_booking_id": created["id"], "row_count": len(current)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:8055")
    parser.add_argument("--expect-booking", type=int)
    parser.add_argument("--credentials-file", type=Path, help="Disposable automated-test input only")
    args = parser.parse_args()
    try:
        passwords = (json.loads(args.credentials_file.read_text()) if args.credentials_file else
                     {role: getpass.getpass("Fictional " + role + " passphrase: ")
                      for role in ("reader", "dispatcher")})
        print(json.dumps(verify(args.url, passwords, args.expect_booking), indent=2))
    except (RuntimeError, OSError, ValueError, KeyError) as error:
        print("Verification failed. Check the service, role, identity version and returned status.")
        # Suppress third-party exception text that might contain input values.
        if isinstance(error, RuntimeError):
            print(str(error))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
