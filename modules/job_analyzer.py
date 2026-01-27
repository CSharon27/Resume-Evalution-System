"""
HireLens Job Description Analyzer
Extracts structured requirements from job descriptions
"""

import re
from typing import List, Optional
from config.config import TECHNICAL_SKILLS
from config.models import JobDescription
from utils.nlp_utils import load_spacy_model, clean_skill_name
from utils.logger import logger


def extract_must_have_skills(text: str, nlp_model=None) -> List[str]:
    """
    Extract required/mandatory skills from job description
    
    Args:
        text: Job description text
        nlp_model: spaCy model (optional)
        
    Returns:
        List of must-have skills
    """
    must_have = set()
    text_lower = text.lower()
    
    # Keywords indicating required skills
    required_keywords = [
        'required', 'must have', 'mandatory', 'essential', 'necessary',
        'need', 'should have', 'requires', 'requirement'
    ]
    
    # Find sections with required keywords
    for keyword in required_keywords:
        # Look for patterns like "Required: Python, Java"
        pattern = rf'{keyword}[:\s]+(.*?)(?:\n\n|\n[a-z]+[:\s]|preferred|nice to have|$)'
        matches = re.finditer(pattern, text_lower, re.IGNORECASE | re.DOTALL)
        
        for match in matches:
            section_text = match.group(1)
            
            # Extract skills from this section
            for skill in TECHNICAL_SKILLS:
                if re.search(r'\b' + re.escape(skill.lower()) + r'\b', section_text):
                    must_have.add(clean_skill_name(skill))
    
    # Also scan bullet points before "preferred" section
    bullets_pattern = r'(?:requirements?|qualifications?)[:\s]+(.*?)(?:preferred|nice to have|$)'
    bullets_match = re.search(bullets_pattern, text_lower, re.IGNORECASE | re.DOTALL)
    
    if bullets_match:
        bullets_text = bullets_match.group(1)
        for skill in TECHNICAL_SKILLS:
            if re.search(r'\b' + re.escape(skill.lower()) + r'\b', bullets_text):
                must_have.add(clean_skill_name(skill))
    
    # FALLBACK: If no required skills found, scan entire text
    if not must_have:
        logger.warning("No required skills found via patterns, scanning entire job description")
        for skill in TECHNICAL_SKILLS:
            if re.search(r'\b' + re.escape(skill.lower()) + r'\b', text_lower):
                must_have.add(clean_skill_name(skill))
    
    logger.info(f"Extracted {len(must_have)} required skills from job description")
    return sorted(list(must_have))


def extract_good_to_have_skills(text: str, nlp_model=None) -> List[str]:
    """
    Extract preferred/optional skills from job description
    
    Args:
        text: Job description text
        nlp_model: spaCy model (optional)
        
    Returns:
        List of good-to-have skills
    """
    good_to_have = set()
    text_lower = text.lower()
    
    # Keywords indicating preferred skills
    preferred_keywords = [
        'preferred', 'nice to have', 'bonus', 'plus', 'desirable',
        'optional', 'advantage', 'beneficial'
    ]
    
    # Find sections with preferred keywords
    for keyword in preferred_keywords:
        pattern = rf'{keyword}[:\s]+(.*?)(?:\n\n|$)'
        matches = re.finditer(pattern, text_lower, re.IGNORECASE | re.DOTALL)
        
        for match in matches:
            section_text = match.group(1)
            
            # Extract skills from this section
            for skill in TECHNICAL_SKILLS:
                if re.search(r'\b' + re.escape(skill.lower()) + r'\b', section_text):
                    good_to_have.add(clean_skill_name(skill))
    
    logger.info(f"Extracted {len(good_to_have)} preferred skills from job description")
    return sorted(list(good_to_have))


def extract_experience_requirements(text: str) -> Optional[str]:
    """
    Extract years of experience required
    
    Args:
        text: Job description text
        
    Returns:
        Experience requirement string (e.g., "3-5 years")
    """
    # Patterns for experience
    patterns = [
        r'(\d+)\s*[-–to]+\s*(\d+)\s*years?',
        r'(\d+)\+?\s*years?',
        r'minimum\s+of\s+(\d+)\s*years?',
        r'at least\s+(\d+)\s*years?'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0)
    
    return None


def extract_job_title(text: str) -> Optional[str]:
    """
    Extract job title from job description
    Usually in first few lines or marked as "Position:" or "Role:"
    
    Args:
        text: Job description text
        
    Returns:
        Job title
    """
    # Look for explicit markers
    title_pattern = r'(?:position|role|job title|title)[:\s]+([^\n]+)'
    match = re.search(title_pattern, text, re.IGNORECASE)
    
    if match:
        return match.group(1).strip()
    
    # Fallback: first non-empty line
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        if line and len(line) < 100:  # Titles are typically short
            return line
    
    return None


def extract_company_name(text: str, nlp_model=None) -> Optional[str]:
    """
    Extract company name from job description
    
    Args:
        text: Job description text
        nlp_model: spaCy model
        
    Returns:
        Company name
    """
    # Look for explicit company mention
    company_pattern = r'(?:company|organization|employer)[:\s]+([^\n]+)'
    match = re.search(company_pattern, text, re.IGNORECASE)
    
    if match:
        return match.group(1).strip()
    
    # Use NLP to find ORG entities
    if nlp_model is None:
        nlp_model = load_spacy_model()
    
    doc = nlp_model(text[:500])  # First 500 chars
    for ent in doc.ents:
        if ent.label_ == "ORG":
            return ent.text
    
    return None


def extract_location(text: str, nlp_model=None) -> Optional[str]:
    """
    Extract job location from description
    
    Args:
        text: Job description text
        nlp_model: spaCy model
        
    Returns:
        Location string
    """
    # Look for explicit location markers
    location_pattern = r'(?:location|based in|office)[:\s]+([^\n]+)'
    match = re.search(location_pattern, text, re.IGNORECASE)
    
    if match:
        return match.group(1).strip()
    
    # Use NLP to find GPE (Geo-Political Entity)
    if nlp_model is None:
        nlp_model = load_spacy_model()
    
    doc = nlp_model(text[:500])
    for ent in doc.ents:
        if ent.label_ == "GPE":
            return ent.text
    
    return None


def extract_salary_range(text: str) -> Optional[str]:
    """
    Extract salary information if mentioned
    
    Args:
        text: Job description text
        
    Returns:
        Salary range string
    """
    # Patterns for salary
    salary_patterns = [
        r'\$[\d,]+\s*[-–to]+\s*\$[\d,]+',
        r'[\d,]+\s*[-–to]+\s*[\d,]+\s*(?:LPA|per annum|annually)',
        r'salary[:\s]+([^\n]+)'
    ]
    
    for pattern in salary_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0)
    
    return None


def analyze_job_description(job_text: str) -> JobDescription:
    """
    Main function to analyze job description and extract all requirements
    
    Args:
        job_text: Job description text
        
    Returns:
        JobDescription object with extracted information
    """
    logger.info("Analyzing job description...")
    
    if not job_text or len(job_text.strip()) < 50:
        raise ValueError("Job description text is too short or empty")
    
    # Load NLP model
    nlp_model = load_spacy_model()
    
    # Extract all components
    job_data = JobDescription(
        title=extract_job_title(job_text),
        company=extract_company_name(job_text, nlp_model),
        must_have_skills=extract_must_have_skills(job_text, nlp_model),
        good_to_have_skills=extract_good_to_have_skills(job_text, nlp_model),
        experience_required=extract_experience_requirements(job_text),
        role_description=job_text,
        location=extract_location(job_text, nlp_model),
        salary_range=extract_salary_range(job_text)
    )
    
    # Remove duplicates between must_have and good_to_have
    good_to_have_set = set(job_data.good_to_have_skills) - set(job_data.must_have_skills)
    job_data.good_to_have_skills = sorted(list(good_to_have_set))
    
    logger.info(f"Job description analyzed. Found {len(job_data.must_have_skills)} required skills, "
                f"{len(job_data.good_to_have_skills)} preferred skills")
    
    return job_data


def save_job_to_json(job_data: JobDescription, output_path: str):
    """
    Save job description data to JSON file
    
    Args:
        job_data: JobDescription object
        output_path: Path to output JSON file
    """
    from utils.json_handler import append_to_json
    
    # Convert to dict
    job_dict = job_data.model_dump(mode='json')
    
    # Append to JSON file
    append_to_json(job_dict, output_path, key=job_data.job_id)
    logger.info(f"Job description saved to {output_path}")
