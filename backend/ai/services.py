import json
import re
from urllib import error, request

from django.conf import settings


def _missing_ai_config():
    missing = []
    if not getattr(settings, "AI_API_KEY", None):
        missing.append("AI_API_KEY")
    if not getattr(settings, "AI_API_URL", None):
        missing.append("AI_API_URL")
    if not getattr(settings, "AI_MODEL", None):
        missing.append("AI_MODEL")
    return missing


def _log_ai_error(message):
    print(message)


def _call_llm(prompt):
    missing = _missing_ai_config()
    if missing:
        _log_ai_error(f"AI configuration is incomplete. Check {', '.join(missing)}.")
        return None

    payload = json.dumps({
        "model": settings.AI_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5,
    }).encode("utf-8")

    headers = {
        "Authorization": f"Bearer {settings.AI_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        request_obj = request.Request(settings.AI_API_URL, data=payload, headers=headers)
        with request.urlopen(request_obj, timeout=20) as response:
            result = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        _log_ai_error(f"AI request failed: HTTP {exc.code}")
        if detail:
            try:
                parsed_error = json.loads(detail)
                message = parsed_error.get("error", {}).get("message") or parsed_error.get("message")
                if message:
                    _log_ai_error(f"AI provider error: {message}")
            except (TypeError, ValueError):
                _log_ai_error(f"AI provider response: {detail[:250]}")
        return None
    except (error.URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
        _log_ai_error(f"AI request failed: {exc}")
        return None

    if result.get("error"):
        _log_ai_error(f"AI response error: {result['error']}")
        return None

    choices = result.get("choices") or []
    if not choices:
        _log_ai_error("AI response parsing failed: no choices returned.")
        return None

    message = choices[0].get("message", {})
    content = message.get("content")
    if isinstance(content, list):
        text = "".join(part.get("text", "") for part in content if isinstance(part, dict))
        if text:
            return text
    if isinstance(content, str):
        return content

    _log_ai_error("AI response parsing failed: invalid content format.")
    return None


def _json_from_response(content, fallback):
    if not content:
        return fallback
    if not isinstance(content, str):
        return content if isinstance(content, dict) else fallback

    cleaned = content.strip()
    match = re.search(r"```(?:json)?\s*(.*?)\s*```", cleaned, re.S)
    candidate = match.group(1) if match else cleaned
    try:
        return json.loads(candidate)
    except (json.JSONDecodeError, TypeError):
        compact = re.search(r"\{.*\}", cleaned, re.S)
        if compact:
            try:
                return json.loads(compact.group(0))
            except json.JSONDecodeError:
                return fallback
        return fallback


def _normalize_ingredients(ingredients):
    return [item.strip().lower() for item in ingredients if item and item.strip()]


def _title_from_ingredients(ingredients):
    normalized = _normalize_ingredients(ingredients)
    if not normalized:
        return "Garden Herb Skillet"

    if "chicken" in normalized and "rice" in normalized:
        return "Garlic Chicken and Tomato Rice Skillet"
    if "beef" in normalized and "potato" in normalized:
        return "Savory Beef and Potato Skillet"
    if "egg" in normalized and "tomato" in normalized:
        return "Tomato Egg and Herb Skillet"
    if "pasta" in normalized and "tomato" in normalized:
        return "Tomato Herb Pasta"
    if "rice" in normalized and "tomato" in normalized:
        return "Tomato Rice and Veggie Skillet"

    nice_name = normalized[0].replace("-", " ").title()
    return f"{nice_name} and Veggie Skillet"


def _instruction_list(raw_steps):
    if isinstance(raw_steps, list):
        ordered_steps = []
        for step in raw_steps:
            if isinstance(step, dict):
                title = step.get("title")
                description = step.get("description") or step.get("text")
                if title and description:
                    ordered_steps.append(f"{title}: {description}")
                elif description:
                    ordered_steps.append(description)
                elif title:
                    ordered_steps.append(str(title))
            elif isinstance(step, str) and step.strip():
                ordered_steps.append(step.strip())
        if ordered_steps:
            return ordered_steps
    return [
        "Heat a large pan over medium heat and add a little oil.",
        "Add the aromatics and cook until softened and fragrant.",
        "Add the main protein and cook until browned and fully cooked through.",
        "Stir in the remaining vegetables and seasonings, then simmer until the flavours combine.",
        "Taste and adjust seasoning before serving warm.",
    ]


def _fallback_recipe(ingredients, servings=4, difficulty="Easy"):
    normalized = _normalize_ingredients(ingredients)
    title = _title_from_ingredients(normalized)
    additional = ["olive oil", "salt", "black pepper", "garlic powder"]
    instructions = [
        "Heat a large skillet over medium heat and add 1 tablespoon of oil.",
        "Add the onion and garlic, then cook for 3 to 4 minutes until softened and fragrant.",
        "Add the chicken and cook for 6 to 8 minutes, stirring occasionally, until lightly browned and cooked through.",
        "Stir in the tomatoes and any remaining vegetables, then cook for another 4 to 5 minutes until the tomatoes soften and release their juices.",
        "Add the rice and a splash of water, reduce the heat to low, and simmer for 8 to 10 minutes until the rice is tender and the mixture is glossy.",
        "Taste and adjust the seasoning before serving warm with extra herbs or a squeeze of lemon if you have it.",
    ]
    return {
        "name": title,
        "description": "A practical home-style dish using your available ingredients and a few pantry basics for extra flavour.",
        "ingredients": normalized,
        "additional_ingredients": additional,
        "servings": servings,
        "prep_time": "15 minutes",
        "cook_time": "25 minutes",
        "difficulty": difficulty,
        "instructions": instructions,
        "available_ingredients": normalized,
        "missing_ingredients": sorted(set(additional) - set(normalized)),
        "source": "local",
    }


def generate_recipe(ingredients, servings=4, difficulty="Easy"):
    prompt = (
        "You are an experienced home chef and recipe developer.\n"
        "Create a realistic recipe using the user's ingredients.\n"
        f"Available ingredients: {', '.join(ingredients)}.\n"
        f"Servings: {servings}.\n"
        f"Difficulty: {difficulty}.\n"
        "Important requirements:\n"
        "- Use the available ingredients as the main ingredients.\n"
        "- Do not invent ingredients unless they are basic pantry staples.\n"
        "- Clearly list additional ingredients required.\n"
        "- Return valid JSON only.\n"
        "- Do not mention AI, Gemini, or provider names.\n"
        "- Include realistic quantities and beginner-friendly cooking guidance.\n"
        "- Use these keys exactly: name, description, servings, prep_time, cook_time, difficulty, ingredients, additional_ingredients, available_ingredients, instructions.\n"
        "Return this structure:\n"
        "{\n"
        "  \"name\": \"Recipe title\",\n"
        "  \"description\": \"Short summary\",\n"
        "  \"servings\": 4,\n"
        "  \"prep_time\": \"15 minutes\",\n"
        "  \"cook_time\": \"25 minutes\",\n"
        "  \"difficulty\": \"Easy\",\n"
        "  \"ingredients\": [\"ingredient 1\", \"ingredient 2\"],\n"
        "  \"additional_ingredients\": [\"salt\", \"pepper\", \"olive oil\"],\n"
        "  \"available_ingredients\": [\"ingredient 1\", \"ingredient 2\"],\n"
        "  \"instructions\": [\n"
        "    {\"step\": 1, \"title\": \"Sauté aromatics\", \"description\": \"Heat the pan...\", \"duration\": \"5 minutes\"},\n"
        "    {\"step\": 2, \"title\": \"Cook the main ingredient\", \"description\": \"Add ...\", \"duration\": \"8 minutes\"}\n"
        "  ]\n"
        "}\n"
    )
    content = _call_llm(prompt)
    if content:
        parsed = _json_from_response(content, {})
        if isinstance(parsed, dict):
            recipe = parsed.get("recipe", parsed)
            name = recipe.get("name")
            if name and not re.search(r"Gemini|AI\b|Local Demo|provider", name, re.I):
                normalized_ingredients = recipe.get("ingredients") or ingredients
                instructions = _instruction_list(recipe.get("instructions") or [])
                return {
                    "name": name,
                    "description": recipe.get("description") or "A satisfying meal built from your available ingredients.",
                    "ingredients": normalized_ingredients,
                    "additional_ingredients": recipe.get("additional_ingredients") or ["salt", "pepper", "oil"],
                    "servings": recipe.get("servings") or servings,
                    "prep_time": recipe.get("prep_time") or recipe.get("preparation_time") or "15 minutes",
                    "cook_time": recipe.get("cook_time") or recipe.get("cooking_time") or "25 minutes",
                    "difficulty": recipe.get("difficulty") or difficulty,
                    "available_ingredients": recipe.get("available_ingredients") or normalized_ingredients,
                    "instructions": instructions,
                    "source": "ai",
                }
    return _fallback_recipe(ingredients, servings, difficulty)


def generate_cooking_instructions(recipe, ingredients):
    prompt = (
        "You are an experienced home cook. Based on this recipe, write beginner-friendly cooking steps.\n"
        f"Recipe name: {recipe.get('name', '')}\n"
        f"Ingredients: {', '.join(ingredients)}\n"
        f"Recipe details: {json.dumps(recipe, default=str)}\n"
        "Requirements:\n"
        "- Use clear numbered steps.\n"
        "- Include realistic timing and method.\n"
        "- Explain how to tell when food is ready.\n"
        "- Keep it practical and beginner-friendly.\n"
        "- Return JSON only with a list of step objects in this format: [{\"step\": 1, \"title\": \"\", \"description\": \"\", \"duration\": \"\"}].\n"
    )
    content = _call_llm(prompt)
    if content:
        parsed = _json_from_response(content, [])
        if isinstance(parsed, list):
            steps = _instruction_list(parsed)
            if steps:
                return steps
        if isinstance(parsed, dict):
            instructions = parsed.get("instructions") or parsed.get("steps") or []
            steps = _instruction_list(instructions)
            if steps:
                return steps
    return recipe.get("instructions") or _fallback_recipe(ingredients).get("instructions")


def generate_social_media_post(recipe, platform, ingredients):
    prompt = (
        "Write a compelling social media caption for this recipe.\n"
        f"Recipe: {recipe.get('name', '')}\n"
        f"Available ingredients: {', '.join(ingredients)}\n"
        f"Description: {recipe.get('description', '')}\n"
        "Requirements:\n"
        "- Do not mention AI, Gemini, or Local Demo Mode.\n"
        "- Return valid JSON only.\n"
        "- Include keys: text, call_to_action, hashtags.\n"
        "- Include a short appetizing description and 5-10 relevant hashtags.\n"
    )
    content = _call_llm(prompt)
    if content:
        parsed = _json_from_response(content, {})
        if isinstance(parsed, dict):
            text = parsed.get("text")
            if text:
                return {
                    "platform": platform,
                    "text": text,
                    "call_to_action": parsed.get("call_to_action") or "Save this recipe and make it tonight.",
                    "hashtags": parsed.get("hashtags") or ["#homecooking", "#recipe", "#familydinner"],
                }
    title = recipe.get("name", "This recipe")
    hashtags = ["#homecooking", "#recipe", "#easymeals", "#familydinner"]
    return {
        "platform": platform,
        "text": f"{title} is the kind of comforting, flavour-packed meal that turns a few ingredients into a satisfying dinner. Ready to cook and perfect for busy evenings.",
        "call_to_action": "Save this recipe and share it with someone who loves good food.",
        "hashtags": hashtags,
    }


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
