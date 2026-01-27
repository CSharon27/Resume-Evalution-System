"""
HireLens Data Models
Pydantic models for data validation and serialization
"""

from typing import List, Dict, Optional
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
import uuid


# Resume Models
class Education(BaseModel):
    degree: str
    institution: str
    year: Optional[str] = None
    gpa: Optional[str] = None


class Experience(BaseModel):
    title: str
    company: str
    duration: str
    description: Optional[str] = None
    location: Optional[str] = None


class ResumeData(BaseModel):
    resume_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: List[str] = []
    education: List[Education] = []
    experience: List[Experience] = []
    projects: List[str] = []
    certifications: List[str] = []
    raw_text: str
    created_at: datetime = Field(default_factory=datetime.now)


# Job Description Models
class JobDescription(BaseModel):
    job_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: Optional[str] = None
    company: Optional[str] = None
    must_have_skills: List[str] = []
    good_to_have_skills: List[str] = []
    experience_required: Optional[str] = None
    role_description: str
    location: Optional[str] = None
    salary_range: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)


# Evaluation Models
class EvaluationResult(BaseModel):
    evaluation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    resume_id: str
    job_id: str
    tfidf_score: float = Field(ge=0, le=1)
    fuzzy_score: float = Field(ge=0, le=1)
    embedding_score: float = Field(ge=0, le=1)
    hybrid_score: float = Field(ge=0, le=100)
    classification: str  # High, Medium, Low
    matched_skills: List[str] = []
    missing_skills: List[str] = []
    timestamp: datetime = Field(default_factory=datetime.now)


# Skill Gap Models
class SkillGap(BaseModel):
    gap_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    evaluation_id: str
    missing_must_have: List[str] = []
    missing_good_to_have: List[str] = []
    weak_skills: List[str] = []
    categorized_gaps: Dict[str, List[str]] = {}
    created_at: datetime = Field(default_factory=datetime.now)


# Course Recommendation Models
class Course(BaseModel):
    title: str
    provider: str
    url: str
    rating: float = Field(ge=0, le=5)
    duration: Optional[str] = None
    level: Optional[str] = None  # Beginner, Intermediate, Advanced


class CourseRecommendation(BaseModel):
    recommendation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    gap_id: str
    evaluation_id: str
    courses: Dict[str, List[Course]] = {}  # skill -> list of courses
    created_at: datetime = Field(default_factory=datetime.now)


# Feedback Models
class LearningRoadmap(BaseModel):
    immediate: List[str] = []  # 1-2 weeks
    short_term: List[str] = []  # 1-3 months
    long_term: List[str] = []  # 3-6 months


class Feedback(BaseModel):
    feedback_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    evaluation_id: str
    strengths: List[str] = []
    weaknesses: List[str] = []
    suggestions: List[str] = []
    learning_roadmap: LearningRoadmap
    overall_assessment: str
    created_at: datetime = Field(default_factory=datetime.now)


# API Request/Response Models
class EvaluateRequest(BaseModel):
    resume_text: Optional[str] = None
    resume_file_path: Optional[str] = None
    job_description: str


class EvaluateResponse(BaseModel):
    evaluation_id: str
    filename: Optional[str] = None
    candidate_name: Optional[str] = None
    score: float
    classification: str
    matched_skills: List[str]
    skill_gaps: List[str]
    recommendations: Dict[str, List[Course]]
    feedback: Feedback


class BatchEvaluateRequest(BaseModel):
    resume_file_paths: List[str]
    job_description: str


class BatchEvaluateResponse(BaseModel):
    results: List[EvaluateResponse]
    total_evaluated: int
    average_score: float


# Health Check
class HealthCheck(BaseModel):
    status: str
    timestamp: datetime = Field(default_factory=datetime.now)
    version: str = "1.0.0"
