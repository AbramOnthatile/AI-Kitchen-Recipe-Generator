import json
import os
import re
from urllib import error, request

from django.conf import settings


def _call_llm(prompt):
    if not settings.AI_API_KEY:
        return None
    payload = json.dumps({"model": settings.AI_MODEL, "messages": [{"role": "user", "content": prompt}], "temperature": 0.5}).encode()
    http_request = request.Request(settings.AI_API_URL, data=payload, headers={"Authorization": f"Bearer {settings.AI_API_KEY}", "Content-Type": "application/json"})
    try:
        with request.urlopen(http_request, timeout=20) as response:
            result = json.loads(response.read().decode())
        return result["choices"][0]["message"]["content"]
    except (error.URLError, KeyError, ValueError, TimeoutError):
        return None


def _json_from_response(content, fallback):
    if not content:
        return fallback
    try:
        match = re.search(r"```json\s*(.*?)\s*```", content, re.S)
        return json.loads(match.group(1) if match else content)
    except (json.JSONDecodeError, AttributeError):
        return fallback


def _normalize_ingredients(ingredients):
    return [item.strip().lower() for item in ingredients if item.strip()]


def _recipe_from_ingredients(ingredients, servings=4, difficulty="Easy"):
    normalized = _normalize_ingredients(ingredients)
    title = "Kitchen Surprise " + str(len(normalized) + 1)
    return {
        "name": title, "description": "A practical recipe built from the ingredients you have on hand.",
        "ingredients": normalized, "additional_ingredients": ["salt", "pepper", "oil"],
        "servings": servings, "preparation_time": "20 minutes", "cooking_time": "30 minutes",
        "difficulty": difficulty, "instructions": ["Prepare all ingredients and wash them well.", "Cook the main ingredients using your preferred method.", "Combine the cooked ingredients, season to taste, and serve."],
        "match_percentage": 100, "available_ingredients": normalized, "missing_ingredients": ["salt", "pepper", "oil"],
    }


def _generate_local_recipe(ingredients, servings, difficulty):
    recipe = _recipe_from_ingredients(ingredients, servings, difficulty)
    recipe.update({"name": f"Gemini Kitchen {recipe['ingredients'][0].title()} Bowl", "description": "A flexible meal made with the available kitchen ingredients and simple pantry seasonings."})
    return recipe


def generate_recipe(ingredients, servings=4, difficulty="Easy"):
    prompt = f"Create a recipe JSON object using exactly these ingredients: {', '.join(ingredients)}. Servings: {servings}. Difficulty: {difficulty}. Include name, description, ingredients, additional_ingredients, servings, preparation_time, cooking_time, difficulty, match_percentage, available_ingredients, missing_ingredients, and instructions."
    content = _call_llm(prompt)
    if content:
        parsed = _json_from_response(content, {})
        if parsed.get("name"):
            return parsed
    return _generate_local_recipe(ingredients, servings, difficulty)


def generate_cooking_instructions(recipe, ingredients):
    prompt = f"Provide beginner-friendly numbered cooking instructions for this recipe: {recipe.get('name', '')}. Ingredients: {', '.join(ingredients)}. Recipe details: {json.dumps(recipe, default=str)}"
    content = _call_llm(prompt)
    if content:
        if "\n" in content and not content.lstrip().startswith("{"):
            return [line.strip() for line in content.splitlines() if line.strip()][:10]
    return recipe.get("instructions", ["Prepare ingredients.", "Cook the main ingredients.", "Serve the finished dish."])


def generate_social_media_post(recipe, platform, ingredients):
    prompt = f"Write a social media post for {platform} based on this recipe: {recipe.get('name', '')}. Ingredients: {', '.join(ingredients)}. Include a call to action and hashtags. Return JSON with text, call_to_action, hashtags."
    content = _call_llm(prompt)
    if content:
        parsed = _json_from_response(content, {})
        if parsed.get("text"):
            return {"platform": platform, "text": parsed["text"], "call_to_action": parsed.get("call_to_action", "Try this recipe today!"), "hashtags": parsed.get("hashtags", ["#kitchen", "#recipe"])}
    return {"platform": platform, "text": f"Try {recipe.get('name', 'this recipe')} with ingredients from your kitchen! #Recipe #CookingTips", "call_to_action": "Save this recipe and try it tonight.", "hashtags": ["#recipe", "#cooking", "#food"]}


def _score_prompt(prompt):
    if not prompt:
        return 0
    checks = {"clear": bool(re.search(r"\b(use|create|make|generate|provide)\b", prompt, re.I)), "context": bool(re.search(r"\b(kitchen|ingredients|recipe|audience|constraints)\b", prompt, re.I)), "specificity": len(prompt) >= 45, "instructions": bool(re.search(r"\b(include|step|format|output|instructions)\b", prompt, re.I)), "format": bool(re.search(r"\bJSON|format|structure|fields\b", prompt, re.I)), "constraints": bool(re.search(r"\bservings|difficulty|time|budget|beginner|suitable\b", prompt, re.I))}
    raw = 55 + sum(7 if value else 0 for value in checks.values())
    return min(100, max(0, raw))


def analyse_prompt(prompt):
    content = _call_llm("Analyze this prompt for clarity, context, specificity, instructions, output format, and constraints. Return JSON with scores from 0 to 100 and reasons.") if settings.AI_API_KEY else None
    if content:
        parsed = _json_from_response(content, {})
        if parsed:
            score = int(parsed.get("score", _score_prompt(prompt)))
            return {"score": min(100, max(0, score)), "analysis": parsed.get("analysis", "AI-assisted analysis"), "breakdown": parsed.get("breakdown", {})}
    return {"score": _score_prompt(prompt), "analysis": "Local analysis estimates how complete the prompt is.", "breakdown": {"Clarity": 60, "Context": 60, "Specificity": 55, "Instructions": 50, "Output format": 50, "Constraints": 45}}


def optimize_prompt(prompt, goal=""):
    original = prompt.strip()
    content = _call_llm(f"Improve this prompt: {original}. Goal: {goal}. Add important context, constraints, audience, and output requirements. Return only the optimized prompt.") if settings.AI_API_KEY else None
    optimized = content.strip() if content else f"Create an easy, practical recipe using the available kitchen ingredients and the request: {original}. Include servings, preparation time, cooking time, required ingredients, missing ingredients, and clear beginner-friendly step-by-step instructions."
    return {"original": original, "optimized": optimized, "improvements": ["Added context", "Added specific instructions", "Added output requirements", "Added constraints", "Added target user"], "score": analyse_prompt(optimized)["score"]}


def fallback_generate(prompt, variables):
    rendered = prompt
    for key, value in variables.items():
        rendered = rendered.replace("{" + key + "}", str(value))
    return rendered
