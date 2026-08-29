"""
CV parsing utilities for extracting text and data from uploaded files
"""

import os
import PyPDF2
import re
from typing import Dict, List

# Common skills database
COMMON_SKILLS = [
    'Python', 'JavaScript', 'Java', 'C++', 'C#', 'Ruby', 'PHP', 'Go', 'Rust',
    'SQL', 'Database', 'MongoDB', 'PostgreSQL', 'MySQL', 'Redis',
    'HTML', 'CSS', 'React', 'Vue', 'Angular', 'Node.js', 'Express', 'Django', 'Flask',
    'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Git', 'CI/CD',
    'Machine Learning', 'AI', 'Data Science', 'TensorFlow', 'PyTorch', 'Pandas',
    'Communication', 'Leadership', 'Project Management', 'Agile', 'Scrum',
    'Testing', 'QA', 'DevOps', 'REST API', 'GraphQL', 'Microservices'
]

EXPERIENCE_KEYWORDS = {
    'years': r'(\d+)\s*(?:years?|yrs?)\s*(?:of\s*)?experience',
    'months': r'(\d+)\s*(?:months?|mons?)\s*(?:of\s*)?experience'
}

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF file"""
    try:
        text = ""
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

def extract_text_from_txt(file_path: str) -> str:
    """Extract text from TXT file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading TXT: {e}")
        return ""

def extract_text_from_file(file_path: str, file_ext: str) -> str:
    """Extract text from file based on extension"""
    if file_ext.lower() == 'pdf':
        return extract_text_from_pdf(file_path)
    elif file_ext.lower() == 'txt':
        return extract_text_from_txt(file_path)
    else:
        # For .doc, .docx, just read as text if possible
        try:
            return extract_text_from_txt(file_path)
        except:
            return ""

def extract_skills(text: str) -> List[str]:
    """Extract skills from CV text"""
    text_lower = text.lower()
    found_skills = []
    
    for skill in COMMON_SKILLS:
        if skill.lower() in text_lower:
            found_skills.append(skill)
    
    return list(set(found_skills))  # Remove duplicates

def extract_experience_years(text: str) -> int:
    """Extract years of experience from CV"""
    years_match = re.search(EXPERIENCE_KEYWORDS['years'], text, re.IGNORECASE)
    if years_match:
        return int(years_match.group(1))
    
    months_match = re.search(EXPERIENCE_KEYWORDS['months'], text, re.IGNORECASE)
    if months_match:
        months = int(months_match.group(1))
        return max(1, months // 12)
    
    return 0

def extract_email(text: str) -> str:
    """Extract email from CV"""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(email_pattern, text)
    return match.group(0) if match else ""

def extract_phone(text: str) -> str:
    """Extract phone number from CV"""
    phone_pattern = r'(?:\+1)?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}'
    match = re.search(phone_pattern, text)
    return match.group(0) if match else ""

def parse_cv(file_path: str, file_ext: str) -> Dict:
    """Parse CV and extract structured data"""
    try:
        # Extract text
        text = extract_text_from_file(file_path, file_ext)
        
        if not text:
            return {
                'error': 'Could not extract text from file',
                'skills': [],
                'experience_years': 0
            }
        
        # Extract information
        skills = extract_skills(text)
        experience_years = extract_experience_years(text)
        email = extract_email(text)
        phone = extract_phone(text)
        
        return {
            'text': text[:1000],  # First 1000 chars
            'skills': skills,
            'experience_years': experience_years,
            'email': email,
            'phone': phone,
            'total_text_length': len(text)
        }
    
    except Exception as e:
        return {
            'error': str(e),
            'skills': [],
            'experience_years': 0
        }
