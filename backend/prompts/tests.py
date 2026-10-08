from django.test import TestCase
from rest_framework.test import APIClient
from .models import Prompt, PromptVersion

class PromptApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_prompt_crud_and_versions(self):
        create = self.client.post("/api/prompts/", {"name": "Chicken Recipe", "category": "Recipe", "purpose": "Creates a chicken recipe", "prompt_text": "Create an easy chicken recipe using {ingredients}", "variables": ["ingredients"]}, format="json")
        self.assertEqual(create.status_code, 201)
        prompt_id = create.data["id"]
        self.assertEqual(Prompt.objects.count(), 1)
        update = self.client.put(f"/api/prompts/{prompt_id}/", {"name": "Better Chicken Recipe", "category": "Recipe", "purpose": "Creates a chicken recipe", "prompt_text": "Create an easy chicken recipe using {ingredients}", "variables": ["ingredients"]}, format="json")
        self.assertEqual(update.status_code, 200)
        version = self.client.post(f"/api/prompts/{prompt_id}/versions/", {"prompt_text": "Create an easy chicken recipe using {ingredients}", "score": 90}, format="json")
        self.assertEqual(version.status_code, 201)
        self.assertEqual(PromptVersion.objects.count(), 1)
        delete = self.client.delete(f"/api/prompts/{prompt_id}/")
        self.assertEqual(delete.status_code, 204)

    def test_prompt_optimization_and_scoring(self):
        optimized = self.client.post("/api/prompts/optimize/", {"prompt": "Make something with chicken and rice."})
        self.assertEqual(optimized.status_code, 200)
        self.assertIn("optimized", optimized.data)
        self.assertIn("score", optimized.data)
        scored = self.client.post("/api/prompts/analyse/", {"prompt": "Create an easy chicken recipe with servings and instructions."})
        self.assertEqual(scored.status_code, 200)
        self.assertIsInstance(scored.data["score"], int)
