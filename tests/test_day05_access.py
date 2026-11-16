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





def _token(client, username, password):
    """Sign in and return the raw access token string."""
    response = client.post("/session", json={"username": username, "password": password})
    assert response.status_code == 200
    return response.json()["access_token"]


def _auth(token):
    return {"Authorization": f"Bearer {token}"}


def test_visitor_cannot_create_task(lab):
    client, db_path, _ = lab
    before = rows(db_path)

    response = client.post("/tasks", json={"title": "visitor attempt to create task"})

    assert response.status_code == 401
    assert rows(db_path) == before


def test_reader_cannot_create_task(lab):
    client, db_path, passwords = lab
    token = _token(client, "reader", passwords["reader"])
    before = rows(db_path)

    response = client.post("/tasks", json={"title": "reader attempt"}, headers=_auth(token))

    assert response.status_code == 403
    assert rows(db_path) == before


def test_dispatcher_can_create_task(lab):
    client, db_path, passwords = lab
    token = _token(client, "dispatcher", passwords["dispatcher"])
    before = rows(db_path)

    response = client.post(
        "/tasks", json={"title": "chester the new task"}, headers=_auth(token)
    )

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "chester the new task"
    assert isinstance(body["id"], int)

    after = rows(db_path)
    assert len(after) == len(before) + 1
    assert (body["id"], body["title"]) in after


def test_invalid_token_cannot_create_task(lab):
    client, db_path, _ = lab
    before = rows(db_path)

    response = client.post(
        "/tasks", json={"title": "invalid token attempt"},
        headers=_auth("this.is.not.a.valid.token"),
    )

    assert response.status_code == 401
    assert rows(db_path) == before


# Stretch challenge
def test_altered_token_cannot_create_task(lab):
    client, db_path, passwords = lab
    token = _token(client, "dispatcher", passwords["dispatcher"])
    # Alter the payload so the signature no longer matches. Swapping the first
    # character always changes the segment, unlike overwriting with fixed text.
    head, payload, signature = token.split(".")
    payload = ("B" if payload[0] == "A" else "A") + payload[1:]
    tampered = ".".join([head, payload, signature])
    assert tampered != token
    before = rows(db_path)

    response = client.post(
        "/tasks", json={"title": "tampered token attempt"}, headers=_auth(tampered)
    )

    assert response.status_code == 401
    assert rows(db_path) == before


def test_dispatcher_overlong_title_is_rejected(lab):
    client, db_path, passwords = lab
    token = _token(client, "dispatcher", passwords["dispatcher"])
    before = rows(db_path)

    response = client.post(
        "/tasks", json={"title": "X" * 101}, headers=_auth(token)
    )

    assert response.status_code == 422
    assert rows(db_path) == before


def test_expired_token_cannot_create_task(tmp_path):
    from datetime import datetime, timedelta, timezone

    import jwt

    from exercises.day05_identity import AUDIENCE, ISSUER

    passwords = {name: secrets.token_urlsafe(18) for name in ("reader", "dispatcher")}
    identity = LocalIdentity(make_state(passwords["reader"], passwords["dispatcher"]))
    db_path = tmp_path / "bookings.db"

   
    now = datetime.now(timezone.utc)
    expired = jwt.encode(
        {"iss": ISSUER, "aud": AUDIENCE, "sub": "dispatcher",
         "iat": now - timedelta(minutes=20), "exp": now - timedelta(minutes=10),
         "token_use": "access", "roles": ["dispatcher"]},
        identity._key, algorithm="HS256",
    )

    with TestClient(create_secure(db_path, identity)) as client:
        before = rows(db_path)
        response = client.post(
            "/tasks", json={"title": "expired token attempt"}, headers=_auth(expired)
        )

        assert response.status_code == 401
        assert rows(db_path) == before
