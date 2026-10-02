from .config import settings


def _demo_plan(user) -> str:
    return f"""FITBUDDY 7-DAY PLAN
Name: {user.username}
Goal: {user.goal.title()}
Intensity: {user.intensity.title()}

Day 1 - Full Body
Warm-up: 5-10 minutes of easy movement.
Main: bodyweight squats, wall/incline push-ups, glute bridges, bird-dogs.
Cooldown: gentle stretching.

Day 2 - Cardio & Mobility
Warm-up: 5 minutes.
Main: brisk walking or easy cycling, followed by light mobility.
Cooldown: relaxed stretching.

Day 3 - Upper Body & Core
Warm-up: 5-10 minutes.
Main: wall/incline push-ups, resistance-band rows if available, dead bugs, side plank.
Cooldown: gentle stretching.

Day 4 - Recovery
Easy walk and comfortable mobility work. Keep effort light.

Day 5 - Lower Body
Warm-up: 5-10 minutes.
Main: bodyweight squats, step-ups, glute bridges, calf raises.
Cooldown: gentle stretching.

Day 6 - Full Body Circuit
Warm-up: 5-10 minutes.
Main: repeat a few comfortable rounds of squats, incline push-ups, glute bridges and marching.
Cooldown: easy walking and stretching.

Day 7 - Rest & Recovery
Rest, hydrate, sleep well, and do light movement if comfortable.

Safety: Start comfortably, use good technique, stop if you feel pain, dizziness or feel unwell. This is general wellness information, not medical advice."""


def generate_workout_gemini(user) -> str:
    if not settings.gemini_api_key:
        if settings.demo_mode:
            return _demo_plan(user)
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    from google import genai

    client = genai.Client(api_key=settings.gemini_api_key)

    age_note = (
        "The user is under 18. Keep the plan focused on general wellness, "
        "age-appropriate activity, technique, recovery and enjoyment. Do not prescribe "
        "calorie restriction, supplements, extreme training, or weight-loss targets."
        if user.age < 18
        else "Keep recommendations general, sustainable and safety-conscious."
    )

    prompt = f"""
Create a safe, structured 7-day fitness plan for FitBuddy.

User:
- Name: {user.username}
- Age: {user.age}
- Weight: {user.weight} kg
- Goal: {user.goal}
- Preferred intensity: {user.intensity}

Requirements:
1. Give exactly Day 1 through Day 7.
2. Include a warm-up, main activity, and cooldown/recovery guidance.
3. For strength exercises, give simple sets/repetitions only where appropriate.
4. For cardio, use simple duration guidance.
5. Keep the plan realistic for a general web app user and include rest/recovery.
6. Do not diagnose conditions or claim medical outcomes.
7. Do not recommend unsafe challenges, extreme exercise, starvation, purging, or performance-enhancing drugs.
8. {age_note}
9. End with a short safety note.
Use plain text headings; do not use markdown tables.
"""

    response = client.models.generate_content(
        model=settings.workout_model,
        contents=prompt,
    )
    text = (response.text or "").strip()
    if not text:
        raise RuntimeError("Gemini returned an empty workout plan.")
    return text
