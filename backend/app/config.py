# backend/app/config.py
"""
Configuration for Resume Evaluation System Backend.
Loads environment variables for API keys, database, and frontend URL.
"""

import os
from dotenv import load_dotenv

# Load variables from .env file if present
load_dotenv()

# OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Database URL (SQLAlchemy or any DB)
DATABASE_URL = os.getenv("DATABASE_URL")

# Frontend URL for CORS
FRONTEND_URL = os.getenv("FRONTEND_URL", "*")

# Other configurable settings
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
