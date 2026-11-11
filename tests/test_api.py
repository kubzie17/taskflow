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
        self.assertEqual(response.json()["service"], "taskflow")

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

    def test_rejects_overlong_title_without_writing(self):
        self.client.post("/tasks", json={"title": "Book van service"})  # existing booking that must survive
        before = self.client.get("/tasks").json()  # list with the existing booking
        response = self.client.post("/tasks", json={"title": "X" * 101})  # 101 chars, one over the limit
        self.assertEqual(response.status_code, 400)  # rejected
        self.assertEqual(self.client.get("/tasks").json(), before)  # existing bookings unchanged
