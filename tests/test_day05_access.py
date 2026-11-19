"""Access-control regression tests for the protected Day 5 TaskFlow API.

Every denied or invalid write is verified twice: by the HTTP status and by reading
the SQLite file directly. A handler that wrote a row and then returned an error
would pass a status-only test but fails these.
"""
import base64
import json
import secrets
import sqlite3
from contextlib import closing
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

import jwt
import pytest
from fastapi.testclient import TestClient

from app import database
from exercises.day05_api import create_secure
from exercises.day05_identity import AUDIENCE, ISSUER, LocalIdentity, make_state

SEED_TITLE = "Seeded booking: inspect fictional bay A4"
VALID_TITLE = "Inspect fictional station equipment"
PUBLIC_STATUS = {"status": "ok", "service": "taskflow"}


# --- Fixtures and helpers ---------------------------------------------------

@pytest.fixture(scope="module")
def identity_bundle():
    """One set of fictional identities per module. Hashing passphrases is slow by design."""
    passwords = {name: secrets.token_urlsafe(18) for name in ("reader", "dispatcher")}
    state = make_state(passwords["reader"], passwords["dispatcher"])
    signing_key = base64.b64decode(state["key"], validate=True)
    return LocalIdentity(state), passwords, signing_key


@pytest.fixture(scope="module")
def tokens(identity_bundle, tmp_path_factory):
    """Obtain each role's token through the real POST /session route, once."""
    identity, passwords, _ = identity_bundle
    db_path = tmp_path_factory.mktemp("signin") / "signin.db"
    issued = {}
    with TestClient(create_secure(db_path, identity)) as client:
        for role in ("reader", "dispatcher"):
            response = client.post("/session", json={"username": role, "password": passwords[role]})
            assert response.status_code == 200, response.text
            issued[role] = response.json()["access_token"]
    return issued


@dataclass
class Lab:
    client: TestClient
    db_path: Path
    passwords: dict
    signing_key: bytes
    tokens: dict

    def headers(self, caller):
        if caller == "visitor":
            return {}
        return {"Authorization": f"Bearer {self.tokens[caller]}"}


@pytest.fixture()
def lab(tmp_path, identity_bundle, tokens):
    """A fresh database per test, seeded with one known booking."""
    identity, passwords, signing_key = identity_bundle
    db_path = tmp_path / "bookings.db"
    with TestClient(create_secure(db_path, identity)) as client:
        database.create_task(db_path, SEED_TITLE)
        yield Lab(client, db_path, passwords, signing_key, tokens)


def rows(db_path):
    """Read the stored bookings straight from SQLite, bypassing the API."""
    with closing(sqlite3.connect(db_path)) as connection:
        return connection.execute("SELECT id, title FROM tasks ORDER BY id").fetchall()


def forge(key, **overrides):
    """Mint a token with the server's real signing key and chosen claim overrides."""
    now = datetime.now(timezone.utc)
    claims = {"iss": ISSUER, "aud": AUDIENCE, "sub": "dispatcher", "iat": now,
              "exp": now + timedelta(minutes=10), "token_use": "access", "roles": ["dispatcher"]}
    claims.update(overrides)
    return jwt.encode(claims, key, algorithm="HS256")


def segment(data):
    return base64.urlsafe_b64encode(data).decode().rstrip("=")


def edit_roles(token):
    """Rewrite the roles claim to dispatcher while keeping the original signature."""
    head, body, signature = token.split(".")
    claims = json.loads(base64.urlsafe_b64decode(body + "==="))
    claims["roles"] = ["dispatcher"]
    return ".".join((head, segment(json.dumps(claims).encode()), signature))


def bearer(token):
    return {"Authorization": f"Bearer {token}"}


# --- The agreed status matrix ----------------------------------------------

MATRIX = [
    ("visitor", "GET", 401, 0),
    ("reader", "GET", 200, 0),
    ("dispatcher", "GET", 200, 0),
    ("visitor", "POST", 401, 0),
    ("reader", "POST", 403, 0),
    ("dispatcher", "POST", 201, 1),
]


@pytest.mark.parametrize("caller,method,expected,added", MATRIX,
                         ids=[f"{c}-{m}" for c, m, _, _ in MATRIX])
def test_status_matrix_and_row_delta(lab, caller, method, expected, added):
    before = rows(lab.db_path)
    if method == "GET":
        response = lab.client.get("/tasks", headers=lab.headers(caller))
    else:
        response = lab.client.post("/tasks", headers=lab.headers(caller), json={"title": VALID_TITLE})
    assert response.status_code == expected
    after = rows(lab.db_path)
    assert len(after) == len(before) + added
    assert after[:len(before)] == before  # existing rows are never altered
    if added:
        assert after[-1][1] == VALID_TITLE  # exactly the dispatcher's row was stored


@pytest.mark.parametrize("caller", ["reader", "dispatcher"])
def test_both_roles_read_the_seeded_booking(lab, caller):
    response = lab.client.get("/tasks", headers=lab.headers(caller))
    assert response.status_code == 200
    listed = [(task["id"], task["title"]) for task in response.json()]
    assert listed == rows(lab.db_path)
    assert SEED_TITLE in [title for _, title in listed]


def test_dispatcher_creates_then_reads_back_the_same_booking(lab):
    created = lab.client.post("/tasks", headers=lab.headers("dispatcher"), json={"title": VALID_TITLE})
    assert created.status_code == 201
    booking = created.json()
    assert (booking["id"], booking["title"]) in rows(lab.db_path)
    listing = lab.client.get("/tasks", headers=lab.headers("reader"))
    assert booking in listing.json()


# --- Invalid, expired, tampered and forged credentials ----------------------

BAD_CREDENTIALS = {
    "missing": lambda lab: {},
    "malformed": lambda lab: bearer("fictional.not-a-token"),
    "empty-bearer": lambda lab: {"Authorization": "Bearer "},
    "wrong-scheme": lambda lab: {"Authorization": "Basic " + lab.tokens["dispatcher"]},
    "edited-roles-old-signature": lambda lab: bearer(edit_roles(lab.tokens["reader"])),
    "signature-stripped": lambda lab: bearer(".".join(lab.tokens["dispatcher"].split(".")[:2]) + "."),
    "expired": lambda lab: bearer(forge(lab.signing_key,
                                        iat=datetime.now(timezone.utc) - timedelta(minutes=20),
                                        exp=datetime.now(timezone.utc) - timedelta(minutes=1))),
    "signed-with-another-key": lambda lab: bearer(forge(secrets.token_bytes(48))),
    "wrong-audience": lambda lab: bearer(forge(lab.signing_key, aud="urn:other:api")),
    "wrong-issuer": lambda lab: bearer(forge(lab.signing_key, iss="urn:someone:else")),
    "not-an-access-token": lambda lab: bearer(forge(lab.signing_key, token_use="id")),
}


@pytest.mark.parametrize("name", BAD_CREDENTIALS)
def test_bad_credentials_cannot_write(lab, name):
    before = rows(lab.db_path)
    response = lab.client.post("/tasks", headers=BAD_CREDENTIALS[name](lab), json={"title": VALID_TITLE})
    assert response.status_code == 401
    assert rows(lab.db_path) == before


@pytest.mark.parametrize("name", BAD_CREDENTIALS)
def test_bad_credentials_cannot_read(lab, name):
    response = lab.client.get("/tasks", headers=BAD_CREDENTIALS[name](lab))
    assert response.status_code == 401


def test_rejection_asks_for_a_bearer_token(lab):
    response = lab.client.get("/tasks")
    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"


def test_validly_signed_token_with_unknown_role_is_forbidden(lab):
    before = rows(lab.db_path)
    headers = bearer(forge(lab.signing_key, roles=["admin"]))
    assert lab.client.get("/tasks", headers=headers).status_code == 403
    assert lab.client.post("/tasks", headers=headers, json={"title": VALID_TITLE}).status_code == 403
    assert rows(lab.db_path) == before


def test_role_header_from_the_client_is_ignored(lab):
    before = rows(lab.db_path)
    headers = {**lab.headers("reader"), "X-Role": "dispatcher"}
    response = lab.client.post("/tasks", headers=headers, json={"title": VALID_TITLE})
    assert response.status_code == 403
    assert rows(lab.db_path) == before


def test_role_in_the_body_is_ignored(lab):
    before = rows(lab.db_path)
    payload = {"title": VALID_TITLE, "role": "dispatcher", "roles": ["dispatcher"]}
    response = lab.client.post("/tasks", headers=lab.headers("reader"), json=payload)
    assert response.status_code == 403
    assert rows(lab.db_path) == before


def test_anonymous_caller_cannot_claim_a_role_with_a_header(lab):
    before = rows(lab.db_path)
    response = lab.client.post("/tasks", headers={"X-Role": "dispatcher"}, json={"title": VALID_TITLE})
    assert response.status_code == 401
    assert rows(lab.db_path) == before


# --- Title validation by an authorised dispatcher ---------------------------

TITLE_CASES = [
    ({"title": "A"}, 201),
    ({"title": "X" * 100}, 201),
    ({"title": "  padded title  "}, 201),
    ({"title": "X" * 101}, 422),
    ({"title": ""}, 422),
    ({"title": "   "}, 422),
    ({"title": 123}, 422),
    ({}, 422),
]


@pytest.mark.parametrize("payload,expected", TITLE_CASES,
                         ids=["1-char", "100-chars", "trimmed", "101-chars", "empty",
                              "whitespace-only", "not-a-string", "missing-title"])
def test_title_boundaries_for_an_authorised_dispatcher(lab, payload, expected):
    before = rows(lab.db_path)
    response = lab.client.post("/tasks", headers=lab.headers("dispatcher"), json=payload)
    assert response.status_code == expected
    after = rows(lab.db_path)
    if expected == 201:
        assert len(after) == len(before) + 1
        assert after[-1][1] == payload["title"].strip()
    else:
        assert after == before  # invalid data must not be stored


# --- Public endpoints -------------------------------------------------------

@pytest.mark.parametrize("path", ["/health", "/support/status"])
def test_public_endpoints_need_no_token_and_expose_only_two_fields(lab, path):
    response = lab.client.get(path)
    assert response.status_code == 200
    assert response.json() == PUBLIC_STATUS


# --- Sign-in ----------------------------------------------------------------

def test_sign_in_returns_a_short_lived_bearer_token_for_the_right_role(lab):
    response = lab.client.post("/session", json={"username": "reader",
                                                 "password": lab.passwords["reader"]})
    assert response.status_code == 200
    body = response.json()
    assert set(body) == {"access_token", "token_type", "expires_in"}
    assert body["token_type"] == "bearer"
    assert body["expires_in"] == 600
    assert response.headers["Cache-Control"] == "no-store"
    claims = jwt.decode(body["access_token"], lab.signing_key, algorithms=["HS256"],
                        issuer=ISSUER, audience=AUDIENCE)
    assert claims["roles"] == ["reader"]
    assert claims["exp"] - claims["iat"] == 600


def test_wrong_passphrase_and_unknown_user_look_identical(lab):
    wrong = lab.client.post("/session", json={"username": "reader", "password": "wrong-passphrase-123"})
    unknown = lab.client.post("/session", json={"username": "nobody", "password": "wrong-passphrase-123"})
    assert wrong.status_code == unknown.status_code == 401
    assert wrong.json() == unknown.json()


def test_a_role_cannot_be_requested_at_sign_in(lab):
    response = lab.client.post("/session", json={"username": "reader",
                                                 "password": lab.passwords["reader"],
                                                 "role": "dispatcher"})
    assert response.status_code == 422
    assert lab.passwords["reader"] not in response.text  # the passphrase is never echoed back
