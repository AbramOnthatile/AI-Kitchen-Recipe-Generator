from unittest.mock import patch

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

    def test_local_fallback_recipe_is_realistic_and_not_provider_branded(self):
        response = self.client.post("/api/recipes/generate-all/", {"ingredients": ["chicken", "tomatoes", "onion", "garlic", "rice"], "platform": "Instagram"}, format="json")
        self.assertEqual(response.status_code, 201)
        recipe_name = response.data["recipe"]["name"]
        self.assertNotIn("Gemini", recipe_name)
        self.assertNotIn("Kitchen", recipe_name)
        self.assertTrue(len(response.data["instructions"]) >= 3)
        first_step = response.data["instructions"][0].lower()
        self.assertTrue(any(word in first_step for word in ["heat", "sauté", "cook", "add"]))

    @patch("recipes.services.generate_recipe_image")
    def test_generate_all_returns_image_metadata(self, mock_generate_image):
        mock_generate_image.return_value = {"status": "success", "url": "https://example.com/food.jpg"}

        response = self.client.post("/api/recipes/generate-all/", {"ingredients": ["Chicken", "Rice", "Tomato"], "platform": "Instagram"}, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertIn("image", response.data)
        self.assertEqual(response.data["image"]["status"], "success")
        self.assertTrue(response.data["image"]["url"].startswith("https://"))

    @patch("recipes.services.generate_recipe_image")
    def test_generate_all_keeps_recipe_when_image_generation_fails(self, mock_generate_image):
        mock_generate_image.return_value = {"status": "error", "error": "Image provider unavailable"}

        response = self.client.post("/api/recipes/generate-all/", {"ingredients": ["Chicken", "Rice", "Tomato"], "platform": "Instagram"}, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertIn("recipe", response.data)
        self.assertEqual(response.data["image"]["status"], "error")
        self.assertIn("image", response.data)

    def test_regenerate_image_endpoint_updates_recipe(self):
        recipe = Recipe.objects.create(
            name="Garlic Chicken Rice Bowl",
            description="A tasty rice bowl.",
            ingredients=["chicken", "rice", "garlic"],
            additional_ingredients=["salt"],
            servings=2,
            preparation_time="10 minutes",
            cooking_time="20 minutes",
            difficulty="Easy",
            instructions=["Cook everything."],
            match_percentage=80,
            available_ingredients=["chicken", "rice", "garlic"],
            missing_ingredients=["salt"],
        )

        with patch("recipes.views.generate_recipe_image") as mock_generate_image:
            mock_generate_image.return_value = {"status": "success", "url": "https://example.com/regenerated.png"}
            response = self.client.post(f"/api/recipes/{recipe.pk}/generate-image/", {}, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["image"]["status"], "success")
        self.assertEqual(response.data["image"]["url"], "https://example.com/regenerated.png")

    def test_ingredient_matching(self):
        result = match_ingredients(["Chicken", "Rice", "Tomato", "Onion"], ["Chicken", "Rice", "Tomato", "Onion", "Garlic"])
        self.assertEqual(result["percentage"], 80.0)
        self.assertEqual(result["missing"], ["garlic"])
