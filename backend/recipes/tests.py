from django.test import TestCase
from rest_framework.test import APIClient
from .models import Recipe
from .services import match_ingredients

class RecipeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_empty_ingredient_input_is_rejected(self):
        response = self.client.post("/api/recipes/generate/", {"ingredients": []})
        self.assertEqual(response.status_code, 400)
        self.assertIn("ingredients", response.data)

    def test_generate_all_uses_local_fallback(self):
        response = self.client.post("/api/recipes/generate-all/", {"ingredients": ["Chicken", "Rice", "Tomato"], "platform": "Instagram"}, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertIn("recipe", response.data)
        self.assertIn("instructions", response.data)
        self.assertIn("social_media_post", response.data)
        self.assertGreaterEqual(response.data["match"]["percentage"], 0)
        self.assertTrue(Recipe.objects.count())

    def test_ingredient_matching(self):
        result = match_ingredients(["Chicken", "Rice", "Tomato", "Onion"], ["Chicken", "Rice", "Tomato", "Onion", "Garlic"])
        self.assertEqual(result["percentage"], 80.0)
        self.assertEqual(result["missing"], ["garlic"])
