"""
HireLens Course Recommender
Maps skill gaps to relevant online courses
"""

from typing import List, Dict
from pathlib import Path
from rapidfuzz import fuzz
from config.config import COURSES_DATASET_PATH, MAX_COURSES_PER_SKILL, MIN_COURSE_RATING
from config.models import SkillGap, Course, CourseRecommendation
from utils.json_handler import load_json
from utils.logger import logger


def load_courses_dataset(path: str | Path = None) -> Dict[str, List[Dict]]:
    """
    Load courses dataset from JSON file
    
    Args:
        path: Path to courses dataset (default: from config)
        
    Returns:
        Dictionary mapping skill to list of courses
    """
    if path is None:
        path = COURSES_DATASET_PATH
    
    courses_data = load_json(path)
    
    if not courses_data:
        logger.warning("Courses dataset is empty or not found")
        return {}
    
    logger.info(f"Loaded courses for {len(courses_data)} skills")
    return courses_data


def map_skill_to_courses(
    skill: str,
    courses_db: Dict[str, List[Dict]],
    max_courses: int = MAX_COURSES_PER_SKILL
) -> List[Course]:
    """
    Find matching courses for a skill
    
    Args:
        skill: Skill name to find courses for
        courses_db: Courses database
        max_courses: Maximum number of courses to return
        
    Returns:
        List of Course objects
    """
    courses = []
    
    # Try exact match first
    if skill in courses_db:
        course_list = courses_db[skill][:max_courses]
        for course_dict in course_list:
            courses.append(Course(**course_dict))
        return courses
    
    # Try case-insensitive match
    skill_lower = skill.lower()
    for db_skill, course_list in courses_db.items():
        if db_skill.lower() == skill_lower:
            for course_dict in course_list[:max_courses]:
                courses.append(Course(**course_dict))
            return courses
    
    # Try fuzzy matching
    best_match = None
    best_score = 0
    
    for db_skill in courses_db.keys():
        score = fuzz.ratio(skill_lower, db_skill.lower())
        if score > best_score:
            best_score = score
            best_match = db_skill
    
    # Use best match if score is high enough (> 80)
    if best_match and best_score > 80:
        logger.info(f"Fuzzy matched '{skill}' to '{best_match}' (score: {best_score})")
        course_list = courses_db[best_match][:max_courses]
        for course_dict in course_list:
            courses.append(Course(**course_dict))
        return courses
    
    # No match found
    logger.warning(f"No courses found for skill: {skill}")
    return []


def recommend_courses(
    skill_gaps: SkillGap,
    courses_db: Dict[str, List[Dict]] = None,
    max_per_skill: int = MAX_COURSES_PER_SKILL
) -> Dict[str, List[Course]]:
    """
    Generate course recommendations for skill gaps
    
    Args:
        skill_gaps: SkillGap object
        courses_db: Courses database (will load if None)
        max_per_skill: Maximum courses per skill
        
    Returns:
        Dictionary mapping skill to list of recommended courses
    """
    logger.info(f"Generating course recommendations for gap {skill_gaps.gap_id}")
    
    if courses_db is None:
        courses_db = load_courses_dataset()
    
    recommendations = {}
    
    # Prioritize must-have skills
    all_skills = []
    
    # Add must-have skills first (highest priority)
    all_skills.extend(skill_gaps.missing_must_have)
    
    # Then good-to-have skills
    all_skills.extend(skill_gaps.missing_good_to_have)
    
    # Then weak skills
    all_skills.extend(skill_gaps.weak_skills)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_skills = []
    for skill in all_skills:
        if skill not in seen:
            seen.add(skill)
            unique_skills.append(skill)
    
    # Map each skill to courses
    for skill in unique_skills:
        courses = map_skill_to_courses(skill, courses_db, max_per_skill)
        
        if courses:
            # Filter by minimum rating
            courses = [c for c in courses if c.rating >= MIN_COURSE_RATING]
            
            if courses:
                recommendations[skill] = courses
                logger.info(f"Found {len(courses)} courses for {skill}")
    
    logger.info(f"Generated recommendations for {len(recommendations)} skills")
    
    return recommendations


def save_recommendations(
    recommendation: CourseRecommendation,
    output_path: str
):
    """
    Save course recommendations to JSON file
    
    Args:
        recommendation: CourseRecommendation object
        output_path: Path to output JSON file
    """
    from utils.json_handler import append_to_json
    
    # Convert to dict (need special handling for nested Course objects)
    rec_dict = recommendation.model_dump(mode='json')
    
    # Append to JSON file
    append_to_json(rec_dict, output_path, key=recommendation.recommendation_id)
    logger.info(f"Recommendations saved to {output_path}")


def get_learning_path(
    recommendations: Dict[str, List[Course]],
    skill_gaps: SkillGap
) -> Dict[str, List[str]]:
    """
    Create a structured learning path from recommendations
    
    Args:
        recommendations: Course recommendations
        skill_gaps: Skill gaps
        
    Returns:
        Dictionary with immediate/short_term/long_term learning paths
    """
    learning_path = {
        "immediate": [],  # 1-2 weeks
        "short_term": [],  # 1-3 months
        "long_term": []  # 3-6 months
    }
    
    # Categorize by priority and course level
    for skill in skill_gaps.missing_must_have[:3]:  # Top 3 critical skills
        if skill in recommendations:
            courses = recommendations[skill]
            # Add beginner courses to immediate
            for course in courses:
                if course.level == "Beginner":
                    learning_path["immediate"].append(f"{skill}: {course.title} ({course.provider})")
                    break
    
    # Short-term: good-to-have skills
    for skill in skill_gaps.missing_good_to_have[:5]:
        if skill in recommendations:
            courses = recommendations[skill]
            for course in courses:
                if course.level in ["Beginner", "Intermediate"]:
                    learning_path["short_term"].append(f"{skill}: {course.title} ({course.provider})")
                    break
    
    # Long-term: advanced courses for must-have skills
    for skill in skill_gaps.missing_must_have[:5]:
        if skill in recommendations:
            courses = recommendations[skill]
            for course in courses:
                if course.level in ["Intermediate", "Advanced"]:
                    learning_path["long_term"].append(f"{skill}: {course.title} ({course.provider})")
                    break
    
    return learning_path


def get_top_recommendations(
    recommendations: Dict[str, List[Course]],
    top_n: int = 5
) -> List[Dict[str, any]]:
    """
    Get top N course recommendations across all skills
    
    Args:
        recommendations: All recommendations
        top_n: Number of top recommendations to return
        
    Returns:
        List of top recommended courses with skill info
    """
    all_recs = []
    
    for skill, courses in recommendations.items():
        for course in courses:
            all_recs.append({
                "skill": skill,
                "course": course,
                "priority_score": course.rating  # Could be more sophisticated
            })
    
    # Sort by rating (descending)
    all_recs.sort(key=lambda x: x["priority_score"], reverse=True)
    
    return all_recs[:top_n]
