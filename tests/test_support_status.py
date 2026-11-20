"""Regression test: the public /support/status must not leak internal fields."""
from pathlib import Path
from tempfile import TemporaryDirectory

from fastapi.testclient import TestClient

from exercises.day04_candidate import create_candidate, support_snapshot


def test_public_status_contract():
    with TemporaryDirectory() as folder:
        client = TestClient(create_candidate(Path(folder) / "test.db"))
        response = client.get("/support/status")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "taskflow"}

def test_local_support_retains_its_diagnostics():
    assert support_snapshot() == {
        "status": "ok",
        "service": "taskflow",
        "support_node": "nb-lab-amber-02",
        "runbook": "NB-DEMO-17",
    }

def test_candidate_preserves_health_and_booking():
    with TemporaryDirectory() as folder:
     
        with TestClient(create_candidate(Path(folder) / "test.db")) as client:
            assert client.get("/health").status_code == 200
            created = client.post("/tasks", json={"title": "Book van service"})
            assert created.status_code == 201
            assert client.get("/tasks").json() == [created.json()]







 










