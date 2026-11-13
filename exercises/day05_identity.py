"""Provided lab primitives. Create two fictional identities with python -m exercises.day05_identity."""
from __future__ import annotations

import base64
import getpass
import hashlib
import hmac
import json
import os
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

import jwt

STATE = Path.home() / ".taskflow-lab" / "day05.json"
ISSUER = "urn:northbridge:taskflow:lab"
AUDIENCE = "urn:northbridge:taskflow:bookings"


@dataclass(frozen=True)
class Principal:
    subject: str
    roles: frozenset[str]


class InvalidCredential(ValueError):
    """The caller cannot establish a valid identity."""


def _b64(raw: bytes) -> str:
    return base64.b64encode(raw).decode("ascii")


def _derive(password: str, salt: bytes) -> bytes:
    return hashlib.scrypt(password.encode("utf-8"), salt=salt, n=2**15, r=8, p=3,
                          maxmem=128 * 1024 * 1024, dklen=32)


def password_record(password: str) -> dict:
    salt = secrets.token_bytes(16)
    return {"salt": _b64(salt), "digest": _b64(_derive(password, salt))}


def make_state(reader_password: str, dispatcher_password: str) -> dict:
    if min(len(reader_password), len(dispatcher_password)) < 12 or reader_password == dispatcher_password:
        raise ValueError("Choose two different fictional passphrases of at least 12 characters.")
    users = {name: {**password_record(password), "role": name}
             for name, password in (("reader", reader_password), ("dispatcher", dispatcher_password))}
    return {"key": _b64(secrets.token_bytes(48)), "users": users}


def initialise_file(path: Path, state: dict) -> None:
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    with open(path, "x", encoding="utf-8",
              opener=lambda name, flags: os.open(name, flags, 0o600)) as handle:
        json.dump(state, handle)


class LocalIdentity:
    def __init__(self, state: dict):
        self.users = state["users"]
        self._key = base64.b64decode(state["key"], validate=True)
        self._dummy = self.users["reader"]

    @classmethod
    def from_file(cls, path: Path = STATE):
        if not path.is_file():
            raise RuntimeError("In this account run: python -m exercises.day05_identity")
        return cls(json.loads(path.read_text(encoding="utf-8")))

    def check_password(self, username: str, password: str) -> Principal | None:
        record = self.users.get(username)
        source = record if record is not None else self._dummy
        actual = _derive(password, base64.b64decode(source["salt"]))
        matches = hmac.compare_digest(actual, base64.b64decode(source["digest"]))
        if matches and record is not None:
            return Principal(username, frozenset({record["role"]}))
        return None

    def issue(self, principal: Principal) -> str:
        now = datetime.now(timezone.utc)
        claims = {"iss": ISSUER, "aud": AUDIENCE, "sub": principal.subject,
                  "iat": now, "exp": now + timedelta(minutes=10),
                  "token_use": "access", "roles": sorted(principal.roles)}
        return jwt.encode(claims, self._key, algorithm="HS256")

    def verify(self, token: str) -> Principal:
        required = ["iss", "aud", "sub", "iat", "exp", "token_use", "roles"]
        try:
            claims = jwt.decode(token, self._key, algorithms=["HS256"], issuer=ISSUER,
                                audience=AUDIENCE, options={"require": required})
            roles = claims["roles"]
            if (claims["token_use"] != "access" or not claims["sub"]
                    or not isinstance(roles, list) or not all(isinstance(r, str) for r in roles)):
                raise InvalidCredential()
            return Principal(claims["sub"], frozenset(roles))
        except (jwt.InvalidTokenError, TypeError, ValueError, OverflowError) as exc:
            raise InvalidCredential("Invalid access token") from exc


if __name__ == "__main__":
    if STATE.exists():
        raise SystemExit("The lab identities already exist. Use the original fictional passphrases.")
    try:
        reader = getpass.getpass("New fictional reader passphrase (12+ characters): ")
        dispatcher = getpass.getpass("New different fictional dispatcher passphrase: ")
        initialise_file(STATE, make_state(reader, dispatcher))
    except (ValueError, FileExistsError) as error:
        raise SystemExit(str(error))
    print("Local lab identities created outside the repository. No credentials printed.")
