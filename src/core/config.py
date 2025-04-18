# app/core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    debug: bool = True  # Enable debugging
    PROJECT_NAME: str = "Talk to PDF"
    API_V1_STR: str = "/api"
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGO: str = "HS256",
    extra: str = "allow"
    OPENAI_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
