"""
HireLens Skill Gap Analyzer
Identifies missing and weak skills through comparison
"""

from typing import List, Dict
from rapidfuzz import fuzz
from config.models import ResumeData, JobDescription, SkillGap, EvaluationResult
from utils.logger import logger


def identify_missing_skills(resume_skills: List[str], job_required_skills: List[str]) -> List[str]:
    """
    Identify skills completely missing from resume
    
    Args:
        resume_skills: Skills from resume
        job_required_skills: Required skills from job
        
    Returns:
        List of missing skills
    """
    missing = []
    
    for job_skill in job_required_skills:
        found = False
        
        for resume_skill in resume_skills:
            # Check for exact or close match
            if fuzz.token_set_ratio(job_skill.lower(), resume_skill.lower()) > 80:
                found = True
                break
        
        if not found:
            missing.append(job_skill)
    
    return missing


def identify_weak_skills(
    resume_skills: List[str],
    job_preferred_skills: List[str],
    fuzzy_threshold: float = 70
) -> List[str]:
    """
    Identify skills that partially match (weak areas)
    
    Args:
        resume_skills: Skills from resume
        job_preferred_skills: Preferred skills from job
        fuzzy_threshold: Threshold for considering a weak match
        
    Returns:
        List of weak/partially matching skills
    """
    weak = []
    
    for job_skill in job_preferred_skills:
        for resume_skill in resume_skills:
            similarity = fuzz.token_set_ratio(job_skill.lower(), resume_skill.lower())
            
            # Partial match (not strong enough)
            if 50 <= similarity <= fuzzy_threshold:
                weak.append(job_skill)
                break
    
    return weak


def categorize_gaps(missing_skills: List[str]) -> Dict[str, List[str]]:
    """
    Categorize skill gaps by domain
    
    Args:
        missing_skills: List of missing skills
        
    Returns:
        Dictionary mapping category to list of skills
    """
    categories = {
        "programming": [],
        "cloud": [],
        "database": [],
        "devops": [],
        "web_development": [],
        "data_science": [],
        "mobile": [],
        "testing": [],
        "soft_skills": [],
        "other": []
    }
    
    # Define skill categories
    category_keywords = {
        "programming": [
            "python", "java", "javascript", "typescript", "c++", "c#", "go",
            "rust", "ruby", "php", "swift", "kotlin", "scala", "r"
        ],
        "cloud": [
            "aws", "azure", "gcp", "google cloud", "ec2", "s3", "lambda",
            "heroku", "digitalocean", "cloudfront", "route 53"
        ],
        "database": [
            "sql", "postgresql", "mysql", "mongodb", "redis", "cassandra",
            "dynamodb", "oracle", "sql server", "elasticsearch"
        ],
        "devops": [
            "docker", "kubernetes", "jenkins", "gitlab ci", "github actions",
            "terraform", "ansible", "chef", "puppet", "ci/cd", "git"
        ],
        "web_development": [
            "react", "angular", "vue", "node.js", "express", "django",
            "flask", "fastapi", "spring boot", "html", "css", "sass",
            "bootstrap", "tailwind"
        ],
        "data_science": [
            "machine learning", "deep learning", "tensorflow", "pytorch",
            "scikit-learn", "pandas", "numpy", "jupyter", "nlp", "computer vision"
        ],
        "mobile": [
            "react native", "flutter", "android", "ios", "swiftui",
            "jetpack compose"
        ],
        "testing": [
            "jest", "mocha", "pytest", "junit", "selenium", "cypress",
            "unit testing", "integration testing", "tdd", "bdd"
        ],
        "soft_skills": [
            "agile", "scrum", "leadership", "communication", "problem solving",
            "team collaboration", "project management"
        ]
    }
    
    # Categorize each skill
    for skill in missing_skills:
        skill_lower = skill.lower()
        categorized = False
        
        for category, keywords in category_keywords.items():
            for keyword in keywords:
                if keyword in skill_lower or skill_lower in keyword:
                    categories[category].append(skill)
                    categorized = True
                    break
            
            if categorized:
                break
        
        if not categorized:
            categories["other"].append(skill)
    
    # Remove empty categories
    return {k: v for k, v in categories.items() if v}


def analyze_skill_gaps(
    resume_data: ResumeData,
    job_data: JobDescription,
    evaluation: EvaluationResult = None
) -> SkillGap:
    """
    Main skill gap analysis function
    
    Args:
        resume_data: Parsed resume data
        job_data: Analyzed job description
        evaluation: Optional evaluation result
        
    Returns:
        SkillGap object with categorized gaps
    """
    logger.info(f"Analyzing skill gaps for resume {resume_data.resume_id}")
    
    # Identify missing must-have skills
    missing_must_have = identify_missing_skills(
        resume_data.skills,
        job_data.must_have_skills
    )
    
    # Identify missing good-to-have skills
    missing_good_to_have = identify_missing_skills(
        resume_data.skills,
        job_data.good_to_have_skills
    )
    
    # Identify weak skills (partial matches)
    weak_skills = identify_weak_skills(
        resume_data.skills,
        job_data.good_to_have_skills
    )
    
    # Combine all gaps for categorization
    all_gaps = missing_must_have + missing_good_to_have
    categorized_gaps = categorize_gaps(all_gaps)
    
    # Create skill gap object
    skill_gap = SkillGap(
        evaluation_id=evaluation.evaluation_id if evaluation else "unknown",
        missing_must_have=missing_must_have,
        missing_good_to_have=missing_good_to_have,
        weak_skills=weak_skills,
        categorized_gaps=categorized_gaps
    )
    
    logger.info(f"Skill gap analysis complete. "
                f"Critical gaps: {len(missing_must_have)}, "
                f"Moderate gaps: {len(missing_good_to_have)}, "
                f"Weak areas: {len(weak_skills)}")
    
    return skill_gap


def save_skill_gaps(skill_gap: SkillGap, output_path: str):
    """
    Save skill gap analysis to JSON file
    
    Args:
        skill_gap: SkillGap object
        output_path: Path to output JSON file
    """
    from utils.json_handler import append_to_json
    
    # Convert to dict
    gap_dict = skill_gap.model_dump(mode='json')
    
    # Append to JSON file
    append_to_json(gap_dict, output_path, key=skill_gap.gap_id)
    logger.info(f"Skill gaps saved to {output_path}")


def get_priority_skills(skill_gap: SkillGap) -> List[str]:
    """
    Get prioritized list of skills to learn (most important first)
    
    Args:
        skill_gap: SkillGap object
        
    Returns:
        Prioritized list of skills
    """
    # Priority order: must-have > good-to-have > weak
    priority_skills = []
    
    # Critical gaps first
    priority_skills.extend(skill_gap.missing_must_have)
    
    # Moderate gaps
    priority_skills.extend(skill_gap.missing_good_to_have)
    
    # Weak skills
    priority_skills.extend(skill_gap.weak_skills)
    
    # Remove duplicates while preserving order
    seen = set()
    result = []
    for skill in priority_skills:
        if skill not in seen:
            seen.add(skill)
            result.append(skill)
    
    return result
