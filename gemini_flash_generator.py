from .config import settings


def generate_nutrition_tip_with_flash(goal: str, age: int) -> str:
    if not settings.gemini_api_key:
        if settings.demo_mode:
            tips = {
                "weight loss": "Build balanced meals around vegetables or fruit, a protein source and regular meals. Avoid extreme dieting.",
                "muscle gain": "Include a protein-rich food with regular meals and prioritize enough food, hydration and sleep.",
                "general wellness": "Aim for regular meals, varied foods, hydration and consistent sleep.",
                "flexibility": "Support recovery with balanced meals, hydration and regular sleep.",
            }
            return tips.get(goal, "Choose varied foods, stay hydrated and prioritize regular sleep.")
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    from google import genai

    client = genai.Client(api_key=settings.gemini_api_key)
    prompt = f"""
Give one concise nutrition or recovery tip for a FitBuddy user whose goal is "{goal}".
The user is {age} years old.
Do not prescribe calorie restriction, supplements, fasting, or medical treatment.
If the user is under 18, focus only on balanced nutrition, hydration, recovery and healthy routines.
Return 2-4 simple sentences.
"""
    response = client.models.generate_content(
        model=settings.tip_model,
        contents=prompt,
    )
    text = (response.text or "").strip()
    if not text:
        raise RuntimeError("Gemini returned an empty nutrition tip.")
    return text
