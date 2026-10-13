import json
from urllib import error, request

from django.conf import settings


def _missing_image_config():
    missing = []
    if not getattr(settings, "IMAGE_API_KEY", None):
        missing.append("IMAGE_API_KEY")
    if not getattr(settings, "IMAGE_API_URL", None):
        missing.append("IMAGE_API_URL")
    if not getattr(settings, "IMAGE_MODEL", None):
        missing.append("IMAGE_MODEL")
    return missing


def _build_image_prompt(recipe, ingredients):
    name = (recipe or {}).get("name") or "This dish"
    description = (recipe or {}).get("description") or "A flavourful homemade meal"
    ingredient_list = ingredients or (recipe or {}).get("ingredients") or []
    ingredients_text = ", ".join(str(item) for item in ingredient_list)
    instruction_text = " ".join(str(step) for step in ((recipe or {}).get("instructions") or [])[:3])

    return (
        f"Create a photorealistic food photograph of {name}. "
        f"Show a finished plated dish that matches this recipe: {description}. "
        f"Use the key ingredients: {ingredients_text}. "
        f"Cooking method and intended appearance: {instruction_text}. "
        "Use natural kitchen lighting, rich textures, appetizing colors, and a polished restaurant-style presentation. "
        "Close-up three-quarter view, clean background, realistic food styling, no text, no watermark, no logo, no branding."
    )


def generate_recipe_image(recipe, ingredients=None):
    missing = _missing_image_config()
    if missing:
        return {
            "status": "unavailable",
            "error": f"Image API configuration is incomplete: {', '.join(missing)}.",
            "url": None,
        }

    prompt = _build_image_prompt(recipe, ingredients)
    payload = {
        "model": settings.IMAGE_MODEL,
        "prompt": prompt,
        "size": "1024x1024",
        "quality": "high",
        "response_format": "b64_json",
    }

    headers = {
        "Authorization": f"Bearer {settings.IMAGE_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        request_obj = request.Request(settings.IMAGE_API_URL, data=json.dumps(payload).encode("utf-8"), headers=headers)
        with request.urlopen(request_obj, timeout=30) as response:
            raw = response.read().decode("utf-8", errors="replace")
    except (error.HTTPError, error.URLError, TimeoutError, ValueError) as exc:
        detail = ""
        try:
            detail = exc.read().decode("utf-8", errors="replace") if hasattr(exc, "read") else str(exc)
        except Exception:
            detail = str(exc)
        return {
            "status": "error",
            "error": f"Image generation failed: {detail[:300] or str(exc)}",
            "url": None,
        }

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {"status": "error", "error": "Image generation returned an invalid response.", "url": None}

    if isinstance(data, dict):
        image_candidates = data.get("data") or []
        for candidate in image_candidates:
            if isinstance(candidate, dict):
                if candidate.get("url"):
                    return {"status": "success", "url": candidate["url"], "prompt": prompt}
                if candidate.get("b64_json"):
                    return {
                        "status": "success",
                        "url": f"data:image/png;base64,{candidate['b64_json']}",
                        "prompt": prompt,
                    }

        if data.get("url"):
            return {"status": "success", "url": data["url"], "prompt": prompt}
        if data.get("b64_json"):
            return {"status": "success", "url": f"data:image/png;base64,{data['b64_json']}", "prompt": prompt}

        if data.get("error"):
            return {"status": "error", "error": str(data["error"]), "url": None}

    return {"status": "error", "error": "Image generation returned no usable image data.", "url": None}
