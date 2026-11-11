"""The tests use a temporary database, isolated from the learner's own tasks."""
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from fastapi.testclient import TestClient

from app.main import create_app


class TestTaskFlow(TestCase):
    def setUp(self):
        folder = self.enterContext(TemporaryDirectory())
        api = create_app(Path(folder) / "test.db")
        self.client = self.enterContext(TestClient(api))

    def test_health_reports_ok(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_health_identifies_service(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["status"], "ok")
        self.assertEqual(body["service"], "taskflow")

    def test_created_task_appears_in_list(self):
        response = self.client.post("/tasks", json={"title": "Book van service"})
        self.assertEqual(response.status_code, 201)
        created = response.json()
        self.assertIsInstance(created["id"], int)
        self.assertEqual(created["title"], "Book van service")
        listing = self.client.get("/tasks")
        self.assertEqual(listing.status_code, 200)
        self.assertEqual(listing.json(), [created])

    def test_rejects_overlong_title_without_writing(self):
        # Seed an existing booking so we can prove it is left untouched.
        seeded = self.client.post("/tasks", json={"title": "Book van service"})
        self.assertEqual(seeded.status_code, 201)
        before = self.client.get("/tasks").json()

        # An overlong title (one character past the 100 limit) must be rejected.
        overlong_title = "a" * 101
        response = self.client.post("/tasks", json={"title": overlong_title})
        self.assertEqual(response.status_code, 400)

        # The rejection must leave the existing bookings exactly as they were:
        # nothing added, nothing changed.
        after = self.client.get("/tasks").json()
        self.assertEqual(after, before)
        self.assertEqual(after, [seeded.json()])
