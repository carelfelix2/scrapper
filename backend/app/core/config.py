import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Scrapper - Web Scraping SaaS"
    PROJECT_DESCRIPTION: str = "A comprehensive web scraping platform for e-commerce and social commerce"
    VERSION: str = "0.1.0"
    
    # Environment
    ENVIRONMENT: str = os.getenv("FASTAPI_ENV", "development")
    DEBUG: bool = os.getenv("FASTAPI_DEBUG", "true").lower() == "true"
    
    # Server Configuration
    HOST: str = os.getenv("FASTAPI_HOST", "0.0.0.0")
    PORT: int = int(os.getenv("FASTAPI_PORT", 8000))
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/scrapper_db")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Celery
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")
    
    # CORS
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8000"]
    
    # Scraping Configuration
    PLAYWRIGHT_HEADLESS: bool = os.getenv("PLAYWRIGHT_HEADLESS", "true").lower() == "true"
    BROWSER_TIMEOUT: int = int(os.getenv("BROWSER_TIMEOUT", 30000))
    PROXY_LIST: list = os.getenv("PROXY_LIST", "").split(",") if os.getenv("PROXY_LIST") else []
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
