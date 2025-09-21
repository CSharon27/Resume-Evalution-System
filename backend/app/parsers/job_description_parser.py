"""Job description parsing utilities for extracting structured requirements."""

import re
import json
from typing import Dict, List, Any, Optional
from spacy import load as spacy_load


class JobDescriptionParser:
    """Parse job descriptions to extract requirements and skills."""
    
    def __init__(self):
        """Initialize the parser with spaCy model."""
        try:
            self.nlp = spacy_load("en_core_web_sm")
        except OSError:
            print("spaCy model not found. Please install with: python -m spacy download en_core_web_sm")
            self.nlp = None
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize job description text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,;:!?()-]', ' ', text)
        # Remove multiple spaces
        text = re.sub(r' +', ' ', text)
        return text.strip()
    
    def extract_job_title(self, text: str) -> str:
        """Extract job title from job description."""
        # Common job title patterns
        title_patterns = [
            r'job\s+title[:\s]+([^\n]+)',
            r'position[:\s]+([^\n]+)',
            r'role[:\s]+([^\n]+)',
            r'we\s+are\s+looking\s+for\s+([^\n]+)',
            r'hiring\s+for\s+([^\n]+)'
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        # If no specific pattern found, try to extract from first few lines
        lines = text.split('\n')[:5]
        for line in lines:
            line = line.strip()
            if len(line) > 5 and len(line) < 100:
                return line
        
        return "Software Engineer"  # Default fallback
    
    def extract_company(self, text: str) -> str:
        """Extract company name from job description."""
        # Look for company name patterns
        company_patterns = [
            r'at\s+([A-Z][a-zA-Z\s&]+)',
            r'company[:\s]+([A-Z][a-zA-Z\s&]+)',
            r'organization[:\s]+([A-Z][a-zA-Z\s&]+)'
        ]
        
        for pattern in company_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return "Company Name"  # Default fallback
    
    def extract_location(self, text: str) -> str:
        """Extract job location from job description."""
        # Common location patterns
        location_patterns = [
            r'location[:\s]+([^\n]+)',
            r'based\s+in\s+([^\n]+)',
            r'office\s+in\s+([^\n]+)',
            r'hybrid\s+([^\n]+)',
            r'remote\s+([^\n]+)'
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        # Look for common city names
        cities = ['Hyderabad', 'Bangalore', 'Pune', 'Delhi', 'Mumbai', 'Chennai', 'Kolkata']
        for city in cities:
            if city.lower() in text.lower():
                return city
        
        return "Location Not Specified"
    
    def extract_skills(self, text: str) -> Dict[str, List[str]]:
        """Extract must-have and good-to-have skills."""
        must_have_skills = []
        good_to_have_skills = []
        
        # Common technical skills
        technical_skills = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node.js',
            'django', 'flask', 'fastapi', 'spring', 'express', 'sql', 'mysql',
            'postgresql', 'mongodb', 'redis', 'docker', 'kubernetes', 'aws',
            'azure', 'gcp', 'git', 'github', 'gitlab', 'jenkins', 'ci/cd',
            'machine learning', 'deep learning', 'tensorflow', 'pytorch',
            'pandas', 'numpy', 'scikit-learn', 'opencv', 'nlp', 'computer vision',
            'html', 'css', 'bootstrap', 'jquery', 'typescript', 'php', 'ruby',
            'c++', 'c#', '.net', 'android', 'ios', 'swift', 'kotlin'
        ]
        
        text_lower = text.lower()
        
        # Extract skills mentioned in requirements
        for skill in technical_skills:
            if skill in text_lower:
                # Check if it's mentioned as must-have
                if any(keyword in text_lower for keyword in ['must', 'required', 'mandatory', 'essential']):
                    must_have_skills.append(skill.title())
                else:
                    good_to_have_skills.append(skill.title())
        
        # Look for specific skill sections
        skills_section_patterns = [
            r'required\s+skills[:\s]*([^\n]+)',
            r'must\s+have[:\s]*([^\n]+)',
            r'technical\s+skills[:\s]*([^\n]+)',
            r'qualifications[:\s]*([^\n]+)'
        ]
        
        for pattern in skills_section_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                skills_text = match.group(1)
                skills_list = re.split(r'[,;|\n]', skills_text)
                for skill in skills_list:
                    skill = skill.strip()
                    if skill and len(skill) > 1:
                        must_have_skills.append(skill)
        
        return {
            'must_have': list(set(must_have_skills)),
            'good_to_have': list(set(good_to_have_skills))
        }
    
    def extract_qualifications(self, text: str) -> List[str]:
        """Extract educational qualifications required."""
        qualifications = []
        
        # Common qualification patterns
        qual_patterns = [
            r'bachelor[s]?\s+of\s+\w+',
            r'master[s]?\s+of\s+\w+',
            r'phd\s+in\s+\w+',
            r'b\.?[a-z]\.?[a-z]\.?',
            r'm\.?[a-z]\.?[a-z]\.?',
            r'ph\.?d\.?',
            r'degree\s+in\s+([^\n]+)',
            r'qualification[:\s]+([^\n]+)'
        ]
        
        for pattern in qual_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    qualifications.append(match[0].strip())
                else:
                    qualifications.append(match.strip())
        
        return list(set(qualifications))
    
    def extract_experience_required(self, text: str) -> str:
        """Extract years of experience required."""
        # Experience patterns
        exp_patterns = [
            r'(\d+)\s*[-+]?\s*years?\s+of\s+experience',
            r'experience[:\s]+(\d+)\s*years?',
            r'(\d+)\s*[-+]?\s*years?\s+in\s+',
            r'minimum\s+(\d+)\s*years?'
        ]
        
        for pattern in exp_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return f"{match.group(1)} years"
        
        return "Not specified"
    
    def extract_responsibilities(self, text: str) -> List[str]:
        """Extract job responsibilities."""
        responsibilities = []
        
        # Look for responsibility sections
        resp_patterns = [
            r'responsibilities[:\s]*([^\n]+)',
            r'key\s+responsibilities[:\s]*([^\n]+)',
            r'job\s+description[:\s]*([^\n]+)',
            r'what\s+you\s+will\s+do[:\s]*([^\n]+)'
        ]
        
        for pattern in resp_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                resp_text = match.group(1)
                # Split by common delimiters
                resp_list = re.split(r'[•\-\*\n]', resp_text)
                for resp in resp_list:
                    resp = resp.strip()
                    if resp and len(resp) > 10:
                        responsibilities.append(resp)
        
        return responsibilities
    
    def parse_job_description(self, text: str) -> Dict[str, Any]:
        """Parse a job description and extract structured data."""
        try:
            # Clean text
            clean_text = self.clean_text(text)
            
            # Extract structured data
            title = self.extract_job_title(clean_text)
            company = self.extract_company(clean_text)
            location = self.extract_location(clean_text)
            skills = self.extract_skills(clean_text)
            qualifications = self.extract_qualifications(clean_text)
            experience_required = self.extract_experience_required(clean_text)
            responsibilities = self.extract_responsibilities(clean_text)
            
            return {
                'title': title,
                'company': company,
                'location': location,
                'content': clean_text,
                'must_have_skills': skills['must_have'],
                'good_to_have_skills': skills['good_to_have'],
                'qualifications': qualifications,
                'experience_required': experience_required,
                'responsibilities': responsibilities
            }
        
        except Exception as e:
            raise ValueError(f"Error parsing job description: {str(e)}")
