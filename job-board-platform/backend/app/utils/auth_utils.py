"""
Authentication utilities
"""

import hashlib
import secrets
from typing import Tuple
import re

def hash_password(password: str) -> str:
    """Hash password with salt"""
    salt = secrets.token_hex(16)
    hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return f"{salt}${hash_obj.hex()}"

def verify_password(password: str, password_hash: str) -> bool:
    """Verify password against hash"""
    try:
        salt, hash_value = password_hash.split('$')
        hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return hash_obj.hex() == hash_value
    except:
        return False

def is_valid_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_strong_password(password: str) -> Tuple[bool, str]:
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one digit"
    return True, "Password is strong"

def validate_registration_data(email: str, password: str, name: str, role: str) -> Tuple[bool, str]:
    """Validate registration data"""
    if not email or not is_valid_email(email):
        return False, "Invalid email address"
    
    if not name or len(name.strip()) < 2:
        return False, "Name must be at least 2 characters"
    
    is_strong, msg = is_strong_password(password)
    if not is_strong:
        return False, msg
    
    if role not in ['job_seeker', 'recruiter']:
        return False, "Invalid role"
    
    return True, "Valid"
