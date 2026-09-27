from app.config import AI_DEMO_MODE, GEMINI_API_KEY, GOOGLE_API_KEY, GEMINI_FLASH_MODEL


def generate_nutrition_tip_with_flash(goal: str, weight: float) -> str:
    """
    Generate a simple nutrition/recovery tip.
    Demo mode works without an API key.
    """

    if AI_DEMO_MODE or not (GEMINI_API_KEY or GOOGLE_API_KEY):
        return (
            f"Nutrition Tip: For your goal of {goal}, focus on balanced meals "
            f"with enough protein, vegetables, whole grains, and water. "
            f"Based on your weight of {weight} kg, maintain a consistent "
            f"healthy eating routine and avoid skipping meals."
        )

    try:
        from google import genai

        api_key = GEMINI_API_KEY or GOOGLE_API_KEY
        client = genai.Client(api_key=api_key)

        prompt = f"""
        Give one short and practical nutrition tip for a person with:
        Goal: {goal}
        Weight: {weight} kg

        Keep the answer simple and safe.
        """

        response = client.models.generate_content(
            model=GEMINI_FLASH_MODEL,
            contents=prompt
        )

        return response.text.strip()

    except Exception:
        return (
            "Nutrition Tip: Eat balanced meals, stay hydrated, "
            "include protein and vegetables, and maintain a regular meal schedule."
        )