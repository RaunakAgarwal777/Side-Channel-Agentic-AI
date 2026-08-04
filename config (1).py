"""
config.py - Central configuration for SideChannel Sentinel OS backend.
Loads settings from environment variables with sane defaults.
"""

import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    APP_NAME: str = "SideChannel Sentinel OS"
    ENV: str = os.getenv("ENV", "development")
    DEBUG: bool = ENV == "development"

    # API
    API_V1_PREFIX: str = "/api/v1"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./sentinel.db")

    # Vector DB
    VECTOR_DB_URL: str = os.getenv("VECTOR_DB_URL", "http://localhost:6333")  # Qdrant default
    VECTOR_COLLECTION: str = "sidechannel_knowledge"

    # LLM
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "ollama")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "llama3.1")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    # Auth
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
