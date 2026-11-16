"""Independent HTTP and SQLite checks. Copy to tests/ in the trainer's disposable reference tree."""
import base64
import json
import secrets
import sqlite3
from contextlib import closing
from datetime import datetime, timezone

import jwt
import pytest
from fastapi.testclient import TestClient

from exercises.day04_candidate import support_snapshot
from exercises.day05_api import create_secure
from exercises.day05_identity import AUDIENCE, ISSUER, LocalIdentity, make_state, password_record


@pytest.fixture(scope="module")
def identities():
    passwords = {role: secrets.token_urlsafe(18) for role in ("reader", "dispatcher")}
    state = make_state(passwords["reader"], passwords["dispatcher"])
    return passwords, state


@pytest.fixture
def lab(tmp_path, identities):
    passwords, state = identities
    db = tmp_path / "case.db"
    with TestClient(create_secure(db, LocalIdentity(state))) as client:
        yield client, db, passwords, state


def rows(db):
    with closing(sqlite3.connect(db)) as connection:
        return connection.execute("SELECT id, title FROM tasks ORDER BY id").fetchall()


def bearer(token):
    return {"Authorization": "Bearer " + token}


def login(client, name, passwords):
    response = client.post("/session", json={"username": name, "password": passwords[name]})
    assert response.status_code == 200
    assert response.headers["cache-control"] == "no-store"
    assert response.json()["token_type"] == "bearer"
    assert response.json()["expires_in"] == 600
    return bearer(response.json()["access_token"])


def manufacture(state, *, fields=None, remove=None, wrong_key=False):
    # Controlled test issuer only. Never copy, print or export the running lab's signing key.
    now = int(datetime.now(timezone.utc).timestamp())
    payload = dict(iss=ISSUER, aud=AUDIENCE, sub="test-person", iat=now - 20, exp=now + 60,
                   roles=["dispatcher"], token_use="access")
    payload.update(fields or {})
    if remove:
        del payload[remove]
    key = secrets.token_bytes(48) if wrong_key else base64.b64decode(state["key"])
    return jwt.encode(payload, key, algorithm="HS256")


def denied(client, db, code, headers=None, path="/tasks"):
    original = rows(db)
    response = client.post(path, json={"title": "Fictional attempted booking"}, headers=headers or {})
    assert response.status_code == code
    if code == 401:
        assert response.headers["www-authenticate"] == "Bearer"
    assert rows(db) == original


def test_credentials_reject_unknown_and_bad_password_the_same_way(lab):
    client, db, passwords, _ = lab
    first = client.post("/session", json={"username": "reader", "password": "invalid-fiction-only"})
    second = client.post("/session", json={"username": "unknown", "password": passwords["reader"]})
    assert (first.status_code, first.json()) == (second.status_code, second.json()) == (401, {"detail":"Authentication required"})
    missing_name = client.post("/session", json={"password": passwords["reader"]})
    assert missing_name.status_code == 422 and passwords["reader"] not in missing_name.text
    assert rows(db) == []


def test_secret_storage(identities):
    passwords, data = identities
    one = data["users"]["reader"]
    other = password_record(passwords["reader"])
    assert one["salt"] != other["salt"] and one["digest"] != other["digest"]
    assert all(password not in json.dumps(data) for password in passwords.values())


def test_health_and_public_status(lab):
    client, *_ = lab
    expected = {"status": "ok", "service": "taskflow"}
    assert client.get("/health").json() == expected
    response = client.get("/support/status")
    assert response.status_code == 200 and response.json() == expected
    assert {"support_node", "runbook"} <= support_snapshot().keys()


def test_anonymous_and_fake_role(lab):
    client, db, *_ = lab
    denied(client, db, 401)
    denied(client, db, 401, {"X-Role": "dispatcher"})
    assert client.get("/tasks").status_code == 401


def test_reader_can_read_but_cannot_write(lab):
    client, db, passwords, _ = lab
    headers = login(client, "reader", passwords)
    assert client.get("/tasks", headers=headers).status_code == 200
    denied(client, db, 403, {**headers, "X-Role":"dispatcher"})
    r = client.post("/session", json={"username":"reader", "password":passwords["reader"], "role":"dispatcher"})
    assert r.status_code == 422
    assert rows(db) == []


def test_dispatcher_write_read_and_existing_reader_access(lab):
    client, db, passwords, _ = lab
    dispatcher = login(client, "dispatcher", passwords)
    reader = login(client, "reader", passwords)
    response = client.post("/tasks", headers=dispatcher, json={"title":"  Book van service  "})
    assert response.status_code == 201
    created = response.json()
    assert type(created["id"]) is int and created["title"] == "Book van service"
    assert rows(db) == [(created["id"], created["title"])]
    for user in (reader, dispatcher):
        assert client.get("/tasks", headers=user).json() == [created]
    denied(client, db, 401)
    denied(client, db, 403, reader)


def test_authorised_title_boundaries(lab):
    client, db, passwords, _ = lab
    headers = login(client, "dispatcher", passwords)
    for title in ("A", "X"*100):
        assert client.post("/tasks", headers=headers, json={"title":title}).status_code == 201
    expected = rows(db)
    for title in ("", "   ", "X"*101):
        assert client.post("/tasks", headers=headers, json={"title":title}).status_code == 422
        assert rows(db) == expected


@pytest.mark.parametrize("fields", [
    {"exp": 1}, {"iss":"urn:other"}, {"aud":"urn:other-api"}, {"token_use":"id"},
    {"iat":4102444800}, {"roles":"dispatcher"}, {"roles":[{}]}, {"sub":""}
])
def test_bad_claim_is_rejected(lab, fields):
    client, db, _, state = lab
    denied(client, db, 401, bearer(manufacture(state, fields=fields)))


@pytest.mark.parametrize("claim", ["iss","aud","exp","iat","sub","roles","token_use"])
def test_required_claim(lab, claim):
    client, db, _, state = lab
    denied(client, db, 401, bearer(manufacture(state, remove=claim)))


def test_signature_malformed_unsigned_and_wrong_scheme(lab):
    client, db, passwords, state = lab
    raw = login(client, "reader", passwords)["Authorization"].split()[1]
    head, body, sig = raw.split(".")
    claims = json.loads(base64.urlsafe_b64decode(body + "==="))
    claims["roles"] = ["dispatcher"]
    altered = base64.urlsafe_b64encode(json.dumps(claims).encode()).decode().rstrip("=")
    for token in (head+"."+altered+"."+sig, "invalid.value", jwt.encode(claims, None, algorithm="none"),
                  manufacture(state, wrong_key=True)):
        denied(client, db, 401, bearer(token))
    denied(client, db, 401, {"Authorization":"Basic fictional"})


def test_unknown_signed_role_and_path_variants(lab):
    client, db, _, state = lab
    denied(client, db, 403, bearer(manufacture(state, fields={"roles":["unknown"]})))
    for path in ("/tasks/", "/%74asks", "/tasks?role=dispatcher"):
        denied(client, db, 401, path=path)
    schema = client.get("/openapi.json").json()["paths"]
    assert set(schema["/tasks"]) == {"get", "post"}
    for method in ("get","post"):
        assert schema["/tasks"][method]["security"]
