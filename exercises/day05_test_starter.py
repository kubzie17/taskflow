"""Copy to tests/test_day05_access.py. Write your own tests using this isolated fixture."""
import secrets
import sqlite3
from contextlib import closing

import pytest
from fastapi.testclient import TestClient

from exercises.day05_api import create_secure
from exercises.day05_identity import LocalIdentity, make_state


@pytest.fixture()
def lab(tmp_path):
    passwords = {name: secrets.token_urlsafe(18) for name in ("reader", "dispatcher")}
    identity = LocalIdentity(make_state(passwords["reader"], passwords["dispatcher"]))
    db_path = tmp_path / "bookings.db"
    with TestClient(create_secure(db_path, identity)) as client:
        yield client, db_path, passwords


def rows(db_path):
    with closing(sqlite3.connect(db_path)) as connection:
        return connection.execute("SELECT id, title FROM tasks ORDER BY id").fetchall()


# Start with a test that would catch the Day 4 bug.
# Which observation would catch code that writes a booking and then returns 403?
