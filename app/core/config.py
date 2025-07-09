# app/core/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    MAX_FILE_SIZE_MB: int = 5
    ALLOWED_EXTENSIONS: tuple = ("pdf", "docx", "txt")
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY")
    JWT_SECRET: str = os.getenv("JWT_SECRET")
    MONGO_URI: str = os.getenv("MONGO_URI")


settings = Settings()
