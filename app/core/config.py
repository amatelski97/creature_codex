from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Database Configuration
    DATABASE_URL: str
    
    # API settings
    API_URL: str = "http://localhost:8000"  # Default value for REACT_APP_API_URL
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    
    # Other settings (e.g., environment mode, app title)
    DEBUG: bool = True  # Toggle debug mode for development

    class Config:
        env_file = "/home/tcc/tccodex/V2/app/.env"  # Correctly specifies the .env file path


# Create a singleton settings instance
settings = Settings()
