"""Read TaskFlow's health and confirm that a previously created booking still exists."""

import argparse
import json
import sys
from http.client import HTTPConnection, HTTPException


def read_json(port, path):
    connection = HTTPConnection("127.0.0.1", port, timeout=5)
    try:
        connection.request("GET", path, headers={"Accept": "application/json"})
        response = connection.getresponse()
        if response.status != 200:
            raise ValueError(f"GET {path} returned HTTP {response.status}")
        return json.loads(response.read())
    finally:
        connection.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("booking_id", type=int, help="id returned when the booking was created")
    parser.add_argument("title", help="exact title returned when the booking was created")
    parser.add_argument("--port", type=int, default=8083, help="published loopback port (default 8083)")
    args = parser.parse_args()
    if not 1 <= args.port <= 65535 or args.booking_id < 1:
        parser.error("use a port from 1 to 65535 and a positive booking id")

    try:
        health = read_json(args.port, "/health")
        if not isinstance(health, dict) or health.get("status") != "ok":
            raise ValueError("GET /health returned an unexpected body")
        print("GET /health: HTTP 200, status ok")
        bookings = read_json(args.port, "/tasks")
        if not isinstance(bookings, list):
            raise ValueError("GET /tasks did not return a list")
        for booking in bookings:
            if isinstance(booking, dict) and booking.get("id") == args.booking_id:
                if booking.get("title") != args.title:
                    raise ValueError(f"booking {args.booking_id} has a different title")
                print(f"PASS: booking {args.booking_id} matches {args.title!r}")
                return 0
        raise ValueError(f"booking {args.booking_id} was absent from GET /tasks")
    except (OSError, HTTPException, ValueError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
