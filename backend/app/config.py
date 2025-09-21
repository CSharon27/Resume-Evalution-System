"""Configuration settings for the Resume Evaluation System."""

from typing import List
from pydantic_settings import BaseSettings
import os
# Load environment variables automatically from .env
class Settings(BaseSettings):
    """Application settings."""

    # API Configuration
    openai_api_key: str = ""  # Will be loaded from environment variable
    database_url: str = "sqlite:///./resume_evaluation.db"
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = int(os.getenv("PORT", 8000))

    # File Upload Settings
    max_file_size: int = 10485760  # 10MB
    allowed_extensions: List[str] = ["pdf", "docx"]
    upload_dir: str = "data/uploads"

    # Scoring Weights
    hard_match_weight: float = 0.4
    semantic_match_weight: float = 0.6

    # LLM Settings
    enable_llm: bool = True  # Enable LLM features (requires OpenAI API key)
    model_name: str = "gpt-3.5-turbo"
    temperature: float = 0.1
    max_tokens: int = 1000

    # Evaluation Thresholds
    high_suitability_threshold: float = 80.0
    medium_suitability_threshold: float = 60.0

    class Config:
        env_file = ".env"
        case_sensitive = False

# Create a settings instance
settings = Settings()
    





