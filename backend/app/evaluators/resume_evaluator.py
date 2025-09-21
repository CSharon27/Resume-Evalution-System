"""Main resume evaluation system combining hard and semantic matching."""

import time
from typing import Dict, List, Any, Tuple
from backend.app.evaluators.hard_matcher import HardMatcher
from backend.app.evaluators.semantic_matcher import SemanticMatcher
from backend.app.config import settings
import openai

# Set OpenAI API key from config (only if LLM is enabled)
if settings.enable_llm and settings.openai_api_key:
    openai.api_key = settings.openai_api_key

def generate_mock_llm_feedback(resume_data: Dict[str, Any], job_requirements: Dict[str, Any]) -> Dict[str, Any]:
    """Generate mock LLM feedback when OpenAI API is not available."""
    return {
        "improvement_suggestions": "This is a demo version. To get AI-powered feedback, please configure your OpenAI API key in the settings.",
        "overall_feedback": "Resume evaluation completed using rule-based matching. For detailed AI analysis, please enable LLM features with a valid OpenAI API key.",
        "strengths": ["Good technical skills", "Relevant experience", "Clear formatting"],
        "weaknesses": ["Could benefit from more specific achievements", "Consider adding quantifiable results"],
        "missing_skills": ["Advanced certifications", "Leadership experience"],
        "missing_certifications": ["Industry-specific certifications"],
        "missing_projects": ["Portfolio projects", "Open source contributions"]
    }

class ResumeEvaluator:
    """Main resume evaluation system."""
    
    def __init__(self):
        """Initialize the evaluator with hard and semantic matchers."""
        self.hard_matcher = HardMatcher()
        self.semantic_matcher = SemanticMatcher()
    
    def calculate_final_score(self, hard_score: float, semantic_score: float) -> float:
        """Calculate final weighted score."""
        return (
            hard_score * settings.hard_match_weight +
            semantic_score * settings.semantic_match_weight
        )
    
    def determine_verdict(self, final_score: float) -> str:
        """Determine suitability verdict based on final score."""
        if final_score >= settings.high_suitability_threshold:
            return "High"
        elif final_score >= settings.medium_suitability_threshold:
            return "Medium"
        else:
            return "Low"
    
    def generate_missing_elements(self, hard_match_results: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate missing elements analysis."""
        missing_skills = hard_match_results.get('missing_skills', [])
        missing_qualifications = hard_match_results.get('missing_qualifications', [])
        
        # Generate missing projects and certifications based on missing skills
        missing_projects = []
        missing_certifications = []
        
        # Technical skills that would benefit from projects
        technical_skills = ['python', 'java', 'javascript', 'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'sql', 'mongodb', 'postgresql']
        
        for skill in missing_skills:
            skill_lower = skill.lower()
            if any(tech in skill_lower for tech in technical_skills):
                missing_projects.append(f"Build a project using {skill}")
                missing_certifications.append(f"Get certified in {skill}")
        
        # Add general project suggestions if no specific skills are missing
        if not missing_projects and missing_skills:
            missing_projects.append("Build a portfolio project showcasing your skills")
            missing_projects.append("Create a GitHub repository with sample code")
        
        return {
            'missing_skills': missing_skills,
            'missing_qualifications': missing_qualifications,
            'missing_projects': missing_projects,
            'missing_certifications': missing_certifications
        }
    
    def evaluate_resume(self, resume_data: Dict[str, Any], job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate a resume against a job description."""
        start_time = time.time()
        
        try:
            # Hard matching
            hard_match_results = self.hard_matcher.calculate_hard_match_score(resume_data, job_data)
            hard_score = hard_match_results['hard_match_score']
            
            # Semantic matching
            semantic_match_results = self.semantic_matcher.calculate_semantic_match_score(resume_data, job_data)
            semantic_score = semantic_match_results['semantic_match_score']
            
            # Calculate final score
            final_score = self.calculate_final_score(hard_score, semantic_score)
            
            # Determine verdict
            verdict = self.determine_verdict(final_score)
            
            # Generate missing elements
            missing_elements = self.generate_missing_elements(hard_match_results)
            
            # Generate LLM feedback (use mock if API key not available)
            if settings.enable_llm and settings.openai_api_key:
                llm_feedback = self.semantic_matcher.generate_llm_feedback(
                    resume_data, job_data, hard_match_results
                )
            else:
                llm_feedback = generate_mock_llm_feedback(resume_data, job_data)
            
            # Calculate evaluation time
            evaluation_time = time.time() - start_time
            
            # Compile results
            results = {
                'relevance_score': round(final_score, 2),
                'hard_match_score': round(hard_score, 2),
                'semantic_match_score': round(semantic_score, 2),
                'verdict': verdict,
                'missing_skills': missing_elements['missing_skills'],
                'missing_qualifications': missing_elements['missing_qualifications'],
                'missing_projects': missing_elements['missing_projects'],
                'missing_certifications': missing_elements['missing_certifications'],
                'strengths': llm_feedback['strengths'],
                'weaknesses': llm_feedback['weaknesses'],
                'improvement_suggestions': llm_feedback['improvement_suggestions'],
                'overall_feedback': llm_feedback['overall_feedback'],
                'evaluation_time': round(evaluation_time, 2),
                'hard_match_details': hard_match_results,
                'semantic_match_details': semantic_match_results
            }
            
            return results
            
        except Exception as e:
            return {
                'error': f"Evaluation failed: {str(e)}",
                'relevance_score': 0,
                'hard_match_score': 0,
                'semantic_match_score': 0,
                'verdict': 'Low',
                'missing_skills': [],
                'missing_qualifications': [],
                'missing_projects': [],
                'missing_certifications': [],
                'strengths': [],
                'weaknesses': [],
                'improvement_suggestions': [],
                'overall_feedback': f"Error during evaluation: {str(e)}",
                'evaluation_time': time.time() - start_time
            }
    
    def batch_evaluate(self, resumes: List[Dict[str, Any]], job_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Evaluate multiple resumes against a job description."""
        results = []
        
        for resume in resumes:
            result = self.evaluate_resume(resume, job_data)
            results.append(result)
        
        return results
    
    def get_evaluation_summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get summary statistics for batch evaluation results."""
        if not results:
            return {}
        
        scores = [r.get('relevance_score', 0) for r in results if 'relevance_score' in r]
        verdicts = [r.get('verdict', 'Low') for r in results if 'verdict' in r]
        
        summary = {
            'total_resumes': len(results),
            'average_score': round(sum(scores) / len(scores), 2) if scores else 0,
            'highest_score': max(scores) if scores else 0,
            'lowest_score': min(scores) if scores else 0,
            'high_suitability': verdicts.count('High'),
            'medium_suitability': verdicts.count('Medium'),
            'low_suitability': verdicts.count('Low'),
            'verdict_distribution': {
                'High': verdicts.count('High'),
                'Medium': verdicts.count('Medium'),
                'Low': verdicts.count('Low')
            }
        }
        
        return summary



