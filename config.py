import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "").strip()
    workout_model: str = os.getenv("GEMINI_WORKOUT_MODEL", "gemini-3.7-flash")
    tip_model: str = os.getenv("GEMINI_TIP_MODEL", "gemini-3.5-flash")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./fitbuddy.db")
    demo_mode: bool = os.getenv("DEMO_MODE", "true").lower() == "true"


settings = Settings()
