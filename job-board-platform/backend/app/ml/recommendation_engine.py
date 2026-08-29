"""
ML-powered job recommendation engine
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List, Dict

class JobRecommendationEngine:
    """
    ML-based job recommendation system using TF-IDF and cosine similarity
    """
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=100,
            stop_words='english',
            lowercase=True,
            token_pattern=r'\b\w+\b'
        )
        self.job_vectors = None
        self.jobs = []
    
    def _extract_job_text(self, job: Dict) -> str:
        """Extract searchable text from job"""
        title = job.get('title', '')
        description = job.get('description', '')
        skills = ' '.join(job.get('required_skills', []))
        experience = job.get('experience_level', '')
        
        return f"{title} {description} {skills} {experience}".lower()
    
    def _extract_profile_text(self, profile: Dict) -> str:
        """Extract searchable text from user profile"""
        skills = ' '.join(profile.get('skills', []))
        bio = profile.get('bio', '')
        position = profile.get('position', '')
        experience = str(profile.get('experience_years', 0))
        
        return f"{skills} {bio} {position} {experience} years experience".lower()
    
    def fit(self, jobs: List[Dict]):
        """Train recommendation engine with jobs"""
        if not jobs:
            return
        
        self.jobs = jobs
        
        # Extract text from all jobs
        job_texts = [self._extract_job_text(job) for job in jobs]
        
        # Fit vectorizer and transform
        self.job_vectors = self.vectorizer.fit_transform(job_texts)
    
    def recommend(self, user_profile: Dict, top_n: int = 5) -> List[Dict]:
        """
        Recommend jobs based on user profile
        Returns top N most similar jobs
        """
        if not self.jobs or self.job_vectors is None:
            return []
        
        # Extract and vectorize user profile
        profile_text = self._extract_profile_text(user_profile)
        profile_vector = self.vectorizer.transform([profile_text])
        
        # Calculate similarity scores
        similarities = cosine_similarity(profile_vector, self.job_vectors)[0]
        
        # Get top N indices
        top_indices = np.argsort(similarities)[::-1][:top_n]
        
        # Return recommendations with scores
        recommendations = []
        for idx in top_indices:
            if similarities[idx] > 0:  # Only include if there's some similarity
                recommendations.append({
                    'job': self.jobs[idx],
                    'score': float(similarities[idx]),
                    'match_percentage': round(similarities[idx] * 100, 2)
                })
        
        return recommendations
    
    def get_skill_match(self, user_skills: List[str], job_skills: List[str]) -> Dict:
        """Calculate skill match between user and job"""
        user_skills_set = set(s.lower() for s in user_skills)
        job_skills_set = set(s.lower() for s in job_skills)
        
        matched = user_skills_set & job_skills_set
        missing = job_skills_set - user_skills_set
        extra = user_skills_set - job_skills_set
        
        match_percentage = len(matched) / len(job_skills_set) * 100 if job_skills_set else 0
        
        return {
            'matched_skills': list(matched),
            'missing_skills': list(missing),
            'extra_skills': list(extra),
            'match_percentage': round(match_percentage, 2)
        }
    
    def get_experience_match(self, user_experience: int, min_experience: int) -> Dict:
        """Calculate experience match"""
        if min_experience == 0:
            return {
                'meets_requirement': True,
                'match_percentage': 100,
                'note': 'Any experience level acceptable'
            }
        
        if user_experience >= min_experience:
            return {
                'meets_requirement': True,
                'match_percentage': 100,
                'note': f'Has {user_experience} years, meets requirement'
            }
        else:
            percentage = (user_experience / min_experience) * 100
            return {
                'meets_requirement': False,
                'match_percentage': round(percentage, 2),
                'note': f'Has {user_experience} years, needs {min_experience} years'
            }
