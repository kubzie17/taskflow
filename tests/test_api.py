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
        self.db_path = Path(folder) / "test.db"
        api = create_app(self.db_path)
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

    def test_health_identifies_service(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["service"], "taskflow")

   

    def test_rejects_overlong_title_without_writing(self):
        tasklist_start = self.client.get("/tasks").json()
        response = self.client.post("/tasks", json={"title": "X" * 101})
        self.assertEqual(response.status_code, 422)
        tasklist_end = self.client.get("/tasks").json()
        self.assertEqual(tasklist_end, tasklist_start)



    def test_booking_survives_container_replacement(self):
        created = self.client.post("/tasks", json={"title": "Inspect bay A4"})
        self.assertEqual(created.status_code, 201)
        booking = created.json()


        replacement = create_app(self.db_path)
        with TestClient(replacement) as new_client:
            listing = new_client.get("/tasks")
            self.assertEqual(listing.status_code, 200)
            self.assertIn(booking, listing.json())


    def test_public_status_contract(self):
        folder = self.enterContext(TemporaryDirectory())
        candidate = create_candidate(Path(folder) / "day04-test.db")
        with TestClient(candidate) as client:
            response = client.get("/support/status")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"status": "ok", "service": "taskflow"})

    def test_local_support_retains_its_diagnostics(self):
        self.assertEqual(
            support_snapshot(),
            {
                "status": "ok",
                "service": "taskflow",
                "support_node": "nb-lab-amber-02",
                "runbook": "NB-DEMO-17",
            },
        )

    def test_candidate_preserves_health_and_booking(self):
        folder = self.enterContext(TemporaryDirectory())
        candidate = create_candidate(Path(folder) / "day04-test.db")
        with TestClient(candidate) as client:
            health = client.get("/health")
            self.assertEqual(health.status_code, 200)
            self.assertEqual(health.json(), {"status": "ok", "service": "taskflow"})

            created = client.post("/tasks", json={"title": "Book van service"})
            self.assertEqual(created.status_code, 201)
            booking = created.json()
            self.assertIsInstance(booking["id"], int)
            self.assertEqual(booking["title"], "Book van service")

            listing = client.get("/tasks")
            self.assertEqual(listing.status_code, 200)
            self.assertEqual(listing.json(), [booking])

            