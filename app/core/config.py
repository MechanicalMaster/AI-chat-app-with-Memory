from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    CORS_ORIGINS: str = "*"
    
    class Config:
        env_file = ".env"

settings = Settings() 