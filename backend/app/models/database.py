"""Database models for the Resume Evaluation System."""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Optional
from backend.app.config import settings

Base = declarative_base()


class JobDescription(Base):
    """Job description model."""
    
    __tablename__ = "job_descriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    must_have_skills = Column(Text)  # JSON string
    good_to_have_skills = Column(Text)  # JSON string
    qualifications = Column(Text)  # JSON string
    experience_required = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    evaluations = relationship("ResumeEvaluation", back_populates="job_description")


class Resume(Base):
    """Resume model."""
    
    __tablename__ = "resumes"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    student_name = Column(String(255), nullable=False)
    student_email = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    skills = Column(Text)  # JSON string
    education = Column(Text)  # JSON string
    experience = Column(Text)  # JSON string
    projects = Column(Text)  # JSON string
    certifications = Column(Text)  # JSON string
    file_path = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    evaluations = relationship("ResumeEvaluation", back_populates="resume")


class ResumeEvaluation(Base):
    """Resume evaluation results model."""
    
    __tablename__ = "resume_evaluations"
    
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    job_description_id = Column(Integer, ForeignKey("job_descriptions.id"), nullable=False)
    
    # Scores
    relevance_score = Column(Float, nullable=False)  # 0-100
    hard_match_score = Column(Float, nullable=False)  # 0-100
    semantic_match_score = Column(Float, nullable=False)  # 0-100
    
    # Verdict
    verdict = Column(String(20), nullable=False)  # High/Medium/Low
    
    # Analysis
    matched_skills = Column(Text)
    missing_skills = Column(Text)  # JSON string
    missing_certifications = Column(Text)  # JSON string
    missing_projects = Column(Text)  # JSON string
    missing_qualifications = Column(Text) # JSON string
    strengths = Column(Text)  # JSON string
    weaknesses = Column(Text)  # JSON string
    
    # Feedback
    improvement_suggestions = Column(Text)
    overall_feedback = Column(Text)
    
    # Metadata
    evaluation_time = Column(Float)  # Time taken in seconds
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    resume = relationship("Resume", back_populates="evaluations")
    job_description = relationship("JobDescription", back_populates="evaluations")

if __name__ == "__main__":
    from sqlalchemy import create_engine
    from app.config.settings import settings  # pyright: ignore[reportMissingImports]

    engine = create_engine(settings.database_url)
    Base.metadata.create_all(bind=engine)
    print("✅ Database created with all tables!")

