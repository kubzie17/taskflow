"""Day 7 loopback workbench. Run from the course root with python -m exercises.day07_lab."""
import argparse
from contextlib import closing
from datetime import datetime, timezone
import getpass
import hashlib
import http.client
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import re
import secrets
import sqlite3
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1] / "data" / "day07-lab"
TARGET = ROOT / "upstream-port.txt"
PATHS = {"GET": {"/health", "/tasks", "/support/status"}, "POST": {"/tasks", "/session"}}
PORTS = (8071, 8072, 8073)


def label(text):
    if not re.fullmatch(r"[a-z][a-z0-9-]{0,27}", text):
        raise argparse.ArgumentTypeError("Choose 1–28 lower-case letters, digits or hyphens, starting with a letter.")
    return text


def db_path(name):
    return ROOT / "stores" / name / "tasks.db"


def open_readonly(path):
    return sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True, timeout=5)


def point(port):
    ROOT.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", dir=ROOT, delete=False) as tmp:
        tmp.write(str(port))
    os.replace(tmp.name, TARGET)
    print(f"Gateway now targets 127.0.0.1:{port}.")


def upstream():
    port = int(TARGET.read_text()) if TARGET.exists() else 8071
    if port not in PORTS:
        raise ValueError("Invalid lab upstream")
    return port


def transfer_snapshot(source, folder):
    # Reserve a new destination; the final name becomes visible only after SQLite completes its copy.
    with closing(open_readonly(source)) as origin:
        origin.execute("SELECT id, title FROM tasks LIMIT 1")
        folder.parent.mkdir(parents=True, exist_ok=True)
        folder.mkdir()
        stage = folder / "writing.tmp"
        try:
            with closing(sqlite3.connect(stage)) as dest:
                origin.backup(dest)
                if dest.execute("PRAGMA quick_check").fetchone() != ("ok",):
                    raise ValueError("SQLite integrity check failed.")
            os.replace(stage, folder / "tasks.db")
        except BaseException:
            stage.unlink(missing_ok=True)
            try:
                folder.rmdir()
            except OSError:
                pass
            raise
    print("Consistent SQLite copy:", (folder / "tasks.db").relative_to(ROOT))


class Gateway(BaseHTTPRequestHandler):
    # Forward only known classroom routes to loopback. Never log credentials or response bodies.
    def log_message(self, *unused):
        pass

    def reply(self, code, data, auth=None):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(data)))
        if auth:
            self.send_header("WWW-Authenticate", "Bearer")
        self.end_headers()
        self.wfile.write(data)

    def forward(self):
        if self.path not in PATHS.get(self.command, set()):
            return self.reply(404, b'{"detail":"Unknown workshop route"}')
        try:
            size = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            return self.reply(400, b'{"detail":"Invalid body length"}')
        if not 0 <= size <= 16384 or self.headers.get("Transfer-Encoding"):
            return self.reply(413, b'{"detail":"Unsupported body"}')
        body = self.rfile.read(size) if size else None
        headers = {key: self.headers[key] for key in ("Content-Type", "Authorization") if key in self.headers}
        try:
            with closing(http.client.HTTPConnection("127.0.0.1", upstream(), timeout=5)) as conn:
                conn.request(self.command, self.path, body=body, headers=headers)
                result = conn.getresponse()
                code, data, auth = result.status, result.read(), result.getheader("WWW-Authenticate")
        except (OSError, ValueError, http.client.HTTPException):
            return self.reply(502, b'{"detail":"Workshop gateway could not reach the selected upstream"}')
        self.reply(code, data, auth)

    do_GET = forward
    do_POST = forward


def request(port, method, path, body=None, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = "Bearer " + token
    encoded = json.dumps(body).encode() if body is not None else None
    with closing(http.client.HTTPConnection("127.0.0.1", port, timeout=6)) as conn:
        conn.request(method, path, body=encoded, headers=headers)
        result = conn.getresponse()
        return result.status, json.loads(result.read())


def call(args):
    token = None
    if args.role != "visitor":
        password = getpass.getpass("Fictional Friday passphrase (hidden): ")
        status, data = request(args.port, "POST", "/session", {"username": args.role, "password": password})
        if status != 200:
            print("Sign-in HTTP", status, "(no token displayed)")
            return 1
        token = data["access_token"]
    method, path = {"health": ("GET","/health"), "list": ("GET","/tasks"), "book": ("POST","/tasks")}[args.operation]
    payload = {"title": args.title} if args.operation == "book" else None
    status, data = request(args.port, method, path, payload, token)
    print("HTTP", status, json.dumps(data, ensure_ascii=True))
    return 0 if status < 400 else 1


def manifest(team):
    folder = ROOT / "evidence"
    folder.mkdir(parents=True, exist_ok=True)
    name = team + "-" + secrets.token_hex(6) + ".txt"
    path = folder / name
    body = (f"TaskFlow workshop manifest\nteam={team}\nrun={name[:-4]}\n"
            f"utc={datetime.now(timezone.utc).isoformat()}\nclassification=fictional\n").encode()
    with path.open("xb") as handle:
        handle.write(body)
    print("FILE", path)
    print("SHA256", hashlib.sha256(body).hexdigest(), "| bytes", len(body))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="cmd", required=True)
    api = commands.add_parser("api")
    api.add_argument("--mode", choices=("protected","historical"), default="protected")
    api.add_argument("--store", type=label, default="primary")
    commands.add_parser("gateway")
    commands.add_parser("point").add_argument("port", type=int, choices=PORTS)
    client = commands.add_parser("call")
    client.add_argument("operation", choices=("health","list","book"))
    client.add_argument("--as", dest="role", choices=("visitor","reader","dispatcher"), default="visitor")
    client.add_argument("--title", default="Fictional inspection")
    client.add_argument("--port", type=int, choices=(8070,8071,8073), default=8070)
    commands.add_parser("rows").add_argument("--store", type=label, default="primary")
    for operation in ("backup","restore"):
        entry = commands.add_parser(operation)
        entry.add_argument("name", type=label)
        entry.add_argument("--store", type=label, required=operation == "restore", default="primary")
    commands.add_parser("manifest").add_argument("team", type=label)
    args = parser.parse_args()
    if args.cmd == "api":
        import uvicorn
        if args.mode == "protected":
            from exercises.day05_api import create_secure as factory
        else:
            from app.main import create_app as factory
        path = db_path(args.store)
        api_app = factory(db_path=path)
        print("Entry point", factory.__module__ + ":" + factory.__name__, "| database", path, flush=True)
        uvicorn.run(api_app, host="127.0.0.1", port=8071, access_log=False)
    elif args.cmd == "gateway":
        with ThreadingHTTPServer(("127.0.0.1",8070), Gateway) as server:
            print("Gateway http://127.0.0.1:8070/health | target", upstream(), flush=True)
            server.serve_forever()
    elif args.cmd == "point":
        point(args.port)
    elif args.cmd == "call":
        return call(args)
    elif args.cmd == "rows":
        with closing(open_readonly(db_path(args.store))) as db:
            print(json.dumps(db.execute("SELECT id,title FROM tasks ORDER BY id").fetchall()))
    elif args.cmd == "backup":
        transfer_snapshot(db_path(args.store), ROOT / "backups" / args.name)
    elif args.cmd == "restore":
        transfer_snapshot(ROOT / "backups" / args.name / "tasks.db", db_path(args.store).parent)
    else:
        manifest(args.team)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
    except (OSError, ValueError, RuntimeError, sqlite3.Error, http.client.HTTPException) as exc:
        raise SystemExit(f"Lab operation stopped: {exc}")
