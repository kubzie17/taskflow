"""Small SQLite store. Each operation owns and closes its connection."""
import sqlite3
from contextlib import closing
from pathlib import Path


def initialise(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(path)) as db, db:
        db.execute(
            """CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL
            )"""
        )


def create_task(path: Path, title: str) -> dict:
    with closing(sqlite3.connect(path)) as db, db:
        cursor = db.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        return {"id": cursor.lastrowid, "title": title}


def list_tasks(path: Path) -> list[dict]:
    with closing(sqlite3.connect(path)) as db:
        db.row_factory = sqlite3.Row
        rows = db.execute("SELECT id, title FROM tasks ORDER BY id").fetchall()
        return [dict(row) for row in rows]
