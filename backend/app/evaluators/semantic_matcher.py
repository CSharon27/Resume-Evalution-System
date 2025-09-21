# app/evaluators/semantic_matcher.py

from sentence_transformers import SentenceTransformer
import openai
from typing import Dict, Any, List
import numpy as np

class SemanticMatcher:
    """Semantic matching system using embeddings and LLM for resume evaluation."""

    def __init__(self):
        """Initialize the semantic matcher."""
        # SentenceTransformer model for embeddings
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Load OpenAI API key from config (only if LLM is enabled)
        from app.config import settings
        if settings.enable_llm and settings.openai_api_key:
            openai.api_key = settings.openai_api_key

    def embed_text(self, text: str) -> np.ndarray:
        """Generate embedding for a given text using SentenceTransformer."""
        return self.embedding_model.encode(text)

    def semantic_similarity(self, text1: str, text2: str) -> float:
        """Compute cosine similarity between two texts."""
        emb1 = self.embed_text(text1)
        emb2 = self.embed_text(text2)
        return float(np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2)))

    def evaluate_resume(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate a resume and return a semantic analysis.
        This is a placeholder; replace with real embeddings + LLM logic.
        """
        # Example: Calculate dummy scores
        relevance_score = 75.0
        hard_match_score = 70.0
        semantic_match_score = 80.0

        # Example: extract missing skills / certifications / projects
        missing_skills: List[str] = ["NLP", "AWS", "Machine Learning"]
        missing_certifications: List[str] = []
        missing_projects: List[str] = []

        strengths: List[str] = ["Python", "Machine Learning"]
        weaknesses: List[str] = ["Docker", "Kubernetes"]
        improvement_suggestions: List[str] = [
            "Add cloud certifications", 
            "Learn Docker and Kubernetes basics"
        ]

        overall_feedback = "Good match, but needs more cloud and container skills."

        return {
            "relevance_score": relevance_score,
            "hard_match_score": hard_match_score,
            "semantic_match_score": semantic_match_score,
            "missing_skills": missing_skills,
            "missing_certifications": missing_certifications,
            "missing_projects": missing_projects,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "improvement_suggestions": improvement_suggestions,
            "overall_feedback": overall_feedback
        }
    
    def calculate_semantic_match_score(self, resume_data: Dict[str, Any], job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate semantic match score between resume and job description."""
        # Extract text content
        resume_text = resume_data.get('content', '')
        job_text = job_data.get('content', '')
        
        # Calculate semantic similarity
        similarity_score = self.semantic_similarity(resume_text, job_text)
        
        # Convert to percentage
        semantic_score = similarity_score * 100
        
        return {
            'semantic_match_score': round(semantic_score, 2),
            'similarity_score': round(similarity_score, 4),
            'resume_length': len(resume_text),
            'job_length': len(job_text)
        }
    
    def generate_llm_feedback(self, resume_data: Dict[str, Any], job_data: Dict[str, Any], hard_match_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate LLM feedback for resume evaluation."""
        from app.config import settings
        
        # If LLM is not enabled or API key is not available, return mock feedback
        if not settings.enable_llm or not settings.openai_api_key:
            return {
                "strengths": ["Good technical skills", "Relevant experience", "Clear formatting"],
                "weaknesses": ["Could benefit from more specific achievements", "Consider adding quantifiable results"],
                "improvement_suggestions": "This is a demo version. To get AI-powered feedback, please configure your OpenAI API key in the settings.",
                "overall_feedback": "Resume evaluation completed using rule-based matching. For detailed AI analysis, please enable LLM features with a valid OpenAI API key."
            }
        
        # If LLM is enabled, try to generate real feedback
        try:
            # This would contain the actual OpenAI API call
            # For now, return enhanced mock feedback
            return {
                "strengths": ["Strong technical background", "Relevant project experience", "Good educational foundation"],
                "weaknesses": ["Limited industry experience", "Could use more certifications"],
                "improvement_suggestions": "Consider adding more specific achievements with quantifiable results. Include relevant certifications and industry-specific skills.",
                "overall_feedback": "Good potential candidate with solid technical skills. Would benefit from more industry experience and specific achievements."
            }
        except Exception as e:
            # Fallback to mock feedback if API call fails
            return {
                "strengths": ["Technical skills present", "Basic qualifications met"],
                "weaknesses": ["Limited detailed analysis available"],
                "improvement_suggestions": f"LLM analysis temporarily unavailable: {str(e)}",
                "overall_feedback": "Evaluation completed with basic matching. LLM analysis could not be performed."
            }
