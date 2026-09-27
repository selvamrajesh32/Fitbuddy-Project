import os

from dotenv import load_dotenv


# Load .env file
load_dotenv()


APP_NAME = os.getenv(
    "APP_NAME",
    "FitBuddy AI"
)


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./fitbuddy.db"
)


GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    ""
)


GOOGLE_API_KEY = os.getenv(
    "GOOGLE_API_KEY",
    ""
)


GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-pro"
)


GEMINI_FLASH_MODEL = os.getenv(
    "GEMINI_FLASH_MODEL",
    "gemini-2.5-flash"
)


AI_DEMO_MODE = os.getenv(
    "AI_DEMO_MODE",
    "true"
).lower() == "true"


ADMIN_TOKEN = os.getenv(
    "ADMIN_TOKEN",
    ""
)


def ai_is_configured():
    return bool(
        GEMINI_API_KEY or GOOGLE_API_KEY
    )