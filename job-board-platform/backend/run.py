"""
Main Flask application entry point
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

if __name__ == '__main__':
    app = create_app()
    
    # Development settings
    ENV = os.environ.get('FLASK_ENV', 'development')
    DEBUG = ENV == 'development'
    PORT = int(os.environ.get('FLASK_PORT', 5000))
    HOST = os.environ.get('FLASK_HOST', '127.0.0.1')
    
    print(f"Starting Job Board Platform API...")
    print(f"Environment: {ENV}")
    print(f"Server: http://{HOST}:{PORT}")
    print(f"API Docs will be available at http://{HOST}:{PORT}/api/health")
    
    app.run(host=HOST, port=PORT, debug=DEBUG)
