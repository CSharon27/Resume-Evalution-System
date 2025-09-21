"""Hard matching system for keyword and skill-based resume evaluation."""

import re
from typing import Dict, List, Tuple, Any
from difflib import SequenceMatcher
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class HardMatcher:
    """Hard matching system for exact and fuzzy keyword matching."""
    
    def __init__(self):
        """Initialize the hard matcher."""
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            max_features=1000
        )
    
    def calculate_keyword_similarity(self, text1: str, text2: str) -> float:
        """Calculate keyword similarity using TF-IDF and cosine similarity."""
        try:
            # Create TF-IDF vectors
            tfidf_matrix = self.vectorizer.fit_transform([text1, text2])
            
            # Calculate cosine similarity
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(similarity)
        except Exception:
            return 0.0
    
    def fuzzy_match(self, text1: str, text2: str, threshold: float = 0.6) -> float:
        """Calculate fuzzy string matching score."""
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text."""
        # Remove common stop words and extract meaningful words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        # Filter out common words
        stop_words = {
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
            'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before',
            'after', 'above', 'below', 'between', 'among', 'within', 'without'
        }
        
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        return list(set(keywords))
    
    def match_skills(self, resume_skills: List[str], required_skills: List[str]) -> Dict[str, Any]:
        """Match resume skills against required skills."""
        matched_skills = []
        missing_skills = []
        partial_matches = []
        
        resume_skills_lower = [skill.lower() for skill in resume_skills]
        required_skills_lower = [skill.lower() for skill in required_skills]
        
        for required_skill in required_skills:
            skill_found = False
            
            # Exact match
            if required_skill.lower() in resume_skills_lower:
                matched_skills.append(required_skill)
                skill_found = True
            else:
                # Fuzzy match
                best_match_score = 0
                best_match_skill = None
                
                for resume_skill in resume_skills:
                    similarity = self.fuzzy_match(required_skill, resume_skill)
                    if similarity > best_match_score and similarity > 0.7:
                        best_match_score = similarity
                        best_match_skill = resume_skill
                
                if best_match_skill:
                    partial_matches.append({
                        'required': required_skill,
                        'matched': best_match_skill,
                        'score': best_match_score
                    })
                    skill_found = True
            
            if not skill_found:
                missing_skills.append(required_skill)
        
        # Calculate skill match score
        total_skills = len(required_skills)
        exact_matches = len(matched_skills)
        partial_matches_count = len(partial_matches)
        
        skill_score = ((exact_matches + partial_matches_count * 0.7) / total_skills) * 100 if total_skills > 0 else 0
        
        return {
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'partial_matches': partial_matches,
            'skill_score': skill_score,
            'total_required': total_skills,
            'exact_matches': exact_matches,
            'partial_matches_count': partial_matches_count
        }
    
    def match_education(self, resume_education: List[Dict], required_qualifications: List[str]) -> Dict[str, Any]:
        """Match resume education against required qualifications."""
        matched_qualifications = []
        missing_qualifications = []
        
        # Extract degree information from resume education
        resume_degrees = []
        for edu in resume_education:
            if 'degree' in edu:
                resume_degrees.append(edu['degree'].lower())
        
        # Match qualifications
        for qualification in required_qualifications:
            qual_found = False
            qual_lower = qualification.lower()
            
            for degree in resume_degrees:
                if self.fuzzy_match(qual_lower, degree) > 0.6:
                    matched_qualifications.append(qualification)
                    qual_found = True
                    break
            
            if not qual_found:
                missing_qualifications.append(qualification)
        
        # Calculate education match score
        total_qualifications = len(required_qualifications)
        education_score = (len(matched_qualifications) / total_qualifications) * 100 if total_qualifications > 0 else 100
        
        return {
            'matched_qualifications': matched_qualifications,
            'missing_qualifications': missing_qualifications,
            'education_score': education_score,
            'total_required': total_qualifications,
            'matched_count': len(matched_qualifications)
        }
    
    def match_experience(self, resume_experience: List[Dict], required_experience: str) -> Dict[str, Any]:
        """Match resume experience against required experience."""
        # Extract years from required experience
        exp_years = 0
        if required_experience and required_experience != "Not specified":
            years_match = re.search(r'(\d+)', required_experience)
            if years_match:
                exp_years = int(years_match.group(1))
        
        # For now, we'll use a simple heuristic
        # In a real system, you'd parse resume experience more carefully
        resume_years = len(resume_experience) * 2  # Rough estimate
        
        experience_score = 100 if resume_years >= exp_years else (resume_years / exp_years) * 100
        
        return {
            'required_years': exp_years,
            'estimated_resume_years': resume_years,
            'experience_score': experience_score,
            'meets_requirement': resume_years >= exp_years
        }
    
    def calculate_hard_match_score(self, resume_data: Dict[str, Any], job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall hard match score."""
        # Extract data
        resume_skills = resume_data.get('skills', [])
        resume_education = resume_data.get('education', [])
        resume_experience = resume_data.get('experience', [])
        
        required_skills = job_data.get('must_have_skills', [])
        good_to_have_skills = job_data.get('good_to_have_skills', [])
        required_qualifications = job_data.get('qualifications', [])
        required_experience = job_data.get('experience_required', 'Not specified')
        
        # Match skills
        must_have_skill_match = self.match_skills(resume_skills, required_skills)
        good_to_have_skill_match = self.match_skills(resume_skills, good_to_have_skills)
        
        # Match education
        education_match = self.match_education(resume_education, required_qualifications)
        
        # Match experience
        experience_match = self.match_experience(resume_experience, required_experience)
        
        # Calculate weighted scores
        must_have_weight = 0.4
        good_to_have_weight = 0.2
        education_weight = 0.2
        experience_weight = 0.2
        
        hard_match_score = (
            must_have_skill_match['skill_score'] * must_have_weight +
            good_to_have_skill_match['skill_score'] * good_to_have_weight +
            education_match['education_score'] * education_weight +
            experience_match['experience_score'] * experience_weight
        )
        
        return {
            'hard_match_score': hard_match_score,
            'must_have_skills': must_have_skill_match,
            'good_to_have_skills': good_to_have_skill_match,
            'education': education_match,
            'experience': experience_match,
            'missing_skills': must_have_skill_match['missing_skills'],
            'missing_qualifications': education_match['missing_qualifications']
        }
