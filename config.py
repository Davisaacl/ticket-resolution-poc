# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENV: str = "dev"                  # dev|stage|prod
    LOG_LEVEL: str = "INFO"
    GEMINI_API_KEY: str | None = None
    GEMINI_MODEL: str = "gemini-2.0-flash"
    EMBED_MODEL: str = "all-MiniLM-L6-v2"
    KB_INDEX_PATH: str = "kb.index"
    KB_META_PATH: str = "kb_meta.json"

    class Config:
        env_file = ".env"             # loads your .env automatically

settings = Settings()
