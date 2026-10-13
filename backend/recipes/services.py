from django.conf import settings

from ai.image_service import generate_recipe_image
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
    image = generate_recipe_image(recipe, ingredients)

    recipe.update({
        "match_percentage": match["percentage"],
        "available_ingredients": match["available"],
        "missing_ingredients": match["missing"],
        "preparation_time": recipe.get("prep_time") or recipe.get("preparation_time") or "15 minutes",
        "cooking_time": recipe.get("cook_time") or recipe.get("cooking_time") or "25 minutes",
        "image": image,
    })

    saved_recipe = Recipe.objects.create(
        name=recipe["name"],
        description=recipe["description"],
        ingredients=recipe.get("ingredients", ingredients),
        additional_ingredients=recipe.get("additional_ingredients", []),
        servings=recipe.get("servings", servings),
        preparation_time=recipe.get("preparation_time", "15 minutes"),
        cooking_time=recipe.get("cooking_time", "25 minutes"),
        difficulty=recipe.get("difficulty", difficulty),
        instructions=instructions,
        match_percentage=match["percentage"],
        available_ingredients=match["available"],
        missing_ingredients=match["missing"],
        image_url=image.get("url") or "",
        image_status=image.get("status", "unavailable"),
        image_error=image.get("error", ""),
    )
    history = GenerationHistory.objects.create(
        ingredients=ingredients,
        recipe=recipe,
        cooking_instructions=instructions,
        social_media_post=social,
        platform=platform,
        prompt=recipe.get("name", ""),
        prompt_score=match["percentage"],
        image_url=image.get("url") or "",
        image_status=image.get("status", "unavailable"),
        image_error=image.get("error", ""),
    )
    local_mode = recipe.get("source") == "local" or not getattr(settings, "AI_API_KEY", None)
    return {"recipe": recipe, "instructions": instructions, "social_media_post": social, "image": image, "match": match, "history_id": history.pk, "recipe_id": saved_recipe.pk, "local_mode": local_mode}
