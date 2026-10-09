import json

from django.test import TestCase
from rest_framework.test import APIClient

class HealthTests(TestCase):
    def test_root_status_endpoint(self):
        response = APIClient().get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)["status"], "ok")

    def test_health_endpoint(self):
        response = APIClient().get("/api/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "ok")

    def test_frontend_origin_is_allowed(self):
        response = APIClient().get(
            "/api/health/", HTTP_ORIGIN="http://localhost:5173"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Access-Control-Allow-Origin"], "http://localhost:5173"
        )
