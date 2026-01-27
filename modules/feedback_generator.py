"""
HireLens Feedback Generator
Generates comprehensive, actionable feedback for candidates
"""

from typing import List, Dict
from config.models import (
    EvaluationResult, SkillGap, CourseRecommendation,
    Feedback, LearningRoadmap, Course
)
from utils.logger import logger


def identify_strengths(evaluation: EvaluationResult, resume_skills: List[str]) -> List[str]:
    """
    Identify candidate strengths based on evaluation
    
    Args:
        evaluation: Evaluation result
        resume_skills: Skills from resume
        
    Returns:
        List of strength statements
    """
    strengths = []
    
    # High match rate
    if evaluation.hybrid_score >= 80:
        strengths.append("Excellent overall match for this position")
    elif evaluation.hybrid_score >= 70:
        strengths.append("Strong alignment with job requirements")
    
    # Matched skills
    if len(evaluation.matched_skills) > 0:
        if len(evaluation.matched_skills) >= 5:
            strengths.append(f"Possesses {len(evaluation.matched_skills)} key technical skills required for the role")
        
        # Highlight specific high-value skills
        high_value_skills = ["AWS", "Kubernetes", "Docker", "Python", "Java", "React", 
                            "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch"]
        
        matched_high_value = [s for s in evaluation.matched_skills if s in high_value_skills]
        if matched_high_value:
            strengths.append(f"Strong expertise in high-demand technologies: {', '.join(matched_high_value[:3])}")
    
    # Strong embedding score (semantic match)
    if evaluation.embedding_score >= 0.7:
        strengths.append("Resume demonstrates relevant experience and context matching the job description")
    
    # Total skills
    if len(resume_skills) >= 10:
        strengths.append(f"Diverse technical skill set with {len(resume_skills)} identified skills")
    
    return strengths


def identify_weaknesses(skill_gap: SkillGap, evaluation: EvaluationResult) -> List[str]:
    """
    Identify candidate weaknesses based on skill gaps
    
    Args:
        skill_gap: Skill gap analysis
        evaluation: Evaluation result
        
    Returns:
        List of weakness statements
    """
    weaknesses = []
    
    # Critical missing skills
    if skill_gap.missing_must_have:
        if len(skill_gap.missing_must_have) == 1:
            weaknesses.append(f"Missing critical required skill: {skill_gap.missing_must_have[0]}")
        elif len(skill_gap.missing_must_have) <= 3:
            weaknesses.append(f"Lacks required skills: {', '.join(skill_gap.missing_must_have)}")
        else:
            weaknesses.append(f"Missing {len(skill_gap.missing_must_have)} required skills including: " 
                            f"{', '.join(skill_gap.missing_must_have[:3])}")
    
    # Moderate gaps
    if len(skill_gap.missing_good_to_have) >= 3:
        weaknesses.append(f"Could strengthen profile with preferred skills like: "
                        f"{', '.join(skill_gap.missing_good_to_have[:3])}")
    
    # Weak areas
    if skill_gap.weak_skills:
        weaknesses.append(f"Areas needing improvement: {', '.join(skill_gap.weak_skills[:2])}")
    
    # Low overall score
    if evaluation.hybrid_score < 50:
        weaknesses.append("Overall profile needs significant development to match job requirements")
    elif evaluation.hybrid_score < 70:
        weaknesses.append("Profile partially matches requirements but has room for improvement")
    
    # Low TF-IDF (keyword mismatch)
    if evaluation.tfidf_score < 0.4:
        weaknesses.append("Resume could better highlight relevant keywords and technologies from job description")
    
    return weaknesses


def generate_improvement_suggestions(skill_gap: SkillGap) -> List[str]:
    """
    Generate actionable improvement suggestions
    
    Args:
        skill_gap: Skill gap analysis
        
    Returns:
        List of suggestion statements
    """
    suggestions = []
    
    # Priority on must-have skills
    if skill_gap.missing_must_have:
        for skill in skill_gap.missing_must_have[:3]:
            suggestions.append(f"Acquire {skill} skills through online courses or hands-on projects")
    
    # Category-specific suggestions
    if skill_gap.categorized_gaps:
        if "cloud" in skill_gap.categorized_gaps:
            suggestions.append("Gain cloud platform experience through free tier accounts and certifications")
        
        if "devops" in skill_gap.categorized_gaps:
            suggestions.append("Build CI/CD pipelines and containerize applications for practical DevOps experience")
        
        if "programming" in skill_gap.categorized_gaps:
            suggestions.append("Strengthen programming fundamentals through coding challenges and open-source contributions")
        
        if "database" in skill_gap.categorized_gaps:
            suggestions.append("Practice database design and optimization with real-world projects")
    
    # General suggestions
    suggestions.append("Update resume to emphasize skills and experiences relevant to the target role")
    suggestions.append("Build portfolio projects demonstrating proficiency in key technologies")
    
    # Limit to top suggestions
    return suggestions[:6]


def create_learning_roadmap(
    skill_gap: SkillGap,
    recommendations: Dict[str, List[Course]]
) -> LearningRoadmap:
    """
    Create structured learning roadmap
    
    Args:
        skill_gap: Skill gap analysis
        recommendations: Course recommendations
        
    Returns:
        LearningRoadmap object
    """
    roadmap = LearningRoadmap()
    
    # Immediate (1-2 weeks): Top 3 critical skills with beginner courses
    immediate_skills = skill_gap.missing_must_have[:3]
    for skill in immediate_skills:
        if skill in recommendations:
            courses = recommendations[skill]
            beginner_courses = [c for c in courses if c.level == "Beginner"]
            if beginner_courses:
                roadmap.immediate.append(f"Complete {skill} fundamentals: {beginner_courses[0].title}")
            else:
                roadmap.immediate.append(f"Start learning {skill} basics")
        else:
            roadmap.immediate.append(f"Begin {skill} fundamentals")
    
    # If no must-have skills, add good-to-have
    if not roadmap.immediate and skill_gap.missing_good_to_have:
        for skill in skill_gap.missing_good_to_have[:2]:
            roadmap.immediate.append(f"Begin {skill} basics")
    
    # Short-term (1-3 months): Intermediate skills + good-to-have
    short_term_skills = skill_gap.missing_must_have[3:6] + skill_gap.missing_good_to_have[:3]
    for skill in short_term_skills:
        if skill in recommendations:
            courses = recommendations[skill]
            if courses:
                roadmap.short_term.append(f"Master {skill}: {courses[0].title}")
            else:
                roadmap.short_term.append(f"Develop {skill} proficiency")
        else:
            roadmap.short_term.append(f"Gain experience with {skill}")
    
    # Add practical application
    if skill_gap.categorized_gaps.get("devops"):
        roadmap.short_term.append("Build and deploy application using CI/CD pipeline")
    if skill_gap.categorized_gaps.get("cloud"):
        roadmap.short_term.append("Deploy full-stack application on cloud platform")

    # Fallback if short-term is still empty
    if not roadmap.short_term:
        if skill_gap.missing_must_have:
            roadmap.short_term.append(f"Build a small project integrating {skill_gap.missing_must_have[0]}")
        
        roadmap.short_term.append("Solve 10+ intermediate coding problems on LeetCode/HackerRank")
        roadmap.short_term.append("Contribute to Documentation or Fix bugs in an Open Source repo")
    
    # Long-term (3-6 months): Advanced topics and certifications
    for skill in skill_gap.missing_must_have[:3]:
        if skill in recommendations:
            courses = recommendations[skill]
            advanced_courses = [c for c in courses if c.level in ["Intermediate", "Advanced"]]
            if advanced_courses:
                roadmap.long_term.append(f"Achieve {skill} mastery: {advanced_courses[0].title}")
        
        # Add certification suggestions
        cert_skills = ["AWS", "Azure", "GCP", "Kubernetes", "Python", "Java"]
        if skill in cert_skills:
            roadmap.long_term.append(f"Earn professional {skill} certification")
    
    # Add portfolio and contribution goals
    roadmap.long_term.append("Build comprehensive portfolio with 3-5 substantial projects")
    roadmap.long_term.append("Contribute to open-source projects in target technology stack")
    
    return roadmap


def generate_overall_assessment(evaluation: EvaluationResult, skill_gap: SkillGap) -> str:
    """
    Generate overall assessment summary
    
    Args:
        evaluation: Evaluation result
        skill_gap: Skill gap analysis
        
    Returns:
        Assessment summary string
    """
    score = evaluation.hybrid_score
    classification = evaluation.classification
    
    if classification == "High":
        assessment = (
            f"With a score of {score:.1f}/100, you are a strong candidate for this position. "
            f"You possess {len(evaluation.matched_skills)} of the key required skills. "
        )
        
        if skill_gap.missing_must_have:
            assessment += (
                f"To become an ideal candidate, focus on acquiring the {len(skill_gap.missing_must_have)} "
                f"remaining required skills, particularly {skill_gap.missing_must_have[0]}. "
            )
        else:
            assessment += "You meet all critical requirements. Consider expanding into advanced topics. "
    
    elif classification == "Medium":
        assessment = (
            f"With a score of {score:.1f}/100, you show moderate alignment with this position. "
            f"You have {len(evaluation.matched_skills)} relevant skills, but "
            f"{len(skill_gap.missing_must_have)} critical skills are missing. "
        )
        
        assessment += (
            "Focus your learning efforts on the required skills gap to significantly improve your candidacy. "
            "With dedicated effort over 2-3 months, you can become a competitive candidate. "
        )
    
    else:  # Low
        assessment = (
            f"With a score of {score:.1f}/100, there is a significant gap between your current profile "
            f"and this position's requirements. You match {len(evaluation.matched_skills)} skills but need "
            f"to develop {len(skill_gap.missing_must_have)} critical required skills. "
        )
        
        assessment += (
            "Consider this a longer-term career goal (4-6 months) and follow the structured learning roadmap. "
            "Alternatively, seek positions that better align with your current skill set while building these skills. "
        )
    
    return assessment


def generate_feedback(
    evaluation: EvaluationResult,
    skill_gap: SkillGap,
    recommendations: Dict[str, List[Course]],
    resume_skills: List[str]
) -> Feedback:
    """
    Main function to generate comprehensive feedback
    
    Args:
        evaluation: Evaluation result
        skill_gap: Skill gap analysis
        recommendations: Course recommendations
        resume_skills: Skills from resume
        
    Returns:
        Feedback object with complete analysis
    """
    logger.info(f"Generating feedback for evaluation {evaluation.evaluation_id}")
    
    # Generate all feedback components
    strengths = identify_strengths(evaluation, resume_skills)
    weaknesses = identify_weaknesses(skill_gap, evaluation)
    suggestions = generate_improvement_suggestions(skill_gap)
    learning_roadmap = create_learning_roadmap(skill_gap, recommendations)
    overall_assessment = generate_overall_assessment(evaluation, skill_gap)
    
    # Create feedback object
    feedback = Feedback(
        evaluation_id=evaluation.evaluation_id,
        strengths=strengths,
        weaknesses=weaknesses,
        suggestions=suggestions,
        learning_roadmap=learning_roadmap,
        overall_assessment=overall_assessment
    )
    
    logger.info("Feedback generated successfully")
    
    return feedback


def save_feedback(feedback: Feedback, output_path: str):
    """
    Save feedback to JSON file
    
    Args:
        feedback: Feedback object
        output_path: Path to output JSON file
    """
    from utils.json_handler import append_to_json
    
    # Convert to dict
    feedback_dict = feedback.model_dump(mode='json')
    
    # Append to JSON file
    append_to_json(feedback_dict, output_path, key=feedback.feedback_id)
    logger.info(f"Feedback saved to {output_path}")
