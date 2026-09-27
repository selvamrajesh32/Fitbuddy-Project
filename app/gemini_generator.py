from app.config import AI_DEMO_MODE, GEMINI_API_KEY, GOOGLE_API_KEY, GEMINI_MODEL


def generate_demo_workout(name, age, weight, goal, intensity):
    return {
        "user": name,
        "goal": goal,
        "intensity": intensity,
        "days": [
            {
                "day": "Day 1",
                "focus": "Full Body",
                "exercises": [
                    "Squats - 3 sets × 12 reps",
                    "Push-ups - 3 sets × 10 reps",
                    "Lunges - 3 sets × 10 reps",
                    "Plank - 3 × 30 seconds"
                ]
            },
            {
                "day": "Day 2",
                "focus": "Upper Body",
                "exercises": [
                    "Push-ups - 3 sets × 10 reps",
                    "Shoulder Press - 3 sets × 12 reps",
                    "Bicep Curls - 3 sets × 12 reps",
                    "Tricep Dips - 3 sets × 10 reps"
                ]
            },
            {
                "day": "Day 3",
                "focus": "Cardio",
                "exercises": [
                    "Brisk Walking - 20 minutes",
                    "Jumping Jacks - 3 × 30 seconds",
                    "High Knees - 3 × 30 seconds"
                ]
            },
            {
                "day": "Day 4",
                "focus": "Lower Body",
                "exercises": [
                    "Squats - 3 sets × 12 reps",
                    "Lunges - 3 sets × 10 reps",
                    "Glute Bridges - 3 sets × 15 reps",
                    "Calf Raises - 3 sets × 15 reps"
                ]
            },
            {
                "day": "Day 5",
                "focus": "Core",
                "exercises": [
                    "Crunches - 3 sets × 15 reps",
                    "Leg Raises - 3 sets × 10 reps",
                    "Plank - 3 × 30 seconds",
                    "Bicycle Crunches - 3 sets × 15 reps"
                ]
            },
            {
                "day": "Day 6",
                "focus": "Full Body",
                "exercises": [
                    "Bodyweight Squats - 3 sets × 15 reps",
                    "Push-ups - 3 sets × 10 reps",
                    "Mountain Climbers - 3 × 30 seconds",
                    "Plank - 3 × 30 seconds"
                ]
            },
            {
                "day": "Day 7",
                "focus": "Recovery",
                "exercises": [
                    "Light Walking - 20 minutes",
                    "Full Body Stretching - 10 minutes",
                    "Deep Breathing - 5 minutes"
                ]
            }
        ]
    }


def generate_workout_gemini(name, age, weight, goal, intensity):
    """
    Generate a personalized workout plan.
    Demo mode works without a Gemini API key.
    """

    if AI_DEMO_MODE or not (GEMINI_API_KEY or GOOGLE_API_KEY):
        return generate_demo_workout(
            name=name,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity
        )

    try:
        from google import genai

        api_key = GEMINI_API_KEY or GOOGLE_API_KEY
        client = genai.Client(api_key=api_key)

        prompt = f"""
Create a personalized 7-day workout plan.

User name: {name}
Age: {age}
Weight: {weight} kg
Fitness goal: {goal}
Workout intensity: {intensity}

Give a simple and safe plan for each of the 7 days.
Include exercises, sets/reps or duration, and a recovery day.
"""

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        return {
            "user": name,
            "goal": goal,
            "intensity": intensity,
            "days": response.text
        }

    except Exception:
        return generate_demo_workout(
            name=name,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity
        )