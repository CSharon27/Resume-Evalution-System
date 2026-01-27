"""
HireLens Resume Parser
Extracts structured information from PDF and DOCX resumes
"""

import re
from pathlib import Path
from typing import Dict, List, Optional
import PyPDF2
import docx
from config.config import TECHNICAL_SKILLS, EDUCATION_KEYWORDS, EXPERIENCE_KEYWORDS
from config.models import ResumeData, Education, Experience
from utils.nlp_utils import load_spacy_model, clean_skill_name
from utils.logger import logger


def extract_text_from_pdf(file_path: str | Path) -> str:
    """
    Extract text from PDF file
    
    Args:
        file_path: Path to PDF file
        
    Returns:
        Extracted text
    """
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + " \n"
            return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF {file_path}: {e}")
        return ""


def extract_text_from_docx(file_path: str | Path) -> str:
    """
    Extract text from DOCX file
    
    Args:
        file_path: Path to DOCX file
        
    Returns:
        Extracted text
    """
    try:
        doc = docx.Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        logger.error(f"Error extracting text from DOCX {file_path}: {e}")
        return ""


def extract_email(text: str) -> Optional[str]:
    """Extract email address from text"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.search(email_pattern, text)
    return match.group(0) if match else None


def extract_phone(text: str) -> Optional[str]:
    """Extract phone number from text"""
    # Matches various phone formats
    phone_patterns = [
        r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
        r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
        r'\d{10}'
    ]
    
    for pattern in phone_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    
    return None


def extract_name(text: str, nlp_model) -> Optional[str]:
    """
    Extract candidate name from resume text
    Uses first PERSON entity found or first line
    """
    doc = nlp_model(text[:500])  # First 500 chars likely contain name
    
    # Try to find PERSON entity
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    
    # Fallback: first non-empty line
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if line and len(line) < 50:  # Names are typically short
            return line
    
    return None


def extract_skills(text: str, nlp_model) -> List[str]:
    """
    Extract technical skills from resume text
    
    Args:
        text: Resume text
        nlp_model: spaCy model
        
    Returns:
        List of extracted skills
    """
    skills = set()
    text_lower = text.lower()
    
    # Method 1: Direct keyword matching
    for skill in TECHNICAL_SKILLS:
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text_lower):
            skills.add(clean_skill_name(skill))
    
    # Method 2: Look in skills section
    skills_section_pattern = r'(?:skills?|technical skills?|core competencies)[:\s]+(.*?)(?:\n\n|\n[A-Z]|$)'
    skills_match = re.search(skills_section_pattern, text, re.IGNORECASE | re.DOTALL)
    
    if skills_match:
        skills_text = skills_match.group(1)
        # Split by common delimiters
        skill_items = re.split(r'[,;|•\n]', skills_text)
        
        for item in skill_items:
            item = item.strip()
            # Check if this item matches any known skill
            for skill in TECHNICAL_SKILLS:
                if skill.lower() in item.lower():
                    skills.add(clean_skill_name(skill))
    
    return sorted(list(skills))


def extract_skills_fallback(text: str) -> List[str]:
    """
    Fallback skill extraction without NLP model
    """
    skills = set()
    text_lower = text.lower()
    
    for skill in TECHNICAL_SKILLS:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text_lower):
            skills.add(clean_skill_name(skill))
            
    return sorted(list(skills))


def extract_education(text: str, nlp_model) -> List[Education]:
    """
    Extract education information from resume
    
    Args:
        text: Resume text
        nlp_model: spaCy model
        
    Returns:
        List of Education objects
    """
    education_list = []
    
    # Find education section
    edu_pattern = r'(?:education|academic|qualification)[:\s]+(.*?)(?:\n\n|\n[A-Z][A-Z\s]+\n|$)'
    edu_match = re.search(edu_pattern, text, re.IGNORECASE | re.DOTALL)
    
    if not edu_match:
        return education_list
    
    edu_text = edu_match.group(1)
    
    # Extract degree, institution, and year
    lines = edu_text.split('\n')
    current_edu = {}
    
    for line in lines:
        line = line.strip()
        if not line:
            if current_edu:
                education_list.append(Education(**current_edu))
                current_edu = {}
            continue
        
        # Check for degree keywords
        for keyword in EDUCATION_KEYWORDS:
            if keyword.lower() in line.lower():
                current_edu['degree'] = line
                break
        
        # Extract year (4 digits)
        year_match = re.search(r'\b(19|20)\d{2}\b', line)
        if year_match and 'year' not in current_edu:
            current_edu['year'] = year_match.group(0)
        
        # If line contains "University", "College", "Institute"
        if any(word in line.lower() for word in ['university', 'college', 'institute']):
            if 'institution' not in current_edu:
                current_edu['institution'] = line
    
    if current_edu and 'degree' in current_edu:
        education_list.append(Education(**current_edu))
    
    return education_list


def extract_experience(text: str, nlp_model) -> List[Experience]:
    """
    Extract work experience from resume
    
    Args:
        text: Resume text
        nlp_model: spaCy model
        
    Returns:
        List of Experience objects
    """
    experience_list = []
    
    # Find experience section
    exp_pattern = r'(?:experience|employment|work history)[:\s]+(.*?)(?:\n\n[A-Z][A-Z\s]+\n|education|skills|projects|$)'
    exp_match = re.search(exp_pattern, text, re.IGNORECASE | re.DOTALL)
    
    if not exp_match:
        return experience_list
    
    exp_text = exp_match.group(1)
    
    # Split by likely job entries (lines with job titles or companies)
    entries = re.split(r'\n(?=[A-Z])', exp_text)
    
    for entry in entries:
        entry = entry.strip()
        if not entry or len(entry) < 20:
            continue
        
        exp_data = {}
        lines = entry.split('\n')
        
        # First line often contains title and/or company
        first_line = lines[0] if lines else ""
        
        # Check for job title
        for keyword in EXPERIENCE_KEYWORDS:
            if keyword.lower() in first_line.lower():
                exp_data['title'] = first_line
                break
        
        if 'title' not in exp_data:
            exp_data['title'] = first_line
        
        # Extract duration (e.g., "2020-2023", "Jan 2020 - Present")
        duration_pattern = r'(\d{4}\s*[-–]\s*(?:\d{4}|Present|Current))|(\w+\s+\d{4}\s*[-–]\s*(?:\w+\s+\d{4}|Present))'
        duration_match = re.search(duration_pattern, entry, re.IGNORECASE)
        if duration_match:
            exp_data['duration'] = duration_match.group(0)
        else:
            exp_data['duration'] = "Not specified"
        
        # Extract company (ORG entities)
        doc = nlp_model(entry[:200])
        for ent in doc.ents:
            if ent.label_ == "ORG":
                exp_data['company'] = ent.text
                break
        
        if 'company' not in exp_data:
            exp_data['company'] = "Company not specified"
        
        # Description is remaining text
        exp_data['description'] = entry[:300]  # First 300 chars
        
        if exp_data.get('title'):
            experience_list.append(Experience(**exp_data))
    
    return experience_list


def extract_projects(text: str) -> List[str]:
    """
    Extract project information from resume
    
    Args:
        text: Resume text
        
    Returns:
        List of project names/descriptions
    """
    projects = []
    
    # Find projects section
    proj_pattern = r'(?:projects?|personal projects?|academic projects?)[:\s]+(.*?)(?:\n\n[A-Z][A-Z\s]+\n|education|skills|experience|$)'
    proj_match = re.search(proj_pattern, text, re.IGNORECASE | re.DOTALL)
    
    if not proj_match:
        return projects
    
    proj_text = proj_match.group(1)
    
    # Split by bullet points or numbers
    proj_items = re.split(r'[\n](?:[•\-\*]|\d+\.)\s*', proj_text)
    
    for item in proj_items:
        item = item.strip()
        if item and len(item) > 10:
            # Take first line or first 100 chars
            project_name = item.split('\n')[0][:100]
            projects.append(project_name.strip())
    
    return projects


def extract_certifications(text: str) -> List[str]:
    """
    Extract certifications from resume
    
    Args:
        text: Resume text
        
    Returns:
        List of certifications
    """
    certifications = []
    
    # Find certifications section
    cert_pattern = r'(?:certifications?|certificates?|licenses?)[:\s]+(.*?)(?:\n\n[A-Z][A-Z\s]+\n|education|skills|experience|$)'
    cert_match = re.search(cert_pattern, text, re.IGNORECASE | re.DOTALL)
    
    if not cert_match:
        return certifications
    
    cert_text = cert_match.group(1)
    
    # Split by lines or bullet points
    cert_items = re.split(r'[\n][•\-\*]?\s*', cert_text)
    
    for item in cert_items:
        item = item.strip()
        if item and len(item) > 5:
            certifications.append(item)
    
    return certifications


def parse_resume(file_path: str | Path) -> ResumeData:
    """
    Main function to parse resume and extract all information
    
    Args:
        file_path: Path to resume file (PDF or DOCX)
        
    Returns:
        ResumeData object with extracted information
    """
    logger.info(f"Parsing resume: {file_path}")
    
    file_path = Path(file_path)
    
    # Extract text based on file type
    if file_path.suffix.lower() == '.pdf':
        text = extract_text_from_pdf(file_path)
    elif file_path.suffix.lower() in ['.docx', '.doc']:
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_path.suffix}")
    
    if not text:
        raise ValueError("No text could be extracted from resume")
    
    # Load NLP model
    try:
        nlp_model = load_spacy_model()
    except Exception as e:
        logger.error(f"Failed to load spaCy model: {e}")
        nlp_model = None

    # Extract all components
    try:
        resume_data = ResumeData(
            name=extract_name(text, nlp_model) if nlp_model else "Candidate",
            email=extract_email(text),
            phone=extract_phone(text),
            skills=extract_skills(text, nlp_model) if nlp_model else extract_skills_fallback(text),
            education=extract_education(text, nlp_model) if nlp_model else [],
            experience=extract_experience(text, nlp_model) if nlp_model else [],
            projects=extract_projects(text),
            certifications=extract_certifications(text),
            raw_text=text
        )
    except Exception as e:
        logger.error(f"Error extracting resume components: {e}")
        import traceback
        traceback.print_exc()
        # Return basic data if parsing fails
        import uuid
        resume_data = ResumeData(
            name="Unknown Candidate",
            email=extract_email(text),
            phone=extract_phone(text),
            skills=[],
            education=[],
            experience=[],
            projects=[],
            certifications=[],
            raw_text=text
        )

    logger.info(f"Resume parsed successfully. Found {len(resume_data.skills)} skills")
    
    return resume_data


def save_resume_to_json(resume_data: ResumeData, output_path: str | Path):
    """
    Save parsed resume data to JSON file
    
    Args:
        resume_data: ResumeData object
        output_path: Path to output JSON file
    """
    from utils.json_handler import append_to_json
    
    # Convert to dict
    resume_dict = resume_data.model_dump(mode='json')
    
    # Append to JSON file
    append_to_json(resume_dict, output_path, key=resume_data.resume_id)
    logger.info(f"Resume saved to {output_path}")
