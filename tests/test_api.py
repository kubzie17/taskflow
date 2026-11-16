"""The tests use a temporary database, isolated from the learner's own tasks."""
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from fastapi.testclient import TestClient

from app.main import create_app
from exercises.day04_candidate import create_candidate, support_snapshot


class TestTaskFlow(TestCase):
    def setUp(self):
        folder = self.enterContext(TemporaryDirectory())
        api = create_app(Path(folder) / "test.db")
        self.client = self.enterContext(TestClient(api))

    def test_health_reports_ok(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_created_task_appears_in_list(self):
        response = self.client.post("/tasks", json={"title": "Book van service"})
        self.assertEqual(response.status_code, 201)
        created = response.json()
        self.assertIsInstance(created["id"], int)
        self.assertEqual(created["title"], "Book van service")
        listing = self.client.get("/tasks")
        self.assertEqual(listing.status_code, 200)
        self.assertEqual(listing.json(), [created])

    def test_health_indentifies_service(self):
        response = self.client.get("/health")
        self.assertEqual(response.json()["service"], "taskflow")

    # TEST 1 — The public endpoint must return only two fields
def test_public_status_contract(tmp_path):
    with TestClient(create_candidate(tmp_path / "status.db")) as client:
        response = client.get("/support/status")

    assert response.status_code == 200

    assert response.json() == {
        "status": "ok",
        "service": "taskflow",
    }


# TEST 2 — Internal support diagnostics must still exist
def test_local_support_retains_its_diagnostics():
    snapshot = support_snapshot()

    assert snapshot["support_node"] == "nb-lab-amber-02"
    assert snapshot["runbook"] == "NB-DEMO-17"


# TEST 3 — Existing TaskFlow functionality must still work
def test_candidate_preserves_health_and_booking(tmp_path):
    with TestClient(create_candidate(tmp_path / "booking.db")) as client:

        # Check existing health endpoint
        health = client.get("/health")

        assert health.status_code == 200
        assert health.json()["status"] == "ok"

        # Create a fictional booking
        created = client.post(
            "/tasks",
            json={"title": "Check west shutter T4"},
        )

        assert created.status_code == 201

        booking = created.json()

        assert isinstance(booking["id"], int)
        assert booking["title"] == "Check west shutter T4"

        # Confirm the booking is stored
        listing = client.get("/tasks")

        assert listing.status_code == 200
        assert booking in listing.json()

