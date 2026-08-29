"""
Job applications management routes - MongoDB Version
"""

from flask import Blueprint, request, jsonify, session, current_app
from app.services.db_services import ApplicationService, JobService, UserService, ProfileService
from config import get_config
from bson import ObjectId

applications_bp = Blueprint('applications', __name__)
config = get_config()

def is_authenticated():
    """Check if user is authenticated"""
    return 'user_id' in session

def use_mongodb():
    """Check if MongoDB should be used"""
    try:
        return current_app.config.get('USE_MONGODB', False)
    except:
        return False

@applications_bp.route('', methods=['POST'])
def apply_for_job():
    """Submit job application (Job seeker only)"""
    try:
        if not is_authenticated():
            return jsonify({'error': 'Not authenticated'}), 401
        
        if session.get('role') != 'job_seeker':
            return jsonify({'error': 'Only job seekers can apply for jobs'}), 403
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        job_id = data.get('job_id')
        if not job_id:
            return jsonify({'error': 'Job ID required'}), 400
        
        user_id = session.get('user_id')
        
        if use_mongodb():
            # Use MongoDB
            # Check if job exists
            job = JobService.get_job_by_id(job_id)
            if not job:
                return jsonify({'error': 'Job not found'}), 404
            
            # Check if already applied
            existing_apps = ApplicationService.get_user_applications(user_id)
            for app in existing_apps:
                if str(app.get('job_id')) == job_id:
                    return jsonify({'error': 'You have already applied for this job'}), 409
            
            # Create application
            application_data = {
                'cover_letter': data.get('cover_letter', ''),
                'match_percentage': data.get('match_percentage', 0)
            }
            
            application = ApplicationService.create_application(job_id, user_id, application_data)
            
            if not application:
                return jsonify({'error': 'Failed to submit application'}), 500
            
            return jsonify({
                'message': 'Application submitted successfully',
                'application': application
            }), 201
        else:
            # Use JSON storage (fallback)
            from app.models.data_models import ApplicationModel, JobModel
            application_model = ApplicationModel(config)
            job_model = JobModel(config)
            
            # Check if job exists in JSON
            try:
                job_id_int = int(job_id)
            except:
                job_id_int = job_id
            
            job = job_model.get_by_id(job_id_int)
            if not job:
                return jsonify({'error': 'Job not found'}), 404
            
            # Check if already applied
            if application_model.already_applied(user_id, job_id_int):
                return jsonify({'error': 'You have already applied for this job'}), 409
            
            # Create application
            application = application_model.create(user_id, job_id_int)
            
            return jsonify({
                'message': 'Application submitted successfully',
                'application': application
            }), 201
    
    except Exception as e:
        print(f"Error in apply_for_job: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@applications_bp.route('/user', methods=['GET'])
def get_user_applications():
    """Get all applications from current user"""
    try:
        if not is_authenticated():
            return jsonify({'error': 'Not authenticated'}), 401
        
        if session.get('role') != 'job_seeker':
            return jsonify({'error': 'Only job seekers can access this'}), 403
        
        user_id = session.get('user_id')
        
        if use_mongodb():
            applications = ApplicationService.get_user_applications(user_id)
        else:
            from app.models.data_models import ApplicationModel, JobModel
            application_model = ApplicationModel(config)
            job_model = JobModel(config)
            
            applications = application_model.get_by_user(user_id)
            
            # Add job details
            for app in applications:
                job = job_model.get_by_id(app.get('job_id'))
                app['job'] = job
        
        return jsonify({
            'count': len(applications),
            'applications': applications
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@applications_bp.route('/job/<job_id>', methods=['GET'])
def get_job_applications(job_id):
    """Get all applications for a specific job (Recruiter only)"""
    try:
        if not is_authenticated():
            return jsonify({'error': 'Not authenticated'}), 401
        
        if session.get('role') != 'recruiter':
            return jsonify({'error': 'Only recruiters can access this'}), 403
        
        if use_mongodb():
            # Check if job exists and belongs to recruiter
            job = JobService.get_job_by_id(job_id)
            if not job:
                return jsonify({'error': 'Job not found'}), 404
            
            if str(job.get('posted_by')) != session.get('user_id'):
                return jsonify({'error': 'Unauthorized'}), 403
            
            applications = ApplicationService.get_job_applications(job_id)
            
            # Enrich with user details
            for app in applications:
                user = UserService.get_user_by_id(app.get('user_id'))
                profile = ProfileService.get_profile_by_user_id(app.get('user_id'))
                app['user'] = user
                app['profile'] = profile
        else:
            from app.models.data_models import ApplicationModel, JobModel, UserModel, ProfileModel
            application_model = ApplicationModel(config)
            job_model = JobModel(config)
            user_model = UserModel(config)
            profile_model = ProfileModel(config)
            
            try:
                job_id_int = int(job_id)
            except:
                job_id_int = job_id
            
            job = job_model.get_by_id(job_id_int)
            if not job:
                return jsonify({'error': 'Job not found'}), 404
            
            if job.get('recruiter_id') != session.get('user_id'):
                return jsonify({'error': 'Unauthorized'}), 403
            
            applications = application_model.get_by_job(job_id_int)
            
            # Add applicant details
            for app in applications:
                user = user_model.get_by_id(app.get('user_id'))
                profile = profile_model.get_by_user_id(app.get('user_id'))
                app['user'] = user
                app['profile'] = profile
        
        return jsonify({
            'count': len(applications),
            'applications': applications
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@applications_bp.route('/<app_id>/status', methods=['PUT'])
def update_application_status(app_id):
    """Update application status (Recruiter only)"""
    try:
        if not is_authenticated():
            return jsonify({'error': 'Not authenticated'}), 401
        
        data = request.get_json()
        status = data.get('status')
        
        if status not in ['pending', 'reviewed', 'shortlisted', 'rejected', 'hired']:
            return jsonify({'error': 'Invalid status'}), 400
        
        if use_mongodb():
            application = ApplicationService.get_application_by_id(app_id)
            if not application:
                return jsonify({'error': 'Application not found'}), 404
            
            # Check authorization
            job = JobService.get_job_by_id(application.get('job_id'))
            if not job or str(job.get('posted_by')) != session.get('user_id'):
                return jsonify({'error': 'Unauthorized'}), 403
            
            updated_app = ApplicationService.update_application_status(app_id, status)
        else:
            from app.models.data_models import ApplicationModel, JobModel
            application_model = ApplicationModel(config)
            job_model = JobModel(config)
            
            try:
                app_id_int = int(app_id)
            except:
                app_id_int = app_id
            
            app = application_model.get_by_id(app_id_int)
            if not app:
                return jsonify({'error': 'Application not found'}), 404
            
            job = job_model.get_by_id(app.get('job_id'))
            if job.get('recruiter_id') != session.get('user_id'):
                return jsonify({'error': 'Unauthorized'}), 403
            
            updated_app = application_model.update(app_id_int, {'status': status})
        
        return jsonify({
            'message': 'Application status updated',
            'application': updated_app
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@applications_bp.route('/<app_id>', methods=['GET'])
def get_application(app_id):
    """Get specific application details"""
    try:
        if not is_authenticated():
            return jsonify({'error': 'Not authenticated'}), 401
        
        if use_mongodb():
            application = ApplicationService.get_application_by_id(app_id)
            if not application:
                return jsonify({'error': 'Application not found'}), 404
            
            # Check permissions
            if session.get('user_id') != application.get('user_id'):
                job = JobService.get_job_by_id(application.get('job_id'))
                if not job or str(job.get('posted_by')) != session.get('user_id'):
                    return jsonify({'error': 'Unauthorized'}), 403
            
            user = UserService.get_user_by_id(application.get('user_id'))
            job = JobService.get_job_by_id(application.get('job_id'))
            profile = ProfileService.get_profile_by_user_id(application.get('user_id'))
            
            application['user'] = user
            application['job'] = job
            application['profile'] = profile
        else:
            from app.models.data_models import ApplicationModel, JobModel, UserModel, ProfileModel
            application_model = ApplicationModel(config)
            job_model = JobModel(config)
            user_model = UserModel(config)
            profile_model = ProfileModel(config)
            
            try:
                app_id_int = int(app_id)
            except:
                app_id_int = app_id
            
            application = application_model.get_by_id(app_id_int)
            if not application:
                return jsonify({'error': 'Application not found'}), 404
            
            # Check permissions
            if session.get('user_id') != application.get('user_id'):
                job = job_model.get_by_id(application.get('job_id'))
                if job.get('recruiter_id') != session.get('user_id'):
                    return jsonify({'error': 'Unauthorized'}), 403
            
            user = user_model.get_by_id(application.get('user_id'))
            job = job_model.get_by_id(application.get('job_id'))
            profile = profile_model.get_by_user_id(application.get('user_id'))
            
            application['user'] = user
            application['job'] = job
            application['profile'] = profile
        
        return jsonify({
            'application': application
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500