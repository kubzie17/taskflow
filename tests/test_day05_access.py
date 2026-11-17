"""Day 5 regression suite: authentication + role-based authorisation for TaskFlow.

Covers the client-agreed status matrix, token integrity (missing / malformed /
expired / tampered / forged role), both allowed reads, title validation
boundaries and the public status contract. Every denied or invalid write is
checked against the database directly so a route that writes-then-refuses is
caught.

The fixture builds an isolated in-memory identity and a temporary SQLite file,
so the suite is independent of the local lab file in ~/.taskflow-lab.
"""
import secrets
import sqlite3
from contextlib import closing
from datetime import datetime, timedelta, timezone

import jwt
import pytest
from fastapi.testclient import TestClient

from exercises.day05_api import create_secure
from exercises.day05_identity import (
    AUDIENCE,
    ISSUER,
    LocalIdentity,
    Principal,
    make_state,
)


@pytest.fixture()
def lab(tmp_path):
    passwords = {name: secrets.token_urlsafe(18) for name in ("reader", "dispatcher")}
    identity = LocalIdentity(make_state(passwords["reader"], passwords["dispatcher"]))
    db_path = tmp_path / "bookings.db"
    with TestClient(create_secure(db_path, identity)) as client:
        yield client, db_path, passwords, identity


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #

def rows(db_path):
    """Direct read-only SQLite reader -- the source of truth for writes."""
    with closing(sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)) as c:
        return c.execute("SELECT id, title FROM tasks ORDER BY id").fetchall()


def seed(db_path, title):
    """Insert a known booking directly so reads have something to return."""
    with closing(sqlite3.connect(db_path)) as c, c:
        c.execute("INSERT INTO tasks (title) VALUES (?)", (title,))


def token(client, passwords, who):
    resp = client.post("/session", json={"username": who, "password": passwords[who]})
    assert resp.status_code == 200
    return resp.json()["access_token"]


def auth(client, passwords, who):
    return {"Authorization": f"Bearer {token(client, passwords, who)}"}


def _mint(identity: LocalIdentity, *, sub="dispatcher", roles=("dispatcher",),
          lifetime=timedelta(minutes=10), key=None, token_use="access"):
    """Mint a synthetic token signed with the provider key (or a wrong key)."""
    now = datetime.now(timezone.utc)
    claims = {
        "iss": ISSUER, "aud": AUDIENCE, "sub": sub,
        "iat": now, "exp": now + lifetime,
        "token_use": token_use, "roles": sorted(roles),
    }
    signing_key = key if key is not None else identity._key
    return jwt.encode(claims, signing_key, algorithm="HS256")


# --------------------------------------------------------------------------- #
# agreed status matrix
# --------------------------------------------------------------------------- #

def test_visitor_cannot_list(lab):
    client, _, _, _ = lab
    assert client.get("/tasks").status_code == 401


def test_visitor_cannot_create_and_writes_nothing(lab):
    client, db, _, _ = lab
    before = rows(db)
    assert client.post("/tasks", json={"title": "visitor booking"}).status_code == 401
    assert rows(db) == before


def test_reader_can_list(lab):
    client, db, p, _ = lab
    seed(db, "known booking")
    resp = client.get("/tasks", headers=auth(client, p, "reader"))
    assert resp.status_code == 200
    assert resp.json() == [{"id": 1, "title": "known booking"}]


def test_reader_cannot_create_and_writes_nothing(lab):
    client, db, p, _ = lab
    before = rows(db)
    resp = client.post("/tasks", json={"title": "reader booking"},
                       headers=auth(client, p, "reader"))
    assert resp.status_code == 403
    assert rows(db) == before


def test_dispatcher_can_list(lab):
    client, db, p, _ = lab
    seed(db, "known booking")
    assert client.get("/tasks", headers=auth(client, p, "dispatcher")).status_code == 200


def test_dispatcher_can_create_exactly_one_row(lab):
    client, db, p, _ = lab
    before = rows(db)
    resp = client.post("/tasks", json={"title": "dispatcher booking"},
                       headers=auth(client, p, "dispatcher"))
    assert resp.status_code == 201
    body = resp.json()
    after = rows(db)
    assert len(after) == len(before) + 1
    assert (body["id"], body["title"]) in after


# --------------------------------------------------------------------------- #
# title validation boundaries
# --------------------------------------------------------------------------- #

def test_dispatcher_max_length_title_accepted(lab):
    client, db, p, _ = lab
    resp = client.post("/tasks", json={"title": "A" * 100}, headers=auth(client, p, "dispatcher"))
    assert resp.status_code == 201
    assert rows(db) == [(1, "A" * 100)]


def test_dispatcher_over_length_title_rejected_no_write(lab):
    client, db, p, _ = lab
    before = rows(db)
    resp = client.post("/tasks", json={"title": "A" * 101}, headers=auth(client, p, "dispatcher"))
    assert resp.status_code == 422
    assert rows(db) == before


def test_dispatcher_blank_title_rejected_no_write(lab):
    client, db, p, _ = lab
    before = rows(db)
    resp = client.post("/tasks", json={"title": "   "}, headers=auth(client, p, "dispatcher"))
    assert resp.status_code == 422
    assert rows(db) == before


# --------------------------------------------------------------------------- #
# token integrity
# --------------------------------------------------------------------------- #

def test_missing_token_rejected(lab):
    client, _, _, _ = lab
    assert client.get("/tasks").status_code == 401


def test_malformed_token_rejected(lab):
    client, _, _, _ = lab
    r = client.get("/tasks", headers={"Authorization": "Bearer this.is.not.a.valid.token"})
    assert r.status_code == 401


def test_malformed_bearer_post_rejected_no_write(lab):
    client, db, _, _ = lab
    before = rows(db)
    r = client.post("/tasks", json={"title": "malformed bearer"},
                    headers={"Authorization": "Bearer this.is.not.a.valid.token"})
    assert r.status_code == 401
    assert rows(db) == before


def test_expired_token_rejected_no_write(lab):
    client, db, _, identity = lab
    before = rows(db)
    expired = _mint(identity, lifetime=timedelta(minutes=-5))  # already expired
    r = client.post("/tasks", json={"title": "expired attempt"},
                    headers={"Authorization": f"Bearer {expired}"})
    assert r.status_code == 401
    assert rows(db) == before


def test_tampered_signature_rejected(lab):
    client, _, p, _ = lab
    good = token(client, p, "dispatcher")
    # Flip the final character of the signature to break it.
    tampered = good[:-1] + ("a" if good[-1] != "a" else "b")
    r = client.get("/tasks", headers={"Authorization": f"Bearer {tampered}"})
    assert r.status_code == 401


def test_token_signed_with_wrong_key_rejected(lab):
    client, _, _, identity = lab
    forged = _mint(identity, key=b"a-different-signing-key-entirely-32b!")
    r = client.get("/tasks", headers={"Authorization": f"Bearer {forged}"})
    assert r.status_code == 401


def test_forged_role_in_self_signed_token_cannot_be_used(lab):
    # A caller cannot forge a dispatcher role without the server's signing key.
    # Signing with a key we don't control yields a token the server rejects (401).
    client, db, _, identity = lab
    before = rows(db)
    forged = _mint(identity, sub="attacker", roles=("dispatcher",),
                   key=b"attacker-controlled-key-padded-to-32b")
    r = client.post("/tasks", json={"title": "forged role"},
                    headers={"Authorization": f"Bearer {forged}"})
    assert r.status_code == 401
    assert rows(db) == before


# --------------------------------------------------------------------------- #
# public status contract
# --------------------------------------------------------------------------- #

def test_public_health_open(lab):
    client, _, _, _ = lab
    assert client.get("/health").status_code == 200


def test_public_support_status_contract(lab):
    client, _, _, _ = lab
    resp = client.get("/support/status")
    assert resp.status_code == 200
    # Only the two public fields -- no internal diagnostics leaked.
    assert resp.json() == {"status": "ok", "service": "taskflow"}
