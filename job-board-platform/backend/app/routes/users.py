"""
User profile routes
"""

from flask import Blueprint, request, jsonify, session, current_app, send_file
from app.models.data_models import UserModel, ProfileModel
from app.services.db_services import UserService, ProfileService
from config import get_config
import os
from werkzeug.utils import secure_filename
from app.utils.cv_utils import parse_cv
from bson import ObjectId

users_bp = Blueprint('users', __name__)
config = get_config()

# Legacy JSON models (fallback)
user_model = UserModel(config)
profile_model = ProfileModel(config)

def is_authenticated():
    """Check if user is authenticated"""
    return 'user_id' in session

def use_mongodb():
    """Check if MongoDB should be used"""
    try:
        return current_app.config.get('USE_MONGODB', False)
    except:
        return False

# ============== CURRENT USER ENDPOINTS (uses session) ==============

@users_bp.route('/me', methods=['GET'])
def get_current_user_profile():
    """Get current user's own profile using session"""
    try:
        if not is_authenticated():
            return jsonify({'error': 'Not authenticated'}), 401
        
        user_id = session.get('user_id')
        
        if use_mongodb():
            user = UserService.get_user_by_id(user_id)
            profile = ProfileService.get_profile_by_user_id(user_id)
        else:
            try:
                user_id_int = int(user_id)
            except:
                user_id_int = user_id
            user = user_model.get_by_id(user_id_int)
            profile = profile_model.get_by_user_id(user_id_int)
        
        if not user:
            session.clear()
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': user,
            'profile': profile
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/me', methods=['PUT'])
def update_current_user_profile():
    """Update current user's own profile using session"""
    try:
        if not is_authenticated():
            return jsonify({'error': 'Not authenticated'}), 401
        
        user_id = session.get('user_id')
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        if use_mongodb():
            # Prepare user updates
            user_updates = {}
            if 'name' in data:
                user_updates['name'] = data['name']
            
            if user_updates:
                UserService.update_user(user_id, user_updates)
            
            # Prepare profile updates
            profile_updates = {}
            profile_fields = ['bio', 'location', 'website', 'company', 'position', 'skills', 'experience_years', 'phone', 'education']
            for field in profile_fields:
                if field in data:
                    profile_updates[field] = data[field]
            
            if profile_updates:
                ProfileService.update_profile(user_id, profile_updates)
            
            user = UserService.get_user_by_id(user_id)
            profile = ProfileService.get_profile_by_user_id(user_id)
        else:
            # JSON fallback
            try:
                user_id_int = int(user_id)
            except:
                user_id_int = user_id
            
            # Update user info
            user_updates = {}
            if 'name' in data:
                user_updates['name'] = data['name']
            
            if user_updates:
                user_model.update(user_id_int, user_updates)
            
            # Update profile
            profile_updates = {}
            profile_fields = ['bio', 'location', 'website', 'company', 'position', 'skills', 'experience_years', 'phone', 'education']
            for field in profile_fields:
                if field in data:
                    profile_updates[field] = data[field]
            
            if profile_updates:
                profile_model.update_by_user_id(user_id_int, profile_updates)
            
            user = user_model.get_by_id(user_id_int)
            profile = profile_model.get_by_user_id(user_id_int)
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user,
            'profile': profile
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/me/upload-cv', methods=['POST'])
def upload_my_cv():
    """Upload CV for current user using session"""
    try:
        if not is_authenticated():
            return jsonify({'error': 'Not authenticated'}), 401
        
        user_id = session.get('user_id')
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file
        filename = secure_filename(file.filename)
        file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        
        if file_ext not in config.ALLOWED_EXTENSIONS:
            return jsonify({'error': f'Allowed formats: {", ".join(config.ALLOWED_EXTENSIONS)}'}), 400
        
        # Save file
        cv_filename = f"cv_{user_id}_{filename}"
        cv_path = os.path.join(config.UPLOAD_DIR, cv_filename)
        file.save(cv_path)
        
        # Parse CV
        cv_data = parse_cv(cv_path, file_ext)
        
        # Update profile
        profile_updates = {
            'cv_path': cv_filename,
            'skills': cv_data.get('skills', []),
            'experience_years': cv_data.get('experience_years', 0)
        }
        
        if use_mongodb():
            ProfileService.update_profile(user_id, profile_updates)
            profile = ProfileService.get_profile_by_user_id(user_id)
        else:
            try:
                user_id_int = int(user_id)
            except:
                user_id_int = user_id
            
            profile_model.update_by_user_id(user_id_int, profile_updates)
            profile = profile_model.get_by_user_id(user_id_int)
        
        return jsonify({
            'message': 'CV uploaded successfully',
            'profile': profile,
            'cv_data': cv_data
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/me/download-cv', methods=['GET'])
def download_my_cv():
    """Download current user's CV"""
    try:
        if not is_authenticated():
            return jsonify({'error': 'Not authenticated'}), 401
        
        user_id = session.get('user_id')
        
        # Get profile to find cv_path
        if use_mongodb():
            profile = ProfileService.get_profile_by_user_id(user_id)
        else:
            try:
                user_id_int = int(user_id)
            except:
                user_id_int = user_id
            profile = profile_model.get_by_user_id(user_id_int)
        
        if not profile or not profile.get('cv_path'):
            return jsonify({'error': 'No CV found'}), 404
        
        cv_filename = profile.get('cv_path')
        cv_path = os.path.join(config.UPLOAD_DIR, cv_filename)
        
        if not os.path.exists(cv_path):
            return jsonify({'error': 'CV file not found'}), 404
        
        # Get file extension for correct mime type
        file_ext = cv_filename.rsplit('.', 1)[1].lower() if '.' in cv_filename else ''
        mime_types = {
            'pdf': 'application/pdf',
            'doc': 'application/msword',
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        }
        mime_type = mime_types.get(file_ext, 'application/octet-stream')
        
        return send_file(
            cv_path,
            mimetype=mime_type,
            as_attachment=False,
            download_name=cv_filename
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/me/delete-cv', methods=['DELETE'])
def delete_my_cv():
    """Delete current user's CV"""
    try:
        if not is_authenticated():
            return jsonify({'error': 'Not authenticated'}), 401
        
        user_id = session.get('user_id')
        
        # Get profile to find cv_path
        if use_mongodb():
            profile = ProfileService.get_profile_by_user_id(user_id)
        else:
            try:
                user_id_int = int(user_id)
            except:
                user_id_int = user_id
            profile = profile_model.get_by_user_id(user_id_int)
        
        if not profile or not profile.get('cv_path'):
            return jsonify({'error': 'No CV found'}), 404
        
        cv_filename = profile.get('cv_path')
        cv_path = os.path.join(config.UPLOAD_DIR, cv_filename)
        
        # Delete file if it exists
        if os.path.exists(cv_path):
            os.remove(cv_path)
        
        # Update profile to remove cv_path
        profile_updates = {
            'cv_path': None
        }
        
        if use_mongodb():
            ProfileService.update_profile(user_id, profile_updates)
            profile = ProfileService.get_profile_by_user_id(user_id)
        else:
            try:
                user_id_int = int(user_id)
            except:
                user_id_int = user_id
            profile_model.update_by_user_id(user_id_int, profile_updates)
            profile = profile_model.get_by_user_id(user_id_int)
        
        return jsonify({
            'message': 'CV deleted successfully',
            'profile': profile
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============== USER ENDPOINTS (by ID) ==============

@users_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get user profile by ID"""
    try:
        user = None
        profile = None
        
        if use_mongodb():
            # MongoDB uses string IDs (ObjectId strings)
            user = UserService.get_user_by_id(user_id)
            if user:
                profile = ProfileService.get_profile_by_user_id(user_id)
        else:
            # JSON uses integer IDs
            try:
                user_id_int = int(user_id)
            except:
                user_id_int = user_id
            
            user = user_model.get_by_id(user_id_int)
            if user:
                profile = profile_model.get_by_user_id(user_id_int)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': {
                'id': user.get('id'),
                'email': user.get('email'),
                'name': user.get('name'),
                'role': user.get('role'),
                'created_at': user.get('created_at')
            },
            'profile': profile
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user profile by ID"""
    try:
        if not is_authenticated():
            return jsonify({'error': 'Not authenticated'}), 401
        
        # For string user_ids (MongoDB), direct comparison
        # For int user_ids (JSON), convert session user_id too
        auth_user_id = session.get('user_id')
        if str(auth_user_id) != str(user_id):
            return jsonify({'error': 'Unauthorized'}), 403
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        if use_mongodb():
            # Prepare user updates
            user_updates = {}
            if 'name' in data:
                user_updates['name'] = data['name']
            
            if user_updates:
                UserService.update_user(user_id, user_updates)
            
            # Prepare profile updates
            profile_updates = {}
            profile_fields = ['bio', 'location', 'website', 'company', 'position', 'skills', 'experience_years', 'phone', 'education']
            for field in profile_fields:
                if field in data:
                    profile_updates[field] = data[field]
            
            if profile_updates:
                ProfileService.update_profile(user_id, profile_updates)
            
            user = UserService.get_user_by_id(user_id)
            profile = ProfileService.get_profile_by_user_id(user_id)
        else:
            # JSON fallback
            try:
                user_id_int = int(user_id)
            except:
                user_id_int = user_id
            
            # Update user info
            user_updates = {}
            if 'name' in data:
                user_updates['name'] = data['name']
            
            if user_updates:
                user_model.update(user_id_int, user_updates)
            
            # Update profile
            profile_updates = {}
            profile_fields = ['bio', 'location', 'website', 'company', 'position', 'skills', 'experience_years', 'phone', 'education']
            for field in profile_fields:
                if field in data:
                    profile_updates[field] = data[field]
            
            if profile_updates:
                profile_model.update_by_user_id(user_id_int, profile_updates)
            
            user = user_model.get_by_id(user_id_int)
            profile = profile_model.get_by_user_id(user_id_int)
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': {
                'id': user.get('id'),
                'email': user.get('email'),
                'name': user.get('name'),
                'role': user.get('role')
            },
            'profile': profile
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users_bp.route('/<user_id>/upload-cv', methods=['POST'])
def upload_cv(user_id):
    """Upload and parse CV for specific user"""
    try:
        if not is_authenticated():
            return jsonify({'error': 'Not authenticated'}), 401
        
        if str(session.get('user_id')) != str(user_id):
            return jsonify({'error': 'Unauthorized'}), 403
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file
        filename = secure_filename(file.filename)
        file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        
        if file_ext not in config.ALLOWED_EXTENSIONS:
            return jsonify({'error': f'Allowed formats: {", ".join(config.ALLOWED_EXTENSIONS)}'}), 400
        
        # Save file
        cv_filename = f"cv_{user_id}_{filename}"
        cv_path = os.path.join(config.UPLOAD_DIR, cv_filename)
        file.save(cv_path)
        
        # Parse CV
        cv_data = parse_cv(cv_path, file_ext)
        
        # Update profile
        profile_updates = {
            'cv_path': cv_filename,
            'skills': cv_data.get('skills', []),
            'experience_years': cv_data.get('experience_years', 0)
        }
        
        if use_mongodb():
            ProfileService.update_profile(user_id, profile_updates)
            profile = ProfileService.get_profile_by_user_id(user_id)
        else:
            try:
                user_id_int = int(user_id)
            except:
                user_id_int = user_id
            
            profile_model.update_by_user_id(user_id_int, profile_updates)
            profile = profile_model.get_by_user_id(user_id_int)
        
        return jsonify({
            'message': 'CV uploaded successfully',
            'profile': profile,
            'cv_data': cv_data
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============== SEARCH ENDPOINTS ==============

@users_bp.route('/search', methods=['GET'])
def search_users():
    """Search users by role or skills"""
    try:
        query = request.args.get('query', '').strip()
        role = request.args.get('role', '').strip()
        
        if use_mongodb():
            # Use MongoDB search
            from database import get_profiles_collection, get_users_collection
            profiles_collection = get_profiles_collection()
            users_collection = get_users_collection()
            
            if profiles_collection is None:
                return jsonify({'count': 0, 'profiles': []}), 200
            
            # Build query
            search_query = {}
            if role:
                # Need to join with users collection to filter by role
                users = list(users_collection.find({'role': role}) if users_collection else [])
                user_ids = [str(u['_id']) for u in users]
                if user_ids:
                    from bson import ObjectId
                    search_query['user_id'] = {'$in': [ObjectId(uid) for uid in user_ids]}
                else:
                    return jsonify({'count': 0, 'profiles': []}), 200
            
            profiles = list(profiles_collection.find(search_query))
            
            # Filter by skills if query provided
            if query:
                profiles = [p for p in profiles if any(query.lower() in skill.lower() for skill in p.get('skills', []))]
            
            # Convert ObjectIds to strings
            for profile in profiles:
                profile['_id'] = str(profile['_id'])
                if 'user_id' in profile:
                    profile['user_id'] = str(profile['user_id'])
            
            return jsonify({
                'count': len(profiles),
                'profiles': profiles
            }), 200
        else:
            # Use JSON storage
            from app.models.data_models import DataStore
            profile_store = DataStore(config.PROFILES_DATA_FILE)
            profiles = profile_store.get_all('profiles')
            
            results = []
            for profile in profiles:
                if role and profile.get('role') != role:
                    continue
                
                if query:
                    # Search in skills
                    skills = profile.get('skills', [])
                    query_lower = query.lower()
                    if not any(query_lower in skill.lower() for skill in skills):
                        continue
                
                results.append(profile)
            
            return jsonify({
                'count': len(results),
                'profiles': results
            }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============== DEBUG ENDPOINT ==============

@users_bp.route('/debug/session', methods=['GET'])
def debug_session():
    """Debug endpoint to check session (for development only)"""
    if current_app.config.get('DEBUG', False):
        return jsonify({
            'session_exists': 'user_id' in session,
            'user_id': session.get('user_id'),
            'user_role': session.get('role'),
            'session_keys': list(session.keys())
        }), 200
    return jsonify({'error': 'Not available in production'}), 403

@users_bp.route('/debug/profile', methods=['GET'])
def debug_profile():
    """Debug endpoint to check profile data directly"""
    if not is_authenticated():
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session.get('user_id')
    
    from database import get_profiles_collection
    collection = get_profiles_collection()
    
    if collection is None:
        return jsonify({'error': 'Collection not found'}), 500
    
    profile = collection.find_one({'user_id': ObjectId(user_id)})
    
    if profile:
        profile['_id'] = str(profile['_id'])
        profile['user_id'] = str(profile['user_id'])
    
    return jsonify({
        'profile': profile,
        'cv_path': profile.get('cv_path') if profile else None
    }), 200

@users_bp.route('/me/generate-cv', methods=['POST'])
def generate_cv():
    """Generate PDF CV from CV Builder data"""
    try:
        if not is_authenticated():
            return jsonify({'error': 'Not authenticated'}), 401
        
        user_id = session.get('user_id')
        data = request.get_json()
        cv_data = data.get('cvData', {})
        
        # Get user info
        if use_mongodb():
            user = UserService.get_user_by_id(user_id)
        else:
            try:
                user_id_int = int(user_id)
            except:
                user_id_int = user_id
            user = user_model.get_by_id(user_id_int)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Generate PDF filename
        pdf_filename = f"cv_{user_id}_generated.pdf"
        pdf_path = os.path.join(config.UPLOAD_DIR, pdf_filename)
        
        # Generate PDF using our new function
        from app.utils.pdf_generator import generate_cv_pdf
        generate_cv_pdf(cv_data, user, pdf_path)
        
        # Calculate total experience
        total_years = 0
        for exp in cv_data.get('experience', []):
            if exp.get('startDate') and exp.get('endDate'):
                try:
                    from datetime import datetime
                    start = datetime.strptime(exp['startDate'], '%b %Y')
                    end = datetime.strptime(exp['endDate'], '%b %Y') if exp['endDate'] != 'Present' else datetime.now()
                    years = (end - start).days / 365.25
                    total_years += years
                except:
                    pass
        
        # Format education
        education_text = ""
        for edu in cv_data.get('education', []):
            if edu.get('degree'):
                edu_line = edu.get('degree', '')
                if edu.get('institution'):
                    edu_line += f" - {edu.get('institution')}"
                if edu.get('year'):
                    edu_line += f" ({edu.get('year')})"
                if education_text:
                    education_text += "; "
                education_text += edu_line
        
        # Update profile with CV data
        profile_updates = {
            'cv_path': pdf_filename,
            'skills': cv_data.get('skills', []),
            'experience_years': round(total_years, 1),
            'position': cv_data.get('experience', [{}])[0].get('position', ''),
            'bio': cv_data.get('summary', ''),
            'location': cv_data.get('personalInfo', {}).get('location', ''),
            'phone': cv_data.get('personalInfo', {}).get('phone', ''),
            'website': cv_data.get('personalInfo', {}).get('portfolio', ''),
            'education': education_text
        }
        
        if use_mongodb():
            ProfileService.update_profile(user_id, profile_updates)
            profile = ProfileService.get_profile_by_user_id(user_id)
        else:
            try:
                user_id_int = int(user_id)
            except:
                user_id_int = user_id
            profile_model.update_by_user_id(user_id_int, profile_updates)
            profile = profile_model.get_by_user_id(user_id_int)
        
        return jsonify({
            'message': 'CV generated successfully',
            'profile': profile,
            'cv_path': pdf_filename
        }), 200
        
    except Exception as e:
        print(f"Error generating CV: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500