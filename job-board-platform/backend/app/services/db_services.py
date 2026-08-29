"""
Database Services for MongoDB CRUD Operations
"""

from bson import ObjectId
from database import get_users_collection, get_jobs_collection, get_applications_collection, get_profiles_collection
from app.models.mongodb_models import User, Job, Application, Profile
from datetime import datetime

# ============== USER SERVICES ==============
class UserService:
    """User database operations"""
    
    @staticmethod
    def create_user(user_data):
        """Create a new user"""
        collection = get_users_collection()
        if collection is None:
            return None
        
        # Check if email already exists
        if collection.find_one({'email': user_data.get('email', '').lower()}):
            return None
        
        user_doc = User.create(user_data)
        result = collection.insert_one(user_doc)
        
        if result.inserted_id:
            return User.to_json(user_doc)
        return None
    
    @staticmethod
    def get_user_by_email(email):
        """Get user by email"""
        collection = get_users_collection()
        if collection is None:
            return None
        
        user = collection.find_one({'email': email.lower()})
        return User.to_json(user) if user else None
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        collection = get_users_collection()
        if collection is None:
            return None
        
        try:
            user = collection.find_one({'_id': ObjectId(user_id)})
            return User.to_json(user) if user else None
        except:
            return None
    
    @staticmethod
    def update_user(user_id, update_data):
        """Update user data"""
        collection = get_users_collection()
        if collection is None:
            return None
        
        update_data['updated_at'] = datetime.utcnow()
        
        result = collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': update_data}
        )
        
        if result.modified_count > 0:
            return UserService.get_user_by_id(user_id)
        return None
    
    @staticmethod
    def delete_user(user_id):
        """Delete user"""
        collection = get_users_collection()
        if collection is None:
            return False
        
        result = collection.delete_one({'_id': ObjectId(user_id)})
        return result.deleted_count > 0


# ============== JOB SERVICES ==============
class JobService:
    """Job listing database operations"""
    
    @staticmethod
    def create_job(job_data, recruiter_id):
        """Create a new job listing"""
        collection = get_jobs_collection()
        if collection is None:
            return None
        
        job_doc = Job.create(job_data, recruiter_id)
        result = collection.insert_one(job_doc)
        
        if result.inserted_id:
            return Job.to_json(job_doc)
        return None
    
    @staticmethod
    def get_job_by_id(job_id):
        """Get job by ID"""
        collection = get_jobs_collection()
        if collection is None:
            return None
        
        try:
            job = collection.find_one({'_id': ObjectId(job_id)})
            return Job.to_json(job) if job else None
        except:
            return None
    
    @staticmethod
    def get_all_jobs(filters=None, limit=50, skip=0):
        """Get all jobs with optional filters"""
        collection = get_jobs_collection()
        if collection is None:
            return []
        
        query = {'status': 'active'}
        
        if filters:
            if filters.get('category'):
                query['category'] = filters['category']
            if filters.get('type'):
                query['type'] = filters['type']
            if filters.get('location'):
                query['location'] = {'$regex': filters['location'], '$options': 'i'}
            if filters.get('search'):
                query['$or'] = [
                    {'title': {'$regex': filters['search'], '$options': 'i'}},
                    {'company': {'$regex': filters['search'], '$options': 'i'}},
                    {'description': {'$regex': filters['search'], '$options': 'i'}}
                ]
        
        jobs = list(collection.find(query).sort('created_at', -1).limit(limit).skip(skip))
        return [Job.to_json(job) for job in jobs]
    
    @staticmethod
    def get_jobs_by_recruiter(recruiter_id):
        """Get all jobs posted by a recruiter"""
        collection = get_jobs_collection()
        if collection is None:
            return []
        
        jobs = list(collection.find({'posted_by': ObjectId(recruiter_id)}).sort('created_at', -1))
        return [Job.to_json(job) for job in jobs]
    
    @staticmethod
    def update_job(job_id, update_data, recruiter_id):
        """Update job listing"""
        collection = get_jobs_collection()
        if collection is None:
            return None
        
        update_data['updated_at'] = datetime.utcnow()
        
        result = collection.update_one(
            {'_id': ObjectId(job_id), 'posted_by': ObjectId(recruiter_id)},
            {'$set': update_data}
        )
        
        if result.modified_count > 0:
            return JobService.get_job_by_id(job_id)
        return None
    
    @staticmethod
    def delete_job(job_id, recruiter_id):
        """Delete job listing"""
        collection = get_jobs_collection()
        if collection is None:
            return False
        
        result = collection.delete_one({
            '_id': ObjectId(job_id),
            'posted_by': ObjectId(recruiter_id)
        })
        return result.deleted_count > 0
    
    @staticmethod
    def increment_applications_count(job_id):
        """Increment job applications counter"""
        collection = get_jobs_collection()
        if collection is None:
            return
        
        collection.update_one(
            {'_id': ObjectId(job_id)},
            {'$inc': {'applications_count': 1}}
        )


# ============== APPLICATION SERVICES ==============
class ApplicationService:
    """Job application database operations"""
    
    @staticmethod
    def create_application(job_id, user_id, application_data):
        """Create a new job application"""
        collection = get_applications_collection()
        if collection is None:
            return None
        
        # Check if user already applied
        existing = collection.find_one({
            'job_id': ObjectId(job_id),
            'user_id': ObjectId(user_id)
        })
        
        if existing:
            return None
        
        app_doc = Application.create(job_id, user_id, application_data)
        result = collection.insert_one(app_doc)
        
        if result.inserted_id:
            # Increment job applications count
            JobService.increment_applications_count(job_id)
            return Application.to_json(app_doc)
        return None
    
    @staticmethod
    def get_application_by_id(app_id):
        """Get application by ID"""
        collection = get_applications_collection()
        if collection is None:
            return None
        
        try:
            app = collection.find_one({'_id': ObjectId(app_id)})
            return Application.to_json(app) if app else None
        except:
            return None
    
    @staticmethod
    def get_user_applications(user_id):
        """Get all applications by a user"""
        collection = get_applications_collection()
        if collection is None:
            return []
        
        apps = list(collection.find({'user_id': ObjectId(user_id)}).sort('applied_at', -1))
        
        # Enrich with job data
        result = []
        for app in apps:
            job = JobService.get_job_by_id(str(app['job_id']))
            result.append(Application.to_json(app, job=job))
        
        return result
    
    @staticmethod
    def get_job_applications(job_id):
        """Get all applications for a job"""
        collection = get_applications_collection()
        if collection is None:
            return []
        
        apps = list(collection.find({'job_id': ObjectId(job_id)}).sort('applied_at', -1))
        return [Application.to_json(app) for app in apps]
    
    @staticmethod
    def update_application_status(app_id, status, feedback=None):
        """Update application status"""
        collection = get_applications_collection()
        if collection is None:
            return None
        
        update_data = {
            'status': status,
            'updated_at': datetime.utcnow()
        }
        
        if feedback:
            update_data['recruiter_feedback'] = feedback
        
        result = collection.update_one(
            {'_id': ObjectId(app_id)},
            {'$set': update_data}
        )
        
        if result.modified_count > 0:
            return ApplicationService.get_application_by_id(app_id)
        return None


# ============== PROFILE SERVICES ==============
# ============== PROFILE SERVICES ==============
class ProfileService:
    """User profile database operations"""
    
    @staticmethod
    def create_profile(user_id, profile_data):
        """Create a new user profile"""
        collection = get_profiles_collection()
        if collection is None:
            return None
        
        # Check if profile already exists
        if collection.find_one({'user_id': ObjectId(user_id)}):
            return None
        
        profile_doc = Profile.create(user_id, profile_data)
        result = collection.insert_one(profile_doc)
        
        if result.inserted_id:
            return Profile.to_json(profile_doc)
        return None
    
    @staticmethod
    def get_profile_by_user_id(user_id):
        """Get profile by user ID"""
        collection = get_profiles_collection()
        if collection is None:
            print("[DEBUG] get_profiles_collection returned None")
            return None
        
        try:
            profile = collection.find_one({'user_id': ObjectId(user_id)})
            if profile:
                print(f"[DEBUG] Found profile: {profile}")
                # Convert ObjectId to string
                profile['_id'] = str(profile['_id'])
                profile['user_id'] = str(profile['user_id'])
                # Log cv_path specifically
                print(f"[DEBUG] cv_path in profile: {profile.get('cv_path')}")
            else:
                print(f"[DEBUG] No profile found for user_id: {user_id}")
            return Profile.to_json(profile) if profile else None
        except Exception as e:
            print(f"[DEBUG] Error getting profile: {e}")
            return None
    
    @staticmethod
    def update_profile(user_id, update_data):
        """Update user profile"""
        collection = get_profiles_collection()
        if collection is None:
            print("[DEBUG] update_profile: collection is None")
            return None
        
        update_data['updated_at'] = datetime.utcnow()
        
        print(f"[DEBUG] Updating profile for user_id: {user_id}")
        print(f"[DEBUG] Update data: {update_data}")
        
        result = collection.update_one(
            {'user_id': ObjectId(user_id)},
            {'$set': update_data},
            upsert=True
        )
        
        print(f"[DEBUG] Update result: modified_count={result.modified_count}, upserted_id={result.upserted_id}")
        
        if result.modified_count > 0 or result.upserted_id:
            # Update user profile_completed status
            users_collection = get_users_collection()
            if users_collection is not None:
                users_collection.update_one(
                    {'_id': ObjectId(user_id)},
                    {'$set': {'profile_completed': True}}
                )
            return ProfileService.get_profile_by_user_id(user_id)
        return None
    @staticmethod
    def add_experience(user_id, experience_data):
        """Add experience to profile"""
        collection = get_profiles_collection()
        if collection is None:
            return None
        
        result = collection.update_one(
            {'user_id': ObjectId(user_id)},
            {
                '$push': {'experience': experience_data},
                '$set': {'updated_at': datetime.utcnow()}
            }
        )
        
        if result.modified_count > 0:
            return ProfileService.get_profile_by_user_id(user_id)
        return None
    
    @staticmethod
    def add_education(user_id, education_data):
        """Add education to profile"""
        collection = get_profiles_collection()
        if collection is None:
            return None
        
        result = collection.update_one(
            {'user_id': ObjectId(user_id)},
            {
                '$push': {'education': education_data},
                '$set': {'updated_at': datetime.utcnow()}
            }
        )
        
        if result.modified_count > 0:
            return ProfileService.get_profile_by_user_id(user_id)
        return None
    
    @staticmethod
    def update_resume(user_id, resume_data):
        """Update resume information"""
        collection = get_profiles_collection()
        if collection is None:
            return None
        
        result = collection.update_one(
            {'user_id': ObjectId(user_id)},
            {
                '$set': {
                    'resume_url': resume_data.get('resume_url'),
                    'resume_parsed_data': resume_data.get('parsed_data', {}),
                    'updated_at': datetime.utcnow()
                }
            }
        )
        
        if result.modified_count > 0:
            return ProfileService.get_profile_by_user_id(user_id)
        return None
    
    @staticmethod
    def search_profiles_by_skills(skills, limit=20):
        """Search profiles by skills"""
        collection = get_profiles_collection()
        if collection is None:
            return []
        
        # Find profiles with matching skills
        profiles = list(collection.find({
            'skills': {'$in': skills}
        }).limit(limit))
        
        return [Profile.to_json(profile) for profile in profiles]