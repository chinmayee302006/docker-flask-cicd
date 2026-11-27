import unittest
from unittest.mock import patch
from app import app


class FlaskAppTest(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome", response.data)

    def test_health(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "healthy")

    def test_info(self):
        with patch.dict("os.environ", {"APP_ENV": "testing"}):
            response = self.client.get("/api/info")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.json["application"],
                "Docker Flask App"
            )
            self.assertEqual(
                response.json["environment"],
                "testing"
            )


if __name__ == "__main__":
    unittest.main()