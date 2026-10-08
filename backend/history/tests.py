from django.test import TestCase
from rest_framework.test import APIClient

class HistoryApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_history_is_stored_and_deleted(self):
        response = self.client.post("/api/history/", {"ingredients": ["Chicken"], "recipe": {"name": "Chicken"}, "cooking_instructions": ["Cook"], "social_media_post": {"text": "Post"}, "platform": "Instagram"}, format="json")
        self.assertEqual(response.status_code, 201)
        history_id = response.data["id"]
        self.assertEqual(self.client.get("/api/history/").status_code, 200)
        self.assertEqual(self.client.delete(f"/api/history/{history_id}/").status_code, 204)
