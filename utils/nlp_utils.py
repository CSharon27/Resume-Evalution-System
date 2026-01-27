"""
HireLens NLP Utilities
Helper functions for loading and managing NLP models
"""

import spacy
from sentence_transformers import SentenceTransformer
from typing import List
import re
import string


# Global model cache
_spacy_model = None
_sentence_transformer = None


def load_spacy_model(model_name: str = "en_core_web_sm"):
    """
    Load spaCy model (cached)
    
    Args:
        model_name: Name of spaCy model to load
        
    Returns:
        Loaded spaCy model
    """
    global _spacy_model
    
    if _spacy_model is None:
        try:
            _spacy_model = spacy.load(model_name)
        except OSError:
            print(f"Model '{model_name}' not found. Downloading...")
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", model_name])
            _spacy_model = spacy.load(model_name)
    
    return _spacy_model


def load_sentence_transformer(model_name: str = "all-MiniLM-L6-v2"):
    """
    Load Sentence Transformer model (cached)
    
    Args:
        model_name: Name of Sentence Transformer model
        
    Returns:
        Loaded Sentence Transformer model
    """
    global _sentence_transformer
    
    if _sentence_transformer is None:
        print(f"Loading Sentence Transformer: {model_name}...")
        _sentence_transformer = SentenceTransformer(model_name)
        print("Model loaded successfully!")
    
    return _sentence_transformer


def preprocess_text(text: str) -> str:
    """
    Preprocess text for NLP
    
    Args:
        text: Raw text
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove special characters but keep basic punctuation
    # text = re.sub(r'[^\w\s.,;:!?-]', ' ', text)
    
    return text.strip()


def tokenize(text: str) -> List[str]:
    """
    Simple tokenization
    
    Args:
        text: Text to tokenize
        
    Returns:
        List of tokens
    """
    # Remove punctuation and split
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = text.lower().split()
    return [t for t in tokens if len(t) > 1]


def extract_sentences(text: str, nlp_model=None) -> List[str]:
    """
    Extract sentences from text using spaCy
    
    Args:
        text: Text to process
        nlp_model: spaCy model (will load if None)
        
    Returns:
        List of sentences
    """
    if nlp_model is None:
        nlp_model = load_spacy_model()
    
    doc = nlp_model(text)
    return [sent.text.strip() for sent in doc.sents]


def extract_noun_phrases(text: str, nlp_model=None) -> List[str]:
    """
    Extract noun phrases from text
    
    Args:
        text: Text to process
        nlp_model: spaCy model (will load if None)
        
    Returns:
        List of noun phrases
    """
    if nlp_model is None:
        nlp_model = load_spacy_model()
    
    doc = nlp_model(text)
    return [chunk.text for chunk in doc.noun_chunks]


def is_technical_skill(word: str, skill_list: List[str]) -> bool:
    """
    Check if a word matches any skill in the skill list
    
    Args:
        word: Word to check
        skill_list: List of valid skills
        
    Returns:
        True if word is a skill, False otherwise
    """
    word_lower = word.lower()
    
    for skill in skill_list:
        if skill.lower() == word_lower or skill.lower() in word_lower:
            return True
    
    return False


def clean_skill_name(skill: str) -> str:
    """
    Clean and normalize skill name
    
    Args:
        skill: Raw skill name
        
    Returns:
        Cleaned skill name
    """
    # Remove extra whitespace
    skill = ' '.join(skill.split())
    
    # Capitalize properly
    # Common abbreviations should be uppercase
    uppercase_skills = ['aws', 'gcp', 'sql', 'nosql', 'api', 'rest', 'html', 
                       'css', 'php', 'iot', 'ai', 'ml', 'nlp', 'ci', 'cd',
                       'tdd', 'bdd', 'orm', 'mvc', 'mvvm','rpa', 'etl']
    
    if skill.lower() in uppercase_skills:
        return skill.upper()
    
    # Title case for multi-word skills
    return skill.title()


def calculate_text_similarity(text1: str, text2: str, method: str = "jaccard") -> float:
    """
    Calculate similarity between two text strings
    
    Args:
        text1: First text
        text2: Second text
        method: Similarity method ('jaccard' or 'overlap')
        
    Returns:
        Similarity score (0-1)
    """
    tokens1 = set(tokenize(text1))
    tokens2 = set(tokenize(text2))
    
    if not tokens1 or not tokens2:
        return 0.0
    
    intersection = tokens1.intersection(tokens2)
    
    if method == "jaccard":
        union = tokens1.union(tokens2)
        return len(intersection) / len(union) if union else 0.0
    elif method == "overlap":
        return len(intersection) / min(len(tokens1), len(tokens2))
    else:
        return 0.0
