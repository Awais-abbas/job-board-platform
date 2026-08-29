"""
MongoDB Atlas Database Connection for ONJOB Platform
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import os
from functools import wraps

# Global database instance
_db = None
_client = None

def get_mongodb_uri():
    """Get MongoDB URI from environment variable"""
    uri = os.environ.get('MONGODB_URI')
    if not uri:
        # Default to local MongoDB for development
        uri = 'mongodb://localhost:27017/onjob'
    return uri

def init_db():
    """Initialize database connection"""
    global _db, _client
    
    try:
        uri = get_mongodb_uri()
        
        print(f"   Connecting to MongoDB Atlas...")
        
        # Simple connection without custom SRV conversion
        # Let pymongo handle the SRV resolution automatically
        client_options = {
            'serverSelectionTimeoutMS': 30000,  # 30 seconds
            'connectTimeoutMS': 30000,
            'socketTimeoutMS': 30000,
            'retryWrites': True,
            'w': 'majority'
        }
        
        _client = MongoClient(uri, **client_options)
        
        # Test connection
        _client.admin.command('ping')
        print("   ✅ MongoDB ping successful!")
        
        # Get database name from URI or use default
        db_name = os.environ.get('MONGODB_DB_NAME', 'onjob')
        _db = _client[db_name]
        
        # Test database access
        _db.list_collection_names()
        print(f"   ✅ Connected to database: {db_name}")
        
        # Create indexes
        try:
            from app.models.mongodb_models import create_indexes
            create_indexes(_db)
            print("   ✅ Database indexes created successfully")
        except Exception as index_error:
            print(f"   ⚠️  Index creation warning: {index_error}")
        
        print(f"✅ Successfully connected to MongoDB Atlas: {db_name}")
        return _db
        
    except ConnectionFailure as e:
        print(f"❌ MongoDB Connection Failed: {e}")
        print("   Falling back to local JSON storage")
        return None
    except ServerSelectionTimeoutError as e:
        print(f"❌ MongoDB Server Selection Timeout: {e}")
        print("   Possible solutions:")
        print("      1. Check your internet connection")
        print("      2. Whitelist your IP in MongoDB Atlas (0.0.0.0/0)")
        print("      3. Check if cluster name is correct")
        print("   Falling back to local JSON storage")
        return None
    except Exception as e:
        print(f"❌ MongoDB Error: {e}")
        print("   Falling back to local JSON storage")
        return None

def get_db():
    """Get database instance"""
    global _db
    if _db is None:
        _db = init_db()
    return _db

def get_collections():
    """Get all database collections"""
    db = get_db()
    if db is None:
        return None
    
    return {
        'users': db.users,
        'jobs': db.jobs,
        'applications': db.applications,
        'profiles': db.profiles,
        'resumes': db.resumes
    }

def close_db():
    """Close database connection"""
    global _client
    if _client:
        _client.close()
        print("🔌 MongoDB connection closed")

# Collection references - FIXED for PyMongo 4.0+
def get_users_collection():
    """Get users collection"""
    db = get_db()
    if db is None:
        return None
    return db.users

def get_jobs_collection():
    """Get jobs collection"""
    db = get_db()
    if db is None:
        return None
    return db.jobs

def get_applications_collection():
    """Get applications collection"""
    db = get_db()
    if db is None:
        return None
    return db.applications

def get_profiles_collection():
    """Get profiles collection"""
    db = get_db()
    if db is None:
        return None
    return db.profiles

def get_resumes_collection():
    """Get resumes collection"""
    db = get_db()
    if db is None:
        return None
    return db.resumes

# Health check
def check_db_health():
    """Check database connection health"""
    try:
        db = get_db()
        if db is None:
            return {'status': 'disconnected', 'mode': 'json_fallback'}
        
        # Ping the database
        _client.admin.command('ping')
        
        return {
            'status': 'connected',
            'mode': 'mongodb_atlas',
            'database': db.name
        }
    except Exception as e:
        return {
            'status': 'error',
            'mode': 'json_fallback',
            'error': str(e)
        }