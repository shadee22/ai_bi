import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # API Configuration
    api_v1_str: str = "/api/v1"
    project_name: str = "CSV Analysis API"
    version: str = "1.0.0"
    
    # CORS Configuration
    frontend_url: str = "http://localhost:3000"
    backend_url: str = "http://localhost:8000"
    
    # OpenAI Configuration
    openai_api_key: Optional[str] = None
    
    # File Upload Configuration
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_extensions: list = [".csv"]
    upload_dir: str = "uploads"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings() 