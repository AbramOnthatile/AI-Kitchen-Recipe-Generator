from django.conf import settings
from ai.services import generate_cooking_instructions, generate_recipe, generate_social_media_post
from history.models import GenerationHistory
from .models import Recipe


def match_ingredients(available, required):
    available_normalized = {item.strip().lower() for item in available}
    required_normalized = [item.strip().lower() for item in required]
    matched = [item for item in required_normalized if item in available_normalized]
    missing = [item for item in required_normalized if item not in available_normalized]
    percentage = round((len(matched) / len(required_normalized) * 100), 1) if required_normalized else 0
    return {"percentage": percentage, "matched": matched, "missing": missing, "available": [item for item in available_normalized if item in required_normalized]}


def generate_all(ingredients, platform="Instagram", servings=4, difficulty="Easy"):
    recipe = generate_recipe(ingredients, servings, difficulty)
    instructions = generate_cooking_instructions(recipe, ingredients)
    social = generate_social_media_post(recipe, platform, ingredients)
    match = match_ingredients(ingredients, recipe.get("ingredients", ingredients))
    recipe.update({"match_percentage": match["percentage"], "available_ingredients": match["available"], "missing_ingredients": match["missing"]})
    Recipe.objects.create(name=recipe["name"], description=recipe["description"], ingredients=recipe.get("ingredients", ingredients), additional_ingredients=recipe.get("additional_ingredients", []), servings=recipe.get("servings", servings), preparation_time=recipe.get("preparation_time", "20 minutes"), cooking_time=recipe.get("cooking_time", "30 minutes"), difficulty=recipe.get("difficulty", difficulty), instructions=instructions, match_percentage=match["percentage"], available_ingredients=match["available"], missing_ingredients=match["missing"])
    history = GenerationHistory.objects.create(ingredients=ingredients, recipe=recipe, cooking_instructions=instructions, social_media_post=social, platform=platform, prompt=recipe.get("name", ""), prompt_score=match["percentage"])
    return {"recipe": recipe, "instructions": instructions, "social_media_post": social, "match": match, "history_id": history.pk, "local_mode": not settings.AI_API_KEY}
