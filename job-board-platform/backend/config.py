# Configuration for Job Board Platform

import os
from datetime import timedelta

class Config:
    """Base configuration"""
    # Flask settings
    DEBUG = False
    TESTING = False
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')
    
    # Upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt'}
    
    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False  # Set True for HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # CORS settings
    CORS_ALLOW_ORIGINS = "*"
    CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    
    # App settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # MongoDB Atlas Configuration
    # Replace with your actual MongoDB Atlas URI
    MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/onjob')
    MONGODB_DB_NAME = os.environ.get('MONGODB_DB_NAME', 'onjob')
    USE_MONGODB = os.environ.get('USE_MONGODB', 'false').lower() == 'true'
    
    # Dataset paths (fallback if MongoDB not available)
    USERS_DATA_FILE = os.path.join(DATA_DIR, 'users.json')
    JOBS_DATA_FILE = os.path.join(DATA_DIR, 'jobs.json')
    APPLICATIONS_DATA_FILE = os.path.join(DATA_DIR, 'applications.json')
    PROFILES_DATA_FILE = os.path.join(DATA_DIR, 'profiles.json')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True

# Load configuration based on environment
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    env = os.environ.get('FLASK_ENV', 'development')
    return config_by_name.get(env, DevelopmentConfig)
