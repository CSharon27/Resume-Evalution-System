# backend/app/main.py
"""
FastAPI application for Resume Evaluation System.
Exposes API endpoints for resume parsing, evaluation, and AI processing.
"""

import os
from fastapi import FastAPI, APIRouter, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.config import FRONTEND_URL
from datetime import datetime

# -----------------------------
# App setup
# -----------------------------
app = FastAPI(title="Resume Evaluation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Resume Evaluation API is running!"}

# -----------------------------
# Setup spaCy NLP
# -----------------------------
try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# -----------------------------
# In-memory "databases"
# -----------------------------
resumes_db = []
job_descriptions_db = []
evaluations_db = []

# -----------------------------
# Resumes Router
# -----------------------------
resumes_router = APIRouter()

@resumes_router.get("/")
async def list_resumes():
    return resumes_db

@resumes_router.post("/")
async def upload_resume(file: UploadFile = File(...)):
    upload_dir = "data/uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    # Add to in-memory DB
    resume_entry = {
        "id": len(resumes_db) + 1,
        "filename": file.filename,
        "student_name": "Unknown",
        "student_email": "Unknown",
        "created_at": datetime.now().isoformat()
    }
    resumes_db.append(resume_entry)
    return {"message": f"Resume '{file.filename}' uploaded successfully"}

# -----------------------------
# Job Descriptions Router
# -----------------------------
jobs_router = APIRouter()

@jobs_router.get("/")
async def list_job_descriptions():
    return job_descriptions_db

@jobs_router.post("/")
async def upload_job_description(file: UploadFile = File(...)):
    upload_dir = "data/job_descriptions"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    jd_entry = {
        "id": len(job_descriptions_db) + 1,
        "title": file.filename,
        "company": "Unknown",
        "location": "Unknown",
        "created_at": datetime.now().isoformat()
    }
    job_descriptions_db.append(jd_entry)
    return {"message": f"Job description '{file.filename}' uploaded successfully"}

# -----------------------------
# Evaluations Router
# -----------------------------
evaluations_router = APIRouter()

@evaluations_router.get("/")
async def list_evaluations():
    return evaluations_db

@evaluations_router.post("/")
async def create_evaluation(evaluation: dict):
    evaluation_entry = evaluation.copy()
    evaluation_entry["id"] = len(evaluations_db) + 1
    evaluation_entry["created_at"] = datetime.now().isoformat()
    evaluations_db.append(evaluation_entry)
    return evaluation_entry

# -----------------------------
# Register routers
# -----------------------------
app.include_router(resumes_router, prefix="/resumes", tags=["Resumes"])
app.include_router(jobs_router, prefix="/job-descriptions", tags=["Job Descriptions"])
app.include_router(evaluations_router, prefix="/evaluations", tags=["Evaluations"])
