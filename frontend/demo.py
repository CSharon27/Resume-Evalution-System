"""Demo script for the Resume Evaluation System."""

import os
import sys
import json
from pathlib import Path

# Add app directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def create_demo_data():
    """Create demo data for the system."""
    print("🎬 Creating demo data...")
    
    # Create sample resume file
    sample_resume = """John Doe
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
    
    # Save sample resume
    os.makedirs("data", exist_ok=True)
    with open("data/demo_resume.txt", "w", encoding="utf-8") as f:
        f.write(sample_resume)
    
    # Create sample job description
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
    
    with open("data/demo_job_description.txt", "w", encoding="utf-8") as f:
        f.write(sample_jd)
    
    print("✅ Demo data created")

def run_demo():
    """Run the demo evaluation."""
    print("🚀 Running Resume Evaluation Demo")
    print("=" * 50)
    
    try:
        # Import required modules
        from app.parsers.resume_parser import ResumeParser
        from app.parsers.job_description_parser import JobDescriptionParser
        from app.evaluators.resume_evaluator import ResumeEvaluator
        
        # Initialize components
        resume_parser = ResumeParser()
        jd_parser = JobDescriptionParser()
        evaluator = ResumeEvaluator()
        
        print("📄 Parsing Resume...")
        resume_data = resume_parser.parse_resume("data/demo_resume.txt", "John Doe", "john.doe@email.com")
        print(f"   ✅ Parsed resume: {resume_data['filename']}")
        print(f"   📊 Skills found: {len(resume_data['skills'])}")
        print(f"   🎓 Education entries: {len(resume_data['education'])}")
        print(f"   💼 Experience entries: {len(resume_data['experience'])}")
        
        print("\n💼 Parsing Job Description...")
        job_data = jd_parser.parse_job_description(open("data/demo_job_description.txt", "r").read())
        print(f"   ✅ Parsed job: {job_data['title']} at {job_data['company']}")
        print(f"   📍 Location: {job_data['location']}")
        print(f"   🔧 Must-have skills: {len(job_data['must_have_skills'])}")
        print(f"   ⭐ Good-to-have skills: {len(job_data['good_to_have_skills'])}")
        
        print("\n🔍 Evaluating Resume...")
        evaluation_result = evaluator.evaluate_resume(resume_data, job_data)
        
        print("\n📊 EVALUATION RESULTS")
        print("=" * 50)
        print(f"🎯 Relevance Score: {evaluation_result['relevance_score']:.1f}/100")
        print(f"🔧 Hard Match Score: {evaluation_result['hard_match_score']:.1f}/100")
        print(f"🧠 Semantic Match Score: {evaluation_result['semantic_match_score']:.1f}/100")
        print(f"📋 Verdict: {evaluation_result['verdict']}")
        print(f"⏱️  Evaluation Time: {evaluation_result['evaluation_time']:.2f}s")
        
        print("\n❌ Missing Skills:")
        for skill in evaluation_result['missing_skills']:
            print(f"   • {skill}")
        
        print("\n✅ Strengths:")
        for strength in evaluation_result['strengths']:
            print(f"   • {strength}")
        
        print("\n⚠️  Weaknesses:")
        for weakness in evaluation_result['weaknesses']:
            print(f"   • {weakness}")
        
        print("\n💡 Improvement Suggestions:")
        print(f"   {evaluation_result['improvement_suggestions']}")
        
        print("\n📝 Overall Feedback:")
        print(f"   {evaluation_result['overall_feedback']}")
        
        print("\n🎉 Demo completed successfully!")
        print("\n📝 Next Steps:")
        print("1. Run 'python run_system.py' to start the full system")
        print("2. Open http://localhost:8501 in your browser")
        print("3. Upload resumes and job descriptions (PDF/DOCX/TXT files supported!)")
        print("4. Evaluate resumes against job descriptions")
        print("\n✨ New Features:")
        print("• File upload for job descriptions (PDF/DOCX/TXT)")
        print("• Enhanced UI with interactive elements")
        print("• Real-time progress tracking")
        print("• Advanced filtering and search")
        print("• Export functionality")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure all dependencies are installed: pip install -r requirements.txt")
        print("2. Download spaCy model: python -m spacy download en_core_web_sm")
        print("3. Check if OpenAI API key is set in .env file")

def main():
    """Main demo function."""
    print("🎬 Resume Evaluation System Demo")
    print("=" * 50)
    
    # Create demo data
    create_demo_data()
    
    # Run demo
    run_demo()

if __name__ == "__main__":
    main()
