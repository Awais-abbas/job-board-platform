"""
Authentication routes
"""

from flask import Blueprint, request, jsonify, session
from app.models.data_models import UserModel, ProfileModel
from app.utils.auth_utils import (
    hash_password, verify_password, validate_registration_data
)
from config import get_config

auth_bp = Blueprint('auth', __name__)
config = get_config()
user_model = UserModel(config)
profile_model = ProfileModel(config)

@auth_bp.route('/register', methods=['POST'])
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
        
        # Check if user already exists
        if user_model.exists(email):
            return jsonify({'error': 'Email already registered'}), 409
        
        # Create user
        password_hash = hash_password(password)
        user = user_model.create(
            email=email,
            password_hash=password_hash,
            role=role,
            name=name
        )
        
        # Create profile
        profile = profile_model.create(user.get('id'), role)
        
        # Store in session
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

@auth_bp.route('/login', methods=['POST'])
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
        
        # Find user
        user = user_model.get_by_email(email)
        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Verify password
        if not verify_password(password, user.get('password_hash', '')):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Store in session
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

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout user"""
    session.clear()
    return jsonify({'message': 'Logout successful'}), 200

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """Get current logged-in user"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session.get('user_id')
    user = user_model.get_by_id(user_id)
    
    if not user:
        session.clear()
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'user': {
            'id': user.get('id'),
            'email': user.get('email'),
            'name': user.get('name'),
            'role': user.get('role')
        }
    }), 200

@auth_bp.route('/check', methods=['GET'])
def check_auth():
    """Check if user is authenticated"""
    is_authenticated = 'user_id' in session
    return jsonify({
        'authenticated': is_authenticated,
        'user_id': session.get('user_id') if is_authenticated else None,
        'role': session.get('role') if is_authenticated else None
    }), 200
