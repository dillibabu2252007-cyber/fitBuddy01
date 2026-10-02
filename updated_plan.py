from .config import settings


def _demo_update(original_plan: str, feedback: str) -> str:
    return f"""{original_plan}

UPDATED USING USER FEEDBACK
Feedback: {feedback}

Adjustment: Keep the same overall weekly structure while making the requested change
in a moderate and sustainable way. Add recovery time when needed and avoid painful or
extreme activity."""


def update_workout_plan(original_plan: str, feedback: str, age: int) -> str:
    if not settings.gemini_api_key:
        if settings.demo_mode:
            return _demo_update(original_plan, feedback)
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    from google import genai

    client = genai.Client(api_key=settings.gemini_api_key)
    prompt = f"""
Update this FitBuddy 7-day workout plan based on the user's feedback.

USER AGE: {age}
USER FEEDBACK:
{feedback}

ORIGINAL PLAN:
{original_plan}

Rules:
- Preserve the 7-day structure.
- Apply the feedback where it is reasonable.
- Keep activity safe, moderate and sustainable.
- Include recovery/rest.
- Do not prescribe extreme exercise, starvation, supplements, drugs, or unsafe challenges.
- If the user is under 18, do not create weight-loss targets or calorie restriction.
- Do not diagnose or treat medical conditions.
- Return the complete revised plan, not just the changes.
"""

    response = client.models.generate_content(
        model=settings.workout_model,
        contents=prompt,
    )
    text = (response.text or "").strip()
    if not text:
        raise RuntimeError("Gemini returned an empty updated plan.")
    return text
