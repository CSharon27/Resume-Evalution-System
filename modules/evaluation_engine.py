"""
HireLens Evaluation Engine
Hybrid NLP evaluation using TF-IDF, Fuzzy Matching, and Sentence Embeddings
"""

from typing import List, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rapidfuzz import fuzz
from config.config import (
    TFIDF_WEIGHT, FUZZY_WEIGHT, EMBEDDING_WEIGHT,
    HIGH_RELEVANCE_THRESHOLD, MEDIUM_RELEVANCE_THRESHOLD
)
from config.models import ResumeData, JobDescription, EvaluationResult
from utils.nlp_utils import load_sentence_transformer, preprocess_text
from utils.logger import logger


def tfidf_similarity(resume_text: str, job_text: str) -> float:
    """
    Calculate TF-IDF cosine similarity between resume and job description
    
    Args:
        resume_text: Resume text
        job_text: Job description text
        
    Returns:
        Similarity score (0-1)
    """
    try:
        # Preprocess texts
        resume_clean = preprocess_text(resume_text)
        job_clean = preprocess_text(job_text)
        
        if not resume_clean or not job_clean:
            return 0.0
        
        # Create TF-IDF vectors
        vectorizer = TfidfVectorizer(
            max_features=500,
            stop_words='english',
            ngram_range=(1, 2)  # Unigrams and bigrams
        )
        
        # Fit and transform
        tfidf_matrix = vectorizer.fit_transform([resume_clean, job_clean])
        
        # Calculate cosine similarity
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        return float(similarity)
    
    except Exception as e:
        logger.error(f"Error calculating TF-IDF similarity: {e}")
        return 0.0


def fuzzy_skill_match(resume_skills: List[str], job_skills: List[str]) -> float:
    """
    Calculate fuzzy matching score between resume and job skills
    
    Args:
        resume_skills: List of skills from resume
        job_skills: List of skills from job description
        
    Returns:
        Fuzzy match score (0-1)
    """
    if not resume_skills or not job_skills:
        return 0.0
    
    try:
        matched_count = 0
        total_score = 0
        
        for job_skill in job_skills:
            # Find best match for this job skill in resume skills
            best_match_score = 0
            
            for resume_skill in resume_skills:
                # Use token set ratio for flexible matching
                score = fuzz.token_set_ratio(
                    job_skill.lower(),
                    resume_skill.lower()
                )
                best_match_score = max(best_match_score, score)
            
            total_score += best_match_score
            
            # Consider it matched if score > 70
            if best_match_score > 70:
                matched_count += 1
        
        # Average match score
        avg_score = total_score / len(job_skills) if job_skills else 0
        
        # Normalize to 0-1
        return avg_score / 100.0
    
    except Exception as e:
        logger.error(f"Error calculating fuzzy match: {e}")
        return 0.0


def embedding_similarity(resume_text: str, job_text: str) -> float:
    """
    Calculate semantic similarity using sentence embeddings
    
    Args:
        resume_text: Resume text
        job_text: Job description text
        
    Returns:
        Embedding similarity score (0-1)
    """
    try:
        # Load sentence transformer model
        model = load_sentence_transformer()
        
        # Preprocess texts
        resume_clean = preprocess_text(resume_text)
        job_clean = preprocess_text(job_text)
        
        if not resume_clean or not job_clean:
            return 0.0
        
        # Truncate texts to avoid memory issues (first 1000 chars)
        resume_clean = resume_clean[:1000]
        job_clean = job_clean[:1000]
        
        # Generate embeddings
        embeddings = model.encode([resume_clean, job_clean])
        
        # Calculate cosine similarity
        similarity = cosine_similarity(
            embeddings[0].reshape(1, -1),
            embeddings[1].reshape(1, -1)
        )[0][0]
        
        return float(similarity)
    
    except Exception as e:
        logger.error(f"Error calculating embedding similarity: {e}")
        return 0.0


def calculate_hybrid_score(
    tfidf_score: float,
    fuzzy_score: float,
    embedding_score: float,
    weights: Tuple[float, float, float] = None
) -> float:
    """
    Calculate weighted hybrid score
    
    Args:
        tfidf_score: TF-IDF similarity (0-1)
        fuzzy_score: Fuzzy match score (0-1)
        embedding_score: Embedding similarity (0-1)
        weights: Tuple of (tfidf_weight, fuzzy_weight, embedding_weight)
        
    Returns:
        Hybrid score (0-100)
    """
    if weights is None:
        weights = (TFIDF_WEIGHT, FUZZY_WEIGHT, EMBEDDING_WEIGHT)
    
    w1, w2, w3 = weights
    
    # Weighted average
    hybrid = (w1 * tfidf_score) + (w2 * fuzzy_score) + (w3 * embedding_score)
    
    # Scale to 0-100
    return hybrid * 100


def classify_relevance(score: float) -> str:
    """
    Classify relevance based on score
    
    Args:
        score: Hybrid score (0-100)
        
    Returns:
        Classification: "High", "Medium", or "Low"
    """
    if score >= HIGH_RELEVANCE_THRESHOLD:
        return "Good Fit"
    elif score >= MEDIUM_RELEVANCE_THRESHOLD:
        return "Average Fit"
    else:
        return "Not Fit"


def identify_matched_skills(resume_skills: List[str], job_skills: List[str]) -> List[str]:
    """
    Identify skills that match between resume and job
    
    Args:
        resume_skills: Resume skills
        job_skills: Job skills
        
    Returns:
        List of matched skills
    """
    matched = []
    
    for job_skill in job_skills:
        for resume_skill in resume_skills:
            # Exact match or fuzzy match
            if (job_skill.lower() == resume_skill.lower() or
                fuzz.token_set_ratio(job_skill.lower(), resume_skill.lower()) > 85):
                matched.append(job_skill)
                break
    
    return matched


def identify_missing_skills(resume_skills: List[str], job_skills: List[str]) -> List[str]:
    """
    Identify skills from job description missing in resume
    
    Args:
        resume_skills: Resume skills
        job_skills: Job skills
        
    Returns:
        List of missing skills
    """
    missing = []
    
    for job_skill in job_skills:
        found = False
        for resume_skill in resume_skills:
            if fuzz.token_set_ratio(job_skill.lower(), resume_skill.lower()) > 85:
                found = True
                break
        
        if not found:
            missing.append(job_skill)
    
    return missing


def evaluate(resume_data: ResumeData, job_data: JobDescription) -> EvaluationResult:
    """
    Main evaluation function - performs hybrid NLP evaluation
    
    Args:
        resume_data: Parsed resume data
        job_data: Analyzed job description
        
    Returns:
        EvaluationResult with scores and classification
    """
    logger.info(f"Evaluating resume {resume_data.resume_id} against job {job_data.job_id}")
    
    # Get text content
    resume_text = resume_data.raw_text
    job_text = job_data.role_description
    
    # Combine all job skills for evaluation
    all_job_skills = job_data.must_have_skills + job_data.good_to_have_skills
    
    # Calculate individual scores
    logger.info("Calculating TF-IDF similarity...")
    tfidf_score = tfidf_similarity(resume_text, job_text)
    logger.info(f"TF-IDF score: {tfidf_score:.3f}")
    
    logger.info("Calculating fuzzy skill match...")
    fuzzy_score = fuzzy_skill_match(resume_data.skills, all_job_skills)
    logger.info(f"Fuzzy match score: {fuzzy_score:.3f}")
    
    logger.info("Calculating embedding similarity...")
    embed_score = embedding_similarity(resume_text, job_text)
    logger.info(f"Embedding score: {embed_score:.3f}")
    
    # Calculate hybrid score
    hybrid_score = calculate_hybrid_score(tfidf_score, fuzzy_score, embed_score)
    logger.info(f"Hybrid score: {hybrid_score:.2f}")
    
    # Classify relevance
    classification = classify_relevance(hybrid_score)
    logger.info(f"Classification: {classification}")
    
    # Identify matched and missing skills
    matched_skills = identify_matched_skills(resume_data.skills, all_job_skills)
    missing_skills = identify_missing_skills(resume_data.skills, all_job_skills)
    
    # Create evaluation result
    evaluation = EvaluationResult(
        resume_id=resume_data.resume_id,
        job_id=job_data.job_id,
        tfidf_score=tfidf_score,
        fuzzy_score=fuzzy_score,
        embedding_score=embed_score,
        hybrid_score=hybrid_score,
        classification=classification,
        matched_skills=matched_skills,
        missing_skills=missing_skills
    )
    
    logger.info(f"Evaluation complete. Matched: {len(matched_skills)}, Missing: {len(missing_skills)}")
    
    return evaluation


def save_evaluation(evaluation: EvaluationResult, output_path: str):
    """
    Save evaluation result to JSON file
    
    Args:
        evaluation: EvaluationResult object
        output_path: Path to output JSON file
    """
    from utils.json_handler import append_to_json
    
    # Convert to dict
    eval_dict = evaluation.model_dump(mode='json')
    
    # Append to JSON file
    append_to_json(eval_dict, output_path, key=evaluation.evaluation_id)
    logger.info(f"Evaluation saved to {output_path}")
