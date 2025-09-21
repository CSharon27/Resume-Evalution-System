"""
FastAPI application for Resume Evaluation System.
Render-ready version for deployment.
"""

import os
import shutil
from typing import List, Optional
import json

from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel

# Import your internal modules
from app.database import get_db
from app.services.resume_service import ResumeService
from app.config import settings
from app.models.database import ResumeEvaluation

# Create FastAPI app
app = FastAPI(
    title="Resume Evaluation System",
    description="AI-powered resume evaluation against job descriptions",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize service
resume_service = ResumeService()

# Ensure upload directory exists
os.makedirs(settings.upload_dir, exist_ok=True)

# === Startup Event ===
@app.on_event("startup")
def startup_event():
    """Run once at startup to create DB tables."""
    from app.database import create_tables
    create_tables()


# === Pydantic Models ===
class JobDescriptionCreate(BaseModel):
    title: str
    company: str
    location: str
    content: str

class ResumeEvaluationRequest(BaseModel):
    resume_id: int
    job_description_id: int

class ResumeEvaluationResponse(BaseModel):
    id: int
    relevance_score: float
    hard_match_score: float
    semantic_match_score: float
    verdict: str
    missing_skills: List[str]
    missing_certifications: List[str]
    missing_projects: List[str]
    strengths: List[str]
    weaknesses: List[str]
    improvement_suggestions: str
    overall_feedback: str
    evaluation_time: float


# === API Endpoints ===
@app.get("/")
async def root():
    return {"message": "Resume Evaluation System API", "version": "1.0.0"}


@app.post("/upload/resume")
async def upload_resume(
    file: UploadFile = File(...),
    student_name: str = Form(...),
    student_email: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        if not file.filename.lower().endswith(('.pdf', '.docx')):
            raise HTTPException(status_code=400, detail="Only PDF and DOCX files are allowed")

        file_path = os.path.join(settings.upload_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        resume = resume_service.save_resume(db, file_path, student_name, student_email)

        return {
            "message": "Resume uploaded successfully",
            "resume_id": resume.id,
            "filename": resume.filename,
            "student_name": resume.student_name,
            "student_email": resume.student_email
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload/job-description")
async def upload_job_description(job_data: JobDescriptionCreate, db: Session = Depends(get_db)):
    try:
        job_description = resume_service.save_job_description(
            db,
            job_data.content,
            job_data.title,
            job_data.company,
            job_data.location
        )
        return {
            "message": "Job description uploaded successfully",
            "job_description_id": job_description.id,
            "title": job_description.title,
            "company": job_description.company,
            "location": job_description.location
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/evaluate")
async def evaluate_resume(evaluation_request: ResumeEvaluationRequest, db: Session = Depends(get_db)):
    try:
        evaluation = resume_service.evaluate_resume_against_job(
            db,
            evaluation_request.resume_id,
            evaluation_request.job_description_id
        )
        return ResumeEvaluationResponse(
            id=evaluation.id,
            relevance_score=evaluation.relevance_score,
            hard_match_score=evaluation.hard_match_score,
            semantic_match_score=evaluation.semantic_match_score,
            verdict=evaluation.verdict,
            missing_skills=json.loads(evaluation.missing_skills or '[]'),
            missing_certifications=json.loads(evaluation.missing_certifications or '[]'),
            missing_projects=json.loads(evaluation.missing_projects or '[]'),
            strengths=json.loads(evaluation.strengths or '[]'),
            weaknesses=json.loads(evaluation.weaknesses or '[]'),
            improvement_suggestions=evaluation.improvement_suggestions,
            overall_feedback=evaluation.overall_feedback,
            evaluation_time=evaluation.evaluation_time
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/resumes")
async def get_resumes(db: Session = Depends(get_db)):
    resumes = resume_service.get_all_resumes(db)
    return [
        {
            "id": r.id,
            "filename": r.filename,
            "student_name": r.student_name,
            "student_email": r.student_email,
            "created_at": r.created_at.isoformat()
        } for r in resumes
    ]


@app.get("/job-descriptions")
async def get_job_descriptions(db: Session = Depends(get_db)):
    jobs = resume_service.get_all_job_descriptions(db)
    return [
        {
            "id": j.id,
            "title": j.title,
            "company": j.company,
            "location": j.location,
            "created_at": j.created_at.isoformat()
        } for j in jobs
    ]


# === Uvicorn Runner (Render-ready) ===
#if __name__ == "__main__":
    #port = int(os.environ.get("PORT", 8000))
    #uvicorn.run("app.main:app", host="0.0.0.0", port=port)

