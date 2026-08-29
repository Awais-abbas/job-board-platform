"""
Authentication routes with MongoDB support
"""

from flask import Blueprint, request, jsonify, session
from app.services import UserService, ProfileService
from app.models.data_models import UserModel, ProfileModel
from app.utils.auth_utils import (
    hash_password, verify_password, validate_registration_data
)
from config import get_config
from database import get_db

auth_mongodb_bp = Blueprint('auth_mongodb', __name__)
config = get_config()

# Check if MongoDB is available
def use_mongodb():
    return config.USE_MONGODB and get_db() is not None

# Fallback models for JSON storage
user_model = UserModel(config)
profile_model = ProfileModel(config)

@auth_mongodb_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        email = data.get('email', '').strip()
        password = data.get('password', '')
        name = data.get('name', '').strip()
        role = data.get('role', '').lower()
        
        # Validate input
        is_valid, msg = validate_registration_data(email, password, name, role)
        if not is_valid:
            return jsonify({'error': msg}), 400
        
        if use_mongodb():
            # Use MongoDB
            # Check if user already exists
            if UserService.get_user_by_email(email):
                return jsonify({'error': 'Email already registered'}), 409
            
            # Create user
            password_hash = hash_password(password)
            user_data = {
                'email': email,
                'password': password_hash,
                'role': role,
                'name': name
            }
            user = UserService.create_user(user_data)
            
            if not user:
                return jsonify({'error': 'Failed to create user'}), 500
            
            # Create profile
            profile_data = {'role': role}
            ProfileService.create_profile(user['id'], profile_data)
            
            # Store in session
            session['user_id'] = user['id']
            session['email'] = user['email']
            session['role'] = user['role']
            
            return jsonify({
                'message': 'User registered successfully',
                'user': user
            }), 201
        else:
            # Use JSON storage (fallback)
            if user_model.exists(email):
                return jsonify({'error': 'Email already registered'}), 409
            
            password_hash = hash_password(password)
            user = user_model.create(
                email=email,
                password_hash=password_hash,
                role=role,
                name=name
            )
            
            profile = profile_model.create(user.get('id'), role)
            
            session['user_id'] = user.get('id')
            session['email'] = user.get('email')
            session['role'] = user.get('role')
            
            return jsonify({
                'message': 'User registered successfully',
                'user': {
                    'id': user.get('id'),
                    'email': user.get('email'),
                    'name': user.get('name'),
                    'role': user.get('role')
                }
            }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_mongodb_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400
        
        if use_mongodb():
            # Use MongoDB
            user = UserService.get_user_by_email(email)
            if not user:
                return jsonify({'error': 'Invalid email or password'}), 401
            
            # Get the actual user document for password verification
            from database import get_users_collection
            collection = get_users_collection()
            user_doc = collection.find_one({'email': email.lower()})
            
            if not verify_password(password, user_doc.get('password', '')):
                return jsonify({'error': 'Invalid email or password'}), 401
            
            # Store in session
            session['user_id'] = user['id']
            session['email'] = user['email']
            session['role'] = user['role']
            
            return jsonify({
                'message': 'Login successful',
                'user': user
            }), 200
        else:
            # Use JSON storage (fallback)
            user = user_model.get_by_email(email)
            if not user:
                return jsonify({'error': 'Invalid email or password'}), 401
            
            if not verify_password(password, user.get('password_hash', '')):
                return jsonify({'error': 'Invalid email or password'}), 401
            
            session['user_id'] = user.get('id')
            session['email'] = user.get('email')
            session['role'] = user.get('role')
            
            return jsonify({
                'message': 'Login successful',
                'user': {
                    'id': user.get('id'),
                    'email': user.get('email'),
                    'name': user.get('name'),
                    'role': user.get('role')
                }
            }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_mongodb_bp.route('/logout', methods=['POST'])
def logout():
    """Logout user"""
    session.clear()
    return jsonify({'message': 'Logout successful'}), 200

@auth_mongodb_bp.route('/me', methods=['GET'])
def get_current_user():
    """Get current logged-in user"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session.get('user_id')
    
    if use_mongodb():
        user = UserService.get_user_by_id(user_id)
    else:
        user = user_model.get_by_id(user_id)
    
    if not user:
        session.clear()
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({'user': user}), 200

@auth_mongodb_bp.route('/check', methods=['GET'])
def check_auth():
    """Check if user is authenticated"""
    is_authenticated = 'user_id' in session
    return jsonify({
        'authenticated': is_authenticated,
        'user_id': session.get('user_id') if is_authenticated else None,
        'role': session.get('role') if is_authenticated else None
    }), 200
