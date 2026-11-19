"""Regression checks for the runtime adapter, separate from prior learner tests."""
import json
import secrets
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from exercises.day05_identity import make_state
from exercises.day09_entry import application


@pytest.fixture
def configured(tmp_path, monkeypatch):
    passwords = {role: secrets.token_urlsafe(18) for role in ("reader", "dispatcher")}
    identity = tmp_path / "identity.json"
    identity.write_text(json.dumps(make_state(passwords["reader"], passwords["dispatcher"])))
    monkeypatch.setenv("TASKFLOW_IDENTITY_FILE", str(identity))
    monkeypatch.setenv("TASKFLOW_DB", str(tmp_path / "bookings.db"))
    monkeypatch.setenv("APP_ENVIRONMENT", "ci")
    return passwords, identity


@pytest.mark.parametrize("name", ["TASKFLOW_DB", "TASKFLOW_IDENTITY_FILE", "APP_ENVIRONMENT"])
def test_required_config(configured, monkeypatch, name):
    monkeypatch.delenv(name)
    with pytest.raises(RuntimeError, match="Missing runtime configuration"):
        application()


def test_runtime_database_survives_factory_restart(configured):
    passwords, _ = configured
    with TestClient(application()) as api:
        assert api.get("/tasks").status_code == 401
        token = api.post("/session", json={"username": "dispatcher", "password": passwords["dispatcher"]}).json()["access_token"]
        made = api.post("/tasks", json={"title": "Persistent fictional booking"}, headers={"Authorization": "Bearer " + token})
        assert made.status_code == 201
    with TestClient(application()) as api:
        token = api.post("/session", json={"username": "reader", "password": passwords["reader"]}).json()["access_token"]
        headers = {"Authorization": "Bearer " + token}
        assert api.get("/tasks", headers=headers).json() == [made.json()]
        assert api.post("/tasks", json={"title": "Denied"}, headers=headers).status_code == 403
        assert api.get("/tasks", headers=headers).json() == [made.json()]


def test_bad_identity_fails_without_contents(configured):
    _, identity = configured
    identity.write_text('SECRET_SENTINEL')
    with pytest.raises(RuntimeError, match="unavailable or invalid") as error:
        application()
    assert "SECRET_SENTINEL" not in str(error.value)


def test_missing_identity_does_not_create_anonymous_api(configured):
    _, identity = configured
    identity.unlink()
    with pytest.raises(RuntimeError, match="unavailable or invalid"):
        application()


def test_reject_relative_database(configured, monkeypatch):
    monkeypatch.setenv("TASKFLOW_DB", "data/accidental-root-disk.db")
    with pytest.raises(RuntimeError, match="absolute"):
        application()


def test_missing_data_directory_fails_before_startup(configured, tmp_path, monkeypatch):
    monkeypatch.setenv("TASKFLOW_DB", str(tmp_path / "absent" / "bookings.db"))
    with pytest.raises(RuntimeError, match="already exist"):
        application()


def test_unknown_environment_fails(configured, monkeypatch):
    monkeypatch.setenv("APP_ENVIRONMENT", "wrong")
    with pytest.raises(RuntimeError, match="APP_ENVIRONMENT"):
        application()
