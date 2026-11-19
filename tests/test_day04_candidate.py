"""Workshop B regression tests for the Day 4 candidate.

The public /support/status endpoint must expose only the two approved fields.
The internal diagnostic snapshot must still carry the support information.
Existing health and booking behaviour must keep working.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from fastapi.testclient import TestClient

from exercises.day04_candidate import create_candidate, support_snapshot


class TestDay04Candidate(TestCase):
    def setUp(self):
        folder = self.enterContext(TemporaryDirectory())
        api = create_candidate(Path(folder) / "day04-test.db")
        self.client = self.enterContext(TestClient(api))

    def test_public_status_contract(self):
        response = self.client.get("/support/status")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok", "service": "taskflow"})

    def test_local_support_retains_its_diagnostics(self):
        snapshot = support_snapshot()
        self.assertEqual(snapshot["support_node"], "nb-lab-amber-02")
        self.assertEqual(snapshot["runbook"], "NB-DEMO-17")

    def test_candidate_preserves_health_and_booking(self):
        health = self.client.get("/health")
        self.assertEqual(health.status_code, 200)
        self.assertEqual(health.json()["status"], "ok")

        created = self.client.post("/tasks", json={"title": "Inspect east gate Q7"})
        self.assertEqual(created.status_code, 201)
        booking = created.json()
        self.assertEqual(booking["title"], "Inspect east gate Q7")

        listing = self.client.get("/tasks")
        self.assertEqual(listing.status_code, 200)
        self.assertEqual(listing.json(), [booking])
