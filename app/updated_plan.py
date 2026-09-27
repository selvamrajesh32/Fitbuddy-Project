from app.config import AI_DEMO_MODE, GEMINI_API_KEY, GOOGLE_API_KEY, GEMINI_MODEL


def update_demo_plan(original_plan, feedback, goal, intensity):
    """
    Create a simple revised workout plan based on user feedback.
    """

    return {
        "updated": True,
        "goal": goal,
        "intensity": intensity,
        "feedback": feedback,
        "message": "Workout plan updated based on your feedback.",
        "days": [
            {
                "day": "Day 1",
                "focus": "Light Full Body",
                "exercises": [
                    "Bodyweight Squats - 2 sets × 10 reps",
                    "Wall Push-ups - 2 sets × 10 reps",
                    "Glute Bridges - 2 sets × 12 reps",
                    "Light Stretching - 5 minutes"
                ]
            },
            {
                "day": "Day 2",
                "focus": "Cardio",
                "exercises": [
                    "Walking - 20 minutes",
                    "Light Jogging - 10 minutes"
                ]
            },
            {
                "day": "Day 3",
                "focus": "Upper Body",
                "exercises": [
                    "Wall Push-ups - 3 sets × 10 reps",
                    "Arm Circles - 3 × 30 seconds",
                    "Shoulder Raises - 2 sets × 12 reps"
                ]
            },
            {
                "day": "Day 4",
                "focus": "Recovery",
                "exercises": [
                    "Light Walking - 15 minutes",
                    "Full Body Stretching - 10 minutes"
                ]
            },
            {
                "day": "Day 5",
                "focus": "Lower Body",
                "exercises": [
                    "Squats - 2 sets × 10 reps",
                    "Lunges - 2 sets × 8 reps",
                    "Calf Raises - 2 sets × 12 reps"
                ]
            },
            {
                "day": "Day 6",
                "focus": "Core",
                "exercises": [
                    "Crunches - 2 sets × 12 reps",
                    "Plank - 2 × 20 seconds",
                    "Bird Dog - 2 sets × 10 reps"
                ]
            },
            {
                "day": "Day 7",
                "focus": "Recovery",
                "exercises": [
                    "Light Walking - 20 minutes",
                    "Stretching - 10 minutes",
                    "Deep Breathing - 5 minutes"
                ]
            }
        ]
    }


def update_workout_plan(original_plan, feedback, goal, intensity):
    """
    Update an existing workout plan using user feedback.
    """

    if AI_DEMO_MODE or not (GEMINI_API_KEY or GOOGLE_API_KEY):
        return update_demo_plan(
            original_plan=original_plan,
            feedback=feedback,
            goal=goal,
            intensity=intensity
        )

    try:
        from google import genai

        api_key = GEMINI_API_KEY or GOOGLE_API_KEY
        client = genai.Client(api_key=api_key)

        prompt = f"""
Update the following workout plan based on the user's feedback.

Goal: {goal}
Intensity: {intensity}

Original plan:
{original_plan}

User feedback:
{feedback}

Create a revised 7-day workout plan.
Keep it simple, safe, and practical.
"""

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        return {
            "updated": True,
            "goal": goal,
            "intensity": intensity,
            "feedback": feedback,
            "days": response.text
        }

    except Exception:
        return update_demo_plan(
            original_plan=original_plan,
            feedback=feedback,
            goal=goal,
            intensity=intensity
        )