from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # API Configuration
    OPENAI_API_KEY: str
    CORS_ORIGINS: str = "*"
    
    # Railway-specific settings
    PORT: Optional[int] = 8000
    RAILWAY_ENVIRONMENT: Optional[str] = os.getenv("RAILWAY_ENVIRONMENT")
    
    # System Configuration
    SYSTEM_PROMPT: str = "You are a helpful Channel Finance assistant. You help users with loan-related questions."
    
    class Config:
        env_file = ".env"

settings = Settings() 