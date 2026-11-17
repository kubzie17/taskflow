"""The tests use a temporary database, isolated from the learner's own tasks."""
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from fastapi.testclient import TestClient

from app.main import create_app
from exercises.day04_candidate import *
from exercises.day05_api import *
from exercises.day05_identity import LocalIdentity, make_state


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

    def test_rejects_overlong_title_without_writing(self):
        response = self.client.post("/tasks", json={"title": "Book van service"})
        self.assertEqual(response.status_code, 201)
        tasklist_start = self.client.get("/tasks").json()
        response = self.client.post("/tasks", json={"title": "1"*101})
        self.assertEqual(response.status_code, 422)
        tasklist_end = self.client.get("/tasks").json()
        self.assertEqual(tasklist_end, tasklist_start)


class TestTaskFlow2(TestCase):
    def test_public_status_contract(self):
        folder = self.enterContext(TemporaryDirectory())
        api = create_candidate(Path(folder) / "test2.db")
        self.client = self.enterContext(TestClient(api))
        response = self.client.get("/support/status")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")
        self.assertEqual(response.json()["service"], "taskflow")
    
    def test_local_support_retains_its_diagnostics(self):
        self.assertEqual(support_snapshot(), {
        "status": "ok",
        "service": "taskflow",
        "support_node": "nb-lab-amber-02",
        "runbook": "NB-DEMO-17"})

    def test_candidate_preserves_health_and_booking(self):
        folder = self.enterContext(TemporaryDirectory())
        api = create_candidate(Path(folder) / "test2.db")
        self.client = self.enterContext(TestClient(api))
        TestTaskFlow.test_health_reports_ok(self)
        TestTaskFlow.test_created_task_appears_in_list(self)
        
class TestTaskFlowPermissions(TestCase):
    def setUp(self):
        folder = self.enterContext(TemporaryDirectory())
        self.passwords = {"reader": "reader-password", "dispatcher": "dispatcher-password"}
        identity = LocalIdentity(make_state(self.passwords["reader"], self.passwords["dispatcher"]))
        api = create_secure(Path(folder) / "test.db", identity)
        self.client = self.enterContext(TestClient(api))

    def headers_for(self, username):
        response = self.client.post("/session", json={"username": username, "password": self.passwords[username]})
        self.assertEqual(response.status_code, 200)
        return {"Authorization": f"Bearer {response.json()['access_token']}"}

    def test_visitor_is_rejected(self):
        response = self.client.get("/tasks")
        self.assertEqual(response.status_code, 401)
        response = self.client.post("/tasks", json={"title": "Book van service"})
        self.assertEqual(response.status_code, 401)

    def test_reader_can_get_but_not_post(self):
        headers = self.headers_for("reader")
        response = self.client.get("/tasks", headers=headers)
        self.assertEqual(response.status_code, 200)
        response = self.client.post("/tasks", json={"title": "Book van service"}, headers=headers)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.client.get("/tasks", headers=headers).json(), [])
    
    def test_dispatcher_can_get_and_post(self):
        headers = self.headers_for("dispatcher")
        response = self.client.get("/tasks", headers=headers)
        self.assertEqual(response.status_code, 200)
        response = self.client.post("/tasks", json={"title": "Book van service"}, headers=headers)
        self.assertEqual(response.status_code, 201)
        
        


