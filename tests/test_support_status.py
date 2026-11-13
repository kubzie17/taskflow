from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from fastapi.testclient import TestClient

from exercises.day04_candidate import create_candidate
from exercises.day04_candidate import support_snapshot


class TestSupportStatusDisclosure(TestCase):
    def setUp(self):
        folder = self.enterContext(TemporaryDirectory())
        api = create_candidate(Path(folder) / "support-test.db")
        self.client = self.enterContext(TestClient(api))

    def test_public_status_returns_only_approved_two_fields(self):
        response = self.client.get("/support/status")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"status": "ok", "service": "taskflow"},
        )

    def test_local_support_retains_its_diagnostics(self):
        self.assertEqual( support_snapshot(),
            {"status": "ok", "service": "taskflow", "support_node": "nb-lab-amber-02", "runbook": "NB-DEMO-17"},
        )

    def test_candidate_preserves_health_and_booking(self):
        health = self.client.get("/health")
        self.assertEqual(health.status_code, 200)
        self.assertEqual(health.json(), {"status": "ok", "service": "taskflow"})

        created = self.client.post("/tasks", json={"title": "chester the dog"})
        self.assertEqual(created.status_code, 201)
        booking = created.json()
        self.assertIsInstance(booking["id"], int)
        self.assertEqual(booking["title"], "chester the dog")

        listing = self.client.get("/tasks")
        self.assertEqual(listing.status_code, 200)
        self.assertEqual(listing.json(), [booking])

