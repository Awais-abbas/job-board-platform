"""
Jobs management routes
"""

from flask import Blueprint, request, jsonify, session, current_app
from app.models.data_models import JobModel, UserModel, ApplicationModel
from app.services.db_services import JobService, UserService
from config import get_config

jobs_bp = Blueprint('jobs', __name__)
config = get_config()

# Legacy JSON models (fallback)
job_model = JobModel(config)
user_model = UserModel(config)
application_model = ApplicationModel(config)

def is_authenticated():
    """Check if user is authenticated"""
    return 'user_id' in session

def is_recruiter():
    """Check if user is a recruiter"""
    return session.get('role') == 'recruiter'

def use_mongodb():
    """Check if MongoDB should be used"""
    try:
        return current_app.config.get('USE_MONGODB', False)
    except:
        return False

@jobs_bp.route('', methods=['GET'])
def get_all_jobs():
    """Get all active job listings"""
    try:
        # Get filters
        search = request.args.get('search', '').strip().lower()
        skill_filter = request.args.get('skill', '').strip().lower()
        experience = request.args.get('experience', '').strip()
        
        jobs = []
        use_mongo = use_mongodb()
        
        print(f"[DEBUG] use_mongodb={use_mongo}")
        
        if use_mongo:
            try:
                # FIXED: Changed 'filter' to 'filters'
                jobs_result = JobService.get_all_jobs(filters={'status': 'active'})
                jobs = jobs_result if jobs_result else []
                print(f"[DEBUG] Found {len(jobs)} jobs from JobService")
            except Exception as service_error:
                print(f"[ERROR] JobService.get_all_jobs() failed: {service_error}")
                import traceback
                traceback.print_exc()
                jobs = []
        else:
            print("[DEBUG] MongoDB not enabled, using JSON fallback")
            try:
                jobs = [j for j in job_model.get_all() if j.get('status') == 'active']
            except Exception as json_error:
                print(f"[ERROR] JSON fallback failed: {json_error}")
                jobs = []
        
        # Apply filters
        if search:
            jobs = [j for j in jobs if search in j.get('title', '').lower() or
                    search in j.get('description', '').lower()]
        
        if skill_filter:
            jobs = [j for j in jobs if any(skill_filter in skill.lower()
                    for skill in j.get('skills_required', []) or j.get('required_skills', []))]
        
        if experience:
            jobs = [j for j in jobs if j.get('experience_level', '').lower() == experience.lower()]
        
        return jsonify({
            'count': len(jobs),
            'jobs': jobs
        }), 200
        
    except Exception as e:
        print(f"[ERROR] get_all_jobs failed: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@jobs_bp.route('/<job_id>', methods=['GET'])
def get_job(job_id):
    """Get specific job details"""
    try:
        job = None
        recruiter = None
        
        # Use MongoDB if available
        if use_mongodb():
            job = JobService.get_job_by_id(job_id)
            if job:
                recruiter_id = job.get('posted_by')
                if recruiter_id:
                    recruiter = UserService.get_user_by_id(recruiter_id)
        else:
            # Use JSON fallback
            # Try to convert string ID to int for JSON
            try:
                job_id_int = int(job_id)
            except:
                job_id_int = job_id
            
            job = job_model.get_by_id(job_id_int)
            if job:
                recruiter = user_model.get_by_id(job.get('recruiter_id'))
        
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        return jsonify({
            'job': job,
            'recruiter': {
                'id': recruiter.get('id'),
                'name': recruiter.get('name'),
                'email': recruiter.get('email')
            } if recruiter else None
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@jobs_bp.route('', methods=['POST'])
def create_job():
    """Create a new job listing (Recruiter only)"""
    try:
        if not is_authenticated():
            return jsonify({'error': 'Not authenticated'}), 401
        
        if not is_recruiter():
            return jsonify({'error': 'Only recruiters can post jobs'}), 403
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['title', 'description', 'skills_required', 'experience_level']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Use MongoDB if available
        if use_mongodb():
            job = JobService.create_job(data, session.get('user_id'))
        else:
            # Use JSON fallback
            job = job_model.create(
                recruiter_id=session.get('user_id'),
                title=data.get('title'),
                description=data.get('description'),
                required_skills=data.get('skills_required', data.get('required_skills', [])),
                experience_level=data.get('experience_level'),
                salary_min=data.get('salary_min'),
                salary_max=data.get('salary_max')
            )
        
        return jsonify({
            'message': 'Job posted successfully',
            'job': job
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@jobs_bp.route('/<job_id>', methods=['PUT'])
def update_job(job_id):
    """Update a job listing (Recruiter only)"""
    try:
        if not is_authenticated():
            return jsonify({'error': 'Not authenticated'}), 401
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Use MongoDB if available
        if use_mongodb():
            job = JobService.get_job_by_id(job_id)
            if not job:
                return jsonify({'error': 'Job not found'}), 404
            
            # Check authorization (posted_by should match user_id)
            if job.get('posted_by') != session.get('user_id'):
                return jsonify({'error': 'Unauthorized'}), 403
            
            # Prepare updates
            updates = {}
            for field in ['title', 'description', 'skills_required', 'experience_level', 'salary_min', 'salary_max', 'status']:
                if field in data:
                    updates[field] = data[field]
            
            updated_job = JobService.update_job(job_id, updates, session.get('user_id'))
        else:
            # Use JSON fallback
            try:
                job_id_int = int(job_id)
            except:
                job_id_int = job_id
                
            job = job_model.get_by_id(job_id_int)
            if not job:
                return jsonify({'error': 'Job not found'}), 404
            
            if job.get('recruiter_id') != session.get('user_id'):
                return jsonify({'error': 'Unauthorized'}), 403
            
            updates = {}
            for field in ['title', 'description', 'required_skills', 'experience_level', 'salary_min', 'salary_max', 'status']:
                if field in data:
                    updates[field] = data[field]
            
            updated_job = job_model.update(job_id_int, updates)
        
        return jsonify({
            'message': 'Job updated successfully',
            'job': updated_job
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@jobs_bp.route('/<job_id>', methods=['DELETE'])
def delete_job(job_id):
    """Delete a job listing (Recruiter only)"""
    try:
        if not is_authenticated():
            return jsonify({'error': 'Not authenticated'}), 401
        
        # Use MongoDB if available
        if use_mongodb():
            job = JobService.get_job_by_id(job_id)
            if not job:
                return jsonify({'error': 'Job not found'}), 404
            
            if job.get('posted_by') != session.get('user_id'):
                return jsonify({'error': 'Unauthorized'}), 403
            
            success = JobService.delete_job(job_id, session.get('user_id'))
        else:
            # Use JSON fallback
            try:
                job_id_int = int(job_id)
            except:
                job_id_int = job_id
                
            job = job_model.get_by_id(job_id_int)
            if not job:
                return jsonify({'error': 'Job not found'}), 404
            
            if job.get('recruiter_id') != session.get('user_id'):
                return jsonify({'error': 'Unauthorized'}), 403
            
            success = job_model.delete(job_id_int)
        
        if success:
            return jsonify({'message': 'Job deleted successfully'}), 200
        else:
            return jsonify({'error': 'Failed to delete job'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@jobs_bp.route('/posted', methods=['GET'])
def get_recruiter_jobs():
    """Get jobs posted by the current recruiter"""
    try:
        if not is_authenticated():
            return jsonify({'error': 'Not authenticated'}), 401
        
        if not is_recruiter():
            return jsonify({'error': 'Only recruiters can access this'}), 403
        
        recruiter_id = session.get('user_id')
        
        # Use MongoDB if available
        if use_mongodb():
            jobs = JobService.get_jobs_by_recruiter(recruiter_id)
        else:
            jobs = job_model.get_by_recruiter(recruiter_id)
        
        return jsonify({
            'count': len(jobs) if jobs else 0,
            'jobs': jobs if jobs else []
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
