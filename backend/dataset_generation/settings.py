from typing import List, Optional
from dotenv import load_dotenv
import os
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    load_dotenv("../.env")

    # Modify to restrict to origin of your choice
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl | str] = [
        "*",
        # "http://localhost:3000"
    ]

    # OpenAI API settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1/")

    # Qdrant API Config
    QDRANT_URL: str = os.getenv("QDRANT_URL", "")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")


# Exporting for use
settings = AppSettings()
