"""
MongoDB Models for ONJOB Platform
"""

from datetime import datetime
from bson import ObjectId

# Helper function to safely convert datetime to ISO format
def safe_isoformat(value):
    """Safely convert datetime to ISO format string"""
    if value is None:
        return None
    if hasattr(value, 'isoformat'):
        return value.isoformat()
    if isinstance(value, str):
        return value
    return None

# ============== USER MODEL ==============
class User:
    """User account model"""
    
    @staticmethod
    def create(user_data):
        """Create a new user document"""
        return {
            '_id': ObjectId(),
            'name': user_data.get('name', ''),
            'email': user_data.get('email', '').lower(),
            'password': user_data.get('password', ''),  # Should be hashed
            'role': user_data.get('role', 'job_seeker'),  # job_seeker or recruiter
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'is_active': True,
            'last_login': None,
            'profile_completed': False
        }
    
    @staticmethod
    def to_json(user):
        """Convert user document to JSON response"""
        if not user:
            return None
        return {
            'id': str(user.get('_id')),
            'name': user.get('name'),
            'email': user.get('email'),
            'role': user.get('role'),
            'created_at': safe_isoformat(user.get('created_at')),
            'profile_completed': user.get('profile_completed', False)
        }


# ============== JOB MODEL ==============
class Job:
    """Job listing model"""
    
    @staticmethod
    def create(job_data, recruiter_id):
        """Create a new job document"""
        return {
            '_id': ObjectId(),
            'title': job_data.get('title', ''),
            'company': job_data.get('company', ''),
            'location': job_data.get('location', ''),
            'type': job_data.get('type', 'Full-time'),  # Full-time, Part-time, Contract, Internship
            'category': job_data.get('category', ''),
            'description': job_data.get('description', ''),
            'requirements': job_data.get('requirements', []),
            'responsibilities': job_data.get('responsibilities', []),
            'skills_required': job_data.get('skills_required', []),
            'experience_level': job_data.get('experience_level', 'Entry'),  # Entry, Mid, Senior
            'salary_min': job_data.get('salary_min'),
            'salary_max': job_data.get('salary_max'),
            'salary_currency': job_data.get('salary_currency', 'USD'),
            'posted_by': ObjectId(recruiter_id) if recruiter_id else None,
            'status': 'active',  # active, closed, draft
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'expires_at': job_data.get('expires_at'),
            'views_count': 0,
            'applications_count': 0
        }
    
    @staticmethod
    def to_json(job):
        """Convert job document to JSON response"""
        if not job:
            return None
        return {
            'id': str(job.get('_id')),
            'title': job.get('title'),
            'company': job.get('company'),
            'location': job.get('location'),
            'type': job.get('type'),
            'category': job.get('category'),
            'description': job.get('description'),
            'requirements': job.get('requirements', []),
            'responsibilities': job.get('responsibilities', []),
            'skills_required': job.get('skills_required', []),
            'experience_level': job.get('experience_level'),
            'salary_min': job.get('salary_min'),
            'salary_max': job.get('salary_max'),
            'salary_currency': job.get('salary_currency'),
            'posted_by': str(job.get('posted_by')) if job.get('posted_by') else None,
            'status': job.get('status'),
            'created_at': safe_isoformat(job.get('created_at')),
            'applications_count': job.get('applications_count', 0),
            'views_count': job.get('views_count', 0)
        }


# ============== APPLICATION MODEL ==============
class Application:
    """Job application model"""
    
    @staticmethod
    def create(job_id, user_id, application_data):
        """Create a new application document"""
        return {
            '_id': ObjectId(),
            'job_id': ObjectId(job_id),
            'user_id': ObjectId(user_id),
            'status': 'pending',  # pending, reviewed, shortlisted, rejected, hired
            'cover_letter': application_data.get('cover_letter', ''),
            'resume_url': application_data.get('resume_url'),
            'expected_salary': application_data.get('expected_salary'),
            'notice_period': application_data.get('notice_period'),
            'match_percentage': application_data.get('match_percentage', 0),
            'applied_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'notes': '',
            'recruiter_feedback': None
        }
    
    @staticmethod
    def to_json(application, job=None, user=None):
        """Convert application document to JSON response"""
        if not application:
            return None
        return {
            'id': str(application.get('_id')),
            'job_id': str(application.get('job_id')),
            'user_id': str(application.get('user_id')),
            'status': application.get('status'),
            'cover_letter': application.get('cover_letter'),
            'match_percentage': application.get('match_percentage', 0),
            'applied_at': safe_isoformat(application.get('applied_at')),
            'job': Job.to_json(job) if job else None,
            'user': User.to_json(user) if user else None
        }


# ============== PROFILE MODEL ==============
class Profile:
    """User profile model"""
    
    @staticmethod
    def create(user_id, profile_data):
        """Create a new profile document"""
        return {
            '_id': ObjectId(),
            'user_id': ObjectId(user_id),
            'bio': profile_data.get('bio', ''),
            'phone': profile_data.get('phone', ''),
            'location': profile_data.get('location', ''),
            'website': profile_data.get('website', ''),
            'linkedin_url': profile_data.get('linkedin_url', ''),
            'github_url': profile_data.get('github_url', ''),
            
            # For Job Seekers
            'skills': profile_data.get('skills', []),
            'experience': profile_data.get('experience', []),  # Array of experience objects
            'education': profile_data.get('education', []),  # Array of education objects
            'resume_url': profile_data.get('resume_url'),
            'resume_parsed_data': profile_data.get('resume_parsed_data', {}),
            'cv_path': profile_data.get('cv_path'),  # ADDED: Path to uploaded CV file
            'position': profile_data.get('position', ''),  # ADDED: Job title/position
            'company': profile_data.get('company', ''),  # ADDED: Company name
            'experience_years': profile_data.get('experience_years', 0),  # ADDED: Years of experience
            
            'job_preferences': {
                'desired_roles': profile_data.get('desired_roles', []),
                'preferred_locations': profile_data.get('preferred_locations', []),
                'remote_preference': profile_data.get('remote_preference', False),
                'expected_salary_min': profile_data.get('expected_salary_min'),
                'expected_salary_max': profile_data.get('expected_salary_max')
            },
            
            # For Recruiters
            'company_name': profile_data.get('company_name'),
            'company_website': profile_data.get('company_website'),
            'company_description': profile_data.get('company_description'),
            'company_logo_url': profile_data.get('company_logo_url'),
            
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
    
    @staticmethod
    def to_json(profile):
        """Convert profile document to JSON response"""
        if not profile:
            return None
        return {
            'id': str(profile.get('_id')),
            'user_id': str(profile.get('user_id')),
            'bio': profile.get('bio'),
            'phone': profile.get('phone'),
            'location': profile.get('location'),
            'website': profile.get('website'),
            'linkedin_url': profile.get('linkedin_url'),
            'github_url': profile.get('github_url'),
            'skills': profile.get('skills', []),
            'experience': profile.get('experience', []),
            'education': profile.get('education', []),
            'resume_url': profile.get('resume_url'),
            'cv_path': profile.get('cv_path'),  # ADDED: Return cv_path
            'position': profile.get('position', ''),  # ADDED: Return position
            'company': profile.get('company', ''),  # ADDED: Return company
            'experience_years': profile.get('experience_years', 0),  # ADDED: Return experience_years
            'job_preferences': profile.get('job_preferences', {}),
            'company_name': profile.get('company_name'),
            'company_website': profile.get('company_website'),
            'company_description': profile.get('company_description'),
            'company_logo_url': profile.get('company_logo_url'),
            'created_at': safe_isoformat(profile.get('created_at')),
            'updated_at': safe_isoformat(profile.get('updated_at'))
        }


# ============== RESUME MODEL ==============
class Resume:
    """Resume/CV upload model"""
    
    @staticmethod
    def create(user_id, file_data):
        """Create a new resume document"""
        return {
            '_id': ObjectId(),
            'user_id': ObjectId(user_id),
            'filename': file_data.get('filename'),
            'original_name': file_data.get('original_name'),
            'file_path': file_data.get('file_path'),
            'file_size': file_data.get('file_size'),
            'file_type': file_data.get('file_type'),
            'parsed_content': file_data.get('parsed_content', {}),
            'skills_extracted': file_data.get('skills_extracted', []),
            'uploaded_at': datetime.utcnow(),
            'is_current': True
        }
    
    @staticmethod
    def to_json(resume):
        """Convert resume document to JSON response"""
        if not resume:
            return None
        return {
            'id': str(resume.get('_id')),
            'filename': resume.get('filename'),
            'original_name': resume.get('original_name'),
            'file_size': resume.get('file_size'),
            'skills_extracted': resume.get('skills_extracted', []),
            'uploaded_at': safe_isoformat(resume.get('uploaded_at')),
            'is_current': resume.get('is_current', False)
        }


# ============== DATABASE INDEXES ==============
def create_indexes(db):
    """Create necessary indexes for collections"""
    
    # Users collection indexes
    db.users.create_index('email', unique=True)
    db.users.create_index('role')
    
    # Jobs collection indexes
    db.jobs.create_index('posted_by')
    db.jobs.create_index('category')
    db.jobs.create_index('location')
    db.jobs.create_index('type')
    db.jobs.create_index('status')
    db.jobs.create_index('created_at')
    
    # Applications collection indexes
    db.applications.create_index([('job_id', 1), ('user_id', 1)], unique=True)
    db.applications.create_index('user_id')
    db.applications.create_index('job_id')
    db.applications.create_index('status')
    db.applications.create_index('applied_at')
    
    # Profiles collection indexes
    db.profiles.create_index('user_id', unique=True)
    db.profiles.create_index('skills')
    db.profiles.create_index('location')
    
    # Resumes collection indexes
    db.resumes.create_index('user_id')
    db.resumes.create_index([('user_id', 1), ('is_current', 1)])
    
    print("✅ Database indexes created successfully")