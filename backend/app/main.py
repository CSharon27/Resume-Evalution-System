# backend/app/main.py
"""
FastAPI application for Resume Evaluation System.
Exposes API endpoints for resume parsing, evaluation, and AI processing.
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import FRONTEND_URL

# Create FastAPI app instance
app = FastAPI(title="Resume Evaluation API")

# Enable CORS so frontend can call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Example health check endpoint
@app.get("/")
async def root():
    return {"message": "Resume Evaluation API is running!"}

# Setup spaCy NLP model (downloads if not present)
try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# TODO: Include your routers here
# from .routers import resume_router
# app.include_router(resume_router)
