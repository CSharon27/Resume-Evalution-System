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

# Health check endpoint
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

# -----------------------------
# Include Routers for Resources
# -----------------------------
from fastapi import APIRouter
from fastapi import UploadFile, File

# --- Resumes Router ---
resumes_router = APIRouter()

@resumes_router.get("/")
async def list_resumes():
    return {"resumes": []}

@resumes_router.post("/")
async def upload_resume(file: UploadFile = File(...)):
    # Example: Save file to data/uploads
    upload_dir = "data/uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"message": f"Resume '{file.filename}' uploaded successfully"}

# --- Job Descriptions Router ---
jobs_router = APIRouter()

@jobs_router.get("/")
async def list_job_descriptions():
    return {"job_descriptions": []}

# --- Evaluations Router ---
evaluations_router = APIRouter()

@evaluations_router.get("/")
async def list_evaluations():
    return {"evaluations": []}

# Register routers with prefixes
app.include_router(resumes_router, prefix="/resumes", tags=["Resumes"])
app.include_router(jobs_router, prefix="/job-descriptions", tags=["Job Descriptions"])
app.include_router(evaluations_router, prefix="/evaluations", tags=["Evaluations"])
