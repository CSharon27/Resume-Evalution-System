"""
HireLens FastAPI Backend
Main application and endpoints
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List
import uuid
from datetime import datetime
from pathlib import Path

from config.config import UPLOAD_DIR, API_HOST, API_PORT
from config.models import (
    EvaluateRequest, EvaluateResponse, BatchEvaluateRequest,
    BatchEvaluateResponse, HealthCheck, Feedback
)
from backend.routes import (
    evaluate_resume, batch_evaluate_resumes, upload_resume_file, get_all_courses_handler,
    list_uploaded_files_handler, delete_uploaded_file_handler
)
from utils.logger import logger

# Create FastAPI app
app = FastAPI(
    title="HireLens API",
    description="Automated Resume Relevance Check System with AI-powered evaluation",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to HireLens API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthCheck, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return HealthCheck(status="healthy")


@app.post("/upload-resume", tags=["Resume"])
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload and parse resume file
    
    Args:
        file: PDF or DOCX resume file
        
    Returns:
        Parsed resume data
    """
    return await upload_resume_file(file)


@app.post("/evaluate", response_model=EvaluateResponse, tags=["Evaluation"])
async def evaluate(request: EvaluateRequest):
    """
    Evaluate resume against job description
    
    Full pipeline: parse → analyze → evaluate → gap analysis → recommendations → feedback
    
    Args:
        request: Evaluation request with resume and job description
        
    Returns:
        Comprehensive evaluation results
    """
    return await evaluate_resume(request)


@app.post("/batch-evaluate", response_model=BatchEvaluateResponse, tags=["Evaluation"])
async def batch_evaluate(request: BatchEvaluateRequest, background_tasks: BackgroundTasks):
    """
    Evaluate multiple resumes against one job description
    
    Args:
        request: Batch evaluation request
        background_tasks: FastAPI background tasks
        
    Returns:
        Batch evaluation results
    """
    return await batch_evaluate_resumes(request, background_tasks)


@app.get("/evaluation/{evaluation_id}", tags=["Results"])
async def get_evaluation(evaluation_id: str):
    """
    Retrieve evaluation results by ID
    
    Args:
        evaluation_id: Evaluation ID
        
    Returns:
        Evaluation results
    """
    from config.config import EVALUATIONS_PATH
    from utils.json_handler import get_by_id
    
    evaluation = get_by_id(evaluation_id, EVALUATIONS_PATH, id_field="evaluation_id")
    
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    
    return evaluation


@app.get("/recommendations/{evaluation_id}", tags=["Results"])
async def get_recommendations(evaluation_id: str):
    """
    Retrieve course recommendations by evaluation ID
    
    Args:
        evaluation_id: Evaluation ID
        
    Returns:
        Course recommendations
    """
    from config.config import RECOMMENDATIONS_PATH
    from utils.json_handler import get_all
    
    all_recs = get_all(RECOMMENDATIONS_PATH)
    
    # Find recommendations for this evaluation
    for rec in all_recs:
        if isinstance(rec, dict) and rec.get("evaluation_id") == evaluation_id:
            return rec
    
    raise HTTPException(status_code=404, detail="Recommendations not found")


@app.get("/feedback/{evaluation_id}", tags=["Results"])
async def get_feedback(evaluation_id: str):
    """
    Retrieve feedback by evaluation ID
    
    Args:
        evaluation_id: Evaluation ID
        
    Returns:
        Feedback
    """
    from config.config import FEEDBACK_PATH
    from utils.json_handler import get_all
    
    all_feedback = get_all(FEEDBACK_PATH)
    
    # Find feedback for this evaluation
    for fb in all_feedback:
        if isinstance(fb, dict) and fb.get("evaluation_id") == evaluation_id:
            return fb
    
    raise HTTPException(status_code=404, detail="Feedback not found")


@app.delete("/evaluation/{evaluation_id}", tags=["Management"])
async def delete_evaluation(evaluation_id: str):
    """
    Delete evaluation and associated data
    
    Args:
        evaluation_id: Evaluation ID
        
    Returns:
        Success message
    """
    from config.config import EVALUATIONS_PATH, SKILL_GAPS_PATH, RECOMMENDATIONS_PATH, FEEDBACK_PATH
    from utils.json_handler import delete_by_id
    
    # Delete from all related files
    deleted_eval = delete_by_id(evaluation_id, EVALUATIONS_PATH, "evaluation_id")
    deleted_gap = delete_by_id(evaluation_id, SKILL_GAPS_PATH, "evaluation_id")
    deleted_rec = delete_by_id(evaluation_id, RECOMMENDATIONS_PATH, "evaluation_id")
    deleted_fb = delete_by_id(evaluation_id, FEEDBACK_PATH, "evaluation_id")
    
    if not deleted_eval:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    
    return {"message": "Evaluation deleted successfully", "evaluation_id": evaluation_id}


@app.get("/courses", tags=["Courses"])
async def get_courses():
    """
    Get all available courses
    """
    return await get_all_courses_handler()


@app.get("/uploads", tags=["Uploads"])
async def list_files():
    """List uploaded files"""
    return await list_uploaded_files_handler()


@app.delete("/uploads/{filename}", tags=["Uploads"])
async def delete_file(filename: str):
    """Delete uploaded file"""
    return await delete_uploaded_file_handler(filename)


# Run with: uvicorn backend.main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT)
