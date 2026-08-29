"""
Data Models for Job Board Platform
"""

from datetime import datetime, UTC
from typing import Dict, List, Optional
import json
import os
from config import get_config

class DataStore:
    """JSON-based data storage layer"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Ensure the data file exists"""
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump({}, f)
    
    def read(self) -> Dict:
        """Read all data from file"""
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def write(self, data: Dict):
        """Write data to file"""
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_all(self, key: str = None) -> List:
        """Get all records from a key"""
        data = self.read()
        if key:
            return data.get(key, [])
        return data
    
    def get_by_id(self, key: str, record_id: int) -> Optional[Dict]:
        """Get a specific record by ID"""
        data = self.read()
        records = data.get(key, [])
        for record in records:
            if record.get('id') == record_id:
                return record
        return None
    
    def add(self, key: str, record: Dict) -> Dict:
        """Add a new record"""
        data = self.read()
        if key not in data:
            data[key] = []
        
        # Generate ID
        record['id'] = data.get('last_id', 0) + 1
        data['last_id'] = record['id']
        
        data[key].append(record)
        self.write(data)
        return record
    
    def update(self, key: str, record_id: int, updates: Dict) -> Optional[Dict]:
        """Update an existing record"""
        data = self.read()
        records = data.get(key, [])
        
        for i, record in enumerate(records):
            if record.get('id') == record_id:
                record.update(updates)
                data[key][i] = record
                self.write(data)
                return record
        return None
    
    def delete(self, key: str, record_id: int) -> bool:
        """Delete a record"""
        data = self.read()
        records = data.get(key, [])
        
        for i, record in enumerate(records):
            if record.get('id') == record_id:
                del records[i]
                self.write(data)
                return True
        return False


class UserModel:
    """User data model"""
    
    def __init__(self, config):
        self.store = DataStore(config.USERS_DATA_FILE)
    
    def create(self, email: str, password_hash: str, role: str, name: str) -> Dict:
        """Create a new user"""
        user = {
            'email': email,
            'password_hash': password_hash,
            'role': role,  # 'job_seeker' or 'recruiter'
            'name': name,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        return self.store.add('users', user)
    
    def get_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        users = self.store.get_all('users')
        for user in users:
            if user.get('email') == email:
                return user
        return None
    
    def get_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        return self.store.get_by_id('users', user_id)
    
    def update(self, user_id: int, updates: Dict) -> Optional[Dict]:
        """Update user"""
        updates['updated_at'] = datetime.now().isoformat()
        return self.store.update('users', user_id, updates)
    
    def exists(self, email: str) -> bool:
        """Check if user exists"""
        return self.get_by_email(email) is not None


class ProfileModel:
    """User profile data model"""
    
    def __init__(self, config):
        self.store = DataStore(config.PROFILES_DATA_FILE)
    
    def create(self, user_id: int, role: str) -> Dict:
        """Create a new profile"""
        profile = {
            'user_id': user_id,
            'role': role,
            'bio': '',
            'location': '',
            'website': '',
            'company': '',
            'position': '',
            'cv_path': None,
            'skills': [],
            'experience_years': 0,
            'education': [],
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        return self.store.add('profiles', profile)
    
    def get_by_user_id(self, user_id: int) -> Optional[Dict]:
        """Get profile by user ID"""
        profiles = self.store.get_all('profiles')
        for profile in profiles:
            if profile.get('user_id') == user_id:
                return profile
        return None
    
    def update_by_user_id(self, user_id: int, updates: Dict) -> Optional[Dict]:
        """Update profile by user ID"""
        profiles = self.store.get_all('profiles')
        for profile in profiles:
            if profile.get('user_id') == user_id:
                updates['updated_at'] = datetime.now().isoformat()
                return self.store.update('profiles', profile.get('id'), updates)
        return None


class JobModel:
    """Job listing data model"""
    
    def __init__(self, config):
        self.store = DataStore(config.JOBS_DATA_FILE)
    
    def create(self, recruiter_id: int, title: str, description: str,
               required_skills: List[str], experience_level: str,
               salary_min: int = None, salary_max: int = None) -> Dict:
        """Create a new job listing"""
        job = {
            'recruiter_id': recruiter_id,
            'title': title,
            'description': description,
            'required_skills': required_skills,
            'experience_level': experience_level,
            'salary_min': salary_min,
            'salary_max': salary_max,
            'status': 'active',  # active, closed, archived
            'applicants_count': 0,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        return self.store.add('jobs', job)
    
    def get_all(self) -> List[Dict]:
        """Get all active jobs"""
        jobs = self.store.get_all('jobs')
        return [j for j in jobs if j.get('status') == 'active']
    
    def get_by_id(self, job_id: int) -> Optional[Dict]:
        """Get job by ID"""
        return self.store.get_by_id('jobs', job_id)
    
    def get_by_recruiter(self, recruiter_id: int) -> List[Dict]:
        """Get jobs posted by a recruiter"""
        jobs = self.store.get_all('jobs')
        return [j for j in jobs if j.get('recruiter_id') == recruiter_id]
    
    def update(self, job_id: int, updates: Dict) -> Optional[Dict]:
        """Update job"""
        updates['updated_at'] = datetime.now().isoformat()
        return self.store.update('jobs', job_id, updates)
    
    def delete(self, job_id: int) -> bool:
        """Delete job"""
        return self.store.delete('jobs', job_id)


class ApplicationModel:
    """Job application data model"""
    
    def __init__(self, config):
        self.store = DataStore(config.APPLICATIONS_DATA_FILE)
    
    def create(self, user_id: int, job_id: int) -> Dict:
        """Create a new application"""
        application = {
            'user_id': user_id,
            'job_id': job_id,
            'status': 'pending',  # pending, accepted, rejected
            'resume_used': None,
            'applied_at': datetime.now().isoformat(),
            'reviewed_at': None
        }
        return self.store.add('applications', application)
    
    def get_by_job(self, job_id: int) -> List[Dict]:
        """Get applications for a job"""
        applications = self.store.get_all('applications')
        return [a for a in applications if a.get('job_id') == job_id]
    
    def get_by_user(self, user_id: int) -> List[Dict]:
        """Get applications from a user"""
        applications = self.store.get_all('applications')
        return [a for a in applications if a.get('user_id') == user_id]
    
    def get_by_id(self, app_id: int) -> Optional[Dict]:
        """Get application by ID"""
        return self.store.get_by_id('applications', app_id)
    
    def already_applied(self, user_id: int, job_id: int) -> bool:
        """Check if user already applied for this job"""
        applications = self.store.get_all('applications')
        for app in applications:
            if app.get('user_id') == user_id and app.get('job_id') == job_id:
                return True
        return False
    
    def update(self, app_id: int, updates: Dict) -> Optional[Dict]:
        """Update application"""
        updates['reviewed_at'] = datetime.now().isoformat()
        return self.store.update('applications', app_id, updates)
