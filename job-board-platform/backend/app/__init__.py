"""
Job Board Platform Backend Application Factory
"""

from flask import Flask
from flask_cors import CORS
from config import get_config
from database import init_db, check_db_health
import os
import json

def create_app():
    """Application factory function"""
    app = Flask(__name__)
    
    # Load configuration
    config = get_config()
    app.config.from_object(config)
    
    # Enable CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": ["*"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })
    
    # Create necessary directories
    os.makedirs(app.config['DATA_DIR'], exist_ok=True)
    os.makedirs(app.config['UPLOAD_DIR'], exist_ok=True)
    
    # Initialize MongoDB (if enabled)
    db = None
    if app.config.get('USE_MONGODB'):
        with app.app_context():
            db = init_db()
            if db is not None:
                app.mongodb = db
                print("MongoDB initialized successfully")
            else:
                print("Using JSON file storage as fallback")
                _initialize_data_files(app)
    else:
        _initialize_data_files(app)
        print("Using JSON file storage (set USE_MONGODB=true to use MongoDB)")
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.auth_mongodb import auth_mongodb_bp
    from app.routes.users import users_bp
    from app.routes.jobs import jobs_bp
    from app.routes.applications import applications_bp
    from app.routes.recommendations import recommendations_bp
    
    # Register auth routes (MongoDB version takes precedence if enabled)
    if db is not None:
        app.register_blueprint(auth_mongodb_bp, url_prefix='/api/auth')
        print("Using MongoDB auth routes")
    else:
        app.register_blueprint(auth_bp, url_prefix='/api/auth')
        print("Using JSON file auth routes")
    
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(jobs_bp, url_prefix='/api/jobs')
    app.register_blueprint(applications_bp, url_prefix='/api/applications')
    app.register_blueprint(recommendations_bp, url_prefix='/api/recommendations')
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health():
        db_health = check_db_health()
        return {
            'status': 'ok',
            'database': db_health,
            'mode': 'mongodb' if db is not None else 'json_files'
        }, 200
    
    # Database info endpoint
    @app.route('/api/db-info', methods=['GET'])
    def db_info():
        if db is not None:
            collections = db.list_collection_names()
            return {
                'database': db.name,
                'collections': collections,
                'collection_count': len(collections)
            }, 200
        return {'database': 'json_files', 'message': 'Using file-based storage'}, 200
    
    return app

def _initialize_data_files(app):
    """Initialize JSON data files if they don't exist"""
    data_files = {
        app.config['USERS_DATA_FILE']: {
            'users': [],
            'last_id': 0
        },
        app.config['JOBS_DATA_FILE']: {
            'jobs': [],
            'last_id': 0
        },
        app.config['APPLICATIONS_DATA_FILE']: {
            'applications': [],
            'last_id': 0
        },
        app.config['PROFILES_DATA_FILE']: {
            'profiles': [],
            'last_id': 0
        }
    }
    
    for file_path, default_data in data_files.items():
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump(default_data, f, indent=2)
