"""Test script for the Resume Evaluation System."""

import os
import sys
import json
import requests
import time
from pathlib import Path

# Add app directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.database import create_tables
from app.services.resume_service import ResumeService
from app.config import settings

# API Configuration
API_BASE_URL = "http://localhost:8000"

def test_api_connection():
    """Test if API is running."""
    try:
        response = requests.get(f"{API_BASE_URL}/")
        if response.status_code == 200:
            print("✅ API is running")
            return True
        else:
            print(f"❌ API returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API connection failed: {e}")
        return False

def create_sample_resume_files():
    """Create sample resume files for testing."""
    sample_resumes = [
        {
            "filename": "john_doe_resume.txt",
            "content": """John Doe
Email: john.doe@email.com
Phone: +91-9876543210
Location: Hyderabad, India

EDUCATION:
Bachelor of Technology in Computer Science
Indian Institute of Technology, Hyderabad
Graduated: 2022

SKILLS:
- Python programming
- Django framework
- PostgreSQL
- REST API development
- Git
- Docker
- HTML/CSS
- JavaScript

EXPERIENCE:
Software Developer Intern
TechStart Solutions, Hyderabad
June 2021 - August 2021
- Developed web applications using Django
- Created REST APIs for mobile app integration
- Worked with PostgreSQL database
- Participated in agile development process

PROJECTS:
1. E-commerce Website
   - Built using Django and PostgreSQL
   - Implemented user authentication and payment processing
   - Deployed on AWS EC2

2. Task Management API
   - RESTful API using Django REST framework
   - JWT authentication
   - Docker containerization

CERTIFICATIONS:
- AWS Cloud Practitioner
- Python Programming Certificate"""
        },
        {
            "filename": "jane_smith_resume.txt",
            "content": """Jane Smith
Email: jane.smith@email.com
Phone: +91-9876543211
Location: Bangalore, India

EDUCATION:
Master of Science in Data Science
Indian Institute of Science, Bangalore
Graduated: 2023

SKILLS:
- Python programming
- Machine learning
- Pandas and NumPy
- Scikit-learn
- SQL
- Jupyter notebooks
- Data visualization
- Statistics

EXPERIENCE:
Data Science Intern
DataCorp, Bangalore
January 2023 - June 2023
- Analyzed customer behavior data
- Built predictive models for sales forecasting
- Created interactive dashboards
- Collaborated with business teams

PROJECTS:
1. Customer Churn Prediction
   - Used machine learning algorithms
   - Achieved 85% accuracy
   - Implemented in production

2. Sales Forecasting Dashboard
   - Time series analysis
   - Interactive visualizations
   - Real-time data updates

CERTIFICATIONS:
- Google Data Analytics Certificate
- Machine Learning Specialization"""
        }
    ]
    
    # Create sample files
    for resume in sample_resumes:
        file_path = os.path.join("data", resume["filename"])
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(resume["content"])
        print(f"✅ Created sample resume: {resume['filename']}")

def test_resume_parsing():
    """Test resume parsing functionality."""
    print("\n🔍 Testing Resume Parsing...")
    
    try:
        from app.parsers.resume_parser import ResumeParser
        
        parser = ResumeParser()
        
        # Test with sample resume
        sample_file = "data/john_doe_resume.txt"
        if os.path.exists(sample_file):
            result = parser.parse_resume(sample_file, "John Doe", "john.doe@email.com")
            
            print(f"✅ Parsed resume: {result['filename']}")
            print(f"   Skills found: {len(result['skills'])}")
            print(f"   Education entries: {len(result['education'])}")
            print(f"   Experience entries: {len(result['experience'])}")
            
            return True
        else:
            print("❌ Sample resume file not found")
            return False
            
    except Exception as e:
        print(f"❌ Resume parsing test failed: {e}")
        return False

def test_job_description_parsing():
    """Test job description parsing functionality."""
    print("\n🔍 Testing Job Description Parsing...")
    
    try:
        from app.parsers.job_description_parser import JobDescriptionParser
        
        parser = JobDescriptionParser()
        
        # Test with sample job description
        sample_jd = """Software Engineer at TechCorp

We are looking for a Software Engineer to join our team in Hyderabad. The ideal candidate should have:

Required Skills:
- Python programming
- Django framework
- PostgreSQL database
- REST API development
- Git version control
- Docker containerization

Good to have:
- React.js frontend development
- AWS cloud services
- Machine learning basics
- Agile methodology experience

Qualifications:
- Bachelor's degree in Computer Science or related field
- 2-3 years of experience in software development

Responsibilities:
- Develop and maintain web applications
- Design and implement REST APIs
- Collaborate with cross-functional teams
- Write clean, maintainable code
- Participate in code reviews"""
        
        result = parser.parse_job_description(sample_jd)
        
        print(f"✅ Parsed job description: {result['title']}")
        print(f"   Company: {result['company']}")
        print(f"   Location: {result['location']}")
        print(f"   Must-have skills: {len(result['must_have_skills'])}")
        print(f"   Good-to-have skills: {len(result['good_to_have_skills'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Job description parsing test failed: {e}")
        return False

def test_evaluation_system():
    """Test the evaluation system."""
    print("\n🔍 Testing Evaluation System...")
    
    try:
        from app.evaluators.resume_evaluator import ResumeEvaluator
        from app.parsers.resume_parser import ResumeParser
        from app.parsers.job_description_parser import JobDescriptionParser
        
        # Initialize components
        evaluator = ResumeEvaluator()
        resume_parser = ResumeParser()
        jd_parser = JobDescriptionParser()
        
        # Parse sample resume
        sample_resume_file = "data/john_doe_resume.txt"
        if not os.path.exists(sample_resume_file):
            print("❌ Sample resume file not found")
            return False
        
        resume_data = resume_parser.parse_resume(sample_resume_file, "John Doe", "john.doe@email.com")
        
        # Parse sample job description
        sample_jd = """Software Engineer at TechCorp

We are looking for a Software Engineer to join our team in Hyderabad. The ideal candidate should have:

Required Skills:
- Python programming
- Django framework
- PostgreSQL database
- REST API development
- Git version control
- Docker containerization

Good to have:
- React.js frontend development
- AWS cloud services
- Machine learning basics
- Agile methodology experience

Qualifications:
- Bachelor's degree in Computer Science or related field
- 2-3 years of experience in software development

Responsibilities:
- Develop and maintain web applications
- Design and implement REST APIs
- Collaborate with cross-functional teams
- Write clean, maintainable code
- Participate in code reviews"""
        
        job_data = jd_parser.parse_job_description(sample_jd)
        
        # Evaluate resume
        evaluation_result = evaluator.evaluate_resume(resume_data, job_data)
        
        print(f"✅ Evaluation completed")
        print(f"   Relevance Score: {evaluation_result['relevance_score']}")
        print(f"   Hard Match Score: {evaluation_result['hard_match_score']}")
        print(f"   Semantic Match Score: {evaluation_result['semantic_match_score']}")
        print(f"   Verdict: {evaluation_result['verdict']}")
        print(f"   Missing Skills: {len(evaluation_result['missing_skills'])}")
        print(f"   Evaluation Time: {evaluation_result['evaluation_time']}s")
        
        return True
        
    except Exception as e:
        print(f"❌ Evaluation system test failed: {e}")
        return False

def test_database():
    """Test database functionality."""
    print("\n🔍 Testing Database...")
    
    try:
        # Create tables
        create_tables()
        print("✅ Database tables created")
        
        # Test service
        from app.services.resume_service import ResumeService
        from app.database import SessionLocal
        
        service = ResumeService()
        db = SessionLocal()
        
        # Test job description creation
        sample_jd = """Software Engineer at TechCorp

We are looking for a Software Engineer to join our team in Hyderabad. The ideal candidate should have:

Required Skills:
- Python programming
- Django framework
- PostgreSQL database
- REST API development
- Git version control
- Docker containerization

Good to have:
- React.js frontend development
- AWS cloud services
- Machine learning basics
- Agile methodology experience

Qualifications:
- Bachelor's degree in Computer Science or related field
- 2-3 years of experience in software development

Responsibilities:
- Develop and maintain web applications
- Design and implement REST APIs
- Collaborate with cross-functional teams
- Write clean, maintainable code
- Participate in code reviews"""
        
        job_description = service.save_job_description(db, sample_jd, "Software Engineer", "TechCorp", "Hyderabad")
        print(f"✅ Job description saved with ID: {job_description.id}")
        
        # Test resume creation
        sample_resume_file = "data/john_doe_resume.txt"
        if os.path.exists(sample_resume_file):
            resume = service.save_resume(db, sample_resume_file, "John Doe", "john.doe@email.com")
            print(f"✅ Resume saved with ID: {resume.id}")
            
            # Test evaluation
            evaluation = service.evaluate_resume_against_job(db, resume.id, job_description.id)
            print(f"✅ Evaluation completed with ID: {evaluation.id}")
            print(f"   Relevance Score: {evaluation.relevance_score}")
            print(f"   Verdict: {evaluation.verdict}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting Resume Evaluation System Tests")
    print("=" * 50)
    
    # Create necessary directories
    os.makedirs("data", exist_ok=True)
    os.makedirs("data/uploads", exist_ok=True)
    
    # Create sample files
    create_sample_resume_files()
    
    # Run tests
    tests = [
        ("Resume Parsing", test_resume_parsing),
        ("Job Description Parsing", test_job_description_parsing),
        ("Evaluation System", test_evaluation_system),
        ("Database", test_database),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    print(f"\n{'='*50}")
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is ready to use.")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
    
    print("\n📝 Next Steps:")
    print("1. Start the API server: uvicorn app.main:app --reload")
    print("2. Start the dashboard: streamlit run app/frontend/dashboard.py")
    print("3. Open http://localhost:8501 in your browser")

if __name__ == "__main__":
    main()
