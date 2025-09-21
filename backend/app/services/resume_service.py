"""Service for managing resume operations."""

import os
import json
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from backend.app.models.database import Resume, JobDescription, ResumeEvaluation
from backend.app.parsers.resume_parser import ResumeParser
from backend.app.parsers.job_description_parser import JobDescriptionParser
from backend.app.evaluators.resume_evaluator import ResumeEvaluator


class ResumeService:
    """Service for resume-related operations."""
    
    def __init__(self):
        """Initialize the service."""
        self.resume_parser = ResumeParser()
        self.jd_parser = JobDescriptionParser()
        self.evaluator = ResumeEvaluator()
    
    def save_resume(self, db: Session, file_path: str, student_name: str, student_email: str) -> Resume:
        """Save resume to database."""
        try:
            # Parse resume
            parsed_data = self.resume_parser.parse_resume(file_path, student_name, student_email)
            
            # Create resume record
            resume = Resume(
                filename=parsed_data['filename'],
                student_name=parsed_data['student_name'],
                student_email=parsed_data['student_email'],
                content=parsed_data['content'],
                skills=json.dumps(parsed_data['skills']),
                education=json.dumps(parsed_data['education']),
                experience=json.dumps(parsed_data['experience']),
                projects=json.dumps(parsed_data['sections'].get('projects', [])),
                certifications=json.dumps(parsed_data['sections'].get('certifications', [])),
                file_path=file_path
            )
            
            db.add(resume)
            db.commit()
            db.refresh(resume)
            
            return resume
            
        except Exception as e:
            db.rollback()
            raise ValueError(f"Error saving resume: {str(e)}")
    
    def save_job_description(self, db: Session, content: str, title: str = "", company: str = "", location: str = "") -> JobDescription:
        """Save job description to database."""
        try:
            # Parse job description
            parsed_data = self.jd_parser.parse_job_description(content)
            
            # Use provided values or parsed values
            final_title = title or parsed_data['title']
            final_company = company or parsed_data['company']
            final_location = location or parsed_data['location']
            
            # Create job description record
            job_description = JobDescription(
                title=final_title,
                company=final_company,
                location=final_location,
                content=parsed_data['content'],
                must_have_skills=json.dumps(parsed_data['must_have_skills']),
                good_to_have_skills=json.dumps(parsed_data['good_to_have_skills']),
                qualifications=json.dumps(parsed_data['qualifications']),
                experience_required=parsed_data['experience_required']
            )
            
            db.add(job_description)
            db.commit()
            db.refresh(job_description)
            
            return job_description
            
        except Exception as e:
            db.rollback()
            raise ValueError(f"Error saving job description: {str(e)}")
    
    def evaluate_resume_against_job(self, db: Session, resume_id: int, job_description_id: int) -> ResumeEvaluation:
        """Evaluate a resume against a job description."""
        try:
            # Fetch resume and job description from DB
            resume = db.query(Resume).filter(Resume.id == resume_id).first()
            job_description = db.query(JobDescription).filter(JobDescription.id == job_description_id).first()
            
            if not resume or not job_description:
                raise ValueError("Resume or job description not found")

            # Prepare data for evaluation
            resume_data = {
                'content': resume.content,
                'skills': json.loads(resume.skills or '[]'),
                'education': json.loads(resume.education or '[]'),
                'experience': json.loads(resume.experience or '[]'),
                'projects': json.loads(resume.projects or '[]'),
                'certifications': json.loads(resume.certifications or '[]')
            }

            job_data = {
                'content': job_description.content,
                'must_have_skills': json.loads(job_description.must_have_skills or '[]'),
                'good_to_have_skills': json.loads(job_description.good_to_have_skills or '[]'),
                'qualifications': json.loads(job_description.qualifications or '[]'),
                'experience_required': job_description.experience_required,
                'responsibilities': []
            }

            # Evaluate resume
            evaluation_results = self.evaluator.evaluate_resume(resume_data, job_data)

            # Save evaluation to DB
            evaluation = ResumeEvaluation(
                resume_id=resume_id,
                job_description_id=job_description_id,
                relevance_score=evaluation_results.get('relevance_score', 0),
                hard_match_score=evaluation_results.get('hard_match_score', 0),
                semantic_match_score=evaluation_results.get('semantic_match_score', 0),
                verdict=evaluation_results.get('verdict', ''),
                matched_skills=json.dumps(evaluation_results.get('matched_skills', [])), 
                missing_skills=json.dumps(evaluation_results.get('missing_skills', [])),
                missing_certifications=json.dumps(evaluation_results.get('missing_certifications', [])),
                missing_projects=json.dumps(evaluation_results.get('missing_projects', [])),
                strengths=json.dumps(evaluation_results.get('strengths', [])),
                weaknesses=json.dumps(evaluation_results.get('weaknesses', [])),
                improvement_suggestions=json.dumps(evaluation_results.get('improvement_suggestions', [])),
                missing_qualifications=json.dumps(evaluation_results.get('missing_qualifications', [])),
                overall_feedback=evaluation_results.get('overall_feedback', ''),
                evaluation_time=evaluation_results.get('evaluation_time', 0)
            )

            db.add(evaluation)
            db.commit()
            db.refresh(evaluation)

            return evaluation

        except Exception as e:
            db.rollback()
            raise ValueError(f"Error evaluating resume: {str(e)}")

    
    def get_resume_evaluations(self, db: Session, job_description_id: Optional[int] = None) -> List[ResumeEvaluation]:
        """Get resume evaluations, optionally filtered by job description."""
        query = db.query(ResumeEvaluation)
        
        if job_description_id:
            query = query.filter(ResumeEvaluation.job_description_id == job_description_id)
        
        return query.order_by(ResumeEvaluation.relevance_score.desc()).all()
    
    def get_resume_by_id(self, db: Session, resume_id: int) -> Optional[Resume]:
        """Get resume by ID."""
        return db.query(Resume).filter(Resume.id == resume_id).first()
    
    def get_job_description_by_id(self, db: Session, job_description_id: int) -> Optional[JobDescription]:
        """Get job description by ID."""
        return db.query(JobDescription).filter(JobDescription.id == job_description_id).first()
    
    def get_all_resumes(self, db: Session) -> List[Resume]:
        """Get all resumes."""
        return db.query(Resume).all()
    
    def get_all_job_descriptions(self, db: Session) -> List[JobDescription]:
        """Get all job descriptions."""
        return db.query(JobDescription).all()
    
    def delete_resume(self, db: Session, resume_id: int) -> bool:
        """Delete a resume and its evaluations."""
        try:
            resume = db.query(Resume).filter(Resume.id == resume_id).first()
            if not resume:
                return False
            
            # Delete associated evaluations
            db.query(ResumeEvaluation).filter(ResumeEvaluation.resume_id == resume_id).delete()
            
            # Delete resume
            db.delete(resume)
            db.commit()
            
            return True
            
        except Exception as e:
            db.rollback()
            return False
    
    def delete_job_description(self, db: Session, job_description_id: int) -> bool:
        """Delete a job description and its evaluations."""
        try:
            job_description = db.query(JobDescription).filter(JobDescription.id == job_description_id).first()
            if not job_description:
                return False
            
            # Delete associated evaluations
            db.query(ResumeEvaluation).filter(ResumeEvaluation.job_description_id == job_description_id).delete()
            
            # Delete job description
            db.delete(job_description)
            db.commit()
            
            return True
            
        except Exception as e:
            db.rollback()
            return False

