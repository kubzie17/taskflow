from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from fastapi.testclient import TestClient

from app.main import create_app
from exercises.day04_candidate import *
from exercises.day05_api import *
from exercises.day05_identity import LocalIdentity, make_state


class TEST(TestCase):
    def setUp(self):
        folder = self.enterContext(TemporaryDirectory())
        api = create_app(Path(folder) / "test.db")
        self.client = self.enterContext(TestClient(api))

    def test_fake_on_purpose(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        