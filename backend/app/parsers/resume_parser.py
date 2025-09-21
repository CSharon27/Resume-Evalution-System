"""Resume parsing utilities for extracting text and structured data from PDF/DOCX files."""

import os
import json
import re
from typing import Dict, List, Optional, Any
from pathlib import Path

import fitz  # PyMuPDF
import pdfplumber
from docx import Document
import docx2txt
import spacy
from spacy.matcher import Matcher


class ResumeParser:
    """Parse resumes from PDF and DOCX files."""
    
    def __init__(self):
        """Initialize the parser with spaCy model."""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("spaCy model not found. Please install with: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        self.matcher = Matcher(self.nlp.vocab) if self.nlp else None
        self._setup_patterns()
    
    def _setup_patterns(self):
        """Setup regex patterns for extracting resume sections."""
        if not self.matcher:
            return
            
        # Skills patterns
        skills_pattern = [
            {"LOWER": {"IN": ["skills", "technical", "technologies", "tools", "programming"]}},
            {"OP": ":"},
            {"OP": "?"}
        ]
        self.matcher.add("SKILLS", [skills_pattern])
        
        # Education patterns
        education_pattern = [
            {"LOWER": {"IN": ["education", "academic", "qualification", "degree"]}},
            {"OP": ":"},
            {"OP": "?"}
        ]
        self.matcher.add("EDUCATION", [education_pattern])
        
        # Experience patterns
        experience_pattern = [
            {"LOWER": {"IN": ["experience", "work", "employment", "career"]}},
            {"OP": ":"},
            {"OP": "?"}
        ]
        self.matcher.add("EXPERIENCE", [experience_pattern])
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file using PyMuPDF."""
        try:
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""
    
    def extract_text_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file."""
        try:
            return docx2txt.process(file_path)
        except Exception as e:
            print(f"Error extracting text from DOCX: {e}")
            return ""
    
    def extract_text(self, file_path: str) -> str:
        """Extract text from file based on extension."""
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif file_ext == '.docx':
            return self.extract_text_from_docx(file_path)
        elif file_ext == '.txt':  # <-- Add support for plain text files
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                raise ValueError(f"Error reading text file: {e}")
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize extracted text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,;:!?()-]', ' ', text)
        # Remove multiple spaces
        text = re.sub(r' +', ' ', text)
        return text.strip()
    
    def extract_sections(self, text: str) -> Dict[str, str]:
        """Extract structured sections from resume text."""
        sections = {
            'skills': '',
            'education': '',
            'experience': '',
            'projects': '',
            'certifications': ''
        }
        
        if not self.nlp:
            return sections
        
        doc = self.nlp(text)
        
        # Find section headers
        for match_id, start, end in self.matcher(doc):
            label = self.nlp.vocab.strings[match_id]
            section_text = doc[start:end].text
            
            # Extract content after the header
            next_section_start = self._find_next_section(doc, end)
            content = doc[end:next_section_start].text.strip()
            
            if label.lower() in sections:
                sections[label.lower()] = content
        
        return sections
    
    def _find_next_section(self, doc, start_pos: int) -> int:
        """Find the start of the next section."""
        # Look for common section headers
        section_headers = [
            'education', 'experience', 'skills', 'projects', 'certifications',
            'achievements', 'awards', 'publications', 'references'
        ]
        
        for i in range(start_pos, len(doc)):
            token = doc[i]
            if token.text.lower() in section_headers and i > start_pos + 5:
                return i
        
        return len(doc)
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from resume text."""
        skills = []
        
        # Common technical skills
        technical_skills = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node.js',
            'django', 'flask', 'fastapi', 'spring', 'express', 'sql', 'mysql',
            'postgresql', 'mongodb', 'redis', 'docker', 'kubernetes', 'aws',
            'azure', 'gcp', 'git', 'github', 'gitlab', 'jenkins', 'ci/cd',
            'machine learning', 'deep learning', 'tensorflow', 'pytorch',
            'pandas', 'numpy', 'scikit-learn', 'opencv', 'nlp', 'computer vision'
        ]
        
        text_lower = text.lower()
        for skill in technical_skills:
            if skill in text_lower:
                skills.append(skill.title())
        
        # Extract skills from skills section
        skills_section = self.extract_sections(text)['skills']
        if skills_section:
            # Split by common delimiters
            skill_list = re.split(r'[,;|\n]', skills_section)
            for skill in skill_list:
                skill = skill.strip()
                if skill and len(skill) > 1:
                    skills.append(skill)
        
        return list(set(skills))  # Remove duplicates
    
    def extract_education(self, text: str) -> List[Dict[str, str]]:
        """Extract education information."""
        education = []
        
        # Common degree patterns
        degree_patterns = [
            r'bachelor[s]?\s+of\s+\w+',
            r'master[s]?\s+of\s+\w+',
            r'phd\s+in\s+\w+',
            r'b\.?[a-z]\.?[a-z]\.?',
            r'm\.?[a-z]\.?[a-z]\.?',
            r'ph\.?d\.?'
        ]
        
        education_section = self.extract_sections(text)['education']
        if education_section:
            lines = education_section.split('\n')
            for line in lines:
                line = line.strip()
                if any(re.search(pattern, line, re.IGNORECASE) for pattern in degree_patterns):
                    education.append({'degree': line})
        
        return education
    
    def extract_experience(self, text: str) -> List[Dict[str, str]]:
        """Extract work experience information."""
        experience = []
        
        # Look for common job title patterns
        job_patterns = [
            r'software\s+engineer',
            r'data\s+scientist',
            r'web\s+developer',
            r'full\s+stack\s+developer',
            r'frontend\s+developer',
            r'backend\s+developer',
            r'machine\s+learning\s+engineer',
            r'devops\s+engineer'
        ]
        
        experience_section = self.extract_sections(text)['experience']
        if experience_section:
            lines = experience_section.split('\n')
            for line in lines:
                line = line.strip()
                if any(re.search(pattern, line, re.IGNORECASE) for pattern in job_patterns):
                    experience.append({'position': line})
        
        return experience
    
    def parse_resume(self, file_path: str, student_name: str = "", student_email: str = "") -> Dict[str, Any]:
        """Parse a resume file and extract structured data."""
        try:
            # Extract raw text
            raw_text = self.extract_text(file_path)
            if not raw_text:
                raise ValueError("Could not extract text from file")
            
            # Clean text
            clean_text = self.clean_text(raw_text)
            
            # Extract sections
            sections = self.extract_sections(clean_text)
            
            # Extract structured data
            skills = self.extract_skills(clean_text)
            education = self.extract_education(clean_text)
            experience = self.extract_experience(clean_text)
            
            return {
                'filename': os.path.basename(file_path),
                'student_name': student_name,
                'student_email': student_email,
                'content': clean_text,
                'raw_content': raw_text,
                'sections': sections,
                'skills': skills,
                'education': education,
                'experience': experience,
                'file_path': file_path
            }
        
        except Exception as e:
            raise ValueError(f"Error parsing resume: {str(e)}")
