"""
HireLens API Routes
Route handlers for all API endpoints
"""

from fastapi import UploadFile, HTTPException, BackgroundTasks
from pathlib import Path
import shutil
from typing import List

from config.config import (
    UPLOAD_DIR, PARSED_RESUMES_PATH, JOB_DESCRIPTIONS_PATH,
    EVALUATIONS_PATH, SKILL_GAPS_PATH, RECOMMENDATIONS_PATH, FEEDBACK_PATH
)
from config.models import (
    EvaluateRequest, EvaluateResponse, BatchEvaluateRequest, BatchEvaluateResponse,
    ResumeData, JobDescription, Course
)
from modules.resume_parser import parse_resume, save_resume_to_json
from modules.job_analyzer import analyze_job_description, save_job_to_json
from modules.evaluation_engine import evaluate, save_evaluation
from modules.skill_gap_analyzer import analyze_skill_gaps, save_skill_gaps
from modules.course_recommender import recommend_courses, save_recommendations, load_courses_dataset
from modules.feedback_generator import generate_feedback, save_feedback
from config.models import CourseRecommendation
from utils.logger import logger


async def upload_resume_file(file: UploadFile) -> dict:
    """
    Handle resume file upload and parsing
    
    Args:
        file: Uploaded resume file
        
    Returns:
        Parsed resume data
    """
    logger.info(f"Uploading resume: {file.filename}")
    
    # Validate file type
    if not file.filename.endswith(('.pdf', '.docx', '.doc')):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only PDF and DOCX files are supported."
        )
    
    # Save file
    file_path = UPLOAD_DIR / file.filename
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"File saved to {file_path}")
        
        # Parse resume
        resume_data = parse_resume(file_path)
        
        # Save to JSON
        save_resume_to_json(resume_data, PARSED_RESUMES_PATH)
        
        return {
            "resume_id": resume_data.resume_id,
            "filename": file.filename,
            "name": resume_data.name,
            "email": resume_data.email,
            "skills_found": len(resume_data.skills),
            "message": "Resume uploaded and parsed successfully"
        }
    
    except Exception as e:
        logger.error(f"Error uploading resume: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")


async def evaluate_resume(request: EvaluateRequest) -> EvaluateResponse:
    """
    Full evaluation pipeline
    
    Args:
        request: Evaluation request
        
    Returns:
        Complete evaluation response
    """
    logger.info("Starting evaluation pipeline")
    
    try:
        # Step 1: Parse resume
        if request.resume_file_path:
            logger.info("Parsing resume from file")
            resume_data = parse_resume(request.resume_file_path)
            save_resume_to_json(resume_data, PARSED_RESUMES_PATH)
        elif request.resume_text:
            # Create temporary file from text
            logger.info("Creating resume from text")
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp:
                tmp.write(request.resume_text)
                tmp_path = tmp.name
            
            resume_data = ResumeData(
                raw_text=request.resume_text,
                skills=[],  # Would need to parse from text
                education=[],
                experience=[],
                projects=[],
                certifications=[]
            )
            save_resume_to_json(resume_data, PARSED_RESUMES_PATH)
        else:
            raise HTTPException(status_code=400, detail="Either resume_file_path or resume_text must be provided")
        
        # Step 2: Analyze job description
        logger.info("Analyzing job description")
        job_data = analyze_job_description(request.job_description)
        save_job_to_json(job_data, JOB_DESCRIPTIONS_PATH)
        
        # Step 3: Evaluate
        logger.info("Performing hybrid evaluation")
        evaluation = evaluate(resume_data, job_data)
        save_evaluation(evaluation, EVALUATIONS_PATH)
        
        # Step 4: Analyze skill gaps
        logger.info("Analyzing skill gaps")
        skill_gap = analyze_skill_gaps(resume_data, job_data, evaluation)
        save_skill_gaps(skill_gap, SKILL_GAPS_PATH)
        
        # Step 5: Get course recommendations
        logger.info("Generating course recommendations")
        courses_db = load_courses_dataset()
        recommendations = recommend_courses(skill_gap, courses_db)
        
        course_rec = CourseRecommendation(
            gap_id=skill_gap.gap_id,
            evaluation_id=evaluation.evaluation_id,
            courses=recommendations
        )
        save_recommendations(course_rec, RECOMMENDATIONS_PATH)
        
        # Step 6: Generate feedback
        logger.info("Generating feedback")
        feedback = generate_feedback(evaluation, skill_gap, recommendations, resume_data.skills)
        save_feedback(feedback, FEEDBACK_PATH)
        
        # Prepare response
        response = EvaluateResponse(
            evaluation_id=evaluation.evaluation_id,
            filename=Path(request.resume_file_path).name if request.resume_file_path else "Uploaded Text",
            candidate_name=resume_data.name,
            score=evaluation.hybrid_score,
            classification=evaluation.classification,
            matched_skills=evaluation.matched_skills,
            skill_gaps=skill_gap.missing_must_have + skill_gap.missing_good_to_have,
            recommendations=recommendations,
            feedback=feedback
        )
        
        logger.info(f"Evaluation complete: {evaluation.evaluation_id}")
        
        return response
    
    except Exception as e:
        logger.error(f"Error in evaluation pipeline: {e}")
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")


async def batch_evaluate_resumes(
    request: BatchEvaluateRequest,
    background_tasks: BackgroundTasks
) -> BatchEvaluateResponse:
    """
    Batch evaluation of multiple resumes
    
    Args:
        request: Batch evaluation request
        background_tasks: Background tasks handler
        
    Returns:
        Batch evaluation results
    """
    logger.info(f"Starting batch evaluation of {len(request.resume_file_paths)} resumes")
    
    try:
        results = []
        total_score = 0.0
        
        # Analyze job description once
        job_data = analyze_job_description(request.job_description)
        save_job_to_json(job_data, JOB_DESCRIPTIONS_PATH)
        
        # Load courses dataset once
        courses_db = load_courses_dataset()
        
        # Evaluate each resume
        for resume_path in request.resume_file_paths:
            try:
                logger.info(f"Evaluating resume: {resume_path}")
                
                # Parse resume
                full_path = UPLOAD_DIR / Path(resume_path).name
                logger.info(f"Parsing resume from {full_path}")
                resume_data = parse_resume(full_path)
                save_resume_to_json(resume_data, PARSED_RESUMES_PATH)
                
                # Evaluate
                evaluation = evaluate(resume_data, job_data)
                save_evaluation(evaluation, EVALUATIONS_PATH)
                
                # Skill gaps
                skill_gap = analyze_skill_gaps(resume_data, job_data, evaluation)
                save_skill_gaps(skill_gap, SKILL_GAPS_PATH)
                
                # Recommendations
                recommendations = recommend_courses(skill_gap, courses_db)
                course_rec = CourseRecommendation(
                    gap_id=skill_gap.gap_id,
                    evaluation_id=evaluation.evaluation_id,
                    courses=recommendations
                )
                save_recommendations(course_rec, RECOMMENDATIONS_PATH)
                
                # Feedback
                feedback = generate_feedback(evaluation, skill_gap, recommendations, resume_data.skills)
                save_feedback(feedback, FEEDBACK_PATH)
                
                # Add to results
                result = EvaluateResponse(
                    evaluation_id=evaluation.evaluation_id,
                    filename=resume_path,
                    candidate_name=resume_data.name,
                    score=evaluation.hybrid_score,
                    classification=evaluation.classification,
                    matched_skills=evaluation.matched_skills,
                    skill_gaps=skill_gap.missing_must_have + skill_gap.missing_good_to_have,
                    recommendations=recommendations,
                    feedback=feedback
                )
                results.append(result)
                total_score += evaluation.hybrid_score
                
            except Exception as e:
                logger.error(f"Error evaluating resume {resume_path}: {e}")
                continue
        
        avg_score = total_score / len(results) if results else 0.0
        
        logger.info(f"Batch evaluation complete. Evaluated {len(results)} resumes, avg score: {avg_score:.2f}")
        
        return BatchEvaluateResponse(
            results=results,
            total_evaluated=len(results),
            average_score=avg_score
        )
    
    except Exception as e:
        logger.error(f"Error in batch evaluation: {e}")
        raise HTTPException(status_code=500, detail=f"Batch evaluation failed: {str(e)}")


async def get_all_courses_handler():
    """
    Get all available courses from dataset
    """
    try:
        courses_db = load_courses_dataset()
        # Flatten structure or return as is? Returning as is (by category/skill) is better for display
        return courses_db
    except Exception as e:
        logger.error(f"Error fetching courses: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch courses: {str(e)}")


async def list_uploaded_files_handler():
    """
    List all uploaded files
    """
    try:
        files = []
        if UPLOAD_DIR.exists():
            for file_path in UPLOAD_DIR.glob('*'):
                if file_path.is_file() and file_path.suffix.lower() in ['.pdf', '.docx', '.doc']:
                    stats = file_path.stat()
                    files.append({
                        "filename": file_path.name,
                        "size": stats.st_size,
                        "modified": stats.st_mtime
                    })
        return sorted(files, key=lambda x: x['modified'], reverse=True)
    except Exception as e:
        logger.error(f"Error listing files: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list files: {str(e)}")


async def delete_uploaded_file_handler(filename: str):
    """
    Delete an uploaded file
    """
    try:
        if not filename:
            raise HTTPException(status_code=400, detail="Filename required")
            
        file_path = UPLOAD_DIR / filename
        
        # Security check: ensure path is within UPLOAD_DIR
        if not file_path.resolve().is_relative_to(UPLOAD_DIR.resolve()):
             raise HTTPException(status_code=403, detail="Invalid file path")

        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
            
        file_path.unlink()
        logger.info(f"Deleted file: {filename}")
        return {"message": f"File {filename} deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting file {filename}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")
