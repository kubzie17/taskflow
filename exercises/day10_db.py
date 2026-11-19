"""Consistent SQLite checkpoints and restores. A target must be a NEW file."""
import argparse
from contextlib import closing
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import time


def utc():
    return datetime.now(timezone.utc).isoformat()


def source_path(value):
    path = Path(value).expanduser()
    if not path.is_absolute():
        raise ValueError("Use an absolute source path")
    path = path.resolve(strict=True)
    if not path.is_file():
        raise ValueError("Source must be an existing database file")
    return path


def connect_readonly(path):
    # mode=ro includes committed WAL contents. Do not use immutable=1 for a live DB.
    return sqlite3.connect(path.as_uri() + "?mode=ro", uri=True, timeout=5)


def inspect_database(value):
    path = source_path(value)
    with closing(connect_readonly(path)) as db:
        integrity = db.execute("PRAGMA quick_check").fetchall()
        if integrity != [("ok",)]:
            raise ValueError("Database integrity check failed")
        rows = db.execute("SELECT id FROM tasks ORDER BY id").fetchall()
        mode = db.execute("PRAGMA journal_mode").fetchone()[0]
    return {"database": str(path), "task_ids": [r[0] for r in rows],
            "count": len(rows), "integrity": "ok", "journal_mode": mode}


def copy_database(source, target, operation="checkpoint"):
    source = source_path(source)
    target = Path(target).expanduser()
    if not target.is_absolute() or not target.parent.is_dir():
        raise ValueError("Target must have an existing absolute parent directory")
    target = target.parent.resolve(strict=True) / target.name
    metadata = Path(str(target) + ".record.json")
    related = [target, metadata] + [Path(str(target) + s) for s in ("-wal", "-shm", "-journal")]
    if source == target or any(os.path.lexists(p) for p in related):
        raise ValueError("Target or its companion file already exists; choose a NEW target")
    inspect_database(source)
    start = utc()
    started = time.monotonic()
    created = []
    try:
        for p in (metadata, target):
            fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            os.close(fd)
            created.append(p)
        def progress(status, remaining, total):
            if time.monotonic() - started > 30:
                raise TimeoutError("Backup timed out; pause competing writers and retry to a new path")
        with closing(connect_readonly(source)) as src, closing(sqlite3.connect(target)) as dst:
            src.backup(dst, pages=128, progress=progress, sleep=0.05)
            # Leave a self-contained finished checkpoint, without WAL companions.
            dst.execute("PRAGMA journal_mode=DELETE")
        result = inspect_database(target)
        result.update(operation=operation, source=str(source), started_utc=start,
                      completed_utc=utc(), copy_seconds=round(time.monotonic()-started, 3),
                      sha256=hashlib.sha256(target.read_bytes()).hexdigest())
        metadata.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        return result
    except Exception:
        for p in created:
            p.unlink(missing_ok=True)
        # Only companions belonging to the exclusively created target may be removed.
        if target in created:
            for suffix in ("-wal", "-shm", "-journal"):
                Path(str(target)+suffix).unlink(missing_ok=True)
        raise


def main():
    p = argparse.ArgumentParser(description=__doc__)
    commands = p.add_subparsers(dest="operation", required=True)
    for name in ("checkpoint", "restore"):
        sub = commands.add_parser(name)
        sub.add_argument("--source", required=True)
        sub.add_argument("--target", required=True)
    sub = commands.add_parser("inspect")
    sub.add_argument("--source", required=True)
    a = p.parse_args()
    try:
        result = inspect_database(a.source) if a.operation == "inspect" else copy_database(a.source, a.target, a.operation)
        print(json.dumps(result, indent=2))
    except (OSError, ValueError, sqlite3.Error, TimeoutError) as error:
        raise SystemExit("Database operation stopped: " + str(error)) from None


if __name__ == "__main__":
    main()
